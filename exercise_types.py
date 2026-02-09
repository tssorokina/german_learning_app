"""
Exercise Type Registry — abstracts different exercise mechanics.

Each exercise type defines its template, JS module, and checker function name.
New exercise types can be added here without modifying existing code.
"""

EXERCISE_TYPES = {
    "reconstruction": {
        "template": "exercise.html",
        "js_module": "app.js",
        "checker": "check_reconstruction",
        "label": "Satzrekonstruktion",
        "description": "Reconstruct the complete sentence from scrambled words."
    },
    "gap_fill": {
        "template": "gap_fill.html",
        "js_module": "gap_fill.js",
        "checker": "check_gap_fill",
        "label": "Lückentext",
        "description": "Fill in the correct ending or word in the gaps."
    },
    "transformation": {
        "template": "transformation.html",
        "js_module": "transformation.js",
        "checker": "check_transformation",
        "label": "Umformung",
        "description": "Transform the source sentence into the target structure."
    },
    "quick_select": {
        "template": "quick_select.html",
        "js_module": "quick_select.js",
        "checker": "check_quick_select",
        "label": "Schnellauswahl",
        "description": "Select the correct option from the choices."
    }
}

# Module definitions — each grammar module has a name, icon, and description
GRAMMAR_MODULES = {
    "verb_position": {
        "name": "Verbstellung",
        "name_en": "Verb Position",
        "description": "Verb placement in subordinate clauses",
        "exercise_type": "reconstruction",
        "levels": [1, 2, 3, 4],
        "color": "#6366f1"
    },
    "adjektive": {
        "name": "Adjektivdeklination",
        "name_en": "Adjective Declension",
        "description": "Adjective endings after articles",
        "exercise_type": "gap_fill",
        "levels": [1, 2, 3],
        "color": "#60a5fa"
    },
    "konnektoren": {
        "name": "Konnektoren",
        "name_en": "Connectors & Word Order",
        "description": "Connectors and sentence structure",
        "exercise_type": "reconstruction",
        "levels": [1, 2, 3, 4],
        "color": "#a78bfa"
    },
    "passiv": {
        "name": "Passiv",
        "name_en": "Passive Voice",
        "description": "Active to passive transformations",
        "exercise_type": "transformation",
        "levels": [2, 3, 4],
        "color": "#f472b6"
    },
    "konjunktiv": {
        "name": "Konjunktiv",
        "name_en": "Subjunctive Mood",
        "description": "Konjunktiv II and I forms",
        "exercise_type": "reconstruction",
        "levels": [2, 3, 4],
        "color": "#fb923c"
    },
    "relativ": {
        "name": "Relativsätze",
        "name_en": "Relative Clauses",
        "description": "Building relative clauses",
        "exercise_type": "reconstruction",
        "levels": [2, 3, 4],
        "color": "#4ade80"
    },
    "praepositionen": {
        "name": "Präpositionen",
        "name_en": "Prepositions & Cases",
        "description": "Prepositions with correct cases",
        "exercise_type": "quick_select",
        "levels": [1, 2, 3],
        "color": "#fbbf24"
    },
    "nominalisierung": {
        "name": "Nominalisierung",
        "name_en": "Nominalization",
        "description": "Clause-to-noun transformations",
        "exercise_type": "transformation",
        "levels": [3, 4],
        "color": "#f87171"
    }
}


def get_module_info(module_key):
    """Get info about a grammar module."""
    return GRAMMAR_MODULES.get(module_key)


def get_exercise_type_info(type_key):
    """Get info about an exercise type."""
    return EXERCISE_TYPES.get(type_key)


def get_all_modules():
    """Get all grammar modules."""
    return GRAMMAR_MODULES


def get_all_exercise_types():
    """Get all exercise types."""
    return EXERCISE_TYPES
