"""
Dynamic exercise generation using Claude API.

On app startup, calls Claude to generate 20 fresh exercises per module.
Falls back to cached exercises (JSON file) if the API key is missing or the call fails.
"""

import os
import json
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Where to cache generated exercises
CACHE_DIR = Path(os.environ.get("DATA_DIR", ".")) / "generated"
CACHE_FILE = CACHE_DIR / "exercises_cache.json"

EXERCISES_PER_MODULE = 20

# ─── MODULE PROMPT TEMPLATES ─────────────────────────────────────────

VERB_POSITION_PROMPT = """Generate {count} German grammar exercises for VERB PLACEMENT IN SUBORDINATE CLAUSES.

These exercises test where the conjugated verb goes in subordinate clauses (dass, weil, wenn, obwohl, als, ob, damit, bevor, nachdem, während, relative clauses, nested clauses).

Distribute exercises across difficulty levels:
- Level 1 (A2): ~5 exercises. Simple subordinate clauses (dass, weil, wenn). 1 verb to place.
- Level 2 (B1): ~5 exercises. Relative clauses, compound verb forms (hat...gemacht). 1-2 verbs.
- Level 3 (B2): ~5 exercises. Nested subordinate clauses, separable verbs. 2-3 verbs.
- Level 4 (C1): ~5 exercises. Double infinitive, multiple nested clauses. 2-4 verbs.

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_vp_{n:03d}",
    "text": "Full correct German sentence.",
    "verbs": ["verb1", "verb2"],
    "clause_type": "dass_clause|weil_clause|wenn_clause|relative_clause|nested_clause|...",
    "difficulty": 1-4,
    "explanation": "Why the verb(s) go to the end in this sentence structure."
}}

CRITICAL RULES:
- "text" must be the complete, grammatically correct sentence
- "verbs" must list ONLY the verbs that the student needs to place (the ones that move to clause-end positions)
- Each verb in "verbs" must appear exactly as written in "text" (same case, conjugation)
- "explanation" must clearly explain the verb-end rule being tested
- Use natural, realistic German sentences (not textbook-sounding)
- Vary vocabulary: daily life, work, travel, culture, news, relationships
- Include proper German punctuation (commas before subordinate clauses)

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

ADJEKTIVE_PROMPT = """Generate {count} German grammar exercises for ADJECTIVE DECLENSION (Adjektivdeklination).

Distribute across difficulty levels:
- Level 1 (A2): ~7 exercises. Adjectives after bestimmter Artikel (der/die/das). Simple cases (Nom, Akk).
- Level 2 (B1): ~7 exercises. Adjectives after unbestimmter Artikel (ein/eine) and possessives. All cases including Dativ.
- Level 3 (B2): ~6 exercises. Adjectives without article (starke Deklination), Genitiv, multiple adjectives.

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_adj_{n:03d}",
    "module": "adjektive",
    "type": "gap_fill",
    "level": 1-3,
    "topic": "adj_bestimmt|adj_unbestimmt|adj_possessiv|adj_ohne_artikel|adj_genitiv|adj_multiple",
    "data": {{
        "sentence_template": "Sentence with {{gap_1}} marking where the ending goes. E.g. 'Ich kaufe den neu{{gap_1}} Pullover.'",
        "gaps": [
            {{
                "position": "gap_1",
                "context": "neu__",
                "answer": "en",
                "article_type": "bestimmt|unbestimmt|possessiv|ohne",
                "case": "Nominativ|Akkusativ|Dativ|Genitiv",
                "gender": "maskulin|feminin|neutrum|plural",
                "options": ["e", "en", "er", "es", "em"]
            }}
        ],
        "full_correct": "Ich kaufe den neuen Pullover."
    }},
    "grammar_rule": "Clear rule: After [article type], [case] [gender] -> -[ending]",
    "grammar_tip": "Short mnemonic for the student"
}}

