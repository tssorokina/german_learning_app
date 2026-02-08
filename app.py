"""
Verb-End Torture Chamber — Flask Web Application.

A German grammar trainer focused on verb placement in subordinate/nested clauses.
"""
import os
import json
import secrets
from datetime import date, datetime
from functools import wraps

from flask import (Flask, render_template, request, jsonify, session,
                   redirect, url_for, abort)

from database import (init_db, get_or_create_user, get_retry_template,
                      mark_sentence_shown, record_attempt,
                      log_error, schedule_retry, complete_retry, get_error_stats,
                      get_recent_attempts, get_accuracy_over_time, get_user_summary,
                      store_daily_message, get_daily_message, mark_daily_sent,
                      save_word, get_saved_words, delete_saved_word)
from sentences import (get_exercise_by_difficulty, prepare_exercise,
                       get_template_by_id, get_daily_sentence, SENTENCE_BANK,
                       count_by_difficulty)
from error_analyzer import (analyze_errors, get_error_explanation,
                            get_all_categories, ERROR_CATEGORIES)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Auth token for API / notification endpoints
API_TOKEN = os.environ.get("API_TOKEN", secrets.token_hex(16))


def get_user_token():
    """Get or create a persistent user token in the session."""
    if "user_token" not in session:
        session["user_token"] = secrets.token_hex(8)
        session.permanent = True
    get_or_create_user(session["user_token"])
    return session["user_token"]


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


# ─── WEB ROUTES ────────────────────────────────────────────────────────

@app.route("/")
def index():
    token = get_user_token()
    summary = get_user_summary(token)
    return render_template("index.html", summary=summary)


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
        # Get list of shown template IDs for this user
        exercise = get_exercise_by_difficulty(difficulty)

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
    }

    return render_template("exercise.html",
                           exercise=json.dumps(safe_exercise),
                           retry_id=retry_id,
                           difficulty_label=_diff_label(exercise["difficulty"]))


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
        r["full_text"] = tmpl["text"] if tmpl else r.get("template_id", "?")
        r["clause_structure"] = tmpl["clause_type"] if tmpl else ""

    return render_template("dashboard.html",
                           error_stats=error_stats,
                           recent=recent,
                           accuracy=json.dumps(accuracy),
                           summary=summary,
                           saved_words=saved_words)

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

    # Record attempt
    record_attempt(token, template_id, user_positions, all_correct,
                   errors if errors else None)

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

    return jsonify({
        "correct": all_correct,
        "full_sentence": exercise["full_text"],
        "explanation": exercise["explanation"],
        "errors": explanations,
        "slot_results": slot_results
    })


@app.route("/api/stats", methods=["GET"])
def api_stats():
    token = get_user_token()
    return jsonify({
        "summary": get_user_summary(token),
        "error_categories": get_error_stats(token),
        "accuracy_over_time": get_accuracy_over_time(token)
    })


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
        "clause_types": list(set(t["clause_type"] for t in SENTENCE_BANK))
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
