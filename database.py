"""SQLite database layer for the German Verb-End Torture Chamber."""
import sqlite3
import os
import json
from datetime import datetime, date

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
    """)

    # Add module and exercise_type columns to attempts if missing
    try:
        conn.execute("SELECT module FROM attempts LIMIT 1")
    except Exception:
        conn.execute("ALTER TABLE attempts ADD COLUMN module TEXT DEFAULT 'verb_position'")
        conn.execute("ALTER TABLE attempts ADD COLUMN exercise_type TEXT DEFAULT 'reconstruction'")

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
                   module="verb_position", exercise_type="reconstruction"):
    conn = get_db()
    conn.execute(
        """INSERT INTO attempts (user_token, template_id, user_positions_json, correct, errors_json,
           module, exercise_type)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_token, template_id, json.dumps(user_positions), 1 if correct else 0,
         json.dumps(errors) if errors else None, module, exercise_type)
    )
    conn.commit()
    conn.close()


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
