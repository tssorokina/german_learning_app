"""
German Grammar Torture Chamber — Flask Web Application.

A German grammar trainer with multiple exercise modules:
- Verb placement (reconstruction)
- Adjective declension (gap-fill)
- Connectors & word order (reconstruction)
- Passive voice (transformation)
- Konjunktiv (reconstruction + gap-fill)
- Relative clauses (reconstruction)
- Prepositions & cases (quick-select)
- Nominalization (transformation)
"""
import os
import json
import random
import secrets
import logging
from datetime import date, datetime
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import (Flask, render_template, request, jsonify, session,
                   redirect, url_for, abort, flash)

from database import (init_db, get_or_create_user, get_retry_template,
                      mark_sentence_shown, record_attempt,
                      log_error, schedule_retry, complete_retry, get_error_stats,
                      get_recent_attempts, get_accuracy_over_time, get_user_summary,
                      store_daily_message, get_daily_message, mark_daily_sent,
                      save_word, get_saved_words, delete_saved_word,
                      update_grammar_rule, get_module_stats,
                      get_active_micro_session, create_micro_session,
                      advance_micro_session, abandon_micro_session,
                      record_exercise_timing, update_transfer_progress,
                      promote_transfer_stage, update_confusion_set_state,
                      get_delayed_retention, get_transfer_scores,
                      get_fluency_score, get_confidence_calibration,
                      get_scaffold_dependence, get_all_transfer_progress,
                      register_user, authenticate_user, get_user_by_token,
                      merge_anonymous_into_user)
from sentences import (get_exercise_by_difficulty, prepare_exercise,
                       get_template_by_id, get_daily_sentence, SENTENCE_BANK,
                       count_by_difficulty, load_generated_verb_sentences)
from error_analyzer import (analyze_errors, analyze_gap_fill_errors,
                            analyze_quick_select_errors, get_error_explanation,
                            get_all_categories, ERROR_CATEGORIES)
from exercise_types import GRAMMAR_MODULES, EXERCISE_TYPES
from exercise_selector import select_exercise
from micro_curricula import get_curriculum_for_error, get_current_step, MICRO_CURRICULA
from transfer_chain import check_promotion, get_far_transfer_prompt
from confusion_sets import get_confusion_sets_for_errors
from grammar_exercises import (get_exercises_by_module, get_exercise_by_id,
                               count_by_module_and_level, ALL_GRAMMAR_EXERCISES,
                               load_generated_exercises)
from generate_exercises import refresh_exercise_banks

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Auth token for API / notification endpoints
API_TOKEN = os.environ.get("API_TOKEN", secrets.token_hex(16))

# ─── EXERCISE GENERATION ON STARTUP ─────────────────────────────────
logging.basicConfig(level=logging.INFO)

def _init_exercises():
    """Generate or load exercises from cache on startup."""
    try:
        verb_sentences, grammar_exs = refresh_exercise_banks()
        if verb_sentences:
            load_generated_verb_sentences(verb_sentences)
        if grammar_exs:
            load_generated_exercises(grammar_exs)
    except Exception as e:
        logger.error(f"Exercise generation failed, using fallback: {e}")

_init_exercises()


def get_user_token():
    """Get or create a persistent user token in the session.

    If a user is logged in, their registered token is used.
    Otherwise, an anonymous session token is created.
    """
    if "user_token" not in session:
        session["user_token"] = secrets.token_hex(8)
        session.permanent = True
    get_or_create_user(session["user_token"])
    return session["user_token"]


def get_current_user():
    """Return the current user dict if logged in, else None."""
    token = session.get("user_token")
    if not token:
        return None
    user = get_user_by_token(token)
    if user and user.get("email"):
        return user
    return None


def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            token = request.args.get("token", "")
        if token != API_TOKEN:
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# ─── INIT ──────────────────────────────────────────────────────────────
@app.before_request
def ensure_db():
    init_db()


@app.context_processor
def inject_user():
    """Make current_user available in all templates."""
    return {"current_user": get_current_user()}


