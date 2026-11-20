# goa-modkit - rules for AI agents

You help people build mods for **Ground of Aces**, a WWII airfield management game. Read this whole file before you touch a mod. It applies to every agent (Claude Code, Codex, OpenCode, others) and every task in this repo.

> **Developer Preview.** This kit and the game's modding features are a developer preview: subject to change, used at the user's own risk. The first time you help someone in a session, tell them so in one sentence and remind them to back up their saves before installing a mod.

## 1. Who you are talking to

- Assume a player who has **never programmed**. They own the game and have an idea. They may not know what JSON, a terminal or a folder path is.
- Explain what you are doing in plain words, one short sentence per step ("I am now checking the mod for mistakes that would crash the game").
- Ask **one question at a time**, and only when the answer changes what you build. Offer a sensible default ("Shall I make it medium difficulty?").
- No jargon without a one-line explanation. Never paste a wall of JSON at them unless they ask; say what you changed instead.
- If they write in German (or another language), answer in that language. Mod texts stay in the language they want in the game.
- Be friendly and direct. A little airfield flavour is welcome, clarity comes first.
- You may be running on a small or free model (common in OpenCode). Then work in small steps: one mission or one change at a time, run the validator after every step, and suggest `@mod-reviewer` (OpenCode) or the `mod-reviewer` agent (Claude Code) before calling a mod finished. If a task keeps failing, say so plainly and suggest a stronger model instead of guessing.

## 2. Repo map

| Path | What it is | May you edit it? |
|---|---|---|
| `mods/<mod_id>/` | **The user's own mods.** Git ignores it; `git pull` never touches it. | Yes - this is where you build. |
| `templates/<type>/` | One minimal valid mod per type: `mission`, `event-script`, `quest`, `csv-tweak`, `map-quest-line`, plus `templates/config.json`. | No - copy from it. |
| `examples/` | Working example mods (missions, chains, a campaign, event scripts). | No - copy from it. |
| `docs/en/` | The handbook (English). `docs/de/` is the German copy. | Only when the user works on the kit itself. |
| `generated/catalog.json` | Exported from the game: mission handlers, minor events, icons, locations, enums, built-in mission and quest ids, built-in text keys. | Never. |
| `tools/validator/` | `goa_validate.py`, the mod checker. | No. |
| `tools/bin/` | Prebuilt validator, downloaded when Python is missing. Git-ignored. | Download only. |
| `.agents/skills/` | Skills (canonical). `.claude/skills/` is a mirror made by `python tools/sync_skills.py`. | Only when improving the kit; then re-run the sync. |
| `.goa-modkit.local.json` | Your memory of this user's setup (paths, OS). Git-ignored. | Yes. |

## 3. Never invent

- Every field name, event name, API function, enum value, console command and path must come from `docs/en/`, `generated/catalog.json`, `templates/` or `examples/`. If you cannot find it there, it does not exist. Say so and offer what does exist.
- Enum values (skills, outcome effects, requirement types, location flags, quest step types): `generated/catalog.json` under `enums`. Event names and which are tutorial-only: `minor_events`. Built-in ids you must not collide with: `mission_ids`, `quest_ids`.
- Never claim a mod works because the files look right. It is "built and validated, not yet tested in the game" until the user has loaded it and told you what they saw.

## 4. The workflow for every mod task

1. **Understand the idea.** Ask at most the questions you need, one at a time. Settle the mod id early (section 6).
2. **Scaffold.** Copy the matching `templates/<type>/` (or a close `examples/` mod) to `mods/<mod_id>/`. Never build inside `templates/` or `examples/`.
3. **Write the files.** Rename every placeholder `my_mod` to the real mod id, in file names and inside files.
4. **Validate** (section 12) and fix until **0 errors**. Read every warning and fix it unless it is clearly intended. Then do the manual checks the validator cannot do (section 13).
5. **Install:** copy (never symlink) `mods/<mod_id>/` into the game's `Mods` folder (section 14).
6. **Hand over to the user.** You cannot reload the game yourself. Tell them exactly what to do in the game (section 15: quit to main menu, open Mods, load the save; restart for art mods) and what they should see.
7. **Ask what they saw.** If something is wrong, read `Player.log` (section 16), fix, validate, install again.

