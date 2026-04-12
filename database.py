"""SQLite database layer for the German Verb-End Torture Chamber."""
import sqlite3
import os
import json
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.environ.get("DB_PATH", "german_app.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            template_id TEXT NOT NULL,
            user_positions_json TEXT NOT NULL,
            correct INTEGER NOT NULL DEFAULT 0,
            errors_json TEXT,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS shown_sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            template_id TEXT NOT NULL,
            shown_date DATE NOT NULL,
            UNIQUE(user_token, template_id)
        );

        CREATE TABLE IF NOT EXISTS error_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            template_id TEXT NOT NULL,
            error_category TEXT NOT NULL,
            error_detail TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS retry_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            template_id TEXT NOT NULL,
            source_error_id INTEGER,
            scheduled_after DATE NOT NULL,
            completed INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS daily_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_date DATE UNIQUE NOT NULL,
            sentence_text TEXT NOT NULL,
            sent INTEGER DEFAULT 0,
            sent_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            word TEXT NOT NULL,
            definition TEXT,
            examples TEXT,
            source_sentence TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_token, word)
        );

        CREATE TABLE IF NOT EXISTS grammar_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            module TEXT NOT NULL,
            rule_id TEXT NOT NULL,
            times_tested INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            ease_factor REAL DEFAULT 2.5,
            interval_days REAL DEFAULT 1,
            last_tested TIMESTAMP,
            next_review TIMESTAMP,
            UNIQUE(user_token, rule_id)
        );

        CREATE TABLE IF NOT EXISTS micro_curriculum_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            error_category TEXT NOT NULL,
            source_error_id INTEGER,
            source_exercise_id TEXT,
            curriculum_key TEXT NOT NULL,
            total_steps INTEGER NOT NULL,
            current_step INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transfer_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            module TEXT NOT NULL,
            rule_id TEXT NOT NULL,
            current_stage TEXT DEFAULT 'controlled',
            controlled_correct INTEGER DEFAULT 0,
            controlled_total INTEGER DEFAULT 0,
            near_correct INTEGER DEFAULT 0,
            near_total INTEGER DEFAULT 0,
            far_completed INTEGER DEFAULT 0,
            delayed_correct INTEGER DEFAULT 0,
            delayed_total INTEGER DEFAULT 0,
            last_stage_change TIMESTAMP,
            next_delayed_review TIMESTAMP,
            UNIQUE(user_token, rule_id)
        );

        CREATE TABLE IF NOT EXISTS exercise_timing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            attempt_id INTEGER,
            template_id TEXT NOT NULL,
            duration_ms INTEGER NOT NULL,
            input_mode TEXT,
            predicted_correct INTEGER,
            actual_correct INTEGER,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS confusion_set_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            confusion_set_key TEXT NOT NULL,
            times_tested INTEGER DEFAULT 0,
            discrimination_correct INTEGER DEFAULT 0,
            last_tested TIMESTAMP,
            UNIQUE(user_token, confusion_set_key)
        );

        CREATE TABLE IF NOT EXISTS user_scaffold (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT UNIQUE NOT NULL,
            level INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS input_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            title TEXT,
            raw_text TEXT NOT NULL,
            sentences_json TEXT NOT NULL,
            difficulty_score REAL,
            word_count INTEGER,
            unknown_word_count INTEGER,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS input_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            text_id INTEGER NOT NULL REFERENCES input_texts(id),
            sentence_index INTEGER NOT NULL,
            sentence_text TEXT NOT NULL,
            english TEXT DEFAULT '',
            difficulty_score REAL,
            read_at TIMESTAMP,
            drilled INTEGER DEFAULT 0,
            drill_correct INTEGER DEFAULT 0,
            ease_factor REAL DEFAULT 2.5,
            interval_days REAL DEFAULT 1,
            next_review TIMESTAMP,
            last_reviewed TIMESTAMP,
            UNIQUE(user_token, text_id, sentence_index)
        );

        CREATE TABLE IF NOT EXISTS input_mined_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_token TEXT NOT NULL,
            text_id INTEGER NOT NULL REFERENCES input_texts(id),
            word TEXT NOT NULL,
            phrase TEXT,
            definition TEXT,
            examples TEXT,
            source_sentence TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_token, text_id, word)
        );
    """)

    # Add module and exercise_type columns to attempts if missing
    try:
        conn.execute("SELECT module FROM attempts LIMIT 1")
    except Exception:
        conn.execute("ALTER TABLE attempts ADD COLUMN module TEXT DEFAULT 'verb_position'")
        conn.execute("ALTER TABLE attempts ADD COLUMN exercise_type TEXT DEFAULT 'reconstruction'")

    # Add transfer/timing/curriculum columns to attempts
    for col, defn in [
        ("transfer_stage", "TEXT"),
        ("duration_ms", "INTEGER"),
        ("input_mode", "TEXT"),
        ("micro_curriculum_session_id", "INTEGER"),
    ]:
        try:
            conn.execute(f"SELECT {col} FROM attempts LIMIT 1")
        except Exception:
            conn.execute(f"ALTER TABLE attempts ADD COLUMN {col} {defn}")

    # Add email and password_hash columns to users if missing
    for col, defn in [
        ("email", "TEXT"),
        ("password_hash", "TEXT"),
        ("display_name", "TEXT"),
    ]:
        try:
            conn.execute(f"SELECT {col} FROM users LIMIT 1")
        except Exception:
            conn.execute(f"ALTER TABLE users ADD COLUMN {col} {defn}")

    # Add english column to input_segments if missing
    try:
        conn.execute("SELECT english FROM input_segments LIMIT 1")
    except Exception:
        try:
            conn.execute("ALTER TABLE input_segments ADD COLUMN english TEXT DEFAULT ''")
        except Exception:
            pass

    conn.commit()
    conn.close()


def get_or_create_user(token):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    if not row:
        conn.execute("INSERT INTO users (token) VALUES (?)", (token,))
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    conn.close()
    return dict(row)


# ─── AUTHENTICATION ────────────────────────────────────────────────────

def register_user(email, password, display_name=None):
    """Register a new user with email and password.

    Returns (user_dict, error_string). On success error is None.
    """
    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return None, "An account with this email already exists."

    import secrets as _secrets
    token = _secrets.token_hex(8)
    pw_hash = generate_password_hash(password, method="pbkdf2:sha256")
    conn.execute(
        "INSERT INTO users (token, email, password_hash, display_name) VALUES (?, ?, ?, ?)",
        (token, email, pw_hash, display_name or email.split("@")[0])
    )
    conn.commit()
    row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    conn.close()
    return dict(row), None


def authenticate_user(email, password):
    """Check email/password credentials.

    Returns user dict on success, None on failure.
    """
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if not row:
        return None
    user = dict(row)
    if not user.get("password_hash"):
        return None
    if check_password_hash(user["password_hash"], password):
        return user
    return None


def get_user_by_token(token):
    """Retrieve a user record by token."""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    conn.close()
    return dict(row) if row else None


def merge_anonymous_into_user(anon_token, user_token):
    """Migrate all learning data from an anonymous session into a registered user.

    This transfers attempts, shown_sentences, error_log, retry_queue,
    saved_words, grammar_rules, micro_curriculum_sessions,
    transfer_progress, exercise_timing, and confusion_set_state.
    """
    conn = get_db()
    tables_with_user_token = [
        "attempts", "shown_sentences", "error_log", "retry_queue",
        "saved_words", "grammar_rules", "micro_curriculum_sessions",
        "transfer_progress", "exercise_timing", "confusion_set_state",
    ]
    for table in tables_with_user_token:
        conn.execute(
            f"UPDATE {table} SET user_token = ? WHERE user_token = ?",
            (user_token, anon_token)
        )
    # Delete the anonymous user record
    conn.execute("DELETE FROM users WHERE token = ?", (anon_token,))
    conn.commit()
    conn.close()


def get_shown_template_ids(user_token):
    conn = get_db()
    rows = conn.execute(
        "SELECT template_id FROM shown_sentences WHERE user_token = ?",
        (user_token,)
    ).fetchall()
    conn.close()
    return {r["template_id"] for r in rows}


def get_retry_template(user_token):
    """Get a template_id from the retry queue (previously failed)."""
    conn = get_db()
    today = date.today().isoformat()
    row = conn.execute("""
        SELECT template_id, id as retry_id FROM retry_queue
        WHERE user_token = ? AND completed = 0 AND scheduled_after <= ?
        ORDER BY scheduled_after ASC LIMIT 1
    """, (user_token, today)).fetchone()
    conn.close()
    return dict(row) if row else None


def mark_sentence_shown(user_token, template_id):
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO shown_sentences (user_token, template_id, shown_date) VALUES (?, ?, ?)",
            (user_token, template_id, date.today().isoformat())
        )
        conn.commit()
    finally:
        conn.close()


def record_attempt(user_token, template_id, user_positions, correct, errors=None,
                   module="verb_position", exercise_type="reconstruction",
                   transfer_stage=None, duration_ms=None, input_mode=None,
                   micro_curriculum_session_id=None):
    conn = get_db()
    cur = conn.execute(
        """INSERT INTO attempts (user_token, template_id, user_positions_json, correct, errors_json,
           module, exercise_type, transfer_stage, duration_ms, input_mode, micro_curriculum_session_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_token, template_id, json.dumps(user_positions), 1 if correct else 0,
         json.dumps(errors) if errors else None, module, exercise_type,
         transfer_stage, duration_ms, input_mode, micro_curriculum_session_id)
    )
    attempt_id = cur.lastrowid
    conn.commit()
    conn.close()
    return attempt_id