# ─── AUTHENTICATION ROUTES ─────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if get_current_user():
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        display_name = request.form.get("display_name", "").strip()

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("register.html")
        if password != password2:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        # Remember the anonymous token so we can merge progress
        anon_token = session.get("user_token")

        user, error = register_user(email, password, display_name or None)
        if error:
            flash(error, "error")
            return render_template("register.html")

        # Merge any anonymous learning progress into the new account
        if anon_token and anon_token != user["token"]:
            merge_anonymous_into_user(anon_token, user["token"])

        session["user_token"] = user["token"]
        session.permanent = True
        flash("Account created! Your learning progress is now saved.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user():
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = authenticate_user(email, password)
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        # Merge any anonymous progress accumulated before login
        anon_token = session.get("user_token")
        if anon_token and anon_token != user["token"]:
            merge_anonymous_into_user(anon_token, user["token"])

        session["user_token"] = user["token"]
        session.permanent = True
        flash("Welcome back!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


# ─── WEB ROUTES ────────────────────────────────────────────────────────

@app.route("/")
def index():
    token = get_user_token()
    summary = get_user_summary(token)
    module_stats = get_module_stats(token)
    module_counts = count_by_module_and_level()

    # Build stats lookup {module: {total, correct}}
    stats_by_module = {}
    for s in module_stats:
        mod = s["module"]
        if mod not in stats_by_module:
            stats_by_module[mod] = {"total": 0, "correct": 0}
        stats_by_module[mod]["total"] += s["total"]
        stats_by_module[mod]["correct"] += (s["correct_count"] or 0)

    return render_template("index.html",
                           summary=summary,
                           modules=GRAMMAR_MODULES,
                           module_counts=module_counts,
                           stats_by_module=stats_by_module)


@app.route("/exercise")
def exercise_page():
    token = get_user_token()
    difficulty = request.args.get("difficulty", type=int)

    # First check retry queue
    retry = get_retry_template(token)
    exercise = None
    retry_id = None

    if retry and not request.args.get("skip_retry"):
        template = get_template_by_id(retry.get("template_id", ""))
        if template:
            exercise = prepare_exercise(template)
            retry_id = retry.get("retry_id")

    if not exercise:
        # Smart selection: prefer unseen, then failed, then any
        exercise = get_exercise_by_difficulty(difficulty, user_token=token)

    if not exercise:
        return render_template("no_exercises.html")

    mark_sentence_shown(token, exercise["template_id"])

    # Build safe exercise data for the frontend (don't leak correct answers)
    safe_exercise = {
        "template_id": exercise["template_id"],
        "num_slots": len(exercise["all_slots"]),
        "slot_suffixes": [s["suffix"] for s in exercise["all_slots"]],
        "verb_indices": exercise["verb_positions"],
        "shuffled_words": exercise["shuffled_words"],
        "clause_type": exercise["clause_type"],
        "difficulty": exercise["difficulty"],
        "english": exercise.get("english", ""),
    }

    return render_template("exercise.html",
                           exercise=json.dumps(safe_exercise),
                           retry_id=retry_id,
                           difficulty_label=_diff_label(exercise["difficulty"]))


# ─── MODULE-BASED EXERCISE ROUTES ─────────────────────────────────────

@app.route("/grammar")
def grammar_index():
    """Grammar modules overview page."""
    token = get_user_token()
    summary = get_user_summary(token)
    module_stats = get_module_stats(token)
    module_counts = count_by_module_and_level()

    stats_by_module = {}
    for s in module_stats:
        mod = s["module"]
        if mod not in stats_by_module:
            stats_by_module[mod] = {"total": 0, "correct": 0}
        stats_by_module[mod]["total"] += s["total"]
        stats_by_module[mod]["correct"] += (s["correct_count"] or 0)

    return render_template("grammar_index.html",
                           modules=GRAMMAR_MODULES,
                           module_counts=module_counts,
                           stats_by_module=stats_by_module,
                           summary=summary)


@app.route("/grammar/<module_key>")
def grammar_exercise(module_key):
    """Serve a grammar exercise for a specific module."""
    token = get_user_token()
    module_info = GRAMMAR_MODULES.get(module_key)
    if not module_info:
        abort(404)

    level = request.args.get("level", type=int)
    skip_micro = request.args.get("skip_micro", type=int, default=0)

    # Use adaptive exercise selector
    result = select_exercise(token, module_key, level, skip_micro=bool(skip_micro))

    if not result:
        return render_template("no_exercises.html")

    ex = result["exercise"]
    context = result["context"]

    # Handle micro-curriculum study steps (minimal_pair, matrix_display, far_transfer)
    if ex.get("type") == "micro_step":
        curriculum_name = context.get("curriculum_name", "")
        return render_template("micro_step.html",
                               step=json.dumps(ex["step_data"]),
                               context=json.dumps({
                                   "session_id": context.get("session_id"),
                                   "module_key": module_key
                               }),
                               curriculum_name=curriculum_name,
                               current_step=context.get("step", 0),
                               total_steps=context.get("total_steps", 1),
                               module_name=module_info["name"],
                               module_key=module_key)

    exercise_type = ex["type"]

    # Route to the correct template based on exercise type
    if exercise_type == "gap_fill":
        return _serve_gap_fill(ex, module_key, module_info, context)
    elif exercise_type == "transformation":
        return _serve_transformation(ex, module_key, module_info, context)
    elif exercise_type == "quick_select":
        return _serve_quick_select(ex, module_key, module_info, context)
    else:
        # reconstruction — use existing engine via prepare_exercise
        return _serve_reconstruction(ex, module_key, module_info, token, context)


def _serve_gap_fill(ex, module_key, module_info, context=None):
    """Serve a gap-fill exercise."""
    safe_data = {
        "exercise_id": ex["id"],
        "module": module_key,
        "type": "gap_fill",
        "level": ex["level"],
        "topic": ex["topic"],
        "sentence_template": ex["data"]["sentence_template"],
        "gaps": [{
            "position": g["position"],
            "context": g.get("context", ""),
            "options": g["options"],
            "indicative_hint": g.get("indicative_hint", "")
        } for g in ex["data"]["gaps"]],
        "grammar_tip": ex.get("grammar_tip", ""),
        "english": ex["data"].get("english", ""),
    }
    return render_template("gap_fill.html",
                           exercise=json.dumps(safe_data),
                           exercise_context=context,
                           module_name=module_info["name"],
                           module_key=module_key,
                           difficulty_label=_diff_label(ex["level"]))


def _serve_transformation(ex, module_key, module_info, context=None):
    """Serve a transformation exercise."""
    words = list(ex["data"]["target_words"])
    random.shuffle(words)
    safe_data = {
        "exercise_id": ex["id"],
        "module": module_key,
        "type": "transformation",
        "level": ex["level"],
        "topic": ex["topic"],
        "source": ex["data"]["source"],
        "shuffled_words": words,
        "num_slots": len(ex["data"]["target_words"]),
        "optional_words": ex["data"].get("optional_words", []),
        "grammar_tip": ex.get("grammar_tip", "")
    }
    return render_template("transformation.html",
                           exercise=json.dumps(safe_data),
                           exercise_context=context,
                           module_name=module_info["name"],
                           module_key=module_key,
                           difficulty_label=_diff_label(ex["level"]))


def _serve_quick_select(ex, module_key, module_info, context=None):
    """Serve a quick-select exercise."""
    safe_data = {
        "exercise_id": ex["id"],
        "module": module_key,
        "type": "quick_select",
        "level": ex["level"],
        "topic": ex["topic"],
        "sentence": ex["data"]["sentence"],
        "gaps": [{
            "position": g["position"],
            "options": g["options"]
        } for g in ex["data"]["gaps"]],
        "grammar_tip": ex.get("grammar_tip", "")
    }
    return render_template("quick_select.html",
                           exercise=json.dumps(safe_data),
                           exercise_context=context,
                           module_name=module_info["name"],
                           module_key=module_key,
                           difficulty_label=_diff_label(ex["level"]))


def _serve_reconstruction(ex, module_key, module_info, token, context=None):
    """Serve a reconstruction exercise for grammar modules."""
    # These exercises have a 'data' dict with text, verbs, clause_type
    # We need to prepare them like the existing sentence bank
    template = {
        "id": ex["id"],
        "text": ex["data"]["text"],
        "english": ex["data"].get("english", ""),
        "verbs": ex["data"]["verbs"],
        "clause_type": ex["data"]["clause_type"],
        "difficulty": ex["level"],
        "explanation": ex["grammar_rule"]
    }
    exercise = prepare_exercise(template)

    mark_sentence_shown(token, exercise["template_id"])

    safe_exercise = {
        "template_id": exercise["template_id"],
        "num_slots": len(exercise["all_slots"]),
        "slot_suffixes": [s["suffix"] for s in exercise["all_slots"]],
        "verb_indices": exercise["verb_positions"],
        "shuffled_words": exercise["shuffled_words"],
        "clause_type": exercise["clause_type"],
        "difficulty": exercise["difficulty"],
        "module": module_key,
        "english": exercise.get("english", ""),
        # Extra info for reconstruction exercises with source sentences
        "sentence_a": ex["data"].get("sentence_a", ""),
        "sentence_b": ex["data"].get("sentence_b", ""),
    }

    return render_template("exercise.html",
                           exercise=json.dumps(safe_exercise),
                           exercise_context=context,
                           retry_id=None,
                           difficulty_label=_diff_label(ex["level"]),
                           module_name=module_info["name"],
                           module_key=module_key)


# ─── MICRO-CURRICULUM & ADAPTIVE ENDPOINTS ───────────────────────────

@app.route("/api/micro_step_complete", methods=["POST"])
def api_micro_step_complete():
    """Advance a micro-curriculum session to the next step."""
    token = get_user_token()
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "no session_id"}), 400

    status = advance_micro_session(session_id)
    return jsonify({"status": status or "error"})


