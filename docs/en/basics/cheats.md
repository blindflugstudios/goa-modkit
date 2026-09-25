# Cheat console

The cheat console is a small command window inside the game. For modders it is the fastest way to test: create your mission right now instead of waiting days for it, jump to the quest you are working on, or skip ahead in time.

## Switch it on and open it

1. Load a save or start a game. The console only works while a game is running.
2. Open **Options** and switch on **Cheats**.
3. A cheat button appears on the game screen. Click it to open the console.

<!-- screenshot: Options window with the Cheats toggle, and the cheat button on the game screen -->

Type a command into the **Enter cheat...** field and press **Enter**. The answer appears above the field.

| Key | Does |
|---|---|
| **Enter** | Run the command |
| **Tab** | Complete the command name, and for many commands the next argument (mission ids, quest ids, resources ...) |
| **Up / Down** | Step through commands you typed before |

Type `help` for the full list with an example for each command, or `help create_mission` for one command. Command names are not case-sensitive.

!!! warning "Cheats change your save"
    Whatever a cheat does is saved with your game. Test mods on a spare save, not on your favourite campaign.

!!! note "Reloading your mod is not a console command"
    After changing a mod: **Options → Quit to main menu**, open **Mods**, then load your save. Quests are re-read too; only models and textures need a full game restart. See [Testing and reloading](testing.md).

## The commands

Arguments in `[brackets]` are placeholders: replace them, without the brackets. Commands marked ★ are the ones you will use most when testing mods.

### Missions and quests

| | Command | What it does | Example |
|---|---|---|---|
| ★ | `create_mission [mission_id]` | Creates that mission right away, so it shows up on the war map without waiting. Answers `Unknown mission ID` if the game did not load it. | `create_mission coastal_patrol` |
| ★ | `quest [quest_id]` | Starts the quest with that id. | `quest quest3` |
| ★ | `go_to_quest [quest_id]` | Completes quests one after another until that quest is reached. | `go_to_quest quest5` |
| ★ | `complete_current_quests` | Completes the running quests (not tutorial or skin quests). | `complete_current_quests` |
| | `enable_tutorial [true/false]` | Turns the tutorial on or off. | `enable_tutorial false` |
| | `set_game_goals_visibility [ShowAll/ShowPriority/Minimized]` | Changes how the goals panel is shown. | `set_game_goals_visibility ShowAll` |

### Time and days

| | Command | What it does | Example |
|---|---|---|---|
| ★ | `skip_day` | Jumps to the next day. Good for missions with a minimum day. | `skip_day` |
| ★ | `set_day [day of week] [hour] [minute]` | Moves to a day of the current week. | `set_day Friday` |
| | `go_to_day_phase [Work/Leisure/Sleep]` | Jumps to the start of the next day phase. This also freezes the clock: follow it with `freeze_time off`. | `go_to_day_phase Leisure` |
| | `force_day_phase [Work/Leisure/Sleep/off]` | Keeps the base in one day phase until you pass `off`. | `force_day_phase Work` |
| | `freeze_time [hour] [minute]` | Holds the time of day while days keep counting. `off` unfreezes. | `freeze_time 12 0` |

### Base, rank and unlocks

| | Command | What it does | Example |
|---|---|---|---|
| ★ | `list_airstrips` | Lists your airstrips and their ids. | `list_airstrips` |
| ★ | `set_airstrip_tier [airstrip_id] [tier]` | Sets one airstrip's tier. Missions can require a runway tier. | `set_airstrip_tier [id] 2` |
| ★ | `set_all_airstrips_tier [tier]` | Sets the tier of every airstrip. | `set_all_airstrips_tier 3` |
| ★ | `set_air_base_rank [rank]` | Sets the air base rank. | `set_air_base_rank 2` |
| | `set_victory_points [amount]` | Sets your victory points. | `set_victory_points 50` |
| | `unlock [id]` | Unlocks one entry by id. Tab suggests ids. | `unlock [id]` |
| | `unlock_all_skins` | Unlocks all airplane skins. | `unlock_all_skins` |
| | `add_resource_pile [resource] [x] [y] [true/false]` | Drops an endless pile of a resource at the mouse cursor, or at a map position. Pass `false` last for a normal pile. | `add_resource_pile Tarp 10 30 false` |
| | `start_shipment [type] [amount] ...` | Sends a delivery truck. Without arguments it brings the shipment set in the HQ window. | `start_shipment Tarp 20` |
| | `storage_blacklist_override [true/false]` | When on, storages block all resources by default. | `storage_blacklist_override false` |
| | `enable_crates_interaction [true/false]` | Allows or blocks harvesting and deconstructing crates. | `enable_crates_interaction true` |
| | `enable_equipment_deconstruction [true/false]` | Allows or blocks deconstructing equipment. | `enable_equipment_deconstruction true` |
| | `set_growing_time [hours] [x] [y]` | Sets the remaining growing time of a plant under the cursor or at a position. | `set_growing_time 1` |
| | `fill_grave` | Fills a random empty grave. | `fill_grave` |

### Planes

| | Command | What it does | Example |
|---|---|---|---|
| ★ | `spawn_plane [plane_id] [x] [y]` | Adds a new plane with a pilot. Without a position it comes in to land. | `spawn_plane [plane_id]` |
| | `set_airplane_fuel [0-100]` | Sets fuel. | `set_airplane_fuel 100` |
| | `set_airplane_health [0-100]` | Sets plane health. | `set_airplane_health 100` |
| | `set_airplane_integrity [0-100]` | Sets plane integrity. | `set_airplane_integrity 100` |
| | `destroy_airplane [airplane_id]` | Removes a plane. | `destroy_airplane [id]` |
| | `plane_fire` | Sets a random plane on fire. | `plane_fire` |
| | `spawn_plane_crash [airplane_id]` | Plays a crash for that plane. | `spawn_plane_crash [id]` |
| | `landing_queue_event [Wobbly/Overshoot/Smoked/Burning/Crash]` | The next arriving plane lands with that event. | `landing_queue_event Wobbly` |
| | `set_max_scramble_damage [amount]` | Caps the damage a scrambling plane can take. | `set_max_scramble_damage 10` |

