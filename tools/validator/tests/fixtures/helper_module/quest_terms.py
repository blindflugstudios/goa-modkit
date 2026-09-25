# A helper module: no handlers, no .json, and correct.
#
# The loader imports every .py in Missions/, which runs the module top level. That is how a
# mod gives its quests readable text, since quests carry no script of their own and no raw
# text fields. Flagging this file would tell a modder to delete working code.

TERMS = {
    "mymod/patrol/title": "Eyes on the Channel",
    "mymod/patrol/subQuest0_title": "Fly a coastal patrol",
}

try:
    for term, text in TERMS.items():
        localization.SetTerm("en", term, text)
except Exception as error:
    print("mymod: could not register quest terms: %s" % error)