@app.route("/api/micro_session_skip", methods=["POST"])
def api_micro_session_skip():
    """Abandon the active micro-curriculum session."""
    token = get_user_token()
    session = get_active_micro_session(token)
    if session:
        abandon_micro_session(session["id"])
    return jsonify({"status": "skipped"})


def _handle_post_check(token, exercise_id, errors, all_correct, data, module, topic):
    """Common post-check logic: timing, micro-curriculum trigger, transfer tracking."""
    # Record exercise timing
    duration_ms = data.get("duration_ms")
    predicted_correct = data.get("predicted_correct")
    if duration_ms is not None:
        record_exercise_timing(
            token, None, exercise_id, duration_ms,
            input_mode=data.get("input_mode", "chip"),
            predicted_correct=predicted_correct,
            actual_correct=1 if all_correct else 0
        )

    # Trigger micro-curriculum for errors if none is active
    if errors and not get_active_micro_session(token):
        primary_error = errors[0]["category"] if isinstance(errors[0], dict) else errors[0]
        curriculum = get_curriculum_for_error(primary_error)
        if curriculum:
            error_id = None
            create_micro_session(
                token, primary_error, error_id, exercise_id,
                primary_error, len(curriculum["steps"])
            )

    # Advance micro-curriculum if we're in a drill step
    session = get_active_micro_session(token)
    if session and all_correct:
        step = get_current_step(session)
        if step and step["type"] in ("controlled_drill", "discrimination", "transfer"):
            advance_micro_session(session["id"])

    # Update transfer progress
    if topic:
        transfer_stage = data.get("transfer_stage", "controlled")
        update_transfer_progress(token, module, topic, transfer_stage, all_correct)

        # Check for promotion
        from database import get_transfer_progress as get_tp
        progress = get_tp(token, topic)
        if progress:
            new_stage = check_promotion(progress)
            if new_stage:
                promote_transfer_stage(token, topic, new_stage)

    # Update confusion set state if applicable
    if errors:
        error_cats = [e["category"] if isinstance(e, dict) else e for e in errors]
        relevant_sets = get_confusion_sets_for_errors(error_cats)
        for set_key in relevant_sets:
            update_confusion_set_state(token, set_key, all_correct)


