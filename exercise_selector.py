"""
Exercise Selector — adaptive exercise sequencing.

Replaces random.choice with a multi-strategy priority cascade:
1. Active micro-curriculum session (highest priority)
2. Confusion-set interleaving
3. Transfer chain progression
4. SM-2 spaced repetition review
5. Random fallback (existing behavior)
"""
import random
import logging

from grammar_exercises import get_exercises_by_module, get_exercise_by_id
from micro_curricula import get_current_step, get_curriculum_info, MICRO_CURRICULA
from confusion_sets import (CONFUSION_SETS, get_confusion_sets_for_errors,
                            get_next_side, get_confusion_set_info)
from database import (get_active_micro_session, get_grammar_rules_due,
                      get_confusion_set_states, get_recent_error_categories,
                      get_transfer_progress, get_all_transfer_progress,
                      get_mastered_exercise_ids, get_attempted_exercise_ids,
                      get_failed_exercise_topics, schedule_retry)

logger = logging.getLogger(__name__)


def select_exercise(user_token, module_key=None, level=None, skip_micro=False):
    """
    Select the next exercise for a user using the priority cascade.

    Returns dict with:
      - exercise: the exercise dict (or micro_step pseudo-exercise)
      - context: metadata about why this exercise was chosen
    Returns None if no exercises available.
    """

    # Priority 1: Active micro-curriculum
    if not skip_micro:
        result = _try_micro_curriculum(user_token, module_key)
        if result:
            return result

    # Priority 2: Confusion-set interleaving
    result = _try_confusion_interleave(user_token, module_key, level)
    if result:
        return result

    # Priority 3: Transfer chain
    result = _try_transfer_chain(user_token, module_key, level)
    if result:
        return result

    # Priority 4: SM-2 review
    result = _try_sm2_review(user_token, module_key)
    if result:
        return result

    # Priority 5: Reinforcement of recent errors (2-3 exercises on same topic)
    result = _try_error_reinforcement(user_token, module_key, level)
    if result:
        return result

    # Priority 6: Smart fallback — prefer unseen exercises, skip mastered ones
    result = _try_smart_fallback(user_token, module_key, level)
    if result:
        return result

    return None


def _try_micro_curriculum(user_token, module_key):
    """Check for active micro-curriculum and serve next step."""
    session = get_active_micro_session(user_token)
    if not session:
        return None

    step = get_current_step(session)
    if not step:
        return None

    curriculum_info = get_curriculum_info(session["curriculum_key"])

    # Study steps (minimal_pair, matrix_display) -> serve as micro_step
    if step["type"] in ("minimal_pair", "matrix_display", "far_transfer"):
        return {
            "exercise": {
                "type": "micro_step",
                "step_data": step,
                "id": f"micro_{step['type']}_{session['current_step']}"
            },
            "context": {
                "source": "micro_curriculum",
                "session_id": session["id"],
                "step": session["current_step"],
                "total_steps": session["total_steps"],
                "step_type": step["type"],
                "curriculum_name": curriculum_info.get("name", ""),
                "module_key": module_key
            }
        }

    # Drill steps -> resolve to an actual exercise from the bank
    exercise = _resolve_drill_step(step, module_key)
    if exercise:
        return {
            "exercise": exercise,
            "context": {
                "source": "micro_curriculum",
                "session_id": session["id"],
                "step": session["current_step"],
                "total_steps": session["total_steps"],
                "step_type": step["type"],
                "curriculum_name": curriculum_info.get("name", ""),
                "module_key": module_key
            }
        }

    return None


def _resolve_drill_step(step, fallback_module):
    """Resolve a drill/discrimination/transfer step to an exercise from the bank."""
    filt = step.get("filter", {})
    mod = filt.get("module", fallback_module)
    if not mod:
        return None

    exercises = get_exercises_by_module(mod)

    # Apply topic filter
    if "topic" in filt:
        filtered = [e for e in exercises if e.get("topic") == filt["topic"]]
        if filtered:
            exercises = filtered

    # Apply topic_contains filter
    if "topic_contains" in filt:
        filtered = [e for e in exercises
                    if filt["topic_contains"] in (e.get("topic") or "")]
        if filtered:
            exercises = filtered

    # Apply clause_type_contains filter (for verb_position exercises)
    if "clause_type_contains" in filt:
        filtered = [e for e in exercises
                    if filt["clause_type_contains"] in (e.get("clause_type") or "")
                    or filt["clause_type_contains"] in (e.get("topic") or "")]
        if filtered:
            exercises = filtered

    if exercises:
        return random.choice(exercises)
    return None


def _try_confusion_interleave(user_token, module_key, level):
    """Serve an exercise from a confusion set if the user has relevant errors."""
    recent_errors = get_recent_error_categories(user_token, limit=5)
    if not recent_errors:
        return None

    relevant_sets = get_confusion_sets_for_errors(recent_errors)
    if not relevant_sets:
        return None

    # Get confusion set state to determine position in interleave pattern
    states = get_confusion_set_states(user_token)

    for set_key in relevant_sets:
        state = states.get(set_key)
        current_index = state["times_tested"] if state else 0

        side = get_next_side(set_key, current_index)
        if not side:
            continue

        # Check if the side's module matches the requested module (if specified)
        side_module = side["filter"].get("module")
        if module_key and side_module != module_key:
            continue

        exercises = get_exercises_by_module(side_module, level=level)

        # Apply topic filter from side
        topic = side["filter"].get("topic")
        topic_contains = side["filter"].get("topic_contains")
        if topic:
            filtered = [e for e in exercises if e.get("topic") == topic]
            if filtered:
                exercises = filtered
        elif topic_contains:
            filtered = [e for e in exercises
                        if topic_contains in (e.get("topic") or "")]
            if filtered:
                exercises = filtered

        if exercises:
            info = get_confusion_set_info(set_key)
            return {
                "exercise": random.choice(exercises),
                "context": {
                    "source": "confusion_set",
                    "confusion_set_key": set_key,
                    "confusion_set_name": info["name"] if info else "",
                    "side_label": side["label"]
                }
            }

    return None


