"""
Micro-Curricula — error-driven remediation sequences.

Each error category maps to a curriculum: a list of 3-5 steps.
Step types:
  - minimal_pair: Show correct/incorrect contrast pairs (study step)
  - matrix_display: Show grammar reference table (study step)
  - controlled_drill: Filter existing exercises by module/topic
  - discrimination: Exercise from contrasting confusion set side
  - transfer: Near-transfer exercise (same structure, new context)
  - far_transfer: Free-writing prompt (display-only)
"""

MICRO_CURRICULA = {
    "auxiliary_before_participle": {
        "name": "Hilfsverb-Partizip Reihenfolge",
        "description": "Partizip II kommt VOR dem Hilfsverb im Nebensatz",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Vergleiche: Welche Reihenfolge ist richtig im Nebensatz?",
                "pairs": [
                    {
                        "correct": "...dass er das Buch gelesen hat.",
                        "incorrect": "...dass er das Buch hat gelesen.",
                        "rule": "Partizip II + Hilfsverb"
                    },
                    {
                        "correct": "...weil sie nach Hause gegangen ist.",
                        "incorrect": "...weil sie nach Hause ist gegangen.",
                        "rule": "Partizip II + sein"
                    },
                    {
                        "correct": "...obwohl er den Brief geschrieben hatte.",
                        "incorrect": "...obwohl er den Brief hatte geschrieben.",
                        "rule": "Partizip II + Hilfsverb (Plusquamperfekt)"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "verb_position", "clause_type_contains": "perfekt"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konnektoren", "topic": "nebensatz_konnektor"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "verb_position"}
            }
        ]
    },

    "inversion_missing": {
        "name": "Inversion nach Adverbialkonnektoren",
        "description": "Nach deshalb/trotzdem steht das Verb an Position 2 (Inversion)",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Vergleiche: Konnektoren mit und ohne Inversion",
                "pairs": [
                    {
                        "connector": "deshalb",
                        "example": "Es regnet. Deshalb bleiben wir zu Hause.",
                        "rule": "Adverbialkonnektor -> Verb Position 2 (Inversion)",
                        "shows_inversion": True
                    },
                    {
                        "connector": "und",
                        "example": "Es regnet und wir bleiben zu Hause.",
                        "rule": "Konjunktion -> keine Inversion",
                        "shows_inversion": False
                    },
                    {
                        "connector": "trotzdem",
                        "example": "Es regnet. Trotzdem gehen wir spazieren.",
                        "rule": "Adverbialkonnektor -> Verb Position 2 (Inversion)",
                        "shows_inversion": True
                    },
                    {
                        "connector": "aber",
                        "example": "Es regnet, aber wir gehen spazieren.",
                        "rule": "Konjunktion -> keine Inversion",
                        "shows_inversion": False
                    },
                ]
            },
            {
                "type": "discrimination",
                "confusion_set": "weil_deshalb",
                "filter": {"module": "konnektoren", "topic": "adverbial_konnektor"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konnektoren", "topic": "adverbial_konnektor"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konnektoren", "topic": "hauptsatz_konnektor"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "konnektoren"}
            }
        ]
    },

    "wrong_relative_pronoun": {
        "name": "Relativpronomen: Genus + Kasus",
        "description": "Das Relativpronomen richtet sich nach Genus des Bezugsworts und Kasus im Relativsatz",
        "steps": [
            {
                "type": "matrix_display",
                "instruction": "Lerne diese Tabelle der Relativpronomen:",
                "matrix": {
                    "title": "Relativpronomen",
                    "headers": ["", "Maskulin", "Feminin", "Neutrum", "Plural"],
                    "rows": [
                        ["Nominativ", "der", "die", "das", "die"],
                        ["Akkusativ", "den", "die", "das", "die"],
                        ["Dativ", "dem", "der", "dem", "denen"],
                        ["Genitiv", "dessen", "deren", "dessen", "deren"]
                    ]
                }
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "relativ", "topic": "relativpronomen_nom"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "relativ", "topic": "relativpronomen_akk"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "relativ", "topic": "relativpronomen_dat"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "relativ"}
            }
        ]
    },

    "wrong_adjective_ending": {
        "name": "Adjektivendungen systematisch",
        "description": "Adjektivendungen hangen vom Artikel, Kasus und Genus ab",
        "steps": [
            {
                "type": "matrix_display",
                "instruction": "Adjektivendungen nach bestimmtem Artikel:",
                "matrix": {
                    "title": "Adjektivdeklination (bestimmter Artikel)",
                    "headers": ["", "Maskulin", "Feminin", "Neutrum", "Plural"],
                    "rows": [
                        ["Nominativ", "-e", "-e", "-e", "-en"],
                        ["Akkusativ", "-en", "-e", "-e", "-en"],
                        ["Dativ", "-en", "-en", "-en", "-en"],
                        ["Genitiv", "-en", "-en", "-en", "-en"]
                    ]
                }
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "adjektive", "topic": "adj_bestimmt"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "adjektive", "topic": "adj_unbestimmt"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "adjektive", "topic": "adj_ohne_artikel"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "adjektive"}
            }
        ]
    },

    "wrong_passive_form": {
        "name": "Vorgangs- vs. Zustandspassiv",
        "description": "Vorgangspassiv (werden + Partizip II) vs Zustandspassiv (sein + Partizip II)",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Vergleiche Vorgangspassiv (werden) und Zustandspassiv (sein):",
                "pairs": [
                    {
                        "correct": "Der Brief wird geschrieben. (Vorgang)",
                        "incorrect": "Der Brief ist geschrieben. (Zustand)",
                        "rule": "werden = Prozess / sein = Ergebnis"
                    },
                    {
                        "correct": "Das Fenster wird geöffnet. (jetzt gerade)",
                        "incorrect": "Das Fenster ist geöffnet. (schon offen)",
                        "rule": "werden = aktiver Vorgang / sein = resultierender Zustand"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "passiv", "topic": "vorgangspassiv_praesens"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "passiv", "topic": "zustandspassiv"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "passiv"}
            }
        ]
    },

    "wrong_konjunktiv_form": {
        "name": "Konjunktiv II vs. Konjunktiv I",
        "description": "K2 = irreale Bedingungen/Wünsche, K1 = indirekte Rede",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "K2 für irreale Situationen, K1 für indirekte Rede:",
                "pairs": [
                    {
                        "correct": "Wenn ich reich wäre, würde ich reisen. (K2 - irreal)",
                        "incorrect": "Er sagt, er sei reich. (K1 - indirekte Rede)",
                        "rule": "K2: wäre/hätte/würde + Infinitiv"
                    },
                    {
                        "correct": "Ich hätte gern mehr Zeit. (K2 - Wunsch)",
                        "incorrect": "Sie meint, sie habe keine Zeit. (K1 - Bericht)",
                        "rule": "K1: Stammform + -e (sei, habe, komme)"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konjunktiv", "topic": "konjunktiv_wenn"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konjunktiv"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "konjunktiv"}
            }
        ]
    },

    "wrong_preposition": {
        "name": "Wechselpräpositionen: Wohin vs. Wo",
        "description": "Bewegung (Akkusativ) vs. Ort (Dativ)",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Bewegung = Akkusativ (Wohin?), Ort = Dativ (Wo?):",
                "pairs": [
                    {
                        "correct": "Ich gehe in die Schule. (Wohin? -> Akk.)",
                        "incorrect": "Ich bin in der Schule. (Wo? -> Dat.)",
                        "rule": "Bewegung -> Akkusativ"
                    },
                    {
                        "correct": "Er legt das Buch auf den Tisch. (Wohin? -> Akk.)",
                        "incorrect": "Das Buch liegt auf dem Tisch. (Wo? -> Dat.)",
                        "rule": "legen/stellen/setzen -> Akk. / liegen/stehen/sitzen -> Dat."
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "praepositionen", "topic": "wechselpraep"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "praepositionen"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "praepositionen"}
            }
        ]
    },

    "wrong_nominalization": {
        "name": "Nominalisierung: Nebensatz zu Nomen",
        "description": "Nebensätze können als Nominalphrasen ausgedrückt werden",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Nebensatz vs. Nominalphrase:",
                "pairs": [
                    {
                        "correct": "Wegen des Regens bleiben wir.",
                        "incorrect": "Weil es regnet, bleiben wir.",
                        "rule": "weil + Nebensatz -> wegen + Genitiv"
                    },
                    {
                        "correct": "Trotz seiner Müdigkeit arbeitet er.",
                        "incorrect": "Obwohl er müde ist, arbeitet er.",
                        "rule": "obwohl + Nebensatz -> trotz + Genitiv"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "nominalisierung"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "nominalisierung"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "nominalisierung"}
            }
        ]
    },

    "verb_not_at_end": {
        "name": "Verb am Ende im Nebensatz",
        "description": "Im Nebensatz steht das konjugierte Verb am Ende",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Im Nebensatz wandert das Verb ans Ende:",
                "pairs": [
                    {
                        "correct": "Ich weiß, dass er morgen kommt.",
                        "incorrect": "Ich weiß, dass er kommt morgen.",
                        "rule": "dass/weil/wenn/obwohl -> Verb am Ende"
                    },
                    {
                        "correct": "Sie fragt, ob wir heute Zeit haben.",
                        "incorrect": "Sie fragt, ob wir haben heute Zeit.",
                        "rule": "ob -> Verb am Ende"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "verb_position"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "konnektoren", "topic": "nebensatz_konnektor"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "verb_position"}
            }
        ]
    },

    "wrong_verb_order": {
        "name": "Verbreihenfolge im Nebensatz",
        "description": "Bei mehreren Verben im Nebensatz: richtige Reihenfolge beachten",
        "steps": [
            {
                "type": "minimal_pair",
                "instruction": "Verbreihenfolge bei Modalverben und Perfekt:",
                "pairs": [
                    {
                        "correct": "...dass er kommen kann.",
                        "incorrect": "...dass er kann kommen.",
                        "rule": "Infinitiv + Modalverb (konjugiert)"
                    },
                    {
                        "correct": "...dass er hat kommen können. (Ersatzinfinitiv)",
                        "incorrect": "...dass er kommen gekonnt hat.",
                        "rule": "Ersatzinfinitiv bei Modal + Perfekt"
                    },
                ]
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "verb_position"}
            },
            {
                "type": "controlled_drill",
                "filter": {"module": "verb_position"}
            },
            {
                "type": "transfer",
                "stage": "near",
                "filter": {"module": "verb_position"}
            }
        ]
    },
}


def get_curriculum_for_error(error_category):
    """Return the curriculum dict for an error category, or None."""
    return MICRO_CURRICULA.get(error_category)


def get_current_step(session):
    """Given a micro_curriculum_sessions row dict, return the current step definition."""
    curriculum = MICRO_CURRICULA.get(session["curriculum_key"])
    if not curriculum:
        return None
    steps = curriculum["steps"]
    if session["current_step"] >= len(steps):
        return None
    return steps[session["current_step"]]


def get_curriculum_info(curriculum_key):
    """Get name and description for a curriculum."""
    curriculum = MICRO_CURRICULA.get(curriculum_key)
    if not curriculum:
        return {"name": "", "description": ""}
    return {
        "name": curriculum["name"],
        "description": curriculum.get("description", ""),
        "total_steps": len(curriculum["steps"])
    }
