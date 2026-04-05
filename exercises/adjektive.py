"""
Adjective Declension (Adjektivdeklination) — Exercise Bank.

Tests adjective endings after bestimmter/unbestimmter Artikel, possessives,
without article (starke Deklination), Genitiv, and multiple adjectives.
Exercise type: gap_fill
"""

ADJEKTIVE_BANK = [
    {'id': 'gen_adj_001', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Ich sehe den alt{gap_1} Mann im Park.', 'gaps': [{'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ich sehe den alten Mann im Park.'}, 'grammar_rule': 'After bestimmter Artikel, Akkusativ maskulin -> -en', 'grammar_tip': 'Der-Wörter im Akkusativ maskulin bekommen immer -en.'},
    {'id': 'gen_adj_002', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Die nett{gap_1} Nachbarin hilft mir oft.', 'gaps': [{'position': 'gap_1', 'context': 'nett__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'feminin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Die nette Nachbarin hilft mir oft.'}, 'grammar_rule': 'After bestimmter Artikel, Nominativ feminin -> -e', 'grammar_tip': 'Die + Nominativ feminin = -e.'},
    {'id': 'gen_adj_003', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Das klein{gap_1} Kind spielt im Garten.', 'gaps': [{'position': 'gap_1', 'context': 'klein__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'neutrum', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Das kleine Kind spielt im Garten.'}, 'grammar_rule': 'After bestimmter Artikel, Nominativ neutrum -> -e', 'grammar_tip': 'Das + Nominativ = -e.'},
    {'id': 'gen_adj_004', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Ich kaufe die frisch{gap_1} Erdbeeren.', 'gaps': [{'position': 'gap_1', 'context': 'frisch__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'plural', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ich kaufe die frischen Erdbeeren.'}, 'grammar_rule': 'After bestimmter Artikel, Akkusativ plural -> -en', 'grammar_tip': 'Im Plural mit der-Wörtern fast immer -en.'},
    {'id': 'gen_adj_005', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Wir besuchen das neu{gap_1} Museum.', 'gaps': [{'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'neutrum', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Wir besuchen das neue Museum.'}, 'grammar_rule': 'After bestimmter Artikel, Akkusativ neutrum -> -e', 'grammar_tip': 'Das bleibt -e im Nominativ und Akkusativ.'},
    {'id': 'gen_adj_006', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Der jung{gap_1} Student lernt viel.', 'gaps': [{'position': 'gap_1', 'context': 'jung__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Der junge Student lernt viel.'}, 'grammar_rule': 'After bestimmter Artikel, Nominativ maskulin -> -e', 'grammar_tip': 'Der im Nominativ braucht -e.'},
    {'id': 'gen_adj_007', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt', 'data': {'sentence_template': 'Ich nehme die groß{gap_1} Tasche mit.', 'gaps': [{'position': 'gap_1', 'context': 'groß__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'feminin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ich nehme die große Tasche mit.'}, 'grammar_rule': 'After bestimmter Artikel, Akkusativ feminin -> -e', 'grammar_tip': 'Die bleibt -e in Nom und Akk.'},
    {'id': 'gen_adj_008', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt', 'data': {'sentence_template': 'Ein alt{gap_1} Baum steht vor dem Haus.', 'gaps': [{'position': 'gap_1', 'context': 'alt__', 'answer': 'er', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ein alter Baum steht vor dem Haus.'}, 'grammar_rule': 'After ein-Wort, Nominativ maskulin -> -er', 'grammar_tip': 'Fehlt die Endung am Artikel, zeigt sie das Adjektiv.'},
    {'id': 'gen_adj_009', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt', 'data': {'sentence_template': 'Ich trinke ein kalt{gap_1} Wasser.', 'gaps': [{'position': 'gap_1', 'context': 'kalt__', 'answer': 'es', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'neutrum', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ich trinke ein kaltes Wasser.'}, 'grammar_rule': 'After ein-Wort, Akkusativ neutrum -> -es', 'grammar_tip': 'Ein (ohne Endung) braucht starkes -es.'},
    {'id': 'gen_adj_010', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv', 'data': {'sentence_template': 'Meine neu{gap_1} Wohnung ist sehr hell.', 'gaps': [{'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'possessiv', 'case': 'Nominativ', 'gender': 'feminin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Meine neue Wohnung ist sehr hell.'}, 'grammar_rule': 'After possessiv, Nominativ feminin -> -e', 'grammar_tip': 'Meine funktioniert wie eine.'},
    {'id': 'gen_adj_011', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv', 'data': {'sentence_template': 'Mit meinem neu{gap_1} Fahrrad fahre ich zur Arbeit.', 'gaps': [{'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Dativ', 'gender': 'neutrum', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Mit meinem neuen Fahrrad fahre ich zur Arbeit.'}, 'grammar_rule': 'After possessiv, Dativ -> -en', 'grammar_tip': 'Im Dativ fast immer -en.'},
    {'id': 'gen_adj_012', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt', 'data': {'sentence_template': 'Er wohnt in einer schön{gap_1} Stadt.', 'gaps': [{'position': 'gap_1', 'context': 'schön__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Dativ', 'gender': 'feminin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Er wohnt in einer schönen Stadt.'}, 'grammar_rule': 'After ein-Wort, Dativ feminin -> -en', 'grammar_tip': 'Dativ = -en.'},
    {'id': 'gen_adj_013', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt', 'data': {'sentence_template': 'Sie hat einen interessant{gap_1} Job gefunden.', 'gaps': [{'position': 'gap_1', 'context': 'interessant__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Sie hat einen interessanten Job gefunden.'}, 'grammar_rule': 'After ein-Wort, Akkusativ maskulin -> -en', 'grammar_tip': 'Einen + maskulin = -en.'},
    {'id': 'gen_adj_014', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv', 'data': {'sentence_template': 'Ich danke meinem hilfsbereit{gap_1} Kollegen.', 'gaps': [{'position': 'gap_1', 'context': 'hilfsbereit__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Dativ', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Ich danke meinem hilfsbereiten Kollegen.'}, 'grammar_rule': 'After possessiv, Dativ maskulin -> -en', 'grammar_tip': 'Dativ maskulin braucht -en.'},
    {'id': 'gen_adj_015', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel', 'data': {'sentence_template': 'Frisch{gap_1} Brot schmeckt am besten am Morgen.', 'gaps': [{'position': 'gap_1', 'context': 'Frisch__', 'answer': 'es', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'neutrum', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Frisches Brot schmeckt am besten am Morgen.'}, 'grammar_rule': 'Without article, Nominativ neutrum -> -es', 'grammar_tip': 'Ohne Artikel übernimmt das Adjektiv die starke Endung.'},
    {'id': 'gen_adj_016', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel', 'data': {'sentence_template': 'Mit gut{gap_1} Freunden reist man gern.', 'gaps': [{'position': 'gap_1', 'context': 'gut__', 'answer': 'en', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'plural', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Mit guten Freunden reist man gern.'}, 'grammar_rule': 'Without article, Dativ plural -> -en', 'grammar_tip': 'Dativ Plural immer -en.'},
    {'id': 'gen_adj_017', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_genitiv', 'data': {'sentence_template': 'Wegen stark{gap_1} Regens fiel das Konzert aus.', 'gaps': [{'position': 'gap_1', 'context': 'stark__', 'answer': 'en', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'maskulin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Wegen starken Regens fiel das Konzert aus.'}, 'grammar_rule': 'Without article, Genitiv maskulin -> -en', 'grammar_tip': 'Genitiv maskulin stark = -en.'},
    {'id': 'gen_adj_018', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_multiple', 'data': {'sentence_template': 'Alt{gap_1}, historisch{gap_2} Gebäude prägen das Stadtbild.', 'gaps': [{'position': 'gap_1', 'context': 'Alt__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural', 'options': ['e', 'en', 'er', 'es', 'em']}, {'position': 'gap_2', 'context': 'historisch__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Alte, historische Gebäude prägen das Stadtbild.'}, 'grammar_rule': 'Without article, Nominativ plural -> -e', 'grammar_tip': 'Mehrere Adjektive bekommen die gleiche starke Endung.'},
    {'id': 'gen_adj_019', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel', 'data': {'sentence_template': 'Kalt{gap_1} Winter können sehr hart sein.', 'gaps': [{'position': 'gap_1', 'context': 'Kalt__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Kalte Winter können sehr hart sein.'}, 'grammar_rule': 'Without article, Nominativ plural -> -e', 'grammar_tip': 'Ohne Artikel zeigt das Adjektiv den Kasus.'},
    {'id': 'gen_adj_020', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_genitiv', 'data': {'sentence_template': 'Trotz groß{gap_1} Hitze gingen wir spazieren.', 'gaps': [{'position': 'gap_1', 'context': 'groß__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'feminin', 'options': ['e', 'en', 'er', 'es', 'em']}], 'full_correct': 'Trotz großer Hitze gingen wir spazieren.'}, 'grammar_rule': 'Without article, Genitiv feminin -> -er', 'grammar_tip': 'Genitiv feminin stark = -er.'},
]

