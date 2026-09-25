---
name: read-log
description: Read the Ground of Aces Player.log and explain in plain words why a mod misbehaves. Use when the user says "it does not work", "nothing happens", "my mission does not show up", "the game crashed", "texts look like missions/...", "look at the log", "read my Player.log".
---

# Read the Player.log

## 1. Find the log

Use `player_log` from `.goa-modkit.local.json` if present. Otherwise:

| OS | Player.log |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

The game rewrites it on every start (the previous run may be in `Player-prev.log` next to it). Ask the user **not to restart** before you have read it, and to tell you roughly what they did and what they saw. Ask before reading a file outside the repo if your tool needs permission.

The file can be large. Search it rather than reading it all (`grep -n` on Mac/Linux, `Select-String` in PowerShell).

## 2. Search for

| Search for | Meaning |
|---|---|
| the mod id, mission id, quest id | Nothing at all: the game did not read the file - wrong folder, wrong file name, mod switched off, or the game was not reloaded (main menu, Mods, load again; art needs a restart). |
| `Python syntax error:` ... `(line N, column M)` | That script was skipped completely. Open it at that line. Often syntax newer than Python 3.6 or a typo. |
| `Traceback`, `Exception`, `Error` near the mod's names | A script failed while running. The last lines name the file, line and error. |
| `ArgumentOutOfRangeException` when a mission ends | `_missionOutcomes` does not have exactly 4 entries. |
| `IndexOutOfRangeException` at the skill roll | `_missionStats` has fewer than 2 entries. |
| `[Mod <mod_id>]` | CSV changes accepted or refused, with the reason. Informational lines may only appear in development builds; refusals and errors are the ones to look for. |

## 3. Symptoms without a log line

| Symptom | Usual cause |
|---|---|
| Text shows as `missions/<id>/mission_name` | That text key was never defined (typo, or the script did not run). |
| Mission never appears | Gates: `RunwayTier`, `EarliestAppearanceDay`, a chain predecessor, or `_tags` not shared with the map. Test with `create_mission <id>`. |
| Quest step stays at 0 | Step `_type` 3/15/unknown, tutorial-only event, misspelt id, spaces in `_parameter`. |
| Quest shows no title | Text script not in `Missions/`, or it failed; or the level was not loaded again after the change. |
| Change seems ignored | Old copy installed, the player's own `Missions/` folder next to `Mods/` has a same-named file, or the game was not reloaded. |

More in `docs/en/start/troubleshooting.md`.

## 4. Fix and hand over

Quote the one or two relevant log lines, explain them in a plain sentence, fix the file in `mods/<mod_id>/`, run `validate`, then `install-mod`, and ask the user to try again.