# ─── GRAMMAR API ENDPOINTS ────────────────────────────────────────────

@app.route("/api/check_gap", methods=["POST"])
def api_check_gap_fill():
    """Check a gap-fill exercise answer."""
    token = get_user_token()
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    exercise_id = data.get("exercise_id")
    user_answers = data.get("answers", {})

    ex = get_exercise_by_id(exercise_id)
    if not ex:
        return jsonify({"error": "unknown exercise"}), 404

    # Check answers
    errors = analyze_gap_fill_errors(ex["data"], user_answers)
    all_correct = len(errors) == 0

    # Record attempt
    record_attempt(token, exercise_id, user_answers, all_correct,
                   errors if errors else None,
                   module=ex["module"], exercise_type="gap_fill")

    # Update grammar rule tracking
    update_grammar_rule(token, ex["module"], ex["topic"], all_correct)

    # Log errors
    explanations = []
    if errors:
        for err in errors:
            error_id = log_error(token, exercise_id, err["category"], err["detail"])
            schedule_retry(token, exercise_id, error_id, days_delay=2)
            explanations.append(get_error_explanation(err))

    # Adaptive: timing, micro-curriculum, transfer, confusion sets
    _handle_post_check(token, exercise_id, errors, all_correct, data,
                       ex["module"], ex["topic"])

    return jsonify({
        "correct": all_correct,
        "full_sentence": ex["data"].get("full_correct", ""),
        "grammar_rule": ex.get("grammar_rule", ""),
        "grammar_tip": ex.get("grammar_tip", ""),
        "errors": explanations,
        "gap_results": [{
            "position": g["position"],
            "correct_answer": g["answer"],
            "user_answer": user_answers.get(g["position"], ""),
            "is_correct": user_answers.get(g["position"], "") == g["answer"]
        } for g in ex["data"]["gaps"]]
    })


@app.route("/api/check_transformation", methods=["POST"])
def api_check_transformation():
    """Check a transformation exercise answer."""
    token = get_user_token()
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    exercise_id = data.get("exercise_id")
    user_positions = data.get("positions", [])

    ex = get_exercise_by_id(exercise_id)
    if not ex:
        return jsonify({"error": "unknown exercise"}), 404

    correct_words = ex["data"]["target_words"]
    correct_order = ex["data"]["correct_order"]

    # Compare user word order to correct order
    user_words = [p["word"] for p in sorted(user_positions, key=lambda x: x["slot_index"])]

    slot_results = []
    all_correct = True
    for i, correct_word in enumerate(correct_words):
        user_word = user_words[i] if i < len(user_words) else None
        is_correct = (user_word == correct_word)
        if not is_correct:
            all_correct = False
        slot_results.append({
            "index": i,
            "correct_word": correct_word,
            "user_word": user_word,
            "is_correct": is_correct
        })

    # Record attempt
    record_attempt(token, exercise_id, user_positions, all_correct,
                   None, module=ex["module"], exercise_type="transformation")

    # Update grammar rule tracking
    update_grammar_rule(token, ex["module"], ex["topic"], all_correct)

    errors_for_adaptive = []
    if not all_correct:
        error_cat = "wrong_" + ex["module"] + "_form"
        error_id = log_error(token, exercise_id, error_cat,
                            f"Expected: {correct_order}")
        schedule_retry(token, exercise_id, error_id, days_delay=2)
        errors_for_adaptive = [{"category": error_cat}]

    # Adaptive: timing, micro-curriculum, transfer, confusion sets
    _handle_post_check(token, exercise_id, errors_for_adaptive, all_correct, data,
                       ex["module"], ex["topic"])

    return jsonify({
        "correct": all_correct,
        "full_sentence": correct_order,
        "grammar_rule": ex.get("grammar_rule", ""),
        "grammar_tip": ex.get("grammar_tip", ""),
        "errors": [],
        "slot_results": slot_results
    })