### Crew and morale

| | Command | What it does | Example |
|---|---|---|---|
| ★ | `deliver_crew [count] [Male/Female]` | Sends a truck with new crew (default 2). | `deliver_crew 4` |
| | `spawn_character [role] [male/female] [true/false] [x] [y]` | Spawns a crew member at the cursor or a position. Role is an air crew role, or `none` for ground crew. | `spawn_character none female` |
| | `set_crew_morale [Confidence/Mood/Energy] [-100..100]` | Sets one morale value for everyone. With only a number, sets all values. `random` scatters them. | `set_crew_morale Confidence 100` |
| | `freeze_morale [true/false]` | Stops morale from changing. | `freeze_morale true` |
| | `set_morale_flag [add/sub] [flag] [character_id]` | Adds or removes a morale flag (happy, sad, angry ...) on one crew member. | `set_morale_flag add [flag] [id]` |
| | `set_crisis [Confidence/Mood/Energy] [character_id]` | Sends one crew member into a crisis: panic, rage or exhaustion. | `set_crisis Confidence [id]` |
| | `set_character_health [character_id] [health]` | Sets one crew member's health. | `set_character_health [id] 100` |
| | `set_invulnerable_characters [true/false]` | Crew take no damage. | `set_invulnerable_characters true` |
| | `injure_random_character [count]` | Badly injures random crew. | `injure_random_character 1` |
| | `character_fire [count]` | Sets random crew on fire. | `character_fire 1` |
| | `poison` | Gives random crew mushroom poisoning. | `poison` |
| | `destroy_character [name]` | Removes a crew member. | `destroy_character [name]` |
| | `spawn_dogs [count]` | Adds dogs at random spawn points. | `spawn_dogs 3` |

### Attacks, fire and damage

| | Command | What it does | Example |
|---|---|---|---|
| | `attack [severity]` | Starts a base attack now. Pass a severity, or an exact mix like `fighters=6 divers=4 bombers=3`. | `attack 3` |
| | `schedule_attack [day of week / +hours]` | Schedules a base attack for a day, or in a number of hours. | `schedule_attack +2` |
| | `show_grid` / `show_grid off` | Draws the attack grid (A1 to P16) on the ground. | `show_grid` |
| | `grid_info [square]` | Lists what is on the grid squares, or on one square. | `grid_info G6` |
| | `attack_square [square] [divers=] [bombers=]` | Attacks one grid square. | `attack_square G6 divers=3 bombers=2` |
| | `get_attack_severity` | Prints the current attack severity. | `get_attack_severity` |
| | `bomb [x] [y]` | Drops a bomb at a position or the cursor. | `bomb 20 40` |
| | `bomber_mode [true/false]` | Left click drops a bomb, right click a dive bomb. | `bomber_mode true` |
| | `explode [x] [y]` | Explosion effects at a position. | `explode 10 30` |
| | `explode_prop [build_id]` | Blows up a placed prop or workbench, for example `Kitchen`. | `explode_prop Kitchen` |
| | `fire [x] [y] [count]` | Starts fires at a position, at random places (count only), or at the cursor. | `fire 5` |
| | `disable_fires [true/false]` | Stops fires from starting and spreading. | `disable_fires true` |
| | `target` | Makes aiming planes target the thing under the cursor. | `target` |

### Map settings

These change the settings you choose when starting a map. The number is the setting's level.

| | Command | What it does | Example |
|---|---|---|---|
| | `attacks_rate_parameter [value]` | Attack frequency setting. | `attacks_rate_parameter 1` |
| | `change_attack_severity_parameter [value]` | Attack severity shift setting. | `change_attack_severity_parameter 1` |
| | `change_harvest_rate_parameter [value]` | Harvest rate setting. | `change_harvest_rate_parameter 1` |
| | `change_resource_degradation_rate_parameter [value]` | Resource decay setting. | `change_resource_degradation_rate_parameter 1` |
| | `explosion_damage_rate_parameter [value]` | Explosion damage setting. | `explosion_damage_rate_parameter 1` |
| | `hq_strikes_parameter [value]` | HQ requirement setting. | `hq_strikes_parameter 0` |
| | `set_random_event_chance [0-1]` | Base chance of random events. | `set_random_event_chance 0.5` |

### Debug views and technical

Use these only if you know why. `enable_system` and `enable_input_action` can leave a save in a strange state.

| | Command | What it does | Example |
|---|---|---|---|
| | `show_attack_heatmap` | Shows where attacks will aim. | `show_attack_heatmap` |
| | `show_voxel_owners` / `show_voxel_owners off` | Shows which object owns each tile. | `show_voxel_owners` |
| | `damage_debug [true/false]` | Visualizes explosion damage. | `damage_debug true` |
| | `set_target_fps [fps]` | Caps the frame rate. | `set_target_fps 30` |
| | `enable_input_action [map/action] [true/false]` | Turns one input action on or off. | `enable_input_action Game/TimeScalePause false` |
| | `enable_system [name] [true/false]` | Turns one internal game process on or off. | `enable_system [name] false` |

## A typical test run

```text
create_mission coastal_patrol
set_all_airstrips_tier 3
deliver_crew 4
skip_day
```

Create your mission, make sure the base meets its requirements, get enough crew, and move on a day to see what happens next.