ADJEKTIVE_ENGLISH = {
    "gen_adj_001": "I see the old man in the park.",
    "gen_adj_002": "The nice neighbour helps me often.",
    "gen_adj_003": "The small child is playing in the garden.",
    "gen_adj_004": "I buy the fresh strawberries.",
    "gen_adj_005": "We visit the new museum.",
    "gen_adj_006": "The young student studies a lot.",
    "gen_adj_007": "I take the big bag with me.",
    "gen_adj_008": "An old tree stands in front of the house.",
    "gen_adj_009": "I drink some cold water.",
    "gen_adj_010": "My new apartment is very bright.",
    "gen_adj_011": "With my new bike, I ride to work.",
    "gen_adj_012": "He lives in a beautiful city.",
    "gen_adj_013": "She found an interesting job.",
    "gen_adj_014": "I thank my helpful colleague.",
    "gen_adj_015": "Fresh bread tastes best in the morning.",
    "gen_adj_016": "People like to travel with good friends.",
    "gen_adj_017": "Because of heavy rain, the concert was cancelled.",
    "gen_adj_018": "Old, historic buildings shape the cityscape.",
    "gen_adj_019": "Cold winters can be very harsh.",
    "gen_adj_020": "Despite great heat, we went for a walk.",
}

for ex in ADJEKTIVE_BANK:
    ex.setdefault("data", {})
    ex["data"]["english"] = ADJEKTIVE_ENGLISH.get(ex["id"], "")