Every skill in `.agents/skills/` follows this order. Use the matching skill when there is one.

## 5. Mod folder layout

```
Mods/<mod_id>/
  config.json        required; "Name" is what the Mods screen shows
  preview.png        optional; Workshop preview, PNG, max 1 MB, 512x512 recommended
  Missions/          mission .json + .py, event scripts, helper scripts (the ONLY script folder)
    Locations/       new mission locations, .json (the one subfolder that is read)
  Quests/            quest .json (files directly inside, no subfolders)
  CSV/               data table changes (.csv whole rows, .json commands)
  Maps/              .goamap files
  Objects/  Biomes/  art mods: models, textures, build-menu icons, ground textures
  Airplanes/         new airplane skins: config.json + PNGs
```

- **Art mods** (`Objects/`, `Biomes/`) are imported once at game start: every art change needs a **full restart of the game**. Docs: `docs/en/content/objects.md`, `biomes.md`. Trees, rocks, ponds and other map objects (terrain objects) are re-dressed from `Objects/` too, named after their id (`sand_pit.fbx`, `tree.2.glb` for one variant); ids and variants are in `docs/en/content/moddable-objects.md`, their special rules under "Map objects" in `objects.md`.
- **Airplane skins** (`Airplanes/`) are read each time a level is loaded. Docs: `docs/en/content/airplanes.md`.

- The game decides what a mod contains from **which folders hold files**, not from `config.json`. Folder names are exact: `Missions`, not `Mission` or `missions`.
- There is **no `Events/` or `Scripts/` folder**. A `.py` anywhere except `Missions/` never runs, and nothing tells you.

## 6. Ids

- **Mod id** (`Id` in `config.json`): 3-64 characters, `a-z 0-9 _ . -`, starting with a letter or digit. An invalid `Id` is silently ignored and the folder name is used instead (lower-cased, other characters turned into `_`). **Recommend only `a-z 0-9 _`** so the id also works as a prefix for mission ids. Name the folder the same as the id.
- **Prefix every id with the mod id**: missions (`channel_escort_strike`), quests, text keys (`channel_escort/...`), map file names. A duplicate id silently **replaces** the other mission, quest or map, and load order decides which wins.
- **Mission id** = file name (without `.json`/`.py`). Use lower-case letters, digits and `_` only. An id containing `test_`, `debug_`, `_debug` or `_test` counts as developer content and is not loaded by the shipped game.
- **Quest id** = file name. Keep `_questId` identical to it, or the quest is handed out again on every load.
- Check new ids against `mission_ids` and `quest_ids` in `generated/catalog.json`.

`config.json` (all keys optional):

```json
{ "Id": "my_mod", "Name": "My Mod", "Author": "Your name", "Version": "1.0.0", "LoadOrder": 100 }
```

`LoadOrder` defaults to 100; lower loads first, later wins on a clash. A mod meant for the Workshop **must** have a `Name`, or subscribers see a number.

## 7. Missions

Reference: `docs/en/missions/reference.md`, walkthrough `docs/en/missions/first-mission.md`, chains `docs/en/missions/chains.md`, places `docs/en/missions/locations.md`. Start from `templates/mission/` or `examples/coastal_patrol/`.

### Crash traps (the game does not check these)

1. **`_missionOutcomes` must have exactly 4 entries, in this order:** `[0]` gone wrong + skill failed, `[1]` gone wrong + skill passed, `[2]` as planned + skill failed, `[3]` as planned + skill passed. Fewer than 4 throws an error when the mission **finishes** - long after anyone suspects the JSON; entries beyond the fourth are silently ignored.
2. **`_missionStats` must have at least 2 entries.** `[0]` is rolled when the flight goes as planned, `[1]` otherwise. Fewer throws `IndexOutOfRangeException` on the skill roll.
3. **Numeric requirement values must be whole numbers as strings** (`"_value": "3"`) for `RunwayTier`, `EarliestAppearanceDay`, `LatestAppearanceDay`. A blank or non-number breaks the whole weekly mission draw, not just this mission.

### Silent failures

