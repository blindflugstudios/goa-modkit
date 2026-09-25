# my_mod_campaign_terms - text for the quest line in Quests/.
# Registers no handlers; the game runs it once when scripts load.
# Replace "my_mod" with your own mod id everywhere.

TERMS = {
    "my_mod/campaign_start/title": "A new airfield",
    "my_mod/campaign_start/step0_title": "Build an airstrip",
    "my_mod/campaign_start/step1_title": "Lay out two parking spots",
    "my_mod/campaign_next/title": "Supplies",
    "my_mod/campaign_next/step0_title": "Mark a storage zone of 20 tiles",
}

try:
    for term, text in TERMS.items():
        localization.SetTerm("en", term, text)
except Exception as error:
    logger.LogWarning("my_mod", "could not register campaign terms: {}".format(error))
