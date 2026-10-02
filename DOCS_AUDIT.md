# Docs audit 2026-10-01

Comparison of the modkit handbook (`docs/en/`, `docs/de/`, `AGENTS.md`, skills, templates, examples) with the
game team's docs in `SquadronLeader_Demo/Docs` (local checkout `SquadronLeader_Demo - 2`, branch `develop`,
commit `c307ef6a59` 2026-10-01 "Link the Objects modding page from the main page and mods page"; one local
commit ahead of `origin/develop`, working tree clean). **The game docs are the reference.** "SRC" =
`SquadronLeader_Demo/Docs`. Previous audit: 2026-09-28 (commit `35f391ddab`).

Main SRC changes since the last audit:

- **Historic missions** are checked every in-game hour, no longer at the weekly slot (`ff143666f4`).
- **Mods can add mission locations** in `Missions/Locations/*.json` (`1077ae90bf`, feature 6082).
- **Airplane skins** in a new `Airplanes/` folder (`d380f829cd`), new page `Modding/airplanes.md`.
- **Art** rewritten and presented as working: `Modding/art.md`, `objects.md`, generated `moddable-objects.md`
  and `textures.md`. SRC no longer calls art mods unsupported or work in progress anywhere.

Verdicts: **Wrong**, **Outdated**, **Missing**, **Less detailed**, **Open**, **Unverifiable** (see the
`update-docs` skill). Every finding also applies to the matching `docs/de/` page. Line numbers are `docs/en/`.

---

## 1. Mods basics, start pages, Workshop (`mainpage.md`, `Modding/mods.md`)

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| `basics/mods.md` 10 | content folders `CSV/` ... `Objects/` or `Biomes/` | mainpage 34-35: "... `Biomes/` or `Airplanes/`" | **Outdated** - add `Airplanes/` |
| `basics/mods.md` 38-58 (tree + folder table) | no `Airplanes/`, no `Missions/Locations/` | mods.md 44 "`Locations/` new mission locations"; 49 "`Airplanes/` new airplane skins" | **Missing** - add both |
| `basics/mods.md` 69 | "only files directly inside the subfolder are read; anything deeper is ignored." | mods.md 60-61 "... with one exception: `Missions/Locations/` is read as well." | **Wrong** - add exception |
| `basics/mods.md` 69 | nothing about `Airplanes/` | mods.md 62-63 "`Airplanes/` holds new airplane skins" | **Missing** - add sentence + link |
| `basics/mods.md` 142-148 | "Seeing your changes" table has no skin row | mods.md 145 "An airplane skin PNG or the `Airplanes/config.json` \| Load a level" | **Missing** - add row |
| `basics/mods.md` 148 | art restart row only | mods.md 148-150 "A future update adds an option to reload mods from the main menu" | **Less detailed** - add note |
| `basics/mods.md` 99 | "Without one the Mods window shows a placeholder picture." | mods.md 93-94 "... and the Workshop item has no picture until you add one on its Steam page." | **Less detailed** - add |
| `index.md` 54-62 | "What you can build" has no skins row | mainpage 18 "Add airplane skins" | **Missing** - add row |
| `start/glossary.md` 71, 77 | Mod / content folder lists without skins / `Airplanes` | mods.md 42-49 | **Outdated** - add |
| `basics/testing.md` 10, 16 | "Missions, scripts, quests and CSV tables are read fresh every time a save is loaded." | mods.md 135-136 "tables, quests, missions, scripts and maps alike"; 145 skins | **Less detailed** - add maps, skins |
| `basics/testing.md` 41 | "historic missions with a date are checked at every day change" | missions.md 146 "The game checks every in-game hour" | **Outdated** - reword |
| `basics/testing.md` 51-52 | "appear at the next weekly slot ... wait for the next slot." | missions.md 146-152 "never waits for the weekly schedule ... within the hour" | **Wrong** - reword |
| `basics/testing.md` 123 | missing text shows "a raw key like `missions/mymod_patrol/mission_name`" | missions.md 199 "Missing narrative text \| that slot shows nothing in game" | **Wrong** - "shows nothing" (see Open 4) |
| `basics/cheats.md` 135 | `set_random_event_chance` listed as a normal cheat | scripting.md 265-266 "the development-build cheat `set_random_event_chance`" | **Wrong** - hide row (dev builds only) |
| `AGENTS.md` 52-60 (section 5) | layout without `Airplanes/`, `Missions/Locations/` | mods.md 44, 49, 60-63 | **Missing** - add |
| `AGENTS.md` 225-226 (section 15) | Refresh for "a brand-new mod folder (or a content folder that was empty ...)"; picked up: "Missions, scripts, quests, maps and CSV" | mods.md 143 "a renamed folder, a changed `config.json`"; 145 skins | **Less detailed** - add |
| Skills `csv-tweak` 37, `event-script` 38, `new-map` 38, `new-mission` 56, `new-quest` 41; `templates/csv-tweak/README.md` 22 | opening Mods "rescans the folder" | mods.md 136, 143; quests.md 63-64; csv-data.md 219-221: new folders need **Refresh** | **Wrong** - same wording as `install-mod` 51 |