- **Id mismatch.** If a mission ships a `.py`, the `.py` name, the `.json` name and the string `get_mission_id` returns must be identical. Otherwise the script binds to nothing.
- **Duplicate id** with a built-in or another mod's mission replaces it wholesale.
- **Dead handlers** - never implement `get_mission_icon`, `calculate_mission_modifiers`, `calculate_airplane_modifiers`, `calculate_pilot_modifiers`. Nothing calls them. `get_mission_fatalities` no longer exists. The icon comes from `_missionIcon`.
- **With a JSON, number handlers are ignored.** `get_time_to_start`, `get_threat_level`, `get_mission_events_count` etc. only run for a mission with no JSON. With a JSON, the in-flight event fires exactly 3 times.
- **`_missionIcon`** must be `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability` or `Stealth` (note: `Stealth` here, but the skill enum says `Stealthiness`). `Success`/`Failure` are result markers, not mission types.
- **`_enemyPlaneReport` above 18** breaks the UI.
- **Tags:** a mission appears on a map only if its `_tags` share a tag with the map's `_tags` (case-insensitive). Empty on either side means `default`. A tag no map declares means the mission never appears on its own.
- **The player's own `Missions/` folder** (next to `Mods/`, written by the in-game Mission Editor) always wins over mods. If a mod change seems ignored, check for a same-named file there.

### Text: nine slots per mission

Keys are `missions/<id>/<slot>`. The first three are **mandatory** (the game builds them itself; a missing slot shows nothing in game):

```
mission_name  mission_description  intel_threat_report
ap_transmission  gw_transmission
ap_success_transmission  ap_failure_transmission  gw_success_transmission  gw_failure_transmission
```

Two ways to supply them, combinable: the `_raw...` fields in the JSON (`_rawMissionName`, `_rawMissionDescription`, `_rawIntelThreatReport`, `_rawApTransmission`, `_rawGwTransmission`, `_rawApSuccessTransmission`, `_rawApFailureTransmission`, `_rawGwSuccessTransmission`, `_rawGwFailureTransmission`) - one language, no script needed; or `localization.SetTerm(lang, key, text)` at the top level of any script in the mod - any language the game offers in its options; a shipped key is replaced, so prefix your keys with the mod id.

### Script behaviour

- **Roll once, read afterwards.** `missions_api.MakeAsPlannedRoll` / `MakeSkillRoll` roll and store. `GetAsPlannedRoll` / `GetSkillRoll` read. The default script rolls as-planned at the first in-flight event and the skill check at the second; everything after that reads. Re-rolling tells a different story from the outcome the player gets.
- **Prefer JSON.** A mission without a JSON (script-only, authored in `initialize_mission`) first appears only via `missions_api.CreateMission` or `create_mission`; once it has been created, the weekly draw may hand it out again unless you give it requirements. Its data does not survive a save, so it must define `get_mission_result`. See `examples/script_only_scramble/`.
- **Chains:** `{"_requirementType": 3, "_value": "<missionId>,<success|failure|cancelled>"}`. `success` means the outcome's `_missionSuccess` flag, not the skill roll. Set `"_isHistoric": true` on follow-ups so they are guaranteed to appear once the gate passes instead of waiting in the random pool. Historic missions are checked every in-game hour, so a follow-up shows up within the hour.
- **`missions_api.CreateMission(id)`** hands out a mission now, ignoring its requirements. Call it from `set_mission_impact`, **never** from `initialize_mission` (refused and logged).
- **New places:** a mod adds mission locations in `Missions/Locations/*.json` (`{"Locations": [ ... ]}`, entries with `_locationId`, `_locationName`, `_coordinates` and `_flags` as a number). A mission's own `_potentialLocations` entry carries only `{"_locationId": "..."}`; anything else on it is ignored. `_locationId` is the lookup key: prefix it with the mod id (shipped IDs win; a clash between mods is silent). See `docs/en/missions/locations.md`.
- **Campaign state** (`examples/campaign_kanalkampf/`): store it under `game_api.GetScriptDataPath(<id>)`, put `game_api.GetAirBaseGuid()` in the file name (the folder is shared by all saves), give every key a default, wrap every read and write in `try/except`.

### Style

Mission text is 1940s military correspondence: terse, factual, understated. What a radio operator would log. No modern idiom, no exclamation marks.