@app.route("/api/check_quick_select", methods=["POST"])
def api_check_quick_select():
    """Check a quick-select exercise answer."""
    token = get_user_token()
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    exercise_id = data.get("exercise_id")
    user_answers = data.get("answers", {})

    ex = get_exercise_by_id(exercise_id)
    if not ex:
        return jsonify({"error": "unknown exercise"}), 404

    errors = analyze_quick_select_errors(ex["data"], user_answers)
    all_correct = len(errors) == 0

    # Record attempt
    record_attempt(token, exercise_id, user_answers, all_correct,
                   errors if errors else None,
                   module=ex["module"], exercise_type="quick_select")

    # Update grammar rule tracking
    update_grammar_rule(token, ex["module"], ex["topic"], all_correct)

    explanations = []
    if errors:
        for err in errors:
            error_id = log_error(token, exercise_id, err["category"], err["detail"])
            schedule_retry(token, exercise_id, error_id, days_delay=2)
            explanations.append(get_error_explanation(err))

    # Adaptive: timing, micro-curriculum, transfer, confusion sets
    _handle_post_check(token, exercise_id, errors, all_correct, data,
                       ex["module"], ex["topic"])

    # Build full sentence with correct answers filled in
    full_sentence = ex["data"]["sentence"]
    for gap in ex["data"]["gaps"]:
        full_sentence = full_sentence.replace("{" + gap["position"] + "}", gap["answer"])

    return jsonify({
        "correct": all_correct,
        "full_sentence": full_sentence,
        "grammar_rule": ex.get("grammar_rule", ""),
        "grammar_tip": ex.get("grammar_tip", ""),
        "errors": explanations,
        "gap_results": [{
            "position": g["position"],
            "correct_answer": g["answer"],
            "user_answer": user_answers.get(g["position"], ""),
            "is_correct": user_answers.get(g["position"], "") == g["answer"],
            "explanation": g.get("explanation", "")
        } for g in ex["data"]["gaps"]]
    })


@app.route("/dashboard")
def dashboard():
    token = get_user_token()
    error_stats = get_error_stats(token)
    recent = get_recent_attempts(token, limit=30)
    accuracy = get_accuracy_over_time(token, days=30)
    summary = get_user_summary(token)
    categories = get_all_categories()
    saved_words = get_saved_words(token)

    # Enrich error stats with category info
    for stat in error_stats:
        cat_info = categories.get(stat["error_category"], {})
        stat["name"] = cat_info.get("name_en", stat["error_category"])
        stat["tip"] = cat_info.get("tip", "")

    # Enrich recent attempts with sentence info from the bank
    for r in recent:
        tmpl = get_template_by_id(r.get("template_id", ""))
        if tmpl:
            r["full_text"] = tmpl["text"]
            r["clause_structure"] = tmpl["clause_type"]
        else:
            # Check grammar exercises
            gex = get_exercise_by_id(r.get("template_id", ""))
            if gex:
                r["full_text"] = (gex["data"].get("full_correct")
                                  or gex["data"].get("correct_order")
                                  or gex["data"].get("text", r.get("template_id", "?")))
                r["clause_structure"] = gex.get("topic", "")
            else:
                r["full_text"] = r.get("template_id", "?")
                r["clause_structure"] = ""

    # Enhanced learning quality metrics
    retention = get_delayed_retention(token)
    transfer_scores = get_transfer_scores(token)
    fluency = get_fluency_score(token)
    calibration = get_confidence_calibration(token)
    scaffold = get_scaffold_dependence(token)
    transfer_progress = get_all_transfer_progress(token)

    return render_template("dashboard.html",
                           error_stats=error_stats,
                           recent=recent,
                           accuracy=json.dumps(accuracy),
                           summary=summary,
                           saved_words=saved_words,
                           retention=retention,
                           transfer_scores=transfer_scores,
                           fluency=fluency,
                           calibration=calibration,
                           scaffold=scaffold,
                           transfer_progress=transfer_progress)


