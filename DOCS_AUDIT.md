# Docs audit 2026-09-28

Comparison of the modkit handbook (`docs/en/`, `docs/de/`, `AGENTS.md`, skills, templates) with the game team's docs in
`SquadronLeader_Demo/Docs` (state of 2026-09-28, commit 35f391ddab). **The game docs are treated as correct.**
"SRC" = `SquadronLeader_Demo/Docs`.

What was done with each finding:

- **Fixed** - a wrong statement, reworded to match SRC.
- **Hidden** - a section or page that describes something that no longer exists. Hidden pages are in
  `exclude_docs` in `mkdocs.yml`; hidden passages are wrapped in `<!-- OUTDATED (docs audit 2026-09-28) ... -->`
  so they can be restored or rewritten later.
- **Open** - SRC contradicts itself or the game code, or SRC trimmed something that is still true. Needs a decision
  by the game team, left unchanged.
- Things SRC simply does not mention (unverifiable) are listed at the end and left unchanged.

Art mods (Objects, Biomes, the former TerrainObjects) are **work in progress and not supported by the current alpha**.
Every page and skill about them now carries a notice saying so.

---

## 1. Art mods (Objects, TerrainObjects, Biomes)

SRC `Modding/mods.md` 59-78 describes a new layout:

- `Objects/` is one flat pool of models and textures. A model's **file name** is the object id (`Chair.fbx`,
  `Chair.destroyed.fbx`, `tree.2.glb`); subfolder names mean nothing (`Objects/Chair/model.fbx` is an object
  called `model`). Textures are found by the name the material references (`Objects/wood-01.png`).
  `Chair.thumbnail.png` (max 256x256) replaces the build-menu icon. Settings live in one `Objects/config.json`
  keyed by id: `{"Objects": {"Chair": {"UseGameMaterial": false}}}`; a `config.json` in a subfolder is ignored.
- `Biomes/` holds one PNG per slot, named by the slot number (`8.png`), directly inside the folder.
- **There is no `TerrainObjects/` folder any more.** Trees, rocks etc. are re-dressed from `Objects/`.
- Art is imported once at startup: restart needed; neither Refresh nor the Enabled switch re-imports it.

| Where | Problem | Action |
|---|---|---|
| `content/terrain-objects.md` (whole page) | Describes the removed `TerrainObjects/` folder | Hidden (page excluded, nav entry removed) |
| `content/objects.md` (almost whole page) | Per-object subfolders, `model.glb`/`albedo.png`/`destroyed.glb` names, per-folder `config.json`, no thumbnails, `TerrainObjects` cross-refs, folder-path log lines | WIP notice; outdated parts hidden |
| `content/biomes.md` | `Biomes/<name>/albedo.png` instead of `Biomes/<slot>.png` | WIP notice; outdated parts hidden |
| `basics/mods.md` 10, 47-49, 58-60, 68 | Lists `TerrainObjects/`; "Biomes = biome definitions" (SRC: ground textures, one PNG per slot); "each object gets its own subfolder" | Fixed / hidden, WIP notice |
| `basics/mods.md` 106 | Enabled switch: art missing, art needs a restart | Fixed |
| `basics/mods.md` 141-146 | "Seeing your changes" table has no art row | Fixed |
| `basics/testing.md` 20, `start/glossary.md` 77, `index.md` 61, `content/maps.md` 45 | Mention `TerrainObjects` / link to the hidden page | Fixed |
| `ai/skills.md` 21, `.agents/skills/import-model`, `.agents/skills/install-mod` 53 | `TerrainObjects/`, old layout | WIP notice / fixed |
| `AGENTS.md` 59, 225, 263 | `TerrainObjects/`, terrain-objects page | Fixed, WIP note |

## 2. Mods basics, testing, start pages, Workshop

