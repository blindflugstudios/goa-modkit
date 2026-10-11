# API

Everything a mod script can call. Eight objects are available in every script without an import, plus the decorator `event_handler`:

| Name | Purpose |
|---|---|
| `event_handler` | the decorator that registers a handler, see [Events](events.md#the-decorator) and [Missions](../missions/reference.md#handlers) |
| `event_log` | write lines to the in-game event log |
| `localization` | define or override text |
| `missions_api` | mission state, dice rolls, authoring missions from a script |
| `characters_api` | crew morale, health, state |
| `airplanes_api` | plane health, integrity, fuel, pilot |
| `resources_api` | spawn and spoil resources |
| `game_api` | save-game identity and a folder for your own files |
| `logger` | write debug lines to [`Player.log`](../start/troubleshooting.md#find-the-playerlog) |

Names of game values come from imports:

| Import | Used for |
|---|---|
| `from Blindflug.FlightMission import MissionEvent` | mission handler names, `MissionEvent.SEND_MISSION_EVENT` |
| `from Blindflug.MinorEvents import MinorEvent` | event names, `MinorEvent.MIDNIGHT` |
| `from Blindflug.MinorEvents import EventLogType` | the look of an event log line |
| `from Blindflug.GameResources import ResourceType` | resource types, `ResourceType.FoodRations` |
| `from Blindflug.Game.Characters.Morale import MoraleCategory` | `MoraleCategory.Mood`, `.Confidence`, `.Energy` |
| `from Blindflug.Game.Characters.Morale import CharacterMoraleStateFlag` | temporary morale states |
| `from Blindflug.DayPhases import DayPhase` | `DayPhase.Work`, `.Leisure`, `.Sleep` |

Mod scripts run on IronPython 3.4. Avoid syntax newer than Python 3.6 (`:=`, `match`), and stick to the standard library modules the examples use (`json`, `os`). Mod scripts can import each other by file name when they sit in the same `Missions/` folder.

## event_log

```python
event_log.Create(loc_key, parameters=None, event_log_type=EventLogType.Default)
```

Writes one line to the event log. `loc_key` is a text key (see [Localization](localization.md)). `parameters` is a dictionary that fills `{[NAME]}` placeholders in that text; all values must be strings.

```python
event_log.Create("mymod/pilot_returned", {"PILOT": str(character_id)})
```

Characters written as `[character:<id>]` in the text become clickable names, and are linked to the log line.

`event_log_type` changes how the line looks: `EventLogType.Default`, `EventLogType.Warning`, `EventLogType.Error` or `EventLogType.Success`.

## localization

```python
localization.SetTerm(language_code, key, text)
```

Defines a text for one language, or replaces it. Call it at the top level of your script so the text exists as soon as the script loads. The [Localization](localization.md) page explains keys, languages, placeholders and what happens when your mod is removed.

## missions_api

Mission state and dice rolls. Every call takes the `mission_entity_id` your handler received.

| Call | Returns |
|---|---|
| `GetMissionId(id)` | the mission's id (its file name), or `None` if the mission no longer exists |
| `GetMissionAirplaneFormation(id)` | the numbers of the planes assigned to the mission |
| `GetEnemyCount(id)` | reported enemy planes |
| `IsMissionSuccessful(id)` | whether the mission succeeded; meaningful from `set_mission_impact` on |
| `GetNumberOfEventsSent(id)` | how many in-flight steps have fired, counting the current one |
| `MakeAsPlannedRoll(id)` | **rolls** whether the mission goes as planned, stores and returns it |
| `GetAsPlannedRoll(id)` | reads that roll back |
| `MakeSkillRoll(id)` | **rolls** the squadron's skill check, stores and returns it; the crew gains experience on a pass |
| `GetSkillRoll(id)` | reads that roll back |
| `CreateMission(mission_id)` | puts another mission on the war map now, see below |

**Roll once, read afterwards.** `Make...` performs a roll; `Get...` reads it. Make the as-planned roll before the skill roll: the skill roll uses it to pick which of the two mission stats to roll against. Rolling twice gives the player one story and a different outcome.

`GetMissionId` exists because many missions share one script: a handler cannot tell from the file name which mission it is running for, so it asks. The shared default mission script uses it to build its text keys.

### Creating a mission

```python
missions_api.CreateMission("mymod_airfield_pursuit")
```

Puts a mission on the war map immediately, skipping the weekly draw. Returns `True` if a mission was created.

It still checks the target mission's own requirements and its map tags. If either fails, nothing is created, it returns `False`, and a warning naming the mission is written to [`Player.log`](../start/troubleshooting.md#find-the-playerlog). It also returns `False` for an unknown id. A script-only mission that has never been created has nothing to check yet and is always allowed.

Call it from `set_mission_impact`, where the outcome is known. From `initialize_mission` it is refused and [logged](../start/troubleshooting.md#find-the-playerlog), because that handler runs in the middle of creating a mission.

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
    else:
        missions_api.CreateMission("mymod_regroup")
```

When the condition is simply "the previous mission succeeded", a JSON requirement is better: `"_requirementType": 3` with `"<id>,success"`, no script at all. See [Chains and campaigns](../missions/chains.md).

### Authoring a mission from a script

These calls write what a mission's JSON would otherwise declare. A script-only mission needs them, because nothing else sets its stats, location or outcomes. Call them from `initialize_mission`.

| Call | Sets |
|---|---|
| `SetMissionStat(id, skill, min, max)` | one skill's target range. `skill` is `"Fight"`, `"Bomb"`, `"Recon"`, `"Transport"`, `"Maneuverability"` or `"Stealthiness"`. The first skill you set is rolled when the mission goes as planned, the second when it does not. Setting the same skill again replaces its range. |
| `SetAsPlannedChance(id, chance)` | 0–100. Default for a script-only mission: 50. |
| `SetMissionLocation(id, location_id)` | places the mission on the war map and works out distance and fuel. `location_id` is the ID of a shipped place from [Locations](../missions/locations.md) or of one an enabled mod adds, never coordinates. |
| `SetMaxAirplaneSlots(id, slots)` | how many planes may be assigned, at least 1. Default: 1. |
| `SetDifficulty(id, rating)` | the star rating, 1–3. Default: 1. |
| `SetOutcome(id, index, is_success)` | whether outcome `index` (0–3, in the [mandatory order](../missions/reference.md#the-two-rolls-and-the-outcome-index)) counts as a success |
| `AddOutcomeEffect(id, index, type, value)` | adds an effect to outcome `index`. `type` is `"CrewMood"`, `"CrewConfidence"`, `"CrewEnergy"`, `"Damage"`, `"BaseMood"`, `"BaseConfidence"`, `"BaseEnergy"` or `"VictoryPoints"`. `value` is a whole number like `"-40"`, or a range like `"70-140"` for `Damage`. |
| `AddMissionRequirement(id, type, value)` | one appearance gate. `type` is `"RunwayTier"`, `"EarliestAppearanceDay"`, `"LatestAppearanceDay"` or `"CompletedMission"`. Gates combine with AND. |
| `SetTags(id, tag, ...)` | which maps the mission belongs to, like `_tags` in JSON. Replaces what was set before. |

All of them return `True` on success and `False` when the mission, the index or a name is unknown. None of them raises an error, so check the return value while developing.

Do not use `"MaxVictoryPoints"` with `AddOutcomeEffect`. It is accepted, but crashes the mission when it ends.

A script-only mission starts each creation with its effects and requirements cleared, so `initialize_mission` can add them every time without piling up duplicates. On a mission that has a JSON file, the calls change the loaded file data for the rest of the session instead: effects and requirements you add accumulate with every copy of the mission. Adjust stats and chances there if you like; add effects and gates only in script-only missions.

### Gating a script-only mission

Without gates, a script-only mission appears anywhere once it has been created the first time: the weekly draw now knows its data, and with no requirements it passes every check. Set them in `initialize_mission` alongside the rest:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    missions_api.AddMissionRequirement(mission_entity_id, "RunwayTier", "2")
    missions_api.AddMissionRequirement(mission_entity_id, "EarliestAppearanceDay", "14")
    missions_api.AddMissionRequirement(mission_entity_id, "LatestAppearanceDay", "40")
    missions_api.AddMissionRequirement(mission_entity_id, "CompletedMission", "mymod_convoy_spotted,success")
    missions_api.SetTags(mission_entity_id, "campaign_debden")
```

`CompletedMission` takes `"<missionId>"`, or `"<missionId>,success"`, `",failure"` or `",cancelled"` to require a particular outcome. Day numbers count from the start of the campaign.

Tags work like `_tags` in JSON: the mission can appear only on maps that share one of its tags. Leaving tags unset means `"default"`, which every built-in map supports. That is right for a mission meant to appear anywhere, and wrong for one that belongs to a single campaign. See [Map tags](../missions/reference.md#map-tags).

## characters_api

Character ids are strings, as they arrive in event arguments or from `airplanes_api.GetPilot`. Several calls come in two forms: one for every character, one for a single character.

| Call | Effect |
|---|---|
| `GetMorale(character_id, category)` | read one morale value |
| `SetMorale(category, value)` | set for **everyone** |
| `SetMorale(character_id, category, value)` | set for one character |
| `ModifyMorale(category, delta)` | change for **everyone** |
| `ModifyMorale(character_id, category, delta)` | change for one character |
| `TriggerEffect(character_id, category)` | trigger that character's breaking-point reaction for that category, as if the morale had bottomed out; returns whether the character was found |
| `SetTemporaryMoraleState(character_id, state, duration)` | put a character into a temporary state, see below |
| `ModifyHealth(character_id, delta, notify=True)` | change health; with `notify=True` the player gets the usual health notification |
| `HealthEventsBlocked()` | `True` while the game protects a young base from health events, see below |
| `SetFire(character_id, fires)` | set a character on fire, with `fires` fires around them |
| `GetPilotMissionCount(character_id)` | missions flown |
| `GetPilotSuccessfulMissionCount(character_id)` | missions won |
| `DestroyCarriedResource(character_id)` | destroy what they carry; returns whether there was something |
| `DropCarriedResource(character_id)` | drop what they carry; returns whether there was something |
| `GetVoxelObjectId(character_id)` | the number of the character's object in the world, for `resources_api.SpawnNextTo`; 0 if not found |

Morale runs from -100 to 100. `category` is `MoraleCategory.Mood`, `MoraleCategory.Confidence` or `MoraleCategory.Energy`.

`SetTemporaryMoraleState` takes a `CharacterMoraleStateFlag`: `Happy`, `Sad`, `Injured`, `Sick`, `Exhausted`, `Fearful`, `Angry`, `Panic`, `Collapse`, `Rage` or `HeavilyInjured`, and a duration.

`HealthEventsBlocked()` returns `True` during the first days of a campaign while a member of the ground crew is already hurt, so a young base is not hit twice. A script that hurts someone should check it first and `return False` if it is set:

```python
@event_handler(MinorEvent.TASK_COMPLETED, chance=0.01, max_occurrences=1)
def twisted_ankle(character_id, task_type):
    if characters_api.HealthEventsBlocked():
        return False

    characters_api.ModifyHealth(character_id, -10)
    event_log.Create("mymod/twisted_ankle", {"CHARACTER": str(character_id)})
```

## airplanes_api

Planes are identified by number: the values `missions_api.GetMissionAirplaneFormation` returns, and the `airplaneEntityId` arguments of events.

| Call | Returns or does |
|---|---|
| `GetPilot(airplane_id)` | the character id of the first crew member |
| `GetAirplaneHealth(airplane_id)` | health as a fraction, 0.0–1.0 |
| `SetAirplaneHealth(airplane_id, value)` | set health in points (whole number), limited to the plane's maximum |
| `AddAirplaneHealth(airplane_id, value)` | change health by that many points; negative values damage |
| `GetAirplaneIntegrity(airplane_id)` | structural integrity as a fraction, 0.0–1.0 |
| `GetAirplaneParkingLot(airplane_id)` | the number of the plane's parking spot; raises an error if it has none |
| `ReduceAirplaneFuel(airplane_id, fuel)` | burn fuel; a plane that runs dry is missing in action |

For damage caused by a mission, prefer the `Damage` outcome effect in the JSON. It also handles injuries to the crew.

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    for airplane_id in missions_api.GetMissionAirplaneFormation(mission_entity_id):
        pilot = airplanes_api.GetPilot(airplane_id)
        characters_api.ModifyMorale(pilot, MoraleCategory.Energy, -10)
```

## resources_api

| Call | Effect |
|---|---|
| `SpawnNextTo(voxel_object_id, resource_type, amount)` | drop a pile of resources on the nearest free spot beside an object |
| `SpoilPile(resource_type)` | spoil one pile of that resource |

Both return `True` or `False`. `SpoilPile` fails when there is nothing to spoil, which is a natural moment for `return False` in an event handler. Get a `voxel_object_id` for a character with `characters_api.GetVoxelObjectId`; dog events deliver one directly.

```python
from Blindflug.GameResources import ResourceType

resources_api.SpawnNextTo(characters_api.GetVoxelObjectId(character_id), ResourceType.FoodRations, 2)
```

## game_api

| Call | Returns |
|---|---|
| `GetAirBaseGuid()` | a unique id for the current save game |
| `GetScriptDataPath(id)` | a folder your script may read and write |

`GetScriptDataPath` creates the folder `Scripts/<id>` inside the game data folder if needed, and returns its path. It is the supported way to keep your own data across sessions. `id` may contain only letters, digits, `_`, `-` and `.`, up to 64 characters; anything else raises an error.

Two things to know:

- The folder belongs to the **id**, not to one mission. Several missions that want to share state must use the same id.
- It is **not per save game**. Put `GetAirBaseGuid()` in your file name so separate saves do not overwrite each other.

```python
import os

def _path():
    return os.path.join(
        game_api.GetScriptDataPath("mymod_campaign"),
        "campaign_{}.json".format(game_api.GetAirBaseGuid())
    )
```

This is what makes a campaign possible: a mission can ask how many raids have been lost, who won the first one, or what the player chose two missions ago. [Chains and campaigns](../missions/chains.md#from-a-chain-to-a-campaign) has the full pattern and the three ways to get it wrong.

## logger

Writes to [`Player.log`](../start/troubleshooting.md#find-the-playerlog).

```python
logger.Log("mymod: campaign state loaded")
```

Use `event_log` for anything the player should see; `logger` is for you, while debugging. Prefix your lines with your mod name so you can search for them.

## What is not available

- `eval` is removed from the scripts' built-in functions.
- The handlers `get_mission_icon` and `calculate_*_modifiers` are never called, so there is no way to add success modifiers from a script. Change stats and chances with the authoring calls above instead.
