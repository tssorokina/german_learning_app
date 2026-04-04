"""
German Grammar Exercise Banks — Consolidated Package.

Each module file contains a bank of exercises for one grammar topic.
This __init__.py re-exports the banks so other parts of the app can
import from a single location.

Usage:
    from exercises import VERB_POSITION_BANK, ADJEKTIVE_BANK, ...
    from exercises import ALL_EXERCISE_BANKS  # dict of module_key -> list
"""

from exercises.verb_position import (
    VERB_POSITION_BANK,
    GENERATED_VERB_EXERCISES,
    ORIGINAL_VERB_EXERCISES,
)
from exercises.adjektive import ADJEKTIVE_BANK
from exercises.konnektoren import KONNEKTOREN_BANK
from exercises.passiv import PASSIV_BANK
from exercises.konjunktiv import KONJUNKTIV_BANK
from exercises.relativ import RELATIV_BANK
from exercises.praepositionen import PRAEPOSITIONEN_BANK
from exercises.nominalisierung import NOMINALISIERUNG_BANK

# Convert verb_position exercises from legacy format to unified format
# so they work with the grammar module route (/grammar/verb_position)
_VERB_POSITION_UNIFIED = [
    {
        "id": ex["id"],
        "module": "verb_position",
        "type": "reconstruction",
        "level": ex["difficulty"],
        "topic": ex["clause_type"],
        "data": {
            "text": ex["text"],
            "english": ex.get("english", ""),
            "verbs": ex["verbs"],
            "clause_type": ex["clause_type"],
        },
        "grammar_rule": ex["explanation"],
        "grammar_tip": "",
    }
    for ex in VERB_POSITION_BANK
]

# Grammar module banks — all modules including verb_position
GRAMMAR_EXERCISE_BANKS = {
    "verb_position": _VERB_POSITION_UNIFIED,
    "adjektive": ADJEKTIVE_BANK,
    "konnektoren": KONNEKTOREN_BANK,
    "passiv": PASSIV_BANK,
    "konjunktiv": KONJUNKTIV_BANK,
    "relativ": RELATIV_BANK,
    "praepositionen": PRAEPOSITIONEN_BANK,
    "nominalisierung": NOMINALISIERUNG_BANK,
}

# All banks in their ORIGINAL format (verb_position stays in legacy format
# with top-level "text"/"verbs" keys, used by sentences.py / SENTENCE_BANK).
# Do NOT spread GRAMMAR_EXERCISE_BANKS here — its verb_position entry uses
# the unified format which would overwrite the legacy one and break prepare_exercise().
ALL_EXERCISE_BANKS = {
    "verb_position": VERB_POSITION_BANK,
    "adjektive": ADJEKTIVE_BANK,
    "konnektoren": KONNEKTOREN_BANK,
    "passiv": PASSIV_BANK,
    "konjunktiv": KONJUNKTIV_BANK,
    "relativ": RELATIV_BANK,
    "praepositionen": PRAEPOSITIONEN_BANK,
    "nominalisierung": NOMINALISIERUNG_BANK,
}