| Where | Modkit says | SRC says | Action |
|---|---|---|---|
| `index.md` 68, `basics/mods.md` 132, 138, 145, `basics/testing.md` 9, 21, 64, `start/index.md` 56, `start/first-mod.md` 71, 107, `start/without-ai.md` 105, 109, `start/troubleshooting.md` 28, `content/maps.md` 21, `CONTRIBUTING.md` 64, `AGENTS.md` 223, `templates/quest/README.md` 24 | Opening the Mods window rescans the Mods folder | The list of mods is read once at startup; a new mod folder needs **Refresh** in the Mods window (or a restart) (mainpage 35, mods.md 149-158, quests.md 63-64) | Fixed |
| `basics/mods.md` 13 | Every change is picked up at the next level load | Art needs a restart (mods.md 160). *SRC mainpage 36 has the same simplification* | Fixed |
| `basics/mods.md` 125-128, `content/maps.md` 157 | Maps: shipped, then your own `Maps` folder, then mods | Your own `Missions`/`Maps` folders are read after every mod and win over all (mods.md 144-145) | Fixed |
| `basics/mods.md` 89 | Author/Version "kept for you and anyone reading the file" | "kept for you and for the Workshop page; the game does not read them" | Fixed |
| `basics/mods.md` 114, `start/first-mod.md` 72 | Scripting switch only on mods with Python, asks to confirm | Switch on every mod, reserved for a coming opt-in, no effect (mods.md 126) | Fixed (confirm dialog left: unverifiable) |
| `basics/security.md` 18 | "The game asks before you turn on scripting ... say no" | The switch has no effect; disable the mod to stop its scripts (mods.md 126, scripting.md 49-50) | Fixed |
| `basics/testing.md` 66-67, 135, `start/troubleshooting.md` 34 | Player.log lists every loaded script / everything | Shipped game logs errors only; `[Mod ...]` lines only in development builds (mods.md 165) | Fixed |
| `sharing/workshop.md` 15, `.agents/skills/publish-workshop` 28 | Button "Create new Workshop item..." | "New Workshop item" (mods.md 182-183) | Fixed |
| `sharing/workshop.md` 17 | Progress percentage, button opens the item in the overlay | Progress bar, then the window shows the item's Workshop link (mods.md 185) | Fixed |
| `sharing/workshop.md` 26 | An update also uploads `preview.png` | An update replaces files only; title, description and picture are edited on Steam (mods.md 191) | Fixed |
| `.agents/skills/publish-workshop` 18 | Subscribers may have scripts switched off at first | Scripting switch has no effect | Fixed |

## 3. Missions

| Where | Modkit says | SRC says (`Modding/missions.md` unless noted) | Action |
|---|---|---|---|
| `missions/reference.md` 71, `chains.md` 65, `index.md` 75 | An undated historic mission takes the weekly slot | "appears alongside the next weekly mission and does not take up one of that week's slots" (147-148) | Fixed |
| `chains.md` 64, 77, 88, `reference.md` 322, `index.md` 75 | A historic date is a floor ("on or after") | "With a date: it appears on that exact day" (146, 328-329) | Fixed |
| `first-mission.md` 39, `chains.md` 90, `reference.md` 352-353 | Day requirements count from the start of the campaign | "counted from the map's starting date" (121) | Fixed |
| `reference.md` 74 | Up to 5 tries to place a location | One draw plus up to five re-draws (locations.md 5-6) | Fixed |
| `index.md` 100 | No locations: mission can never be placed | Placed at a random shipped location (180) | Fixed |
| `index.md` 140 | Validate catches all three id problems | Catches the first two and a clash with a shipped id; not a clash with another mod or the Supporter Pack (172-174, 220-221) | Fixed |
| `index.md` 161-162, `reference.md` 78, 127-128, 225, `chains.md` 26 | Result/cancel handlers named `send_mission_result_text`/`send_mission_cancelled_text`; result "always"; cancelled = player aborted | Handlers are `send_mission_result_event` / `send_mission_cancelled_event` (event strings `..._text`); result "always, except when cancelled"; cancelled = player aborts **or the mission expires** (252-253, getTimeToStart.md 17-18) | Fixed |
| `index.md` 157 | `get_mission_id` always required | Required only for a mission without JSON (248) | Fixed |
| `reference.md` 18, 138, 277 | `get_mission_result` only asked without outcome data | Required for every script-only mission; without it the mission throws (232-233, 263) | Fixed |
| `first-mission.md` 174, `AGENTS.md` 104 | Missing text shows the raw key | "that slot shows nothing in game" (189) | Fixed |
| `first-mission.md` 74, `reference.md` 387 | Damage rolled per plane | Rolled per flight (140-141) | Fixed (**Open**: confirm whether per flight means once per mission) |
| `index.md` 73, `chains.md` 30, `reference.md` 105 | Outcome index 1 can count as a success if you mark it | Which ending counts as a success is fixed by position: 1 fail, 2 success, 3 fail, 4 success (128-136) | Fixed |
| `index.md` 39-44 | Editor has no mission browser, always opens `new_mission` | Opens a mission list with Create/Edit (shipped ones too), delete, Refresh (58-67) | Hidden |
| `index.md` 116, 118 | Editor cannot open/copy a shipped mission or build longer chains | Removed from the "cannot do" list (196-201) | Hidden |
| `index.md` 63 | Enemy strength is under Difficulty | Moved to Text, flavour only (104-107) | Fixed |
| `index.md` 75, 106 | "Historic day" | Renamed "Is Historic"; bad date = undated historic (143, 186) | Fixed |
| `AGENTS.md` 116 | Roll in the first in-flight event only | Default script rolls as-planned at the first report, skill at the second (357, sendMissionEvent.md 23-24) | Fixed |
| `AGENTS.md` 117 | A script-only mission never enters the random draw | After it was created once the weekly draw may hand it out (AddMissionRequirement doc); modkit `reference.md` 57 agrees | Fixed |
| - | Missing: ids containing `test_`, `debug_`, `_debug`, `_test` are not loaded by the shipped game (51-52) | | Added to `AGENTS.md` §6 |
| **Open** | `AGENTS.md` 119 "CreateMission ignores requirements" vs `api.md` 84 / `chains.md` 117 "checks requirements and tags". SRC doxygen says "bypassing ... the mission's own requirements"; the code checks them | | Open |
| **Open** | `missions/locations.md` 49-62, 155, `reference.md` 430-438: flag values, "`_flags` is not read", test leftovers. SRC trimmed these on 2026-09-28 but they are still true per game data | | Open |
| **Open** | `reference.md` ~376: JSON `_missionSuccess` "whether this ending counts as a success" - SRC says success is fixed by position in the editor, but `SetOutcome(..., is_success)` lets scripts set it. Does the JSON flag still matter? | | Open |
| **Open** | A dated historic mission with a CompletedMission gate whose predecessor finishes *after* the date - SRC does not say what happens | | Open |

