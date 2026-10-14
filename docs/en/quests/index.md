# Quests

A quest is a list of goals the player sees in the quest panel: *build an airstrip, order an aircraft, fly five missions*. Each goal (a **step**) is a counter that fills up as the player does the thing, and when every required step is full the quest is complete and the next one in the chain can start.

Quests are not missions. A mission is a flight whose outcome is decided by dice rolls; a quest is a checklist that watches the game and ticks boxes. A quest is a single `.json` file with nothing to "run", and the kinds of goals it can track are a fixed set built into the game - though a goal can point at your own content, such as a mission from your mod.

!!! note "No quest editor"
    Quests are written and changed in a text editor only. The Mission Editor does not open them, and the game does not check them before loading - the [checklist](#checklist-before-you-ship) near the end of this page is your check.

| Page | Contents |
|---|---|
| [Missions](../missions/index.md) | missions, and the events a quest can wait for when a mission returns |
| [Locations](../missions/locations.md) | the location flags a mission step can filter on (`sea`, `enemyterritory`, ...) |
| [CSV tables](../data/csv.md) | the data tables that hold the ids you use in quests - buildings, aircraft, resources, plants |
| [Example quests](#example-quests) | complete quest files to copy |

## Where quests come from

The game reads quests from two places, and the later one wins when both carry the same id:

1. **Shipped quests** - inside the game, read-only. You can override one by re-using its file name, but you cannot edit it in place.
2. **Mods** - `Mods/<your mod>/Quests/`, holding `.json` files. Only files directly inside `Quests/` are read; subfolders are ignored. Only *enabled* mods are read - a mod switched off in the Mods window contributes no quests.

Unlike missions, there is **no personal quests folder** outside a mod. To try a quest, put it in a mod folder ([How mods work](../basics/mods.md) explains where that folder is and how the Mods window works). The quests go into a `Quests` subfolder next to the other content types:

```text
Mods/
  my_campaign/
    config.json                  required - its "Name" is what the Mods screen shows
    Quests/
      mycampaign_first_steps.json
      mycampaign_first_patrol.json
    Missions/                    optional - mission files, and the .py that holds your quest text
    Maps/                        optional - the map that starts your quest line
```

Two rules follow from how the files are read:

- **The file name is the quest id.** `mycampaign_first_steps.json` is the quest `mycampaign_first_steps`, whatever the `_questId` field inside says. Keep the two identical: the game checks whether a quest already exists in the save by its *file name* but stores the *field* in the save, so if they differ the quest is handed out again every time the game loads, and chains (requirement type 1) refer to the field.
- **Prefix your ids with your mod name.** A file called `quest3.json` silently *replaces* the shipped `quest3`. Between two mods with the same file name, the one loaded later wins (see [Which mod wins](../basics/mods.md#which-mod-wins)).

!!! note "When changes show up"
    Quest files are re-read every time a level is loaded - return to the main menu and load again (loading a save is enough). A brand-new mod folder, or a `Quests/` folder that was still empty when the game started, needs **Refresh** in the Mods window first, or a restart.

## A first quest

This is a complete, working quest. Save it as `Mods/my_campaign/Quests/mycampaign_first_steps.json`, start the game, and load or start any map: it appears in the quest panel right away.

```json
{
    "_questId": "mycampaign_first_steps",
    "_questTitle": "mycampaign/first_steps/title",
    "_questDescription": "",
    "_subQuests": [
        {
            "_subQuestTitle": "mycampaign/first_steps/step0_title",
            "_subQuestDescription": "mycampaign/first_steps/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 7,
                "_parameter": "building_finished,Sickbed",
                "_amount": 1
            },
            "_genericIconKey": "ui_health"
        },
        {
            "_subQuestTitle": "mycampaign/first_steps/step1_title",
            "_subQuestDescription": "",
            "_isOptional": true,
            "_subQuestRequirement": {
                "_type": 4,
                "_parameter": "Bed",
                "_amount": 4
            },
            "_genericIconKey": "ui_bed"
        }
    ],
    "_requirements": [],
    "_isHiddenInUI": false,
    "_questType": 0
}
```

Reading it top to bottom: the quest has two steps. The first waits until a sickbed has been *finished* building - once. The second counts beds standing on the base and is full at four, but it is optional, so the quest completes as soon as the sickbed is done. `_requirements` is empty, which means the quest starts on every map that lists it in its `StartingQuestIds` - see [Quests and maps](#quests-and-maps).

The titles are **localization keys**, not text - until you register them, the player sees no title at all. The section [Text](#text) explains how to give them words.

## The file, field by field

| Field | Meaning |
|---|---|
| `_questId` | The quest's id. Keep it equal to the file name. |
| `_questTitle` | Localization key of the title shown in the quest panel. |
| `_questDescription` | Localization key of a longer text under the title. Leave `""` for none - shipped quests do. |
| `_subQuests` | The steps, in the order they are listed in the panel. At least one. |
| `_requirements` | When the quest is handed out - see [How a quest starts](#how-a-quest-starts). Not progress. |
| `_isHiddenInUI` | `true` hides the quest from the panel while it still runs. Used by the shipped skin-unlock quests. |
| `_questType` | `0` a normal quest, `1` an aircraft-skin quest. Use `0` - see [Quest types](#quest-types). |

Fields you leave out take their default: `false`, `0`, or empty. Extra fields (the shipped files carry a `"Name"` the game no longer reads) are ignored. There is no tags field: quests are tied to maps differently from missions, see [Quests and maps](#quests-and-maps).

Each entry of `_subQuests` is one step:

| Field | Meaning |
|---|---|
| `_subQuestTitle` | Localization key of the step's title. Also the name the game uses for the step (other quests can wait for it through `sub_quest_completed`). |
| `_subQuestDescription` | Localization key of the step's tooltip. `""` for none. |
| `_isOptional` | `true` - the quest can complete without this step. |
| `_subQuestRequirement` | *What* is counted: a `_type`, a `_parameter` and an `_amount`. Exactly one per step. |
| `_genericIconKey` | Which icon the step shows. See [Icons](#icons). |

And the requirement inside it:

| Field | Meaning |
|---|---|
| `_type` | A number picking the kind of condition - the full table is under [What a step can wait for](#what-a-step-can-wait-for). |
| `_parameter` | A comma-separated list whose meaning depends on the type. **No spaces** around the commas. |
| `_amount` | The count at which the step is complete. **At least 1.** |

!!! warning "`_amount` must be at least 1"
    A step with `_amount: 0` behaves inconsistently: depending on whether the quest was created while a save loaded or later in the running game, it either completes instantly or never completes - and in the second case, unless it is optional, it blocks its quest forever. If you want a step the map already satisfies (a "you are here" step), give it a real, already-true condition instead: `_type: 1`, `_parameter: "0"`, `_amount: 1` is complete as soon as the base has any parking spot.

### Text

Every text field of a quest is a **localization key** - a name the game looks up in its translation table when the panel is drawn. A key that is registered in no language is not shown at all: the quest card keeps the text it had before (a placeholder, or the text of the quest that last used that card) and the tooltip stays empty. Register every key.

Missions can carry their text directly in the JSON. **Quests cannot** - there are no raw-text fields, and a quest has no script of its own. You have two options:

**Reuse a shipped key.** The main-line quests already have translated titles for things like "Build an airstrip" or "Order an aircraft". Open the matching shipped quest and copy its key. This costs nothing and is translated into every language the game ships, but you are limited to sentences that already exist.

**Register your own keys from a script.** A `.py` file in your mod's `Missions/` folder runs when a level loads, for every enabled mod, and its top level can register terms:

```python
TERMS = {
    "mycampaign/first_steps/title":             "First steps",
    "mycampaign/first_steps/step0_title":       "Build a sickbed",
    "mycampaign/first_steps/step0_description": "Injured crew recover faster in a bed of their own.",
    "mycampaign/first_steps/step1_title":       "Build four beds",
}

try:
    for term, text in TERMS.items():
        localization.SetTerm("en", term, text)
except Exception as error:
    print("MyCampaign: could not register quest terms: %s" % error)
```

The file needs no mission handlers; it exists only to run this block. Put it in `Missions/`, not in `Quests/` - `Quests/` is read for `.json` only, and `Missions/` is the one folder the game loads scripts from. Call `SetTerm` once per language you want to support (`"de"`, `"fr"`, ...). A language you leave out shows the text of a language you did register, so always register `en`. The `try`/`except` matters: a syntax error skips only your script, but any other error at the top level of a script can stop the loading of every script after it - yours and other mods'.

Registering a key the game already ships - a building name, a shipped quest title - *replaces* the game's own text for that language. Prefix your keys with your mod name so this can never happen by accident. Shipped quests name their keys `quest/<questId>/title`, `quest/<questId>/subQuest0_title` and `quest/<questId>/subQuest0_description`; nothing enforces that shape for your quests. More on terms: [Localization](../scripting/localization.md).

### Icons

`_genericIconKey` picks the step's icon from a fixed set built into the game. A key the game does not know simply shows no icon; nothing is [logged](../start/troubleshooting.md#find-the-playerlog). There is no way to add your own icons from a mod.

| Kind | Keys |
|---|---|
| Base | `ui_path_runway`, `ui_runway`, `ui_path_cars`, `ui_functionarea_runway`, `ui_functionarea_parking`, `ui_functionarea_parking_1`, `ui_functionarea_parking_2`, `ui_functionarea_resources`, `ui_functionarea_safety`, `ui_functionarea_gardening`, `ui_hangar_roof`, `roof`, `wall`, `floor`, `door`, `house`, `ui_decoration_wall`, `ui_decoration_poster`, `ui_props_kitchen`, `ui_props_social` |
| Aircraft | `ui_plane`, `ui_plane_GlosterGladiator_MKI`, `ui_scramble`, `ui_aagun`, `ui_alarm`, `ui_radio` |
| Resources | `ui_resource_wood`, `ui_resource_planks`, `ui_resource_metal`, `ui_resource_bricks`, `ui_resource_cement`, `ui_resource_fuel`, `ui_resource_gunAmmo`, `ui_resource_repairParts`, `ui_resource_trash`, `ui_resource_rubble`, `ui_resource_victoryPoints`, `ui_seeds_beans`, `ui_harvesting`, `ui_tool_gathering`, `ui_fire` |
| Crew | `ui_crew_person_single`, `ui_crew_people_multiple`, `ui_crewjob_cook`, `ui_crewjob_medic`, `ui_health`, `ui_morale`, `ui_bed`, `ui_prop_bed`, `ui_prestige_full`, `Endurance` |
| Interface | `ui_camera`, `ui_move_tool`, `ui_pause`, `ui_speed_1`, `ui_speed_2`, `ui_speed_3`, `ui_timer_clock`, `ui_clock`, `ui_schedule`, `ui_eventlog`, `ui_notifications_all`, `ui_attention`, `ui_search_looking_glass`, `ui_lock_open`, `ui_headquarters`, `ui_stamp_headquarters_approved`, `ui_repairandcrafting`, `ui_cogwheel`, `ui_crown`, `ui_mark_exclamation`, `ui_assigned`, `ui_trash`, `plus` |
| Workbenches | `SawStation`, `FieldKitchen`, `IndoorKitchen`, `ElectronicsWorkbench`, `BrickStation`, `CementMixer` |
| Prop thumbnails | `PP0151_SickBed_thumbnail`, `PP1101_Bofors40mm_thumbnail`, `PP1002_SirenOnAPole_thumbnail`, `PP1006_LargeFuelTankWithConnector_thumbnail`, `PP1020_Flagpole5m_thumbnail`, `PP1030_Water_Pump_thumbnail`, `PP1000_RadioTower_thumbnail`, `PP0101_WoodenChair_thumbnail`, `PP0102_BarStool_thumbnail`, `PP0911_BarCounter_thumbnail`, `PP0956_DividerCurtains_thumbnail`, `BB0900_Sandbag1mStraightVarA_thumbnail`, `BB1300_Table1x2_thumbnail`, `Simple-Rack_thumbnail`, `GraveStoneWhite_thumbnail` |

`""` is fine and means no icon. When in doubt, copy the key from a shipped step that shows the picture you want.

## What a step can wait for

Each step has one requirement, and its `_type` decides what the game counts. There are two kinds:

- **Counted state (polled)** - every couple of seconds the game counts something on the base (airstrips, beds, storage zones) and writes the count into the step. The count can go *down* again if the player demolishes things, right up until the step completes.
- **Counted events** - the step adds one each time something *happens* (a building is finished, an aircraft returns from a mission). These never go down.

Progress is capped at `_amount`, and a completed step stays complete.

### All types at a glance

| `_type` | Name | Kind | Section |
|---|---|---|---|
| 0 | Airstrip | polled | [Building the base](#building-the-base) |
| 1 | Parking | polled | [Building the base](#building-the-base) |
| 2 | Airplane | polled | [Aircraft and missions](#aircraft-and-missions) |
| 3 | PropCategory | - does nothing | [Types that do nothing](#types-that-do-nothing) |
| 4 | Prop | polled | [Building the base](#building-the-base) |
| 5 | SimpleEvent | event | [Events](#events) |
| 6 | Workbench | polled | [Building the base](#building-the-base) |
| 7 | AnyAttributeEvent | event | [Events](#events) |
| 8 | AllAttributesEvent | event | [Events](#events) |
| 9 | FunctionArea (zone) | polled | [Building the base](#building-the-base) |
| 10 | ShelteredStorage | polled | [Building the base](#building-the-base) |
| 11 | TrashStorage | polled | [Building the base](#building-the-base) |
| 12 | SuccessfulMission | event | [Aircraft and missions](#aircraft-and-missions) |
| 13 | FlownMission | event | [Aircraft and missions](#aircraft-and-missions) |
| 15 | UnluckyMission | - does nothing | [Types that do nothing](#types-that-do-nothing) |
| 16 | TakePartInScramble | event | [Aircraft and missions](#aircraft-and-missions) |
| 17 | FailedMission | event | [Aircraft and missions](#aircraft-and-missions) |
| 18 | ScramblePlaneDestroyed | event | [Aircraft and missions](#aircraft-and-missions) |
| 19 | ScrambleToSafety | event | [Aircraft and missions](#aircraft-and-missions) |
| 20 | CoveredFunctionArea | polled | [Building the base](#building-the-base) |
| 21 | PlannedAirstrip | polled | [Building the base](#building-the-base) |
| 22 | CharacterJob | polled | [Crew](#crew) |
| 23 | QuestDismissed (button) | event | [A button on the quest card](#a-button-on-the-quest-card) |
| 24 | GardeningZone | polled | [Building the base](#building-the-base) |
| 25 | StorageAllResourcesEnabled | event | [Building the base](#building-the-base) |

There is no type 14.

### Building the base

| `_type` | Counts | `_parameter` |
|---|---|---|
| 0 | Finished, unobstructed airstrips of at least this tier | The tier as a number: `"1"` ... `"5"`. Required. |
| 21 | Airstrips at any stage - planned, under construction or finished - whose planned length, width and material all reach this tier | The tier as a number. Required. |
| 1 | Usable parking spots of at least this size | The size as a number; `"0"` is any parking spot. Required. |
| 4 | Finished props with one of these ids | Prop ids, e.g. `"Bed"` or `"Flagpole5,Flagpole10"`. Planned or unbuilt props do not count. |
| 6 | Usable workbenches with one of these ids | Workbench ids, e.g. `"SawStation"`, `"FieldKitchen"`. |
| 9 | Zones of a type, optionally of a size | `"<Zone>"`, or `"<Zone>,<min tiles>"`, or `"<Zone>,<min>,<max>"`. Zones: `Airstrip`, `Parking`, `SafetyZone`, `Storage`, `GardeningZone`. Example `"Storage,20"` - a storage zone of at least 20 tiles. |
| 20 | Zones whose *every* tile is covered by a given building | `"<Zone>,<building id>"`, optionally `,<min>,<max>` tiles. Example `"Storage,roof_tent"` - a storage zone entirely under tent roof. |
| 10 | 1 if at least one storage zone has floor **and** roof over every tile, else 0 | Leave empty. A size in here does not restrict which storage counts - it only decides whether the check runs at all. Use `_amount: 1`. |
| 11 | Storage zones that accept trash and rubble | Empty - any storage that lets trash and rubble in. `"true"` - only storages set up for *nothing but* trash and rubble. |
| 25 | Completes when every listed resource is allowed in at least one storage zone | Resource names, e.g. `"GunAmmo,AntiAirAmmo,PlaneBombs"`. Re-checked whenever the player changes a storage's settings or places a zone. Use `_amount: 1`. |
| 24 | Gardening zones growing a plant for a purpose | `"<plant>,<Seeds or Food>"`, optionally `,<min tiles>,<max tiles>`. Example `"beans,Food,10"`. Plant ids are those of the gardening data table. |

!!! warning "The one mistake that hurts other quests too"
    Types 0, 1 and 21 **must** have a number in `_parameter`, and types 20 and 24 **must** have their second part (the building id, the `Seeds`/`Food` purpose). Anything else - including an empty string - is an error inside the game every time the step is checked, and it stalls every other counted-state step that is checked in the same batch until the save is reloaded.

### Aircraft and missions

| `_type` | Counts | `_parameter` |
|---|---|---|
| 2 | Aircraft the player owns | One or more aircraft ids, comma-separated - `"spitfire"` or `"spitfire,hurricane"` - or empty for any aircraft. |
| 12 | Aircraft that returned from a *successful* mission | See below. |
| 13 | Aircraft that returned from any mission, won or lost | See below. |
| 17 | Aircraft that returned from a *failed* mission | See below. |
| 16 | Aircraft that took part in a scramble | Aircraft ids, or empty for any. |
| 18 | Enemy aircraft shot down during a scramble | Aircraft ids of the *defending* aircraft that scored, or empty for any. |
| 19 | Aircraft that scrambled to safety | Aircraft ids, or empty for any. |

Types 12, 13, 16, 17, 18 and 19 add one **per aircraft**, not per mission. A three-aircraft mission that succeeds adds three to a type-12 step. For "fly one mission", keep `_amount: 1` and accept that the step completes when the first aircraft is home.

**Filters for 12, 13 and 17.** An empty `_parameter` accepts every returning aircraft. Otherwise the list is read as a bag of words, and the aircraft must satisfy all of them:

| Word | Types | Meaning |
|---|---|---|
| an aircraft id - `spitfire`, `blenheim`, ... | all three | the returning aircraft must be one of the listed ids. **Required** whenever the list is not empty - a filter with no aircraft id in it matches nothing. |
| a skill - `fight`, `bomb`, `recon`, `transport`, `maneuverability`, `stealthiness` - or `any_skill_type` | 12, 17 | the mission was rolled on that skill. **One of these is required** for types 12 and 17. |
| `gone_wrong` | 12, 17 | only missions that did *not* go as planned |
| `location` followed by `land`, `sea`, `ownterritory` or `enemyterritory` | 12, 13 | the mission's location must carry every listed flag (see [Locations](../missions/locations.md#location-flags)) |
| `low_hp` | 13 | the aircraft came back with a quarter of its health or less |
| `high_success_rate` | 17 | the mission failed although the forecast was above 90 % |

Aircraft ids are the first column of the `VehicleData` table: `gladiator`, `hurricane`, `spitfire`, `meteor`, `mustangmk1`, `vampire`, `beaufighter`, `typhoon`, `tempest`, `kittyhawk`, `blenheim`, `hampden`, `stirling`, `lancaster`, `b17raf`, `mosquito`, `defiant`, `flamingo`, `lysander`.

Examples that work in a normal quest:

```text
"spitfire,hurricane,any_skill_type"                  type 12 - a Spitfire or Hurricane won any mission
"blenheim,bomb,location,enemyterritory"              type 12 - a Blenheim won a bombing mission over enemy land
"lysander,any_skill_type,gone_wrong"                 type 12 - a Lysander pulled through a mission that went wrong
"spitfire,low_hp"                                    type 13 - a Spitfire limped home
""                                                   type 13 - any aircraft flew any mission
```

!!! note
    The shipped skin-unlock quests write a role - `fighter`, `bomber`, `multirole` or `special` - where the aircraft id goes. That works **only** for `_questType: 1`, where the game makes one copy of the quest per matching aircraft and fills the real id in. In a `_questType: 0` quest a role name matches nothing - list the aircraft ids.

**Waiting for one particular mission.** Types 12, 13 and 17 cannot name a mission. Use type 7 with the mission's return event instead - see [Events](#events):

```json
{ "_type": 7, "_parameter": "airplane_on_mission_succeed,mycampaign_channel_sweep", "_amount": 1 }
```

This is how a quest follows a chain of your own missions, one step per mission.

### Crew

| `_type` | Counts | `_parameter` |
|---|---|---|
| 22 | Living, not heavily injured crew members with a job | One job: `RAFAircrew`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`, `AAFLabour`. |

### Events

Three types watch the stream of things that happen on the base (the game's minor events, listed in full on [Events](../scripting/events.md)). Each adds one per matching event - with one exception: `resource_gained` carries the number of units gained and adds that number, so `"resource_gained,Metal"` with `_amount: 20` means twenty metal, not twenty deliveries.

| `_type` | Adds one when... | `_parameter` |
|---|---|---|
| 5 | the named event fires, whatever its details | `"<event>"` |
| 7 | the named event fires and **any** of its details is one of the listed values | `"<event>,<value>,<value>,..."`. With no values listed, every occurrence counts. |
| 8 | the named event fires and **every** listed value is among its details | `"<event>,<value>,<value>,..."` |

Type 7 is the workhorse - "a specific building was finished", "a specific resource arrived":

```text
"building_finished,Sickbed"                          a sickbed finished building
"building_finished,Flagpole5,Flagpole10"             either flagpole finished
"building_type_finished,PropSocial"                  any social prop finished
"project_finished,SawStation.Planks"                 planks came off the saw station
"harvesting_finished,tree,tree_big"                  a tree was felled
"resource_gained,Metal"                              metal arrived by any route - harvest, workbench, delivery
"shipment_received,Bofors40mm"                       a shipment containing a Bofors gun arrived
"assigned_to_equipment,Bofors40mm"                   someone was posted to a Bofors gun
"airplane_on_mission_succeed,mycampaign_sweep"       your mission "mycampaign_sweep" came back a success
```

Type 8 narrows to combinations, and is rarely needed:

```text
"project_finished,SawStation,SawStation.Planks"      planks finished, and at a saw station
"harvesting_finished,bs_owen_m,tree"                 one particular crew member felled a tree
```

Type 8 has two limits type 7 does not have. It compares the listed values against the event's details as **text only**: details that are names (crew ids, building ids, project ids, mission ids) match, but details the game carries as numbers or as types - the resource of `harvesting_finished` and `resource_gained`, the category of `building_type_finished`, the zone of `function_area_placed` - never do. Use type 7 for those. And a type-8 step with listed values on an event that carries no details at all (`victory_points_added`, `quest_dismissed`) is an error every time that event fires. When one value is enough, use type 7.

Events available in normal play, with the details each one carries:

| Event | Details |
|---|---|
| `building_started`, `building_finished`, `deconstruction_finished` | worker, building id (e.g. `Sickbed`, `roof_concrete`, `wall_tent`) |
| `building_type_finished` | worker, building category (e.g. `PropSocial`, `PropPosters`) |
| `project_started`, `project_finished` | worker, workbench id, project id (as `SawStation.Planks`) |
| `harvesting_started`, `harvesting_finished` | worker, harvested object (e.g. `tree`, `tree_big`, `berry_bush`), resource |
| `resource_gained` | resource name |
| `resource_picked_up`, `resouce_consumed` | crew member, resource name (the second is spelt that way in the game) |
| `shipment_received` | the ids in the delivery |
| `victory_points_added` | - |
| `assigned_to_equipment` | crew member, equipment id |
| `training_started`, `training_finished` | crew member, training object |
| `task_started`, `task_completed` | crew member, task name (e.g. `Harvest`, `Build`, `Repair`, `RepairAirplane`, `Refuel`, `Recover`) |
| `chat_started`, `chat_finished` | the two crew members |
| `mission_started`, `mission_success`, `mission_failed` | the mission's location ID |
| `airplane_on_mission_succeed`, `airplane_on_mission_failed` | aircraft id, aircraft, **mission id**, skill, went-as-planned, location ID, forecast |
| `airplane_took_part_in_scramble`, `airplane_scramble_fly_to_safety`, `airplane_scramble_airplane_destroyed` | aircraft id |
| `plane_takeoff`, `plane_landing` | the aircraft's internal number (not its id - you cannot filter for `spitfire` here), pilot |
| `storage_resource_enabled`, `function_area_placed` | resource name / zone type |
| `day_phase_change` | previous phase, current phase |
| `midnight`, `midday` | year, month, day |
| `sub_quest_completed` | the completed step's `_subQuestTitle` key - a quest can wait for a step of another quest |
| `quest_dismissed` | - |
| `dog_sleep`, `dog_walk_started`, `dog_walk_finished`, `dog_sniff_wait` | the dog |

!!! warning "Tutorial-only events"
    A second group of events exists **only while the tutorial is running**: `camera_moved`, `camera_zoomed`, `camera_rotated`, `character_selected`, `task_created`, `tooltip_shown`, `preview_created`, `building_placed`, `state_entered`, `time_scale_changed`, `window_opened`, `character_job_assigned`, `day_phase_ended`, `plane_ordered`, `plane_selected`, `plane_assigned_to_mission`, `shipment_item_added`, `scramble_started`, `attack_finished`, `storage_resource_disabled`, `button_clicked`, `plane_back_from_mission`, `hour_changed`, `workbench_selected`, `project_planned`.

    Outside the tutorial they are switched off and a step waiting for one never moves. Prefer `building_finished` over `building_placed`, and `airplane_on_mission_succeed` over `plane_back_from_mission`.

### A button on the quest card

| `_type` | Completes when... | `_parameter` |
|---|---|---|
| 23 | the player clicks the button this step puts on the quest card | The localization key of the button label, e.g. `"basic_ui/ok"` or `"basic_ui/start"`. |

The button is drawn on the quest card of the quest that owns the step. Note that *any* such button on *any* quest advances every type-23 step that is currently open, so keep to one at a time. With an empty `_parameter` no button is drawn, but the step still completes when a button on another quest is clicked.

### Types that do nothing

`_type: 3` and `_type: 15` exist in old files but have no logic behind them; a step using either never progresses and nothing is [logged](../start/troubleshooting.md#find-the-playerlog). The same goes for any number outside the table. If a step sits at zero forever, check its `_type` first.

## How a quest starts

`_requirements` decides *when the quest is handed to the player*. It has nothing to do with progress. All entries must pass (they are combined with AND), and the check runs every time any quest completes - only quests with a type-1 entry are checked.

| `_requirementType` | Name | Meaning | `_value` |
|---|---|---|---|
| 0 | None | No condition. | `""` |
| 1 | CompletedQuestId | Start once the named quest is complete. | the other quest's id |
| 2, 3 | MinimumDate, MapDependent | **Removed.** The entry is skipped, so the quest behaves as if it were not there. Do not use them. | |

A quest reaches the player in one of three ways only:

- the loaded map lists it in its `StartingQuestIds` - see [Quests and maps](#quests-and-maps);
- it has a type-1 entry and the quest it names completes;
- it is an aircraft skin quest (`_questType: 1`), which is handed out on every map.

A quest with an **empty list** that no map lists never starts.

A **chain** is a series of quests, each requiring the one before it:

```json
"_requirements": [
    { "_requirementType": 1, "_value": "mycampaign_first_steps" }
]
```

A quest is handed out at most once per playthrough - once it exists in the save, complete or not, it is not created again, and a completed quest stays completed. A chain follows its first link: only the first quest needs to be in the map's list, the rest follow through requirement type 1, and on a map that does not list the first quest the whole chain stays away.

### Quests and maps

Every map names the quests it starts, in the `Metadata.json` inside its `.goamap` file:

```json
"StartingQuestIds": ["mycampaign_first_steps"]
```

Those quests are handed out when the map is loaded, whatever their `_requirements` say. A map that names none - an older map, or one whose field was left empty - starts the game's default quest line, `quest0`, so no map is ever without quests.

The shipped `quest0` has no requirements, and every later `questN` requires the one before it. So the moment a map lists *your* quest instead of `quest0`, the whole shipped main line stays away from that map - which is usually what a campaign wants. If you want both, list both: `["quest0", "mycampaign_first_steps"]`.

To make a quest belong to a map, put its id in that map's `StartingQuestIds` and leave its `_requirements` empty. No other map starts it.

!!! note "Missions use tags, quests do not"
    Missions are tied to maps through **tags** (the `_tags` field, see [Missions](../missions/index.md)). Quests are not: a quest has no tags field, and the map's `StartingQuestIds` list is the whole story. The two mechanisms are independent - a campaign map typically uses both, tags for its missions and `StartingQuestIds` for its quests.

**Editing the map's list in the game.** Open the map in the map editor and find the *Starting quest* field in the map settings, next to the tags. Type the quest ids separated by commas - `quest0, mycampaign_first_steps` - and save the map. Maps you save this way land in your `Maps` folder (next to the `Mods` folder); copy the `.goamap` into your mod's `Maps/` folder to ship it. A map that already lives inside a mod folder cannot be saved over from the editor - edit the copy in `Maps`, then replace the one in the mod. More on maps: [Maps](../content/maps.md).

**Editing it in a text editor.** A `.goamap` is an ordinary zip archive with a different file extension. Open it with any archive tool, edit `Metadata.json`, and put it back with the same name. Everything else in the archive stays as it is. `StartingQuestIds` sits at the end of the file, next to `_tags`; add the key if it is missing.

An id in the list that no quest file provides is skipped without a message in the released game; the map still loads.

## Changing a shipped quest

To change a quest the game ships with, drop a file with **the same name** into your mod's `Quests/`. Your copy replaces the shipped one entirely, so start from a full copy of the original and change what you need: an `_amount`, a `_parameter`, a step made optional, a step added or removed.

The shipped files are plain JSON inside the game's installation folder, under `Ground Of Aces_Data/StreamingAssets/Scripts/Quest/` (on macOS: `Ground of Aces.app/Contents/Resources/Data/StreamingAssets/Scripts/Quest/`) - `quest0` to `quest14` and the `*_skin_unlock` quests. Copy from there; never edit them in place, because a game update overwrites that folder. The shipped maps sit nearby in `StreamingAssets/Maps/`, which is also the place to look at a real `Metadata.json`.

Changes reach **existing saves** too. When a save is loaded, every quest already in it is compared with the current file: step titles, step descriptions, requirement types, parameters and amounts are updated in place, steps you added are appended, steps you removed are deleted, and a step whose progress already meets the new amount completes right away. Steps are matched **by position**, so inserting a step in the middle re-labels everything after it in a running save - append new steps at the end when a quest is already out in the wild. Not updated in a running save: the quest's own `_questTitle`, `_questDescription` and `_isHiddenInUI`, and a step's `_isOptional` and `_genericIconKey` - those are fixed when the quest is first handed out.

## Quest types

`_questType: 0` is a normal quest and the one you want. The other type exists for the game's own content and comes with strings attached.

**Aircraft-skin quests (`1`)** are created once per aircraft whose role or id appears in the first step's `_parameter`, and the aircraft's id is appended to every step's parameter. On completion they unlock a skin - but *which* skin is a table inside the game keyed by the shipped quest ids, so a new quest of this type unlocks nothing.

The same table is what makes completing `quest2` unlock new buildings: **rewards are not part of the quest file**. A mod quest cannot unlock a building, an aircraft or a skin. What it can do is *gate*: requirement type 1 chains quests behind each other, and a quest step can wait for a mission chain. The reverse is not available - a mission can be gated by map tags, runway tier, a day window or a *completed mission*, but not by a quest (see [Missions](../missions/index.md)).

## Example quests

Three complete quest files to open, copy and change. They live in the modkit repository as a small mod: [examples/quests](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/quests) (the files themselves are in its `Quests/` folder). Each one goes into `Mods/<your mod>/Quests/` under its file name; the titles are localization keys you give words to as described in [Text](#text).

| File | What it shows |
|---|---|
| `example_first_steps.json` | The quest from [A first quest](#a-first-quest): one required step waiting for a finished sickbed, one optional step counting beds. Starts on every map that lists it in `StartingQuestIds`. |
| `example_patrol_chain.json` | A follow-up quest. It starts once `example_first_steps` is complete, waits for a Spitfire to be owned, then for the shipped mission `calm_supply_drop` to come back a success, and optionally counts three winning sorties by Spitfires or Hurricanes. `calm_supply_drop` only appears from day 20 with a tier-3 runway, so the mission step cannot progress before that. |
| `example_map_campaign.json` | A quest that belongs to one map: it has no requirements, and only that map lists it in `StartingQuestIds` (see [Quests and maps](#quests-and-maps)). Its steps use the counted-state types: an airstrip of tier 1, two parking spots, a storage zone of twenty tiles. |

Install all three together and you have a two-quest chain plus a map-bound quest to compare against. Rename the ids before you build on them - `example_` is only a placeholder prefix.

Here is the chained quest in full:

```json
{
    "_questId": "example_patrol_chain",
    "_questTitle": "example/patrol_chain/title",
    "_questDescription": "example/patrol_chain/description",
    "_subQuests": [
        {
            "_subQuestTitle": "example/patrol_chain/step0_title",
            "_subQuestDescription": "example/patrol_chain/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 2,
                "_parameter": "spitfire",
                "_amount": 1
            },
            "_genericIconKey": "ui_plane"
        },
        {
            "_subQuestTitle": "example/patrol_chain/step1_title",
            "_subQuestDescription": "example/patrol_chain/step1_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 7,
                "_parameter": "airplane_on_mission_succeed,calm_supply_drop",
                "_amount": 1
            },
            "_genericIconKey": "ui_plane"
        },
        {
            "_subQuestTitle": "example/patrol_chain/step2_title",
            "_subQuestDescription": "",
            "_isOptional": true,
            "_subQuestRequirement": {
                "_type": 12,
                "_parameter": "spitfire,hurricane,any_skill_type",
                "_amount": 3
            },
            "_genericIconKey": "ui_plane"
        }
    ],
    "_requirements": [
        {
            "Name": "",
            "_requirementType": 1,
            "_value": "example_first_steps"
        }
    ],
    "_isHiddenInUI": false,
    "_questType": 0
}
```

And the map-bound one:

```json
{
    "_questId": "example_map_campaign",
    "_questTitle": "example/map_campaign/title",
    "_questDescription": "example/map_campaign/description",
    "_subQuests": [
        {
            "_subQuestTitle": "example/map_campaign/step0_title",
            "_subQuestDescription": "example/map_campaign/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 0,
                "_parameter": "1",
                "_amount": 1
            },
            "_genericIconKey": "ui_path_runway"
        },
        {
            "_subQuestTitle": "example/map_campaign/step1_title",
            "_subQuestDescription": "example/map_campaign/step1_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 1,
                "_parameter": "0",
                "_amount": 2
            },
            "_genericIconKey": "ui_functionarea_parking"
        },
        {
            "_subQuestTitle": "example/map_campaign/step2_title",
            "_subQuestDescription": "example/map_campaign/step2_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 9,
                "_parameter": "Storage,20",
                "_amount": 1
            },
            "_genericIconKey": "ui_functionarea_resources"
        }
    ],
    "_requirements": [],
    "_isHiddenInUI": false,
    "_questType": 0
}
```

## Shipped quests

The game's own quest files are worth reading too: they show what the real thing looks like. Find them in the installation folder as described in [Changing a shipped quest](#changing-a-shipped-quest). Remember that a mod file with the same name **replaces** the shipped quest, so rename your copy before you change it.

| File | What it shows |
|---|---|
| `quest0.json` | The first quest of the main line: no requirements, so it only starts on maps that list it in `StartingQuestIds` (or name no starting quest at all). Its steps are the counted-state types - an airstrip of tier 1, a parking spot, a Gladiator, beds. |
| `quest1.json` | The second quest, chained on `quest0` with requirement type 1. It mixes event steps (`harvesting_finished`, `project_finished`) with a workbench count, and has an optional step. |
| `fighter_day_skin_unlock.json` | An aircraft skin achievement: `_questType: 1`, hidden from the quest panel, and the only place where a role name (`fighter`) is allowed where an aircraft id normally goes - see [Quest types](#quest-types). |

## Testing a quest

Load a level again after every edit (a new folder needs **Refresh** in the Mods window first), then use the [cheat console](../basics/cheats.md):

| Command | Effect |
|---|---|
| `quest <id>` | Hands out the quest right now, whatever its requirements or map say. The console suggests loaded quest ids as you type - if yours is never suggested, the file was not read. Running it twice creates a second copy of the quest. |
| `complete_current_quests` | Completes every open normal quest, so the next links in a chain start. |
| `go_to_quest <id>` | Completes every quest the named one requires (through requirement type 1, following the chain back), so the named quest is handed out. It does not complete the named quest itself, and it works for mod quests too. |
| `start_shipment <Resource> <amount> ...` | Puts resources on the base - `start_shipment Wood 12`. |
| `create_mission <mission id>` | Puts a mission on the map to test a mission-return step. |

When a quest does not show up, or a step does not move, read the game's [log](../start/troubleshooting.md#find-the-playerlog) file `Player.log`.

- A quest file that is not valid JSON (a missing comma, an unclosed bracket) is **not** skipped - it breaks the loading of the level. Check your JSON in an editor before you test.
- A map that lists an unknown quest id, and a step that never progresses because of a wrong `_type` or a misspelt id, get **no** line in the [log](../start/troubleshooting.md#find-the-playerlog) - check the tables above.

More testing tips: [Testing and reloading](../basics/testing.md).

### Checklist before you ship

- Valid JSON: every `{` and `[` closed, a comma between entries and none after the last one.
- File name equals `_questId`, and both carry your mod's prefix.
- Every `_amount` is at least 1.
- Types 0, 1 and 21 have a number in `_parameter`; types 20 and 24 have their second part.
- Types 12 and 17 include a skill or `any_skill_type`; any of 12, 13, 17 that is not empty includes at least one aircraft **id**.
- No tutorial-only event.
- No `_requirementType: 2` or `3`.
- Every quest without a type-1 requirement is listed in the `StartingQuestIds` of each map it should run on.
- Every localization key is either a shipped key or registered by your script - load the game and look at the panel.
- No spaces inside `_parameter`.

## Saves and removing a mod

A quest that has been handed out lives in the savegame - name, progress and requirement - independently of your file. Saving and loading with the mod installed is uneventful. A quest you *add* in an update appears in existing saves the next time they are loaded, as long as its requirements pass.

**Remove the mod and the quest stays in the save**, still visible, frozen where it was. Nothing removes a quest because its file is gone, and the text your script registered goes away with the script, so the card shows the bare keys. Steps that wait for your missions can never move, because those missions no longer exist. Putting the mod back restores everything - text, progress, no duplicates.

For the player this means: a quest that can be finished leaves a tidy save behind; one that strands them halfway through a chain does not, and there is nothing they can do about it from inside the game. Prefer quests that reach an end, and treat removing a quest from a published mod as a breaking change for anyone in the middle of a playthrough.

## What a quest cannot do

- **Invent a new condition.** The types in the table are everything. If what you want to count is not there, it cannot be expressed - but a script can watch for it and hand out a mission, and a quest can wait for that mission's return.
- **Run logic.** No Python, no branching, no reading of game state beyond the counters above.
- **Show text without a key.** See [Text](#text).
- **Give a reward.** See [Quest types](#quest-types).
- **Reload inside a running level.** Changes show after the next level load.

For anything that has to *decide*, use a mission or an event script (see [Missions](../missions/index.md) and [Scripting](../scripting/index.md)) and let the quest report where the player has got to.