## 2. Missions and locations (`Modding/missions.md`, `locations.md`, `missions/*.md`)

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| `missions/index.md` 77 | "With a date, it appears on that exact day; without one, it appears alongside the next weekly mission" | missions.md 146-152 hourly check; dated "on that day, or later if its other requirements pass later"; undated "within the hour" | **Outdated** - rewrite |
| `missions/chains.md` 256, 280 | "on that exact day" | missions.md 149 "or later if its other requirements pass later" | **Outdated** - reword |
| `missions/chains.md` 257 | "keeps the normal lead time ... appears alongside the next weekly mission" | missions.md 151-152 "shows up within the hour after that mission succeeds" | **Wrong** - rewrite |
| `missions/chains.md` 259 | "A failed or cancelled attempt brings it back" | missions.md 154-156 "back on the map at the next hourly check, even while its result report is still waiting to be read" | **Less detailed** - add |
| `missions/chains.md` 266-269, 292 | timing table / "alongside the same weekly mission" | missions.md 146-152 | **Outdated** - rewrite rows |
| `missions/chains.md` 290 | forgetting `_isHistoric`: slow, can be drawn again | missions.md 158-161 "A chain without Is Historic ... Use this for a repeatable follow-up." | **Less detailed** - add the repeatable use |
| `missions/reference.md` 70-71 | historic created "at every day change"; undated "alongside this weekly mission" | missions.md 146 hourly | **Wrong** - one "hourly historic check" step |
| `missions/reference.md` 322 | `_historicDay` "The exact day a historic mission appears." | missions.md 149 | **Outdated** - "earliest day" |
| `examples/chain_convoy/README.md` 25, 27; `examples/chain_airfield/README.md` 26 | next mission slot / normal lead time | missions.md 146-156 | **Wrong** - hourly |
| `missions/locations.md` 9 | no locations -> "random place from the list below" | locations.md 13-14 "the places below plus any that enabled mods add" | **Outdated** - add (see Open 5) |
| `missions/locations.md` 45, 159-164 | `SetMissionLocation` only shipped names; "A script cannot use your own place" | locations.md 41-42, 173-178, 186-190 mod-added places work everywhere | **Outdated** - reword |
| none (`locations.md`, `AGENTS.md` 5/7, `new-mission` skill, `scripting/localization.md`) | - | locations.md 150-182 "Adding locations with a mod": `Missions/Locations/*.json`, `{"Locations": [...]}`, numeric `_flags`, toggling without restart, shipped names win, silent clash between mods, `mission_location/<name>` term, bad file skipped with warning | **Missing** - new section |
| `missions/index.md` 63; `reference.md` 310 | times are ranges | missions.md 100-102 "in game minutes ... maximum of `0` means the mission never expires, and a historic mission never expires" | **Missing** - add |
| `missions/reference.md` 253 | `get_time_to_start` default 60 | getTimeToStart.md 22-23 "Returning `0` or a negative number cancels the mission on the next minute tick" | **Less detailed** - add |
| `missions/index.md` 56; `reference.md` 448-450 | tags | missions.md 86-89 "Each shipped map also lists its own name (`debden`, `duxford`, `lichfield`, `perranporth`)" | **Less detailed** - add |
| `missions/index.md` 121 | editor cannot do: "Write the Python side" | missions.md 208-209 "Show a chain as a whole" | **Missing** - add |
| `missions/index.md` 67 | "radio transmissions for each ending" | missions.md 107-109 two mid-flight messages + one per ending | **Less detailed** - spell out |
| `missions/index.md` 39, 75, 89 | editor list; outcomes; "Mission with given ID already exists" | missions.md 67 folder button; 138 "top to bottom from the best ending to the worst"; 173 "Mission id is in use" | **Less detailed** - minor rewording |
| `missions/first-mission.md` 397 | "reads mission files and scripts every time a save is loaded" | missions.md 47-49 "Saving in the Mission Editor reloads them at once" | **Missing** - add |
| `missions/reference.md` 109-117 | import only shown in an example | missions.md 252 "Every mission script needs `from Blindflug.FlightMission import MissionEvent` ... no automatic imports" | **Less detailed** - state as rule |
| none | - | missions.md 313-370 shipped example missions (`calm_supply_drop`, Blitz chain, `default_mission.py`); 318-325 a copy under a new id shows no text without `_raw*`/`SetTerm` | **Missing** - short pointer + the text note |
| `tools/validator` (`discover.py`, `rules.py` 308-314) | skips `Missions/` subfolders; warns on any location not in the catalog | locations.md 150-182 | **Missing (tooling)** - kit maintainers; not a docs edit |

