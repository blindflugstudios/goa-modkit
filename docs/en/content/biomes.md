# Biomes

!!! warning "Work in progress"
    Art mods are work in progress. The current alpha does not support them yet, so biome textures from a mod do not show up in the game for now.

A biome is a ground type: the grass, dirt, road, rock, sand or gravel painted across a map with the **Biomes** tool of the [Map Editor](maps.md). The game has 24 of them. A mod can repaint any of them with a new texture, and the change shows on every map, shipped or custom.

A biome mod changes the **look** only. How fast people and aircraft move over the ground, which runway tier it counts as, and similar rules live in the `Biomes` table and are changed with [CSV tables](../data/csv.md).

## Folder layout (preliminary)

This is how the game will read biome art. It is preliminary and may still change.

- `Biomes/` holds one PNG per biome slot, named after the slot's number, directly inside the folder: `8.png` repaints slot 8, the first grass (see the [list](#biome-names)).
- Subfolders and other file names are reported in the log and ignored.
- Biome textures are imported once, when the game starts. After a change, **restart the game**; neither **Refresh** nor the **Enabled** switch in the Mods window re-imports them.

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

## Quick start

Give the first grass a new texture:

```text
Mods/
  my_ground_mod/
    Biomes/
      Terrain-Type_Grass_A/
        albedo.png
```

Restart the game and load a save or start a map. Everywhere the map uses that grass, you now see your texture.

!!! note
    Biome textures are read once, when the game starts. After changing a texture or switching the mod on or off, **restart the game**.

-->

## How it works

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