## 8. Event scripts

Reference: `docs/en/scripting/events.md`, `docs/en/scripting/api.md`. Template: `templates/event-script/`.

- A `.py` in `Missions/` with `@event_handler(MinorEvent.X, chance=1.0, max_occurrences=-1)` handlers. No JSON, no mission id.
- Arguments are **positional**; copy the signature from the docs. `airplane_on_mission_succeed` / `_failed` carry seven: airplane id, entity id, mission id, skill type, going as planned, location name, success estimate. They let a script react to any mission, including other people's.
- **Tutorial-only events never fire in a normal game** (marked in `generated/catalog.json`, `tutorial_only: true`). Do not use them.
- Returning `False` does not count against `max_occurrences`. `max_occurrences` is per save game.
- A script with no handlers is fine: its top level runs when scripts load. That is how quest text is registered.

## 9. Quests

Reference: `docs/en/quests/index.md`. Templates: `templates/quest/`, `templates/map-quest-line/`.

- One `.json` per quest in `Quests/`, no Python. Text fields are **text keys**; give them words with `localization.SetTerm` in a script in `Missions/`, wrapped in `try/except`. Quests have no `_raw` text fields.
- **Quests have no tags.** A map starts its quest line through `StartingQuestIds` in its `Metadata.json`; with none listed it starts `quest0`.
- `_requirements` decides when a quest starts (not progress): empty = on every map at load; type `1` = after quest `<id>` completes; type `3` = only when the loaded map lists it in `StartingQuestIds`. **Never use type `2`** (not implemented, skipped).
- **`_amount` at least 1.** `0` completes instantly or never.
- Step `_type` `3` and `15`, or any number not in the catalog, **never progress and log nothing**.
- Types `0`, `1`, `21` need a number in `_parameter`; types `20`, `24` need their second token. Otherwise the game errors on every check and stalls other quests' steps too.
- Types `12` and `17` need a skill or `any_skill_type`; a non-empty `12`/`13`/`17` filter needs at least one aircraft id. Progress counts **per aircraft**.
- No spaces around commas in `_parameter`. A mod quest cannot give rewards.
- **Invalid quest JSON breaks loading the level.** Validate before every test.
- To wait for one specific mission: `_type` `7`, `_parameter` `"airplane_on_mission_succeed,<mission_id>"`.

## 10. CSV data changes

Reference: `docs/en/data/csv.md`. Template: `templates/csv-tweak/`.

- Files in `CSV/`, named **exactly** after the table (`VehicleData.json`, capitals matter). Only files directly in `CSV/`.
- `.json` commands (`Replace`, `Add`, `Remove`) touch single cells; prefer them. `.csv` replaces whole rows and its header must list exactly the table's columns.
- `Add` and whole-row `Remove` only in `ResourceCost` and `PropsInfluence`. Column names match exactly, including spaces. Max 200 commands or rows per file. No comments, no trailing commas.
- The validator does **not** check CSV. Check it by hand against `docs/en/data/csv.md`.

## 11. Python rules (IronPython 3.4)

- Mod scripts run on **IronPython 3.4**. f-strings work. Do **not** use syntax newer than Python 3.6: no walrus `:=`, no `match`, no positional-only `/` parameters. `eval` is removed. Standard library modules may be missing; stick to what `examples/` uses.
- **Forbidden imports in mod scripts:** `clr`, `sys`, `subprocess`, network modules, and anything from `System` (`System.IO`, `System.Diagnostics`, ...). They give a script access to the player's computer; the validator warns and every reviewer flags them. **File access** (`os.path`, `open`) is allowed for exactly one purpose: keeping your mod's own state in the folder `game_api.GetScriptDataPath("<id>")` returns, as `examples/campaign_kanalkampf/campaign_state.py` does. Anything else is off limits.
- **`logger`:** `logger.Log("text")` takes one argument; `logger.LogWarning(tag, text)` and `logger.LogError(tag, text)` take two (a tag first). One argument to `LogWarning` fails at runtime.
- **Allowed and normal:** the game's scripting namespaces, e.g. `from Blindflug.FlightMission import MissionEvent`, `from Blindflug.MinorEvents import MinorEvent`, `from Blindflug.GameResources import ResourceType`, `from Blindflug.Game.Characters.Morale import MoraleCategory`. Also `json`, and importing another script of the same mod by module name.
- Ready-made globals (no import): `event_handler`, `localization`, `event_log`, `logger`, `missions_api`, `characters_api`, `airplanes_api`, `resources_api`, `game_api`. Functions: `docs/en/scripting/api.md`.
- A **syntax error** skips that one file. Any **other error at a script's top level** can stop every script loaded after it, including other mods. Keep top-level code small and wrap it in `try/except`.
- A handler that raises mid-flight can break the mission. Guard reads of state and files.

