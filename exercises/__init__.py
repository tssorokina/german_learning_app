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

# Grammar module banks (everything except verb_position which is handled
# separately via sentences.py)
GRAMMAR_EXERCISE_BANKS = {
    "adjektive": ADJEKTIVE_BANK,
    "konnektoren": KONNEKTOREN_BANK,
    "passiv": PASSIV_BANK,
    "konjunktiv": KONJUNKTIV_BANK,
    "relativ": RELATIV_BANK,
    "praepositionen": PRAEPOSITIONEN_BANK,
    "nominalisierung": NOMINALISIERUNG_BANK,
}

# All banks including verb_position (keyed by module name)
ALL_EXERCISE_BANKS = {
    "verb_position": VERB_POSITION_BANK,
    **GRAMMAR_EXERCISE_BANKS,
}
