# Biomes

A biome is a ground type: the grass, dirt, road, rock, sand or gravel painted across a map with the **Biomes** tool of the [Map Editor](maps.md). The game has 24 of them, numbered `0` to `23`. A mod can repaint any of them with a new texture, and the change shows on every map, shipped or custom.

A biome mod changes the **look** only. How fast people and aircraft move over the ground, which runway tier it counts as, and similar rules live in the `Biomes` table and are changed with [CSV tables](../data/csv.md).

## Quick start

Give the first grass a new texture:

```text
Mods/
  my_ground_mod/
    Biomes/
      8.png
```

Restart the game and load a save or start a map. Everywhere the map uses that grass, you now see your texture.

!!! note "Restart after every change"
    Biome textures are imported **once, when the game starts**. After you add or change a PNG, or switch the mod on or off, **quit the game completely and start it again**. Loading a save, **Refresh** and the **Enabled** switch in the Mods window do not re-import them.

## How it works

- `Biomes/` holds one PNG per ground type, named after its number: `8.png` repaints ground type 8, the first grass (see the [list](#biome-names)).
- The number is written in plain digits without leading zeros: `8.png`, not `08.png`. A number outside `0` to `23` is reported in the [log](../start/troubleshooting.md#find-the-playerlog) together with the valid range.
- Only files directly inside `Biomes/` count. Subfolders, other file types and other names are reported in the [log](../start/troubleshooting.md#find-the-playerlog) and ignored.
- A mod cannot add new biomes, only repaint the 24 that exist. A map remembers which biome is painted where by number, so there is nothing a new one could be attached to.
- The biome's surface detail and its burnt look after a fire are not replaced.
- The game's own textures are untouched on disk. Switching the mod off (and restarting) brings the original ground back everywhere.
- The repainted ground is put together on the graphics card. On a computer whose graphics card cannot copy textures there, biome PNGs are not applied and the [log](../start/troubleshooting.md#find-the-playerlog) says so. There is nothing to fix in the mod then.

### The texture

| Rule | Limit |
|---|---|
| Format | A real PNG. A JPEG renamed to `.png` is refused. |
| Size | At most 4096 × 4096 pixels (each side on its own) |
| File size | At most 10 MB |

A PNG over a limit is **not scaled down**: it is skipped with a warning in the [log](../start/troubleshooting.md#find-the-playerlog), and the game's own ground stays. Within the limits, the game resizes your texture to the size of its own ground textures, so any size works; a square image avoids stretching. The texture repeats across the ground, so it should tile seamlessly: the left edge must continue into the right edge, the top into the bottom.

## Biome names

The number is the biome's row in the `Biomes` table. Rows with the same number describe how that ground plays.

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

| You want to change... | Use |
|---|---|
| What a ground type looks like | `Biomes/<number>.png` (this page) |
| How a ground type plays: movement speed, runway tier, wear on stored goods, fire spread | The `Biomes` table, row `<number>` ([CSV tables](../data/csv.md)) |
| Which ground is painted where on a map | The **Biomes** tool in the [Map Editor](maps.md) |

## Several mods, same biome

If two enabled mods repaint the same biome, the mod applied last wins, and the [log](../start/troubleshooting.md#find-the-playerlog) notes which one overrode which. See [How mods work](../basics/mods.md#which-mod-wins) for the order.

## When something does not show up

- Did you **restart the game**? Biome textures are only imported at game start.
- Is the file directly inside `Biomes/`, named with a number from `0` to `23` and no leading zero?
- Is it a real PNG, at most 4096 × 4096 pixels and 10 MB?

Problems are written to [`Player.log`](../start/troubleshooting.md#find-the-playerlog) on lines that start with `[Mod <your mod id>]`. The detailed lines may only appear in development builds, so if the log is silent, go through the list above. The size limits for all art are also on [Objects and models](objects.md#file-limits).