## 3. Quests (`Modding/quests.md`, `examples/quests/*.json`)

The page `quests/index.md` matches SRC almost line for line.

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| `new-quest` skill 41, `new-map` skill 38 | Mods "rescans the folder" | quests.md 63-64 Refresh | **Wrong** - see section 1 |
| `new-quest` skill 27 | aircraft id needed for `12`/`17` when filtered | quests.md 616-617 "any of 12, 13, 17 that is not empty includes at least one aircraft id" | **Less detailed** - add 13 |
| `examples/quests/Quests/example_patrol_chain.json`, `example_map_campaign.json` 41-44; `quests/index.md` 489-492, 545-548 | requirement without `"Name"` | SRC examples line 42 `"Name": "",` (ignored by the game, quests.md 131-132) | **Less detailed** - copy SRC files byte for byte, re-paste blocks |
| `quests/index.md` 558 | shipped quests mentioned in passing | quests.md 570-580 "Shipped quests" table (quest0, quest1, fighter_day_skin_unlock, tutorial_building) | **Less detailed** - add the four descriptions |

## 4. Scripting (`scripting.md`)

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| `scripting/index.md` 258; `scripting/events.md` 34 | `chance` 0.0-1.0, default 1.0 | scripting.md 265-266 "The game adds a global base chance ... `0` unless changed with the development-build cheat" | **Less detailed** - add |
| `scripting/events.md` 56-58 | argument kinds without tasks | scripting.md 238-239 "task arguments are `Blindflug.Tasks.Task` values" | **Less detailed** - add |
| `basics/cheats.md` 135; `event-script` skill 38 | see section 1 | | |

## 5. CSV data (`Modding/csv-data.md`)

