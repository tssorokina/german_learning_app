"""
Input Lab — text processing for meaning-focused input.

Segments German text into sentences, scores difficulty against user's
known vocabulary, and prepares bridge drills from content sentences.
"""

import os
import re
import random
import logging

logger = logging.getLogger(__name__)

# Common German abbreviations that end with a period but are not sentence endings
_ABBREVIATIONS = {
    "z.b.", "d.h.", "u.a.", "v.a.", "bzw.", "ca.", "etc.", "ggf.",
    "inkl.", "nr.", "dr.", "hr.", "fr.", "prof.", "str.", "tel.",
    "vgl.", "s.", "abs.", "max.", "min.", "usw.", "evtl.",
}

# Common German words that are always treated as "known" for difficulty scoring.
# Includes function words AND the ~400 most frequent German content words
# (approx. frequency class ≤12 in Wortschatz Leipzig).
_STOP_WORDS = {
    # ── articles, pronouns, determiners ─────────────────────────────
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "einem", "einer", "und", "oder", "aber", "denn", "sondern", "nicht",
    "kein", "keine", "keinen", "keinem", "ich", "du", "er", "sie", "es",
    "wir", "ihr", "mich", "dich", "sich", "uns", "euch", "mir", "dir",
    "ihm", "ihr", "ihnen", "mein", "dein", "sein", "unser", "euer",
    "dieser", "diese", "dieses", "diesen", "diesem", "jeder", "jede",
    "jedes", "jeden", "jedem", "man", "etwas", "nichts",
    "alle", "alles", "allem", "allen", "aller",
    "welch", "welche", "welcher", "welches", "welchen", "welchem",
    # ── prepositions ────────────────────────────────────────────────
    "in", "an", "auf", "zu", "von", "mit", "für", "über", "unter",
    "nach", "vor", "bei", "aus", "um", "durch", "gegen", "ohne",
    "zwischen", "neben", "hinter", "außer", "trotz", "wegen", "statt",
    "innerhalb", "außerhalb", "gegenüber", "laut", "gemäß", "anstatt",
    # ── conjunctions & particles ────────────────────────────────────
    "dass", "weil", "wenn", "als", "ob", "obwohl", "damit", "bevor",
    "nachdem", "während", "seit", "bis", "da", "so", "wie", "wo",
    "doch", "mal", "ja", "nein", "also", "zwar", "jedoch", "dennoch",
    "außerdem", "deshalb", "deswegen", "daher", "darum", "dabei",
    "dazu", "davon", "dafür", "dagegen", "darauf", "darin", "darüber",
    "darunter", "danach", "davor", "daran", "daraus", "damit",
    # ── common verbs (all forms) ────────────────────────────────────
    "ist", "sind", "war", "waren", "bin", "bist", "wäre", "wären",
    "hat", "haben", "hatte", "hatten", "hätte", "hätten",
    "wird", "werden", "wurde", "wurden", "würde", "würden", "worden",
    "kann", "können", "konnte", "konnten", "könnte", "könnten",
    "muss", "müssen", "musste", "mussten", "müsste", "müssten",
    "soll", "sollen", "sollte", "sollten",
    "will", "wollen", "wollte", "wollten",
    "darf", "dürfen", "durfte", "durften", "dürfte", "dürften",
    "mag", "mögen", "mochte", "möchte", "möchten",
    "gibt", "geben", "gab", "gaben", "gegeben",
    "geht", "gehen", "ging", "gegangen",
    "kommt", "kommen", "kam", "kamen", "gekommen",
    "macht", "machen", "machte", "gemacht",
    "sagt", "sagen", "sagte", "gesagt",
    "steht", "stehen", "stand", "gestanden",
    "liegt", "liegen", "lag", "gelegen",
    "sieht", "sehen", "sah", "gesehen",
    "nimmt", "nehmen", "nahm", "genommen",
    "findet", "finden", "fand", "gefunden",
    "bringt", "bringen", "brachte", "gebracht",
    "hält", "halten", "hielt", "gehalten",
    "lässt", "lassen", "ließ", "gelassen",
    "bleibt", "bleiben", "blieb", "geblieben",
    "heißt", "heißen", "hieß",
    "weiß", "wissen", "wusste", "gewusst",
    "denkt", "denken", "dachte", "gedacht",
    "glaubt", "glauben", "glaubte", "geglaubt",
    "braucht", "brauchen", "brauchte", "gebraucht",
    "zeigt", "zeigen", "zeigte", "gezeigt",
    "spricht", "sprechen", "sprach", "gesprochen",
    "führt", "führen", "führte", "geführt",
    "trägt", "tragen", "trug", "getragen",
    "fährt", "fahren", "fuhr", "gefahren",
    "läuft", "laufen", "lief", "gelaufen",
    "sitzt", "sitzen", "saß", "gesessen",
    "spielt", "spielen", "spielte", "gespielt",
    "arbeitet", "arbeiten", "arbeitete", "gearbeitet",
    "lebt", "leben", "lebte", "gelebt",
    "lernt", "lernen", "lernte", "gelernt",
    "liest", "lesen", "las", "gelesen",
    "schreibt", "schreiben", "schrieb", "geschrieben",
    "beginnt", "beginnen", "begann", "begonnen",
    "erklärt", "erklären", "erklärte", "erklärt",
    "versucht", "versuchen", "versuchte", "versucht",
    "stellt", "stellen", "stellte", "gestellt",
    "setzt", "setzen", "setzte", "gesetzt",
    "legt", "legen", "legte", "gelegt",
    "folgt", "folgen", "folgte", "gefolgt",
    # ── common adverbs ──────────────────────────────────────────────
    "auch", "noch", "schon", "nur", "sehr", "mehr", "viel", "gut",
    "hier", "dort", "dann", "immer", "nie", "oft", "jetzt", "heute",
    "morgen", "gestern", "ganz", "wieder", "schon", "fast", "gerade",
    "bereits", "etwa", "wirklich", "besonders", "eigentlich", "natürlich",
    "vielleicht", "wahrscheinlich", "tatsächlich", "genau", "zusammen",
    "allein", "sogar", "jedenfalls", "überhaupt", "zunächst", "zuerst",
    "bisher", "bislang", "derzeit", "inzwischen", "mittlerweile",
    "eher", "ziemlich", "recht", "kaum", "wenig", "lange", "kurz",
    "früh", "spät", "schnell", "langsam", "häufig", "selten",
    "oben", "unten", "vorne", "hinten", "rechts", "links",
    "maximal", "mindestens", "ungefähr", "rund",
    # ── common adjectives ───────────────────────────────────────────
    "groß", "große", "großen", "großer", "großes", "größer", "größte",
    "klein", "kleine", "kleinen", "kleiner", "kleines",
    "neu", "neue", "neuen", "neuer", "neues",
    "alt", "alte", "alten", "alter", "altes",
    "lang", "lange", "langen", "langer", "langes", "länger", "längste",
    "jung", "junge", "jungen", "junger", "junges",
    "hoch", "hohe", "hohen", "hoher", "hohes", "höher", "höchste",
    "erst", "erste", "ersten", "erster", "erstes",
    "letzt", "letzte", "letzten", "letzter", "letztes",
    "ander", "andere", "anderen", "anderer", "anderes",
    "eigen", "eigene", "eigenen", "eigener", "eigenes",
    "verschieden", "verschiedene", "verschiedenen",
    "möglich", "wichtig", "richtig", "falsch", "schlecht", "schön",
    "frei", "stark", "schwer", "leicht", "weit", "nah", "voll",
    "gleich", "bestimmt", "einzig", "weiter", "weitere", "weiteren",
    "öffentlich", "politisch", "sozial", "international", "deutsch",
    "deutsche", "deutschen", "deutscher", "deutsches",
    # ── common nouns (top frequency) ────────────────────────────────
    "Jahr", "Jahre", "Jahren", "Jahres",
    "Zeit", "Mal", "Teil", "Seite",
    "Mensch", "Menschen", "Kind", "Kinder", "Kindern",
    "Frau", "Frauen", "Mann", "Männer",
    "Tag", "Tage", "Tagen", "Woche", "Wochen", "Monat", "Monate",
    "Land", "Länder", "Stadt", "Städte", "Welt",
    "Haus", "Häuser", "Schule", "Arbeit",
    "Frage", "Fragen", "Antwort", "Antworten",
    "Beispiel", "Fall", "Fälle", "Grund", "Gründe",
    "Ende", "Anfang", "Leben",
    "Geld", "Wasser", "Weg", "Platz",
    "Hand", "Kopf", "Auge", "Augen",
    "Wort", "Sprache", "Buch", "Bild",
    "Thema", "Problem", "Probleme",
    "Prozent", "Zahl", "Zahlen", "Stunde", "Stunden", "Minute",
    "Eltern", "Familie", "Freund", "Freunde",
    "Euro", "Dollar", "Milliarde", "Million", "Millionen",
    "Regierung", "Staat", "Gesellschaft",
    # ── common adjectival / misc ────────────────────────────────────
    "viele", "vielen", "vieler", "wenige", "wenigen", "weniger",
    "einige", "einigen", "einiger",
    "beiden", "beide", "beider",
    "solche", "solchen", "solcher", "solches",
    "gar", "denn", "wohl", "eben", "bloß", "übrigens",
    "zum", "zur", "vom", "beim", "ins", "im", "am",
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


def translate_sentences(sentences):
    """Translate German sentences to English.

    Tries DeepL API first (if DEEPL_API_KEY is set), then falls back
    to MyMemory free API.  Returns dict mapping German sentence → English.
    """
    if not sentences:
        return {}

    import requests

    api_key = os.environ.get("DEEPL_API_KEY", "")

    # ── Try DeepL first ───────────────────────────────────────────
    if api_key:
        translations = {}
        batch_size = 50
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            try:
                base_url = (
                    "https://api-free.deepl.com" if api_key.endswith(":fx")
                    else "https://api.deepl.com"
                )
                resp = requests.post(
                    f"{base_url}/v2/translate",
                    data={
                        "auth_key": api_key,
                        "text": batch,
                        "source_lang": "DE",
                        "target_lang": "EN",
                    },
                    timeout=10,
                )
                if resp.status_code == 200:
                    results = resp.json().get("translations", [])
                    for sent, tr in zip(batch, results):
                        translations[sent] = tr.get("text", "")
                else:
                    logger.warning(f"DeepL returned {resp.status_code}")
            except Exception as e:
                logger.warning(f"DeepL translation failed: {e}")
        if translations:
            return translations

    # ── Fallback: MyMemory free API (1 sentence at a time) ────────
    translations = {}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GermanLearningApp/1.0)"}
    for sent in sentences:
        try:
            resp = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": sent, "langpair": "de|en"},
                headers=headers,
                timeout=8,
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("responseData", {}).get("translatedText", "")
                if text and "MYMEMORY" not in text.upper():
                    translations[sent] = text
        except Exception:
            pass
    return translations


def prepare_bridge_drill(sentence_text, sentence_index=0, text_id=0, english=""):
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
        "english": english,
    }
