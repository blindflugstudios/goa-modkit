# Events

Events (the game calls them **minor events**) are the second way a script can hook into the game. They have nothing to do with owning a mission: they fire from life on the base (construction, crew, time of day, resources, planes coming and going), and any script can listen to them.

That makes them the tool for small stories: someone's patrol comes back shot up, a crew member has a bad night, mice get into the rations at midnight. The `event_script` example reacts to missions it did not write; see [Examples](../examples.md).

## A complete event script

Save this as `Mods/my_first_mod/Missions/mymod_quiet_night.py`. No JSON, no mission id, nothing else needed:

```python
from Blindflug.MinorEvents import MinorEvent

localization.SetTerm("en", "mymod/quiet_night",
                     "A quiet night. The duty officer reports nothing but owls.")


@event_handler(MinorEvent.MIDNIGHT, chance=0.02, max_occurrences=2)
def quiet_night(year, month, day):
    event_log.Create("mymod/quiet_night")
```

Event scripts live in the mod's `Missions/` folder, like mission scripts. It is a mod's only script folder; a script in any other folder never runs.

## The decorator

```python
@event_handler(event_name, chance=1.0, max_occurrences=-1)
def handler(argument1, argument2):
    ...
```

- `event_name`: which event, usually written as `MinorEvent.SOME_NAME` (import it with `from Blindflug.MinorEvents import MinorEvent`). The plain string, like `"midnight"`, works too.
- `chance`: the probability that the handler runs when the event fires, from 0.0 to 1.0. Default 1.0 (always).
- `max_occurrences`: how often the handler may run in one save game. The count is stored in the save, keyed by the handler's `<module>.<function>` name, so renaming either resets it. A negative value means no limit and is the default (`-1`); `0` means the handler never runs. The chance roll and the limit check both happen before the handler is called.

**Returning `False` does not count** against `max_occurrences`. Use it to check a condition and bail out without using up the budget. Returning nothing, `True` or any other value counts.

```python
@event_handler(MinorEvent.MIDNIGHT, chance=0.05, max_occurrences=2)
def midnight_mice(year, month, day):
    if resources_api.SpoilPile(ResourceType.FoodRations):
        event_log.Create("mymod/midnight_mice")
    else:
        return False    # nothing to spoil: try again another night
```

The count is stored per handler under the name `<file name>.<function name>`. Renaming either the file or the function starts the count again. Two handlers with the same function name in the same file share one count.

Several scripts may listen to the same event. Each handler is rolled and counted on its own.

## Arguments

The game passes arguments **by position**, in the order listed below. The names are only descriptions: call your parameters whatever you like, but take the right number of them, or the call fails.

- Ids of characters, buildings, workbenches and so on arrive as strings.
- Ids of planes and dogs (`...EntityId`, `voxelObjectId`) arrive as numbers. These are the numbers `airplanes_api` and `resources_api` expect.
- Values like a resource type or a day phase arrive as game values you can compare directly: `if resource == ResourceType.MilitaryConstruction:`. Turn them into text with `str(value)`.