- `Biomes/` holds one folder per biome you want to repaint, named exactly after the biome (see the [list](#biome-names)). Capitalisation does not matter.
- Each folder needs one file: `albedo.png`, the colour texture.

-->

- A mod cannot add new biomes, only repaint the 24 that exist. A map remembers which biome is painted where by number, so there is nothing a new one could be attached to.
- The biome's surface detail and its burnt look after a fire are not replaced.
- The game's own textures are untouched on disk. When you leave a map, the original ground returns, and switching the mod off (and restarting) brings it back everywhere.

### The texture

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

| Rule | Limit |
|---|---|
| Format | PNG only |
| Size | At most 2048 × 2048 pixels |
| File size | At most 8 MB |
| File name | `albedo.png` |

-->

| Rule | Limit |
|---|---|
| Format | PNG only |
| Size | At most 2048 × 2048 pixels |
| File size | At most 8 MB |

The game scales your texture to the size of its own ground textures, so any size within the limit works; a square image avoids stretching. The texture repeats across the ground, so it should tile seamlessly: the left edge must continue into the right edge, the top into the bottom.

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

Other files in a biome folder (`model.glb`, `destroyed_albedo.png`, ...) mean nothing here. The log says so, and `albedo.png` still loads.

-->

## Biome names

The number is the biome's row in the `Biomes` table. Rows with the same number describe how that ground plays.

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

| Number | Folder name | Ground |
|---|---|---|
| 0 | `Terrain-Type_Dirt_A` | dirt |
| 1 | `Terrain-Type_Dirt_B` | dirt |
| 2 | `Terrain-Type_Dirt_C` | dirt |
| 3 | `Terrain-Type_Dirt_D` | dirt |
| 4 | `Terrain-Type_Dirt_E` | dirt |
| 5 | `Terrain-Type_Dirt_F` | dirt |
| 6 | `Terrain-Type_Dirt_G` | dirt, also laid under parking spots, gardening plots and dirt runways |
| 7 | `Terrain-Type_Dirt_H` | dirt |
| 8 | `Terrain-Type_Grass_A` | grass |
| 9 | `Terrain-Type_Grass_B` | grass |
| 10 | `Terrain-Type_Grass_C` | grass |
| 11 | `Terrain-Type_Grass_D` | grass |
| 12 | `Terrain-Type_Grass_E` | grass |
| 13 | `Terrain-Type_Road_A` | road, also laid under tarmac runways |
| 14 | `Terrain-Type_Road_B` | road |
| 15 | `Terrain-Type_Road_C` | road, also laid under concrete runways |
| 16 | `Terrain-Type_Rock_A` | rock |
| 17 | `Terrain-Type_Rock_B` | rock |
| 18 | `Terrain-Type_Rock_C` | rock |
| 19 | `Terrain-Type_Sand_A` | sand |
| 20 | `Terrain-Type_Sand_B` | sand, also laid under sand runways |
| 21 | `Terrain-Type_Sand_C` | sand |
| 22 | `Terrain-Type_Gravel_A` | gravel, also laid under gravel runways |
| 23 | `Terrain-Type_Grass_B3` | grass |

-->

| Number | File name | Ground |
|---|---|---|
| 0 | `0.png` | dirt |
| 1 | `1.png` | dirt |
| 2 | `2.png` | dirt |
| 3 | `3.png` | dirt |
| 4 | `4.png` | dirt |
| 5 | `5.png` | dirt |
| 6 | `6.png` | dirt, also laid under parking spots, gardening plots and dirt runways |
| 7 | `7.png` | dirt |
| 8 | `8.png` | grass |
| 9 | `9.png` | grass |
| 10 | `10.png` | grass |
| 11 | `11.png` | grass |
| 12 | `12.png` | grass |
| 13 | `13.png` | road, also laid under tarmac runways |
| 14 | `14.png` | road |
| 15 | `15.png` | road, also laid under concrete runways |
| 16 | `16.png` | rock |
| 17 | `17.png` | rock |
| 18 | `18.png` | rock |
| 19 | `19.png` | sand |
| 20 | `20.png` | sand, also laid under sand runways |
| 21 | `21.png` | sand |
| 22 | `22.png` | gravel, also laid under gravel runways |
| 23 | `23.png` | grass |

The runway surfaces are the built-in values of the `AirstripTiers` table (`Biome Id` column); a mod that changes that table changes which ground is laid.

## Biomes and the `Biomes` table

The two are independent and combine freely:

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

| You want to change... | Use |
|---|---|
| What a ground type looks like | `Biomes/<name>/albedo.png` (this page) |
| How a ground type plays: movement speed, runway tier, wear on stored goods, fire spread | The `Biomes` table, row `<number>` ([CSV tables](../data/csv.md)) |
| Which ground is painted where on a map | The **Biomes** tool in the [Map Editor](maps.md) |

-->

| You want to change... | Use |
|---|---|
| What a ground type looks like | `Biomes/<number>.png` (this page) |
| How a ground type plays: movement speed, runway tier, wear on stored goods, fire spread | The `Biomes` table, row `<number>` ([CSV tables](../data/csv.md)) |
| Which ground is painted where on a map | The **Biomes** tool in the [Map Editor](maps.md) |

## Several mods, same biome

If two enabled mods repaint the same biome, the mod applied last wins, and the log notes which one overrode which. See [How mods work](../basics/mods.md) for the order.

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

## When something does not show up

Check `Player.log` for lines starting with `[Mod <your mod id>] Biomes/...`:

| Log line (shortened) | Meaning |
|---|---|
| `Biomes/Terrain-Type_Grass_A: replaced biome slot 8 (Terrain-Type_Grass_A).` | Your texture is in use. Written when a map loads. |
| `Biomes/Grass_A names no biome of this game. Known biomes: Terrain-Type_Dirt_A, ...` | The folder name does not match. Copy it from the list above. |
| `Biomes/Terrain-Type_Grass_A has no albedo.png and is ignored` | Add the texture, or fix its name. |
| `Biomes/Terrain-Type_Grass_A: only albedo.png is used for a biome; the other files are ignored.` | Harmless; remove the extra files if you like. |
| `Biomes/Terrain-Type_Grass_A/albedo.png is 4096x4096, over the 2048x2048 limit` | Scale the texture down. |
| `Biomes/Terrain-Type_Grass_A/albedo.png is not a PNG` | Save it as a real PNG. |
| `[Mods] This device cannot copy textures on the GPU; biome textures from mods are not applied.` | Your graphics hardware does not support biome mods. Nothing to fix in the mod. |

-->