CRITICAL RULES:
- The gap marker {{gap_N}} replaces ONLY the adjective ending (not the whole word)
- "context" shows the adjective stem with __ for the missing ending
- "answer" is just the ending (e.g. "en", "e", "er", "em", "es")
- "options" must always include the correct answer plus 4 plausible distractors from: ["e", "en", "er", "es", "em"]
- "full_correct" is the complete sentence with correct endings filled in
- Use natural, varied vocabulary (food, clothing, travel, nature, people, city)
- Adjective endings must be grammatically correct per German declension tables

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

KONNEKTOREN_PROMPT = """Generate {count} German grammar exercises for CONNECTORS & WORD ORDER (Konnektoren & Satzstellung).

Distribute across difficulty levels:
- Level 1 (A2): ~5 exercises. Hauptsatz-Konnektoren (und, aber, oder, denn, sondern) - Position 0, no inversion.
- Level 2 (B1): ~5 exercises. Nebensatz-Konnektoren (weil, dass, obwohl, wenn) - verb to end. Adverbial connectors (deshalb, trotzdem, deswegen) - inversion.
- Level 3 (B2): ~5 exercises. Two-part connectors (entweder...oder, sowohl...als auch, je...desto, nicht nur...sondern auch, zwar...aber).
- Level 4 (C1): ~5 exercises. Complex multi-clause sentences with mixed connector types.

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_kon_{n:03d}",
    "module": "konnektoren",
    "type": "reconstruction",
    "level": 1-4,
    "topic": "hauptsatz_konnektor|nebensatz_konnektor|adverbial_konnektor|zweiteilig_konnektor|complex_konnektoren",
    "data": {{
        "text": "Full correct German sentence with connector.",
        "verbs": ["verb1", "verb2"],
        "clause_type": "aber_hauptsatz|deshalb_inversion|weil_nebensatz|zweiteilig|complex_mixed"
    }},
    "grammar_rule": "Clear explanation of why the word order is the way it is.",
    "grammar_tip": "Short mnemonic about connector position rules"
}}

CRITICAL RULES:
- "text" must be the complete, grammatically correct sentence
- "verbs" must list the key verbs the student needs to place correctly
- Each verb in "verbs" must appear exactly as written in "text"
- For Nebensatz connectors: verb must be at the end of the clause
- For adverbial connectors: verb-subject inversion in the second clause
- For Position 0 connectors: normal SVO order after the connector
- Use natural, varied sentences

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

PASSIV_PROMPT = """Generate {count} German grammar exercises for PASSIVE VOICE (Passiv).

Distribute across difficulty levels:
- Level 2 (B1): ~7 exercises. Vorgangspassiv Präsens (werden + Partizip II). Simple active->passive.
- Level 3 (B2): ~7 exercises. Vorgangspassiv Präteritum/Perfekt, Zustandspassiv (sein + Partizip II).
- Level 4 (C1): ~6 exercises. Passiversatzformen (man, sich lassen, -bar/-lich adjectives).

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_pass_{n:03d}",
    "module": "passiv",
    "type": "transformation",
    "level": 2-4,
    "topic": "vorgangspassiv_praesens|vorgangspassiv_praeteritum|zustandspassiv|passiv_ersatzform",
    "data": {{
        "source": "Active sentence in German.",
        "target_words": ["Word1", "Word2", "wird", "von", "dem", "Subjekt", "gemacht"],
        "correct_order": "Word1 Word2 wird von dem Subjekt gemacht.",
        "optional_words": ["von", "dem", "Subjekt"],
        "transform_type": "aktiv_zu_passiv|aktiv_zu_zustandspassiv|passiv_zu_ersatzform"
    }},
    "grammar_rule": "Rule explanation for this passive construction",
    "grammar_tip": "Short mnemonic"
}}

CRITICAL RULES:
- "source" is the original active voice sentence
- "target_words" is the passive sentence split into individual words (NO punctuation in the words)
- "correct_order" is the full passive sentence with proper punctuation
- "optional_words" lists words that might be omitted (agent phrases like "vom Lehrer")
- The passive transformation must be grammatically correct
- For Vorgangspassiv: Akkusativ-Objekt -> Subjekt, werden + Partizip II
- For Zustandspassiv: sein + Partizip II (result state)
- Use varied, natural sentences

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