def _try_transfer_chain(user_token, module_key, level):
    """Serve an exercise based on transfer chain progression."""
    if not module_key:
        return None

    progress_list = get_all_transfer_progress(user_token)
    if not progress_list:
        return None

    from datetime import datetime
    now = datetime.now()

    for progress in progress_list:
        if progress["module"] != module_key:
            continue

        stage = progress["current_stage"]

        # Delayed transfer: only serve if review is due
        if stage == "delayed" and progress.get("next_delayed_review"):
            try:
                review_time = datetime.fromisoformat(progress["next_delayed_review"])
                if review_time > now:
                    continue
            except (ValueError, TypeError):
                continue

        # Far transfer: serve a writing prompt
        if stage == "far":
            from transfer_chain import get_far_transfer_prompt
            prompt = get_far_transfer_prompt(module_key)
            if prompt:
                return {
                    "exercise": {
                        "type": "micro_step",
                        "step_data": {
                            "type": "far_transfer",
                            "instruction": "Free Writing Exercise",
                            "prompt": prompt
                        },
                        "id": f"far_transfer_{progress['rule_id']}"
                    },
                    "context": {
                        "source": "transfer_chain",
                        "stage": "far",
                        "rule_id": progress["rule_id"],
                        "module_key": module_key
                    }
                }

        # Near/delayed transfer: serve an exercise from the topic
        if stage in ("near", "delayed"):
            exercises = get_exercises_by_module(module_key, level=level)
            topic_exercises = [e for e in exercises
                               if e.get("topic") == progress["rule_id"]]
            if topic_exercises:
                return {
                    "exercise": random.choice(topic_exercises),
                    "context": {
                        "source": "transfer_chain",
                        "stage": stage,
                        "rule_id": progress["rule_id"],
                        "module_key": module_key
                    }
                }

    return None


def _try_sm2_review(user_token, module_key):
    """Serve an exercise due for SM-2 spaced repetition review."""
    due_rules = get_grammar_rules_due(user_token, module=module_key)
    if not due_rules:
        return None

    rule = due_rules[0]
    exercises = get_exercises_by_module(rule["module"])
    topic_exercises = [e for e in exercises if e.get("topic") == rule["rule_id"]]
    if topic_exercises:
        return {
            "exercise": random.choice(topic_exercises),
            "context": {
                "source": "sm2_review",
                "rule_id": rule["rule_id"],
                "module": rule["module"]
            }
        }

    # Fallback: any exercise from the module
    if exercises:
        return {
            "exercise": random.choice(exercises),
            "context": {
                "source": "sm2_review",
                "rule_id": rule["rule_id"],
                "module": rule["module"]
            }
        }

    return None


def _try_error_reinforcement(user_token, module_key, level):
    """After a mistake, serve 2-3 exercises on the same topic/rule.

    Looks at the user's most recent failures and picks exercises with
    matching topics so the user practices the same grammar pattern.
    """
    if not module_key:
        return None

    failed_topics = get_failed_exercise_topics(user_token, module=module_key, limit=3)
    if not failed_topics:
        return None

    exercises = get_exercises_by_module(module_key, level=level)
    if not exercises:
        return None

    mastered = get_mastered_exercise_ids(user_token, module=module_key)

    for topic in failed_topics:
        # Find exercises with the same topic that are NOT already mastered
        topic_exercises = [
            e for e in exercises
            if e.get("topic") == topic and e["id"] not in mastered
        ]
        if topic_exercises:
            chosen = random.choice(topic_exercises)
            logger.info(f"Reinforcement: serving {chosen['id']} for failed topic '{topic}'")
            return {
                "exercise": chosen,
                "context": {
                    "source": "error_reinforcement",
                    "reinforced_topic": topic
                }
            }

    return None


def _try_smart_fallback(user_token, module_key, level):
    """Smart fallback: prefer unseen exercises, skip mastered ones.

    Priority order:
    1. Exercises the user has never seen
    2. Exercises the user has seen but failed (and aren't in retry queue)
    3. All exercises (only if everything else is exhausted)
    """
    exercises = get_exercises_by_module(module_key, level=level) if module_key else []
    if not exercises:
        return None

    mastered = get_mastered_exercise_ids(user_token, module=module_key)
    attempted = get_attempted_exercise_ids(user_token, module=module_key)

    # Tier 1: Never-seen exercises
    unseen = [e for e in exercises if e["id"] not in attempted]
    if unseen:
        chosen = random.choice(unseen)
        logger.info(f"Smart fallback: serving unseen exercise {chosen['id']}")
        return {
            "exercise": chosen,
            "context": {"source": "unseen"}
        }

    # Tier 2: Previously failed (not yet mastered) exercises
    failed = [e for e in exercises if e["id"] not in mastered]
    if failed:
        chosen = random.choice(failed)
        logger.info(f"Smart fallback: serving previously-failed exercise {chosen['id']}")
        return {
            "exercise": chosen,
            "context": {"source": "retry_failed"}
        }

    # Tier 3: All exercises (user has mastered everything — cycle back)
    chosen = random.choice(exercises)
    logger.info(f"Smart fallback: all mastered, cycling exercise {chosen['id']}")
    return {
        "exercise": chosen,
        "context": {"source": "random"}
    }
