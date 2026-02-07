"""
German Verb-End Torture Chamber — Sentence Bank & Generator.

Generates sentences with subordinate/nested clauses where verbs must go to the end.
Covers A2 → C1 progression with increasing complexity.

Verb-end rules tested:
1. Simple subordinate (dass, weil, obwohl, wenn, als, ob, damit, bevor, nachdem, während)
2. Relative clauses (der/die/das + verb at end)
3. Nested subordinate clauses (clause within clause)
4. Compound verb forms at clause end (hat ... gemacht, wird ... können)
5. Separable verbs in subordinate clauses (ankommt, aufsteht)
6. Double infinitive (hat ... lesen wollen)
7. Multiple nested clauses with correct verb stacking
"""

import random
import hashlib
import json

# ─── SENTENCE TEMPLATES ───────────────────────────────────────────────
# Each template:
#   id: unique identifier
#   text: full correct sentence
#   verbs: list of verbs that will be removed for the exercise
#   positions: indices (word-level) where each verb belongs
#   clause_type: what grammatical structure is tested
#   difficulty: 1=A2, 2=B1, 3=B2, 4=C1
#   explanation: why verbs go where they do

SENTENCE_BANK = [
    # ──────────── DIFFICULTY 1 (A2): Simple subordinate clauses ────────────
    {
        "id": "a2_dass_01",
        "text": "Ich weiß, dass er jeden Tag Deutsch lernt.",
        "verbs": ["lernt"],
        "slot_marker": "___",
        "clause_type": "dass_clause",
        "difficulty": 1,
        "explanation": "In a 'dass' clause, the conjugated verb moves to the final position."
    },
    {
        "id": "a2_dass_02",
        "text": "Sie sagt, dass sie morgen nach Berlin fährt.",
        "verbs": ["fährt"],
        "clause_type": "dass_clause",
        "difficulty": 1,
        "explanation": "In a 'dass' clause, the conjugated verb moves to the final position."
    },
    {
        "id": "a2_weil_01",
        "text": "Er bleibt zu Hause, weil er krank ist.",
        "verbs": ["ist"],
        "clause_type": "weil_clause",
        "difficulty": 1,
        "explanation": "In a 'weil' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_weil_02",
        "text": "Ich lerne Deutsch, weil ich in Deutschland arbeite.",
        "verbs": ["arbeite"],
        "clause_type": "weil_clause",
        "difficulty": 1,
        "explanation": "In a 'weil' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_wenn_01",
        "text": "Wenn es regnet, bleibe ich zu Hause.",
        "verbs": ["regnet"],
        "clause_type": "wenn_clause",
        "difficulty": 1,
        "explanation": "In a 'wenn' clause, the verb goes to the end of that clause."
    },
    {
        "id": "a2_wenn_02",
        "text": "Ich bin glücklich, wenn die Sonne scheint.",
        "verbs": ["scheint"],
        "clause_type": "wenn_clause",
        "difficulty": 1,
        "explanation": "In a 'wenn' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_obwohl_01",
        "text": "Er geht zur Arbeit, obwohl er müde ist.",
        "verbs": ["ist"],
        "clause_type": "obwohl_clause",
        "difficulty": 1,
        "explanation": "In an 'obwohl' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_als_01",
        "text": "Als ich ein Kind war, spielte ich oft draußen.",
        "verbs": ["war"],
        "clause_type": "als_clause",
        "difficulty": 1,
        "explanation": "In an 'als' clause, the conjugated verb goes to the end of the subordinate clause."
    },
    {
        "id": "a2_ob_01",
        "text": "Ich weiß nicht, ob er heute kommt.",
        "verbs": ["kommt"],
        "clause_type": "ob_clause",
        "difficulty": 1,
        "explanation": "In an 'ob' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_dass_03",
        "text": "Er hofft, dass das Wetter morgen schön wird.",
        "verbs": ["wird"],
        "clause_type": "dass_clause",
        "difficulty": 1,
        "explanation": "In a 'dass' clause, the conjugated verb 'wird' goes to the end."
    },
    {
        "id": "a2_weil_03",
        "text": "Sie ist traurig, weil ihr Hund krank ist.",
        "verbs": ["ist"],
        "clause_type": "weil_clause",
        "difficulty": 1,
        "explanation": "In a 'weil' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_dass_04",
        "text": "Wir wissen, dass du sehr fleißig bist.",
        "verbs": ["bist"],
        "clause_type": "dass_clause",
        "difficulty": 1,
        "explanation": "In a 'dass' clause, the conjugated verb moves to the final position."
    },
    {
        "id": "a2_bevor_01",
        "text": "Ich esse Frühstück, bevor ich zur Arbeit gehe.",
        "verbs": ["gehe"],
        "clause_type": "bevor_clause",
        "difficulty": 1,
        "explanation": "In a 'bevor' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_damit_01",
        "text": "Er lernt viel, damit er die Prüfung besteht.",
        "verbs": ["besteht"],
        "clause_type": "damit_clause",
        "difficulty": 1,
        "explanation": "In a 'damit' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_waehrend_01",
        "text": "Während ich koche, hört mein Mann Musik.",
        "verbs": ["koche"],
        "clause_type": "waehrend_clause",
        "difficulty": 1,
        "explanation": "In a 'während' clause, the conjugated verb goes to the end."
    },

    # ──────────── DIFFICULTY 2 (B1): Compound verbs & separable verbs ────────────
    {
        "id": "b1_perfekt_01",
        "text": "Ich weiß, dass er gestern das Buch gelesen hat.",
        "verbs": ["gelesen", "hat"],
        "clause_type": "perfekt_in_nebensatz",
        "difficulty": 2,
        "explanation": "In a subordinate clause with Perfekt, the auxiliary 'hat' goes to the very end, after the past participle 'gelesen'."
    },
    {
        "id": "b1_perfekt_02",
        "text": "Sie erzählt, dass sie letzte Woche nach Paris geflogen ist.",
        "verbs": ["geflogen", "ist"],
        "clause_type": "perfekt_in_nebensatz",
        "difficulty": 2,
        "explanation": "In a subordinate clause with Perfekt, the auxiliary 'ist' goes to the very end, after the past participle."
    },
    {
        "id": "b1_modal_01",
        "text": "Er sagt, dass er morgen nicht arbeiten muss.",
        "verbs": ["arbeiten", "muss"],
        "clause_type": "modal_in_nebensatz",
        "difficulty": 2,
        "explanation": "In a subordinate clause with a modal verb, the modal 'muss' goes to the end, after the infinitive 'arbeiten'."
    },
    {
        "id": "b1_modal_02",
        "text": "Ich glaube, dass sie sehr gut Klavier spielen kann.",
        "verbs": ["spielen", "kann"],
        "clause_type": "modal_in_nebensatz",
        "difficulty": 2,
        "explanation": "In a subordinate clause with a modal, the modal 'kann' goes to the end, after the infinitive 'spielen'."
    },
    {
        "id": "b1_sep_01",
        "text": "Ich weiß, dass der Zug um acht Uhr ankommt.",
        "verbs": ["ankommt"],
        "clause_type": "separable_verb_nebensatz",
        "difficulty": 2,
        "explanation": "Separable verbs recombine in subordinate clauses: 'an' + 'kommt' = 'ankommt' at the end."
    },
    {
        "id": "b1_sep_02",
        "text": "Sie sagt, dass er jeden Morgen um sechs Uhr aufsteht.",
        "verbs": ["aufsteht"],
        "clause_type": "separable_verb_nebensatz",
        "difficulty": 2,
        "explanation": "Separable verbs recombine in subordinate clauses: 'auf' + 'steht' = 'aufsteht' at the end."
    },
    {
        "id": "b1_relativ_01",
        "text": "Das Buch, das ich gestern gekauft habe, ist sehr spannend.",
        "verbs": ["gekauft", "habe"],
        "clause_type": "relative_clause",
        "difficulty": 2,
        "explanation": "In a relative clause, verb goes to the end. With Perfekt, the auxiliary 'habe' follows the participle 'gekauft'."
    },
    {
        "id": "b1_relativ_02",
        "text": "Der Mann, der neben mir wohnt, ist sehr freundlich.",
        "verbs": ["wohnt"],
        "clause_type": "relative_clause",
        "difficulty": 2,
        "explanation": "In a relative clause, the conjugated verb goes to the end."
    },
    {
        "id": "b1_nachdem_01",
        "text": "Nachdem er gegessen hatte, ging er spazieren.",
        "verbs": ["gegessen", "hatte"],
        "clause_type": "nachdem_plusquamperfekt",
        "difficulty": 2,
        "explanation": "In a 'nachdem' clause with Plusquamperfekt, the auxiliary 'hatte' goes to the very end."
    },
    {
        "id": "b1_dass_modal_01",
        "text": "Sie glaubt, dass er das Problem lösen kann.",
        "verbs": ["lösen", "kann"],
        "clause_type": "modal_in_nebensatz",
        "difficulty": 2,
        "explanation": "Modal 'kann' goes to the end of the subordinate clause, after the infinitive 'lösen'."
    },
    {
        "id": "b1_weil_perfekt_01",
        "text": "Er ist müde, weil er die ganze Nacht gearbeitet hat.",
        "verbs": ["gearbeitet", "hat"],
        "clause_type": "perfekt_in_nebensatz",
        "difficulty": 2,
        "explanation": "In a 'weil' clause with Perfekt, the auxiliary 'hat' goes after the past participle at the end."
    },
    {
        "id": "b1_wenn_modal_01",
        "text": "Wenn du mitkommen willst, musst du dich beeilen.",
        "verbs": ["mitkommen", "willst"],
        "clause_type": "modal_in_nebensatz",
        "difficulty": 2,
        "explanation": "In the 'wenn' clause, the modal 'willst' goes to the end, after the infinitive 'mitkommen'."
    },
    {
        "id": "b1_sep_perfekt_01",
        "text": "Ich weiß, dass sie gestern sehr früh aufgestanden ist.",
        "verbs": ["aufgestanden", "ist"],
        "clause_type": "separable_perfekt_nebensatz",
        "difficulty": 2,
        "explanation": "Separable verb in Perfekt in subordinate clause: participle 'aufgestanden' + auxiliary 'ist' at the end."
    },
    {
        "id": "b1_ob_modal_01",
        "text": "Ich frage mich, ob er das wirklich machen will.",
        "verbs": ["machen", "will"],
        "clause_type": "modal_in_nebensatz",
        "difficulty": 2,
        "explanation": "In an 'ob' clause with modal, the modal 'will' goes to the end, after the infinitive."
    },
    {
        "id": "b1_relativ_03",
        "text": "Die Frau, die in dem Laden arbeitet, kennt meine Mutter.",
        "verbs": ["arbeitet"],
        "clause_type": "relative_clause",
        "difficulty": 2,
        "explanation": "In a relative clause, the conjugated verb goes to the end."
    },

    # ──────────── DIFFICULTY 3 (B2): Nested clauses & complex structures ────────────
    {
        "id": "b2_nested_01",
        "text": "Er sagt, dass er weiß, dass sie morgen kommt.",
        "verbs": ["weiß", "kommt"],
        "clause_type": "nested_dass",
        "difficulty": 3,
        "explanation": "Two nested 'dass' clauses: each verb goes to the end of its own clause. 'weiß' ends the first dass-clause, 'kommt' ends the inner dass-clause."
    },
    {
        "id": "b2_nested_02",
        "text": "Ich glaube, dass der Film, den wir gestern gesehen haben, sehr gut war.",
        "verbs": ["gesehen", "haben", "war"],
        "clause_type": "relative_in_dass",
        "difficulty": 3,
        "explanation": "A relative clause is embedded inside a dass-clause. 'gesehen haben' ends the relative clause, 'war' ends the dass-clause."
    },
    {
        "id": "b2_passiv_01",
        "text": "Sie sagt, dass das Haus nächstes Jahr renoviert werden soll.",
        "verbs": ["renoviert", "werden", "soll"],
        "clause_type": "passiv_modal_nebensatz",
        "difficulty": 3,
        "explanation": "Passive with modal in subordinate clause: participle 'renoviert' + 'werden' + modal 'soll' stacked at the end."
    },
    {
        "id": "b2_konjunktiv_01",
        "text": "Er tut so, als ob er nichts davon gewusst hätte.",
        "verbs": ["gewusst", "hätte"],
        "clause_type": "als_ob_konjunktiv",
        "difficulty": 3,
        "explanation": "In an 'als ob' clause with Konjunktiv II Perfekt, 'hätte' goes to the very end after the participle."
    },
    {
        "id": "b2_relativ_nested_01",
        "text": "Das ist der Lehrer, der weiß, dass seine Schüler fleißig arbeiten.",
        "verbs": ["weiß", "arbeiten"],
        "clause_type": "relative_with_dass",
        "difficulty": 3,
        "explanation": "A relative clause contains a dass-clause. 'weiß' ends the relative clause part, 'arbeiten' ends the dass-clause."
    },
    {
        "id": "b2_futur_neben_01",
        "text": "Sie hofft, dass er sie nächste Woche besuchen wird.",
        "verbs": ["besuchen", "wird"],
        "clause_type": "futur_in_nebensatz",
        "difficulty": 3,
        "explanation": "Futur I in a subordinate clause: infinitive 'besuchen' + 'wird' at the end."
    },
    {
        "id": "b2_obwohl_perfekt_01",
        "text": "Obwohl er den ganzen Tag hart gearbeitet hatte, ging er abends noch ins Fitnessstudio.",
        "verbs": ["gearbeitet", "hatte"],
        "clause_type": "obwohl_plusquamperfekt",
        "difficulty": 3,
        "explanation": "In the 'obwohl' clause with Plusquamperfekt, 'hatte' goes to the end after the participle."
    },
    {
        "id": "b2_wenn_nested_01",
        "text": "Wenn du wüsstest, was er gestern gemacht hat, wärst du überrascht.",
        "verbs": ["wüsstest", "gemacht", "hat"],
        "clause_type": "nested_wenn_was",
        "difficulty": 3,
        "explanation": "'wüsstest' ends the wenn-clause, 'gemacht hat' ends the embedded was-clause."
    },
    {
        "id": "b2_damit_modal_01",
        "text": "Er übt jeden Tag, damit er die Prüfung bestehen kann.",
        "verbs": ["bestehen", "kann"],
        "clause_type": "damit_modal",
        "difficulty": 3,
        "explanation": "In a 'damit' clause with modal, the modal 'kann' goes to the end after the infinitive."
    },
    {
        "id": "b2_seitdem_01",
        "text": "Seitdem er in München angekommen ist, hat er viele neue Freunde gefunden.",
        "verbs": ["angekommen", "ist"],
        "clause_type": "seitdem_perfekt",
        "difficulty": 3,
        "explanation": "In a 'seitdem' clause with Perfekt, 'ist' goes to the end after the participle 'angekommen'."
    },
    {
        "id": "b2_je_desto_01",
        "text": "Je mehr er Deutsch lernt, desto besser kann er die Grammatik verstehen.",
        "verbs": ["lernt"],
        "clause_type": "je_desto",
        "difficulty": 3,
        "explanation": "In the 'je' clause (subordinate), the verb goes to the end."
    },
    {
        "id": "b2_nachdem_nested_01",
        "text": "Nachdem sie erfahren hatte, dass er gekündigt hat, war sie schockiert.",
        "verbs": ["erfahren", "hatte", "gekündigt", "hat"],
        "clause_type": "nested_nachdem_dass",
        "difficulty": 3,
        "explanation": "Nested clauses: 'erfahren hatte' ends the nachdem-clause, 'gekündigt hat' ends the embedded dass-clause."
    },
    {
        "id": "b2_relativ_modal_01",
        "text": "Das Projekt, das bis Freitag abgeschlossen werden muss, ist sehr umfangreich.",
        "verbs": ["abgeschlossen", "werden", "muss"],
        "clause_type": "relative_passiv_modal",
        "difficulty": 3,
        "explanation": "Relative clause with passive modal: participle + 'werden' + modal 'muss' stacked at the end."
    },
    {
        "id": "b2_ohne_dass_01",
        "text": "Er hat das Haus verlassen, ohne dass jemand ihn gesehen hat.",
        "verbs": ["gesehen", "hat"],
        "clause_type": "ohne_dass_perfekt",
        "difficulty": 3,
        "explanation": "In an 'ohne dass' clause with Perfekt, the auxiliary goes to the end after the participle."
    },

    # ──────────── DIFFICULTY 4 (C1): Complex nesting & rare constructions ────────────
    {
        "id": "c1_triple_01",
        "text": "Er behauptet, dass er weiß, dass sie gesagt hat, dass sie kommen wird.",
        "verbs": ["weiß", "gesagt", "hat", "kommen", "wird"],
        "clause_type": "triple_nested_dass",
        "difficulty": 4,
        "explanation": "Three nested dass-clauses: each verb cluster goes to the end of its own clause."
    },
    {
        "id": "c1_double_inf_01",
        "text": "Ich weiß, dass er das Buch hat lesen wollen.",
        "verbs": ["hat", "lesen", "wollen"],
        "clause_type": "double_infinitive",
        "difficulty": 4,
        "explanation": "Double infinitive (Ersatzinfinitiv): when a modal is in Perfekt in a subordinate clause, 'hat' comes BEFORE the two infinitives. This is an exception to the normal verb-end rule."
    },
    {
        "id": "c1_double_inf_02",
        "text": "Sie erzählt, dass sie ihn hat singen hören.",
        "verbs": ["hat", "singen", "hören"],
        "clause_type": "double_infinitive",
        "difficulty": 4,
        "explanation": "Double infinitive with perception verb: 'hat' precedes the two infinitives in subordinate clause."
    },
    {
        "id": "c1_relativ_deep_01",
        "text": "Der Student, der das Buch, das der Professor empfohlen hatte, endlich gelesen hat, bestand die Prüfung.",
        "verbs": ["empfohlen", "hatte", "gelesen", "hat"],
        "clause_type": "deeply_nested_relative",
        "difficulty": 4,
        "explanation": "Deeply nested relative clauses: inner relative 'empfohlen hatte' and outer relative 'gelesen hat' each end their own clause."
    },
    {
        "id": "c1_passiv_perfekt_01",
        "text": "Sie berichtet, dass das Gebäude vor zwei Jahren renoviert worden ist.",
        "verbs": ["renoviert", "worden", "ist"],
        "clause_type": "passiv_perfekt_nebensatz",
        "difficulty": 4,
        "explanation": "Passive Perfekt in subordinate clause: participle 'renoviert' + 'worden' + 'ist' stacked at the end."
    },
    {
        "id": "c1_konj2_passiv_01",
        "text": "Er wünscht sich, dass er besser informiert worden wäre.",
        "verbs": ["informiert", "worden", "wäre"],
        "clause_type": "konjunktiv_passiv_perfekt",
        "difficulty": 4,
        "explanation": "Konjunktiv II passive Perfekt: participle + 'worden' + 'wäre' at the end of the dass-clause."
    },
    {
        "id": "c1_falls_nested_01",
        "text": "Falls er herausfindet, dass sie das Geheimnis, das er ihr anvertraut hatte, weitergegeben hat, wird er sehr enttäuscht sein.",
        "verbs": ["herausfindet", "anvertraut", "hatte", "weitergegeben", "hat"],
        "clause_type": "falls_nested_relative_dass",
        "difficulty": 4,
        "explanation": "Multiple levels: 'herausfindet' ends the falls-clause, inner relative 'anvertraut hatte', and dass-clause 'weitergegeben hat'."
    },
    {
        "id": "c1_obgleich_01",
        "text": "Obgleich er behauptet, dass er alles verstanden habe, zeigen seine Ergebnisse, dass er den Stoff nicht richtig begriffen hat.",
        "verbs": ["behauptet", "verstanden", "habe", "begriffen", "hat"],
        "clause_type": "complex_obgleich_dass",
        "difficulty": 4,
        "explanation": "Complex nesting: 'behauptet' in obgleich, 'verstanden habe' in its dass-clause, 'begriffen hat' in the second dass-clause."
    },
    {
        "id": "c1_indirekte_rede_01",
        "text": "Er sagt, er wisse, dass sie habe kommen wollen.",
        "verbs": ["wisse", "habe", "kommen", "wollen"],
        "clause_type": "indirekte_rede_double_inf",
        "difficulty": 4,
        "explanation": "Indirect speech (Konjunktiv I) with double infinitive: 'wisse' ends the indirect clause, 'habe kommen wollen' in the dass-clause."
    },
    {
        "id": "c1_anstatt_dass_01",
        "text": "Anstatt dass er sich auf die Prüfung vorbereitet hätte, hat er den ganzen Tag ferngesehen.",
        "verbs": ["vorbereitet", "hätte"],
        "clause_type": "anstatt_dass_konjunktiv",
        "difficulty": 4,
        "explanation": "In 'anstatt dass' with Konjunktiv II Perfekt, 'hätte' goes to the end after the participle."
    },
    {
        "id": "c1_kaum_dass_01",
        "text": "Kaum dass er angefangen hatte zu sprechen, wurde er von seinem Chef unterbrochen.",
        "verbs": ["angefangen", "hatte"],
        "clause_type": "kaum_dass_plusquam",
        "difficulty": 4,
        "explanation": "In 'kaum dass' with Plusquamperfekt, 'hatte' goes to the end after the participle."
    },
    {
        "id": "c1_zumal_01",
        "text": "Er sollte mehr lernen, zumal er weiß, dass die Prüfung sehr schwer sein wird.",
        "verbs": ["weiß", "sein", "wird"],
        "clause_type": "zumal_nested_dass",
        "difficulty": 4,
        "explanation": "'weiß' ends the zumal-clause, 'sein wird' (Futur I) ends the nested dass-clause."
    },

    # ──────────── ADDITIONAL A2 SENTENCES ────────────
    {
        "id": "a2_dass_05",
        "text": "Meine Mutter sagt, dass ich mehr Gemüse essen soll.",
        "verbs": ["essen", "soll"],
        "clause_type": "dass_modal",
        "difficulty": 1,
        "explanation": "In a 'dass' clause with modal, the modal goes to the end after the infinitive."
    },
    {
        "id": "a2_weil_04",
        "text": "Das Kind weint, weil es seinen Teddy verloren hat.",
        "verbs": ["verloren", "hat"],
        "clause_type": "weil_perfekt",
        "difficulty": 1,
        "explanation": "In a 'weil' clause with Perfekt, the auxiliary 'hat' goes to the end after the participle."
    },
    {
        "id": "a2_wenn_03",
        "text": "Wenn du Hunger hast, kannst du etwas essen.",
        "verbs": ["hast"],
        "clause_type": "wenn_clause",
        "difficulty": 1,
        "explanation": "In the 'wenn' clause, the conjugated verb 'hast' goes to the end."
    },
    {
        "id": "a2_dass_06",
        "text": "Ich denke, dass er ein guter Lehrer ist.",
        "verbs": ["ist"],
        "clause_type": "dass_clause",
        "difficulty": 1,
        "explanation": "In a 'dass' clause, the conjugated verb goes to the end."
    },
    {
        "id": "a2_als_02",
        "text": "Als wir in Urlaub waren, hatten wir viel Spaß.",
        "verbs": ["waren"],
        "clause_type": "als_clause",
        "difficulty": 1,
        "explanation": "In an 'als' clause, the conjugated verb goes to the end."
    },

    # ──────────── ADDITIONAL B1 SENTENCES ────────────
    {
        "id": "b1_relativ_04",
        "text": "Die Stadt, in der ich geboren wurde, liegt im Süden.",
        "verbs": ["geboren", "wurde"],
        "clause_type": "relative_passiv",
        "difficulty": 2,
        "explanation": "In a relative clause with passive, 'wurde' goes to the end after the participle."
    },
    {
        "id": "b1_obwohl_modal_01",
        "text": "Obwohl er nicht gut singen kann, tritt er auf der Bühne auf.",
        "verbs": ["singen", "kann"],
        "clause_type": "obwohl_modal",
        "difficulty": 2,
        "explanation": "In the 'obwohl' clause, modal 'kann' goes to the end after the infinitive."
    },
    {
        "id": "b1_bevor_perfekt_01",
        "text": "Bevor er nach Deutschland gezogen ist, hat er zwei Jahre Deutsch gelernt.",
        "verbs": ["gezogen", "ist"],
        "clause_type": "bevor_perfekt",
        "difficulty": 2,
        "explanation": "In the 'bevor' clause with Perfekt, 'ist' goes to the end after the participle."
    },
    {
        "id": "b1_waehrend_modal_01",
        "text": "Während sie auf den Bus warten musste, hat sie ein Buch gelesen.",
        "verbs": ["warten", "musste"],
        "clause_type": "waehrend_modal",
        "difficulty": 2,
        "explanation": "In the 'während' clause, modal 'musste' goes to the end after the infinitive."
    },
    {
        "id": "b1_dass_futur_01",
        "text": "Er sagt, dass er nächstes Jahr nach Japan reisen wird.",
        "verbs": ["reisen", "wird"],
        "clause_type": "dass_futur",
        "difficulty": 2,
        "explanation": "In a dass-clause with Futur I, 'wird' goes to the end after the infinitive."
    },

    # ──────────── ADDITIONAL B2 SENTENCES ────────────
    {
        "id": "b2_indem_01",
        "text": "Man kann viel lernen, indem man regelmäßig Bücher liest.",
        "verbs": ["liest"],
        "clause_type": "indem_clause",
        "difficulty": 3,
        "explanation": "In an 'indem' clause, the conjugated verb goes to the end."
    },
    {
        "id": "b2_sobald_01",
        "text": "Sobald er die Nachricht erhalten hat, wird er uns informieren.",
        "verbs": ["erhalten", "hat"],
        "clause_type": "sobald_perfekt",
        "difficulty": 3,
        "explanation": "In a 'sobald' clause with Perfekt, 'hat' goes to the end after the participle."
    },
    {
        "id": "b2_statt_dass_01",
        "text": "Statt dass er uns hilft, sitzt er den ganzen Tag vor dem Fernseher.",
        "verbs": ["hilft"],
        "clause_type": "statt_dass",
        "difficulty": 3,
        "explanation": "In a 'statt dass' clause, the conjugated verb goes to the end."
    },
    {
        "id": "b2_wer_01",
        "text": "Wer die Regeln nicht kennt, kann das Spiel nicht gewinnen.",
        "verbs": ["kennt"],
        "clause_type": "wer_clause",
        "difficulty": 3,
        "explanation": "In a 'wer' clause (free relative), the verb goes to the end."
    },
    {
        "id": "b2_es_sei_denn_01",
        "text": "Ich gehe nicht raus, es sei denn, dass das Wetter besser wird.",
        "verbs": ["wird"],
        "clause_type": "es_sei_denn_dass",
        "difficulty": 3,
        "explanation": "In 'es sei denn, dass' clause, the verb goes to the end."
    },

    # ──────────── ADDITIONAL C1 SENTENCES ────────────
    {
        "id": "c1_weshalb_01",
        "text": "Er versteht nicht, weshalb sie, obwohl sie die Wahrheit gekannt hat, nichts gesagt hat.",
        "verbs": ["gekannt", "hat", "gesagt", "hat"],
        "clause_type": "nested_weshalb_obwohl",
        "difficulty": 4,
        "explanation": "Nested clauses: 'gekannt hat' ends the obwohl-clause, 'gesagt hat' ends the weshalb-clause."
    },
    {
        "id": "c1_geschweige_01",
        "text": "Er kann nicht einmal einen einfachen Satz bilden, geschweige denn, dass er komplexe Texte verstehen könnte.",
        "verbs": ["verstehen", "könnte"],
        "clause_type": "geschweige_denn_dass",
        "difficulty": 4,
        "explanation": "In 'geschweige denn, dass' with Konjunktiv, 'könnte' goes to the end after the infinitive."
    },
    {
        "id": "c1_wie_auch_immer_01",
        "text": "Wie auch immer er das Problem, das seit Wochen ungelöst geblieben ist, zu lösen versucht, es funktioniert nicht.",
        "verbs": ["geblieben", "ist", "versucht"],
        "clause_type": "complex_embedded_relative",
        "difficulty": 4,
        "explanation": "Embedded relative 'geblieben ist' inside a wie-clause, with 'versucht' ending the main subordinate structure."
    },
    {
        "id": "c1_vorausgesetzt_01",
        "text": "Vorausgesetzt, dass er die Arbeit, die bis Freitag eingereicht werden muss, rechtzeitig abgeschlossen hat, kann er am Wochenende frei nehmen.",
        "verbs": ["eingereicht", "werden", "muss", "abgeschlossen", "hat"],
        "clause_type": "vorausgesetzt_nested_relative",
        "difficulty": 4,
        "explanation": "Nested structures: relative clause 'eingereicht werden muss' and main dass-clause 'abgeschlossen hat'."
    },
    {
        "id": "c1_sofern_01",
        "text": "Sofern er nachweisen kann, dass er die Kurse erfolgreich abgeschlossen hat, wird sein Antrag genehmigt werden.",
        "verbs": ["nachweisen", "kann", "abgeschlossen", "hat"],
        "clause_type": "sofern_nested_dass",
        "difficulty": 4,
        "explanation": "'nachweisen kann' ends the sofern-clause, 'abgeschlossen hat' ends the nested dass-clause."
    },
]


