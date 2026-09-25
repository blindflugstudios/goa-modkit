# Example: Event Script

An event script owns no mission. It listens to minor events, the game's second scripting hook, and reacts to whatever happens at the base or in the air, including missions written by other people.

## Installing it

```text
Mods/my_first_mod/Missions/convoy_reactions.py
```

No JSON, no matching file names, no `get_mission_id`: the game runs every script it finds in the folder and the handlers register themselves.

`Missions/` is not a typo. It is a mod's **only** script folder. There is no `Events/` folder for mods, and a script placed in one never runs, without any warning.

## What to look at

- **`airplane_on_mission_succeed` and `airplane_on_mission_failed` carry seven arguments:** plane type, plane number, mission id, skill type, the as-planned flag, location name and the success estimate the player was shown. That is enough to react to a specific mission, a specific location, or a specific kind of disappointment, without owning any of it.
- **`return False` does not count against `max_occurrences`.** Both mission handlers here bail out early on the wrong location or the wrong estimate, so the budget is only spent on calls that actually produced something.
- **`chance` and `max_occurrences`** keep a reaction from becoming wallpaper. `quiet_night` fires at most twice in a playthrough, at 2% of midnights.

## Useful events for small stories

| Group | Events |
|---|---|
| Missions | `mission_started`, `mission_success`, `mission_failed`, `airplane_on_mission_succeed`, `airplane_on_mission_failed` |
| Flight | `plane_takeoff`, `plane_landing`, the scramble events |
| Time | `midnight`, `midday`, `day_phase_change` |
| Crew | `chat_finished`, `training_finished` |
| Quests | `sub_quest_completed` |

Every event with its arguments is on the Events page of the modkit docs. 25 events fire only in the tutorial and never in normal play.

## Tested

Confirmed in the game: placed in a mod's `Missions/` folder, the handlers load and fire like the game's own event scripts, and the script's terms resolve to their text. The same file in an `Events/` folder never ran.
