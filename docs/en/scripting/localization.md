# Localization

Every piece of text the player sees is looked up by a **key**, a short name like `missions/coastal_patrol/mission_name`. The game finds the text for that key in the player's language. This page shows how a mod gives its keys their text, in one language or many, without touching any of the game's own files.

## The simplest way: text in the mission JSON

A mission can carry its text directly in its JSON file. No script, no keys:

```json
{
    "_rawMissionName": "The Lost Bombers",
    "_rawMissionDescription": "A flight of our own bombers is limping home from France."
}
```

This is one language only, and it covers exactly nine slots per mission. See [Text in the JSON instead of a term](#text-in-the-json-instead-of-a-term) below. For anything else you register text from a script.

## Defining text from a script

```python
localization.SetTerm("en", "mymod/greeting", "Good morning, gentlemen.")
```

`SetTerm(language_code, key, text)` gives a key its text in one language. A key with its texts is called a **term**.

Call it at the **top level** of a script, not inside a handler. The top level runs once, when the game loads the script, so the text exists before anything needs it.

A script that only defines text is perfectly valid. It needs no handler, no JSON and no mission id. Put it in the mod's `Missions/` folder like any other script; the game runs every script it finds there.

### Why this is safe

Text you register does not go into the game's translation files. The game keeps a separate store for text from scripts, adds keys to it as scripts register them, and looks there as well. Nothing you do with `SetTerm` changes a file on disk, and there is no translation step to run.

If the key already exists in the game's own texts, `SetTerm` replaces that text for as long as your mod is loaded. That is how a mod can reword a built-in line. It is also why you should prefix every key of your own with your mod name: an accidental match silently overwrites the game's text.

## Mission texts

A mission uses nine keys, all shaped `missions/<missionId>/<slot>`.

**Three are read by the game itself** and cannot be renamed:

| Key | Shown in |
|---|---|
| `missions/<id>/mission_name` | the mission list and the result window |
| `missions/<id>/mission_description` | the mission window |
| `missions/<id>/intel_threat_report` | the threat line in the mission window |

If one is missing, the raw key appears in the game.

**Six are used by the mission script.** The shared default mission script uses exactly these names, so a mission without a script of its own needs them too:

| Key | When |
|---|---|
| `missions/<id>/ap_transmission` | in flight, going to plan |
| `missions/<id>/gw_transmission` | in flight, gone wrong |
| `missions/<id>/ap_success_transmission` | as planned, skill passed |
| `missions/<id>/ap_failure_transmission` | as planned, skill failed |
| `missions/<id>/gw_success_transmission` | gone wrong, skill passed |
| `missions/<id>/gw_failure_transmission` | gone wrong, skill failed |

`ap` means "as planned", `gw` means "gone wrong". The four `*_success` and `*_failure` keys match the four outcome slots of the mission JSON one to one.

A small helper keeps a mission script readable:

```python
MISSION_ID = "mymod_coastal_patrol"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Coastal Patrol")
_term("mission_description", "Fly the shoreline. Report anything that moves.")
```

A mission script may register as many extra keys as it likes (`missions/<id>/veteran_departure`, say) and use them with `event_log.Create`.

## Text in the JSON instead of a term

The nine `_raw*` fields of a mission JSON answer the nine slots above directly. When a raw field is filled, the game uses it before it looks up the key, so a mission with raw text needs no `SetTerm` call and no script at all.

| JSON field | Slot it answers |
|---|---|
| `_rawMissionName` | `mission_name` |
| `_rawMissionDescription` | `mission_description` |
| `_rawIntelThreatReport` | `intel_threat_report` |
| `_rawApTransmission` | `ap_transmission` |
| `_rawGwTransmission` | `gw_transmission` |
| `_rawApSuccessTransmission` | `ap_success_transmission` |
| `_rawApFailureTransmission` | `ap_failure_transmission` |
| `_rawGwSuccessTransmission` | `gw_success_transmission` |
| `_rawGwFailureTransmission` | `gw_failure_transmission` |

An empty field counts as not filled, and the game falls back to the key.

**Only these nine slots work this way.** There is no tenth `_raw*` field: `event_log.Create("missions/mymod_patrol/my_own_line")` with no term behind it prints the raw key.

### Which to use

| | `_raw*` in JSON | `SetTerm` in a script |
|---|---|---|
| Needs a script | no | yes |
| Number of texts | exactly nine | unlimited |
| Languages | one | any, including ones the game does not ship |
| Good for | a mission whose text is fixed | text that varies with what happened in flight |

The two combine: raw text covers the nine standard slots, and a script adds its own terms for anything beyond them. The `raf_collection` example does exactly that: three missions ship raw text alone, and `greenhorn_watch` adds terms of its own so it can tell a different story depending on how experienced the crew is.

## Quest texts

Quest files carry keys, not text: `_questTitle`, `_subQuestTitle` and `_subQuestDescription` hold keys, and the game looks them up. The game's own quests use this pattern:

```text
quest/<questId>/title
quest/<questId>/subQuest<N>_title
quest/<questId>/subQuest<N>_description
```

To give a mod quest its text, ship a small script in the mod's `Missions/` folder that registers those keys:

```python
QUEST_ID = "mymod_first_steps"

localization.SetTerm("en", "quest/{}/title".format(QUEST_ID), "First Steps")
localization.SetTerm("en", "quest/{}/subQuest0_title".format(QUEST_ID), "Clear the field")
localization.SetTerm("en", "quest/{}/subQuest0_description".format(QUEST_ID), "Fell five trees.")
```

The keys only have to match what the quest file says. See [Quests](../quests/index.md).

## Placeholders

`event_log.Create` takes a dictionary that fills `{[NAME]}` placeholders:

```python
localization.SetTerm("en", "mymod/pilot_tired",
                     "{[PILOT]} came back exhausted after {[HOURS]} hours in the air.")

event_log.Create("mymod/pilot_tired", {"PILOT": str(pilot_id), "HOURS": "6"})
```

Placeholder names are case-sensitive and must match exactly. Values must be strings, so wrap numbers and ids in `str(...)`.

## Inline formatting

Three tags work inside any text:

| Tag | Effect |
|---|---|
| `[character:<id>]` | a clickable link to that character, shown as their name |
| `[resource:<name>]` | the resource's icon and color |
| `[morale:<name>]` | the morale category's icon and color |

Combine them with placeholders to name a character from an event:

```python
localization.SetTerm("en", "mymod/chat",
                     "[character:{[FIRST]}] talked to [character:{[SECOND]}] until dawn.")

event_log.Create("mymod/chat", {"FIRST": str(first_id), "SECOND": str(second_id)})
```

For resources and morale, put the game's own value into the text when the script loads:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Game.Characters.Morale import MoraleCategory

localization.SetTerm("en", "mymod/mice",
                     "Mice got into the [resource:{}] again.".format(ResourceType.FoodRations))
localization.SetTerm("en", "mymod/good_chat",
                     "Their [morale:{}] improved.".format(MoraleCategory.Mood))
```

f-strings work as well, and the game's own scripts use them. Remember to double the braces of a placeholder inside an f-string: `f"[character:{{[FIRST]}}] shared the [resource:{ResourceType.FoodRations}]"`.

## Languages

Always define English (`"en"`). When a term has no text in the player's language, the game falls back to a language that has it, which is English if you defined it, rather than showing the raw key.

To translate, call `SetTerm` once per language:

```python
localization.SetTerm("en", "mymod/greeting", "Good morning, gentlemen.")
localization.SetTerm("de", "mymod/greeting", "Guten Morgen, meine Herren.")
localization.SetTerm("fr", "mymod/greeting", "Bonjour, messieurs.")
```

The game ships these language codes:

`en`, `en-GB`, `de-DE`, `de`, `ar`, `bg`, `ca`, `zh-CN`, `zh-TW`, `cs`, `da`, `nl`, `fi`, `fr`, `el`, `hu`, `id`, `it`, `ja`, `ko`, `ms`, `nb`, `fa`, `pl`, `pt`, `pt-BR`, `ro`, `ru`, `es`, `es-419`, `sv`, `gsw-CH`, `th`, `tr`, `uk`, `vi`

German is `de` - that is the language players pick in the options (`de-DE` in the list is a test language, you can ignore it). An unknown code is added automatically, so text for a language the game does not ship needs no preparation (the player still needs a way to select that language).

A handy pattern for several languages:

```python
TEXTS = {
    "mymod/greeting": {
        "en": "Good morning, gentlemen.",
        "de": "Guten Morgen, meine Herren.",
    },
}

for key, translations in TEXTS.items():
    for language, text in translations.items():
        localization.SetTerm(language, key, text)
```

## When the mod is removed

Text registered with `SetTerm` exists only while the script that registered it is loaded. It is never written into the save game or into the game's files.

If a player removes or switches off your mod and loads a save:

- Your terms are gone. Anything in the save that still points at one of your keys shows the **raw key** instead of the text. That applies to old event log lines your scripts wrote and to missions from your mod that were still waiting on the war map.
- A key of the game's own that your mod had reworded shows the game's original text again.
- Nothing is damaged; reinstalling the mod brings the text back.

Mission text from `_raw*` fields is copied into the mission when it is created, so a mission that was already on the war map keeps its name even after the mod is gone.

## Naming your keys

Prefix every key with your mod name (`mymod/...`) so it cannot collide with the game or another mod: an existing key is silently overwritten. Mission keys are the exception, because they must follow `missions/<missionId>/...`. Make the mission id itself distinctive instead, which you should anyway.
