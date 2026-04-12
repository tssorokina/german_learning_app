"""
Input Lab — text processing for meaning-focused input.

Segments German text into sentences, scores difficulty against user's
known vocabulary, and prepares bridge drills from content sentences.
"""

import re
import random

# Common German abbreviations that end with a period but are not sentence endings
_ABBREVIATIONS = {
    "z.b.", "d.h.", "u.a.", "v.a.", "bzw.", "ca.", "etc.", "ggf.",
    "inkl.", "nr.", "dr.", "hr.", "fr.", "prof.", "str.", "tel.",
    "vgl.", "s.", "abs.", "max.", "min.", "usw.", "evtl.",
}

# Common German "stop words" that are always known — not counted as unknown
_STOP_WORDS = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "einem", "einer", "und", "oder", "aber", "denn", "sondern", "nicht",
    "kein", "keine", "keinen", "keinem", "ich", "du", "er", "sie", "es",
    "wir", "ihr", "mich", "dich", "sich", "uns", "euch", "mir", "dir",
    "ihm", "ihr", "ihnen", "mein", "dein", "sein", "unser", "euer",
    "in", "an", "auf", "zu", "von", "mit", "für", "über", "unter",
    "nach", "vor", "bei", "aus", "um", "durch", "gegen", "ohne",
    "ist", "sind", "war", "hat", "haben", "wird", "werden", "kann",
    "muss", "soll", "will", "darf", "mag", "möchte", "wurde", "worden",
    "dass", "weil", "wenn", "als", "ob", "obwohl", "damit", "bevor",
    "nachdem", "während", "seit", "bis", "da", "so", "wie", "wo",
    "was", "wer", "wem", "wen", "welch", "welche", "welcher", "welches",
    "auch", "noch", "schon", "nur", "sehr", "mehr", "viel", "gut",
    "ja", "nein", "hier", "dort", "dann", "also", "doch", "mal",
    "immer", "nie", "oft", "jetzt", "heute", "morgen", "gestern",
    "alle", "alles", "dieser", "diese", "dieses", "jeder", "jede",
    "man", "etwas", "nichts", "es", "gibt", "sein", "haben", "werden",
}


def segment_text(raw_text):
    """Split German text into sentences.

    Handles common abbreviations and avoids splitting on them.
    Returns a list of sentence strings.
    """
    text = raw_text.strip()
    if not text:
        return []

    # Replace abbreviation periods with a placeholder
    protected = text
    for abbr in _ABBREVIATIONS:
        pattern = re.compile(re.escape(abbr), re.IGNORECASE)
        protected = pattern.sub(abbr.replace(".", "\x00"), protected)

    # Split on sentence-ending punctuation followed by space + uppercase
    # or end of string
    parts = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ\u201e„])', protected)

    # Also split on newlines that look like paragraph breaks
    final_parts = []
    for part in parts:
        subparts = re.split(r'\n\s*\n', part)
        final_parts.extend(subparts)

    # Restore abbreviation periods and clean up
    sentences = []
    for s in final_parts:
        s = s.replace("\x00", ".").strip()
        # Skip very short fragments (less than 3 words)
        if s and len(s.split()) >= 3:
            sentences.append(s)

    return sentences


def _tokenize(text):
    """Simple word tokenizer: split on whitespace, strip punctuation."""
    words = text.split()
    tokens = []
    for w in words:
        clean = re.sub(r'^[^\wÄÖÜäöüß]+|[^\wÄÖÜäöüß]+$', '', w)
        if clean:
            tokens.append(clean)
    return tokens


def score_difficulty(sentences, known_words):
    """Score difficulty of segmented text against user's known vocabulary.

    Returns (overall_score, per_sentence_scores, total_words, unknown_count).
    - overall_score: 0.0 to 1.0 (1.0 = all known)
    - per_sentence_scores: list of floats
    """
    if not sentences:
        return 1.0, [], 0, 0

    # Normalise known words to lowercase
    known_lower = {w.lower() for w in known_words}
    # Add stop words as always-known
    known_lower |= _STOP_WORDS

    total_tokens = 0
    total_known = 0
    per_sentence = []
    all_unknown = set()

    for sent in sentences:
        tokens = _tokenize(sent)
        if not tokens:
            per_sentence.append(1.0)
            continue

        known_count = 0
        for t in tokens:
            total_tokens += 1
            if t.lower() in known_lower:
                known_count += 1
                total_known += 1
            else:
                all_unknown.add(t.lower())

        score = known_count / len(tokens) if tokens else 1.0
        per_sentence.append(score)

    overall = total_known / total_tokens if total_tokens > 0 else 1.0
    unknown_count = len(all_unknown)

    return overall, per_sentence, total_tokens, unknown_count


def get_unknown_words(sentence, known_words):
    """Get list of unknown words in a sentence."""
    known_lower = {w.lower() for w in known_words} | _STOP_WORDS
    tokens = _tokenize(sentence)
    return [t for t in tokens if t.lower() not in known_lower]


def difficulty_band(score):
    """Classify a difficulty score into green/amber/red."""
    if score >= 0.98:
        return "green"
    elif score >= 0.95:
        return "amber"
    else:
        return "red"


def prepare_bridge_drill(sentence_text, sentence_index=0, text_id=0):
    """Convert a sentence into a reconstruction drill template.

    Returns a dict compatible with sentences.prepare_exercise().
    All words become slots (full reconstruction mode).
    """
    tokens = _tokenize(sentence_text)
    # Use all words as "verbs" so they all become active slots
    return {
        "id": f"lab_{text_id}_s{sentence_index}",
        "text": sentence_text,
        "verbs": tokens,  # all words are targets
        "clause_type": "input_lab",
        "difficulty": 2,  # neutral
        "explanation": "Reconstruct the sentence from your reading text.",
        "english": "",
    }