KONJUNKTIV_PROMPT = """Generate {count} German grammar exercises for KONJUNKTIV II (Subjunctive Mood).

Distribute across difficulty levels and types:
- Level 2 (B1): ~6 RECONSTRUCTION exercises. würde+Infinitiv, wenn-clauses with hätte/wäre.
- Level 3 (B2): ~6 RECONSTRUCTION exercises. Konjunktiv II Vergangenheit (hätte/wäre + Partizip II), als ob + Konjunktiv.
- Level 4 (C1): ~4 GAP_FILL exercises. Konjunktiv I (indirect speech) and Konjunktiv II special forms.
- Level 4 (C1): ~4 RECONSTRUCTION exercises. Complex Konjunktiv with nested clauses.

For RECONSTRUCTION exercises, use this structure:
{{
    "id": "gen_konj_{n:03d}",
    "module": "konjunktiv",
    "type": "reconstruction",
    "level": 2-4,
    "topic": "wuerde_infinitiv|konjunktiv_wenn|wunsch|konjunktiv_vergangenheit|als_ob_konjunktiv",
    "data": {{
        "text": "Full correct German sentence with Konjunktiv.",
        "verbs": ["hätte", "würde", "machen"],
        "clause_type": "konjunktiv_wenn|wunsch|konjunktiv_vergangenheit|als_ob_konjunktiv"
    }},
    "grammar_rule": "Rule explanation for this Konjunktiv form.",
    "grammar_tip": "Short mnemonic"
}}

For GAP_FILL exercises (Konjunktiv I / special forms), use this structure:
{{
    "id": "gen_konj_{n:03d}",
    "module": "konjunktiv",
    "type": "gap_fill",
    "level": 4,
    "topic": "konjunktiv_1|konjunktiv_2_spezial",
    "data": {{
        "sentence_template": "Er sagte, er {{gap_1}} keine Zeit.",
        "gaps": [
            {{
                "position": "gap_1",
                "context": "er ___ keine Zeit",
                "answer": "habe",
                "options": ["hat", "habe", "hätte", "hatte", "haben"],
                "indicative_hint": "er hat -> Konjunktiv I?"
            }}
        ],
        "full_correct": "Er sagte, er habe keine Zeit."
    }},
    "grammar_rule": "Rule for this Konjunktiv form.",
    "grammar_tip": "Short mnemonic"
}}

CRITICAL RULES:
- For reconstruction: "verbs" must list verbs exactly as in "text"
- For gap_fill: the gap replaces the ENTIRE Konjunktiv verb form
- Konjunktiv II forms: wäre, hätte, würde+Inf, käme, ginge, etc.
- Konjunktiv II Past: hätte/wäre + Partizip II
- Konjunktiv I: sei, habe, komme, gehe (indirect speech)
- Use varied, natural sentences about wishes, hypotheticals, reported speech

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

RELATIV_PROMPT = """Generate {count} German grammar exercises for RELATIVE CLAUSES (Relativsätze).

Distribute across difficulty levels:
- Level 2 (B1): ~7 exercises. Nominativ and Akkusativ relative pronouns (der/die/das/den).
- Level 3 (B2): ~7 exercises. Dativ relative pronouns (dem/der/denen), with prepositions (in dem, mit der).
- Level 4 (C1): ~6 exercises. Genitiv (dessen/deren), was/wo relative clauses, nested relatives.

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_rel_{n:03d}",
    "module": "relativ",
    "type": "reconstruction",
    "level": 2-4,
    "topic": "relativpronomen_nom|relativpronomen_akk|relativpronomen_dat|relativpronomen_praep|relativpronomen_gen|relativsatz_was|verschachtelt",
    "data": {{
        "text": "Der Mann, der neben mir wohnt, ist Arzt.",
        "verbs": ["wohnt", "ist"],
        "clause_type": "relativsatz_nom|relativsatz_akk|relativsatz_dat|relativsatz_praep|relativsatz_gen|relativsatz_was|verschachtelte_relativsaetze",
        "sentence_a": "Der Mann ist Arzt.",
        "sentence_b": "Der Mann wohnt neben mir."
    }},
    "grammar_rule": "Which relative pronoun and why (case, gender, number).",
    "grammar_tip": "Short mnemonic"
}}

