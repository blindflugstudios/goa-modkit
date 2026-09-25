# my_mod_quest_terms - the text for the quest in Quests/.
#
# Quest files hold only text keys. This script gives the keys their words.
# It registers no handlers; the game runs it once when scripts load.
# Replace "my_mod" with your own mod id everywhere.

TERMS = {
    "my_mod/first_steps/title": "First steps",
    "my_mod/first_steps/step0_title": "Build a sickbed",
    "my_mod/first_steps/step0_description": "Injured crew recover faster in a bed of their own.",
    "my_mod/first_steps/step1_title": "Build four beds",
}

# The try/except matters: an error here could stop other scripts from loading.
try:
    for term, text in TERMS.items():
        localization.SetTerm("en", term, text)
except Exception as error:
    logger.LogWarning("my_mod", "could not register quest terms: {}".format(error))
