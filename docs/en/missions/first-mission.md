# Write your first mission

A mission is a flight the player sends planes on. By the end of this page you will have written one from scratch, installed it, and seen it on the war map.

You need two files, both named after your mission:

- a `.json` file with the numbers: when the mission appears, how hard it is, what it costs and what it pays
- a `.py` file with the text: what the crew radios in, and how it reads afterwards

The `.py` file is optional (you can put the text in the JSON instead, see [Localization](../scripting/localization.md#text-in-the-json-instead-of-a-term)), but writing one teaches you how missions work, so this page uses it.

The finished result is the `coastal_patrol` example: [examples/coastal_patrol](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/coastal_patrol). Copying it and changing things is the fastest way in.

## 1. Pick an id

The **id** is the mission's name inside the game. It is the file name without the extension, and it appears in every text key the mission uses.

It must be unique across every mission the game knows, including the built-in ones and other people's mods. A duplicate does not cause an error: it silently replaces the other mission. So prefix your ids with your mod name:

```text
mymod_coastal_patrol
```

Use only letters, digits and underscores.

## 2. Write the JSON

Create `mymod_coastal_patrol.json`. The easiest start is a copy of `coastal_patrol.json` from the example. These are the parts that need thought.

### When it can appear

```json
"_missionRequirements": [
    { "Name": "RunwayTier",            "_requirementType": 0, "_value": "1" },
    { "Name": "EarliestAppearanceDay", "_requirementType": 1, "_value": "3" }
]
```

Each entry is a gate, and all of them must pass. Type 0 is the runway tier the base must have; type 1 is the earliest day, counted from the start of the campaign. Type 3 makes the mission follow another one, see [Chains and campaigns](chains.md). The full list is in the [Reference](reference.md#requirements).

### How the dice fall

Two rolls decide every mission:

1. `_asPlannedChance` (0–100) is the chance that the mission **goes as planned**.
2. Then a **skill roll** decides whether the crew pulls it off.

Two rolls with two answers each give four possible endings.

### The four outcomes: order is mandatory

```text
index 0   gone wrong,  skill failed
index 1   gone wrong,  skill passed
index 2   as planned,  skill failed
index 3   as planned,  skill passed
```

`_missionOutcomes` must have exactly four entries, in exactly this order. The game does not check: with fewer than four, the mission crashes when it ends.

Each outcome says whether it counts as a success (`_missionSuccess`) and carries effects: crew or base morale, damage to the planes, victory points.

```json
{
    "Name": "3 - as planned, skill passed",
    "_missionSuccess": true,
    "_outcomeEffect": [
        { "_outcomeEffectType": 7, "_effectValue": "1",  "_effectIcon": "ui_resource_victoryPoints" },
        { "_outcomeEffectType": 5, "_effectValue": "15", "_effectIcon": "ui_confidence" }
    ]
}
```

`_effectValue` is always written in quotes. For `Damage` (type 3) it is a range like `"20-60"`, rolled for each plane. For everything else it is a whole number like `"-40"`. All effect types are in the [Reference](reference.md#outcomes).

### The stats: at least two

```json
"_missionStats": [
    { "Name": "Recon",           "_missionSkillType": 2, "_statRange": { "x": 10.0, "y": 45.0 } },
    { "Name": "Maneuverability", "_missionSkillType": 4, "_statRange": { "x": 20.0, "y": 60.0 } }
]
```

The first entry is used when the mission goes as planned, the second when it goes wrong. The range is the difficulty: the game rolls a target inside it, and the squadron's combined skill has to reach that target. With fewer than two entries the skill roll crashes.

### Where it happens

`_potentialLocations` lists candidate places on the war map. One is drawn each time the mission appears. Copy entries from the [Locations](locations.md) page, including the coordinates: the game works out distance and fuel from the coordinates in your file.

## How a mission script actually runs

Before any code, one idea that makes everything else simple: a mission script is **not a program that runs from top to bottom**. It is a set of functions the game calls at fixed moments. You never call them yourself, and you never write a loop that waits for something.

The `@event_handler(...)` line above a function says *when* the game should call it:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    ...
```

This registers `send_mission_event` for "a progress step happened in flight". The game calls it, hands it the number of the mission in question, and does something with what it returns. Between calls your script does nothing at all. Such a function is called a **handler**.

Everything outside a handler (text definitions, constants, helper functions) runs **once**, when the game loads the file. That is why text is registered at the top level of the file and not inside a handler.

### The order the game calls handlers in

For one flight of one mission:

| When | Handler | Typical job |
|---|---|---|
| the mission is created | `initialize_mission` | set up state |
| in flight, once per progress step | `send_mission_event` | roll, and radio in what is happening |
| the flight ends | `set_mission_impact` | react to the outcome |
| the planes are back | `send_mission_result_text` | a closing line in the event log |
| the player opens the result window | `get_mission_result_text` | which text that window shows |

`send_mission_event` is the one that fires several times: three times for a mission with a JSON file, at one third, two thirds and the end of the flight. It is not told which step it is, so the script asks:

```python
events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

if events_sent == 1:      # first step: roll whether it goes to plan
    ...
elif events_sent == 2:    # second step: roll whether the crew pulls it off
    ...
```

That is all the `events_sent` checks in mission scripts mean: "which of my three moments in this flight is this?"

### Roll once, read afterwards

Each of the two rolls is made exactly once:

- `MakeAsPlannedRoll` performs the as-planned roll and stores it.
- `MakeSkillRoll` performs the skill roll and stores it.

`GetAsPlannedRoll` and `GetSkillRoll` read the stored result back. Every handler after the roll uses `Get...`. Rolling a second time would tell the player one story and hand them the outcome of another.

### Which mission am I?

Every handler receives `mission_entity_id`: the number of the one mission this call is about. The same script can be running for two flights of the same mission at once, so never keep per-flight information in a variable at the top of the file. Ask `missions_api` about the number you were given.

## 3. Write the Python

Create `mymod_coastal_patrol.py` next to the JSON. The script does two jobs: define the text, and decide which text appears when.

### Define the nine texts

A mission uses nine text slots, all named `missions/<id>/<slot>`. Register them at the top level of the file with `localization.SetTerm`, so they exist as soon as the script loads:

```python
from Blindflug.FlightMission import MissionEvent

MISSION_ID = "mymod_coastal_patrol"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Coastal Patrol")
_term("mission_description", "Fly the shoreline. Report anything that moves.")
_term("intel_threat_report", "Low. No enemy activity reported.")
_term("ap_transmission", "Patrol is airborne. Clear skies along the coast.")
_term("gw_transmission", "Cloud came in thicker than forecast.")
_term("ap_success_transmission", "Patrol complete. Nothing to report.")
_term("ap_failure_transmission", "The patrol flew its route but came back with nothing usable.")
_term("gw_success_transmission", "Despite the weather the flight brought back a full report.")
_term("gw_failure_transmission", "The flight lost the coastline in the murk and turned back early.")
```

`ap` means "as planned", `gw` means "gone wrong". The first three names are read by the game itself and cannot be changed; if one is missing, the mission window shows the raw key. The other six are used by the script, and every shipped mission uses these names, so stick with them. More in [Localization](../scripting/localization.md).

### Three handlers are enough

**The id.** Return exactly the file name:

```python
@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID
```

**The flight.** Roll in the first two steps and radio in what happened:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        slot = "ap_transmission" if going_as_planned else "gw_transmission"
        event_log.Create("missions/{}/{}".format(MISSION_ID, slot))

    elif events_sent == 2:
        going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        event_log.Create("missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed)))
```

**The result window.** Only read the rolls, never roll here:

```python
@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)
    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"
    return "{}_{}_transmission".format(prefix, suffix)
```

Any handler you do not write falls back to the game's shared default mission script. That is also why a mission with a JSON file and no script at all still flies: the default script does exactly what the code above does.

## 4. Install and run

Put both files into the `Missions` folder of a mod:

```text
Mods/my_first_mod/Missions/mymod_coastal_patrol.json
Mods/my_first_mod/Missions/mymod_coastal_patrol.py
```

Where `Mods/` lives on your computer is explained in [How mods work](../basics/mods.md); in the game, **Main menu → Mods → Open folder** takes you there.

Then start the game and load a save. The game reads mission files and scripts every time a save is loaded, so if the game was already running, go back to the main menu and load the save again.

To see the mission without waiting for the weekly draw, open the cheat console (see [Cheat console](../basics/cheats.md)) and type:

```text
create_mission mymod_coastal_patrol
```

The mission appears on the war map straight away. [Testing and reloading](../basics/testing.md) explains the edit loop and what to check when nothing shows up.

## What not to write

Four handler names exist in the game but are never called: `get_mission_icon`, `calculate_mission_modifiers`, `calculate_airplane_modifiers` and `calculate_pilot_modifiers`. Old scripts implement them at length. That code does nothing. The icon comes from `_missionIcon` in the JSON.

## Going further

- Missions that unlock other missions: [Chains and campaigns](chains.md)
- Scripts that react to the base instead of owning a mission: [Events](../scripting/events.md)
- Every handler, field and number: [Reference](reference.md)
