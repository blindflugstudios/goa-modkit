# CSV tables

Most of the numbers that drive Ground of Aces - what a building costs, how fast a plane flies, how much a meal lifts a crew member's mood - live in data tables. A mod can change any of them without touching the game's code, by dropping a small file into its own folder.

This page is the complete reference: where the files go, what the two file formats look like, what the game checks before it accepts a value, and what every table and column means. Every table section in [The tables](#the-tables) starts with a link to the built-in file, so you can open the real thing or save it and copy its header row.

!!! note
    Nothing here can permanently damage your game. A value the game cannot use is refused and written to the log with the reason; the built-in value stays. Removing the mod folder restores everything.

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

A file is named after the table it changes, matched **exactly**, capital letters included: `VehicleData.csv`, never `vehicledata.csv`. A file naming a table that does not exist is skipped, and the log says so.

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

Every accepted change and every refusal is one line in the game's log, `Player.log` (where to find it: [How mods work](../basics/mods.md#seeing-your-changes)). On Windows there is also an HTML version in the same folder that is easier to read. The label at the start of each line is the mod's id.

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
    These lines are written as information and warnings. The released game writes mainly errors to its log, so you may not see them there. In that case check the effect in the game instead - load a level and look at the value you changed.

A misspelled table name or a header row that does not match still produces a `skipped:` line naming the file. **If you see no `[Mod ...]` lines at all and the change does not show**, the game did not pick the mod up: the `CSV/` folder was still empty when the game started (press **Refresh** in the Mods window), the mod is switched off in the Mods window, or the mod folder is a symbolic link or junction, which is never followed.

### Finding a table's column headers

The game ships header templates for four tables (`BuildingComponents`, `PropsInfluence`, `ResourceCost` and `VehicleData`) in `GroundOfAces_Data/StreamingAssets/Modding/Templates/` inside the installation folder (on macOS: `GroundOfAces.app/Contents/Resources/Data/StreamingAssets/Modding/Templates/`). For the rest, the column list is on this page, and every table section links the built-in file. Or ask the game: write a deliberately wrong header, load once, and the log prints the columns it expected.

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

### Aircraft and base

#### `VehicleData` - aircraft

Built-in file: [VehicleData.csv](../assets/csv/VehicleData.csv)

One row per aircraft. Rows cannot be added or removed.

| Column | Value | Built-in range | Notes |
|---|---|---|---|
| `Name` | localization key | `airplane/spitfire` | must not be empty |
| `Type` | `Fighter`, `Bomber`, `MultiRole`, `Special` | | |
| `Crew` | comma list of seats; repeat a role for two seats | `Pilot`, `"Pilot,Gunner,Navigator"` | roles: `Pilot`, `Gunner`, `Navigator`, `BombAimer`, `FlightEngineer`, `RadioOperator` |
| `Runway Tier` | whole number | 1–5 | above 5 and no airstrip can serve it |
| `Parking Size` | whole number | 0–2 | above 2 and it can never park |
| `Victory Points Cost` | whole number | 0–12 | 0 makes it free |
| `Movement Speed` | whole number | 5 | taxi speed; 0 and it never reaches the runway |
| `Landing Length` | whole number | 60–170 | longer than any buildable strip and it can never land |
| `Health` | whole number | 100 | |
| `Initial Integrity` | whole number | 1000 | hours of wear the aircraft can take before it is worn out (1000 h ≈ 41 days) |
| `Fuel Capacity` | whole number | 200–1260 | |
| `Voxel Size` | `AxBxC` | `10x0x10` | |
| `Fight Power` | `min-max` | `0-0` … `43-60` | `0 ≤ min ≤ max`, and `max` at most **twice the highest built-in value** |
| `Bomb Power` | `min-max` | `0-0` … `50-80` | same |
| `Recon Power` | `min-max` | `5-10` … `42-60` | same |
| `Manoeuvrability` | `min-max` | `2-10` … `28-50` | same |
| `Transport Capacity` | `min-max` | `1-5` … `60-90` | same |
| `Stealthiness` | `min-max` | `10-48` … `88-98` | same |
| `Wreck Resource Type` | `/`-list of resources | `Metal/RepairParts` | both wreck columns set, or both empty |
| `Wreck Resource Amount` | `/`-list of whole numbers | `10/5` | same length as the type list |
| `Low Caliber Ammo Capacity` | whole number | 0–3300 | `GunAmmo` carried; 0 = none |
| `High Caliber Ammo Capacity` | whole number | 0–300 | `AntiAirAmmo`; 0 = none |
| `Plane Bombs Capacity` | whole number | 0–32 | `PlaneBombs`; 0 = none |

!!! warning
    An aircraft already parked at your base keeps the health, integrity and fuel capacity it was built with.
    Only newly delivered aircraft pick up changed values - so a save made while a mod was active keeps that
    mod's numbers even after you remove it.

#### `AirBaseData` - the HQ rank ladder

Built-in file: [AirBaseData.csv](../assets/csv/AirBaseData.csv)

Rows `1`–`6`, one per base category. All six must exist and their ids cannot change.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Airstrip Tier` | whole number | 1,2,3,4,5,5 | required to reach the rank |
| `Minimum Airstrip Count` | whole number | 1–5 | |
| `Minimum Parking Count` | whole number | 1–20 | |
| `Missions Per Week` | whole number | 6–18 | slots the week offers; 0 and no missions are scheduled |
| `Minimum Missions Per Week` | whole number | 2–10 | above `Missions Per Week` makes the quota impossible |
| `Minimum Success Rate` | fraction, not percent | 0.4–0.8 | above 1 is unachievable |
| `Available Shipment Slots` | whole number | 4–8 | 0 disables supply |

#### `AirstripTiers`

Built-in file: [AirstripTiers.csv](../assets/csv/AirstripTiers.csv)

Rows `1`–`5`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Length` | whole number | 80,120,140,160,200 | tiers match on "length or more", so keep them ascending |
| `Width` | whole number | 12,14,18,22,26 | same |
| `Material` | text | `dirt`, `sand`, `gravel`, `concrete`, `tarmac` | **must not repeat another tier's material**; it also names the `ResourceCost` row that prices the surface |
| `Biome Id` | whole number | 6,20,22,15,13 | ground painted under the finished strip |
| `Build Time` | whole number | 5,2,2,2,2 | in-game minutes of work per tile for one crew member; two workers halve it |

#### `Biomes`

Built-in file: [Biomes.csv](../assets/csv/Biomes.csv)

Rows `0`–`23`, the ground types. All columns are numbers, so this table is easy to tune safely.

| Column | Built-in | Notes |
|---|---|---|
| `Airstrip Tier` | 0–5 | tier a runway laid on this ground counts as |
| `Character Speed Modifier` | 1 … 1.2 | 0 freezes anyone standing on it |
| `Airplane Speed Modifier` | 0.5 … 1.2 | |
| `Degradation Penalty` | 0 … 0.2 | extra wear on goods stored here |
| `Fire Spread Modifier` | 0.5 or 1 | |

#### `ScrambleData` - enemy aircraft in a scramble

Built-in file: [ScrambleData.csv](../assets/csv/ScrambleData.csv)

Rows `Fighter`, `Diver`, `Bomber`. The names cannot change. All columns are whole numbers.

| Column | Built-in |
|---|---|
| `PlaneHealth` | 18, 26, 34 |
| `PlanePower` | 23, 17, 14 |
| `PlaneWinDealDamageMin` / `Max` | 15–120 - damage to your aircraft when the enemy wins |
| `PlaneLooseDealDamageMin` / `Max` | 5–25 - damage when the enemy loses |

#### `AttacksComposition` - what an air raid is made of

Built-in file: [AttacksComposition.csv](../assets/csv/AttacksComposition.csv)

The row id is the raid severity. Normal play reaches **1–25**; rows `99`, `101`, `200` and `300` are not
reached by the normal severity ladder and are kept for special raids. The ranges below describe rows 1–25;
the four special rows go beyond them (`9-9` bombers, `10-10` divers, `0-0` fighters) and point at
themselves in the last two columns.

| Column | Value | Built-in (rows 1–25) | Notes |
|---|---|---|---|
| `Bombers` | `min-max` | `0-0` … `4-6` | whole numbers, `0 ≤ min ≤ max` |
| `Divers` | `min-max` | `0-0` … `6-6` | same |
| `Fighters` | `min-max` | `1-2` … `8-8` | same |
| `LowAttacks` | whole number | 1–14 | severity used instead when the map is set to easier raids - **must name a row this table has** |
| `HighAttacks` | whole number | 2–25 | severity used when the map is set to harder raids - same |

#### `EquipmentData` - AA guns, searchlights, towers

Built-in file: [EquipmentData.csv](../assets/csv/EquipmentData.csv)

Rows are equipment ids: `Bofors40mm`, `Searchlight`, `RadioTower`, `VickersGunAA`, `OerlikonGun`, `Lookout`,
`ControlTowerMetal`, `ControlTowerBrick`, `ControlTowerConcrete`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Range` | number | 10–70 | 0 makes the piece useless |
| `Damage` | number | 0–6 | **`0` switches the whole weapon off** - fire rate, ammo and aiming are then ignored |
| `Fire Rate` | whole number | 0–720 | rounds per minute |
| `Ammo Type` | resource name or `None` | `GunAmmo`, `AntiAirAmmo`, `None`, `0` | anything that is not a resource name (`None`, `0`) means the piece stores no ammo |
| `Ammo Capacity` | whole number | 0–80 | rounds loaded at once |
| `Ammo Load Time` | number | 0–6.5 | seconds to reload |
| `Ammo Storage` | whole number | 0–500 | **`0` means it never draws ammo** |
| `Damage Bonus` | number | 0 or 0.25 | granted to others in range (searchlight) |
| `Firing Angle` | number | 0, 140, 360 | `0` is read as a full circle |
| `Aiming Speed` | number | 0–170 | degrees per second |
| `Range Bonus` | number | 0 or 16 | granted to others in range (lookout) |
| `Attacker Priority` | `Bombers`, `Divers`, `Fighters`, `Nearest`, `None` | | anything else falls back to `None` |

### Building and objects

#### `BuildingComponents` - objects and building parts

Built-in file: [BuildingComponents.csv](../assets/csv/BuildingComponents.csv)

One row per object, wall piece, floor, roof, workbench and piece of equipment. Rows cannot be added or
removed.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Dimensions` | `WxHxD`, or `dynamic/1x0x1` for roofs | `1x3x1`, `1x0x1`, `2x2x2` | |
| `Build Time` | whole number | 0–420 | in-game minutes of work for one crew member; two workers halve it |
| `Health` | whole number | 0–10000 | the huge value marks the indestructible pieces |
| `Associated Task` | task name or `None` | `Sleep`, `Chill`, `UseEquipment`, `PlayPiano`, `UseTrainingObject`, `MonitorAirspace`, `UseRadio`, `SaluteTheFlag`, `Grieve`, `ListenToMusic`, `PlayDartboard`, `PlayGuitar`, `PlayBilliardTable`, `UsePlanningBoard` | pointing an object at a task its art does not fit is allowed, and looks wrong |
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
changes what a tier-3 runway costs per tile.

#### `PropsInfluence` - the mood effect an object radiates

Built-in file: [PropsInfluence.csv](../assets/csv/PropsInfluence.csv)

One row per object that lifts or lowers the mood of crew nearby. **Rows can be added and removed**; an object
without a row simply has no effect.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Buff Name` | localization key | `prop_effects/organised_sleep` | must not be empty |
| `Radius` | number | 0.5–50 | in tiles; the control towers reach 20, 30 and 50 |
| `Associated Tasks Or Action` | comma list of task names | `Sleep`, `"Sleep,Chill"`, `UseEquipment` | must not be empty. A name that matches no task is accepted and the effect simply **never fires** |
| `Effect 1` | `<signed number> <name>` | `+0.5 Mood` … `+10 Mood`, `-1 Mood`, `-1.5 Energy`, `+2 Energy`, `+1 Confidence` | names: `Mood`, `Confidence`, `Energy`; the built-in rows go from `-1.5` to `+10` |
| `Effect 2` | same, or empty | | |
| `Effect 3` | same, or empty | | no built-in row uses it |

The sign is part of the number, so `1 Mood` means `+1`. Names are matched loosely, so `+1 mood` works. A name
other than the three above is stored as a special effect (the game uses `-1 Accident` on the three control
towers); an invented name is accepted and does nothing.

#### `MapObjects` - trees, rocks, ponds and other harvestables

Built-in file: [MapObjects.csv](../assets/csv/MapObjects.csv)

One row per world object. Ids are used by map files and cannot change.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `LocKey_Name` | localization key | `map.obj.tree.name` | |
| `LocKey_Description` | localization key | | |
| `Dimensions` | `WxHxD` | `1x4x1`, `2x2x2`, `3x1x3` | |
| `Resource Harvested` | resource name, or empty | `Wood`, `Stone`, `Herbs`, `Food`, `RawWater`, `Clay`, `Sandbags`, `Metal`, `Planks`, `Fuel`, seeds | empty means nothing to harvest |
| `Farming Time` | whole number | 0–400 | in-game minutes of work per harvest for one crew member; two workers halve it |
| `Resource Amount` | whole number | 0–50 | yield per harvest |
| `Resource Total` | whole number | 0–500 | total before it is used up |
| `Limited Harvest Amount` | whole number | 0, 20, 30, 100 | cap for endless sources; 0 = uncapped |
| `Destroyed On Depletion` | `TRUE`/`FALSE` | | `FALSE` with `Refresh Time` 0 leaves something that can never be harvested again |
| `Refresh Time` | whole number | 0–21600 | minutes until it regrows |
| `Health` | whole number | 1–2147483647 | the huge value marks the indestructible ones |
| `Is Fireproof` | `TRUE`/`FALSE` | | making trees fireproof removes fire spread from the map |

#### `GrowingData` - saplings becoming trees

Built-in file: [GrowingData.csv](../assets/csv/GrowingData.csv)

Two rows, `young_tree` and `young_tree_big`.

| Column | Value | Built-in |
|---|---|---|
| `To` | a `MapObjects` id | `tree`, `tree_big` |
| `Min Hours` | whole number | 672 |
| `Max Hours` | whole number | 840 |

A sapling that is already on the map when a save is loaded draws its remaining time between half of
`Min Hours` and `Max Hours`; only newly planted ones use the full minimum.

#### `GardeningData` - the four crops

Built-in file: [GardeningData.csv](../assets/csv/GardeningData.csv)

Rows `grain`, `beans`, `potato`, `tomato`.

| Column | Built-in | Notes |
|---|---|---|
| `Growth` | 3, 6, 15, 10 | watered days until harvest - the plant gains one at midnight for every day its tile was watered; 0 is harvestable instantly |
| `Food` | 3, 4, 20, 7 | food per harvest |
| `Seeds` | 2, 5, 3, 1 | seeds per harvest; 0 makes the crop unsustainable |
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
| `Explosiveness` | whole number | 0, 2, 3 | 0 is inert |
| `Flammable` | `TRUE`/`FALSE` | | |
| `VariantAmountMapping` | `/`-list of whole numbers | `1/2`, `1` | picks the pile's look |

#### `WorkbenchProjectData` - crafting recipes

Built-in file: [WorkbenchProjectData.csv](../assets/csv/WorkbenchProjectData.csv)

The row id is `<Workbench>.<Output>`. Rows cannot be added, so this changes existing recipes rather than
introducing new ones.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `Workbench Type` | workbench name | `FieldKitchen`, `IndoorKitchen`, `SawStation`, `Brickstation`, `CementMixer`, `MetalworksWorkbench`, `CanningStation`, `ElectronicsWorkbench`, `TailorStation`, `EspionageRadio`, `WaterCooker`, `HerbDryer`, `Distillery` | |
| `Output Resource Type` | resource name | | |
| `Output Resource Amount` | whole number | 1–200 | |
| `Input Resource Type` | `/`-list of resources, or `None` | `Food/RawWater`, `Metal`, `None` | `None` means made from nothing |
| `Input Resource Amount` | `/`-list of whole numbers | `2/2`, `0` | **must have as many entries as the type list** |
| `Time To Craft` | whole number | 10–180 | in-game minutes of work for one crew member; two workers halve it |
| `Valid Entry` | `TRUE`/`FALSE` | `TRUE` | left over; the game does not read it |

#### `ShipmentData` - the supply catalogue

Built-in file: [ShipmentData.csv](../assets/csv/ShipmentData.csv)

One row per orderable item.

| Column | Value | Notes |
|---|---|---|
| `Shipment Type` | `Resource` or `Prop` | |
| `Category` | `Military`, `Miscellaneous` or `Large` | **capitalisation matters** - `military` is refused |
| `Amount` | whole number, 1–5000 | units delivered per slot |
| `Slots` | whole number, 1–4 | more slots than any rank offers makes the item unorderable |

### Crew

#### `CharactersInitialStats` - starting skills per job

Built-in file: [CharactersInitialStats.csv](../assets/csv/CharactersInitialStats.csv)

Rows are job and crew role names: `Pilot`, `Gunner`, `BombAimer`, `FlightEngineer`, `Navigator`,
`RadioOperator`, `RAFAirCrew`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`, `AAFLabour`, `None`,
`Custom`.

Columns are the six skills - `Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating` - and
the value is a **rank, 0 to 6**, not a point total. `0` is Untrained and `6` is Ace. Keep it inside that
range. `Endurance` also sets maximum health, which is why every row has at least `1` there.

#### `CharactersStatsRankProgression` - points per rank

Built-in file: [CharactersStatsRankProgression.csv](../assets/csv/CharactersStatsRankProgression.csv)

Rows must stay `Untrained`, `Rank1` … `Rank5`, `Ace`. `LevelUpPoints` (0, 10, 14, 22, 36, 58, 90) is the
points total at which that rank is reached, and the rank is picked as the highest one a character has passed
- so **the values must ascend**. Out of order, crew get stuck low or jump straight to Ace.

#### `CharacterStatsCheck` - what a rank is worth

Built-in file: [CharacterStatsCheck.csv](../assets/csv/CharacterStatsCheck.csv)

Rows are the same seven ranks. For each of the six skills there are two columns: `<Skill>Value` is a flat
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
| `Itentifier` | row id (note the spelling) | `Sleep`, `Chill`, `Panic`, `BaseAttacked` | |
| `IdentifierType` | `Task`, `TaskGroup`, `TaskCategory`, `WarPhase`, `GameEvent`, `-` | | a type that does not suit the id means the row is ignored |
| `Parameter` | the variant key; comma-separates aliases | `default`, `Prop.Bed`, `ResourceType.Meals` | **no alias may be listed twice** |
| `Raw Parameter` | a note | | not read by the game |
| `Confidence` / `Mood` / `Energy` | numbers | -30 … 50 | |
| `Influence Type` | `Timed` or `OnEventTrigger` | | |

`Timed` values apply every tick and are therefore much smaller than `OnEventTrigger` ones. Copying a `+20`
event value into a `Timed` row pins a crew member's mood to the ceiling within a minute.

Six rows hold one variant per line and cannot be changed at all: `Sleep`, `Eat`, `WorkOnWorkbench`,
`UseRecreationalItem`, `MissionCompleted`, `Death`.

### Missions and time

#### `FlightMissionData` - the mission modifiers

Built-in file: [FlightMissionData.csv](../assets/csv/FlightMissionData.csv)

The row id names what is being measured: `AirplaneIntegrity`, `AirplaneHealth`, `AirplaneFuel`, `Mood`,
`Energy`, `Confidence`, `SeatsConfiguration`, `CrewHealth`, `CrewOnFire`.

| Column | Value | Built-in | Notes |
|---|---|---|---|
| `ModifierCategory` | a label | `low`, `high`, `zero`, `critical`, `mismatch` | |
| `ModifierType` | `SkillRollModifier` or `NoFlightModifier` | | |
| `ModifierRange` | `min/max` whole numbers | `0/-5`, `2/0` | bonus applied to the roll |
| `Parameter` | space-separated crew roles, or `Default` | `Default`, `CrewRole.Pilot` | every role must carry the `CrewRole.` prefix - a bare `Pilot` never matches, and neither does an unknown role |
| `ThresholdRange` | `min/max` whole numbers | `1/40`, `-100/-90`, `50/100` | the range of measured values this row covers |

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

| Column | Value | Built-in |
|---|---|---|
| `Phase` | `Work`, `Leisure`, `Sleep` | | (`Alert` and `None` are also accepted but are not meant for the schedule) |
| `StartHour` | whole number, inclusive | 0, 5, 7, 22 |
| `EndHour` | whole number, exclusive | 5, 7, 22, 24 |

The four spans are expanded hour by hour, so **gaps and overlaps both matter**: an hour no row covers has no
phase at all and the crew idle through it. Keep the spans continuous from 0 to 24.

#### `DayNightSystemData` - sun and shadows

Built-in file: [DayNightSystemData.csv](../assets/csv/DayNightSystemData.csv)

Name and value, all numbers, purely visual.

| Row | Meaning | Built-in |
|---|---|---|
| `Morning Time`, `Dawn Time`, `Day Time`, `Evening Time`, `Dusk Time`, `Night Time` | hour each lighting stage begins | 4, 7, 10, 17, 22, 23 |
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
and the log carries an error. This is the table to be most careful with.

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
