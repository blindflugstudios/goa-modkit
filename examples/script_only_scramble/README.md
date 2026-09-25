# Example: Script-Only Scramble

A mission with **no JSON at all**. Everything a `.json` would declare is written from the script in `initialize_mission`.

## Files

| File | Contains |
|---|---|
| `script_only_scramble.py` | the whole mission: gates, stats, location, outcomes, text |

No `.json`, and none is needed. The file name and the string `get_mission_id` returns must still match.

## How it gets onto the map

A script-only mission never turns up by itself the first time: the weekly draw only considers missions whose data the game already knows. It appears when another script calls `missions_api.CreateMission("script_only_scramble")`, or when you type `create_mission script_only_scramble` in the cheat console.

## When this shape is worth it

Only when the values have to be **computed**. A file cannot express "harder each time the player flies it", and that is what this example does: the enemy count and the skill target both grow with the number of scrambles already flown, counted in the mission's own data folder via `game_api.GetScriptDataPath`.

For anything with fixed numbers, write the JSON. It is shorter, the validator can check it, and it survives saving and loading (see below).

## Two things a script-only mission must do

**Gate itself.** A script-authored mission starts with no requirements and no map tags. That matters more than it sounds: once the mission has been created for the first time the game *does* know its data, so the weekly draw stops skipping it, and with no gates it passes every check. Without `AddMissionRequirement` this mission would start appearing in the weekly draw on any map and any date.

```python
missions_api.AddMissionRequirement(mission_entity_id, "RunwayTier", "2")
missions_api.AddMissionRequirement(mission_entity_id, "EarliestAppearanceDay", "10")
missions_api.SetTags(mission_entity_id, "default")
```

**Define `get_mission_result`.** The authored data lives in memory only; it is not written to the save game. Load a save with this mission in flight and its outcomes are gone. The game then asks this handler for the result, and fails with an error if it is missing.

## What to look at

- **The eight getters are optional.** Each falls back to a default when it is missing, so a script may define only the ones it cares about. They run *before* `initialize_mission`, which is why base values and authored values are set in two places.
- **From the second creation on, the getters are not asked any more.** The game then builds the mission from the data authored the first time, like a JSON mission. That is why the script also registers `missions/script_only_scramble/intel_threat_report`: the threat line comes from that key then.
- **Order inside `initialize_mission`.** Gates first: everything else is cosmetic if the mission shows up where it should not.
- **Outcome order is mandatory:** 0 gone wrong + skill failed, 1 gone wrong + passed, 2 as planned + failed, 3 as planned + passed.
- **Rolls happen once.** `MakeAsPlannedRoll` and `MakeSkillRoll` roll; `GetAsPlannedRoll` and `GetSkillRoll` read that roll back. Re-rolling in the result handler would contradict the text the player already saw.
- **State is per save.** `GetScriptDataPath` gives one folder per id, shared by every save game, so the save's guid goes in the file name.

## Tested

Not yet tested in the game. The file passes the validator, and the calls it uses behave as described on the API page, but this specific mission has not been flown.