All 30 `docs/assets/csv/*.csv` files are byte-identical to the files SRC links (`Assets/BlindGame/Data/Raw/`).

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| `data/table-editor.md` 76 | "Columns you leave out get the table's default or stay empty" | csv-data.md 135-142 cell may be empty only where the game leaves some row empty; `ResourceCost` cells become `0`; `Associated Task` becomes `None` | **Outdated** - reword |
| `data/table-editor.md` 66 | unchangeable multi-line rows: `MoraleInfluenceValues`, `TaskValues` | csv-data.md 689-690 `FlightMissionData` rows `AirplaneIntegrity`, `AirplaneHealth`, `Mood`, `Energy`, `Confidence` | **Less detailed** - add |
| `templates/csv-tweak/README.md` 17 | "Only `Replace` works in most tables." | csv-data.md 83 `Remove` with `Columns` works in every table | **Wrong** - reword |
| `templates/csv-tweak/README.md` 22; `csv-tweak` skill 37 | "rescans the folder" | csv-data.md 219-221 Refresh | **Wrong** - see section 1 |
| `data/csv.md` 173-174 | no legend for built-in values | csv-data.md 234-242 "The built-in values are always complete, never a sample" + legend | **Missing** - add legend |
| `data/csv.md` 186, 188, 198-205, 265-270, 289-291, 315, 328, 331, 377, 379, 396-407, 433-434, 468-471, 499-500, 566-570, 592-594, 632 | sample values (`e.g.`, `0-0 ... 43-60`) | csv-data.md 254-721 complete ranges / lists / "by row" values (e.g. 337-340 PlaneWin/Loose damage by row; 398 Dimensions; 401 `None`; 449 full task list; 503-504 "per tile harvested"; 636-640 morale ids and ranges) | **Less detailed** - copy full values (19 cells) |
| `data/csv.md` 585-586 | `FlightMissionData` row ids named only | csv-data.md 655-675 how thresholds apply, SkillRoll vs NoFlight, what each id measures, first match wins | **Missing** - add |

## 6. Art and airplane skins (`Modding/art.md`, `objects.md`, `moddable-objects.md`, `textures.md`, `airplanes.md`) - new row

