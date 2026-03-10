"""
Transfer Task Chain — 4-stage progression for each grammar rule.

Stage 1 - Controlled drill: existing exercise types, same topic
Stage 2 - Near transfer: same structure, different vocabulary/context
Stage 3 - Far transfer: free-writing/speaking prompt (display-only)
Stage 4 - Delayed transfer: same concept, 7 days later
"""
import random

# Promotion thresholds
CONTROLLED_TO_NEAR = 3       # 3 correct controlled drills to advance
NEAR_TO_FAR = 2              # 2 correct near-transfer exercises to advance
FAR_TO_DELAYED = 1           # 1 completed far-transfer prompt to advance

STAGES = ["controlled", "near", "far", "delayed"]

# Far transfer prompts keyed by module
FAR_TRANSFER_PROMPTS = {
    "verb_position": [
        "Schreibe 3 Sätze über deinen Alltag mit weil, obwohl und dass.",
        "Erkläre einem Freund, warum du Deutsch lernst. Benutze mindestens 2 Nebensätze.",
    ],
    "konnektoren": [
        "Beschreibe deine Wochenendpläne mit deshalb, trotzdem und weil.",
        "Beschreibe eine Ursache-Wirkungs-Kette mit 3 verschiedenen Konnektoren.",
    ],
    "adjektive": [
        "Beschreibe deine Traumwohnung mit mindestens 5 Adjektiven (verschiedene Artikel).",
        "Schreibe eine kurze Produktbewertung mit Adjektiven nach bestimmtem, unbestimmtem und ohne Artikel.",
    ],
    "relativ": [
        "Beschreibe 3 Personen mit Relativsätzen im Nominativ, Akkusativ und Dativ.",
        "Schreibe 3 Sätze über deine Lieblingsstadt mit Relativsätzen.",
    ],
    "passiv": [
        "Schreibe diesen Absatz im Passiv um: 'Die Firma baut ein neues Büro. Die Arbeiter renovieren die Küche.'",
        "Beschreibe, wie ein Kuchen gebacken wird (Vorgangspassiv).",
    ],
    "praepositionen": [
        "Beschreibe den Weg von deinem Zuhause zur Arbeit mit Wechselpräpositionen (in, auf, an, über).",
        "Beschreibe dein Zimmer: Wo stehen die Möbel? Wohin hast du sie gestellt?",
    ],
    "nominalisierung": [
        "Wandle diese 3 Nebensätze in Nominalphrasen um: weil es regnete / obwohl er müde war / dass sie kommt.",
        "Schreibe einen formellen Beschwerdebrief mit mindestens 2 Nominalisierungen.",
    ],
    "konjunktiv": [
        "Schreibe 3 Wünsche mit Konjunktiv II und berichte, was jemand gesagt hat (Konjunktiv I).",
        "Was würdest du tun, wenn du Bürgermeister wärst? Schreibe 3 Sätze.",
    ],
}


def get_far_transfer_prompt(module):
    """Get a random far-transfer prompt for a module."""
    prompts = FAR_TRANSFER_PROMPTS.get(module, [])
    if prompts:
        return random.choice(prompts)
    return "Schreibe 3 Sätze zu diesem Grammatikthema."


def check_promotion(transfer_progress):
    """
    Check if a user should be promoted to the next transfer stage.
    Returns the new stage name if promotion is warranted, or None.
    """
    if not transfer_progress:
        return None

    stage = transfer_progress["current_stage"]

    if stage == "controlled":
        if transfer_progress["controlled_correct"] >= CONTROLLED_TO_NEAR:
            return "near"

    elif stage == "near":
        if transfer_progress["near_correct"] >= NEAR_TO_FAR:
            return "far"

    elif stage == "far":
        if transfer_progress["far_completed"] >= FAR_TO_DELAYED:
            return "delayed"

    return None


def get_current_stage_info(transfer_progress):
    """Get human-readable info about the current transfer stage."""
    if not transfer_progress:
        return {"stage": "controlled", "progress": "0/3", "label": "Controlled Drill"}

    stage = transfer_progress["current_stage"]
    labels = {
        "controlled": "Controlled Drill",
        "near": "Near Transfer",
        "far": "Free Writing",
        "delayed": "Delayed Review"
    }

    if stage == "controlled":
        progress = f"{transfer_progress['controlled_correct']}/{CONTROLLED_TO_NEAR}"
    elif stage == "near":
        progress = f"{transfer_progress['near_correct']}/{NEAR_TO_FAR}"
    elif stage == "far":
        progress = f"{transfer_progress['far_completed']}/{FAR_TO_DELAYED}"
    else:
        progress = f"{transfer_progress['delayed_correct']} reviewed"

    return {
        "stage": stage,
        "progress": progress,
        "label": labels.get(stage, stage)
    }