ADJEKTIVE_BANK += [
    # ---------------------------
    # LEVEL 1 — bestimmter Artikel (weak declension)
    # ---------------------------
    {'id': 'gen_adj_021', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Ich helfe dem krank{gap_1} Mann.', 'gaps': [
         {'position': 'gap_1', 'context': 'krank__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich helfe dem kranken Mann.', 'english': 'I help the sick man.'},
     'grammar_rule': 'After bestimmter Artikel, Dativ maskulin -> -en', 'grammar_tip': 'Im Dativ mit der-Wörtern fast immer -en.'},

    {'id': 'gen_adj_022', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Wir danken der freundlich{gap_1} Verkäuferin.', 'gaps': [
         {'position': 'gap_1', 'context': 'freundlich__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Wir danken der freundlichen Verkäuferin.', 'english': 'We thank the friendly saleswoman.'},
     'grammar_rule': 'After bestimmter Artikel, Dativ feminin -> -en', 'grammar_tip': 'Dativ = -en (auch bei der).'},

    {'id': 'gen_adj_023', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Ich spiele mit dem groß{gap_1} Hund.', 'gaps': [
         {'position': 'gap_1', 'context': 'groß__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich spiele mit dem großen Hund.', 'english': 'I play with the big dog.'},
     'grammar_rule': 'After bestimmter Artikel, Dativ maskulin -> -en', 'grammar_tip': 'Mit + Dativ: meistens -en.'},

    {'id': 'gen_adj_024', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Sie wohnt im alt{gap_1} Haus.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Sie wohnt im alten Haus.', 'english': 'She lives in the old house.'},
     'grammar_rule': 'After bestimmter Artikel, Dativ neutrum -> -en', 'grammar_tip': 'Im (= in dem) + Dativ: -en.'},

    {'id': 'gen_adj_025', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Ich gieße die klein{gap_1} Pflanzen.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich gieße die kleinen Pflanzen.', 'english': 'I water the small plants.'},
     'grammar_rule': 'After bestimmter Artikel, Akkusativ plural -> -en', 'grammar_tip': 'Plural mit der-Wörtern: fast immer -en.'},

    {'id': 'gen_adj_026', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Der neu{gap_1} Film ist spannend.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Der neue Film ist spannend.', 'english': 'The new film is exciting.'},
     'grammar_rule': 'After bestimmter Artikel, Nominativ maskulin -> -e', 'grammar_tip': 'Der + Nom maskulin = -e.'},

    {'id': 'gen_adj_027', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Wir mögen das lecker{gap_1} Essen.', 'gaps': [
         {'position': 'gap_1', 'context': 'lecker__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Wir mögen das leckere Essen.', 'english': 'We like the tasty food.'},
     'grammar_rule': 'After bestimmter Artikel, Akkusativ neutrum -> -e', 'grammar_tip': 'Das bleibt -e in Nom und Akk.'},

    {'id': 'gen_adj_028', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Die klein{gap_1} Katze schläft.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Die kleine Katze schläft.', 'english': 'The small cat is sleeping.'},
     'grammar_rule': 'After bestimmter Artikel, Nominativ feminin -> -e', 'grammar_tip': 'Die + Nom feminin = -e.'},

    {'id': 'gen_adj_029', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Ich repariere den kaputt{gap_1} Computer.', 'gaps': [
         {'position': 'gap_1', 'context': 'kaputt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich repariere den kaputten Computer.', 'english': 'I repair the broken computer.'},
     'grammar_rule': 'After bestimmter Artikel, Akkusativ maskulin -> -en', 'grammar_tip': 'Akk maskulin mit den = -en.'},

    {'id': 'gen_adj_030', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'adj_bestimmt',
     'data': {'sentence_template': 'Wir sitzen bei dem lang{gap_1} Tisch.', 'gaps': [
         {'position': 'gap_1', 'context': 'lang__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Wir sitzen bei dem langen Tisch.', 'english': 'We sit at the long table.'},
     'grammar_rule': 'After bestimmter Artikel, Dativ maskulin -> -en', 'grammar_tip': 'Bei + Dativ: -en.'},

    # ---------------------------
    # LEVEL 2 — ein-Wort / Possessiv (mixed declension)
    # ---------------------------
    {'id': 'gen_adj_031', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Ein klein{gap_1} Problem ist nicht schlimm.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'es', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ein kleines Problem ist nicht schlimm.', 'english': 'A small problem is not bad.'},
     'grammar_rule': 'After ein-Wort, Nominativ neutrum -> -es', 'grammar_tip': 'Ein (ohne Endung) braucht starkes -es.'},

    {'id': 'gen_adj_032', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Ich kaufe eine teuer{gap_1} Jacke.', 'gaps': [
         {'position': 'gap_1', 'context': 'teuer__', 'answer': 'e', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich kaufe eine teure Jacke.', 'english': 'I buy an expensive jacket.'},
     'grammar_rule': 'After ein-Wort, Akkusativ feminin -> -e', 'grammar_tip': 'Eine hat schon die Endung, daher meist -e.'},

    {'id': 'gen_adj_033', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Kein gut{gap_1} Plan funktioniert ohne Zeit.', 'gaps': [
         {'position': 'gap_1', 'context': 'gut__', 'answer': 'er', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Kein guter Plan funktioniert ohne Zeit.', 'english': 'No good plan works without time.'},
     'grammar_rule': 'After kein/ein, Nominativ maskulin -> -er', 'grammar_tip': 'Fehlt die Endung am Artikel, zeigt sie das Adjektiv.'},

    {'id': 'gen_adj_034', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Ich habe kein neu{gap_1} Auto.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'es', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich habe kein neues Auto.', 'english': 'I don’t have a new car.'},
     'grammar_rule': 'After kein/ein, Akkusativ neutrum -> -es', 'grammar_tip': 'Kein (ohne Endung) → starkes -es.'},

    {'id': 'gen_adj_035', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv',
     'data': {'sentence_template': 'Meine bequem{gap_1} Schuhe sind teuer.', 'gaps': [
         {'position': 'gap_1', 'context': 'bequem__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Meine bequemen Schuhe sind teuer.', 'english': 'My comfortable shoes are expensive.'},
     'grammar_rule': 'After possessiv, Nominativ plural -> -en', 'grammar_tip': 'Plural nach Possessiv: meistens -en.'},

    {'id': 'gen_adj_036', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Ich spreche mit einer freundlich{gap_1} Kollegin.', 'gaps': [
         {'position': 'gap_1', 'context': 'freundlich__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich spreche mit einer freundlichen Kollegin.', 'english': 'I talk with a friendly colleague.'},
     'grammar_rule': 'After ein-Wort, Dativ feminin -> -en', 'grammar_tip': 'Dativ = -en.'},

    {'id': 'gen_adj_037', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv',
     'data': {'sentence_template': 'Mit meinen alt{gap_1} Freunden lache ich viel.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Dativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Mit meinen alten Freunden lache ich viel.', 'english': 'I laugh a lot with my old friends.'},
     'grammar_rule': 'After possessiv, Dativ plural -> -en', 'grammar_tip': 'Dativ Plural fast immer -en.'},

    {'id': 'gen_adj_038', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_unbestimmt',
     'data': {'sentence_template': 'Wegen eines wichtig{gap_1} Termins komme ich später.', 'gaps': [
         {'position': 'gap_1', 'context': 'wichtig__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Genitiv', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Wegen eines wichtigen Termins komme ich später.', 'english': 'Because of an important appointment, I will come later.'},
     'grammar_rule': 'After ein-Wort, Genitiv maskulin -> -en', 'grammar_tip': 'Genitiv nach eines: meist -en (schwach).'},

    {'id': 'gen_adj_039', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv',
     'data': {'sentence_template': 'Ihre schön{gap_1} Stimme ist sehr klar.', 'gaps': [
         {'position': 'gap_1', 'context': 'schön__', 'answer': 'e', 'article_type': 'possessiv', 'case': 'Nominativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ihre schöne Stimme ist sehr klar.', 'english': 'Her beautiful voice is very clear.'},
     'grammar_rule': 'After possessiv, Nominativ feminin -> -e', 'grammar_tip': 'Ihre funktioniert wie eine.'},

    {'id': 'gen_adj_040', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'adj_possessiv',
     'data': {'sentence_template': 'Ich sehe meinen neu{gap_1} Chef heute.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Akkusativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich sehe meinen neuen Chef heute.', 'english': 'I see my new boss today.'},
     'grammar_rule': 'After possessiv, Akkusativ maskulin -> -en', 'grammar_tip': 'Meinen + Akk maskulin = -en.'},

    # ---------------------------
    # LEVEL 3 — ohne Artikel (strong declension)
    # ---------------------------
    {'id': 'gen_adj_041', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel',
     'data': {'sentence_template': 'Alt{gap_1} Wein schmeckt oft besser.', 'gaps': [
         {'position': 'gap_1', 'context': 'Alt__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Alter Wein schmeckt oft besser.', 'english': 'Old wine often tastes better.'},
     'grammar_rule': 'Without article, Nominativ maskulin -> -er', 'grammar_tip': 'Ohne Artikel zeigt das Adjektiv den Kasus: Nom mask = -er.'},

    {'id': 'gen_adj_042', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel',
     'data': {'sentence_template': 'Ich kaufe frisch{gap_1} Gemüse.', 'gaps': [
         {'position': 'gap_1', 'context': 'frisch__', 'answer': 'es', 'article_type': 'ohne', 'case': 'Akkusativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich kaufe frisches Gemüse.', 'english': 'I buy fresh vegetables.'},
     'grammar_rule': 'Without article, Akkusativ neutrum -> -es', 'grammar_tip': 'Akk neutrum stark = -es.'},

    {'id': 'gen_adj_043', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_dativ_stark',
     'data': {'sentence_template': 'Mit kalt{gap_1} Kaffee kann ich nicht schlafen.', 'gaps': [
         {'position': 'gap_1', 'context': 'kalt__', 'answer': 'em', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Mit kaltem Kaffee kann ich nicht schlafen.', 'english': 'I can’t sleep with cold coffee.'},
     'grammar_rule': 'Without article, Dativ maskulin -> -em', 'grammar_tip': 'Dativ mask/neut stark = -em.'},

    {'id': 'gen_adj_044', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_dativ_stark',
     'data': {'sentence_template': 'Aus groß{gap_1} Angst sagte sie nichts.', 'gaps': [
         {'position': 'gap_1', 'context': 'groß__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Aus großer Angst sagte sie nichts.', 'english': 'Out of great fear, she said nothing.'},
     'grammar_rule': 'Without article, Dativ feminin -> -er', 'grammar_tip': 'Dativ feminin stark = -er.'},

    {'id': 'gen_adj_045', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_genitiv',
     'data': {'sentence_template': 'Wegen neu{gap_1} Projekts arbeite ich länger.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Wegen neuen Projekts arbeite ich länger.', 'english': 'Because of a new project, I work longer.'},
     'grammar_rule': 'Without article, Genitiv neutrum -> -en', 'grammar_tip': 'Genitiv mask/neut stark = -en.'},

    {'id': 'gen_adj_046', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_genitiv',
     'data': {'sentence_template': 'Dank schnell{gap_1} Hilfe war alles leichter.', 'gaps': [
         {'position': 'gap_1', 'context': 'schnell__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'feminin',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Dank schneller Hilfe war alles leichter.', 'english': 'Thanks to quick help, everything was easier.'},
     'grammar_rule': 'Without article, Genitiv feminin -> -er', 'grammar_tip': 'Genitiv feminin stark = -er.'},

    {'id': 'gen_adj_047', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_ohne_artikel',
     'data': {'sentence_template': 'Ich erinnere mich an schön{gap_1} Tage.', 'gaps': [
         {'position': 'gap_1', 'context': 'schön__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Akkusativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Ich erinnere mich an schöne Tage.', 'english': 'I remember beautiful days.'},
     'grammar_rule': 'Without article, Akkusativ plural -> -e', 'grammar_tip': 'Ohne Artikel: Akk Plural stark = -e.'},

    {'id': 'gen_adj_048', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_dativ_stark',
     'data': {'sentence_template': 'Bei gut{gap_1} Wetter gehen wir schwimmen.', 'gaps': [
         {'position': 'gap_1', 'context': 'gut__', 'answer': 'em', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'neutrum',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Bei gutem Wetter gehen wir schwimmen.', 'english': 'In good weather, we go swimming.'},
     'grammar_rule': 'Without article, Dativ neutrum -> -em', 'grammar_tip': 'Dativ mask/neut stark = -em.'},

    {'id': 'gen_adj_049', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_multiple',
     'data': {'sentence_template': 'Frisch{gap_1}, gesund{gap_2} Lebensmittel sind wichtig.', 'gaps': [
         {'position': 'gap_1', 'context': 'Frisch__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']},
         {'position': 'gap_2', 'context': 'gesund__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Frische, gesunde Lebensmittel sind wichtig.', 'english': 'Fresh, healthy foods are important.'},
     'grammar_rule': 'Without article, Nominativ plural -> -e', 'grammar_tip': 'Mehrere Adjektive bekommen die gleiche starke Endung.'},

    {'id': 'gen_adj_050', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'adj_genitiv',
     'data': {'sentence_template': 'Die Meinung klug{gap_1} Menschen zählt.', 'gaps': [
         {'position': 'gap_1', 'context': 'klug__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'plural',
          'options': ['e', 'en', 'er', 'es', 'em']}],
              'full_correct': 'Die Meinung kluger Menschen zählt.', 'english': 'The opinion of wise people matters.'},
     'grammar_rule': 'Without article, Genitiv plural -> -er', 'grammar_tip': 'Genitiv Plural stark = -er.'},
]

ADJEKTIVE_BANK += [
    # ============================================================
    # CONFUSION SET A — "Hund" (maskulin) + "klein"
    # Focus: Nom masc (-e vs -er), Dat masc (-en vs -em)
    # ============================================================

    # Weak (bestimmt)
    {'id': 'gen_adj_051', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Der klein{gap_1} Hund bellt laut.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Der kleine Hund bellt laut.', 'english': 'The small dog barks loudly.'},
     'grammar_rule': 'Definite article, Nom masc -> -e', 'grammar_tip': 'Der + Nominativ maskulin = -e.'},

    {'id': 'gen_adj_052', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Ich spiele mit dem klein{gap_1} Hund.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich spiele mit dem kleinen Hund.', 'english': 'I play with the small dog.'},
     'grammar_rule': 'Definite article, Dat masc -> -en', 'grammar_tip': 'Dativ (dem) = fast immer -en.'},

    # Mixed (unbestimmt)
    {'id': 'gen_adj_053', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Ein klein{gap_1} Hund bellt laut.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'er', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ein kleiner Hund bellt laut.', 'english': 'A small dog barks loudly.'},
     'grammar_rule': 'Ein-word, Nom masc -> -er', 'grammar_tip': 'Ein hat keine Endung → Adjektiv zeigt -er.'},

    {'id': 'gen_adj_054', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Ich spiele mit einem klein{gap_1} Hund.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich spiele mit einem kleinen Hund.', 'english': 'I play with a small dog.'},
     'grammar_rule': 'Ein-word, Dat -> -en', 'grammar_tip': 'Im Dativ (einem) bekommt das Adjektiv -en.'},

    # Strong (ohne Artikel)
    {'id': 'gen_adj_055', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Klein{gap_1} Hund sucht ein Zuhause.', 'gaps': [
         {'position': 'gap_1', 'context': 'Klein__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Kleiner Hund sucht ein Zuhause.', 'english': 'Small dog is looking for a home.'},
     'grammar_rule': 'No article, Nom masc -> -er', 'grammar_tip': 'Stark: Nom mask = -er.'},

    {'id': 'gen_adj_056', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Mit klein{gap_1} Hund reist man nicht so leicht.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'em', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Mit kleinem Hund reist man nicht so leicht.', 'english': 'Travelling with a small dog isn’t that easy.'},
     'grammar_rule': 'No article, Dat masc -> -em', 'grammar_tip': 'Stark: Dativ mask/neut = -em.'},

    # Extra reinforcement (same set, additional contrasts)
    {'id': 'gen_adj_057', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Ich sehe den klein{gap_1} Hund im Park.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich sehe den kleinen Hund im Park.', 'english': 'I see the small dog in the park.'},
     'grammar_rule': 'Definite article, Akk masc -> -en', 'grammar_tip': 'Akk mask (den) = -en.'},

    {'id': 'gen_adj_058', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_hund',
     'data': {'sentence_template': 'Ich sehe einen klein{gap_1} Hund im Park.', 'gaps': [
         {'position': 'gap_1', 'context': 'klein__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'maskulin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich sehe einen kleinen Hund im Park.', 'english': 'I see a small dog in the park.'},
     'grammar_rule': 'Ein-word, Akk masc -> -en', 'grammar_tip': 'Einen + Akk mask = -en.'},


    # ============================================================
    # CONFUSION SET B — "Tasche" (feminin) + "neu"
    # Focus: Dat/Gen fem (-en with article vs -er without article)
    # ============================================================

    # Weak (bestimmt)
    {'id': 'gen_adj_059', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Die neu{gap_1} Tasche ist teuer.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Die neue Tasche ist teuer.', 'english': 'The new bag is expensive.'},
     'grammar_rule': 'Definite article, Nom fem -> -e', 'grammar_tip': 'Die + Nom/ Akk fem = -e.'},

    {'id': 'gen_adj_060', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Ich gehe mit der neu{gap_1} Tasche einkaufen.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich gehe mit der neuen Tasche einkaufen.', 'english': 'I go shopping with the new bag.'},
     'grammar_rule': 'Definite article, Dat fem -> -en', 'grammar_tip': 'Dativ (der) → -en.'},

    {'id': 'gen_adj_061', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Wegen der neu{gap_1} Tasche muss ich sparen.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Genitiv', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Wegen der neuen Tasche muss ich sparen.', 'english': 'Because of the new bag, I have to save money.'},
     'grammar_rule': 'Definite article, Gen fem -> -en', 'grammar_tip': 'Mit der-Wörtern: Genitiv meist -en.'},

    # Mixed (unbestimmt)
    {'id': 'gen_adj_062', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Eine neu{gap_1} Tasche ist praktisch.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Eine neue Tasche ist praktisch.', 'english': 'A new bag is practical.'},
     'grammar_rule': 'Ein-word, Nom fem -> -e', 'grammar_tip': 'Eine zeigt schon die Endung → oft -e.'},

    {'id': 'gen_adj_063', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Ich gehe mit einer neu{gap_1} Tasche einkaufen.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich gehe mit einer neuen Tasche einkaufen.', 'english': 'I go shopping with a new bag.'},
     'grammar_rule': 'Ein-word, Dat fem -> -en', 'grammar_tip': 'Dativ = -en.'},

    # Strong (ohne Artikel) — key contrast for fem: Dat/Gen -> -er
    {'id': 'gen_adj_064', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Mit neu{gap_1} Tasche gehe ich zur Arbeit.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Mit neuer Tasche gehe ich zur Arbeit.', 'english': 'I go to work with a new bag.'},
     'grammar_rule': 'No article, Dat fem -> -er', 'grammar_tip': 'Stark: Dativ feminin = -er.'},

    {'id': 'gen_adj_065', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Wegen neu{gap_1} Tasche muss ich sparen.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Wegen neuer Tasche muss ich sparen.', 'english': 'Because of a new bag, I have to save money.'},
     'grammar_rule': 'No article, Gen fem -> -er', 'grammar_tip': 'Stark: Genitiv feminin = -er.'},

    # Extra reinforcement
    {'id': 'gen_adj_066', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_tasche',
     'data': {'sentence_template': 'Ich nehme die neu{gap_1} Tasche mit.', 'gaps': [
         {'position': 'gap_1', 'context': 'neu__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'feminin',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich nehme die neue Tasche mit.', 'english': 'I take the new bag with me.'},
     'grammar_rule': 'Definite article, Akk fem -> -e', 'grammar_tip': 'Akk fem (die) bleibt -e.'},


    # ============================================================
    # CONFUSION SET C — "Buch" (neutrum) + "interessant"
    # Focus: Nom/Acc neut (-e vs -es), Dat neut (-en vs -em)
    # ============================================================

    # Weak (bestimmt)
    {'id': 'gen_adj_067', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Das interessant{gap_1} Buch ist lang.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Das interessante Buch ist lang.', 'english': 'The interesting book is long.'},
     'grammar_rule': 'Definite article, Nom neut -> -e', 'grammar_tip': 'Das + Nom/ Akk neut = -e.'},

    {'id': 'gen_adj_068', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Ich kaufe das interessant{gap_1} Buch.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'e', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich kaufe das interessante Buch.', 'english': 'I buy the interesting book.'},
     'grammar_rule': 'Definite article, Akk neut -> -e', 'grammar_tip': 'Das bleibt -e in Nom und Akk.'},

    {'id': 'gen_adj_069', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Ich lerne aus dem interessant{gap_1} Buch.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich lerne aus dem interessanten Buch.', 'english': 'I learn from the interesting book.'},
     'grammar_rule': 'Definite article, Dat neut -> -en', 'grammar_tip': 'Dativ (dem) → -en.'},

    # Mixed (unbestimmt)
    {'id': 'gen_adj_070', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Ein interessant{gap_1} Buch ist lang.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'es', 'article_type': 'unbestimmt', 'case': 'Nominativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ein interessantes Buch ist lang.', 'english': 'An interesting book is long.'},
     'grammar_rule': 'Ein-word, Nom neut -> -es', 'grammar_tip': 'Ein hat keine Endung → Adjektiv zeigt -es.'},

    {'id': 'gen_adj_071', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Ich kaufe ein interessant{gap_1} Buch.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'es', 'article_type': 'unbestimmt', 'case': 'Akkusativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich kaufe ein interessantes Buch.', 'english': 'I buy an interesting book.'},
     'grammar_rule': 'Ein-word, Akk neut -> -es', 'grammar_tip': 'Ein (ohne Endung) → starkes -es.'},

    {'id': 'gen_adj_072', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Ich lerne aus einem interessant{gap_1} Buch.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'en', 'article_type': 'unbestimmt', 'case': 'Dativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich lerne aus einem interessanten Buch.', 'english': 'I learn from an interesting book.'},
     'grammar_rule': 'Ein-word, Dat -> -en', 'grammar_tip': 'Im Dativ bekommt das Adjektiv -en.'},

    # Strong (ohne Artikel)
    {'id': 'gen_adj_073', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Interessant{gap_1} Buch!', 'gaps': [
         {'position': 'gap_1', 'context': 'Interessant__', 'answer': 'es', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Interessantes Buch!', 'english': 'Interesting book!'},
     'grammar_rule': 'No article, Nom neut -> -es', 'grammar_tip': 'Stark: Nom neut = -es.'},

    {'id': 'gen_adj_074', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_buch',
     'data': {'sentence_template': 'Aus interessant{gap_1} Buch lernt man viel.', 'gaps': [
         {'position': 'gap_1', 'context': 'interessant__', 'answer': 'em', 'article_type': 'ohne', 'case': 'Dativ', 'gender': 'neutrum',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Aus interessantem Buch lernt man viel.', 'english': 'You learn a lot from an interesting book.'},
     'grammar_rule': 'No article, Dat neut -> -em', 'grammar_tip': 'Stark: Dativ neut = -em.'},


    # ============================================================
    # CONFUSION SET D — "Freunde" (plural) + "alt"
    # Focus: Nom/Acc plural (-en with article vs -e without), Gen plural (-en vs -er)
    # ============================================================

    # Weak (bestimmt)
    {'id': 'gen_adj_075', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Die alt{gap_1} Freunde wohnen hier.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Die alten Freunde wohnen hier.', 'english': 'The old friends live here.'},
     'grammar_rule': 'Definite article, Nom plural -> -en', 'grammar_tip': 'Plural mit der-Wörtern: fast immer -en.'},

    {'id': 'gen_adj_076', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Ich treffe die alt{gap_1} Freunde heute.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Akkusativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich treffe die alten Freunde heute.', 'english': 'I meet the old friends today.'},
     'grammar_rule': 'Definite article, Akk plural -> -en', 'grammar_tip': 'Akk Plural mit die = -en.'},

    {'id': 'gen_adj_077', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Ich gehe mit den alt{gap_1} Freunden aus.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Dativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich gehe mit den alten Freunden aus.', 'english': 'I go out with the old friends.'},
     'grammar_rule': 'Definite article, Dat plural -> -en', 'grammar_tip': 'Dativ Plural: -en.'},

    {'id': 'gen_adj_078', 'module': 'adjektive', 'type': 'gap_fill', 'level': 1, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Wegen der alt{gap_1} Freunde bleibe ich länger.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'bestimmt', 'case': 'Genitiv', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Wegen der alten Freunde bleibe ich länger.', 'english': 'Because of the old friends, I stay longer.'},
     'grammar_rule': 'Definite article, Gen plural -> -en', 'grammar_tip': 'Mit der-Wörtern: Genitiv plural meist -en.'},

    # Mixed (possessiv behaves like ein-words in declension pattern; plural still -en)
    {'id': 'gen_adj_079', 'module': 'adjektive', 'type': 'gap_fill', 'level': 2, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Meine alt{gap_1} Freunde wohnen hier.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'en', 'article_type': 'possessiv', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Meine alten Freunde wohnen hier.', 'english': 'My old friends live here.'},
     'grammar_rule': 'Possessive, Nom plural -> -en', 'grammar_tip': 'Plural nach Possessiv: meistens -en.'},

    # Strong (ohne Artikel) — key contrast for plural: Nom/Acc -> -e, Gen -> -er
    {'id': 'gen_adj_080', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Alt{gap_1} Freunde sind wichtig.', 'gaps': [
         {'position': 'gap_1', 'context': 'Alt__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Nominativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Alte Freunde sind wichtig.', 'english': 'Old friends are important.'},
     'grammar_rule': 'No article, Nom plural -> -e', 'grammar_tip': 'Stark: Nom/Akk plural = -e.'},

    {'id': 'gen_adj_081', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Ich treffe alt{gap_1} Freunde wieder.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'e', 'article_type': 'ohne', 'case': 'Akkusativ', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Ich treffe alte Freunde wieder.', 'english': 'I meet old friends again.'},
     'grammar_rule': 'No article, Akk plural -> -e', 'grammar_tip': 'Stark: Akk plural = -e.'},

    {'id': 'gen_adj_082', 'module': 'adjektive', 'type': 'gap_fill', 'level': 3, 'topic': 'confusion_freunde',
     'data': {'sentence_template': 'Wegen alt{gap_1} Freunde bleibe ich länger.', 'gaps': [
         {'position': 'gap_1', 'context': 'alt__', 'answer': 'er', 'article_type': 'ohne', 'case': 'Genitiv', 'gender': 'plural',
          'options': ['e','en','er','es','em']}],
              'full_correct': 'Wegen alter Freunde bleibe ich länger.', 'english': 'Because of old friends, I stay longer.'},
     'grammar_rule': 'No article, Gen plural -> -er', 'grammar_tip': 'Stark: Genitiv plural = -er.'},
]