| Where | Handbook says | Game docs say | Action |
|---|---|---|---|
| WIP banner: `content/objects.md` 3-4, `biomes.md` 3-4, `basics/mods.md` 60-61, `testing.md` 20, `cheats.md` 27, `maps.md` 43-45, `index.md` 61, `glossary.md` 77, `ai/skills.md` 21, `AGENTS.md` 59, 62, 227, 265, `import-model`, `install-mod` 53 | "Art mods are work in progress. The current alpha does not support them yet" | art.md 6-8, mainpage 17, 79-90 present art as working; no caveat anywhere | **Outdated** - remove only after user confirms (skill rule) |
| `content/objects.md` 10-12, `biomes.md` 10-12 | "Folder layout (preliminary)" | objects.md 38-60 final rules | **Outdated** - rewrite as real content |
| `content/objects.md` 16; `import-model` 29 | thumbnail "at most 256 × 256" | objects.md 219, art.md 74 "512 × 512", 10 MB | **Wrong** - fix |
| `content/biomes.md` 59-60, 68-69 | "2048 × 2048", "8 MB" | art.md 75 "Biome 4096 × 4096 10 MB" | **Wrong** - fix |
| `content/objects.md` 146-157 (hidden) | texture 2048², 8 MB | art.md 70-81 model 32 MB; texture 4096², 10 MB; real PNG; never scaled down | **Wrong** - new visible limits table |
| `content/objects.md` 15 | textures found by the name the material references | objects.md 113-125 three ways in order: `<material>_BaseMap_<tile>`, referenced image name, built-in texture name | **Less detailed** - add |
| none | - | objects.md 146-158 texture-only repaint by built-in name | **Missing** - add, link texture list |
| none | - | objects.md 160-183 UDIM 1001-1003 + `_Specular_` | **Missing** - add |
| `content/objects.md` 18 (+ hidden 119, 135-137 "Default `false`") | `UseGameMaterial` example, no default | objects.md 187-212 default = game material (battle damage), `false` loses it, fallbacks, `tree` covers `tree.2` | **Less detailed** / hidden text **Wrong** - rewrite |
| `content/objects.md` 86-107 (hidden) | glb beats fbx, Y-up metres, first UV, triangulation, LOD | objects.md 51-52, 77-109 (LOD only on objects with built-in LODs; FBX reads base colour/normal/emission textures; embedded images never read) | **Outdated** (largely correct again) - restore in new wording |
| none | - | objects.md 53-58 variants from 0, no leading zeros, `Chair.001.fbx` refused, destroyed skipped if none; 68-69 subfolder name clash; 79-92 footprint/collision stay, static only; 221-224 thumbnail rules | **Missing** - add |
| `content/objects.md` 177 | ids from `BuildingComponents` | objects.md 20-25, 36 + map objects from `MapObjects.csv`, case-insensitive | **Less detailed** - add |
| `content/objects.md` 198-216 | hand list incl. `BarbedWireCorner`, `door_hangar`, `MetalFence`, `MetalFenceCorner`, `Siren`, `WoodenFenceSturdy`, `WoodenFenceSturdyPole` | moddable-objects.md 167 ids, none of these 7 | **Wrong** - use generated list (see Open 1) |
| `content/objects.md` 219-256, 161-163 (hidden); `biomes.md` 181 (hidden) | log table; last mod wins; GPU copy note | art.md 87-95 last wins, objects decided as a whole, `[Mod <id>]` lines in dev builds; 61-62 GPU note | **Outdated** - short new log/conflict section; restore GPU note |
| `content/biomes.md` | no leading-zero rule | art.md 55-56 "`8.png`, not `08.png`", out-of-range reported | **Missing** - add |
| `content/terrain-objects.md` (excluded) | old `TerrainObjects/` page | objects.md 25, 48-54 map objects via `Objects/` | **Removed** (2026-10-01) - modding map/terrain objects is not supported yet; page deleted, map-object parts removed from `objects.md`, `texture-names.md`, `moddable-objects.md`, `maps.md`, `mods.md`, `import-model` skill |
| none | - | `moddable-objects.md`, `textures.md` generated reference lists (no URLs or keys) | **Missing** - ask: generated reference page(s)? |
| none (no page, nav, skill) | - | airplanes.md 1-109: `Airplanes/config.json` `{"Skins": {"<id>": {"Airplane", "Name", "BaseSkin"}}}`, `<id>_BaseMap_1001.png` required, 1002/1003 + `_Specular_` optional, thumbnail, 19 airplane ids, saved as `mod_<modId>_<skinId>`, read on level load, disabled mod falls back | **Missing** - new page `content/airplanes.md` (+ DE, nav), skill trigger |
| `import-model` skill 29, 37 | old texture rule; manual name check | objects.md 113-183, art.md 66-81 | **Less detailed** - update + checklist |

### Problems in `examples/3d_assets/` (branch `3d-assets`) - for the user, not fixed by this audit

| File | Problem | SRC |
|---|---|---|
| `Props-01_Toon-Main_BaseMap_1001.png` | 11,571,790 bytes, over the 10 MB texture limit: skipped in game, 7 of 9 models untextured | art.md 73, 79-81 |
| `Flag-RAF_Toon-Main_BaseMap_1001.png` | the flag FBX material is `Flag-RAF_Toon-Cloth`, so the name does not match | objects.md 118 |
| `_Readme.rtf` | "UDIM (not supported at the initial release)" - SRC supports UDIM | objects.md 160-183 |
| `_Readme.rtf` | contains an Airtable shared-view link (`airtable.com/appvUVR7eS3bq1S8f/...`); the repo/site is public | - |
| `Presets/Substance Painter/export-presets/Unity_GoA_UDIM.spexp` | exports `$textureSet_$udim` without `_BaseMap`, so the files are not found by the material-name rule | objects.md 118, 165-177 |
| whole folder | loose asset pack, no `Objects/` folder or `config.json`; not installable as is | mods.md 47 |

---

## Open (SRC contradicts itself or needs a decision)

