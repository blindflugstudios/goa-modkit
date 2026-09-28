# Table command files

There is no spreadsheet window inside Ground of Aces. Table changes are made with files: you write a short list of commands, `Add`, `Replace` or `Remove`, into a `<Table>.json` file in your mod's `CSV/` folder, and every time a level loads, the game carries them out on its data tables, one by one, checking each change before it writes it.

This page explains how those commands behave in detail. The format itself, the list of tables and the rules for each column are on [CSV tables](csv.md); read that first.

## Quick start

Make the Gladiator carry more fuel and the wooden wall cheaper. Two files in one mod:

```text
Mods/
  my_balance_mod/
    CSV/
      VehicleData.json
      ResourceCost.json
```

`VehicleData.json`:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350 } }
  ]
}
```

`ResourceCost.json`:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
  ]
}
```

Return to the main menu and load a save: the changes are in. No restart needed.

## How a command is carried out

For every command, in the order they appear in the file, the game:

1. Finds the row by `Id`. Capitalisation of the id does not matter; the table's own spelling is kept.
2. Builds the complete row as it would look after the change, on the side, without touching the real table yet.
3. Fills in the two cells the game completes for you, if your change left them empty: `0` in `ResourceCost`, `None` in `Associated Task` of `BuildingComponents`. Any other empty cell is left empty for the check.
4. Checks the whole row against the table's rules (value types, allowed ranges, references to other tables, see [CSV tables](csv.md)).
5. Only if everything passes, writes the row into the table. Otherwise it writes nothing, logs the reason, and moves on to the next command.

So a rejected command never leaves a half-changed row behind, and one bad command does not stop the others.

## The three commands

### `Replace`: change cells of an existing row

```json
{ "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350, "Movement Speed": 7 } }
```

- Changes only the columns named in `Cells`. Every other cell keeps its current value.
- A cell given as `""`, only spaces, or `null` is cleared. That is only allowed in a column where the game already leaves some row empty; elsewhere the command is refused. Only `ResourceCost` cells (which become `0`) and `Associated Task` (which becomes `None`) are filled in instead.
- The row must already exist. Otherwise: `'...' is not a built-in row; use Add to create one`.
- Every key in `Cells` must be a column of the table, spelled exactly. Otherwise the message lists the table's columns.
- The whole resulting row is checked, not just the cells you named. A row that was fine before stays fine unless your values break a rule.
- A few built-in rows span several lines in the game's own table. They are refused, whether patched cell by cell or shipped as a whole row. Only in `ResourceCost` does a whole-row `<Table>.csv` fix them (see [Rows that take up several lines](csv.md#rows-that-take-up-several-lines)); the multi-line rows of `MoraleInfluenceValues` and `TaskValues` cannot be changed at all.

### `Add`: create a new row

```json
{ "Command": "Add", "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } }
```

- Only in the tables that allow new rows (see [CSV tables](csv.md)). Elsewhere: `new rows are not supported in '...'; only built-in rows can be changed`.
- The id must not exist yet. Otherwise: `'...' already exists; use Replace to change it`.
- Columns you leave out get the table's default or stay empty; the row check then decides whether that is acceptable.

### `Remove`: clear cells, or delete a row

```json
{ "Command": "Remove", "Id": "Chair", "Columns": [ "Tarp" ] }
{ "Command": "Remove", "Id": "Drawer" }
```

- With `Columns`: clears the listed cells, exactly like a `Replace` with empty values.
- Without `Columns`: deletes the whole row. Only in the tables that allow it; elsewhere the log says the rows cannot be removed because saves and other content use their ids.
- `Remove` never takes `Cells`.

## Order

- Inside one file, commands run top to bottom. An `Add` can be followed by a `Replace` of the same row.
- Inside one mod, all `.csv` files are applied before any `.json` file, so commands can refine rows your CSV files brought in.
- Between mods, the mod applied later works on the result of the earlier ones and wins where both touch the same cell. The order is described in [How mods work](../basics/mods.md).

## When changes take effect

Tables are rebuilt from the game's own data and all enabled mods every time a level loads. After editing a command file, save your game, choose **Options → Quit to main menu**, and load the save again. No restart is needed; if in doubt, restart anyway. See [Testing and reloading](../basics/testing.md). A brand-new `CSV/` folder, or a new mod, is only noticed after you open **Mods** in the main menu (press **Refresh**) or restart.

Because the tables are rebuilt from scratch, removing a command, or switching the mod off, restores the original value at the next load. The exception are aircraft already parked at your base: they keep the health, integrity and fuel capacity they were built with, so a save made while the mod was active keeps its numbers (see [`VehicleData`](csv.md#vehicledata-aircraft)).

## Reference

### File

| Rule | Value |
|---|---|
| Location | `Mods/<mod>/CSV/<Table>.json`, directly in `CSV/` |
| File name | The table's name, exactly: `VehicleData.json`, not `vehicledata.json` |
| Root | An object with one key, `Commands`, holding a list |
| Commands per file | At most 200. A longer file is skipped whole. |
| Syntax | Plain JSON: no comments, no trailing commas |

### Command fields

| Field | Type | Used by | Notes |
|---|---|---|---|
| `Command` | text | all | `Add`, `Replace` or `Remove`, any capitalisation. |
| `Id` | text | all | The row id, any capitalisation. Required. |
| `Cells` | object: column name to value | `Add`, `Replace` | Required for those two. Values may be strings, numbers or `true`/`false`; they are read as text. |
| `Columns` | list of column names | `Remove` | Optional. Without it, the whole row is removed. |

### Log messages

Every message starts with `[Mod <mod id>] CSV/<Table>.json`. Applied commands:

```text
[Mod my_balance_mod] CSV/VehicleData.json command 1 replaced cells Fuel Capacity of row 'gladiator'.
[Mod my_balance_mod] CSV/ResourceCost.json command 2 added row 'storage_box'.
[Mod my_balance_mod] CSV/ResourceCost.json command 3 cleared cells Tarp of row 'Chair'.
[Mod my_balance_mod] CSV/PropsInfluence.json command 4 removed row 'Drawer'.
```

Problems with the whole file (nothing in it is applied):

| Message ends with | Meaning |
|---|---|
| `skipped: could not be parsed (...)` | Not valid JSON. The part in brackets points to the spot. |
| `skipped: it holds no "Commands".` | The root key is missing, misspelled, or the list is empty. |
| `skipped: 250 commands exceed the limit of 200.` | Split the commands over several mods, or use a `<Table>.csv`. |
| `skipped: ...` (other reasons) | The file name is not a table that mods may change. |

Problems with one command (only that command is skipped):

| Message ends with | Meaning |
|---|---|
| `rejected: it is empty.` | A `null` in the `Commands` list. |
| `rejected: '...' is not a command; use Add, Replace or Remove.` | Misspelled `Command`. |
| `rejected: it has no "Id".` | `Id` missing or blank. |
| `rejected: Replace needs "Cells".` / `Add needs "Cells".` | `Cells` missing or empty. |
| `rejected: Remove lists the cells to clear in "Columns", not in "Cells".` | Use `Columns` with `Remove`. |
| `rejected: '...' is not a column of ...; available: ...` | Column name misspelled. Copy it from the list in the message. |
| `rejected: '...' is not a built-in row ...` | No row with that id. |
| `rejected: '...' already exists; use Replace to change it.` | `Add` of an id that exists. |
| `rejected:` followed by a rule | The value breaks one of the table's rules, see [CSV tables](csv.md). |

The released game logs only errors to `Player.log`; the full list of lines appears in a development build or in the Unity editor.