CRITICAL RULES:
- "text" is the combined sentence with the relative clause properly embedded
- "verbs" lists the key verbs (must match exactly in "text")
- "sentence_a" and "sentence_b" are the two source sentences that get combined
- The relative pronoun must match the gender/number of the antecedent and the case required by its function in the relative clause
- Relative clause verb goes to the END of the clause
- Include commas around the relative clause
- Use varied, natural sentences

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

PRAEPOSITIONEN_PROMPT = """Generate {count} German grammar exercises for PREPOSITIONS & CASES (Präpositionen & Kasus).

Distribute across difficulty levels:
- Level 1 (A2): ~7 exercises. Wechselpräpositionen (in, auf, an, über, unter, vor, hinter, neben, zwischen) with Akkusativ (Wohin?) vs Dativ (Wo?).
- Level 2 (B1): ~7 exercises. Fixed-case prepositions: Akkusativ (für, durch, gegen, ohne, um, bis), Dativ (mit, nach, aus, bei, seit, von, zu, gegenüber).
- Level 3 (B2): ~6 exercises. Genitiv prepositions (wegen, trotz, während, anstatt), verb+preposition idioms (warten auf, sich freuen über).

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_praep_{n:03d}",
    "module": "praepositionen",
    "type": "quick_select",
    "level": 1-3,
    "topic": "wechselpraep|akkusativ_praep|dativ_praep|genitiv_praep|verb_praep",
    "data": {{
        "sentence": "Die Katze springt {{gap_1}} Tisch.",
        "gaps": [
            {{
                "position": "gap_1",
                "options": ["auf den", "auf dem", "auf das", "an den"],
                "answer": "auf den",
                "explanation": "Wohin? -> Akkusativ (Bewegung). Tisch = maskulin -> den"
            }}
        ]
    }},
    "grammar_rule": "Rule about this preposition and its case requirement.",
    "grammar_tip": "Short mnemonic"
}}

CRITICAL RULES:
- The gap {{gap_N}} in "sentence" replaces the preposition+article combination
- "options" must have 3-4 plausible choices with the correct preposition+case combo
- "answer" must be the correct preposition+article combination
- "explanation" explains WHY this case (Wohin/Wo, which preposition requires which case)
- For Wechselpräpositionen: Wohin? = Akkusativ, Wo? = Dativ
- Include the article in the options (e.g., "auf den", not just "auf")
- Use varied sentences about daily activities, locations, movement

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""

NOMINALISIERUNG_PROMPT = """Generate {count} German grammar exercises for NOMINALIZATION (Nominalisierung & Umformung).

Distribute across difficulty levels:
- Level 3 (B2): ~10 exercises. Nebensatz zu Nominalphrase (weil->wegen, dass->die Tatsache dass, wenn->bei).
- Level 4 (C1): ~10 exercises. Verb zu Nomen (verreisen->die Reise), Relativsatz zu Partizipialattribut, Satz zu Infinitivkonstruktion.

Each exercise MUST be a JSON object with EXACTLY this structure:
{{
    "id": "gen_nom_{n:03d}",
    "module": "nominalisierung",
    "type": "transformation",
    "level": 3-4,
    "topic": "nebensatz_zu_nominal|verb_zu_nomen|relativsatz_zu_partizip|satz_zu_infinitiv",
    "data": {{
        "source": "Weil es stark regnet, bleiben wir zu Hause.",
        "target_words": ["Wegen", "des", "starken", "Regens", "bleiben", "wir", "zu", "Hause"],
        "correct_order": "Wegen des starken Regens bleiben wir zu Hause.",
        "optional_words": [],
        "transform_type": "nebensatz_zu_nominal|verb_zu_nomen|relativsatz_zu_partizip|satz_zu_infinitiv"
    }},
    "grammar_rule": "Rule explanation for this nominalization pattern.",
    "grammar_tip": "Short transformation pattern hint"
}}

