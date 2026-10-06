---
name: csv-tweak
description: Change Ground of Aces game numbers (costs, aircraft speed, fuel, morale effects, base values) with a CSV mod in mods/<mod_id>/CSV/. Use when the user says "make X cheaper/faster/stronger", "balance", "change the cost of", "tweak stats", "rebalance", "CSV".
---

# CSV tweak

Read `AGENTS.md` section 10. The only source of truth for tables, columns and allowed values is `docs/en/data/csv.md`. Never guess a table or column name.

## 1. Understand the idea

1. **Mod id**.
2. **What to change** - find the table and column in `docs/en/data/csv.md`, and the row id (e.g. `wall_wood`, `spitfire`). Tell the user the current range listed there and suggest a value inside the allowed limits.

## 2. Scaffold

Copy `templates/csv-tweak/` to `mods/<mod_id>/`. Set `Id` and `Name` in `config.json`. Rename or replace `CSV/ResourceCost.json` with `CSV/<Table>.json`.

## 3. Write

- Prefer the `.json` command format: `{"Commands": [{"Command": "Replace", "Id": "<row>", "Cells": {"<Column>": <value>}}]}`.
- File name = table name, exact capitals. Column names exact, spaces included.
- `Add` and whole-row `Remove` only in `ResourceCost` and `PropsInfluence`.
- Values must have the kind the column already holds (number, `TRUE`/`FALSE`, `min-max`). Respect the limits in the docs (e.g. `Stealthiness` max at most 100).
- Plain JSON: no comments, no trailing commas, max 200 commands.
- Only use `.csv` whole rows when the user wants to edit in a spreadsheet; the header must list exactly the table's columns.

## 4. Validate

The validator does not check CSV yet. Run it anyway (it still checks any other content), then:

- parse every JSON file (`python -c "import json,sys; json.load(open(sys.argv[1]))" <file>`),
- compare every table, column and row id against `docs/en/data/csv.md` by hand.

## 5. Install and hand over

Follow `install-mod`. Tell the user: save, Options -> Quit to main menu, open Mods (if the mod or its `CSV/` folder is new, press **Refresh** - opening the window alone does not rescan; check the mod is on), then load the save again - CSV changes apply when a level loads. Tell them where to look to see the new value. If nothing changed, `read-log` (look for `[Mod <mod_id>]` lines; informational ones may only appear in development builds).
