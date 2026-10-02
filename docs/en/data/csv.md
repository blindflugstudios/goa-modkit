# CSV tables

Most of the numbers that drive Ground of Aces - what a building costs, how fast a plane flies, how much a meal lifts a crew member's mood - live in data tables. A mod can change any of them without touching the game's code, by dropping a small file into its own folder.

This page is the complete reference: where the files go, what the two file formats look like, what the game checks before it accepts a value, and what every table and column means. Every table section in [The tables](#the-tables) starts with a link to the built-in file, so you can open the real thing or save it and copy its header row.

!!! note
    Nothing here can permanently damage your game. A value the game cannot use is refused and written to the [log](../start/troubleshooting.md#find-the-playerlog) with the reason; the built-in value stays. Removing the mod folder restores everything.

!!! tip
    The single-cell `<Table>.json` command files are covered step by step, with more examples, on [Table command files](table-editor.md).

One mod is one folder in your `Mods` folder, and the data tables go into its `CSV/` subfolder:

```text
Mods/
  my_balance_mod/
    config.json          optional
    CSV/
      VehicleData.csv    whole rows
      Variables.json     single cells
```

Where the `Mods` folder is, what `config.json` may contain and how several mods are ordered is explained once, on [How mods work](../basics/mods.md). The folder itself can have any name. The one rule that matters here: if you give the mod an `Id` in `config.json`, it must be 3–64 characters of lower-case letters, digits, `_`, `.` or `-`, starting with a letter or digit; anything else is ignored without a message and the lower-cased folder name is used instead.

Only files directly inside `CSV/` are read - subfolders are ignored.

## Your first mod

Make the wooden wall cost one plank instead of two. Create `Mods/my_balance_mod/CSV/ResourceCost.json` containing:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
  ]
}
```

Start the game, load a level, and the wall costs one plank. That is the whole mod - no manifest, no registration.

## The two file formats

A file is named after the table it changes, matched **exactly**, capital letters included: `VehicleData.csv`, never `vehicledata.csv`. A file naming a table that does not exist is skipped, and the [log](../start/troubleshooting.md#find-the-playerlog) says so.

You may use either format, or both. Within one mod the `.csv` files are applied first and the `.json` files after, so a command can refine a row a CSV file added.

### Single cells - `<Table>.json`

A list of commands, run top to bottom. This is the format to reach for: it touches only the values you name and leaves everything else alone.

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350, "Movement Speed": 7 } },
    { "Command": "Add",     "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } },
    { "Command": "Remove",  "Id": "Chair", "Columns": [ "Tarp" ] },
    { "Command": "Remove",  "Id": "Drawer" }
  ]
}
```

