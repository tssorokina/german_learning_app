"""
German Verb-End Torture Chamber — Sentence Bank & Generator.

Generates sentences with subordinate/nested clauses where verbs must go to the end.
Covers A2 → C1 progression with increasing complexity.

Verb-end rules tested:
1. Simple subordinate (dass, weil, obwohl, wenn, als, ob, damit, bevor, nachdem, während)
2. Relative clauses (der/die/das + verb at end)
3. Nested subordinate clauses (clause within clause)
4. Compound verb forms at clause end (hat ... gemacht, wird ... können)
5. Separable verbs in subordinate clauses (ankommt, aufsteht)
6. Double infinitive (hat ... lesen wollen)
7. Multiple nested clauses with correct verb stacking
"""

import random
import logging

from exercises.verb_position import VERB_POSITION_BANK

logger = logging.getLogger(__name__)

# The live sentence bank — starts with the hardcoded exercises from the
# exercises/ package and can be extended at runtime with API-generated ones.
SENTENCE_BANK = list(VERB_POSITION_BANK)


def _compute_positions(text, verbs):
    """Compute word-level positions of verbs in the sentence."""
    words = text.split()
    positions = []
    used_positions = set()
    for verb in verbs:
        for i, word in enumerate(words):
            # Strip punctuation for matching
            clean = word.strip(".,;:!?\"'()[]{}–—")
            if clean == verb and i not in used_positions:
                positions.append(i)
                used_positions.add(i)
                break
    return positions


def _create_display_text(text, verbs):
    """Create display text with verb slots marked as ___."""
    words = text.split()
    display_words = list(words)
    used_positions = set()
    for verb in verbs:
        for i, word in enumerate(words):
            clean = word.strip(".,;:!?\"'()[]{}–—")
            if clean == verb and i not in used_positions:
                # Preserve punctuation
                suffix = ""
                for ch in reversed(word):
                    if ch in ".,;:!?\"'()[]{}–—":
                        suffix = ch + suffix
                    else:
                        break
                display_words[i] = "___" + suffix
                used_positions.add(i)
                break
    return " ".join(display_words)


def prepare_exercise(template):
    """Prepare a template into an exercise dict ready for the frontend.

    Full-sentence mode: ALL words become slots and chips.
    The user must reconstruct the entire sentence.
    """
    text = template["text"]
    verbs = template["verbs"]
    verb_positions = _compute_positions(text, verbs)

    words = text.split()

    # Build all_slots: every word is a slot
    all_slots = []
    for i, w in enumerate(words):
        clean = w.strip(".,;:!?\"'()[]{}–—")
        suffix = ""
        for ch in reversed(w):
            if ch in ".,;:!?\"'()[]{}–—":
                suffix = ch + suffix
            else:
                break
        all_slots.append({
            "index": i,
            "correct_word": clean,
            "suffix": suffix,
            "is_verb": i in verb_positions
        })

    # Build verb_slots for error analysis (backward compat with error_analyzer)
    verb_slots = []
    for s in all_slots:
        if s["is_verb"]:
            verb_slots.append({
                "index": s["index"],
                "correct_verb": s["correct_word"],
                "suffix": s["suffix"]
            })

    # Shuffled words for the tray (clean, no punctuation)
    shuffled_words = [s["correct_word"] for s in all_slots]
    random.shuffle(shuffled_words)

    return {
        "template_id": template["id"],
        "full_text": text,
        "words": words,
        "all_slots": all_slots,
        "verb_slots": verb_slots,
        "verb_positions": verb_positions,
        "shuffled_words": shuffled_words,
        "clause_type": template["clause_type"],
        "difficulty": template["difficulty"],
        "explanation": template["explanation"],
        # Keep legacy fields for error analyzer
        "slots": verb_slots,
        "verbs": verbs,
        "positions": verb_positions
    }


def load_generated_verb_sentences(generated):
    """Add generated verb-position sentences to the bank.

    Args:
        generated: list of sentence dicts with keys: id, text, verbs,
                   clause_type, difficulty, explanation
    """
    if generated:
        # Add generated sentences alongside the hardcoded ones
        SENTENCE_BANK.extend(generated)
        logger.info(f"Added {len(generated)} generated verb-position sentences "
                    f"(total: {len(SENTENCE_BANK)})")


def get_exercise_by_difficulty(difficulty=None, exclude_ids=None):
    """Get a random exercise, optionally filtered by difficulty."""
    pool = SENTENCE_BANK
    if difficulty is not None:
        pool = [s for s in pool if s["difficulty"] == difficulty]
    if exclude_ids:
        pool = [s for s in pool if s["id"] not in exclude_ids]
    if not pool:
        return None
    template = random.choice(pool)
    return prepare_exercise(template)


def get_template_by_id(template_id):
    """Get a specific template by ID."""
    for t in SENTENCE_BANK:
        if t["id"] == template_id:
            return t
    return None


def get_all_template_ids():
    return [t["id"] for t in SENTENCE_BANK]


def get_daily_sentence():
    """Pick a sentence suitable for the daily iMessage motivation."""
    # Prefer medium difficulty for daily messages
    pool = [s for s in SENTENCE_BANK if s["difficulty"] in (2, 3)]
    if not pool:
        pool = SENTENCE_BANK
    template = random.choice(pool)
    return template


def count_by_difficulty():
    counts = {}
    for t in SENTENCE_BANK:
        d = t["difficulty"]
        counts[d] = counts.get(d, 0) + 1
    return counts
