# Example: Coastal Patrol

A minimal mission: JSON for the numbers, Python for the text. This is the shape to copy for your first mission.

## Files

| File | Contains |
|---|---|
| `coastal_patrol.json` | stats, locations, the four outcomes, timings, appearance gates |
| `coastal_patrol.py` | the nine texts, and which text appears in flight and in the result window |

Both file names, and the string `get_mission_id` returns, must match exactly.

## Installing it

Copy both files into the `Missions` folder of a mod:

```text
Mods/my_first_mod/Missions/coastal_patrol.json
Mods/my_first_mod/Missions/coastal_patrol.py
```

**Main menu → Mods → Open folder** takes you to `Mods/`. Load a save, then type `create_mission coastal_patrol` in the cheat console to see the mission straight away.

Before you ship your own version, rename the id (both file names and `MISSION_ID` in the script) with your mod name as a prefix, for example `mymod_coastal_patrol`.

## What to look at

- **The four outcomes are in mandatory order:** gone wrong + skill failed, gone wrong + skill passed, as planned + skill failed, as planned + skill passed. The `Name` of each outcome in the JSON says which slot it is.
- **Two mission stats, not one.** The first is rolled when the mission goes as planned, the second when it goes wrong. Fewer than two crashes the skill roll.
- **`MakeAsPlannedRoll` rolls, `GetAsPlannedRoll` reads.** Roll once, in the first in-flight step; everything afterwards reads. The skill roll works the same way.
- **All text is defined with `localization.SetTerm` at the top level of the script**, so it is registered when the script loads. Nothing has to be added to the game's translation files.
- **The locations carry their coordinates.** The game measures distance and fuel from the coordinates in the file, so copy them exactly from the locations list.

Walkthrough: the "Write your first mission" page of the modkit docs.

## Tested

Loaded and created in the game: `create_mission coastal_patrol` produced the mission at Dover with all four outcomes and both stats intact. Not yet flown to the end, so the outcome texts are not confirmed in a real flight.