@app.route('/admin/download-db')
def download_db():
    from flask import send_file
    admin_password = os.environ.get('ADMIN_PASSWORD')
    provided_password = request.args.get('password')

    if not admin_password or provided_password != admin_password:
        return "Unauthorized - Invalid password", 401

    if os.environ.get('RENDER'):
        db_path = '/data/german_learning.db'
    else:
        db_path = 'german_learning.db'

    if not os.path.exists(db_path):
        return "Database not found", 404

    return send_file(
        db_path,
        as_attachment=True,
        download_name=f'german_learning_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    )

# ─── API ROUTES ────────────────────────────────────────────────────────

@app.route("/api/exercise", methods=["GET"])
def api_get_exercise():
    token = get_user_token()
    difficulty = request.args.get("difficulty", type=int)
    exercise = get_exercise_by_difficulty(difficulty)
    if not exercise:
        return jsonify({"error": "no exercises available"}), 404
    mark_sentence_shown(token, exercise["template_id"])
    # Don't send the full answer to the frontend
    safe = {
        "template_id": exercise["template_id"],
        "display_text": exercise["display_text"],
        "words": exercise["words"],
        "verbs": exercise["verbs"],
        "slots": [{"index": s["index"], "suffix": s["suffix"]} for s in exercise["slots"]],
        "difficulty": exercise["difficulty"],
        "clause_type": exercise["clause_type"],
        "num_slots": len(exercise["slots"])
    }
    return jsonify(safe)


@app.route("/api/check", methods=["POST"])
def api_check_answer():
    token = get_user_token()
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    template_id = data.get("template_id")
    user_positions = data.get("positions", [])  # [{slot_index, word}, ...]
    retry_id = data.get("retry_id")

    template = get_template_by_id(template_id)
    if not template:
        # Check grammar exercises (konnektoren, konjunktiv, relativ use reconstruction)
        grammar_ex = get_exercise_by_id(template_id)
        if grammar_ex and grammar_ex["type"] == "reconstruction":
            template = {
                "id": grammar_ex["id"],
                "text": grammar_ex["data"]["text"],
                "verbs": grammar_ex["data"]["verbs"],
                "clause_type": grammar_ex["data"]["clause_type"],
                "difficulty": grammar_ex["level"],
                "explanation": grammar_ex["grammar_rule"]
            }
        else:
            return jsonify({"error": "unknown sentence"}), 404

    exercise = prepare_exercise(template)

    # Full sentence check: compare every word position
    all_slots = exercise["all_slots"]
    slot_results = []
    all_correct = True
    for slot in all_slots:
        idx = slot["index"]
        user_word = None
        for up in user_positions:
            if up["slot_index"] == idx:
                user_word = up["word"]
                break
        is_correct = (user_word == slot["correct_word"])
        if not is_correct:
            all_correct = False
        slot_results.append({
            "index": idx,
            "correct_word": slot["correct_word"],
            "user_word": user_word,
            "is_correct": is_correct,
            "is_verb": slot["is_verb"],
            "suffix": slot["suffix"]
        })

    # Extract verb-only positions for error analysis
    verb_user_positions = []
    verb_slot_idx = 0
    for slot in exercise["verb_slots"]:
        word_idx = slot["index"]
        user_word = None
        for up in user_positions:
            if up["slot_index"] == word_idx:
                user_word = up["word"]
                break
        verb_user_positions.append({
            "slot_index": verb_slot_idx,
            "verb": user_word or ""
        })
        verb_slot_idx += 1

    errors = analyze_errors(exercise, verb_user_positions)

    # Determine module from data
    module = data.get("module", "verb_position")

    # Record attempt
    record_attempt(token, template_id, user_positions, all_correct,
                   errors if errors else None, module=module,
                   exercise_type="reconstruction")

    # Update grammar rule tracking for grammar module exercises
    if module != "verb_position":
        grammar_ex = get_exercise_by_id(template_id)
        if grammar_ex:
            update_grammar_rule(token, module,
                                grammar_ex.get("topic", template_id), all_correct)

    # If retry exercise completed correctly, mark it
    if all_correct and retry_id:
        complete_retry(retry_id)

    # Log errors and schedule retries
    explanations = []
    if errors:
        for err in errors:
            error_id = log_error(token, template_id, err["category"], err["detail"])
            schedule_retry(token, template_id, error_id, days_delay=2)
            explanations.append(get_error_explanation(err))

    # Adaptive: timing, micro-curriculum, transfer, confusion sets
    topic = None
    if module != "verb_position":
        grammar_ex_for_topic = get_exercise_by_id(template_id)
        if grammar_ex_for_topic:
            topic = grammar_ex_for_topic.get("topic")
    _handle_post_check(token, template_id, errors, all_correct, data, module, topic)

    # Build response with grammar_rule for consistency with other exercise types
    response = {
        "correct": all_correct,
        "full_sentence": exercise["full_text"],
        "explanation": exercise["explanation"],
        "errors": explanations,
        "slot_results": slot_results
    }
    # Add grammar_rule/grammar_tip for grammar module exercises
    if module != "verb_position":
        grammar_ex = get_exercise_by_id(template_id)
        if grammar_ex:
            response["grammar_rule"] = grammar_ex.get("grammar_rule", "")
            response["grammar_tip"] = grammar_ex.get("grammar_tip", "")

    return jsonify(response)


@app.route("/api/stats", methods=["GET"])
def api_stats():
    token = get_user_token()
    return jsonify({
        "summary": get_user_summary(token),
        "error_categories": get_error_stats(token),
        "accuracy_over_time": get_accuracy_over_time(token)
    })


@app.route("/api/regenerate", methods=["POST"])
@require_api_token
def api_regenerate_exercises():
    """Regenerate all exercises using Claude API. Requires API_TOKEN auth."""
    try:
        verb_sentences, grammar_exs = refresh_exercise_banks()
        if verb_sentences:
            load_generated_verb_sentences(verb_sentences)
        if grammar_exs:
            load_generated_exercises(grammar_exs)
        return jsonify({
            "success": True,
            "verb_position_count": len(verb_sentences),
            "grammar_exercise_count": len(grammar_exs)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── DUDEN LOOKUP ─────────────────────────────────────────────────────

@app.route("/api/duden/<word>", methods=["GET"])
def api_duden_lookup(word):
    """Proxy lookup for Duden dictionary definitions (German only)."""
    import requests
    from bs4 import BeautifulSoup

    word_clean = word.strip().lower()
    url = f"https://www.duden.de/rechtschreibung/{word_clean}"
    definition = ""
    examples = []
    word_type = ""

    try:
        resp = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; GermanLearningApp/1.0)"
        }, timeout=5)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Extract word type (Wortart)
            wortart = soup.select_one('[class*="Wortart"]')
            if not wortart:
                wortart = soup.select_one('.tuple__val')
            if wortart:
                word_type = wortart.get_text(strip=True)

            # Extract definitions (Bedeutungen)
            meanings = soup.select('[id*="bedeutung"] li, [class*="bedeutung"] li, .enumeration__text')
            if meanings:
                definition = "; ".join(
                    m.get_text(strip=True) for m in meanings[:3]
                )
            if not definition:
                # Fallback: try the first text block under Bedeutung
                bed_section = soup.select_one('[id*="bedeutung"]')
                if bed_section:
                    definition = bed_section.get_text(strip=True)[:300]

            # Extract examples (Beispiele)
            example_els = soup.select('[class*="note__list"] li, .beispiel, [class*="Beispiel"] li')
            for ex in example_els[:3]:
                examples.append(ex.get_text(strip=True))

        if not definition:
            # Try alternate URL format
            resp2 = requests.get(
                f"https://www.duden.de/suchen/dudenonline/{word_clean}",
                headers={"User-Agent": "Mozilla/5.0 (compatible; GermanLearningApp/1.0)"},
                timeout=5
            )
            if resp2.status_code == 200:
                soup2 = BeautifulSoup(resp2.text, "html.parser")
                first_result = soup2.select_one('.vignette__link')
                if first_result and first_result.get('href'):
                    result_url = "https://www.duden.de" + first_result['href']
                    resp3 = requests.get(result_url, headers={
                        "User-Agent": "Mozilla/5.0 (compatible; GermanLearningApp/1.0)"
                    }, timeout=5)
                    if resp3.status_code == 200:
                        soup3 = BeautifulSoup(resp3.text, "html.parser")
                        meanings3 = soup3.select('[id*="bedeutung"] li, .enumeration__text')
                        if meanings3:
                            definition = "; ".join(
                                m.get_text(strip=True) for m in meanings3[:3]
                            )
                        example_els3 = soup3.select('[class*="note__list"] li, .beispiel')
                        for ex in example_els3[:3]:
                            examples.append(ex.get_text(strip=True))

    except Exception:
        pass

    if not definition:
        definition = f"Keine Definition gefunden. Bitte suchen Sie auf duden.de nach '{word_clean}'."

    return jsonify({
        "word": word_clean,
        "word_type": word_type,
        "definition": definition,
        "examples": examples,
        "duden_url": f"https://www.duden.de/rechtschreibung/{word_clean}"
    })