| Command | Fields | What it does |
|---|---|---|
| `Replace` | `Id`, `Cells` | Changes only the listed cells of an existing row. Everything else keeps its value. |
| `Add` | `Id`, `Cells` | Adds a new row. Only possible in `ResourceCost` and `PropsInfluence` (see [Adding and removing rows](#adding-and-removing-rows)). |
| `Remove` with `Columns` | `Id`, `Columns` | Clears the listed cells of a row. |
| `Remove` without `Columns` | `Id` | Removes the whole row. Only in `ResourceCost` and `PropsInfluence`. |

Rules of the format:

- Plain JSON - no comments, no trailing commas.
- `Command` and `Id` ignore capitalisation. The keys inside `Cells` and the entries in `Columns` are column headers and must match **exactly**, including spaces.
- Values may be written as JSON strings, numbers or booleans - `300`, `1.5`, `true` and `"300"` all work.
- An empty string, a string of only spaces, or `null` in `Cells` clears that cell, the same as listing it under `Columns` in a `Remove`.
- `Remove` does not take `Cells`; list the cells to clear in `Columns`.
- At most 200 commands per file. A file that does not parse, or has no `Commands`, is skipped whole.
- Each command is judged on its own - a bad one is skipped with a warning and the rest still apply.

### Whole rows - `<Table>.csv`

A spreadsheet file carrying complete rows. Use this when you would rather edit a table in a spreadsheet program and ship the finished rows.

```text
Name,Value
TurboTimeScaleMultiplier,20
RandomActionChatProbability,0.6
```

- The header row must list **exactly** the table's columns: the id column first, then every value column, in any order, none missing and none extra. The id column's own header is ignored, so only the value columns have to match.
- Include only the rows you want to change - a file does not have to cover the whole table.
- A row whose id matches a built-in row replaces that row completely. Ids ignore capitalisation.
- Give every row the same number of cells as the header row. A short row makes the file unreadable and the whole file is skipped; extra cells beyond the header are silently ignored.
- A cell that contains a comma must be quoted, as a spreadsheet program does: `"Sleep,Chill"`. A line break inside a quoted cell is not supported - it ends the row.
- At most 200 rows per file. Fully blank lines and lines starting with `#` are ignored, so you can leave notes. A line that starts with an empty id cell but has other cells is read as a continuation of the row above, and that row is then refused as spanning several lines.
- The same id on two separate lines makes the file unreadable; on two neighbouring lines it is treated as one row and refused.
- Each row is judged on its own - a bad row is skipped and the built-in row stays.

## Rules that apply everywhere

### Columns only take the kind of value they already hold

A column that holds numbers in every built-in row takes only numbers; one that holds `TRUE`/`FALSE` takes only those. `Movement Speed = fast` is refused. Columns that hold text are freer, but most of them still have a rule of their own - the tables further down say which values each one accepts.

### Empty cells

A cell may only be left empty in a column where the game already leaves some row empty. Everywhere else, blanking a cell is refused, because the game has no "no value" case for it.

Two columns are special and are filled in for you instead of being left blank:

- Any `ResourceCost` cell you leave out, clear, or set to `""` becomes `0`. An `Add` therefore only needs the resources that actually cost something.
- `Associated Task` in `BuildingComponents` becomes `None`, meaning "this object gives no task".

### Adding and removing rows

You are normally changing cells of rows that already exist. Whole rows can only be added or removed in two tables, because everywhere else the game and your save files expect a fixed set of ids:

| Table | Rows can be added or removed |
|---|---|
| `ResourceCost` | yes, for any built-in object or aircraft id |
| `PropsInfluence` | yes, for any built-in object or aircraft id |
| every other table | no |

An added row must use an id that already exists as a building object or an aircraft - you are giving an existing thing a build cost or a mood effect it did not have, not inventing a new thing.

### Rows that take up several lines

A few tables spread one row over several lines, because that row holds a list - a task with several settings, a mood effect with one variant per bed type. A single mod row cannot express a list, so those rows are refused. The table sections below name them.

In `ResourceCost` only, some rows carry a leftover heading in their `Money` cell and so count as several lines. There a whole-row CSV is the fix: it rewrites every cell and tidies the row up at the same time. The affected ids are `KickstarterCustomMonument`, `RadioTower`, `window_wood`, `window_tent`, `window_brick`, `window_hangar`, `window_concrete`, `Distillery`, `ParkingLarge` and `gravel`.

## Checking what happened

Every accepted change and every refusal is one line in the game's [log](../start/troubleshooting.md#find-the-playerlog), `Player.log`. On Windows there is also an HTML version in the same folder that is easier to read. The label at the start of each line is the mod's id.

```text
[Mod my_balance_mod] CSV/ResourceCost.json command 1 replaced cells Planks of row 'wall_wood'.
[Mod my_balance_mod] CSV/VehicleData.csv overrides built-in row 'gladiator'.
[Mod my_balance_mod] CSV/PropsInfluence.json command 4 removed row 'Drawer'.
```

A refusal names the file, the row or command number, and the reason:

```text
[Mod my_balance_mod] CSV/VehicleData.json command 3 rejected: 'Fight Power' exceeds 2x the highest built-in value (60).
[Mod my_balance_mod] CSV/AirBaseData.json command 1 rejected: 'Missions Per Week' holds numbers in every built-in row; 'seven' is not one.
```

!!! note
    These lines are written as information and warnings. The released game [logs](../start/troubleshooting.md#find-the-playerlog) errors only, so you will see them only in a development build or in the Unity editor. In the released game, check the effect in the game instead - load a level and look at the value you changed.

A misspelled table name or a header row that does not match still produces a `skipped:` line naming the file. **If you see no `[Mod ...]` lines at all and the change does not show**, the game did not pick the mod up: the `CSV/` folder was still empty when the game started (press **Refresh** in the Mods window), the mod is switched off in the Mods window, or the mod folder is a symbolic link or junction, which is never followed.

### Finding a table's column headers

The game ships header templates for four tables (`BuildingComponents`, `PropsInfluence`, `ResourceCost` and `VehicleData`) in `Ground Of Aces_Data/StreamingAssets/Modding/Templates/` inside the installation folder (on macOS: `Ground of Aces.app/Contents/Resources/Data/StreamingAssets/Modding/Templates/`). For the rest, the column list is on this page, and every table section links the built-in file. Or ask the game: write a deliberately wrong header, load once, and the [log](../start/troubleshooting.md#find-the-playerlog) prints the columns it expected.

## Load order

Mods are applied in the order described on [Which mod wins](../basics/mods.md#which-mod-wins) - Workshop first, then your own, lower `LoadOrder` first. When two mods change the same row, the later one wins for the cells it touches: a whole-row CSV replaces everything an earlier mod did to that row, a `Replace` only the cells it names. A mod switched off in the Mods window contributes nothing.

## When changes take effect

CSV tables are rebuilt every time a level is loaded - return to the main menu and load again. The same happens when the main menu or the map editor opens. Edit a file while a level is running and the change appears on the next load, so you can try out values without restarting. A file you keep open in a spreadsheet program is still read.

A brand-new mod folder, a `CSV/` folder that was still empty when the game started, or a changed `config.json` needs the game to look at the mod list again: press **Refresh** in the Mods window (main menu → Mods) and then load a level, or restart the game.

## The tables

Thirty tables can be modded. Three files that exist in the game but are not loaded - `ResourceDegradation`,
`StartTimeValues` and `StateInfluence` - cannot.

Each section lists the columns, what values they take, and what the built-in rows use. Where a column has no
special rule, only the generic ones above apply.

The built-in values are always complete, never a sample:

- `a–b` is the full range: the lowest and the highest value any built-in row uses.
- A list joined by "or" is every distinct value the built-in rows use.
- A list marked "by row" gives each row's value, in the order the rows appear in the file.
- "on every row" means all built-in rows hold that one value.
- A `min-max` column gives each half its own range: "min 0–43, max 0–60" means the first number runs from 0 to
  43 across the rows and the second from 0 to 60.
- An empty built-in cell means the built-in rows use every value listed under Value.

### Aircraft and base

#### `VehicleData` - aircraft

Built-in file: [VehicleData.csv](../assets/csv/VehicleData.csv)

One row per aircraft. Rows cannot be added or removed.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Name` | localization key | `airplane/<row id>` on every row, e.g. `airplane/spitfire` | must not be empty |
| `Type` | `Fighter`, `Bomber`, `MultiRole`, `Special` | | |
| `Crew` | comma list of seats; repeat a role for two seats | 1–8 seats, from `Pilot` alone to `Pilot,Pilot,BombAimer,Navigator,FlightEngineer,RadioOperator,Gunner,Gunner`; every row starts with `Pilot` and all six roles are used | in a CSV file, wrap a cell with more than one seat in quotes: `"Pilot,Gunner,Navigator"`. Roles: `Pilot`, `Gunner`, `Navigator`, `BombAimer`, `FlightEngineer`, `RadioOperator` |
| `Runway Tier` | whole number | 1–5 | above 5 and no airstrip can serve it |
| `Parking Size` | whole number | 0–2 | above 2 and it can never park |
| `Victory Points Cost` | whole number | 0–12 | 0 makes it free |
| `Movement Speed` | whole number | 5 on every row | taxi speed; 0 and it never reaches the runway |
| `Landing Length` | whole number | 60–170 | longer than any buildable strip and it can never land |
| `Health` | whole number | 100 on every row | |
| `Initial Integrity` | whole number | 1000 on every row | hours of wear the aircraft can take before it is worn out (1000 h ≈ 41 days) |
| `Fuel Capacity` | whole number | 200–1260 | |
| `Voxel Size` | `AxBxC` | `10x0x10` on every row | |
| `Fight Power` | `min-max` | min 0–43, max 0–60 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Bomb Power` | `min-max` | min 0–50, max 0–80 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Recon Power` | `min-max` | min 5–42, max 10–60 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Manoeuvrability` | `min-max` | min 2–28, max 8–50 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Transport Capacity` | `min-max` | min 1–60, max 5–90 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Stealthiness` | `min-max` | min 10–88, max 48–98 | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Wreck Resource Type` | `/`-list of resources | `Metal/RepairParts` on every row | both wreck columns set, or both empty |
| `Wreck Resource Amount` | `/`-list of whole numbers | `10/5` on every row | one amount per entry in `Wreck Resource Type`, in the order listed there |
| `Low Caliber Ammo Capacity` | whole number | 0–3300 | `GunAmmo` carried; 0 = none |
| `High Caliber Ammo Capacity` | whole number | 0–300 | `AntiAirAmmo` carried; 0 = none |
| `Plane Bombs Capacity` | whole number | 0–32 | `PlaneBombs` carried; 0 = none |

!!! warning
    An aircraft already parked at your base keeps the health, integrity and fuel capacity it was built with.
    Only newly delivered aircraft pick up changed values - so a save made while a mod was active keeps that
    mod's numbers even after you remove it.

#### `AirBaseData` - the HQ rank ladder

Built-in file: [AirBaseData.csv](../assets/csv/AirBaseData.csv)

Rows `1`–`6`, one per base category. All six must exist and their ids cannot change.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Airstrip Tier` | whole number | by row: 1, 2, 3, 4, 5, 5 | required to reach the rank |
| `Minimum Airstrip Count` | whole number | 1–5 | |
| `Minimum Parking Count` | whole number | 1–20 | |
| `Missions Per Week` | whole number | 6–18 | slots the week offers; 0 and no missions are scheduled |
| `Minimum Missions Per Week` | whole number | 2–10 | the weekly HQ quota: how many missions the base must fly to a result each week. Won and lost missions count; cancelled ones and failed historic missions do not. Missing this or `Minimum Success Rate` halves the next shipment's slots (rounded up) and, on the normal HQ strikes setting, adds a strike - three weeks missed in a row end the run. Training weeks and the "no requirements" HQ setting skip the check. Above `Missions Per Week` makes the quota impossible |
| `Minimum Success Rate` | fraction, not percent | 0.4–0.8 | share of the missions counted by `Minimum Missions Per Week` that must be won; above 1 is unachievable |
| `Available Shipment Slots` | whole number | 4–8 | 0 disables supply |

#### `AirstripTiers`

Built-in file: [AirstripTiers.csv](../assets/csv/AirstripTiers.csv)

Rows `1`–`5`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Length` | whole number | by row: 80, 120, 140, 160, 200 | tiers match on "length or more", so keep them ascending |
| `Width` | whole number | by row: 12, 14, 18, 22, 26 | tiers match on "width or more", so keep them ascending |
| `Material` | text | by row: `dirt`, `sand`, `gravel`, `concrete`, `tarmac` | **must not repeat another tier's material**, and must name an existing `ResourceCost` row - that row is what each tile of this runway costs. `ResourceCost` does not accept new surface rows, so in practice keep to `dirt`, `sand`, `gravel`, `concrete` and `tarmac` (swapping them between tiers is fine). A material with no `ResourceCost` row is accepted here, and then laying a runway of that tier fails with an error |
| `Biome Id` | whole number | by row: 6, 20, 22, 15, 13 | ground painted under the finished strip |
| `Build Time` | whole number | by row: 5, 2, 2, 2, 2 | in-game minutes of work per tile. Each tile is worked by one crew member at a time, so more crew lay more tiles in parallel, not one tile faster |

#### `Biomes`

Built-in file: [Biomes.csv](../assets/csv/Biomes.csv)

Rows `0`–`23`, the ground types. All columns are numbers, so this table is easy to tune safely.

| Column | Built-in | Notes |
|---|---|---|
| `Airstrip Tier` | 0–5 | tier a runway laid on this ground counts as |
| `Character Speed Modifier` | 1–1.2 | 0 freezes anyone standing on it |
| `Airplane Speed Modifier` | 0.5–1.2 | |
| `Degradation Penalty` | 0–0.2 | extra wear on goods stored here |
| `Fire Spread Modifier` | 0.5 or 1 | |

#### `ScrambleData` - enemy aircraft in a scramble

Built-in file: [ScrambleData.csv](../assets/csv/ScrambleData.csv)

Rows `Fighter`, `Diver`, `Bomber`. The names cannot change. All columns are whole numbers.

| Column | Built-in | Notes |
|---|---|---|
| `PlaneHealth` | by row: 18, 26, 34 | |
| `PlanePower` | by row: 23, 17, 14 | |
| `PlaneWinDealDamageMin` | by row: 20, 20, 15 | damage to your aircraft when the enemy wins |
| `PlaneWinDealDamageMax` | by row: 120, 70, 50 | |
| `PlaneLooseDealDamageMin` | by row: 10, 5, 5 | damage to your aircraft when the enemy loses |
| `PlaneLooseDealDamageMax` | by row: 25, 20, 15 | |

#### `AttacksComposition` - what an air raid is made of

Built-in file: [AttacksComposition.csv](../assets/csv/AttacksComposition.csv)

The row id is the raid severity. Normal play reaches **1–25**; rows `99`, `101`, `200` and `300` are not
reached by the normal severity ladder and are kept for special raids. The ranges below describe rows 1–25.
The four special rows point at themselves in the last two columns and hold:

| Row | `Bombers` | `Divers` | `Fighters` |
|---|---|---|---|
| `99` | `9-9` | `6-6` | `8-8` |
| `200` | `10-10` | `0-0` | `0-0` |
| `300` | `0-0` | `10-10` | `0-0` |
| `101` | `0-0` | `3-3` | `2-2` |

| Column | Value | Built-in (rows 1–25) | Notes |
|---|---|---|---|
| `Bombers` | `min-max` | min 0–4, max 0–6 | whole numbers, `0 ≤ min ≤ max` |
| `Divers` | `min-max` | min 0–6, max 0–6 | whole numbers, `0 ≤ min ≤ max` |
| `Fighters` | `min-max` | min 1–8, max 2–8 | whole numbers, `0 ≤ min ≤ max` |
| `LowAttacks` | whole number | 1–14 | severity used instead when the map is set to easier raids - **must name a row this table has** |
| `HighAttacks` | whole number | 2–25 | severity used when the map is set to harder raids - **must name a row this table has** |

#### `EquipmentData` - AA guns, searchlights, towers

Built-in file: [EquipmentData.csv](../assets/csv/EquipmentData.csv)

Rows are equipment ids: `Bofors40mm`, `Searchlight`, `RadioTower`, `VickersGunAA`, `OerlikonGun`, `Lookout`,
`ControlTowerMetal`, `ControlTowerBrick`, `ControlTowerConcrete`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Range` | number | 10–70 | 0 makes the piece useless |
| `Damage` | number | 0–6 | `0` makes the piece a non-firing station like the `Searchlight` or `Lookout`: it can still be placed and crewed, but it never shoots, and every column from `Fire Rate` onward is not read for it |
| `Fire Rate` | whole number | 0–720 | rounds per minute |
| `Ammo Type` | resource name or `None` | `GunAmmo`, `AntiAirAmmo`, `None` or `0` | anything that is not a resource name (`None`, `0`) means the piece stores no ammo |
| `Ammo Capacity` | whole number | 0–80 | rounds loaded at once |
| `Ammo Load Time` | number | 0–6.5 | seconds to reload |
| `Ammo Storage` | whole number | 0–500 | **`0` means it never draws ammo** |
| `Damage Bonus` | number | 0 or 0.25 | granted to others in range (searchlight) |
| `Firing Angle` | number | 0, 140 or 360 | `0` is read as a full circle |
| `Aiming Speed` | number | 0–170 | degrees per second |
| `Range Bonus` | number | 0 or 16 | granted to others in range (lookout) |
| `Attacker Priority` | `Bombers`, `Divers`, `Fighters`, `Nearest`, `None` | `Bombers`, `Divers`, `Fighters` or `None`; no row uses `Nearest` | anything else falls back to `None` |

### Building and objects

#### `BuildingComponents` - objects and building parts

Built-in file: [BuildingComponents.csv](../assets/csv/BuildingComponents.csv)

One row per object, wall piece, floor, roof, workbench and piece of equipment. Rows cannot be added or
removed.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Dimensions` | `WxHxD`, or `dynamic/1x0x1` for roofs | width 1–32, height 0–6, depth 1–32 (from `1x0x1` to `32x1x32`), `dynamic/1x0x1` on the roofs, empty on 9 rows (listed below) | |
| `Build Time` | whole number | 0–420 | in-game minutes of work. One crew member builds an object at a time; extra crew do not speed it up |
| `Health` | whole number | 0–10000 | the huge value marks the indestructible pieces |
| `Associated Task` | task name or `None` | `None`, `Sleep`, `Chill`, `UseEquipment`, `PlayPiano`, `UseTrainingObject`, `MonitorAirspace`, `UseRadio`, `SaluteTheFlag`, `Grieve`, `ListenToMusic`, `PlayDartboard`, `PlayGuitar`, `PlayBilliardTable` or `UsePlanningBoard` | pointing an object at a task its art does not fit is allowed, and looks wrong |
| `Users Limit` | whole number | 0–5 | 0 on a usable object means nobody can use it |
| `Is Wall Deco` | `TRUE`/`FALSE` | | |
| `Is Floor Deco` | `TRUE`/`FALSE` | | |
| `Is Fireproof` | `TRUE`/`FALSE` | | |
| `Placement Requirement` | `None`, `Indoors`, `Outdoors` | | |

!!! note
    A `Replace` is checked against the finished row, so a row that leaves `Dimensions` or `Users Limit` empty
    cannot be patched unless you also set that cell in the same command - or ship the row as CSV.
    Empty `Dimensions`: `PropagandaPoster`, `MusicPoster`, `AirplanePoster`, `CompanyMascotPoster`,
    `CurtainsClosed`, `CurtainsOpen`, `EntranceSign`, `tombstone`, `storage_box`.
    Empty `Users Limit`: the workbenches and the three parking sizes.

#### `ResourceCost` - what something costs to build

Built-in file: [ResourceCost.csv](../assets/csv/ResourceCost.csv)

One row per object or aircraft id, one column per resource. **Rows can be added and removed.** A removed row
means "no build cost". A cost of `0` means "not required", so zeroing every column has the same effect. An
added row's id must be an existing `BuildingComponents` or `VehicleData` id; anything else is refused as
"neither a built-in prop nor a built-in plane".

Every cell is a whole number, zero or more. The columns are:

```text
Money  VictoryPoints  Trash  Wood  Clay  Sandbags  Stone  Food  RawWater  Herbs  Metal  Bricks
Planks  Tarp  Cement  Fuel  PurifiedWater  Meals  SimpleMedicine  Intel  Machinery  Electronics
LuxuryGoods  MilitaryConstruction  Camouflage  FoodRations  StrongMedicine  RepairParts  GunAmmo
AntiAirAmmo  PlaneBombs
```

Runway surfaces are rows here too - `dirt`, `sand`, `gravel`, `concrete`, `tarmac` - so changing `gravel`
changes what a tier-3 runway costs per tile. **Do not remove a surface row**: unlike an object, a surface with
no row does not become free - laying a runway of that tier fails with an error. To make a surface free, set
every cell of its row to `0`.

#### `PropsInfluence` - the mood effect an object radiates

Built-in file: [PropsInfluence.csv](../assets/csv/PropsInfluence.csv)

One row per object that lifts or lowers the mood of crew nearby. **Rows can be added and removed**; an object
without a row simply has no effect.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Buff Name` | localization key | a `prop_effects/<effect>` key on every row (31 different keys), e.g. `prop_effects/organised_sleep` | must not be empty |
| `Radius` | number | 0.5–50 | in tiles; the control towers reach 20, 30 and 50 |
| `Associated Tasks Or Action` | comma list of task names | 1–4 names per row, e.g. `Sleep` or `"Sleep,Chill"`, drawn from `AidInjured`, `BoardAirplane`, `BringResources`, `Bury`, `Chill`, `Cook`, `Eat`, `Grieve`, `HarvestGardeningTile`, `Landing`, `Loiter`, `MaintainAirplane`, `PlayGuitar`, `PlayPiano`, `Recover`, `RecoverInBed`, `Repair`, `RepairAirplane`, `Sleep`, `Stockpile`, `UseEquipment`, `UsePlanningBoard`, `UseRadio`, `UseTrainingObject`, `Water` or `WorkOnWorkbench` | must not be empty. In a CSV file, wrap a cell with more than one task in quotes: `"Sleep,Chill"`. A name that matches no task is accepted and the effect simply **never fires** |
| `Effect 1` | `<signed number> <name>` | `-1 Mood` to `+3 Mood`, `+1 Energy` to `+2 Energy`, `+0.5 Confidence` to `+10 Confidence`, or `-1 Accident` | names: `Mood`, `Confidence`, `Energy` |
| `Effect 2` | `<signed number> <name>`, or empty | `-1.5 Energy`, `+1 Energy`, `+0.5 Mood`, `+10 Mood` or `+1 Confidence` on 9 rows; empty on the rest | |
| `Effect 3` | `<signed number> <name>`, or empty | empty on every row | |

The sign is part of the number, so `1 Mood` means `+1`. Names are matched loosely, so `+1 mood` works. A name
other than the three above is stored as a special effect (the game uses `-1 Accident` on the three control
towers); an invented name is accepted and does nothing.

#### `MapObjects` - trees, rocks, ponds and other harvestables

Built-in file: [MapObjects.csv](../assets/csv/MapObjects.csv)

One row per world object. Ids are used by map files and cannot change.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `LocKey_Name` | localization key | `map.obj.<object>.name` on 20 rows, e.g. `map.obj.tree.name`; `map.obj.<object>` without `.name` on the other 13, e.g. `map.obj.crate` | |
| `LocKey_Description` | localization key | `map.obj.<object>.description` on 18 rows, e.g. `map.obj.tree.description`; `map.obj.<object>` without `.description` on the other 15, e.g. `map.obj.crate` | |
| `Dimensions` | `WxHxD` | width 1–4, height 1–6, depth 1–6 (from `1x1x1` to `4x6x4`) | |
| `Resource Harvested` | resource name, or empty | `Wood`, `Stone`, `Herbs`, `Food`, `RawWater`, `Clay`, `Sandbags`, `Metal`, `Planks`, `Fuel`, `GrainSeeds`, `BeansSeeds`, `PotatoSeeds` or `TomatoSeeds`; empty on 9 rows | empty means nothing to harvest |
| `Farming Time` | whole number | 0–400 | in-game minutes of work per harvest, by one crew member at a time |
| `Resource Amount` | whole number | 0–50 | yield per harvest |
| `Resource Total` | whole number | 0–500 | total before it is used up |
| `Limited Harvest Amount` | whole number | 0, 20, 30 or 100 | cap for endless sources; 0 = uncapped |
| `Destroyed On Depletion` | `TRUE`/`FALSE` | | `FALSE` with `Refresh Time` 0 leaves something that can never be harvested again |
| `Refresh Time` | whole number | 0–21600 | minutes until it regrows |
| `Health` | whole number | 1–2147483647 | the huge value marks the indestructible ones |
| `Is Fireproof` | `TRUE`/`FALSE` | `TRUE` on the rocks, pits, pond, ocean, `WaterPump` and `WaterTower` | `TRUE` makes the object a firebreak: fire can neither start on nor spread onto the tiles it covers. Fire still crosses the open ground around it |

#### `GrowingData` - saplings becoming trees

Built-in file: [GrowingData.csv](../assets/csv/GrowingData.csv)

Two rows, `young_tree` and `young_tree_big`.

| Column | Value | Built-in |
|---|---|---|
| `To` | a `MapObjects` id | by row: `tree`, `tree_big` |
| `Min Hours` | whole number | 672 on every row |
| `Max Hours` | whole number | 840 on every row |

A sapling that is already on the map when a save is loaded draws its remaining time between half of
`Min Hours` and `Max Hours`; only newly planted ones use the full minimum.

#### `GardeningData` - the four crops

Built-in file: [GardeningData.csv](../assets/csv/GardeningData.csv)

Rows `grain`, `beans`, `potato`, `tomato`.

| Column | Built-in | Notes |
|---|---|---|
| `Growth` | by row: 3, 6, 15, 10 | watered days until harvest - the plant gains one at midnight for every day its tile was watered; 0 is harvestable instantly |
| `Food` | by row: 3, 4, 20, 7 | `Food` per tile harvested, when the zone is set to grow for food |
| `Seeds` | by row: 2, 5, 3, 1 | the crop's own seed resource (`GrainSeeds`, `BeansSeeds`, `PotatoSeeds`, `TomatoSeeds`) per tile harvested, when the zone is set to grow for seeds; 0 makes the crop unsustainable |
| `Regrowth` | only `tomato` is `TRUE` | regrows instead of being consumed |

### Resources and crafting

#### `ResourceData` - what a resource is

Built-in file: [ResourceData.csv](../assets/csv/ResourceData.csv)

One row per resource, named exactly as the game names it.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Initial Integrity` | whole number | 0–50000 | hours before a pile spoils; 0 rots instantly |
| `Carry Limit` | whole number | 0–250 | how much one person carries; 0 means it can never be moved |
| `Stack Limit` | whole number | 0–2000 | pile cap outdoors |
| `Double Stack Limit` | whole number | 0–3000 | pile cap in proper storage; below `Stack Limit` shrinks storage |
| `Resource Tier` | `Meta`, `Basic`, `Advanced`, `Military`, `Trash` | | |
| `Category` | `Food`, `Seeds`, or empty | | removing `Food` from everything edible means the crew can never eat |
| `Always Degrades` | `TRUE`/`FALSE` | | spoils even under a roof |
| `Explosiveness` | whole number | 0, 2 or 3 | 0 is inert |
| `Flammable` | `TRUE`/`FALSE` | | |
| `VariantAmountMapping` | `/`-list of whole numbers | `1/2` or `1` | picks the pile's look |

#### `WorkbenchProjectData` - crafting recipes

Built-in file: [WorkbenchProjectData.csv](../assets/csv/WorkbenchProjectData.csv)

The row id is `<Workbench>.<Output>`. Rows cannot be added, so this changes existing recipes rather than
introducing new ones.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Workbench Type` | workbench name | `FieldKitchen`, `IndoorKitchen`, `SawStation`, `Brickstation`, `CementMixer`, `MetalworksWorkbench`, `CanningStation`, `ElectronicsWorkbench`, `TailorStation`, `EspionageRadio`, `WaterCooker`, `HerbDryer` or `Distillery` | |
| `Output Resource Type` | resource name | `AntiAirAmmo`, `Bricks`, `Camouflage`, `Cement`, `Electronics`, `FoodRations`, `Fuel`, `GunAmmo`, `Intel`, `LuxuryGoods`, `Machinery`, `Meals`, `Metal`, `PlaneBombs`, `Planks`, `PurifiedWater`, `RepairParts`, `SimpleMedicine`, `StrongMedicine` or `Tarp` | |
| `Output Resource Amount` | whole number | 1–200 | |
| `Input Resource Type` | `/`-list of resources, or `None` | `None` on 3 rows; otherwise 1–3 of `Clay`, `Electronics`, `Food`, `Herbs`, `LuxuryGoods`, `Machinery`, `Meals`, `Metal`, `PurifiedWater`, `RawWater`, `Sandbags`, `SimpleMedicine`, `Tarp` or `Wood`, e.g. `Food/RawWater` | `None` means made from nothing |
| `Input Resource Amount` | `/`-list of whole numbers | 1–3 entries, each 1–10, e.g. `2/2`; `0` on the 3 `None` rows | **must have as many entries as the type list** |
| `Time To Craft` | whole number | 10–180 | in-game minutes of work, by one crew member at a time |
| `Valid Entry` | `TRUE`/`FALSE` | `TRUE` on every row | left over; the game does not read it |

#### `ShipmentData` - the supply catalogue

Built-in file: [ShipmentData.csv](../assets/csv/ShipmentData.csv)

One row per orderable item.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Shipment Type` | `Resource` or `Prop` | | |
| `Category` | `Military`, `Miscellaneous` or `Large` | | **capitalisation matters** - `military` is refused |
| `Amount` | whole number | 1–5000 | units delivered per slot |
| `Slots` | whole number | 1–4 | more slots than any rank offers makes the item unorderable |

### Crew

#### `CharactersInitialStats` - starting skills per job

Built-in file: [CharactersInitialStats.csv](../assets/csv/CharactersInitialStats.csv)

Rows are job and crew role names: `Pilot`, `Gunner`, `BombAimer`, `FlightEngineer`, `Navigator`,
`RadioOperator`, `RAFAirCrew`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`, `AAFLabour`, `None`,
`Custom`.

Columns are the six skills - `Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating` - and
the value is a **rank, 0 to 6**, not a point total. `0` is Untrained and `6` is Ace. Keep it inside that
range; the built-in rows use 0–2. `Endurance` also sets maximum health, which is why every row has at least `1` there.

#### `CharactersStatsRankProgression` - points per rank

Built-in file: [CharactersStatsRankProgression.csv](../assets/csv/CharactersStatsRankProgression.csv)

Rows must stay `Untrained`, `Rank1`, `Rank2`, `Rank3`, `Rank4`, `Rank5`, `Ace`. `LevelUpPoints` (0, 10, 14, 22, 36, 58, 90) is the
points total at which that rank is reached, and the rank is picked as the highest one a character has passed
- so **the values must ascend**. Out of order, crew get stuck low or jump straight to Ace.

#### `CharacterStatsCheck` - what a rank is worth

Built-in file: [CharacterStatsCheck.csv](../assets/csv/CharacterStatsCheck.csv)

Rows are the seven ranks `Untrained`, `Rank1`, `Rank2`, `Rank3`, `Rank4`, `Rank5`, `Ace`. For each of the six skills there are two columns: `<Skill>Value` is a flat
bonus added to a mission roll, `<Skill>Percentage` is a **fraction** - `0.25` means 25%. Writing `25` gives a
2500% bonus. Column names cannot be renamed.

#### `CharacterJobPriority` - what each job is willing to do

Built-in file: [CharacterJobPriority.csv](../assets/csv/CharacterJobPriority.csv)

Rows are the job names: `None`, `Custom`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`,
`AAFLabour`, `RAFAircrew`.

There is one column per kind of work - `Building`, `Gardening`, `CraftingAndRepairs`, `Labor`, `Cooking`,
`Medicine`, `PlaneWork`, `Harvest`, `BaseSafety`, `Leisure`, `UseRecreationalItem`, `Socialize`,
`ConsumeLuxuryGood`, `Train`, `Sleep`, `PilotPlane`, `FunctionalGroup`, `Emergency` - holding a priority:
`0` means the job never does this kind of work, `1` is the highest priority and `3` the lowest. (A medic has
`Building 0` and `Medicine 1`.) No column may be dropped or renamed.

These numbers also **identify** a job: a crew member whose priorities match a row exactly is that job, and one
matching none is `Custom`. Give two jobs identical priorities and the game can no longer tell them apart.

#### `CharactersData` - names, nicknames and ranks

Built-in file: [CharactersData.csv](../assets/csv/CharactersData.csv)

Six of the eight rows are long lists - first names, surnames, nicknames, base crew ranks, pilot ranks - and
cannot be changed.

The two you can change are the pilot ranks themselves, where `Goal` is how many successful missions earn the
promotion:

| Row | `Value` | `Goal` |
|---|---|---|
| `OfficerCadet` | 2 | 3 |
| `PilotOfficer` | 3 | 10 |

#### `MoraleValues`

Built-in file: [MoraleValues.csv](../assets/csv/MoraleValues.csv)

Name and value, all numbers: `BaseMoraleBufferDays`, `MoraleLevelMin` (-100), `MoraleLevelMax` (100),
`LeisureThreshold`, `MoraleTrendTreshold`, `MoraleBreakingThreshold`, `MoraleEffectPositiveThreshold`,
`MoraleEffectNegativeThreshold`, `AirBaseMoraleGameOverThreshold`.

Setting `AirBaseMoraleGameOverThreshold` above `MoraleLevelMax` loses the run immediately; putting
`MoraleLevelMin` above `MoraleLevelMax` leaves every limit inverted.

#### `MoraleInfluenceValues` - what changes a crew member's mood

Built-in file: [MoraleInfluenceValues.csv](../assets/csv/MoraleInfluenceValues.csv)

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Itentifier` | row id (note the spelling) | `Sleep`, `Eat`, `WorkOnWorkbench`, `Stockpile`, `Build`, `Harvest`, `Chill`, `ConsumeLuxuryGoods`, `UseRadio`, `SaluteTheFlag`, `UsePlanningBoard`, `Panic`, `Rage`, `Collapse`, `Grieve`, `Bury`, `UseTrainingObject`, `Socialize`, `UseRecreationalItem`, `Work`, `Train`, `Early`, `Mid`, `Late`, `Living`, `MissionCancelled`, `MissionCompleted`, `WarNews`, `BaseAttacked`, `Death`, `Recover` or `RecoverInBed` | |
| `IdentifierType` | `Task`, `TaskGroup`, `TaskCategory`, `WarPhase`, `GameEvent`, `-` | | a type that does not suit the id means the row is ignored |
| `Parameter` | the variant key; comma-separates aliases | `default`; `Prop.Bed`, `Prop.BedMetal`, `Prop.BedWood`, `Prop.BilliardTable`, `Prop.Dartboard`, `Prop.Guitar`, `Prop.Piano`; `ResourceType.Food`, `ResourceType.FoodRations`, `ResourceType.Intel`, `ResourceType.LuxuryGoods`, `ResourceType.Meals`, `ResourceType.PurifiedWater`, `ResourceType.RawWater`; `CharacterClass.AirCrew`, `CharacterClass.BaseCrew`; `InfluenceOutcome.Good`, `InfluenceOutcome.Bad`; and one row with two aliases, `Prop.Jukebox, Prop.Gramophone` | **no alias may be listed twice** |
| `Raw Parameter` | a note | | not read by the game |
| `Confidence` / `Mood` / `Energy` | numbers | `Confidence` -10 to 50, `Mood` -30 to 50, `Energy` -20 to 50 | |
| `Influence Type` | `Timed` or `OnEventTrigger` | | |

`Timed` values apply every tick and are therefore much smaller than `OnEventTrigger` ones. Copying a `+20`
event value into a `Timed` row pins a crew member's mood to the ceiling within a minute.

Six rows hold one variant per line and cannot be changed at all: `Sleep`, `Eat`, `WorkOnWorkbench`,
`UseRecreationalItem`, `MissionCompleted`, `Death`.

### Missions and time

#### `FlightMissionData` - the mission modifiers

Built-in file: [FlightMissionData.csv](../assets/csv/FlightMissionData.csv)

This table decides how the state of an aircraft and its crew affects a mission. The game checks each
aircraft and crew member against these rows. When a measured value falls inside a row's `ThresholdRange`, that
row's modifier applies to the aircraft. The mission briefing lists each one, and they feed the success estimate.
There are two kinds:

- A `SkillRollModifier` shifts the aircraft's mission stats (fight, bomb, recon and the others). Its
  `ModifierRange` is added to the lowest and highest value each stat can roll, so `0/-10` lowers the best
  possible roll by 10 and `2/0` raises the worst one by 2.
- A `NoFlightModifier` stops the aircraft from being sent at all.

The row id names what is being measured:

- `AirplaneIntegrity` - percent of the aircraft's starting integrity that remains
- `AirplaneHealth` - its health
- `AirplaneFuel` - its fuel level; `0` means an empty tank
- `Mood`, `Energy`, `Confidence` - each crew member's value, from -100 to 100, matched against `Parameter` by
  crew role
- `SeatsConfiguration`, `CrewHealth`, `CrewOnFire` - yes/no checks, where `1` means the problem is present: a
  crew member in a seat that does not match their role, one who is injured, or one on fire

For each measured value, the first row whose range and role match is the one used.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `ModifierCategory` | a label | `low`, `high`, `zero`, `critical` or `mismatch` | |
| `ModifierType` | `SkillRollModifier` or `NoFlightModifier` | | |
| `ModifierRange` | `min/max` whole numbers | `0/-10`, `0/-5`, `0/-3`, `0/-2`, `0/0`, `1/0` or `2/0` | added to the lowest/highest stat roll; ignored by `NoFlightModifier` rows |
| `Parameter` | space-separated crew roles, or `Default` | `Default`, `CrewRole.Pilot`, all six roles, or the five roles other than `CrewRole.Pilot` | every role must carry the `CrewRole.` prefix - a bare `Pilot` never matches, and neither does an unknown role |
| `ThresholdRange` | `min/max` whole numbers | `-100/-90`, `-89/-50`, `0/0`, `1/1`, `1/40` or `50/100` | the range of measured values this row covers |

`NoFlightModifier` is the hard block that grounds an aircraft - out of fuel, or a crew member at rock-bottom
mood. Widening its `ThresholdRange` grounds your whole squadron; setting it to something unreachable such as
`-1000/-999` effectively switches it off.

Rows spanning several lines and therefore unchangeable: `AirplaneIntegrity`, `AirplaneHealth`, `Mood`,
`Energy`, `Confidence`.

#### `TaskValues` - durations and thresholds per task

Built-in file: [TaskValues.csv](../assets/csv/TaskValues.csv)

Three columns: the task id, a `Variable Name` and a `Value`.

`Variable Name` is the key the game looks the setting up by, so **only `Value` can be changed**. The names in
use are `Duration` (minutes), `Distance`, `Chance`, `ExperienceGain`, `HealthAmount`, `IntegrityAmount`,
`IntegrityPenalty`, `ScheduleThreshold`, `ScheduleThresholdPercentage`, `ResourceToFuelRatio`, `Targets`,
`Initiation` and `Active`.

Tasks with several settings take up several lines and cannot be changed. These are: `Chat`, `Chill`, `Panic`,
`AirAttackPanic`, `CelebrateSuccessfulMission`, `BreakThings`, `RepairAirplane`, `MaintainAirplane`, `Refuel`,
`RepairEquipment`, `RefillAirplaneAmmo`, `UseTrainingObject`, the six `…Simple…` and six `…Advanced…` training
tasks, and `BeOnFire`. Everything else - `UseRadio`, `Eat`, `Salute`, `Bury`, `Recover`, `MonitorAirspace` and
the rest - has a single setting, almost always `Duration` (`RefillEquipmentAmmo` has only
`ScheduleThresholdPercentage`), and can be changed normally.

`Value` also accepts text (one built-in row names a chair), so a non-number in a numeric setting is accepted
and then fails when the task runs. This is the one place in this table where you can still write nonsense.

#### `DaySchedule` - the phases of a day

Built-in file: [DaySchedule.csv](../assets/csv/DaySchedule.csv)

Four rows, `0`–`3`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Phase` | `Work`, `Leisure`, `Sleep` | by row: `Sleep`, `Leisure`, `Work`, `Leisure` | `Alert` and `None` are also accepted but are not meant for the schedule |
| `StartHour` | whole number, inclusive | by row: 0, 5, 7, 22 | |
| `EndHour` | whole number, exclusive | by row: 5, 7, 22, 24 | |

The four spans are expanded hour by hour, and **every hour from 0 to 23 must be covered by exactly one row**.
With a gap or an overlap, the hourly phase lookup throws an error and the base stays in whatever phase it was
in before - a broken state, not a defined "no phase". A row whose `Phase` is misspelled is skipped with a
warning, which leaves a gap. Keep the spans continuous from 0 to 24, without overlaps.

#### `DayNightSystemData` - sun and shadows

Built-in file: [DayNightSystemData.csv](../assets/csv/DayNightSystemData.csv)

Name and value, all numbers, purely visual.

| Row | Meaning | Built-in |
|---|---|---|
| `Morning Time`, `Dawn Time`, `Day Time`, `Evening Time`, `Dusk Time`, `Night Time` | hour each lighting stage begins | by row: 4, 7, 10, 17, 22, 23 |
| `Sun Min Rotation` / `Sun Max Rotation` | sun elevation sweep, degrees | 15 / 165 |
| `Sun Yaw Offset` | compass rotation | -90 |
| `Sun Tilt` | degrees | 10 |
| `Shadow Day Intens` / `Shadow Night Intens` | shadow strength | 0.85 / 0 |

Keep the six time rows ascending and within 0–23, or the lighting stages flip back and forth.

#### `GameGoalAlerts` - when the game warns the player

Built-in file: [GameGoalAlerts.csv](../assets/csv/GameGoalAlerts.csv)

Name and value, all numbers, alerts only: `LowMoraleThreshold` (-50), `CriticalMoraleThreshold` (-65),
`LowFoodThreshold` (20), `FewLeisureItemsThreshold` (5), `MissionTimerMinutesThreshold` (150),
`LowWaterThreshold` (20).

### General

#### `Variables` - the global number bag

Built-in file: [Variables.csv](../assets/csv/Variables.csv)

Name and value, 86 entries, each read by whichever part of the game needs it.

This column accepts **anything**, because a few entries hold text or a `min-max` range rather than a number.
Write `abc` where a number belongs and it is accepted, then read as `0` - the feature quietly stops working
and the [log](../start/troubleshooting.md#find-the-playerlog) carries an error. This is the table to be most careful with.

Entries worth knowing before you change them:

- `TimeTickInterval` (0.6666) - real seconds per in-game minute. Halving it doubles the speed of the entire
  game, including every timer balanced against it.
- `AirplanesLimit` (24) - how many aircraft a base may own.
- `CharacterBaseHealth` (7) - plus the Endurance rank, this is a crew member's maximum health. Below
  `CharacterHeavyInjuryThreshold` (3) everyone starts badly injured.
- `MaxVictoryPoints` (12) - the aircraft-ordering budget.
- `ScrambleFuelNeeded` (80) - flat fuel per scramble, whatever the aircraft.
- `AttackHourMin` / `AttackHourMax` (12/23) - pulled back into 1–23 if you go outside it.
- `DiverBombFiresCount`, `BomberBombFiresCount`, `CharredTerrainRevertTimeDays` - these three are `min-max`
  ranges, not single numbers.

Eight entries are left over and **nothing reads them**, so changing them does nothing at all:
`AttackedCharacterId`, `BikeMovementSpeedMultiplier`, `LichfieldIntroCrewMembersCount`,
`AirplaneIntegrityModifierTreshold`, `AirplaneHealthModifierTreshold`, `AirAttackFighterHealth`,
`AirAttackDiverHealth`, `AirAttackBomberHealth`.

#### `FeedbackVariables`

Built-in file: [FeedbackVariables.csv](../assets/csv/FeedbackVariables.csv)

The in-game feedback form: `API Endpoint`, `Feedback Character Limit`, `Screenshot Height`, `Survey Link`,
`Survey Link Demo`, `Survey Opened Player Prefs`. There is no reason for a gameplay mod to touch this, and
pointing `API Endpoint` elsewhere sends players' feedback to that address.

---

## Worked example

`Mods/my_balance_mod/CSV/ResourceCost.json` - give the storage box a build cost, make wooden walls cheaper, and
drop the chair's tarp cost:

```json
{
  "Commands": [
    { "Command": "Add", "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } },
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } },
    { "Command": "Remove", "Id": "Chair", "Columns": [ "Tarp" ] }
  ]
}
```

`Mods/my_balance_mod/CSV/Variables.json` - speed up turbo mode and make crew chatter more common. `Value`
in this table takes any text, so a typo such as `0,6` is accepted silently and then read as `0` - check the
number twice:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "TurboTimeScaleMultiplier", "Cells": { "Value": 20 } },
    { "Command": "Replace", "Id": "RandomActionChatProbability", "Cells": { "Value": 0.6 } }
  ]
}
```

The same two changes as `Mods/my_balance_mod/CSV/Variables.csv`:

```text
Name,Value
TurboTimeScaleMultiplier,20
RandomActionChatProbability,0.6
```