1. **`BarbedWireCorner`, `door_hangar`**: in `textures.md` (2026-09-29), not in `moddable-objects.md` (2026-10-01). Moddable or not?
2. **Shared/shader textures** (`cracks`, `shading_map`, `Noise35`, `Texture2D_<guid>`): objects.md 151-153 says shared art keeps the built-in texture; textures.md 11-21 lists them as replaceable.
3. **Art refusals in the shipped log**: art.md 93-95 "logs every file it refused" vs mods.md 155-156 "The shipped game logs errors only".
4. **Missing text**: missions.md 199 "shows nothing" vs scripting.md 167 raw key in the event log (affects `start/troubleshooting.md` 26, `glossary.md` 81).
5. **No-location fallback**: missions.md 190 "shipped list" vs locations.md 13-14 "plus any that enabled mods add".
6. **Location fields read**: locations.md 33 "`_locationName` is the only field the game reads" vs locations.md 9-11, 186-187 coordinates from the mission file give the fuel.
7. **"Everything on next level load"**: mainpage 38 vs art.md 18-20 restart (carried over).
8. **Install folder name**: scripting.md 10 `GroundOfAces_Data` vs csv-data.md 202 `Ground Of Aces_Data` (carried over).
9. **Which ending counts as success**: missions.md 128-129 fixed by position vs 296 `SetOutcome(..., is_success)` (carried over).
10. **`SetAsPlannedChance` default / `CreateMission` checks requirements** (carried over).
11. **Art WIP banner** (section 6) - needs the user's confirmation that art mods work.
12. **Airtable link** in `examples/3d_assets/_Readme.rtf` - user decision before publishing.

## Unverifiable (SRC silent; left unchanged)

- Scripting: Python 3.6 syntax limit, missing stdlib modules, `logger.LogWarning/LogError(tag, text)`, forbidden-import list, event argument lists, API tables, language-code list, "Mods window shows which mods contain scripts".
- Missions: Validate warning "Max Victory Points", Workshop-before-manual load order, `_enemyPlaneReport` max 18, `Luxury` icon, `SetMaxAirplaneSlots`/`SetDifficulty` defaults.
- Quests: polled/event "Kind" column, "no type 14", requirement-type names, cheat button wording.
- CSV: macOS template path, exact log wordings, "longer file skipped whole".
- Mods/Workshop: Workshop button, details view, Scripting confirm dialog, DRM-free, preview >1 MB failing upload, upload error table, 512x512 recommendation, map editor details.
- Art: biome surface detail/burnt look, `Terrain-Type_*` names, terrain variant meanings, `ocean`, readme "-Z forward", skin `Name` localization, Opaque base skins and tile 1002, Enabled toggle for skins.

---

## Applied 2026-10-01

All Wrong, Outdated, Missing and Less detailed findings above were applied in `docs/en/` and `docs/de/`, `AGENTS.md`,
`CONTRIBUTING.md`, `.agents/skills/` (mirrored with `tools/sync_skills.py`), `templates/csv-tweak/README.md`,
`examples/chain_*/README.md` and `examples/quests/Quests/` (two files now byte-identical to SRC). Decisions by the
maintainer:

- **Art mods work**: every "work in progress / not supported by the current alpha" banner and note was removed.
- **New pages** (in `nav`, German titles in `nav_translations`): `content/airplanes.md` (Airplane skins / Flugzeug-Skins),
  `content/moddable-objects.md` (167 ids from SRC `moddable-objects.md`, without `BarbedWireCorner`/`door_hangar`),
  `content/texture-names.md` (from SRC `textures.md`, filtered to `_BaseMap*`, `_SpecularMap*`, `_EmissiveMap*` slots).
- `content/objects.md` and `content/biomes.md` were rewritten from SRC; their stale hidden blocks were deleted.
  `content/terrain-objects.md` was later deleted: map/terrain objects are not moddable yet.
- `basics/cheats.md` `set_random_event_chance` row hidden (development builds only).

Not done: the validator still ignores `Missions/Locations/` and `Airplanes/` (noted in `AGENTS.md` section 13);
`examples/3d_assets/` problems are left for the maintainer; Open and Unverifiable items unchanged.
`mkdocs build --strict` was not run (mkdocs not installed; skipped at the maintainer's request).