CRITICAL RULES:
- "source" is the original sentence (often with a subordinate clause)
- "target_words" splits the nominalized version into individual words (NO punctuation in words)
- "correct_order" is the full nominalized sentence with proper punctuation
- "optional_words" lists words that might be omitted or reordered
- Common patterns: weil -> wegen + Genitiv, dass -> die Tatsache, wenn -> bei + Dativ
- The nominalized version must be grammatically correct and natural
- Use academic/formal register (C1 level)

Return ONLY a JSON array of {count} exercise objects. No markdown, no explanation."""


# Map module keys to their prompts
MODULE_PROMPTS = {
    "verb_position": VERB_POSITION_PROMPT,
    "adjektive": ADJEKTIVE_PROMPT,
    "konnektoren": KONNEKTOREN_PROMPT,
    "passiv": PASSIV_PROMPT,
    "konjunktiv": KONJUNKTIV_PROMPT,
    "relativ": RELATIV_PROMPT,
    "praepositionen": PRAEPOSITIONEN_PROMPT,
    "nominalisierung": NOMINALISIERUNG_PROMPT,
}


# ─── VALIDATION ──────────────────────────────────────────────────────

def _validate_verb_position(ex):
    """Validate a verb_position exercise."""
    required = {"id", "text", "verbs", "clause_type", "difficulty", "explanation"}
    if not required.issubset(ex.keys()):
        return False
    if not isinstance(ex["verbs"], list) or len(ex["verbs"]) == 0:
        return False
    # Every verb must appear in the text
    for v in ex["verbs"]:
        if v not in ex["text"]:
            return False
    if ex["difficulty"] not in (1, 2, 3, 4):
        return False
    return True


def _validate_gap_fill(ex):
    """Validate a gap_fill exercise."""
    required_top = {"id", "module", "type", "level", "topic", "data", "grammar_rule"}
    if not required_top.issubset(ex.keys()):
        return False
    d = ex["data"]
    if "sentence_template" not in d or "gaps" not in d or "full_correct" not in d:
        return False
    for g in d["gaps"]:
        if "position" not in g or "answer" not in g or "options" not in g:
            return False
        if g["answer"] not in g["options"]:
            return False
    return True


def _validate_reconstruction(ex):
    """Validate a reconstruction exercise."""
    required_top = {"id", "module", "type", "level", "topic", "data", "grammar_rule"}
    if not required_top.issubset(ex.keys()):
        return False
    d = ex["data"]
    if "text" not in d or "verbs" not in d or "clause_type" not in d:
        return False
    for v in d["verbs"]:
        if v not in d["text"]:
            return False
    return True


def _validate_transformation(ex):
    """Validate a transformation exercise."""
    required_top = {"id", "module", "type", "level", "topic", "data", "grammar_rule"}
    if not required_top.issubset(ex.keys()):
        return False
    d = ex["data"]
    if "source" not in d or "target_words" not in d or "correct_order" not in d:
        return False
    if not isinstance(d["target_words"], list) or len(d["target_words"]) < 3:
        return False
    return True


def _validate_quick_select(ex):
    """Validate a quick_select exercise."""
    required_top = {"id", "module", "type", "level", "topic", "data", "grammar_rule"}
    if not required_top.issubset(ex.keys()):
        return False
    d = ex["data"]
    if "sentence" not in d or "gaps" not in d:
        return False
    for g in d["gaps"]:
        if "position" not in g or "options" not in g or "answer" not in g:
            return False
        if g["answer"] not in g["options"]:
            return False
    return True


VALIDATORS = {
    "verb_position": _validate_verb_position,
    "gap_fill": _validate_gap_fill,
    "reconstruction": _validate_reconstruction,
    "transformation": _validate_transformation,
    "quick_select": _validate_quick_select,
}

# Module -> exercise type mapping
MODULE_TYPES = {
    "verb_position": "verb_position",  # special: uses sentences.py format
    "adjektive": "gap_fill",
    "konnektoren": "reconstruction",
    "passiv": "transformation",
    "konjunktiv": "reconstruction",  # also has some gap_fill at level 4
    "relativ": "reconstruction",
    "praepositionen": "quick_select",
    "nominalisierung": "transformation",
}


# ─── GENERATION ──────────────────────────────────────────────────────

def _call_claude(prompt, api_key):
    """Call Claude API and return parsed JSON."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        # Remove first line (```json or ```)
        lines = response_text.split("\n")
        lines = lines[1:]  # Remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # Remove closing fence
        response_text = "\n".join(lines)

    return json.loads(response_text)