def log_error(user_token, template_id, error_category, error_detail=None):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO error_log (user_token, template_id, error_category, error_detail) VALUES (?, ?, ?, ?)",
        (user_token, template_id, error_category, error_detail)
    )
    error_id = cur.lastrowid
    conn.commit()
    conn.close()
    return error_id


def schedule_retry(user_token, template_id, error_id, days_delay=2):
    conn = get_db()
    from datetime import timedelta
    scheduled = (date.today() + timedelta(days=days_delay)).isoformat()
    conn.execute(
        """INSERT INTO retry_queue (user_token, template_id, source_error_id, scheduled_after)
           VALUES (?, ?, ?, ?)""",
        (user_token, template_id, error_id, scheduled)
    )
    conn.commit()
    conn.close()


def complete_retry(retry_id):
    conn = get_db()
    conn.execute("UPDATE retry_queue SET completed = 1 WHERE id = ?", (retry_id,))
    conn.commit()
    conn.close()


def get_error_stats(user_token):
    conn = get_db()
    rows = conn.execute("""
        SELECT error_category, COUNT(*) as count,
               MAX(logged_at) as last_occurrence
        FROM error_log
        WHERE user_token = ?
        GROUP BY error_category
        ORDER BY count DESC
    """, (user_token,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_attempts(user_token, limit=20):
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM attempts
        WHERE user_token = ?
        ORDER BY attempted_at DESC
        LIMIT ?
    """, (user_token, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_accuracy_over_time(user_token, days=30):
    conn = get_db()
    rows = conn.execute("""
        SELECT DATE(attempted_at) as day,
               COUNT(*) as total,
               SUM(correct) as correct_count
        FROM attempts
        WHERE user_token = ?
          AND attempted_at >= DATE('now', ?)
        GROUP BY DATE(attempted_at)
        ORDER BY day ASC
    """, (user_token, f"-{days} days")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_summary(user_token):
    conn = get_db()
    total = conn.execute(
        "SELECT COUNT(*) as c FROM attempts WHERE user_token = ?", (user_token,)
    ).fetchone()["c"]
    correct = conn.execute(
        "SELECT COUNT(*) as c FROM attempts WHERE user_token = ? AND correct = 1",
        (user_token,)
    ).fetchone()["c"]
    streak = 0
    rows = conn.execute(
        "SELECT correct FROM attempts WHERE user_token = ? ORDER BY attempted_at DESC",
        (user_token,)
    ).fetchall()
    for r in rows:
        if r["correct"]:
            streak += 1
        else:
            break
    pending_retries = conn.execute(
        "SELECT COUNT(*) as c FROM retry_queue WHERE user_token = ? AND completed = 0",
        (user_token,)
    ).fetchone()["c"]
    conn.close()
    return {
        "total_attempts": total,
        "correct": correct,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "current_streak": streak,
        "pending_retries": pending_retries
    }


def store_daily_message(message_date, sentence_text):
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO daily_messages (message_date, sentence_text) VALUES (?, ?)",
        (message_date, sentence_text)
    )
    conn.commit()
    conn.close()


def get_daily_message(message_date=None):
    if message_date is None:
        message_date = date.today().isoformat()
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM daily_messages WHERE message_date = ?", (message_date,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def mark_daily_sent(message_date):
    conn = get_db()
    conn.execute(
        "UPDATE daily_messages SET sent = 1, sent_at = ? WHERE message_date = ?",
        (datetime.now().isoformat(), message_date)
    )
    conn.commit()
    conn.close()


# ─── SAVED WORDS ──────────────────────────────────────────────────────

def save_word(user_token, word, definition=None, examples=None, source_sentence=None):
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO saved_words
           (user_token, word, definition, examples, source_sentence, saved_at)
           VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
        (user_token, word, definition, examples, source_sentence)
    )
    conn.commit()
    conn.close()


def get_saved_words(user_token):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM saved_words WHERE user_token = ? ORDER BY saved_at DESC",
        (user_token,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_saved_word(user_token, word_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM saved_words WHERE id = ? AND user_token = ?",
        (word_id, user_token)
    )
    conn.commit()
    conn.close()


# ─── GRAMMAR RULES / SM-2 SPACED REPETITION ──────────────

def update_grammar_rule(user_token, module, rule_id, was_correct):
    """Update grammar rule tracking with SM-2 spaced repetition."""
    from datetime import timedelta
    conn = get_db()
    now = datetime.now().isoformat()

    row = conn.execute(
        "SELECT * FROM grammar_rules WHERE user_token = ? AND rule_id = ?",
        (user_token, rule_id)
    ).fetchone()

    if row:
        row = dict(row)
        times_tested = row["times_tested"] + 1
        times_correct = row["times_correct"] + (1 if was_correct else 0)
        ease_factor = row["ease_factor"]
        interval_days = row["interval_days"]

        if was_correct:
            interval_days = interval_days * ease_factor
            ease_factor = min(ease_factor + 0.1, 3.0)
        else:
            interval_days = 1
            ease_factor = max(ease_factor - 0.2, 1.3)

        next_review = (datetime.now() + timedelta(days=interval_days)).isoformat()

        conn.execute("""
            UPDATE grammar_rules
            SET times_tested = ?, times_correct = ?, ease_factor = ?,
                interval_days = ?, last_tested = ?, next_review = ?
            WHERE user_token = ? AND rule_id = ?
        """, (times_tested, times_correct, ease_factor, interval_days,
              now, next_review, user_token, rule_id))
    else:
        interval_days = 1 if not was_correct else 2.5
        ease_factor = 2.5
        next_review = (datetime.now() + timedelta(days=interval_days)).isoformat()

        conn.execute("""
            INSERT INTO grammar_rules
            (user_token, module, rule_id, times_tested, times_correct,
             ease_factor, interval_days, last_tested, next_review)
            VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?)
        """, (user_token, module, rule_id, 1 if was_correct else 0,
              ease_factor, interval_days, now, next_review))

    conn.commit()
    conn.close()


def get_grammar_rules_due(user_token, module=None):
    """Get grammar rules due for review."""
    conn = get_db()
    now = datetime.now().isoformat()
    if module:
        rows = conn.execute("""
            SELECT * FROM grammar_rules
            WHERE user_token = ? AND module = ? AND next_review <= ?
            ORDER BY next_review ASC
        """, (user_token, module, now)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM grammar_rules
            WHERE user_token = ? AND next_review <= ?
            ORDER BY next_review ASC
        """, (user_token, now)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_module_stats(user_token):
    """Get per-module attempt statistics."""
    conn = get_db()
    rows = conn.execute("""
        SELECT module, exercise_type,
               COUNT(*) as total,
               SUM(correct) as correct_count
        FROM attempts
        WHERE user_token = ?
        GROUP BY module, exercise_type
    """, (user_token,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── MICRO-CURRICULUM SESSIONS ───────────────────────────────────────

def get_active_micro_session(user_token):
    """Get the active micro-curriculum session for a user."""
    conn = get_db()
    row = conn.execute("""
        SELECT * FROM micro_curriculum_sessions
        WHERE user_token = ? AND status = 'active'
        ORDER BY started_at DESC LIMIT 1
    """, (user_token,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_micro_session(user_token, error_category, source_error_id,
                         source_exercise_id, curriculum_key, total_steps):
    """Create a new micro-curriculum session. Returns session_id."""
    conn = get_db()
    cur = conn.execute("""
        INSERT INTO micro_curriculum_sessions
        (user_token, error_category, source_error_id, source_exercise_id,
         curriculum_key, total_steps)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_token, error_category, source_error_id,
          source_exercise_id, curriculum_key, total_steps))
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id


def advance_micro_session(session_id):
    """Advance to the next step. Mark completed if all steps done."""
    conn = get_db()
    row = conn.execute(
        "SELECT current_step, total_steps FROM micro_curriculum_sessions WHERE id = ?",
        (session_id,)
    ).fetchone()
    if not row:
        conn.close()
        return None

    next_step = row["current_step"] + 1
    if next_step >= row["total_steps"]:
        conn.execute("""
            UPDATE micro_curriculum_sessions
            SET current_step = ?, status = 'completed', completed_at = ?
            WHERE id = ?
        """, (next_step, datetime.now().isoformat(), session_id))
    else:
        conn.execute(
            "UPDATE micro_curriculum_sessions SET current_step = ? WHERE id = ?",
            (next_step, session_id)
        )
    conn.commit()
    conn.close()
    return "completed" if next_step >= row["total_steps"] else "advanced"


def abandon_micro_session(session_id):
    """Abandon a micro-curriculum session."""
    conn = get_db()
    conn.execute(
        "UPDATE micro_curriculum_sessions SET status = 'abandoned' WHERE id = ?",
        (session_id,)
    )
    conn.commit()
    conn.close()


# ─── EXERCISE TIMING ─────────────────────────────────────────────────

def record_exercise_timing(user_token, attempt_id, template_id, duration_ms,
                           input_mode=None, predicted_correct=None, actual_correct=None):
    """Record timing and confidence data for an exercise attempt."""
    conn = get_db()
    conn.execute("""
        INSERT INTO exercise_timing
        (user_token, attempt_id, template_id, duration_ms,
         input_mode, predicted_correct, actual_correct)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_token, attempt_id, template_id, duration_ms,
          input_mode, predicted_correct, actual_correct))
    conn.commit()
    conn.close()


# ─── TRANSFER PROGRESS ───────────────────────────────────────────────

def get_transfer_progress(user_token, rule_id):
    """Get transfer progress for a specific grammar rule."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM transfer_progress WHERE user_token = ? AND rule_id = ?",
        (user_token, rule_id)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_transfer_progress(user_token, module, rule_id, stage, was_correct):
    """Update transfer progress for a grammar rule at a specific stage."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM transfer_progress WHERE user_token = ? AND rule_id = ?",
        (user_token, rule_id)
    ).fetchone()

    if row:
        row = dict(row)
        total_col = f"{stage}_total"
        correct_col = f"{stage}_correct"
        if stage == "far":
            conn.execute("""
                UPDATE transfer_progress SET far_completed = far_completed + 1
                WHERE user_token = ? AND rule_id = ?
            """, (user_token, rule_id))
        else:
            conn.execute(f"""
                UPDATE transfer_progress
                SET {total_col} = {total_col} + 1,
                    {correct_col} = {correct_col} + ?
                WHERE user_token = ? AND rule_id = ?
            """, (1 if was_correct else 0, user_token, rule_id))
    else:
        total_val = 1
        correct_val = 1 if was_correct else 0
        conn.execute("""
            INSERT INTO transfer_progress
            (user_token, module, rule_id, current_stage,
             controlled_correct, controlled_total)
            VALUES (?, ?, ?, 'controlled', ?, ?)
        """, (user_token, module, rule_id, correct_val, total_val))

    conn.commit()
    conn.close()


def promote_transfer_stage(user_token, rule_id, new_stage):
    """Promote a user to the next transfer stage for a rule."""
    conn = get_db()
    now = datetime.now().isoformat()
    delayed_review = None
    if new_stage == "delayed":
        delayed_review = (datetime.now() + timedelta(days=7)).isoformat()

    conn.execute("""
        UPDATE transfer_progress
        SET current_stage = ?, last_stage_change = ?, next_delayed_review = ?
        WHERE user_token = ? AND rule_id = ?
    """, (new_stage, now, delayed_review, user_token, rule_id))
    conn.commit()
    conn.close()


# ─── CONFUSION SET STATE ─────────────────────────────────────────────

def update_confusion_set_state(user_token, confusion_set_key, was_correct):
    """Update discrimination accuracy for a confusion set."""
    conn = get_db()
    now = datetime.now().isoformat()
    row = conn.execute(
        "SELECT * FROM confusion_set_state WHERE user_token = ? AND confusion_set_key = ?",
        (user_token, confusion_set_key)
    ).fetchone()

    if row:
        conn.execute("""
            UPDATE confusion_set_state
            SET times_tested = times_tested + 1,
                discrimination_correct = discrimination_correct + ?,
                last_tested = ?
            WHERE user_token = ? AND confusion_set_key = ?
        """, (1 if was_correct else 0, now, user_token, confusion_set_key))
    else:
        conn.execute("""
            INSERT INTO confusion_set_state
            (user_token, confusion_set_key, times_tested, discrimination_correct, last_tested)
            VALUES (?, ?, 1, ?, ?)
        """, (user_token, confusion_set_key, 1 if was_correct else 0, now))

    conn.commit()
    conn.close()


def get_confusion_set_states(user_token):
    """Get all confusion set states for a user."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM confusion_set_state WHERE user_token = ?",
        (user_token,)
    ).fetchall()
    conn.close()
    return {r["confusion_set_key"]: dict(r) for r in rows}


# ─── ENHANCED DASHBOARD METRICS ──────────────────────────────────────

def get_delayed_retention(user_token):
    """Accuracy on exercises re-attempted after 24h/7d/30d delays."""
    conn = get_db()
    results = {}
    for label, min_hours, max_hours in [("24h", 20, 48), ("7d", 144, 216), ("30d", 648, 792)]:
        row = conn.execute("""
            SELECT COUNT(*) as total, SUM(a2.correct) as correct_count
            FROM attempts a1
            JOIN attempts a2 ON a1.user_token = a2.user_token
                AND a1.template_id = a2.template_id
                AND a2.id > a1.id
                AND a2.attempted_at > datetime(a1.attempted_at, '+' || ? || ' hours')
                AND a2.attempted_at < datetime(a1.attempted_at, '+' || ? || ' hours')
            WHERE a1.user_token = ? AND a1.correct = 1
        """, (min_hours, max_hours, user_token)).fetchone()
        total = row["total"] or 0
        correct = row["correct_count"] or 0
        results[label] = round(correct / total * 100, 1) if total > 0 else None
    conn.close()
    return results


def get_transfer_scores(user_token):
    """Performance breakdown by transfer stage."""
    conn = get_db()
    rows = conn.execute("""
        SELECT transfer_stage,
               COUNT(*) as total,
               SUM(correct) as correct_count
        FROM attempts
        WHERE user_token = ? AND transfer_stage IS NOT NULL
        GROUP BY transfer_stage
    """, (user_token,)).fetchall()
    conn.close()
    return {r["transfer_stage"]: {
        "total": r["total"],
        "correct": r["correct_count"] or 0,
        "accuracy": round((r["correct_count"] or 0) / r["total"] * 100, 1) if r["total"] > 0 else 0
    } for r in rows}


def get_fluency_score(user_token):
    """Accuracy when response time is below median (speed + accuracy)."""
    conn = get_db()
    count_row = conn.execute(
        "SELECT COUNT(*) as c FROM exercise_timing WHERE user_token = ?",
        (user_token,)
    ).fetchone()
    total_count = count_row["c"]
    if total_count < 4:
        conn.close()
        return None

    median_row = conn.execute("""
        SELECT duration_ms FROM exercise_timing
        WHERE user_token = ?
        ORDER BY duration_ms
        LIMIT 1 OFFSET ?
    """, (user_token, total_count // 2)).fetchone()
    if not median_row:
        conn.close()
        return None

    median = median_row["duration_ms"]
    fast_row = conn.execute("""
        SELECT COUNT(*) as total, SUM(actual_correct) as correct_count
        FROM exercise_timing
        WHERE user_token = ? AND duration_ms < ?
    """, (user_token, median)).fetchone()
    conn.close()

    total = fast_row["total"] or 0
    correct = fast_row["correct_count"] or 0
    return round(correct / total * 100, 1) if total > 0 else None


def get_confidence_calibration(user_token):
    """How well predicted_correct matches actual_correct."""
    conn = get_db()
    rows = conn.execute("""
        SELECT predicted_correct, actual_correct, COUNT(*) as count
        FROM exercise_timing
        WHERE user_token = ? AND predicted_correct IS NOT NULL
        GROUP BY predicted_correct, actual_correct
    """, (user_token,)).fetchall()
    conn.close()

    if not rows:
        return None

    total = sum(r["count"] for r in rows)
    overconf = sum(r["count"] for r in rows
                   if r["predicted_correct"] == 1 and r["actual_correct"] == 0)
    underconf = sum(r["count"] for r in rows
                    if r["predicted_correct"] == 0 and r["actual_correct"] == 1)

    return {
        "overconfidence_pct": round(overconf / total * 100, 1) if total > 0 else 0,
        "underconfidence_pct": round(underconf / total * 100, 1) if total > 0 else 0,
        "calibration_score": round((1 - (overconf + underconf) / total) * 100, 1) if total > 0 else 0
    }


def get_scaffold_dependence(user_token):
    """Gap between chip-mode and typed-mode accuracy."""
    conn = get_db()
    rows = conn.execute("""
        SELECT COALESCE(t.input_mode, 'chip') as mode,
               COUNT(*) as total,
               SUM(a.correct) as correct_count
        FROM attempts a
        LEFT JOIN exercise_timing t ON a.id = t.attempt_id
        WHERE a.user_token = ?
        GROUP BY mode
    """, (user_token,)).fetchall()
    conn.close()

    by_mode = {}
    for r in rows:
        mode = r["mode"] or "chip"
        by_mode[mode] = round((r["correct_count"] or 0) / r["total"] * 100, 1) if r["total"] > 0 else 0

    gap = abs(by_mode.get("chip", 0) - by_mode.get("typed", 0))
    return {"by_mode": by_mode, "gap": round(gap, 1)}


def get_recent_error_categories(user_token, limit=10):
    """Get the most recent error categories for adaptive selection."""
    conn = get_db()
    rows = conn.execute("""
        SELECT DISTINCT error_category FROM error_log
        WHERE user_token = ?
        ORDER BY logged_at DESC
        LIMIT ?
    """, (user_token, limit)).fetchall()
    conn.close()
    return [r["error_category"] for r in rows]


def get_all_transfer_progress(user_token):
    """Get transfer progress for all rules for a user."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM transfer_progress WHERE user_token = ?",
        (user_token,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_mastered_exercise_ids(user_token, module=None):
    """Return set of exercise IDs the user answered correctly (never failed).

    An exercise is 'mastered' if the user has attempted it at least once
    and has NEVER answered it incorrectly.
    """
    conn = get_db()
    query = """
        SELECT template_id
        FROM attempts
        WHERE user_token = ?
    """
    params = [user_token]
    if module:
        query += " AND module = ?"
        params.append(module)

    query += """
        GROUP BY template_id
        HAVING MIN(correct) = 1
    """
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {r["template_id"] for r in rows}


def get_attempted_exercise_ids(user_token, module=None):
    """Return set of exercise IDs the user has attempted at least once."""
    conn = get_db()
    query = "SELECT DISTINCT template_id FROM attempts WHERE user_token = ?"
    params = [user_token]
    if module:
        query += " AND module = ?"
        params.append(module)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {r["template_id"] for r in rows}


def get_recent_failed_rules(user_token, module=None, limit=5):
    """Return the grammar rule IDs (topics) from recent incorrect attempts.

    Used to reinforce the same rule with follow-up exercises.
    """
    conn = get_db()
    query = """
        SELECT DISTINCT a.template_id, e.error_category
        FROM attempts a
        LEFT JOIN error_log e ON e.user_token = a.user_token
            AND e.template_id = a.template_id
        WHERE a.user_token = ? AND a.correct = 0
    """
    params = [user_token]
    if module:
        query += " AND a.module = ?"
        params.append(module)
    query += " ORDER BY a.attempted_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_failed_exercise_topics(user_token, module=None, limit=3):
    """Return topics from the user's most recent failures for reinforcement.

    Returns a list of topic strings (e.g., 'dass_clause', 'relativpronomen_akk').
    """
    conn = get_db()
    # Get the topics of recently-failed exercises by joining with grammar_rules
    # or just pull from attempts directly
    query = """
        SELECT DISTINCT
            json_extract(errors_json, '$[0].category') as error_cat,
            module
        FROM attempts
        WHERE user_token = ? AND correct = 0
    """
    params = [user_token]
    if module:
        query += " AND module = ?"
        params.append(module)
    query += " ORDER BY attempted_at DESC LIMIT ?"
    params.append(limit * 2)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Also get topics from the grammar_rules table for recently-tested low-scoring rules
    conn2 = get_db()
    query2 = """
        SELECT rule_id, module FROM grammar_rules
        WHERE user_token = ? AND times_correct < times_tested
    """
    params2 = [user_token]
    if module:
        query2 += " AND module = ?"
        params2.append(module)
    query2 += " ORDER BY last_tested DESC LIMIT ?"
    params2.append(limit)
    rows2 = conn2.execute(query2, params2).fetchall()
    conn2.close()

    topics = []
    for r in rows2:
        if r["rule_id"] not in topics:
            topics.append(r["rule_id"])
    return topics[:limit]


# ─── INPUT LAB ─────────────────────────────────────────────────────────

def create_input_text(user_token, title, raw_text, sentences,
                      difficulty_score, word_count, unknown_count,
                      translations=None):
    """Create an input text and its segments. Returns text_id.

    translations: optional dict mapping sentence text → English translation.
    """
    conn = get_db()
    cur = conn.execute(
        """INSERT INTO input_texts
           (user_token, title, raw_text, sentences_json,
            difficulty_score, word_count, unknown_word_count)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_token, title, raw_text, json.dumps(sentences, ensure_ascii=False),
         difficulty_score, word_count, unknown_count)
    )
    text_id = cur.lastrowid
    translations = translations or {}
    for i, sent in enumerate(sentences):
        eng = translations.get(sent, "")
        conn.execute(
            """INSERT INTO input_segments
               (user_token, text_id, sentence_index, sentence_text, english)
               VALUES (?, ?, ?, ?, ?)""",
            (user_token, text_id, i, sent, eng)
        )
    conn.commit()
    conn.close()
    return text_id


def get_input_text(text_id, user_token=None):
    """Fetch a single input text with its segments."""
    conn = get_db()
    query = "SELECT * FROM input_texts WHERE id = ?"
    params = [text_id]
    if user_token:
        query += " AND user_token = ?"
        params.append(user_token)
    text_row = conn.execute(query, params).fetchone()
    if not text_row:
        conn.close()
        return None
    text = dict(text_row)
    text["sentences"] = json.loads(text["sentences_json"])

    segments = conn.execute(
        """SELECT * FROM input_segments
           WHERE text_id = ? AND user_token = ?
           ORDER BY sentence_index""",
        (text_id, text["user_token"])
    ).fetchall()
    text["segments"] = [dict(s) for s in segments]
    conn.close()
    return text


def get_input_texts(user_token):
    """List all input texts for a user."""
    conn = get_db()
    rows = conn.execute(
        """SELECT id, title, difficulty_score, word_count, unknown_word_count,
                  status, created_at
           FROM input_texts WHERE user_token = ?
           ORDER BY created_at DESC""",
        (user_token,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_segment_read(segment_id, user_token):
    """Mark a segment as read."""
    conn = get_db()
    conn.execute(
        "UPDATE input_segments SET read_at = ? WHERE id = ? AND user_token = ?",
        (datetime.now().isoformat(), segment_id, user_token)
    )
    conn.commit()
    conn.close()


def mark_segment_drilled(segment_id, user_token, was_correct):
    """Mark a segment as drilled and update SM-2 scheduling."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM input_segments WHERE id = ? AND user_token = ?",
        (segment_id, user_token)
    ).fetchone()
    if not row:
        conn.close()
        return

    seg = dict(row)
    ef = seg["ease_factor"]
    interval = seg["interval_days"]

    if was_correct:
        ef = max(1.3, ef + 0.1)
        interval = interval * ef
    else:
        ef = max(1.3, ef - 0.2)
        interval = 1

    now = datetime.now()
    next_review = (now + timedelta(days=interval)).isoformat()

    conn.execute(
        """UPDATE input_segments
           SET drilled = 1, drill_correct = ?, ease_factor = ?,
               interval_days = ?, next_review = ?, last_reviewed = ?
           WHERE id = ? AND user_token = ?""",
        (1 if was_correct else 0, ef, interval, next_review,
         now.isoformat(), segment_id, user_token)
    )
    conn.commit()
    conn.close()


def mine_word_from_text(user_token, text_id, word, phrase, definition,
                        examples, source_sentence):
    """Mine a word from an input text. Enforces max 5 per text."""
    conn = get_db()
    count = conn.execute(
        "SELECT COUNT(*) as c FROM input_mined_words WHERE user_token = ? AND text_id = ?",
        (user_token, text_id)
    ).fetchone()["c"]
    if count >= 5:
        conn.close()
        return {"error": "Maximum 5 words per text", "count": count}

    try:
        conn.execute(
            """INSERT INTO input_mined_words
               (user_token, text_id, word, phrase, definition, examples, source_sentence)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_token, text_id, word, phrase, definition, examples, source_sentence)
        )
        conn.commit()
        new_count = count + 1
    except Exception:
        conn.close()
        return {"error": "Word already mined", "count": count}

    conn.close()

    # Also save to global saved_words
    save_word(user_token, word, definition, examples, source_sentence)

    return {"count": new_count}


def get_mined_words(user_token, text_id):
    """Get mined words for a text."""
    conn = get_db()
    rows = conn.execute(
        """SELECT * FROM input_mined_words
           WHERE user_token = ? AND text_id = ?
           ORDER BY saved_at""",
        (user_token, text_id)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_segments_for_drill(text_id, user_token, limit=1):
    """Get segments for bridge drills: undrilled first, then due for review."""
    conn = get_db()
    now = datetime.now().isoformat()

    # First: undrilled segments that have been read
    rows = conn.execute(
        """SELECT * FROM input_segments
           WHERE text_id = ? AND user_token = ? AND drilled = 0
                 AND read_at IS NOT NULL
           ORDER BY sentence_index LIMIT ?""",
        (text_id, user_token, limit)
    ).fetchall()

    if not rows:
        # Then: segments due for review
        rows = conn.execute(
            """SELECT * FROM input_segments
               WHERE text_id = ? AND user_token = ?
                     AND next_review IS NOT NULL AND next_review <= ?
               ORDER BY next_review ASC LIMIT ?""",
            (text_id, user_token, now, limit)
        ).fetchall()

    conn.close()
    return [dict(r) for r in rows]


def get_input_text_stats(text_id, user_token):
    """Get stats for a text: segments read, drilled, mined words."""
    conn = get_db()
    total = conn.execute(
        "SELECT COUNT(*) as c FROM input_segments WHERE text_id = ? AND user_token = ?",
        (text_id, user_token)
    ).fetchone()["c"]
    read_count = conn.execute(
        "SELECT COUNT(*) as c FROM input_segments WHERE text_id = ? AND user_token = ? AND read_at IS NOT NULL",
        (text_id, user_token)
    ).fetchone()["c"]
    drilled = conn.execute(
        "SELECT COUNT(*) as c FROM input_segments WHERE text_id = ? AND user_token = ? AND drilled = 1",
        (text_id, user_token)
    ).fetchone()["c"]
    correct = conn.execute(
        "SELECT COUNT(*) as c FROM input_segments WHERE text_id = ? AND user_token = ? AND drill_correct = 1",
        (text_id, user_token)
    ).fetchone()["c"]
    mined = conn.execute(
        "SELECT COUNT(*) as c FROM input_mined_words WHERE text_id = ? AND user_token = ?",
        (text_id, user_token)
    ).fetchone()["c"]
    conn.close()
    return {
        "total_segments": total,
        "read": read_count,
        "drilled": drilled,
        "drill_correct": correct,
        "mined_words": mined,
    }


def delete_input_text(text_id, user_token):
    """Delete an input text and all its segments and mined words."""
    conn = get_db()
    conn.execute("DELETE FROM input_mined_words WHERE text_id = ? AND user_token = ?",
                 (text_id, user_token))
    conn.execute("DELETE FROM input_segments WHERE text_id = ? AND user_token = ?",
                 (text_id, user_token))
    conn.execute("DELETE FROM input_texts WHERE id = ? AND user_token = ?",
                 (text_id, user_token))
    conn.commit()
    conn.close()


def get_user_known_words(user_token):
    """Build the set of words the user knows from saved_words + mined_words."""
    conn = get_db()
    saved = conn.execute(
        "SELECT word FROM saved_words WHERE user_token = ?",
        (user_token,)
    ).fetchall()
    mined = conn.execute(
        "SELECT word FROM input_mined_words WHERE user_token = ?",
        (user_token,)
    ).fetchall()
    conn.close()
    known = set()
    for r in saved:
        known.add(r["word"].lower())
    for r in mined:
        known.add(r["word"].lower())
    return known


def get_scaffold_level(user_token):
    """Return the user's scaffold level (0, 1, or 2). Default 0."""
    conn = get_db()
    row = conn.execute(
        "SELECT level FROM user_scaffold WHERE user_token = ?",
        (user_token,)
    ).fetchone()
    conn.close()
    return row["level"] if row else 0


def set_scaffold_level(user_token, level):
    """Set the user's scaffold level (0, 1, or 2)."""
    level = max(0, min(2, int(level)))
    conn = get_db()
    conn.execute(
        """INSERT INTO user_scaffold (user_token, level) VALUES (?, ?)
           ON CONFLICT(user_token) DO UPDATE SET level = ?""",
        (user_token, level, level)
    )
    conn.commit()
    conn.close()
