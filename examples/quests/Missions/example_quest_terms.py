# example_quest_terms - the words for the three example quests in Quests/.
#
# Quest files hold only text keys. This script gives the keys their words, in English and
# German. It registers no handlers; the game runs it once when scripts load.

TERMS = {
    "en": {
        "example/first_steps/title": "First steps",
        "example/first_steps/step0_title": "Build a sickbed",
        "example/first_steps/step0_description": "Injured crew recover faster in a bed of their own.",
        "example/first_steps/step1_title": "Build four beds",

        "example/patrol_chain/title": "Patrol chain",
        "example/patrol_chain/description": "Get a Spitfire into the air and bring a supply run home.",
        "example/patrol_chain/step0_title": "Own a Spitfire",
        "example/patrol_chain/step0_description": "Build or buy a Spitfire for your airfield.",
        "example/patrol_chain/step1_title": "Complete the supply drop",
        "example/patrol_chain/step1_description": "Fly the calm supply drop mission and come back successful.",
        "example/patrol_chain/step2_title": "Win three sorties with fighters",

        "example/map_campaign/title": "A base of our own",
        "example/map_campaign/description": "Turn this empty field into a working airbase.",
        "example/map_campaign/step0_title": "Lay a runway",
        "example/map_campaign/step0_description": "Build a tier-1 airstrip.",
        "example/map_campaign/step1_title": "Park the planes",
        "example/map_campaign/step1_description": "Build two parking spots.",
        "example/map_campaign/step2_title": "Store the supplies",
        "example/map_campaign/step2_description": "Mark out a storage zone of at least 20 tiles.",
    },
    "de": {
        "example/first_steps/title": "Erste Schritte",
        "example/first_steps/step0_title": "Baue ein Krankenbett",
        "example/first_steps/step0_description": "Verletzte erholen sich schneller in einem eigenen Bett.",
        "example/first_steps/step1_title": "Baue vier Betten",

        "example/patrol_chain/title": "Patrouillenkette",
        "example/patrol_chain/description": "Bring eine Spitfire in die Luft und einen Versorgungsflug nach Hause.",
        "example/patrol_chain/step0_title": "Besitze eine Spitfire",
        "example/patrol_chain/step0_description": "Baue oder kaufe eine Spitfire für deinen Flugplatz.",
        "example/patrol_chain/step1_title": "Schließe den Versorgungsabwurf ab",
        "example/patrol_chain/step1_description": "Fliege die ruhige Versorgungsmission und kehre erfolgreich zurück.",
        "example/patrol_chain/step2_title": "Gewinne drei Einsätze mit Jägern",

        "example/map_campaign/title": "Ein eigener Stützpunkt",
        "example/map_campaign/description": "Mach aus diesem leeren Feld einen funktionierenden Flugplatz.",
        "example/map_campaign/step0_title": "Leg eine Startbahn an",
        "example/map_campaign/step0_description": "Baue eine Startbahn der Stufe 1.",
        "example/map_campaign/step1_title": "Stell die Flugzeuge ab",
        "example/map_campaign/step1_description": "Baue zwei Parkplätze.",
        "example/map_campaign/step2_title": "Lagere die Vorräte",
        "example/map_campaign/step2_description": "Markiere eine Lagerzone mit mindestens 20 Feldern.",
    },
}

# The try/except matters: an error here could stop other scripts from loading.
try:
    for language, terms in TERMS.items():
        for term, text in terms.items():
            localization.SetTerm(language, term, text)
except Exception as error:
    logger.LogWarning("example_quests", "could not register quest terms: {}".format(error))
