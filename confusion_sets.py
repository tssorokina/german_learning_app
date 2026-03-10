"""
Confusion Sets — defines groups of grammar structures that learners commonly confuse.

Each confusion set specifies:
- The structures that contrast with each other
- Exercise filters for each side of the contrast
- The interleaving schedule (how to alternate)
"""

CONFUSION_SETS = {
    "weil_deshalb": {
        "name": "weil/dass (Verb-End) vs deshalb/trotzdem (V2-Inversion)",
        "sides": [
            {
                "label": "Verb-final (weil, dass, obwohl, wenn)",
                "filter": {"module": "konnektoren", "topic": "nebensatz_konnektor"},
                "error_categories": ["verb_not_at_end"]
            },
            {
                "label": "V2 inversion (deshalb, trotzdem, dennoch)",
                "filter": {"module": "konnektoren", "topic": "adverbial_konnektor"},
                "error_categories": ["inversion_missing"]
            }
        ],
        "interleave_pattern": "ABAB"
    },

    "relativ_vs_nebensatz": {
        "name": "Relativsatz vs. Nebensatz (Verschachtelung)",
        "sides": [
            {
                "label": "Relativsätze",
                "filter": {"module": "relativ"},
                "error_categories": ["wrong_relative_pronoun"]
            },
            {
                "label": "Nebensätze (weil/dass)",
                "filter": {"module": "konnektoren", "topic": "nebensatz_konnektor"},
                "error_categories": ["verb_not_at_end"]
            }
        ],
        "interleave_pattern": "ABAB"
    },

    "passiv_vs_nominalisierung": {
        "name": "Passiv vs. Nominalisierung (Transformationen)",
        "sides": [
            {
                "label": "Passivtransformationen",
                "filter": {"module": "passiv"},
                "error_categories": ["wrong_passive_form"]
            },
            {
                "label": "Nominalisierungen",
                "filter": {"module": "nominalisierung"},
                "error_categories": ["wrong_nominalization"]
            }
        ],
        "interleave_pattern": "AABB"
    },

    "wechselpraepositionen": {
        "name": "Wechselpräpositionen: Akkusativ (Wohin?) vs. Dativ (Wo?)",
        "sides": [
            {
                "label": "Akkusativ (Bewegung/Wohin?)",
                "filter": {"module": "praepositionen", "topic_contains": "akk"},
                "error_categories": ["wrong_preposition"]
            },
            {
                "label": "Dativ (Ort/Wo?)",
                "filter": {"module": "praepositionen", "topic_contains": "dat"},
                "error_categories": ["wrong_preposition"]
            }
        ],
        "interleave_pattern": "ABAB"
    },

    "adj_article_types": {
        "name": "Adjektivendungen nach Artikeltyp",
        "sides": [
            {
                "label": "Bestimmter Artikel",
                "filter": {"module": "adjektive", "topic": "adj_bestimmt"},
                "error_categories": ["wrong_adjective_ending"]
            },
            {
                "label": "Unbestimmter Artikel",
                "filter": {"module": "adjektive", "topic": "adj_unbestimmt"},
                "error_categories": ["wrong_adjective_ending"]
            },
            {
                "label": "Ohne Artikel",
                "filter": {"module": "adjektive", "topic": "adj_ohne_artikel"},
                "error_categories": ["wrong_adjective_ending"]
            }
        ],
        "interleave_pattern": "ABCABC"
    },
}


def get_confusion_sets_for_errors(error_categories):
    """Given a list of error categories, find relevant confusion set keys."""
    results = []
    for key, cset in CONFUSION_SETS.items():
        for side in cset["sides"]:
            if any(ec in side.get("error_categories", []) for ec in error_categories):
                results.append(key)
                break
    return results


def get_next_side(confusion_set_key, current_index):
    """Return the side filter for the next exercise in the interleave pattern."""
    cset = CONFUSION_SETS.get(confusion_set_key)
    if not cset:
        return None
    pattern = cset["interleave_pattern"]
    char = pattern[current_index % len(pattern)]
    side_index = ord(char) - ord('A')
    if side_index >= len(cset["sides"]):
        side_index = 0
    return cset["sides"][side_index]


def get_confusion_set_info(confusion_set_key):
    """Get name and side labels for a confusion set."""
    cset = CONFUSION_SETS.get(confusion_set_key)
    if not cset:
        return None
    return {
        "name": cset["name"],
        "sides": [s["label"] for s in cset["sides"]]
    }