Useful imports for comparing:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Game.Characters.Morale import MoraleCategory
from Blindflug.DayPhases import DayPhase
```

### Missions and flights

| Event | Arguments |
|---|---|
| `mission_started` | `locationName` |
| `mission_success` | `locationName` |
| `mission_failed` | `locationName` |
| `airplane_on_mission_succeed` | `airplaneId, airplaneEntityId, missionId, skillType, isGoingAsPlanned, locationName, successEstimate` |
| `airplane_on_mission_failed` | same seven |
| `plane_takeoff` | `airplaneEntityId, characterId` |
| `plane_landing` | `airplaneEntityId, characterId` |
| `airplane_took_part_in_scramble` | `airplaneId, airplaneEntityId` |
| `airplane_scramble_fly_to_safety` | `airplaneId, airplaneEntityId` |
| `airplane_scramble_airplane_destroyed` | `airplaneId` |
| `victory_points_added` | none |

The seven-argument pair is the most useful hook in the whole system: it fires once for every plane that comes back from **any** mission, including ones you did not write. `airplaneId` is the plane's type name, `airplaneEntityId` the number to pass to `airplanes_api`, `skillType` the rolled skill as text (`"Fight"`), `isGoingAsPlanned` `True` or `False`, and `successEstimate` the success chance in percent the player was shown (0 if none).

`plane_takeoff` and `plane_landing` fire once per crew member aboard, each time with that person's id.

`mission_success` and `mission_failed` fire for missions whose outcome comes from outcome data (every mission with a JSON file). A script-only mission that decides its result with `get_mission_result` does not fire them.

### Time

| Event | Arguments |
|---|---|
| `midnight` | `year, month, day` |
| `midday` | `year, month, day` |
| `day_phase_change` | `previousPhase, newPhase` (day phases: `DayPhase.Work`, `DayPhase.Leisure`, `DayPhase.Sleep`) |

### Crew

| Event | Arguments |
|---|---|
| `chat_started` | `characterId, targetCharacterId` |
| `chat_finished` | `characterId, targetCharacterId` |
| `training_started` | `characterId, trainingObjectId` |
| `training_finished` | `characterId, trainingObjectId` |
| `assigned_to_equipment` | `characterId, propId` |
| `task_started` | `characterId, taskType` |
| `task_completed` | `characterId, taskType` |

### Construction and economy

| Event | Arguments |
|---|---|
| `building_started` | `characterId, buildingId` |
| `building_finished` | `characterId, buildingId` |
| `building_type_finished` | `characterId, buildType` |
| `deconstruction_finished` | `characterId, buildingId` (or the id of the terrain object that was cleared) |
| `project_started` | `characterId, workbenchId, projectId` |
| `project_finished` | `characterId, workbenchId, projectId` |
| `resource_picked_up` | `characterId, resourceType` |
| `resource_gained` | `resourceType` |
| `resouce_consumed` | `characterId, resourceType` |
| `harvesting_started` | `characterId, harvestableId, resourceType` |
| `harvesting_finished` | `characterId, harvestableId, resourceType` |
| `shipment_received` | a variable number of shipment ids, one argument each |
| `function_area_placed` | `functionAreaType` |
| `storage_resource_enabled` | `resourceType` |

Notes:

- `resouce_consumed` is spelled with the missing `r`. That is the real event name; `MinorEvent.RESOURCE_CONSUMED` gives you the right string.
- `resource_gained` carries an amount that quests read, but a script only receives the resource type.
- `harvesting_started` and `harvesting_finished` fire only for resource containers, not for crates.
- `building_type_finished` does not fire for buildings without a type.
- For `shipment_received`, write the handler as `def on_shipment(*shipment_ids):` so it accepts any number of arguments.

### Quests

| Event | Arguments |
|---|---|
| `sub_quest_completed` | `subQuestName` (the text key of the sub-quest's title) |
| `quest_dismissed` | none |

### Dogs

| Event | Arguments |
|---|---|
| `dog_walk_started` | `voxelObjectId` |
| `dog_walk_finished` | `voxelObjectId` |
| `dog_sleep` | `voxelObjectId` |
| `dog_sniff_wait` | `voxelObjectId` |

## Tutorial-only events

25 events fire only while the tutorial is switched on. In a normal game they never reach a script, so they are no use for content mods. They are listed here so you do not wonder why your handler stays silent:

| Event | Arguments |
|---|---|
| `camera_moved` | none |
| `camera_zoomed` | none |
| `camera_rotated` | none |
| `character_selected` | `characterId` |
| `task_created` | `taskType` (as text), `targetId` |
| `tooltip_shown` | `id` |
| `preview_created` | `buildingId` |
| `building_placed` | `buildingId` |
| `state_entered` | `stateName, argument` |
| `time_scale_changed` | `timeScale` (as text) |
| `window_opened` | `windowId` |
| `character_job_assigned` | `jobName` |
| `day_phase_ended` | `endedPhase` |
| `plane_ordered` | `airplaneId` |
| `plane_selected` | `airplaneId` |
| `plane_assigned_to_mission` | `airplaneId` |
| `shipment_item_added` | `shipmentId` |
| `scramble_started` | none |
| `attack_finished` | none |
| `storage_resource_disabled` | `resourceType` |
| `button_clicked` | `id` |
| `plane_back_from_mission` | `airplaneEntityId` |
| `hour_changed` | `hour` (0–23) |
| `workbench_selected` | `workbenchId` |
| `project_planned` | `projectId, repetitionCount` (as text) |

## Writing to the event log

```python
event_log.Create("mymod/pilot_tired", {"PILOT": str(character_id)})
```

The first argument is a text key, the second fills `{[NAME]}` placeholders in that text. A character written as `[character:{[PILOT]}]` in the text becomes a clickable name. How to define the text, and the other inline tags, is on the [Localization](localization.md) page. All of `event_log` is on the [API](api.md#event_log) page.