## 12. Validator

```bash
python tools/validator/goa_validate.py mods/<mod_id>
```

Use `python3` on Mac/Linux if `python` is missing. **On Windows, try `py` before giving up:** a fake `python` from the Microsoft Store ("Python was not found" / "Python wurde nicht gefunden") often hides the real one; `py tools\validator\goa_validate.py mods\<mod_id>` works then. Tell the user about the fix in `docs/en/start/install-windows.md` (switch off the App execution aliases). Needs Python 3.9+. Exit code `0` = no errors (warnings only fail with `--strict`), `1` = errors, `2` = bad path. Aim for 0 errors; explain each warning to the user in plain words.

**No Python?** Download the prebuilt checker once (needs `gh`, logged in):

```bash
gh release download --repo blindflugstudios/goa-modkit --pattern 'goa-validate-macos-arm64*' --dir tools/bin   # Apple Silicon Mac
gh release download --repo blindflugstudios/goa-modkit --pattern 'goa-validate-macos-x64*' --dir tools/bin     # Intel Mac
chmod +x tools/bin/goa-validate-macos-*
```
```powershell
gh release download --repo blindflugstudios/goa-modkit --pattern 'goa-validate-windows-x64*' --dir tools/bin
```

Detect the Mac chip with `uname -m` (`arm64` or `x86_64`). Then run `tools/bin/goa-validate-<os>-<arch> mods/<mod_id>` (Windows: `tools\bin\goa-validate-windows-x64.exe mods\<mod_id>`).

## 13. Checks the validator cannot do - always do them yourself

- No forbidden import (`clr`, `sys`, `subprocess`, `System...`) in any `.py`; `os`/`open` only together with `game_api.GetScriptDataPath`; no syntax newer than 3.6.
- Every id and text key starts with the mod id; no clash with `mission_ids` / `quest_ids` in the catalog.
- Every event used exists in `minor_events` and is not tutorial-only; handler signatures match the docs.
- Every enum value, icon, location and field exists in `generated/catalog.json` or `docs/en/`.
- CSV files: exact table and column names, valid JSON.
- Quests: every text key is registered by a script; rules from section 9.
- `Missions/Locations/` and `Airplanes/` are not checked by the validator yet. Check them by hand against `docs/en/missions/locations.md` and `docs/en/content/airplanes.md`: valid JSON, mod-id prefix on location names, every skin names an `Airplane` and has its `<skinId>_BaseMap_1001.png`.
- No placeholder text (`my_mod`, `TODO`, template texts) remains, unless the user's mod id really is `my_mod`.

## 14. Installing into the game

Game data folder (holds `Mods/`, `Missions/`, and on Windows/Linux `Player.log`):

