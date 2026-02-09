"""
Error Analyzer — categorizes errors across all exercise types and generates explanations.

Supports: verb placement, adjective declension, connectors, passive,
Konjunktiv, relative clauses, prepositions, nominalization.
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
    },
    "inversion_missing": {
        "name": "Fehlende Inversion",
        "name_en": "Missing inversion after adverbial connector",
        "description": "After adverbial connectors (deshalb, trotzdem, ...) the verb must come before the subject.",
        "tip": "Position 1: Konnektor -> Position 2: Verb -> Position 3: Subjekt",
        "rule": "Nach Adverbialkonnektoren steht das Verb an Position 2, vor dem Subjekt."
    },
    "konnektor_position": {
        "name": "Konnektorposition falsch",
        "name_en": "Connector at wrong position",
        "description": "Conjunctions (und, aber, denn) stand at Position 0 and don't change word order.",
        "tip": "und/aber/oder/denn/sondern = Position 0 (no inversion)\ndeshalb/trotzdem/deswegen = Position 1 (inversion!)",
        "rule": "Position 0: und, aber, oder, denn, sondern. Position 1: deshalb, trotzdem, außerdem."
    },
    "zweiteilig_incomplete": {
        "name": "Zweiteiliger Konnektor unvollständig",
        "name_en": "Two-part connector incomplete",
        "description": "Two-part connectors must be used as a pair.",
        "tip": "nicht nur ... sondern auch / entweder ... oder / weder ... noch",
        "rule": "Zweiteilige Konnektoren müssen paarweise verwendet werden."
    },
    "wrong_adjective_ending": {
        "name": "Falsche Adjektivendung",
        "name_en": "Wrong adjective ending",
        "description": "The adjective ending depends on the article type, case, and gender.",
        "tip": "Bestimmter Artikel: mostly -e/-en. Unbestimmter: shows gender in Nom. Ohne Artikel: strong endings.",
        "rule": "Adjektivdeklination: Artikel + Kasus + Genus = Endung (-e, -en, -er, -es, -em)."
    },
    "wrong_passive_form": {
        "name": "Falsche Passivform",
        "name_en": "Wrong passive construction",
        "description": "The passive requires werden + Partizip II (Vorgangspassiv) or sein + Partizip II (Zustandspassiv).",
        "tip": "Vorgangspassiv: werden + Part. II / Zustandspassiv: sein + Part. II",
        "rule": "Passiv: Subjekt + werden/sein + Partizip II (+ von + Dativ)."
    },
    "wrong_konjunktiv_form": {
        "name": "Falsche Konjunktivform",
        "name_en": "Wrong subjunctive form",
        "description": "The Konjunktiv form is incorrect for the context.",
        "tip": "K2: hätte/wäre/würde + Inf. K1 (indirekte Rede): habe/sei/könne",
        "rule": "Konjunktiv II: Irrealis. Konjunktiv I: Indirekte Rede."
    },
    "wrong_relative_pronoun": {
        "name": "Falsches Relativpronomen",
        "name_en": "Wrong relative pronoun",
        "description": "The relative pronoun must match the noun's gender and the clause's case requirement.",
        "tip": "Gender from noun, case from function in relative clause.",
        "rule": "Relativpronomen: Genus vom Bezugswort, Kasus von der Funktion im Relativsatz."
    },
    "wrong_preposition": {
        "name": "Falsche Präposition/Kasus",
        "name_en": "Wrong preposition or case",
        "description": "The preposition or the case after the preposition is incorrect.",
        "tip": "Wechselpräpositionen: Wohin? = Akk., Wo? = Dat.",
        "rule": "Präpositionen regieren einen bestimmten Kasus."
    },
    "wrong_nominalization": {
        "name": "Falsche Nominalisierung",
        "name_en": "Wrong nominalization",
        "description": "The transformation from clause to noun phrase is incorrect.",
        "tip": "weil es regnet -> wegen des Regens. obwohl -> trotz + Genitiv.",
        "rule": "Nominalisierung: Nebensatz -> Präposition + Nomen (Genitiv)."
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


def analyze_gap_fill_errors(exercise_data, user_answers):
    """
    Analyze errors for gap-fill exercises (adjective declension, Konjunktiv).

    Args:
        exercise_data: the exercise's 'data' dict with gaps
        user_answers: dict of {gap_position: user_answer}

    Returns:
        list of error dicts
    """
    errors = []
    for gap in exercise_data.get("gaps", []):
        pos = gap["position"]
        expected = gap["answer"]
        user_answer = user_answers.get(pos, "")

        if user_answer != expected:
            # Determine error category based on gap metadata
            if gap.get("article_type") is not None:
                category = "wrong_adjective_ending"
                detail = (f"Expected ending '-{expected}' but got '-{user_answer}'. "
                         f"({gap.get('article_type', '')} Artikel, "
                         f"{gap.get('case', '')}, {gap.get('gender', '')})")
            elif gap.get("indicative_hint"):
                category = "wrong_konjunktiv_form"
                detail = (f"Expected '{expected}' but got '{user_answer}'. "
                         f"Hint: {gap.get('indicative_hint', '')}")
            else:
                category = "wrong_adjective_ending"
                detail = f"Expected '{expected}' but got '{user_answer}'."

            errors.append({
                "category": category,
                "expected": expected,
                "got": user_answer,
                "position": pos,
                "detail": detail
            })

    return errors


def analyze_quick_select_errors(exercise_data, user_answers):
    """
    Analyze errors for quick-select exercises (prepositions).

    Args:
        exercise_data: the exercise's 'data' dict with gaps
        user_answers: dict of {gap_position: user_answer}

    Returns:
        list of error dicts
    """
    errors = []
    for gap in exercise_data.get("gaps", []):
        pos = gap["position"]
        expected = gap["answer"]
        user_answer = user_answers.get(pos, "")

        if user_answer != expected:
            errors.append({
                "category": "wrong_preposition",
                "expected": expected,
                "got": user_answer,
                "position": pos,
                "detail": f"Expected '{expected}' but got '{user_answer}'. "
                         f"{gap.get('explanation', '')}"
            })

    return errors


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
