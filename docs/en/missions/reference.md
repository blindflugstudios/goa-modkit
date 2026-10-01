# Reference

Everything a mission can contain, in one place: how the game finds your files, the order in which it calls your script, every handler, every JSON field and every number the JSON expects.

New to missions? Start with [Write your first mission](first-mission.md) and come back here when you need a detail.

## Two ways to build a mission

A mission is identified by its **id**, which is simply its file name without the extension. `coastal_patrol.json` is the mission `coastal_patrol`.

| | With a JSON file (the normal way) | Script only (no JSON) |
|---|---|---|
| Files | `<id>.json`, optionally `<id>.py` | `<id>.py` |
| Base values (time window, flight time, enemies) | from the JSON | from the getter handlers, each optional |
| Skill stats | `_missionStats` | `missions_api.SetMissionStat` in `initialize_mission` |
| Map location | `_potentialLocations` | `missions_api.SetMissionLocation` |
| As-planned chance | `_asPlannedChance` | `missions_api.SetAsPlannedChance` |
| Outcomes | four `_missionOutcomes` | `missions_api.SetOutcome` and `AddOutcomeEffect`, plus `get_mission_result` (required) |
| In-flight events per flight | always 3 | `get_mission_events_count` (default 3) |
| Appears on its own (weekly draw, historic spawn) | yes | no, see [Script-only missions](#script-only-missions) |

Use the JSON way unless you have a reason not to. It survives saving and loading, it can be checked by the validator, and it appears in the game without any other script handing it out.

### Which script runs

Every mission runs on a script, but you rarely have to write one:

- If a `.py` file named exactly like the mission exists, the game uses its handlers.
- For every handler that file does not define, and for every mission without its own file, the game uses the shared **default mission script** that ships with the game. It reads the mission's id and emits the standard transmissions from the nine text slots (see [Localization](../scripting/localization.md#mission-texts)).

So a JSON file plus its text is a complete mission. Write `<id>.py` only to change what happens in flight or which text appears. The match is on the exact file name: a script called `recon.py` never attaches itself to a mission called `dangerous_recon`.

### Where the game looks

Mission files are read from several places, in this order. When two places hold the same id, the **last one wins**, and replaces the earlier mission completely:

1. the game's own missions
2. DLC missions
3. the `Missions/` folder of every enabled mod (Workshop mods first, then mods you installed by hand)
4. the `Missions/` folder in the game data folder (see [How mods work](../basics/mods.md))

This is why an id that matches a built-in mission replaces that mission, and why a local copy of a mod beats the Workshop version you are subscribed to. Prefix your ids with your mod name (`mymod_coastal_patrol`) unless you really mean to replace something.

A mod's `Missions/` folder is also its only script folder. Event scripts, helper modules and quest text scripts all go there. See [Scripting](../scripting/index.md).

### Script-only missions

A mission with a `.py` and no `.json` never turns up by itself. The weekly draw and the historic spawn only consider missions whose data the game already knows, and a script-only mission has no data until it has been created once.

It can be created two ways:

- `missions_api.CreateMission("<id>")` from another script. This is how a campaign hands out a follow-up.
- the `create_mission <id>` cheat, for testing.

Three consequences to plan for:

- **After the first creation the draw can pick it.** The data your script authored now exists, so the weekly draw treats the mission like any other. If your script added no gates, the mission can appear on any map and any date. Always call `AddMissionRequirement` (and `SetTags` if it belongs to one campaign) from `initialize_mission`.
- **From the second creation on, the getters are no longer asked.** The game now builds the mission from the data authored the first time, like a JSON mission: the name, description and threat line come from the text slots `missions/<id>/mission_name`, `missions/<id>/mission_description` and `missions/<id>/intel_threat_report`, and the flight has 3 events. Register those three terms even in a script-only mission.
- **The authored data is not saved.** It lives in memory for the current session only. If the player loads a save with such a mission in flight, the authored outcomes are gone and the game asks [`get_mission_result`](#get_mission_result) instead. If that handler is missing, the mission fails with an error when it ends. Any script-only mission should define it.

See the `script_only_scramble` example on the [Examples](../examples.md) page.

## Lifecycle

What happens to one mission, from the week it is planned to the result window:

| # | Step | What happens |
|---|---|---|
| 1 | Weekly schedule | At the start of each week the game spreads a number of mission slots across the week. The number depends on the base's rank. |
| 2 | Hourly historic check | Every in-game hour, each historic mission whose gates pass is created: one with a `_historicDay` on that day or, if its other gates only pass later, as soon as they do; one without a date right away. It never waits for the weekly schedule and never takes up a slot. A historic mission that failed or was cancelled is back at the next hourly check, even while its result report is still unread. |
| 3 | Random draw | When one of the week's slots comes due, it is filled by the random draw. All non-historic missions whose gates pass form a pool. One is drawn and removed from the pool. When the pool is empty it refills. |
| 4 | Gates | A mission is eligible when all `_missionRequirements` pass, the current map shares one of its `_tags`, and (for historic missions) it has not been won yet and is not already on the map. |
| 5 | Creation | The game picks a location (one draw, plus up to five re-draws to avoid two missions on the same spot), works out distance and fuel from it, and sets up the mission from JSON or script. Then it calls [`initialize_mission`](#initialize_mission). |
| 6 | Waiting | The mission sits on the war map until the player sends planes or its start window runs out. Historic missions never run out, and neither does a mission whose time-to-start maximum is `0`. |
| 7 | Flight | The clock starts once **all** assigned planes are airborne. [`send_mission_event`](#send_mission_event) fires each time the flight passes another step (by default at one third, two thirds and the end). |
| 8 | Outcome | With data: the rolls pick one of the four outcomes, its effects are applied, then [`set_mission_impact`](#set_mission_impact) runs. Without data: [`get_mission_result`](#get_mission_result) decides, then `set_mission_impact` runs. |
| 9 | Return | Planes land, crew records update, events fire. Then [`send_mission_result_event`](#send_mission_result_event), or [`send_mission_cancelled_event`](#send_mission_cancelled_event) if the player called the mission off or it expired. |
| 10 | Result window | When the player opens it, [`get_mission_result_text`](#get_mission_result_text) supplies the text. |

### The two rolls and the outcome index

Two dice rolls decide every mission:

1. **As planned?** A roll against `_asPlannedChance` (0–100). Did the situation develop as briefed?
2. **Skill passed?** The game rolls a target inside the range of one mission stat, then adds up the skill of the squadron. If the squadron reaches the target, the roll passes. The first stat is used when the mission went as planned, the second when it did not.

The two answers pick the outcome:

| Index | As planned | Skill roll | Meaning |
|---|---|---|---|
| 0 | no | failed | Gone wrong and failed |
| 1 | no | passed | Gone wrong but salvaged |
| 2 | yes | failed | Went to plan, still failed |
| 3 | yes | passed | Full success |

For programmers: `index = (skillPassed ? 1 : 0) | (asPlanned ? 2 : 0)`.

!!! warning "Exactly four outcomes, in this order"
    The game does not check how many outcomes you wrote. With fewer than four, the mission crashes the moment it ends, long after you stopped suspecting the JSON. With more than four, the extras are never used.

!!! warning "At least two mission stats"
    The skill roll reads the first and the second entry of `_missionStats` directly. With only one, the mission crashes on the skill roll.

"Success" in a chain or a quest does not mean index 3. Which ending counts as a success is fixed by its position: index 0 and 2 are failures, index 1 (gone wrong, but salvaged) and index 3 are successes.

## Handlers

A handler is a Python function the game calls at a fixed moment. You mark it with the `@event_handler(...)` decorator and the name of the moment:

```python
from Blindflug.FlightMission import MissionEvent

@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    ...
```

**Every mission script needs `from Blindflug.FlightMission import MissionEvent` at the top.** Scripts get no automatic imports, so without that line `MissionEvent` does not exist in your script.

The function name is up to you; the decorator is what counts. Every handler receives exactly one argument, `mission_entity_id`: the number of the mission this call is about. Pass it on to every `missions_api` call. The same script can run for two flights of the same mission at once, so never store per-flight state in a module-level variable.

| Handler | `MissionEvent` constant | Returns | Called in |
|---|---|---|---|
| `get_mission_id` | `GET_MISSION_ID` | str | both modes |
| `initialize_mission` | `INITIALIZE_MISSION` | nothing | both modes |
| `send_mission_event` | `SEND_MISSION_EVENT` | nothing | both modes |
| `set_mission_impact` | `SET_MISSION_IMPACT` | nothing | both modes |
| `send_mission_result_event` | `SEND_MISSION_RESULT_EVENT` | nothing | both modes, except when cancelled |
| `send_mission_cancelled_event` | `SEND_MISSION_CANCELLED_EVENT` | nothing | both modes |
| `get_mission_result_text` | `GET_MISSION_RESULT_TEXT` | str | both modes |
| `get_mission_name` | `GET_MISSION_NAME` | str | script only |
| `get_mission_description_text` | `GET_MISSION_DESCRIPTION_TEXT` | str | script only |
| `get_time_to_start` | `GET_TIME_TO_START` | int | script only |
| `get_completion_time` | `GET_COMPLETION_TIME` | int | script only |
| `get_threat_level` | `GET_THREAT_LEVEL` | str | script only |
| `get_enemy_count` | `GET_ENEMY_COUNT` | int | script only |
| `get_mission_events_count` | `GET_MISSION_EVENTS_COUNT` | int | script only |
| `get_fuel_level` | `GET_FUEL_LEVEL` | int | script only |
| `get_mission_result` | `GET_MISSION_RESULT` | bool | script only - **required** |
| `get_mission_icon` | `GET_MISSION_ICON` | - | **never called** |
| `calculate_mission_modifiers` | `CALCULATE_MISSION_MODIFIERS` | - | **never called** |
| `calculate_airplane_modifiers` | `CALCULATE_AIRPLANE_MODIFIERS` | - | **never called** |
| `calculate_pilot_modifiers` | `CALCULATE_PILOT_MODIFIERS` | - | **never called** |

"Script only" handlers are asked once, when a mission without a JSON file is created for the first time (see [Script-only missions](#script-only-missions)). A mission with a JSON file ignores them.

### get_mission_id

Returns the mission's id as a string.

```python
MISSION_ID = "mymod_coastal_patrol"

@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID
```

A script-only mission must define it: that is how the game recognises the file as a mission of its own. Return exactly the file name. In a script next to a JSON file the game does not read the value, but your own code usually builds text keys from it, so keep it identical to the file name there too. The shared default script returns `missions_api.GetMissionId(mission_entity_id)`, which works for any mission.

### initialize_mission

Called once, right after the mission has been created and before it appears on the war map.

This is where a script-only mission writes everything a JSON file would carry: gates, stats, location, slots, difficulty, outcomes. A mission with a JSON file can use it too, for example to adjust difficulty to the campaign so far:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    if campaign_state.get("raids_survived") >= 2:
        missions_api.SetMissionStat(mission_entity_id, "Fight", 76, 115)
        missions_api.SetAsPlannedChance(mission_entity_id, 35)
```

Calling `missions_api.CreateMission` from here is refused and logged, because this handler runs in the middle of creating a mission.

!!! note
    On a mission with a JSON file, `SetMissionStat`, `SetOutcome`, `AddOutcomeEffect`, `AddMissionRequirement` and `SetTags` change the data the game loaded from that file, for the rest of the session. Every later copy of the mission sees the change, and effects you add pile up. Adjust stats and chances freely; add effects and gates only in script-only missions.

### send_mission_event

Called while the mission is in flight, once per progress step. A mission with a JSON file always has three steps; a script-only mission has as many as [`get_mission_events_count`](#get_mission_events_count) returns. The steps fall evenly across the flight time, the last one at the end.

The handler is not told which step this is. Ask:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        ...
    elif events_sent == 2:
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        ...
```

`GetNumberOfEventsSent` returns 1 on the first call, 2 on the second, and so on.

**Roll once, read afterwards.** `MakeAsPlannedRoll` and `MakeSkillRoll` perform a roll and store it; `GetAsPlannedRoll` and `GetSkillRoll` read the stored result. Make the as-planned roll first, because the skill roll uses it to pick which stat to roll against. Every later handler only reads. Rolling a second time would tell the player one story and hand them the outcome of another.

If you override this handler, you must make both rolls yourself. The outcome step reads them.

### set_mission_impact

Called when the flight is over and the outcome has been decided. Effects from the JSON outcome have already been applied, and `missions_api.IsMissionSuccessful` already gives the answer.

Use it for consequences the JSON cannot express, and to hand out follow-up missions:

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
```

See [Chains and campaigns](chains.md#when-json-is-not-enough).

### send_mission_result_event

Called after the planes have come back from a mission that was flown to the end - always, except when the mission was cancelled. The usual job is one closing line in the event log with `event_log.Create`. The Python constant is `MissionEvent.SEND_MISSION_RESULT_EVENT`; the event string is `send_mission_result_text`.

### send_mission_cancelled_event

Called instead of `send_mission_result_event` when the player aborts the mission or it expires. The Python constant is `MissionEvent.SEND_MISSION_CANCELLED_EVENT`; the event string is `send_mission_cancelled_text`. A cancelled mission applies no outcome and counts as `cancelled` for chains, not as a failure.

### get_mission_result_text

Called when the player opens the result window of a mission that was flown to the end. Return the text key of the line the window should show. Only read the rolls here; never make them.

```python
@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"
    return "missions/{}/{}_{}_transmission".format(MISSION_ID, prefix, suffix)
```

A key of the form `missions/<id>/<slot>` also picks up the mission's `_raw*` text from the JSON (see [Localization](../scripting/localization.md#text-in-the-json-instead-of-a-term)).

### get_mission_name

Script-only missions. Returns the text key of the mission's name. Default when missing: the mission id.

### get_mission_description_text

Script-only missions. Returns the text key of the description in the mission window. Default when missing: empty.

### get_time_to_start

Script-only missions. Returns how many in-game minutes the mission waits on the war map before it expires. Default when missing: 60.

Returning `0` or a negative number cancels the mission at the next in-game minute. Unlike `_timeToStartRange` in a JSON file, there is no "never expires" value here.

### get_completion_time

Script-only missions. Returns the flight time in in-game minutes. Default when missing: 120.

### get_threat_level

Script-only missions. Returns the text key of the threat line in the mission window. Default when missing: `Low`.

### get_enemy_count

Script-only missions. Returns the number of enemy planes reported. Default when missing: 0. There is no API call to change it later, so on the second and later creation of a script-only mission the count is 0.

### get_mission_events_count

Script-only missions. Returns how many times [`send_mission_event`](#send_mission_event) fires during the flight. Default when missing: 3.

### get_fuel_level

Script-only missions. Returns the fuel the flight costs. Default when missing: 100. If the script calls `SetMissionLocation`, the fuel is recalculated from the distance to that location.

### get_mission_result

Returns `True` if the mission succeeded, `False` if not. Every script-only mission must define it: it decides the ending, and without it the mission fails with an error when it finishes.

```python
@event_handler(MissionEvent.GET_MISSION_RESULT)
def get_mission_result(mission_entity_id):
    return missions_api.GetAsPlannedRoll(mission_entity_id) and missions_api.GetSkillRoll(mission_entity_id)
```

### get_mission_icon

Never called. The icon comes from `_missionIcon` in the JSON. Old example scripts implement this handler at length; that code does nothing.

### calculate_mission_modifiers

Never called. Do not implement it.

### calculate_airplane_modifiers

Never called. Do not implement it.

### calculate_pilot_modifiers

Never called. Do not implement it.

`get_mission_fatalities`, found in very old documentation, no longer exists at all. Losses come from the `Damage` outcome effect.

## JSON schema

The mission file is read field by field. Field names start with an underscore and must be spelled exactly; an unknown or misspelled field is silently ignored. Every field is optional as far as loading goes, but a playable mission needs the ones marked **required**.

| Field | Type | Meaning |
|---|---|---|
| `_maxPlaneSlots` | int | How many planes the player may assign. |
| `_timeToStartRange` | `{"x": min, "y": max}` | Game minutes the mission waits on the war map before it expires, rolled between min and max. A maximum of `0` means it never expires. Ignored for historic missions, which never expire. |
| `_timeToCompleteRange` | `{"x": min, "y": max}` | Flight time in game minutes, rolled between min and max. |
| `_missionRequirements` | list | Gates that must all pass before the mission can appear. See [Requirements](#requirements). |
| `_missionOutcomes` | list | **Required, exactly 4**, in the fixed order. See [Outcomes](#outcomes). |
| `_asPlannedChance` | int | Chance in percent (0–100) that the mission goes as planned. |
| `_missionStats` | list | **Required, at least 2.** The first is rolled when the mission goes as planned, the second when it does not. See [Mission stats](#mission-stats). |
| `_enemyPlaneReport` | int | Enemy planes shown in the mission window. Keep it at 18 or below; the validator warns above that. |
| `_missionIcon` | string | The icon on the war map. See [Icons](#icons). |
| `_potentialLocations` | list | Candidate places on the war map; one is drawn per mission. Distance and fuel follow from it. With an empty list the game picks a random location. See [Locations](locations.md). |
| `_difficultyRating` | int | Stars shown to the player, 1–3. Default 1. |
| `_tags` | list of strings | Which maps the mission belongs to. See [Map tags](#map-tags). |
| `_isHistoric` | bool | Makes the mission a story beat. See [Chains and campaigns](chains.md#historic-missions). |
| `_historicDay` | date | The earliest day a historic mission appears: on that day, or later if its other gates only pass later. A year below 1900 counts as "no date". |
| `_rawMissionName` ... `_rawGwFailureTransmission` | string | Nine optional text fields. See [Localization](../scripting/localization.md#text-in-the-json-instead-of-a-term). |
| `_distanceLocationDependant` | `{"x", "y"}` | Written by Blindflug's own mission tool. The game does not read it; leave it alone or leave it out. |

Dates are written as an object:

```json
"_historicDay": { "Year": 1940, "Month": 8, "Day": 13, "Hour": 0, "Minute": 0 }
```

Fields that older files and older documentation carry, and which the game no longer reads: `_distanceRange`, `_hasMaximumDay`, `_maximumDay`, `_mapId`, `_mapIds`, `_mapTags`, `_missionTags`. A mission that still relies on `_mapTags` loses its map restriction without any warning and appears everywhere. Use `_tags`.

The `"Name"` entries inside lists (`"Name": "RunwayTier"`) are labels for humans. The game ignores them.

### Requirements

Each entry in `_missionRequirements` is one gate. All gates must pass.

```json
"_missionRequirements": [
    { "Name": "RunwayTier",            "_requirementType": 0, "_value": "1" },
    { "Name": "EarliestAppearanceDay", "_requirementType": 1, "_value": "3" }
]
```

`_value` is always a string, even for numbers.

| `_requirementType` | Name | `_value` | Passes when |
|---|---|---|---|
| 0 | `RunwayTier` | tier as a number, `"2"` | the base has a runway of at least this tier |
| 1 | `EarliestAppearanceDay` | days, `"14"` | the day number, counted from the map's starting date, has reached this value |
| 2 | `LatestAppearanceDay` | days, `"40"` | the day number, counted from the map's starting date, has not passed this value |
| 3 | `CompletedMission` | `"<missionId>"` or `"<missionId>,<outcome>"` | the player has finished that mission with that outcome at least once |

For `CompletedMission`, the outcome is `success`, `failure` or `cancelled`. Without an outcome, any finish counts, including a cancelled one. The game remembers every finish, so after a failed and a later successful attempt both `,failure` and `,success` pass. See [Chains and campaigns](chains.md).

### Outcomes

Exactly four entries, in the order of the [outcome index](#the-two-rolls-and-the-outcome-index):

```json
{
    "Name": "3 - as planned, skill passed",
    "_missionSuccess": true,
    "_outcomeEffect": [
        { "_outcomeEffectType": 7, "_effectValue": "5",     "_effectIcon": "ui_resource_victoryPoints" },
        { "_outcomeEffectType": 5, "_effectValue": "15",    "_effectIcon": "ui_confidence" },
        { "_outcomeEffectType": 3, "_effectValue": "10-40", "_effectIcon": "ui_health_poor_injured" }
    ]
}
```

| Field | Meaning |
|---|---|
| `_missionSuccess` | Whether this ending counts as a success, for chains, quests and the player's records. |
| `_outcomeEffect` | List of effects applied when the mission ends this way. May be empty. |
| `_outcomeEffectType` | Which effect, see the table below. |
| `_effectValue` | A string. A whole number for everything except `Damage`; a range `"min-max"` for `Damage`. |
| `_effectIcon` | Icon shown next to the effect in the result window. Copy it from an example; an empty string shows no icon. |

| `_outcomeEffectType` | Name | `_effectValue` | Effect |
|---|---|---|---|
| 0 | `CrewMood` | number, `"-20"` | mood of everyone who flew |
| 1 | `CrewConfidence` | number | confidence of everyone who flew |
| 2 | `CrewEnergy` | number | energy of everyone who flew |
| 3 | `Damage` | range, `"20-60"` | damage to the planes, rolled per flight; heavy damage also hurts the crew |
| 4 | `BaseMood` | number | mood of the whole base |
| 5 | `BaseConfidence` | number | confidence of the whole base |
| 6 | `BaseEnergy` | number | energy of the whole base |
| 7 | `VictoryPoints` | number | victory points, capped at the current limit |
| 8 | `MaxVictoryPoints` | - | **do not use.** The game uses it internally to show "victory point limit reached"; in a mission file it crashes the mission when it ends. |

A number where a range is expected, or the other way round, is not a crash: the game logs an error in `Player.log` and skips that one effect.

### Mission stats

```json
"_missionStats": [
    { "Name": "Recon",           "_missionSkillType": 2, "_statRange": { "x": 10.0, "y": 45.0 } },
    { "Name": "Maneuverability", "_missionSkillType": 4, "_statRange": { "x": 20.0, "y": 60.0 } }
]
```

`_statRange` is the range the target is rolled in. The squadron's combined skill must reach it. The shipped missions sit around 40–70 for an ordinary patrol; 85 and above is meant to be lost more often than won.

| `_missionSkillType` | Name |
|---|---|
| 0 | `Fight` |
| 1 | `Bomb` |
| 2 | `Recon` |
| 3 | `Transport` |
| 4 | `Maneuverability` |
| 5 | `Stealthiness` |

### Icons

Values for `_missionIcon`:

| Value | Use |
|---|---|
| `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability`, `Stealth`, `Luxury` | mission type icons |
| `Success`, `Failure` | result markers |
| `Cancel` | cancelled marker |

Note the spelling: the icon is `Stealth`, the skill type is `Stealthiness`.

### Location flags

Every place on the war map carries flags that describe it. They are a bitmask: add the numbers together (`10` = sea and enemy territory).

| Value | Flag |
|---|---|
| 0 | `None` |
| 1 | `Land` |
| 2 | `Sea` |
| 4 | `OwnTerritory` |
| 8 | `EnemyTerritory` |

The list of places, with their coordinates, is on the [Locations](locations.md) page. Copy the coordinates exactly: the game measures distance and fuel from the coordinates in your file, not from the name.

### Map tags

```json
"_tags": ["campaign_debden"]
```

A map lists the tags it supports in its `Metadata.json`, and a mission lists the tags it is written for. The mission can appear on a map only when the two lists share at least one tag (upper and lower case do not matter). An empty or missing list on either side counts as `["default"]`, and every built-in map supports `default`, so an untagged mission appears everywhere. Each built-in map also lists its own name (`debden`, `duxford`, `lichfield`, `perranporth`), so a mission tagged only `duxford` appears only on Duxford. See [Maps](../content/maps.md).

A mission tagged only `campaign_debden` appears only on maps that list that tag. A mission that should appear on your campaign map and everywhere else lists both: `["campaign_debden", "default"]`.

Tags are checked by the weekly draw, by the historic spawn and by `missions_api.CreateMission`. The `create_mission` cheat ignores them. Quests have no tags; a map chooses its quests differently (see [Quests](../quests/index.md)).

## Known pitfalls

| Problem | What you see | Fix |
|---|---|---|
| Not exactly 4 `_missionOutcomes` | crash when the mission ends | always 4, in index order |
| Fewer than 2 `_missionStats` | crash on the skill roll | always at least 2 |
| `.py` named differently from the `.json` | the script is ignored, the default runs | identical file names |
| Id already used by a built-in or another mod | one mission silently replaces the other | prefix ids with your mod name |
| A never-called handler implemented | nothing happens | delete it |
| `MaxVictoryPoints` in an outcome | crash when the mission ends | use `VictoryPoints` |
| `_coordinates` left at 0, 0 | the mission is placed far away, with a huge fuel cost | copy coordinates from [Locations](locations.md) |
| Old field `_mapTags` instead of `_tags` | map restriction silently lost | rename to `_tags` |
| Script-only mission without gates | appears anywhere once it has been created | `AddMissionRequirement` in `initialize_mission` |
