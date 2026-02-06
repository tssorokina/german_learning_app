"""
Error Analyzer — categorizes verb placement errors and generates explanations.

Error categories:
- verb_not_at_end: Verb placed in main-clause position instead of clause-end
- wrong_verb_order: Multiple verbs at end but in wrong sequence (e.g., hat gelesen vs gelesen hat)
- separable_not_joined: Separable verb not recombined in subordinate clause
- auxiliary_before_participle: Auxiliary placed before participle (should be after in Nebensatz)
- modal_before_infinitive: Modal placed before infinitive
- double_infinitive_error: Incorrect handling of Ersatzinfinitiv
- wrong_clause_assignment: Verb placed in the wrong clause entirely
- extra_verb_in_slot: More verbs placed than needed
"""

ERROR_CATEGORIES = {
    "verb_not_at_end": {
        "name": "Verb nicht am Satzende",
        "name_en": "Verb not at clause end",
        "description": "The conjugated verb must go to the end of a subordinate clause.",
        "tip": "In German subordinate clauses (after dass, weil, wenn, obwohl, etc.), the verb always moves to the final position.",
        "rule": "Nebensatz-Regel: Das konjugierte Verb steht am Ende des Nebensatzes."
    },
    "wrong_verb_order": {
        "name": "Falsche Verbreihenfolge",
        "name_en": "Wrong verb order at clause end",
        "description": "When multiple verbs appear at the end of a subordinate clause, they must be in the correct order.",
        "tip": "In Perfekt: Partizip + Hilfsverb (gelesen hat). With modals: Infinitiv + Modalverb (lesen kann).",
        "rule": "Reihenfolge am Satzende: Partizip vor Hilfsverb, Infinitiv vor Modalverb."
    },
    "auxiliary_before_participle": {
        "name": "Hilfsverb vor Partizip",
        "name_en": "Auxiliary before participle",
        "description": "In subordinate clauses, the past participle comes before the auxiliary verb.",
        "tip": "Correct: '...dass er das Buch gelesen hat' (not 'hat gelesen').",
        "rule": "Im Nebensatz: Partizip II + Hilfsverb (hat/ist) am Ende."
    },
    "modal_before_infinitive": {
        "name": "Modalverb vor Infinitiv",
        "name_en": "Modal before infinitive",
        "description": "In subordinate clauses, the infinitive comes before the modal verb.",
        "tip": "Correct: '...dass er kommen kann' (not 'kann kommen').",
        "rule": "Im Nebensatz: Infinitiv + Modalverb am Ende."
    },
    "double_infinitive_error": {
        "name": "Ersatzinfinitiv-Fehler",
        "name_en": "Double infinitive error",
        "description": "When a modal verb is used in Perfekt in a subordinate clause, 'hat' comes BEFORE the two infinitives.",
        "tip": "Exception! '...dass er hat kommen wollen' — 'hat' precedes the infinitives.",
        "rule": "Ersatzinfinitiv: hat/ist + Infinitiv + Infinitiv (hat kommen wollen)."
    },
    "wrong_clause_assignment": {
        "name": "Verb im falschen Teilsatz",
        "name_en": "Verb in wrong clause",
        "description": "The verb was placed in a different clause than where it belongs.",
        "tip": "Each subordinate clause has its own verb(s) at its end. Make sure you identify which clause each verb belongs to.",
        "rule": "Jeder Nebensatz hat sein eigenes Verb/seine eigenen Verben am Ende."
    },
    "separable_not_joined": {
        "name": "Trennbares Verb nicht zusammengesetzt",
        "name_en": "Separable verb not recombined",
        "description": "In subordinate clauses, separable verbs must be written as one word.",
        "tip": "In Nebensatz: 'ankommt' (not 'kommt...an').",
        "rule": "Im Nebensatz werden trennbare Verben zusammengeschrieben."
    }
}


def analyze_errors(exercise, user_positions):
    """
    Analyze what went wrong with the user's verb placement.

    Args:
        exercise: dict with 'slots', 'verbs', 'words', 'clause_type', 'explanation'
        user_positions: list of dicts [{"slot_index": int, "verb": str}, ...]

    Returns:
        list of error dicts with category, explanation, and detail
    """
    errors = []
    slots = exercise["slots"]
    correct_map = {s["index"]: s["correct_verb"] for s in slots}

    # Build what the user placed where
    user_map = {}
    for up in user_positions:
        slot_idx = up["slot_index"]
        # Find which word position this slot corresponds to
        if slot_idx < len(slots):
            word_pos = slots[slot_idx]["index"]
            user_map[word_pos] = up["verb"]

    # Check each slot
    for slot in slots:
        pos = slot["index"]
        expected = slot["correct_verb"]
        placed = user_map.get(pos)

        if placed is None:
            errors.append({
                "category": "verb_not_at_end",
                "expected": expected,
                "got": None,
                "position": pos,
                "detail": f"No verb placed at position {pos}. Expected '{expected}'."
            })
            continue

        if placed != expected:
            # Determine specific error type
            category = _classify_error(exercise, slot, placed, expected, user_map)
            errors.append({
                "category": category,
                "expected": expected,
                "got": placed,
                "position": pos,
                "detail": f"Expected '{expected}' at position {pos}, but got '{placed}'."
            })

    return errors


def _classify_error(exercise, slot, placed, expected, user_map):
    """Classify the specific type of error."""
    clause_type = exercise["clause_type"]
    verbs = exercise["verbs"]

    # Check if it's a verb order issue (both verbs present but swapped)
    if placed in verbs and expected in verbs:
        # Check if the placed verb belongs to another slot
        for s in exercise["slots"]:
            if s["correct_verb"] == placed and s["index"] != slot["index"]:
                # The verb the user placed here actually belongs elsewhere
                if "perfekt" in clause_type or "plusquam" in clause_type:
                    if placed in ("hat", "hatte", "ist", "war", "habe", "hätte", "wäre", "worden"):
                        return "auxiliary_before_participle"
                    return "wrong_verb_order"
                if "modal" in clause_type:
                    if placed in ("kann", "muss", "will", "soll", "darf", "möchte",
                                  "konnte", "musste", "wollte", "sollte", "durfte", "könnte"):
                        return "modal_before_infinitive"
                    return "wrong_verb_order"
                if "double_infinitive" in clause_type:
                    return "double_infinitive_error"
                return "wrong_verb_order"

    # Check if it's a wrong clause assignment (verb from different part of sentence)
    if placed in verbs:
        return "wrong_clause_assignment"

    return "verb_not_at_end"


def get_error_explanation(error):
    """Generate a user-friendly explanation for an error."""
    cat = error["category"]
    info = ERROR_CATEGORIES.get(cat, ERROR_CATEGORIES["verb_not_at_end"])

    return {
        "category": cat,
        "category_name": info["name"],
        "category_name_en": info["name_en"],
        "description": info["description"],
        "tip": info["tip"],
        "rule": info["rule"],
        "specific": error["detail"]
    }


def get_category_info(category):
    return ERROR_CATEGORIES.get(category)


def get_all_categories():
    return {k: v for k, v in ERROR_CATEGORIES.items()}
