"""
Grammar Exercise Banks for all modules (Modules 1-7).

Each exercise follows the unified format:
{
    "id": "unique_id",
    "module": "module_key",
    "type": "reconstruction|gap_fill|transformation|quick_select",
    "level": 1-4 (A2=1, B1=2, B2=3, C1=4),
    "topic": "specific_grammar_topic_tag",
    "data": { ... type-specific payload },
    "grammar_rule": "Human-readable rule explanation",
    "grammar_tip": "Mnemonic or practical tip"
}
"""

# ═══════════════════════════════════════════════════════════
# MODULE 1: Adjective Declension Trainer (A2-B2)
# Exercise type: gap_fill
# ═══════════════════════════════════════════════════════════

ADJECTIVE_EXERCISES = [
    # ── A2: Adjektive nach bestimmtem Artikel ──
    {
        "id": "adj_001",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_bestimmt",
        "data": {
            "sentence_template": "Ich kaufe den neu{gap_1} Pullover.",
            "gaps": [{
                "position": "gap_1",
                "context": "neu__",
                "answer": "en",
                "article_type": "bestimmt",
                "case": "Akkusativ",
                "gender": "maskulin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Ich kaufe den neuen Pullover."
        },
        "grammar_rule": "After bestimmter Artikel, Akkusativ maskulin -> -en",
        "grammar_tip": "Bestimmter Artikel Akk. mask. -> immer -en"
    },
    {
        "id": "adj_002",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_bestimmt",
        "data": {
            "sentence_template": "Die klein{gap_1} Katze schläft auf dem Sofa.",
            "gaps": [{
                "position": "gap_1",
                "context": "klein__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "feminin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Die kleine Katze schläft auf dem Sofa."
        },
        "grammar_rule": "After bestimmter Artikel, Nominativ feminin -> -e",
        "grammar_tip": "Nom./Akk. feminin + bestimmter Artikel -> -e"
    },
    {
        "id": "adj_003",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_bestimmt",
        "data": {
            "sentence_template": "Das groß{gap_1} Haus steht am Ende der Straße.",
            "gaps": [{
                "position": "gap_1",
                "context": "groß__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Das große Haus steht am Ende der Straße."
        },
        "grammar_rule": "After bestimmter Artikel, Nominativ neutrum -> -e",
        "grammar_tip": "Nom./Akk. neutrum + bestimmter Artikel -> -e"
    },
    {
        "id": "adj_004",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_bestimmt",
        "data": {
            "sentence_template": "Er gibt dem nett{gap_1} Kind ein Geschenk.",
            "gaps": [{
                "position": "gap_1",
                "context": "nett__",
                "answer": "en",
                "article_type": "bestimmt",
                "case": "Dativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Er gibt dem netten Kind ein Geschenk."
        },
        "grammar_rule": "After bestimmter Artikel, Dativ -> always -en",
        "grammar_tip": "Dativ + bestimmter Artikel -> IMMER -en"
    },
    {
        "id": "adj_005",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_bestimmt",
        "data": {
            "sentence_template": "Die alt{gap_1} Bücher liegen auf dem Tisch.",
            "gaps": [{
                "position": "gap_1",
                "context": "alt__",
                "answer": "en",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "plural",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Die alten Bücher liegen auf dem Tisch."
        },
        "grammar_rule": "After bestimmter Artikel, Plural -> always -en",
        "grammar_tip": "Plural + bestimmter Artikel -> IMMER -en"
    },
    # ── A2: Adjektive nach unbestimmtem Artikel ──
    {
        "id": "adj_006",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_unbestimmt",
        "data": {
            "sentence_template": "Ein jung{gap_1} Mann wartet an der Haltestelle.",
            "gaps": [{
                "position": "gap_1",
                "context": "jung__",
                "answer": "er",
                "article_type": "unbestimmt",
                "case": "Nominativ",
                "gender": "maskulin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Ein junger Mann wartet an der Haltestelle."
        },
        "grammar_rule": "After unbestimmter Artikel, Nominativ maskulin -> -er",
        "grammar_tip": "Unbestimmter Artikel Nom. mask. -> -er (shows gender)"
    },
    {
        "id": "adj_007",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_unbestimmt",
        "data": {
            "sentence_template": "Ich habe eine interessant{gap_1} Geschichte gelesen.",
            "gaps": [{
                "position": "gap_1",
                "context": "interessant__",
                "answer": "e",
                "article_type": "unbestimmt",
                "case": "Akkusativ",
                "gender": "feminin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Ich habe eine interessante Geschichte gelesen."
        },
        "grammar_rule": "After unbestimmter Artikel, Akkusativ feminin -> -e",
        "grammar_tip": "Nom./Akk. fem. + unbestimmter Artikel -> -e"
    },
    {
        "id": "adj_008",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_unbestimmt",
        "data": {
            "sentence_template": "Sie hat ein neu{gap_1} Auto gekauft.",
            "gaps": [{
                "position": "gap_1",
                "context": "neu__",
                "answer": "es",
                "article_type": "unbestimmt",
                "case": "Akkusativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Sie hat ein neues Auto gekauft."
        },
        "grammar_rule": "After unbestimmter Artikel, Akkusativ neutrum -> -es",
        "grammar_tip": "Nom./Akk. neutrum + unbestimmter Artikel -> -es (shows gender)"
    },
    # ── A2: Adjektive nach Possessivartikeln ──
    {
        "id": "adj_009",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_possessiv",
        "data": {
            "sentence_template": "Mein alt{gap_1} Auto ist kaputt.",
            "gaps": [{
                "position": "gap_1",
                "context": "alt__",
                "answer": "es",
                "article_type": "possessiv",
                "case": "Nominativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Mein altes Auto ist kaputt."
        },
        "grammar_rule": "After Possessivartikel (like unbestimmt), Nominativ neutrum -> -es",
        "grammar_tip": "Possessivartikel = same endings as unbestimmter Artikel"
    },
    {
        "id": "adj_010",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 1,
        "topic": "adj_possessiv",
        "data": {
            "sentence_template": "Sie besucht ihre krank{gap_1} Großmutter.",
            "gaps": [{
                "position": "gap_1",
                "context": "krank__",
                "answer": "e",
                "article_type": "possessiv",
                "case": "Akkusativ",
                "gender": "feminin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Sie besucht ihre kranke Großmutter."
        },
        "grammar_rule": "After Possessivartikel, Akkusativ feminin -> -e",
        "grammar_tip": "Akk. fem. + Possessivartikel -> -e"
    },
    # ── B1: Adjektivdeklination ohne Artikel ──
    {
        "id": "adj_011",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 2,
        "topic": "adj_ohne_artikel",
        "data": {
            "sentence_template": "Kalt{gap_1} Kaffee schmeckt im Sommer gut.",
            "gaps": [{
                "position": "gap_1",
                "context": "Kalt__",
                "answer": "er",
                "article_type": "ohne",
                "case": "Nominativ",
                "gender": "maskulin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Kalter Kaffee schmeckt im Sommer gut."
        },
        "grammar_rule": "Without article, Nominativ maskulin -> -er (strong ending)",
        "grammar_tip": "Ohne Artikel -> Adjektiv zeigt Genus/Kasus (starke Deklination)"
    },
    {
        "id": "adj_012",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 2,
        "topic": "adj_ohne_artikel",
        "data": {
            "sentence_template": "Mit frisch{gap_1} Brot schmeckt die Suppe besser.",
            "gaps": [{
                "position": "gap_1",
                "context": "frisch__",
                "answer": "em",
                "article_type": "ohne",
                "case": "Dativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Mit frischem Brot schmeckt die Suppe besser."
        },
        "grammar_rule": "Without article, Dativ neutrum -> -em (strong ending)",
        "grammar_tip": "Dativ ohne Artikel -> -em (mask./neutrum), -er (fem.), -en (plural)"
    },
    {
        "id": "adj_013",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 2,
        "topic": "adj_ohne_artikel",
        "data": {
            "sentence_template": "Gut{gap_1} Freunde sind wichtig im Leben.",
            "gaps": [{
                "position": "gap_1",
                "context": "Gut__",
                "answer": "e",
                "article_type": "ohne",
                "case": "Nominativ",
                "gender": "plural",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Gute Freunde sind wichtig im Leben."
        },
        "grammar_rule": "Without article, Nominativ Plural -> -e (strong ending)",
        "grammar_tip": "Nom./Akk. Plural ohne Artikel -> -e"
    },
    # ── B1: Partizip I/II als Adjektiv ──
    {
        "id": "adj_014",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 2,
        "topic": "partizip_adjektiv",
        "data": {
            "sentence_template": "Das schlafend{gap_1} Kind liegt im Bett.",
            "gaps": [{
                "position": "gap_1",
                "context": "schlafend__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "neutrum",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Das schlafende Kind liegt im Bett."
        },
        "grammar_rule": "Partizip I as adjective follows normal declension rules. Bestimmt + Nom. neutrum -> -e",
        "grammar_tip": "Partizip I (schlafend) = Adjektiv -> normale Deklination"
    },
    {
        "id": "adj_015",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 2,
        "topic": "partizip_adjektiv",
        "data": {
            "sentence_template": "Bitte schließen Sie die geöffnet{gap_1} Tür.",
            "gaps": [{
                "position": "gap_1",
                "context": "geöffnet__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Akkusativ",
                "gender": "feminin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Bitte schließen Sie die geöffnete Tür."
        },
        "grammar_rule": "Partizip II as adjective follows normal declension. Bestimmt + Akk. feminin -> -e",
        "grammar_tip": "Partizip II (geöffnet) = Adjektiv -> normale Deklination"
    },
    # ── B2: Erweiterte Partizipialattribute ──
    {
        "id": "adj_016",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 3,
        "topic": "erweitert_partizip",
        "data": {
            "sentence_template": "Die seit Wochen andauernd{gap_1} Diskussion ist beendet.",
            "gaps": [{
                "position": "gap_1",
                "context": "andauernd__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "feminin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Die seit Wochen andauernde Diskussion ist beendet."
        },
        "grammar_rule": "Extended participial attributes follow normal adjective declension",
        "grammar_tip": "Erweitertes Partizipialattribut = Adjektiv mit Erweiterung davor"
    },
    {
        "id": "adj_017",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 3,
        "topic": "erweitert_partizip",
        "data": {
            "sentence_template": "Der von allen Studenten geschätzt{gap_1} Professor geht in Rente.",
            "gaps": [{
                "position": "gap_1",
                "context": "geschätzt__",
                "answer": "e",
                "article_type": "bestimmt",
                "case": "Nominativ",
                "gender": "maskulin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Der von allen Studenten geschätzte Professor geht in Rente."
        },
        "grammar_rule": "Partizip II with extension, bestimmt Nominativ maskulin -> -e",
        "grammar_tip": "Bestimmter Artikel Nom. mask. -> -e (schwache Deklination)"
    },
    {
        "id": "adj_018",
        "module": "adjektive",
        "type": "gap_fill",
        "level": 3,
        "topic": "erweitert_partizip",
        "data": {
            "sentence_template": "Wir besprechen den kürzlich veröffentlicht{gap_1} Bericht.",
            "gaps": [{
                "position": "gap_1",
                "context": "veröffentlicht__",
                "answer": "en",
                "article_type": "bestimmt",
                "case": "Akkusativ",
                "gender": "maskulin",
                "options": ["e", "en", "er", "es", "em"]
            }],
            "full_correct": "Wir besprechen den kürzlich veröffentlichten Bericht."
        },
        "grammar_rule": "Extended Partizip II, bestimmt Akkusativ maskulin -> -en",
        "grammar_tip": "Akk. mask. + bestimmter Artikel -> -en"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 2: Konnektoren & Satzstellung (A2-C1)
# Exercise type: reconstruction (reuses existing engine)
# ═══════════════════════════════════════════════════════════

KONNEKTOR_EXERCISES = [
    # ── A2: Hauptsatz-Konnektoren (Position 0) ──
    {
        "id": "kon_001",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 1,
        "topic": "hauptsatz_konnektor",
        "data": {
            "text": "Ich möchte ins Kino gehen, aber ich habe kein Geld.",
            "verbs": ["gehen", "habe"],
            "clause_type": "aber_hauptsatz"
        },
        "grammar_rule": "After 'aber' (Position 0), the word order stays the same: Subject-Verb.",
        "grammar_tip": "und/aber/oder/denn/sondern = Position 0 (no inversion)"
    },
    {
        "id": "kon_002",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 1,
        "topic": "hauptsatz_konnektor",
        "data": {
            "text": "Er ist müde, denn er hat die ganze Nacht gearbeitet.",
            "verbs": ["hat", "gearbeitet"],
            "clause_type": "denn_hauptsatz"
        },
        "grammar_rule": "'denn' is Position 0: no inversion, normal SVO word order follows.",
        "grammar_tip": "'denn' = Konjunktion (Pos. 0), 'weil' = Subjunktion (Verb-End)"
    },
    {
        "id": "kon_003",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 1,
        "topic": "hauptsatz_konnektor",
        "data": {
            "text": "Möchtest du Tee oder möchtest du Kaffee?",
            "verbs": ["möchtest", "möchtest"],
            "clause_type": "oder_hauptsatz"
        },
        "grammar_rule": "'oder' connects two main clauses without changing word order.",
        "grammar_tip": "oder = Position 0, keine Inversion"
    },
    {
        "id": "kon_004",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 1,
        "topic": "hauptsatz_konnektor",
        "data": {
            "text": "Er lernt nicht Spanisch, sondern er lernt Italienisch.",
            "verbs": ["lernt", "lernt"],
            "clause_type": "sondern_hauptsatz"
        },
        "grammar_rule": "'sondern' corrects a negation, no word order change.",
        "grammar_tip": "sondern = Position 0, korrigiert eine Verneinung (nicht X, sondern Y)"
    },
    # ── B1: Adverbial-Konnektoren (Position 1 -> Inversion) ──
    {
        "id": "kon_005",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "adverbial_konnektor",
        "data": {
            "text": "Es regnet stark, deshalb bleibe ich zu Hause.",
            "verbs": ["regnet", "bleibe"],
            "clause_type": "deshalb_inversion"
        },
        "grammar_rule": "'deshalb' takes Position 1, causing inversion: Verb before Subject.",
        "grammar_tip": "deshalb/trotzdem/deswegen = Position 1 -> Verb-Subjekt (Inversion!)"
    },
    {
        "id": "kon_006",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "adverbial_konnektor",
        "data": {
            "text": "Er war krank, trotzdem ging er zur Arbeit.",
            "verbs": ["war", "ging"],
            "clause_type": "trotzdem_inversion"
        },
        "grammar_rule": "'trotzdem' at Position 1 causes inversion: verb comes before subject.",
        "grammar_tip": "trotzdem = Position 1, Verb sofort danach!"
    },
    {
        "id": "kon_007",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "adverbial_konnektor",
        "data": {
            "text": "Sie hat viel gelernt, außerdem hat sie Übungen gemacht.",
            "verbs": ["gelernt", "hat", "gemacht"],
            "clause_type": "ausserdem_inversion"
        },
        "grammar_rule": "'außerdem' at Position 1 causes inversion in the second clause.",
        "grammar_tip": "außerdem = Position 1 -> Inversion (Verb vor Subjekt)"
    },
    # ── B1: Zweiteilige Konnektoren ──
    {
        "id": "kon_008",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "zweiteilig",
        "data": {
            "text": "Er spricht nicht nur Deutsch, sondern auch Französisch.",
            "verbs": ["spricht"],
            "clause_type": "nicht_nur_sondern_auch"
        },
        "grammar_rule": "'nicht nur ... sondern auch': both parts must be placed correctly.",
        "grammar_tip": "nicht nur X, sondern auch Y — parallele Struktur!"
    },
    {
        "id": "kon_009",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "zweiteilig",
        "data": {
            "text": "Entweder fahren wir ans Meer oder wir bleiben zu Hause.",
            "verbs": ["fahren", "bleiben"],
            "clause_type": "entweder_oder"
        },
        "grammar_rule": "'entweder ... oder': entweder can cause inversion in first clause.",
        "grammar_tip": "entweder (Pos. 1 -> Inversion) ... oder (Pos. 0 -> keine Inversion)"
    },
    {
        "id": "kon_010",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 2,
        "topic": "zweiteilig",
        "data": {
            "text": "Weder hat er angerufen noch hat er geschrieben.",
            "verbs": ["angerufen", "geschrieben"],
            "clause_type": "weder_noch"
        },
        "grammar_rule": "'weder ... noch': both parts cause inversion.",
        "grammar_tip": "weder (Inversion) ... noch (Inversion) — doppelte Verneinung!"
    },
    # ── B2: Advanced Subjunktionen ──
    {
        "id": "kon_011",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 3,
        "topic": "subjunktion_b2",
        "data": {
            "text": "Falls es morgen regnet, bleiben wir zu Hause.",
            "verbs": ["regnet", "bleiben"],
            "clause_type": "falls_nebensatz"
        },
        "grammar_rule": "'falls' introduces a subordinate clause with verb at the end.",
        "grammar_tip": "falls = wenn (konditional), Verb am Ende"
    },
    {
        "id": "kon_012",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 3,
        "topic": "subjunktion_b2",
        "data": {
            "text": "Man kann die Sprache lernen, indem man jeden Tag übt.",
            "verbs": ["lernen", "übt"],
            "clause_type": "indem_nebensatz"
        },
        "grammar_rule": "'indem' = 'by doing', introduces subordinate clause with verb at end.",
        "grammar_tip": "indem = dadurch, dass ... (Verb am Ende)"
    },
    {
        "id": "kon_013",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 3,
        "topic": "subjunktion_b2",
        "data": {
            "text": "Er ging weg, ohne dass er sich verabschiedet hat.",
            "verbs": ["verabschiedet", "hat"],
            "clause_type": "ohne_dass_nebensatz"
        },
        "grammar_rule": "'ohne dass' introduces subordinate clause with verb at the end.",
        "grammar_tip": "ohne dass + Nebensatz (Verb am Ende)"
    },
    {
        "id": "kon_014",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 3,
        "topic": "je_desto",
        "data": {
            "text": "Je mehr du übst, desto besser wirst du.",
            "verbs": ["übst", "wirst"],
            "clause_type": "je_desto"
        },
        "grammar_rule": "'je' clause = subordinate (verb at end), 'desto' clause = inversion.",
        "grammar_tip": "je ... (Verb-End), desto ... (Inversion: Verb vor Subjekt)"
    },
    # ── C1: Nominalisierung vs. Nebensatz ──
    {
        "id": "kon_015",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 4,
        "topic": "nominalisierung_konnektor",
        "data": {
            "text": "Sofern alle Bedingungen erfüllt werden, kann der Vertrag unterschrieben werden.",
            "verbs": ["erfüllt", "werden", "unterschrieben", "werden"],
            "clause_type": "sofern_passiv"
        },
        "grammar_rule": "'sofern' clause with passive: verb cluster at end of subordinate clause.",
        "grammar_tip": "sofern = wenn/falls (formal), Verb am Ende des Nebensatzes"
    },
    {
        "id": "kon_016",
        "module": "konnektoren",
        "type": "reconstruction",
        "level": 4,
        "topic": "nominalisierung_konnektor",
        "data": {
            "text": "Anstatt dass er arbeitet, verbringt er den ganzen Tag im Internet.",
            "verbs": ["arbeitet", "verbringt"],
            "clause_type": "anstatt_dass"
        },
        "grammar_rule": "'anstatt dass' introduces subordinate clause, verb goes to end.",
        "grammar_tip": "anstatt dass = statt dass -> Verb am Ende"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 3: Passiv Transformer (B1-C1)
# Exercise type: transformation
# ═══════════════════════════════════════════════════════════

PASSIV_EXERCISES = [
    # ── B1: Vorgangspassiv Präsens ──
    {
        "id": "pass_001",
        "module": "passiv",
        "type": "transformation",
        "level": 2,
        "topic": "vorgangspassiv_praesens",
        "data": {
            "source": "Der Architekt baut das Haus.",
            "target_words": ["Das", "Haus", "wird", "vom", "Architekten", "gebaut"],
            "correct_order": "Das Haus wird vom Architekten gebaut.",
            "optional_words": ["vom", "Architekten"],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Vorgangspassiv Präsens: Akkusativobjekt -> Subjekt, werden + Partizip II",
        "grammar_tip": "Aktiv -> Passiv: Objekt wird Subjekt, werden + Partizip II"
    },
    {
        "id": "pass_002",
        "module": "passiv",
        "type": "transformation",
        "level": 2,
        "topic": "vorgangspassiv_praesens",
        "data": {
            "source": "Die Lehrerin erklärt die Grammatik.",
            "target_words": ["Die", "Grammatik", "wird", "von", "der", "Lehrerin", "erklärt"],
            "correct_order": "Die Grammatik wird von der Lehrerin erklärt.",
            "optional_words": ["von", "der", "Lehrerin"],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Vorgangspassiv Präsens: werden + Partizip II",
        "grammar_tip": "Subjekt (Aktiv) -> von + Dativ (Passiv)"
    },
    {
        "id": "pass_003",
        "module": "passiv",
        "type": "transformation",
        "level": 2,
        "topic": "vorgangspassiv_praesens",
        "data": {
            "source": "Man repariert die Straße.",
            "target_words": ["Die", "Straße", "wird", "repariert"],
            "correct_order": "Die Straße wird repariert.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "With 'man' as subject, no agent is needed in passive.",
        "grammar_tip": "man + Aktiv -> Passiv ohne Agens (kein 'von ...')"
    },
    # ── B1: Vorgangspassiv Präteritum ──
    {
        "id": "pass_004",
        "module": "passiv",
        "type": "transformation",
        "level": 2,
        "topic": "vorgangspassiv_praeteritum",
        "data": {
            "source": "Der Koch bereitete das Essen vor.",
            "target_words": ["Das", "Essen", "wurde", "vom", "Koch", "vorbereitet"],
            "correct_order": "Das Essen wurde vom Koch vorbereitet.",
            "optional_words": ["vom", "Koch"],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Vorgangspassiv Präteritum: wurde + Partizip II",
        "grammar_tip": "Präteritum Passiv: wurde (nicht 'wird') + Partizip II"
    },
    {
        "id": "pass_005",
        "module": "passiv",
        "type": "transformation",
        "level": 2,
        "topic": "vorgangspassiv_praeteritum",
        "data": {
            "source": "Man baute die Brücke im letzten Jahr.",
            "target_words": ["Die", "Brücke", "wurde", "im", "letzten", "Jahr", "gebaut"],
            "correct_order": "Die Brücke wurde im letzten Jahr gebaut.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Passiv Präteritum with 'man': no agent needed.",
        "grammar_tip": "wurde + Partizip II (Präteritum Passiv)"
    },
    # ── B2: Passiv mit Modalverb ──
    {
        "id": "pass_006",
        "module": "passiv",
        "type": "transformation",
        "level": 3,
        "topic": "passiv_modal",
        "data": {
            "source": "Man muss das Problem lösen.",
            "target_words": ["Das", "Problem", "muss", "gelöst", "werden"],
            "correct_order": "Das Problem muss gelöst werden.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Passiv mit Modalverb: Modalverb + Partizip II + werden",
        "grammar_tip": "Modal + Passiv: Subjekt + Modalverb + Partizip II + werden"
    },
    {
        "id": "pass_007",
        "module": "passiv",
        "type": "transformation",
        "level": 3,
        "topic": "passiv_modal",
        "data": {
            "source": "Man kann die Aufgabe schnell erledigen.",
            "target_words": ["Die", "Aufgabe", "kann", "schnell", "erledigt", "werden"],
            "correct_order": "Die Aufgabe kann schnell erledigt werden.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Passive with modal: Modalverb stays conjugated, Partizip II + werden at end.",
        "grammar_tip": "kann/muss/soll + Partizip II + werden"
    },
    # ── B2: Passiv in Nebensätzen ──
    {
        "id": "pass_008",
        "module": "passiv",
        "type": "transformation",
        "level": 3,
        "topic": "passiv_nebensatz",
        "data": {
            "source": "Er sagt, dass man das Haus renovieren muss.",
            "target_words": ["Er", "sagt", "dass", "das", "Haus", "renoviert", "werden", "muss"],
            "correct_order": "Er sagt, dass das Haus renoviert werden muss.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Passive with modal in subordinate clause: Partizip II + werden + Modalverb at end.",
        "grammar_tip": "Nebensatz-Passiv + Modal: ...Partizip II + werden + Modal (am Ende)"
    },
    # ── B2: Zustandspassiv ──
    {
        "id": "pass_009",
        "module": "passiv",
        "type": "transformation",
        "level": 3,
        "topic": "zustandspassiv",
        "data": {
            "source": "Man hat die Tür geöffnet.",
            "target_words": ["Die", "Tür", "ist", "geöffnet"],
            "correct_order": "Die Tür ist geöffnet.",
            "optional_words": [],
            "transform_type": "aktiv_zu_zustandspassiv"
        },
        "grammar_rule": "Zustandspassiv: sein + Partizip II (describes result/state).",
        "grammar_tip": "Zustandspassiv = Ergebnis: sein + Partizip II (Die Tür IST geöffnet)"
    },
    # ── C1: Passiv Perfekt + Modalverb ──
    {
        "id": "pass_010",
        "module": "passiv",
        "type": "transformation",
        "level": 4,
        "topic": "passiv_perfekt_modal",
        "data": {
            "source": "Man hätte das Haus früher bauen müssen.",
            "target_words": ["Das", "Haus", "hätte", "früher", "gebaut", "werden", "müssen"],
            "correct_order": "Das Haus hätte früher gebaut werden müssen.",
            "optional_words": [],
            "transform_type": "aktiv_zu_passiv"
        },
        "grammar_rule": "Passiv Perfekt + Modal: hätte/hat + Partizip II + werden + Modalverb (Infinitiv)",
        "grammar_tip": "Konjunktiv II Passiv + Modal: hätte + Part. II + werden + Infinitiv"
    },
    # ── C1: Passiversatzformen ──
    {
        "id": "pass_011",
        "module": "passiv",
        "type": "transformation",
        "level": 4,
        "topic": "passiversatzform",
        "data": {
            "source": "Das Problem kann gelöst werden.",
            "target_words": ["Das", "Problem", "lässt", "sich", "lösen"],
            "correct_order": "Das Problem lässt sich lösen.",
            "optional_words": [],
            "transform_type": "passiv_zu_ersatzform"
        },
        "grammar_rule": "Passiversatzform with 'sich lassen': Das lässt sich machen = Das kann gemacht werden.",
        "grammar_tip": "sich lassen + Infinitiv = können + Partizip II + werden"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 4: Konjunktiv II Workshop (B1-C1)
# Exercise type: reconstruction + gap_fill
# ═══════════════════════════════════════════════════════════

KONJUNKTIV_EXERCISES = [
    # ── B1: würde + Infinitiv (reconstruction) ──
    {
        "id": "konj_001",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 2,
        "topic": "wuerde_infinitiv",
        "data": {
            "text": "Wenn ich mehr Geld hätte, würde ich eine Weltreise machen.",
            "verbs": ["hätte", "würde", "machen"],
            "clause_type": "konjunktiv_wenn"
        },
        "grammar_rule": "Konjunktiv II with wenn-clause: hätte/wäre in wenn-clause, würde+Infinitiv in main clause.",
        "grammar_tip": "Wenn + Konj. II (hätte/wäre), Hauptsatz: würde + Infinitiv"
    },
    {
        "id": "konj_002",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 2,
        "topic": "wuerde_infinitiv",
        "data": {
            "text": "Ich würde gern nach Berlin fahren.",
            "verbs": ["würde", "fahren"],
            "clause_type": "konjunktiv_wunsch"
        },
        "grammar_rule": "Konjunktiv II wish: würde + gern + Infinitiv",
        "grammar_tip": "würde + gern + Infinitiv = polite wish"
    },
    # ── B1: hätte, wäre, könnte ──
    {
        "id": "konj_003",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 2,
        "topic": "haette_waere",
        "data": {
            "text": "Wenn ich reich wäre, hätte ich ein großes Haus.",
            "verbs": ["wäre", "hätte"],
            "clause_type": "konjunktiv_wenn"
        },
        "grammar_rule": "Konjunktiv II of sein (wäre) and haben (hätte) in conditional sentences.",
        "grammar_tip": "sein -> wäre, haben -> hätte (immer Konjunktiv II, nie würde!)"
    },
    {
        "id": "konj_004",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 2,
        "topic": "haette_waere",
        "data": {
            "text": "Wenn ich doch mehr Zeit hätte!",
            "verbs": ["hätte"],
            "clause_type": "irrealer_wunsch"
        },
        "grammar_rule": "Irrealer Wunschsatz with 'doch': Wenn + doch + Konjunktiv II!",
        "grammar_tip": "Wunsch: Wenn ich doch ... hätte/wäre/könnte!"
    },
    # ── B2: Konjunktiv II Vergangenheit ──
    {
        "id": "konj_005",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 3,
        "topic": "konj2_vergangenheit",
        "data": {
            "text": "Wenn ich das gewusst hätte, wäre ich früher gekommen.",
            "verbs": ["gewusst", "hätte", "wäre", "gekommen"],
            "clause_type": "konjunktiv_vergangenheit"
        },
        "grammar_rule": "Konjunktiv II Past: hätte/wäre + Partizip II for unrealized past conditions.",
        "grammar_tip": "Vergangenheit: hätte + Partizip II / wäre + Partizip II"
    },
    {
        "id": "konj_006",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 3,
        "topic": "konj2_vergangenheit",
        "data": {
            "text": "Wenn er rechtzeitig losgefahren wäre, hätte er den Zug erreicht.",
            "verbs": ["losgefahren", "wäre", "hätte", "erreicht"],
            "clause_type": "konjunktiv_vergangenheit"
        },
        "grammar_rule": "Konjunktiv II past: irreale Bedingung in der Vergangenheit.",
        "grammar_tip": "wäre + Part. II (Bewegung), hätte + Part. II (andere Verben)"
    },
    # ── B2: Als-ob-Sätze ──
    {
        "id": "konj_007",
        "module": "konjunktiv",
        "type": "reconstruction",
        "level": 3,
        "topic": "als_ob",
        "data": {
            "text": "Er tut so, als ob er nichts wüsste.",
            "verbs": ["tut", "wüsste"],
            "clause_type": "als_ob_konjunktiv"
        },
        "grammar_rule": "'als ob' requires Konjunktiv II, verb goes to end of clause.",
        "grammar_tip": "als ob + Konjunktiv II (Verb am Ende): als ob er das wüsste"
    },
    # ── C1: Konjunktiv I (indirekte Rede) ──
    {
        "id": "konj_008",
        "module": "konjunktiv",
        "type": "gap_fill",
        "level": 4,
        "topic": "konjunktiv_1",
        "data": {
            "sentence_template": "Er sagte, er {gap_1} keine Zeit.",
            "gaps": [{
                "position": "gap_1",
                "context": "er ___ keine Zeit",
                "answer": "habe",
                "options": ["hat", "habe", "hätte", "hatte", "haben"],
                "indicative_hint": "er hat -> Konjunktiv I?"
            }],
            "full_correct": "Er sagte, er habe keine Zeit."
        },
        "grammar_rule": "Konjunktiv I for indirect speech: haben -> habe (3rd person singular).",
        "grammar_tip": "Konjunktiv I: er habe, sie sei, man könne (indirekte Rede)"
    },
    {
        "id": "konj_009",
        "module": "konjunktiv",
        "type": "gap_fill",
        "level": 4,
        "topic": "konjunktiv_1",
        "data": {
            "sentence_template": "Die Zeitung berichtet, der Minister {gap_1} zurückgetreten.",
            "gaps": [{
                "position": "gap_1",
                "context": "der Minister ___ zurückgetreten",
                "answer": "sei",
                "options": ["ist", "sei", "wäre", "war", "sein"],
                "indicative_hint": "er ist -> Konjunktiv I?"
            }],
            "full_correct": "Die Zeitung berichtet, der Minister sei zurückgetreten."
        },
        "grammar_rule": "Konjunktiv I of 'sein' = 'sei' for reported speech.",
        "grammar_tip": "sein -> sei (Konjunktiv I, immer eindeutig!)"
    },
    # ── C1: Konjunktiv I vs. II in indirekter Rede ──
    {
        "id": "konj_010",
        "module": "konjunktiv",
        "type": "gap_fill",
        "level": 4,
        "topic": "konj1_vs_konj2",
        "data": {
            "sentence_template": "Sie sagten, sie {gap_1} keine Zeit.",
            "gaps": [{
                "position": "gap_1",
                "context": "sie ___ keine Zeit",
                "answer": "hätten",
                "options": ["haben", "habe", "hätten", "hatten", "hätte"],
                "indicative_hint": "sie haben -> K1=haben (=Indikativ!) -> K2?"
            }],
            "full_correct": "Sie sagten, sie hätten keine Zeit."
        },
        "grammar_rule": "When K1 is identical to indicative (sie haben = sie haben), use K2 instead (hätten).",
        "grammar_tip": "K1 = Indikativ? -> Ersatz durch K2 (hätten statt haben)"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 5: Relativsätze Builder (B1-C1)
# Exercise type: reconstruction
# ═══════════════════════════════════════════════════════════

RELATIV_EXERCISES = [
    # ── B1: Relativsätze Nominativ/Akkusativ ──
    {
        "id": "rel_001",
        "module": "relativ",
        "type": "reconstruction",
        "level": 2,
        "topic": "relativpronomen_nom",
        "data": {
            "text": "Der Mann, der neben mir wohnt, ist Arzt.",
            "verbs": ["wohnt", "ist"],
            "clause_type": "relativsatz_nom",
            "sentence_a": "Der Mann ist Arzt.",
            "sentence_b": "Der Mann wohnt neben mir."
        },
        "grammar_rule": "Relativpronomen 'der' = Nominativ maskulin (subject of relative clause).",
        "grammar_tip": "Wer/Was ist Subjekt im Relativsatz? -> Nominativ (der/die/das)"
    },
    {
        "id": "rel_002",
        "module": "relativ",
        "type": "reconstruction",
        "level": 2,
        "topic": "relativpronomen_akk",
        "data": {
            "text": "Das Buch, das ich gestern gekauft habe, ist sehr spannend.",
            "verbs": ["gekauft", "habe", "ist"],
            "clause_type": "relativsatz_akk",
            "sentence_a": "Das Buch ist sehr spannend.",
            "sentence_b": "Ich habe das Buch gestern gekauft."
        },
        "grammar_rule": "Relativpronomen 'das' = Akkusativ neutrum (object of relative clause).",
        "grammar_tip": "Was ist Objekt im Relativsatz? -> Akkusativ (den/die/das)"
    },
    {
        "id": "rel_003",
        "module": "relativ",
        "type": "reconstruction",
        "level": 2,
        "topic": "relativpronomen_nom",
        "data": {
            "text": "Die Frau, die dort arbeitet, kennt meinen Bruder.",
            "verbs": ["arbeitet", "kennt"],
            "clause_type": "relativsatz_nom",
            "sentence_a": "Die Frau kennt meinen Bruder.",
            "sentence_b": "Die Frau arbeitet dort."
        },
        "grammar_rule": "Relativpronomen 'die' = Nominativ feminin.",
        "grammar_tip": "feminin + Nominativ -> die (Relativpronomen)"
    },
    # ── B1: Relativsätze Dativ ──
    {
        "id": "rel_004",
        "module": "relativ",
        "type": "reconstruction",
        "level": 2,
        "topic": "relativpronomen_dat",
        "data": {
            "text": "Die Frau, der ich geholfen habe, hat sich bedankt.",
            "verbs": ["geholfen", "habe", "bedankt"],
            "clause_type": "relativsatz_dat",
            "sentence_a": "Die Frau hat sich bedankt.",
            "sentence_b": "Ich habe der Frau geholfen."
        },
        "grammar_rule": "Relativpronomen 'der' = Dativ feminin (helfen + Dativ).",
        "grammar_tip": "Dativverb (helfen, danken, gefallen) -> Dativ-Relativpronomen"
    },
    # ── B2: Relativsätze mit Präposition ──
    {
        "id": "rel_005",
        "module": "relativ",
        "type": "reconstruction",
        "level": 3,
        "topic": "relativpronomen_praep",
        "data": {
            "text": "Das Thema, über das wir gesprochen haben, ist wichtig.",
            "verbs": ["gesprochen", "haben", "ist"],
            "clause_type": "relativsatz_praep",
            "sentence_a": "Das Thema ist wichtig.",
            "sentence_b": "Wir haben über das Thema gesprochen."
        },
        "grammar_rule": "Präposition + Relativpronomen: 'über das' (sprechen über + Akk.).",
        "grammar_tip": "Verb + Präposition -> Präposition + Relativpronomen"
    },
    {
        "id": "rel_006",
        "module": "relativ",
        "type": "reconstruction",
        "level": 3,
        "topic": "relativpronomen_praep",
        "data": {
            "text": "Der Kollege, mit dem ich zusammenarbeite, ist sehr kompetent.",
            "verbs": ["zusammenarbeite", "ist"],
            "clause_type": "relativsatz_praep",
            "sentence_a": "Der Kollege ist sehr kompetent.",
            "sentence_b": "Ich arbeite mit dem Kollegen zusammen."
        },
        "grammar_rule": "Präposition + Relativpronomen: 'mit dem' (zusammenarbeiten mit + Dat.).",
        "grammar_tip": "mit + Dativ -> mit dem/der/dem/denen (Relativpronomen)"
    },
    # ── B2: Relativsätze mit wo, was, wer ──
    {
        "id": "rel_007",
        "module": "relativ",
        "type": "reconstruction",
        "level": 3,
        "topic": "relativpronomen_was_wo",
        "data": {
            "text": "Alles, was er sagt, ist wahr.",
            "verbs": ["sagt", "ist"],
            "clause_type": "relativsatz_was"
        },
        "grammar_rule": "After alles/nichts/etwas/das, use 'was' as relative pronoun.",
        "grammar_tip": "alles/nichts/etwas/das + was (nie 'das'!)"
    },
    # ── C1: Erweiterte Relativsätze (Genitiv) ──
    {
        "id": "rel_008",
        "module": "relativ",
        "type": "reconstruction",
        "level": 4,
        "topic": "relativpronomen_gen",
        "data": {
            "text": "Der Autor, dessen Buch ich gelesen habe, kommt aus Berlin.",
            "verbs": ["gelesen", "habe", "kommt"],
            "clause_type": "relativsatz_genitiv",
            "sentence_a": "Der Autor kommt aus Berlin.",
            "sentence_b": "Ich habe das Buch des Autors gelesen."
        },
        "grammar_rule": "Genitiv-Relativpronomen 'dessen' (mask./neutrum) / 'deren' (fem./plural).",
        "grammar_tip": "Genitiv: dessen (mask./neutr.) / deren (fem./plural)"
    },
    # ── C1: Verschachtelte Relativsätze ──
    {
        "id": "rel_009",
        "module": "relativ",
        "type": "reconstruction",
        "level": 4,
        "topic": "verschachtelt_relativ",
        "data": {
            "text": "Das Haus, das der Mann, den ich kenne, gebaut hat, steht am Fluss.",
            "verbs": ["kenne", "gebaut", "hat", "steht"],
            "clause_type": "verschachtelte_relativsaetze"
        },
        "grammar_rule": "Nested relative clauses: inner clause 'den ich kenne' embedded in outer relative.",
        "grammar_tip": "Verschachtelt: innerer Relativsatz unterbricht den äußeren"
    },
    {
        "id": "rel_010",
        "module": "relativ",
        "type": "reconstruction",
        "level": 4,
        "topic": "verschachtelt_relativ",
        "data": {
            "text": "Die Firma, deren Mitarbeiter, die gut ausgebildet sind, effizient arbeiten, wächst schnell.",
            "verbs": ["ausgebildet", "sind", "arbeiten", "wächst"],
            "clause_type": "verschachtelte_relativsaetze"
        },
        "grammar_rule": "Multiple nested relative clauses with deren (Genitiv plural).",
        "grammar_tip": "deren = Genitiv Plural/Feminin, verschachtelte Relativsätze"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 6: Präpositionen & Kasus Driller (A2-B2)
# Exercise type: quick_select
# ═══════════════════════════════════════════════════════════

PRAEPOSITION_EXERCISES = [
    # ── A2: Wechselpräpositionen (Dativ vs. Akkusativ) ──
    {
        "id": "praep_001",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "wechselpraep",
        "data": {
            "sentence": "Die Katze springt {gap_1} Tisch.",
            "gaps": [{
                "position": "gap_1",
                "options": ["auf den", "auf dem", "auf das"],
                "answer": "auf den",
                "explanation": "Wohin? -> Akkusativ (Bewegung mit Richtung). Tisch = maskulin -> den"
            }]
        },
        "grammar_rule": "Wechselpräpositionen: Wohin? -> Akkusativ, Wo? -> Dativ",
        "grammar_tip": "Wohin? = Akkusativ (Bewegung), Wo? = Dativ (Position)"
    },
    {
        "id": "praep_002",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "wechselpraep",
        "data": {
            "sentence": "Die Katze sitzt {gap_1} Tisch.",
            "gaps": [{
                "position": "gap_1",
                "options": ["auf den", "auf dem", "auf das"],
                "answer": "auf dem",
                "explanation": "Wo? -> Dativ (keine Bewegung, Position). Tisch = maskulin -> dem"
            }]
        },
        "grammar_rule": "Wechselpräpositionen: Wo? -> Dativ (Position/Zustand)",
        "grammar_tip": "sitzen/liegen/stehen/hängen = Wo? = Dativ"
    },
    {
        "id": "praep_003",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "wechselpraep",
        "data": {
            "sentence": "Ich gehe {gap_1} Küche.",
            "gaps": [{
                "position": "gap_1",
                "options": ["in die", "in der", "in das"],
                "answer": "in die",
                "explanation": "Wohin? -> Akkusativ. Küche = feminin -> die"
            }]
        },
        "grammar_rule": "Wechselpräpositionen: gehen -> Wohin? -> Akkusativ",
        "grammar_tip": "gehen/legen/stellen/setzen = Wohin? = Akkusativ"
    },
    {
        "id": "praep_004",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "wechselpraep",
        "data": {
            "sentence": "Das Bild hängt {gap_1} Wand.",
            "gaps": [{
                "position": "gap_1",
                "options": ["an die", "an der", "an dem"],
                "answer": "an der",
                "explanation": "Wo? -> Dativ. Wand = feminin -> der"
            }]
        },
        "grammar_rule": "hängen (intransitiv) = Wo? -> Dativ",
        "grammar_tip": "hängen (hängt) = Wo? = Dativ / hängen (hängt auf) = Wohin? = Akkusativ"
    },
    # ── A2: Verben mit festen Präpositionen ──
    {
        "id": "praep_005",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "feste_praep",
        "data": {
            "sentence": "Ich warte {gap_1} Bus.",
            "gaps": [{
                "position": "gap_1",
                "options": ["auf den", "für den", "an den"],
                "answer": "auf den",
                "explanation": "warten auf + Akkusativ. Bus = maskulin -> den"
            }]
        },
        "grammar_rule": "warten auf + Akkusativ (fixed preposition)",
        "grammar_tip": "warten AUF + Akk., sich freuen AUF + Akk. (Zukunft)"
    },
    {
        "id": "praep_006",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 1,
        "topic": "feste_praep",
        "data": {
            "sentence": "Sie interessiert sich {gap_1} Kunst.",
            "gaps": [{
                "position": "gap_1",
                "options": ["für", "auf", "an"],
                "answer": "für",
                "explanation": "sich interessieren für + Akkusativ"
            }]
        },
        "grammar_rule": "sich interessieren für + Akkusativ",
        "grammar_tip": "sich interessieren FÜR, sich entscheiden FÜR"
    },
    # ── B1: Genitiv-Präpositionen ──
    {
        "id": "praep_007",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 2,
        "topic": "genitiv_praep",
        "data": {
            "sentence": "{gap_1} Regens bleiben wir zu Hause.",
            "gaps": [{
                "position": "gap_1",
                "options": ["Wegen des", "Wegen dem", "Wegen den"],
                "answer": "Wegen des",
                "explanation": "wegen + Genitiv. Regen = maskulin -> des Regens"
            }]
        },
        "grammar_rule": "wegen + Genitiv (formal German)",
        "grammar_tip": "wegen/trotz/während/statt + Genitiv (Schriftsprache)"
    },
    {
        "id": "praep_008",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 2,
        "topic": "genitiv_praep",
        "data": {
            "sentence": "{gap_1} Kälte geht er ohne Jacke raus.",
            "gaps": [{
                "position": "gap_1",
                "options": ["Trotz der", "Trotz die", "Trotz dem"],
                "answer": "Trotz der",
                "explanation": "trotz + Genitiv. Kälte = feminin -> der Kälte"
            }]
        },
        "grammar_rule": "trotz + Genitiv (despite)",
        "grammar_tip": "trotz + Genitiv: trotz des Wetters, trotz der Kälte"
    },
    # ── B1: Pronominaladverbien ──
    {
        "id": "praep_009",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 2,
        "topic": "pronominaladverb",
        "data": {
            "sentence": "{gap_1} wartest du? — Auf den Bus.",
            "gaps": [{
                "position": "gap_1",
                "options": ["Worauf", "Auf was", "Wofür"],
                "answer": "Worauf",
                "explanation": "warten auf -> worauf (Pronominaladverb für Sachen)"
            }]
        },
        "grammar_rule": "Pronominaladverb: wo(r) + Präposition for things, not people.",
        "grammar_tip": "Sache: worauf/wofür/woran — Person: auf wen/für wen/an wen"
    },
    {
        "id": "praep_010",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 2,
        "topic": "pronominaladverb",
        "data": {
            "sentence": "Ich freue mich {gap_1}. (= auf das Konzert)",
            "gaps": [{
                "position": "gap_1",
                "options": ["darauf", "dafür", "damit"],
                "answer": "darauf",
                "explanation": "sich freuen auf -> darauf (da(r) + Präposition)"
            }]
        },
        "grammar_rule": "Pronominaladverb: da(r) + Präposition replaces Präposition + Pronomen for things.",
        "grammar_tip": "darauf = auf das, dafür = für das, damit = mit dem"
    },
    # ── B2: Funktionsverbgefüge ──
    {
        "id": "praep_011",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 3,
        "topic": "funktionsverbgefuege",
        "data": {
            "sentence": "Wir müssen das Problem {gap_1} nehmen.",
            "gaps": [{
                "position": "gap_1",
                "options": ["in Angriff", "unter Angriff", "zum Angriff"],
                "answer": "in Angriff",
                "explanation": "in Angriff nehmen = begin to tackle (Funktionsverbgefüge)"
            }]
        },
        "grammar_rule": "Funktionsverbgefüge: in Angriff nehmen = anfangen zu bearbeiten",
        "grammar_tip": "FVG lernt man am besten als feste Wendungen"
    },
    {
        "id": "praep_012",
        "module": "praepositionen",
        "type": "quick_select",
        "level": 3,
        "topic": "funktionsverbgefuege",
        "data": {
            "sentence": "Der Plan wird {gap_1} gestellt.",
            "gaps": [{
                "position": "gap_1",
                "options": ["in Frage", "zur Frage", "auf Frage"],
                "answer": "in Frage",
                "explanation": "in Frage stellen = to question/challenge (Funktionsverbgefüge)"
            }]
        },
        "grammar_rule": "in Frage stellen = bezweifeln, hinterfragen",
        "grammar_tip": "in Frage stellen, zur Verfügung stellen, in Betracht ziehen"
    },
]

# ═══════════════════════════════════════════════════════════
# MODULE 7: Nominalisierung & Umformung (B2-C1)
# Exercise type: transformation
# ═══════════════════════════════════════════════════════════

NOMINALISIERUNG_EXERCISES = [
    # ── B2: Nebensatz -> Nominalisierung ──
    {
        "id": "nom_001",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 3,
        "topic": "nebensatz_zu_nominal",
        "data": {
            "source": "Weil es stark regnet, bleiben wir zu Hause.",
            "target_words": ["Wegen", "des", "starken", "Regens", "bleiben", "wir", "zu", "Hause"],
            "correct_order": "Wegen des starken Regens bleiben wir zu Hause.",
            "optional_words": [],
            "transform_type": "nebensatz_zu_nominal"
        },
        "grammar_rule": "weil + Verb -> wegen + Genitiv-Nomen (Nominalisierung)",
        "grammar_tip": "weil es regnet -> wegen des Regens"
    },
    {
        "id": "nom_002",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 3,
        "topic": "nebensatz_zu_nominal",
        "data": {
            "source": "Obwohl das Wetter schlecht ist, gehen wir spazieren.",
            "target_words": ["Trotz", "des", "schlechten", "Wetters", "gehen", "wir", "spazieren"],
            "correct_order": "Trotz des schlechten Wetters gehen wir spazieren.",
            "optional_words": [],
            "transform_type": "nebensatz_zu_nominal"
        },
        "grammar_rule": "obwohl + Satz -> trotz + Genitiv (Nominalisierung)",
        "grammar_tip": "obwohl ... -> trotz + Genitiv"
    },
    {
        "id": "nom_003",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 3,
        "topic": "nebensatz_zu_nominal",
        "data": {
            "source": "Während er studierte, arbeitete er auch.",
            "target_words": ["Während", "des", "Studiums", "arbeitete", "er", "auch"],
            "correct_order": "Während des Studiums arbeitete er auch.",
            "optional_words": [],
            "transform_type": "nebensatz_zu_nominal"
        },
        "grammar_rule": "während + Nebensatz -> während + Genitiv-Nomen",
        "grammar_tip": "während er studierte -> während des Studiums"
    },
    # ── B2: Infinitivsätze ──
    {
        "id": "nom_004",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 3,
        "topic": "infinitivsatz",
        "data": {
            "source": "Er arbeitet viel. Er will erfolgreich sein.",
            "target_words": ["Er", "arbeitet", "viel", "um", "erfolgreich", "zu", "sein"],
            "correct_order": "Er arbeitet viel, um erfolgreich zu sein.",
            "optional_words": [],
            "transform_type": "satz_zu_infinitiv"
        },
        "grammar_rule": "Purpose clause: um ... zu + Infinitiv (= damit + Nebensatz)",
        "grammar_tip": "um ... zu + Infinitiv = Zweck/Ziel (gleiches Subjekt!)"
    },
    {
        "id": "nom_005",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 3,
        "topic": "infinitivsatz",
        "data": {
            "source": "Er ging weg. Er verabschiedete sich nicht.",
            "target_words": ["Er", "ging", "weg", "ohne", "sich", "zu", "verabschieden"],
            "correct_order": "Er ging weg, ohne sich zu verabschieden.",
            "optional_words": [],
            "transform_type": "satz_zu_infinitiv"
        },
        "grammar_rule": "ohne ... zu + Infinitiv = without doing something",
        "grammar_tip": "ohne ... zu + Infinitiv = ohne dass + Nebensatz"
    },
    # ── C1: Nomen-Verb-Verbindungen ──
    {
        "id": "nom_006",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 4,
        "topic": "nomen_verb",
        "data": {
            "source": "Das Team muss sich jetzt entscheiden.",
            "target_words": ["Das", "Team", "muss", "jetzt", "eine", "Entscheidung", "treffen"],
            "correct_order": "Das Team muss jetzt eine Entscheidung treffen.",
            "optional_words": [],
            "transform_type": "verb_zu_nomen"
        },
        "grammar_rule": "sich entscheiden -> eine Entscheidung treffen (Nomen-Verb-Verbindung)",
        "grammar_tip": "Verb -> Nomen-Verb-Verbindung (formaler Stil)"
    },
    {
        "id": "nom_007",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 4,
        "topic": "nomen_verb",
        "data": {
            "source": "Die Opposition kritisiert die Regierung.",
            "target_words": ["Die", "Opposition", "übt", "Kritik", "an", "der", "Regierung"],
            "correct_order": "Die Opposition übt Kritik an der Regierung.",
            "optional_words": [],
            "transform_type": "verb_zu_nomen"
        },
        "grammar_rule": "kritisieren -> Kritik üben an + Dativ",
        "grammar_tip": "kritisieren -> Kritik üben an + Dat. (Nomen-Verb-Verbindung)"
    },
    # ── C1: Partizipialkonstruktionen ──
    {
        "id": "nom_008",
        "module": "nominalisierung",
        "type": "transformation",
        "level": 4,
        "topic": "partizipialkonstruktion",
        "data": {
            "source": "Die Proteste, die seit Wochen andauern, werden immer größer.",
            "target_words": ["Die", "seit", "Wochen", "andauernden", "Proteste", "werden", "immer", "größer"],
            "correct_order": "Die seit Wochen andauernden Proteste werden immer größer.",
            "optional_words": [],
            "transform_type": "relativsatz_zu_partizip"
        },
        "grammar_rule": "Relative clause -> Partizipialattribut: die andauern -> die andauernden",
        "grammar_tip": "Relativsatz -> Partizip I + Deklination (aktiv, gleichzeitig)"
    },
]


# ═══════════════════════════════════════════════════════════
# ALL EXERCISES combined
# ═══════════════════════════════════════════════════════════

ALL_GRAMMAR_EXERCISES = (
    ADJECTIVE_EXERCISES +
    KONNEKTOR_EXERCISES +
    PASSIV_EXERCISES +
    KONJUNKTIV_EXERCISES +
    RELATIV_EXERCISES +
    PRAEPOSITION_EXERCISES +
    NOMINALISIERUNG_EXERCISES
)


def get_exercises_by_module(module, level=None):
    """Get exercises filtered by module and optionally by level."""
    pool = [e for e in ALL_GRAMMAR_EXERCISES if e["module"] == module]
    if level is not None:
        pool = [e for e in pool if e["level"] == level]
    return pool


def get_exercise_by_id(exercise_id):
    """Get a specific exercise by its ID."""
    for e in ALL_GRAMMAR_EXERCISES:
        if e["id"] == exercise_id:
            return e
    return None


def count_by_module_and_level():
    """Count exercises per module and level."""
    counts = {}
    for e in ALL_GRAMMAR_EXERCISES:
        module = e["module"]
        level = e["level"]
        if module not in counts:
            counts[module] = {}
        counts[module][level] = counts[module].get(level, 0) + 1
    return counts
