# Testing and reloading

There is no preview window for mods. You test a mod by loading it into the game and watching what happens. This page shows how to make that loop short: change a file, reload, look, without restarting the game.

## The short version

1. Edit your files in the mod folder.
2. In the game, save, then **Options → Quit to main menu**.
3. Open **Mods** from the main menu. The window rescans the `Mods` folder when it opens; **Refresh** rescans it again.
4. Load your save. Missions, scripts, quests and CSV tables are read fresh every time a save is loaded. Only art needs a full restart.
5. For a mission, open the cheat console and type `create_mission <your_mission_id>` to put it on the war map right now.
6. Something wrong? Open `Player.log` (see [below](#reading-playerlog)).

## Reloading without restarting the game

Every time you load a save, the game reads your mod's content again: mission files, Python scripts, quests and CSV tables, from the game itself and from every enabled mod. So the edit loop is: change a file, go back to the main menu, open **Mods**, load the save again.

Two things need more:

- **Art is imported only when the game starts.** Models, textures and other files in `Objects/`, `TerrainObjects/` and `Biomes/` need a full restart of the game.
- **New mods**: a mod folder you just created shows up after the Mods window has rescanned (open it, or press **Refresh**). Check that the mod is switched on.

A mission that was already on the war map in your save keeps the values it was created with. After changing a mission's JSON, create a fresh copy with `create_mission` to see the change.

## Making a mission appear now

Missions are drawn randomly across the week, so waiting for a specific one is slow.

```text
create_mission mymod_coastal_patrol
```

puts the mission on the war map immediately. The cheat console needs a loaded game: switch it on under **Options → Cheats**, then use the cheat button on the game screen (see [Cheat console](cheats.md)). It ignores the mission's requirements, date gates and map tags, so it proves the mission **loads and flies**, not that it would appear on its own. The console suggests mission ids as you type.

If the answer is `Unknown mission ID`, the game has not read your files: see the checklist below. If it is `Mission ... has neither mission data nor a script`, the file was found but could not be used, usually a script-only mission without a `get_mission_id` handler.

Other cheats that help while testing missions:

| Command | Use |
|---|---|
| `skip_day` | jump to the next day; historic missions with a date are checked at every day change |
| `freeze_time off` | if the clock stopped (some cheats freeze time as a side effect) |

The full list is on the [Cheat console](cheats.md) page.

### Testing a chain

`create_mission` skips every gate, so it cannot show that a chain unlocks. To test the unlocking:

1. Lower the gates for the test: `RunwayTier` 1 and `EarliestAppearanceDay` 1 remove the two most common reasons a mission never shows up.
2. Make the follow-up historic (`"_isHistoric": true`). Historic missions skip the random draw and appear at the next weekly slot, or on their date, as soon as their gates pass.
3. Fly the first mission to the outcome you are testing and wait for the next slot.

Remember that a historic mission is one-shot once it has been won. Turn `_isHistoric` off again afterwards if the mission is not meant to be a story beat.

## When nothing shows up

Work down this list before you start doubting your logic.

**1. Is the file in the right place?**
Mission files, event scripts and helper modules all go into `Mods/<your_mod>/Missions/`. There is no `Events/` or `Scripts/` folder for mods; a script placed anywhere else never runs, silently. The extension must be exactly `.py` or `.json` (watch out for `coastal_patrol.json.txt` when your system hides extensions).

**2. Is the mod enabled?**
A mod switched off in the Mods window is not loaded at all. A mod folder you created while the game was running appears after the Mods window has rescanned.

**3. Did the script load?**
Every script that loads successfully is listed in `Player.log` with its file name, followed by the handlers it registered. If your file name is missing, the game did not read it.

**4. Is there a syntax error?**
A Python syntax error shows up in `Player.log` as:

```text
Python syntax error: <message> (line N, column M)
```

The whole file is then skipped; nothing in it registers. Mods run on IronPython 3.4: stick to the Python features the [examples](../examples.md) use, and avoid anything newer than Python 3.6 (`:=`, `match`).

**5. Did the JSON parse?**
A broken mission file is skipped with this line in `Player.log`:

```text
Mission file at <path> could not be parsed, skipping it: <reason>
```

A missing comma or an extra one at the end of a list is the usual cause.

**6. Do the names match?**
The `.py` file name, the `.json` file name and the id `get_mission_id` returns must be identical. With a mismatch, the game runs the default script instead of yours.

**7. Is the id already taken?**
A mission with the same id as a built-in mission, or as one in another mod, replaces it (or is replaced by it). Rename yours with a prefix.

**8. Are the gates passing?**
A mission only enters the pool when all its requirements pass. Check `RunwayTier` against your base, `EarliestAppearanceDay` against the day of the campaign, `CompletedMission` against what has actually been flown, and `_tags` against the map. A chain step additionally needs its predecessor finished with the right outcome.

## The two crashes worth knowing

Both come from checks the game does not make, so there is no friendly message:

- **Not exactly four `_missionOutcomes`:** the mission crashes when it finishes, long after you stopped suspecting the JSON.
- **Fewer than two `_missionStats`:** the mission crashes on the skill roll, in the middle of the flight.

If a mission flies but blows up at the end, count the outcomes first.

## Checks you can run before launching

Everything below can be checked without starting the game, and is worth doing after every edit. The validator does all of it for you (see [Without an AI agent](../start/without-ai.md)):

- the JSON parses
- exactly 4 outcomes, in the order: gone wrong + failed, gone wrong + passed, as planned + failed, as planned + passed
- at least 2 mission stats
- `_missionIcon` is one of `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability`, `Stealth`, `Luxury`, `Success`, `Failure`, `Cancel`
- `_enemyPlaneReport` is 18 or lower
- `.py` and `.json` share a name, and `get_mission_id` returns that name
- the id does not duplicate an existing mission id
- every text key the script writes follows `missions/<id>/<slot>`
- no never-called handler is implemented (`get_mission_icon`, `calculate_*_modifiers`)

A clean validator run means the mod is well-formed, not that it plays well. Only a flight in the game tells you that.

## Where text goes missing

If the mission appears but shows a raw key like `missions/mymod_patrol/mission_name` instead of a name, that text was never defined. The game builds three keys itself and expects them to exist:

```text
missions/<id>/mission_name
missions/<id>/mission_description
missions/<id>/intel_threat_report
```

They cannot be renamed. Define them with `localization.SetTerm`, or fill the matching `_raw*` fields in the JSON (see [Localization](../scripting/localization.md)). The other six keys are used by your own script, so a typo there shows up as a raw key in the event log rather than in the mission window.

## Reading Player.log

The game writes everything it notices into a text file called `Player.log`. It is rewritten each time the game starts, so look at it while the game is running or right after closing it.

| Platform | Location |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

Open it with any text editor and search for your mod name or mission id. Your own scripts can write to it with `logger.Log("...")`, see [API](../scripting/api.md#logger).
