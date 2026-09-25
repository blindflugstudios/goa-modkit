# Template: CSV tweak

Changes numbers in the game's data tables. This one makes the wooden wall cost one plank.

```
csv-tweak/
  config.json
  CSV/
    ResourceCost.json    file name = table name, exact capitals
```

## Use it

1. Copy the folder to `mods/<your_mod_id>/` and set your id in `config.json`.
2. Name each file exactly after the table it changes (`VehicleData.json`, not `vehicledata.json`).
3. Column names inside `Cells` must match the table exactly, spaces included.
4. Only `Replace` works in most tables. `Add` and whole-row `Remove` work only in `ResourceCost` and `PropsInfluence`.
5. Tables and columns: `docs/en/data/csv.md`.

The validator does not check CSV files yet; check the JSON is valid (no comments, no trailing commas).

CSV changes apply when a level loads: save, quit to the main menu, open **Mods** (it rescans the folder), then load the save again.