def _compute_positions(text, verbs):
    """Compute word-level positions of verbs in the sentence."""
    words = text.split()
    positions = []
    verb_idx = 0
    used_positions = set()
    for verb in verbs:
        for i, word in enumerate(words):
            # Strip punctuation for matching
            clean = word.strip(".,;:!?\"'()[]{}–—")
            if clean == verb and i not in used_positions:
                positions.append(i)
                used_positions.add(i)
                break
    return positions


def _create_display_text(text, verbs):
    """Create display text with verb slots marked as ___."""
    words = text.split()
    display_words = list(words)
    used_positions = set()
    for verb in verbs:
        for i, word in enumerate(words):
            clean = word.strip(".,;:!?\"'()[]{}–—")
            if clean == verb and i not in used_positions:
                # Preserve punctuation
                suffix = ""
                for ch in reversed(word):
                    if ch in ".,;:!?\"'()[]{}–—":
                        suffix = ch + suffix
                    else:
                        break
                display_words[i] = "___" + suffix
                used_positions.add(i)
                break
    return " ".join(display_words)


def prepare_exercise(template):
    """Prepare a template into an exercise dict ready for the frontend.

    Full-sentence mode: ALL words become slots and chips.
    The user must reconstruct the entire sentence.
    """
    text = template["text"]
    verbs = template["verbs"]
    verb_positions = _compute_positions(text, verbs)

    words = text.split()

    # Build all_slots: every word is a slot
    all_slots = []
    for i, w in enumerate(words):
        clean = w.strip(".,;:!?\"'()[]{}–—")
        suffix = ""
        for ch in reversed(w):
            if ch in ".,;:!?\"'()[]{}–—":
                suffix = ch + suffix
            else:
                break
        all_slots.append({
            "index": i,
            "correct_word": clean,
            "suffix": suffix,
            "is_verb": i in verb_positions
        })

    # Build verb_slots for error analysis (backward compat with error_analyzer)
    verb_slots = []
    for s in all_slots:
        if s["is_verb"]:
            verb_slots.append({
                "index": s["index"],
                "correct_verb": s["correct_word"],
                "suffix": s["suffix"]
            })

    # Shuffled words for the tray (clean, no punctuation)
    shuffled_words = [s["correct_word"] for s in all_slots]
    random.shuffle(shuffled_words)

    return {
        "template_id": template["id"],
        "full_text": text,
        "words": words,
        "all_slots": all_slots,
        "verb_slots": verb_slots,
        "verb_positions": verb_positions,
        "shuffled_words": shuffled_words,
        "clause_type": template["clause_type"],
        "difficulty": template["difficulty"],
        "explanation": template["explanation"],
        # Keep legacy fields for error analyzer
        "slots": verb_slots,
        "verbs": verbs,
        "positions": verb_positions
    }


def get_exercise_by_difficulty(difficulty=None, exclude_ids=None):
    """Get a random exercise, optionally filtered by difficulty."""
    pool = SENTENCE_BANK
    if difficulty is not None:
        pool = [s for s in pool if s["difficulty"] == difficulty]
    if exclude_ids:
        pool = [s for s in pool if s["id"] not in exclude_ids]
    if not pool:
        return None
    template = random.choice(pool)
    return prepare_exercise(template)


def get_template_by_id(template_id):
    """Get a specific template by ID."""
    for t in SENTENCE_BANK:
        if t["id"] == template_id:
            return t
    return None


def get_all_template_ids():
    return [t["id"] for t in SENTENCE_BANK]


def get_daily_sentence():
    """Pick a sentence suitable for the daily iMessage motivation."""
    # Prefer medium difficulty for daily messages
    pool = [s for s in SENTENCE_BANK if s["difficulty"] in (2, 3)]
    if not pool:
        pool = SENTENCE_BANK
    template = random.choice(pool)
    return template


def count_by_difficulty():
    counts = {}
    for t in SENTENCE_BANK:
        d = t["difficulty"]
        counts[d] = counts.get(d, 0) + 1
    return counts