def generate_module_exercises(module_key, api_key, count=EXERCISES_PER_MODULE):
    """Generate exercises for a single module using Claude API."""
    prompt_template = MODULE_PROMPTS.get(module_key)
    if not prompt_template:
        logger.warning(f"No prompt template for module: {module_key}")
        return []

    prompt = prompt_template.format(count=count, n=1)

    try:
        exercises = _call_claude(prompt, api_key)
    except Exception as e:
        logger.error(f"Claude API call failed for {module_key}: {e}")
        return []

    if not isinstance(exercises, list):
        logger.error(f"Expected list from Claude for {module_key}, got {type(exercises)}")
        return []

    # Validate exercises
    valid = []
    exercise_type = MODULE_TYPES.get(module_key, "reconstruction")

    for i, ex in enumerate(exercises):
        # For verb_position, the validator is different
        if module_key == "verb_position":
            validator = VALIDATORS["verb_position"]
        else:
            # Determine type from the exercise itself (konjunktiv can be both)
            ex_type = ex.get("type", exercise_type)
            validator = VALIDATORS.get(ex_type, VALIDATORS.get(exercise_type))

        if validator and validator(ex):
            # Ensure grammar_tip exists
            if "grammar_tip" not in ex:
                ex["grammar_tip"] = ""
            valid.append(ex)
        else:
            logger.warning(f"Invalid exercise #{i} for {module_key}, skipping")

    logger.info(f"Generated {len(valid)}/{len(exercises)} valid exercises for {module_key}")
    return valid


def generate_all_exercises(api_key=None):
    """Generate exercises for all modules. Returns dict of module_key -> exercise list."""
    if not api_key:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        logger.warning("No ANTHROPIC_API_KEY set — skipping generation, using cache")
        return load_cache()

    all_exercises = {}

    for module_key in MODULE_PROMPTS:
        logger.info(f"Generating exercises for {module_key}...")
        exercises = generate_module_exercises(module_key, api_key)
        if exercises:
            all_exercises[module_key] = exercises
        else:
            logger.warning(f"No exercises generated for {module_key}")
        # Small delay to avoid rate limits
        time.sleep(1)

    if all_exercises:
        save_cache(all_exercises)

    return all_exercises


# ─── CACHING ─────────────────────────────────────────────────────────

def save_cache(exercises_by_module):
    """Save generated exercises to a JSON cache file."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(exercises_by_module, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved exercise cache to {CACHE_FILE}")
    except Exception as e:
        logger.error(f"Failed to save exercise cache: {e}")


def load_cache():
    """Load exercises from the cache file."""
    if not CACHE_FILE.exists():
        logger.info("No exercise cache found")
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded exercise cache: {sum(len(v) for v in data.values())} exercises")
        return data
    except Exception as e:
        logger.error(f"Failed to load exercise cache: {e}")
        return {}


# ─── INTEGRATION ─────────────────────────────────────────────────────

def refresh_exercise_banks():
    """Main entry point: generate or load exercises and update the global banks.

    Returns (verb_position_sentences, grammar_exercises) tuple.
    - verb_position_sentences: list of sentence-bank-format dicts for sentences.py
    - grammar_exercises: list of grammar-exercise-format dicts for grammar_exercises.py
    """
    generated = generate_all_exercises()

    verb_position_sentences = generated.get("verb_position", [])
    grammar_exercises = []

    for module_key, exercises in generated.items():
        if module_key == "verb_position":
            continue  # handled separately
        grammar_exercises.extend(exercises)

    logger.info(
        f"Exercise refresh complete: {len(verb_position_sentences)} verb_position, "
        f"{len(grammar_exercises)} grammar exercises"
    )
    return verb_position_sentences, grammar_exercises