# ─── SAVED WORDS ──────────────────────────────────────────────────────

@app.route("/api/words", methods=["GET"])
def api_get_saved_words():
    token = get_user_token()
    words = get_saved_words(token)
    return jsonify({"words": words})


@app.route("/api/words", methods=["POST"])
def api_save_word():
    token = get_user_token()
    data = request.get_json()
    if not data or not data.get("word"):
        return jsonify({"error": "word required"}), 400
    save_word(
        token,
        data["word"],
        definition=data.get("definition"),
        examples=data.get("examples"),
        source_sentence=data.get("source_sentence")
    )
    return jsonify({"status": "saved"})


@app.route("/api/words/<int:word_id>", methods=["DELETE"])
def api_delete_word(word_id):
    token = get_user_token()
    delete_saved_word(token, word_id)
    return jsonify({"status": "deleted"})


@app.route("/api/words/export/anki", methods=["GET"])
def api_export_anki():
    """Export saved words as Anki-compatible TSV."""
    token = get_user_token()
    words = get_saved_words(token)
    if not words:
        return jsonify({"error": "no words saved"}), 404

    lines = []
    for w in words:
        front = w["word"]
        examples = w.get("examples") or ""
        definition = w.get("definition") or ""
        back = definition
        if examples:
            back += "<br><br><b>Beispiele:</b><br>" + examples.replace("\n", "<br>")
        if w.get("source_sentence"):
            back += "<br><br><i>" + w["source_sentence"] + "</i>"
        # TSV: front \t back
        lines.append(f"{front}\t{back}")

    content = "\n".join(lines)
    from flask import Response
    return Response(
        content,
        mimetype="text/tab-separated-values",
        headers={"Content-Disposition": "attachment; filename=german_words_anki.tsv"}
    )