## 4. Quests

| Where | Modkit says | SRC says (`Modding/quests.md`) | Action |
|---|---|---|---|
| `quests/index.md` 574 | A file with no JSON object is skipped; broken JSON *can* break loading | "A quest file that is not valid JSON is **not** skipped - it breaks the loading of the level" (605) | Fixed |
| `quests/index.md` 426 | Removed cheat lists are ignored with a log warning | Only development builds log a warning (535-536) | Fixed |
| `templates/quest/README.md` 24 | Opening Mods rescans | Refresh (63-64) | Fixed (see §2) |
| `quests/index.md` 416, `data/csv.md` 156, `scripting/index.md` 26 | Install folder `GroundOfAces_Data` / `GroundOfAces.app` | `Ground Of Aces_Data` (csv-data.md 202), `Ground of Aces.app` (scripting.md 11). **But** SRC scripting.md 11 itself writes `GroundOfAces_Data` for Windows | Fixed to `Ground Of Aces_Data` (**Open**: SRC is inconsistent - confirm against a real install) |

## 5. Scripting

| Where | Modkit says | SRC says (`scripting.md`) | Action |
|---|---|---|---|
| `scripting/localization.md` 105, 194, `AGENTS.md` 112 | SetTerm accepts any language, including ones the game does not ship | "The language code must be one the game offers in its options" (163); a shipped key is replaced, so prefix keys (169-172) | Fixed |
| `scripting/localization.md` 147-153 | Three text tags | Four: also `[CharacterStat:<name>]` (298-309) | Fixed |
| `scripting/localization.md` 180 | Fallback is English if defined | A missing language shows the text of a language you did register - always register `en`; no language at all = raw key (166-167) | Fixed |
| `scripting/events.md` 35 | `max_occurrences` per playthrough, -1 unlimited | Per save game, keyed by `<module>.<function>`; negative = no limit, `0` = never runs; checked before the call (267-270) | Fixed |
| **Open** | `scripting/api.md` 106: `SetAsPlannedChance` default 50 for script-only missions | SRC missions.md 291: without it the mission always counts as gone wrong. **Code** (`FlightMissionFactory.cs` 24, 129) uses 50 | Open |
| **Open** | `scripting/localization.md` 32, 34, 218: SetTerm text in a separate store, removed when the mod is removed | SRC silent; code writes overrides of shipped keys into the game's own source | Open |

## 6. CSV tables and table commands

Most drift comes from SRC commits 4fd53f06c5 and b87cf02a07 (2026-09-28), which replaced sample values with full
built-in values and rewrote several mechanics notes.

