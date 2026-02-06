"""
MCP Server for the Verb-End Torture Chamber.

Exposes tools to Claude for:
- Getting exercises
- Checking verb placement answers
- Viewing error stats
- Getting sentence bank info

Run with: python mcp_server.py
Connects via stdio (standard MCP transport).
"""
import json
import sys
import os

# Add parent dir to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentences import (get_exercise_by_difficulty, prepare_exercise,
                       get_template_by_id, SENTENCE_BANK, count_by_difficulty)
from error_analyzer import analyze_errors, get_error_explanation, get_all_categories
from database import (init_db, get_error_stats, get_user_summary,
                      record_attempt, log_error, schedule_retry)


# ─── MCP Protocol Implementation (stdio JSON-RPC) ──────────────────────

def send_response(id, result):
    msg = {"jsonrpc": "2.0", "id": id, "result": result}
    out = json.dumps(msg)
    sys.stdout.write(f"Content-Length: {len(out)}\r\n\r\n{out}")
    sys.stdout.flush()


def send_error(id, code, message):
    msg = {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}
    out = json.dumps(msg)
    sys.stdout.write(f"Content-Length: {len(out)}\r\n\r\n{out}")
    sys.stdout.flush()


def send_notification(method, params=None):
    msg = {"jsonrpc": "2.0", "method": method}
    if params:
        msg["params"] = params
    out = json.dumps(msg)
    sys.stdout.write(f"Content-Length: {len(out)}\r\n\r\n{out}")
    sys.stdout.flush()


TOOLS = [
    {
        "name": "get_exercise",
        "description": "Get a German verb placement exercise. The user must drag verbs to correct positions in subordinate clauses. Returns a sentence with blank slots and verbs to place.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "integer",
                    "description": "Difficulty level: 1=A2 (simple), 2=B1 (compound verbs), 3=B2 (nested clauses), 4=C1 (complex nesting). Omit for random.",
                    "enum": [1, 2, 3, 4]
                }
            }
        }
    },
    {
        "name": "check_answer",
        "description": "Check if verb placements are correct. Provide the template_id from get_exercise and the user's verb placements.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_id": {
                    "type": "string",
                    "description": "The template_id from the exercise"
                },
                "positions": {
                    "type": "array",
                    "description": "Array of {slot_index, verb} objects with the user's placements",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slot_index": {"type": "integer"},
                            "verb": {"type": "string"}
                        },
                        "required": ["slot_index", "verb"]
                    }
                }
            },
            "required": ["template_id", "positions"]
        }
    },
    {
        "name": "get_stats",
        "description": "Get user statistics: accuracy, streak, error categories, and summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_token": {
                    "type": "string",
                    "description": "User token (from the web session)"
                }
            },
            "required": ["user_token"]
        }
    },
    {
        "name": "get_sentence_bank_info",
        "description": "Get info about available sentences: total count, count by difficulty, and clause types covered.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "explain_rule",
        "description": "Explain a German verb placement rule for a specific clause type or error category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The clause type or error category to explain, e.g. 'dass_clause', 'double_infinitive', 'wrong_verb_order'"
                }
            },
            "required": ["topic"]
        }
    }
]


def handle_tool_call(name, arguments):
    if name == "get_exercise":
        difficulty = arguments.get("difficulty")
        exercise = get_exercise_by_difficulty(difficulty)
        if not exercise:
            return {"error": "No exercises available for this difficulty"}
        # Return exercise data for Claude to present to the user
        return {
            "template_id": exercise["template_id"],
            "display_text": exercise["display_text"],
            "verbs_to_place": exercise["verbs"],
            "num_slots": len(exercise["slots"]),
            "difficulty": exercise["difficulty"],
            "clause_type": exercise["clause_type"],
            "instruction": "Place these verbs in the correct blank positions. In German subordinate clauses, verbs move to the end."
        }

    elif name == "check_answer":
        template_id = arguments["template_id"]
        positions = arguments["positions"]

        template = get_template_by_id(template_id)
        if not template:
            return {"error": f"Unknown template: {template_id}"}

        exercise = prepare_exercise(template)
        errors = analyze_errors(exercise, positions)
        explanations = [get_error_explanation(e) for e in errors]

        return {
            "correct": len(errors) == 0,
            "full_correct_sentence": exercise["full_text"],
            "general_explanation": exercise["explanation"],
            "errors": explanations if errors else [],
            "correct_placements": [
                {"position": s["index"], "verb": s["correct_verb"]}
                for s in exercise["slots"]
            ]
        }

    elif name == "get_stats":
        user_token = arguments["user_token"]
        return {
            "summary": get_user_summary(user_token),
            "error_categories": get_error_stats(user_token)
        }

    elif name == "get_sentence_bank_info":
        return {
            "total_sentences": len(SENTENCE_BANK),
            "by_difficulty": count_by_difficulty(),
            "difficulty_labels": {"1": "A2", "2": "B1", "3": "B2", "4": "C1"},
            "clause_types": sorted(set(t["clause_type"] for t in SENTENCE_BANK))
        }

    elif name == "explain_rule":
        topic = arguments["topic"]
        # Check error categories
        cats = get_all_categories()
        if topic in cats:
            cat = cats[topic]
            return {
                "topic": topic,
                "name_de": cat["name"],
                "name_en": cat["name_en"],
                "description": cat["description"],
                "tip": cat["tip"],
                "rule": cat["rule"]
            }
        # Check if it matches a clause type
        examples = [t for t in SENTENCE_BANK if t["clause_type"] == topic]
        if examples:
            ex = examples[0]
            return {
                "topic": topic,
                "explanation": ex["explanation"],
                "example": ex["text"],
                "verbs": ex["verbs"],
                "difficulty": ex["difficulty"]
            }
        return {"error": f"Unknown topic: {topic}. Try a clause_type like 'dass_clause' or error category like 'wrong_verb_order'."}

    return {"error": f"Unknown tool: {name}"}


def read_message():
    """Read a JSON-RPC message from stdin using Content-Length header."""
    headers = {}
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.strip()
        if line == "":
            break
        if ":" in line:
            key, val = line.split(":", 1)
            headers[key.strip()] = val.strip()

    length = int(headers.get("Content-Length", 0))
    if length == 0:
        return None

    body = sys.stdin.read(length)
    return json.loads(body)


def main():
    init_db()

    while True:
        try:
            msg = read_message()
            if msg is None:
                break

            method = msg.get("method")
            id = msg.get("id")
            params = msg.get("params", {})

            if method == "initialize":
                send_response(id, {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "verb-end-torture-chamber",
                        "version": "1.0.0"
                    }
                })

            elif method == "notifications/initialized":
                pass  # Acknowledged

            elif method == "tools/list":
                send_response(id, {"tools": TOOLS})

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = handle_tool_call(tool_name, arguments)
                send_response(id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                })

            elif method == "ping":
                send_response(id, {})

            else:
                if id is not None:
                    send_error(id, -32601, f"Method not found: {method}")

        except Exception as e:
            sys.stderr.write(f"MCP Error: {e}\n")
            if 'id' in dir() and id is not None:
                send_error(id, -32603, str(e))


if __name__ == "__main__":
    main()