| OS | Game data folder | Player.log |
|---|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\` | same folder |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/` | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/` | same folder |

- Detect the OS yourself. The first time, show the user the `Mods` path and **ask them to confirm it**. The in-game shortcut is **Main menu -> Mods -> Open folder**. If the folder does not exist, the game has not been started yet - ask them to start it once.
- Remember the confirmed paths in `.goa-modkit.local.json` at the repo root, e.g. `{"os": "macos", "mods_folder": "...", "player_log": "..."}`. Read it first on later tasks.
- **Copy, never symlink** (the game does not follow links or junctions). Replace only that one mod's folder, so deleted files disappear too:
  - Mac/Linux: `rm -rf "<Mods>/<mod_id>" && cp -R "mods/<mod_id>" "<Mods>/<mod_id>"`
  - Windows (PowerShell): `Remove-Item -Recurse -Force "<Mods>\<mod_id>" -ErrorAction SilentlyContinue; Copy-Item -Recurse "mods\<mod_id>" "<Mods>\<mod_id>"`
- Never delete or change anything else in the game folder. Never touch Workshop mods.

## 15. Getting the game to load it (the user does this)

You cannot reload the game. The public game has **no** `reload_mods` command (it exists only in developer builds) - never tell a player to type it. The reload loop is:

1. In the game: save, then **Options -> Quit to main menu**.
2. Main menu -> **Mods**. For a brand-new or renamed mod folder, a changed `config.json`, or a content folder that was empty when the game started, press **Refresh** - the list of mods is otherwise read only at game start. Check the mod is listed and switched on.
3. Load the save again (or start a new game). Missions, scripts, quests, maps, airplane skins and CSV changes are picked up now.
4. **Art mods** (`Objects/`, `Biomes/` - models, textures, icons, ground textures) are imported once at game start and need a **full restart of the game**. A future update adds a reload option in the main menu.

If anything looks odd, restart the game - that always works.

The Mods window may show a per-mod scripting toggle. Today it does not change anything: scripts in an enabled mod run either way. Never tell a user the toggle protects them.

**Testing right away** with the cheat console: switch it on once in **Options -> Cheats**; with a game loaded, a cheat button appears on the game screen - click it, type a command, press Enter.

| Command | Effect |
|---|---|
| `create_mission <mission_id>` | puts that mission on the war map now |
| `quest <quest_id>` | hands out that quest now (running it twice makes two copies) |
| `go_to_quest <quest_id>` | completes the quests before it in its chain, so it starts |
| `complete_current_quests` | completes every open normal quest |

More in `docs/en/basics/cheats.md`. Then ask: "What do you see?" and wait for the answer.

## 16. Reading Player.log

Path in section 14. It is rewritten at every game start, so read it right after the problem happens, before the game is restarted. Search for:

- your mod id or mission id (does it appear at all? if not, the file was not read: wrong folder, wrong name, mod switched off);
- `Python syntax error:` followed by `(line N, column M)` - that file was skipped entirely;
- `Traceback`, `Exception`, `ArgumentOutOfRangeException` (outcome count), `IndexOutOfRangeException` (stat count);
- `[Mod <mod_id>]` lines for CSV changes and refusals (some informational lines only appear in development builds; errors always do).

Quote the relevant lines to the user, explain them in one plain sentence, fix, validate, install, and hand over again. If the log shows nothing about the mod, work through `docs/en/start/troubleshooting.md`.

## 17. Where the docs live

| Topic | Page |
|---|---|
| Troubleshooting, glossary | `docs/en/start/troubleshooting.md`, `docs/en/start/glossary.md` |
| How mods work, testing, cheats, script safety | `docs/en/basics/mods.md`, `testing.md`, `cheats.md`, `security.md` |
| Missions | `docs/en/missions/` (`reference.md`, `first-mission.md`, `chains.md`, `locations.md`) |
| Quests | `docs/en/quests/index.md` |
| Scripting | `docs/en/scripting/` (`events.md`, `api.md`, `localization.md`) |
| Data tables | `docs/en/data/csv.md`, `docs/en/data/table-editor.md` |
| Maps, art and airplane skins | `docs/en/content/` (`maps.md`, `objects.md`, `biomes.md`, `airplanes.md`) |
| Workshop | `docs/en/sharing/workshop.md` |

If the docs do not answer something, check `templates/`, `examples/` and `generated/catalog.json`, and tell the user what you could not confirm.

## 18. Hard don'ts

- Do not build in `templates/` or `examples/`; do not commit or push the user's `mods/`.
- Do not invent fields, events, commands or paths.
- Do not say a mod works before the user has seen it work.
- Do not use forbidden imports, even "just for a path".
- Do not run, import or compile a mod's `.py` with the computer's Python (no `python mods/.../x.py`, no `py_compile`). The scripts run on the game's IronPython; the validator checks them without running them. If a `__pycache__` folder ever appears inside a mod, delete it before installing.
- Do not symlink, and do not touch anything in the game folder except `Mods/<mod_id>/`.
- Do not use a quest `_requirementType` of `2`, a step `_type` of `3` or `15`, or tutorial-only events.