| Where (`data/csv.md` unless noted) | Modkit says | SRC says (`Modding/csv-data.md`) | Action |
|---|---|---|---|
| 150, `table-editor.md` 156 | The released game writes "mainly" errors | Logs errors only; the lines appear in a development build or the Unity editor (190-192) | Fixed |
| 243, 323, 392, 464 (AirstripTiers, BuildingComponents, MapObjects, WorkbenchProjectData) | Build/farming/crafting time: two workers halve it | One crew member per tile/object at a time; more crew work in parallel, not faster (311, 399, 470, 542) | Fixed |
| 201 | Manoeuvrability `2-10` ... `28-50` | min 2-28, max 8-50 (269) | Fixed |
| 227-228 | Minimum Missions Per Week / Success Rate | Weekly HQ quota, what counts, halved shipment + strike, skipped in training (295-296) | Fixed |
| 241 | Material names the ResourceCost row | ResourceCost accepts no new surfaces; keep to dirt/sand/gravel/concrete/tarmac; missing row = laying fails (309) | Fixed |
| 278-279 | Special attack rows: `0-0` fighters | Row 99 has 8-8 fighters, 101 has 2-2 (350-355) | Fixed |
| 299 | Damage `0` switches the weapon off | `0` makes a non-firing station (Searchlight, Lookout); every column from Fire Rate on is not read (375) | Fixed |
| 357-358 | (missing) | Do not remove a surface row from ResourceCost - laying fails; set cells to `0` instead (434-436) | Fixed |
| 372-373 | PropsInfluence Effect 1 `+10 Mood` etc. | Effect 1: `-1 Mood` to `+3 Mood`, `+1`-`+2 Energy`, `+0.5`-`+10 Confidence`, `-1 Accident`; Effect 2 list (450-451) | Fixed |
| 399 | Fireproof trees remove fire spread from the map | `TRUE` makes a firebreak on the tiles it covers; fire still crosses open ground (477) | Fixed |
| 584 | ModifierRange: bonus applied to the roll | Added to the lowest/highest stat roll; ignored by NoFlightModifier rows (661-662, 681) | Fixed |
| 622-624 | DaySchedule table has a 4th cell in a 3-column table (broken) | | Fixed |
| 628-629 | An uncovered hour has no phase, crew idle | Every hour must be covered by exactly one row; a gap or overlap throws and the phase is stuck (725-729) | Fixed |
| 685-689, `docs/assets/csv/` | FeedbackVariables has no built-in file | SRC links `FeedbackVariables.csv` (787) | Fixed (file copied from the game) |
| `table-editor.md` 47, 62 | Emptied cells are reset to the table default | Blanking a cell is refused except where the game already leaves some row empty; only ResourceCost (`0`) and `Associated Task` (`None`) are filled in (135-142) | Fixed |
| `table-editor.md` 66 | Multi-line rows: ship the whole row as CSV | Refused; whole-row CSV works only in ResourceCost; MoraleInfluenceValues/TaskValues multi-line rows cannot be changed (160-167, 646, 703) | Fixed |
| `table-editor.md` 99 | Removing a command restores the value at the next load | Aircraft already at the base keep their values; a save made with a mod keeps its numbers (278-281) | Fixed |
| `table-editor.md` 128-130 | Log example: `PropsInfluence.json ... cells Tarp of row 'Chair'` | `Tarp` is a ResourceCost column (805) | Fixed |

Less detailed than SRC but not wrong (left unchanged; worth a refresh later): sample values in VehicleData, ScrambleData,
EquipmentData, BuildingComponents, PropsInfluence, MapObjects, GrowingData, GardeningData, WorkbenchProjectData,
MoraleInfluenceValues, FlightMissionData, DaySchedule; the missing value legend (SRC 234-242); the FlightMissionData
explanation (SRC 655-675).

## 7. Unverifiable (SRC is silent, left unchanged)

- Mods window: a **Workshop** button, the details view, the Scripting confirm dialog; DRM-free build behaviour;
  preview over 1 MB failing; "512x512 recommended"; "Workshop mods without Name show a number".
- Maps: the map list is re-read on save; a hand-edited `.goamap` needs a restart; uploading from the Map Editor.
- Art: glb-over-fbx precedence, texture size limits, the terrain-object id/variant table, the 24 biome names.
- Scripting: Python 3.6 syntax limit, available stdlib modules, `logger.LogWarning/LogError(tag, text)`, "no sandbox",
  `GetScriptDataPath` id rules, several event-argument details, tutorial-only event arguments.
- Missions: `_enemyPlaneReport` max 18, `_missionIcon` values (incl. `Luxury`), effect and skill type numbers,
  MaxVictoryPoints crash, legacy fields, script-only data not surviving a save.
- Quests: the "all types at a glance" internal names and polled/event column, requirement-type names, the cheat
  button on the game screen.
- CSV: exact log wordings, "a longer file is skipped whole", the validator not checking CSV.