@app.route("/api/words/export/quizlet", methods=["GET"])
def api_export_quizlet():
    """Export saved words as Quizlet-compatible text (tab-separated, newline between cards)."""
    token = get_user_token()
    words = get_saved_words(token)
    if not words:
        return jsonify({"error": "no words saved"}), 404

    lines = []
    for w in words:
        front = w["word"]
        definition = w.get("definition") or ""
        examples = w.get("examples") or ""
        back = definition
        if examples:
            back += " | Beispiele: " + examples.replace("\n", " | ")
        lines.append(f"{front}\t{back}")

    content = "\n".join(lines)
    from flask import Response
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=german_words_quizlet.txt"}
    )


# ─── DAILY MESSAGE / NOTIFICATION API ──────────────────────────────────

@app.route("/api/daily", methods=["GET"])
def api_daily_message():
    """Public endpoint for daily sentence — used by Shortcuts/automation."""
    today = date.today().isoformat()
    msg = get_daily_message(today)
    if not msg:
        template = get_daily_sentence()
        sentence_text = template["text"]
        store_daily_message(today, sentence_text)
        msg = {"sentence_text": sentence_text, "message_date": today}

    base_url = os.environ.get("BASE_URL", request.host_url.rstrip("/"))
    return jsonify({
        "date": msg["message_date"] if isinstance(msg, dict) else today,
        "sentence": msg["sentence_text"] if isinstance(msg, dict) else msg,
        "exercise_url": f"{base_url}/exercise",
        "message": f"🇩🇪 Verb-End Torture Chamber\n\nHeute: {msg['sentence_text'] if isinstance(msg, dict) else msg}\n\nKannst du das Verb richtig platzieren?\n{base_url}/exercise"
    })


@app.route("/api/daily/send", methods=["POST"])
@require_api_token
def api_trigger_daily():
    """Trigger endpoint for cron job to prepare daily message."""
    today = date.today().isoformat()
    msg = get_daily_message(today)
    if not msg:
        template = get_daily_sentence()
        store_daily_message(today, template["text"])
        msg = get_daily_message(today)
    mark_daily_sent(today)
    base_url = os.environ.get("BASE_URL", request.host_url.rstrip("/"))
    return jsonify({
        "status": "sent",
        "message": msg["sentence_text"] if isinstance(msg, dict) else str(msg),
        "url": f"{base_url}/exercise"
    })


# ─── MCP ENDPOINTS ────────────────────────────────────────────────────

@app.route("/api/mcp/exercise", methods=["GET"])
@require_api_token
def mcp_get_exercise():
    difficulty = request.args.get("difficulty", type=int)
    exercise = get_exercise_by_difficulty(difficulty)
    if not exercise:
        return jsonify({"error": "no exercises"}), 404
    return jsonify(exercise)


@app.route("/api/mcp/check", methods=["POST"])
@require_api_token
def mcp_check():
    data = request.get_json()
    template_id = data.get("template_id")
    user_positions = data.get("positions", [])

    template = get_template_by_id(template_id)
    if not template:
        return jsonify({"error": "unknown sentence"}), 404

    exercise = prepare_exercise(template)
    errors = analyze_errors(exercise, user_positions)
    explanations = [get_error_explanation(e) for e in errors]

    return jsonify({
        "correct": len(errors) == 0,
        "full_sentence": exercise["full_text"],
        "explanation": exercise["explanation"],
        "errors": explanations
    })


@app.route("/api/mcp/stats", methods=["GET"])
@require_api_token
def mcp_stats():
    token = request.args.get("user_token", "")
    if not token:
        return jsonify({"error": "user_token required"}), 400
    return jsonify({
        "summary": get_user_summary(token),
        "error_categories": get_error_stats(token)
    })


@app.route("/api/mcp/sentence-bank/info", methods=["GET"])
@require_api_token
def mcp_sentence_info():
    return jsonify({
        "total_sentences": len(SENTENCE_BANK),
        "by_difficulty": count_by_difficulty(),
        "clause_types": list(set(t["clause_type"] for t in SENTENCE_BANK)),
        "grammar_modules": list(GRAMMAR_MODULES.keys()),
        "grammar_exercise_counts": count_by_module_and_level()
    })

@app.route('/admin/backup-info')
def backup_info():
    admin_password = os.environ.get('ADMIN_PASSWORD')
    provided_password = request.args.get('password')

    if not admin_password or provided_password != admin_password:
        return "Unauthorized", 401

    db_path = '/data/german_learning.db' if os.environ.get('RENDER') else 'german_learning.db'

    if os.path.exists(db_path):
        stat = os.stat(db_path)
        return {
            'database_exists': True,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'download_url': f'/admin/download-db?password=YOUR_PASSWORD'
        }

    return {'database_exists': False}


# ─── HELPERS ───────────────────────────────────────────────────────────

def _diff_label(d):
    return {1: "A2", 2: "B1", 3: "B2", 4: "C1"}.get(d, "?")


# ─── MAIN ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("DEBUG", "0") == "1")
