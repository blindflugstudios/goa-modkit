# Airplane skins

A skin is a new paint scheme for an airplane the game already has. The model stays exactly the same; your mod only brings new pictures that are painted onto it. So you paint on the airplane's existing UV layout (the flat map that says which part of the picture lands where on the model), the same one the built-in skins use.

A mod skin behaves like a built-in one:

- It shows up in every skin selection next to the built-in skins: the airplane's own panel, the fleet's default and randomize settings, and the ordering window.
- It is unlocked from the start.
- It is put on an airplane with the **Paint Airplane** task, like any other skin.
- It is part of the pool the randomize setting picks from.

!!! tip "Example files"
    Example files for airplane skins are in the [example folder on Google Drive](https://drive.google.com/open?id=15fkBMoUdIB0wkL8wjuqEwflo2xZqbXni&usp=drive_fs). Use them as a reference for how your own files should look.

## Quick start

1. Make a mod folder with an `Airplanes/` folder inside:

    ```text
    Mods/
      my_mod/
        Airplanes/
          config.json
          DesertRat_BaseMap_1001.png
    ```

2. Put this into `Airplanes/config.json`:

    ```json
    {
      "Skins": {
        "DesertRat": {
          "Airplane": "spitfire"
        }
      }
    }
    ```

3. Paint `DesertRat_BaseMap_1001.png` on the Spitfire's UV layout and save it as PNG.
4. Open **Main menu → Mods** and press **Refresh** so the game finds the new mod folder, make sure **my_mod** is switched on, then load a save.

The skin **DesertRat** is now in the Spitfire's skin selection.

## The `Airplanes/` folder

Everything for your skins lives in the mod's `Airplanes/` folder:

```text
Mods/
  my_mod/
    Airplanes/
      config.json                   required - which skins the folder adds
      DesertRat_BaseMap_1001.png    required - base colour, tile 1001
      DesertRat_BaseMap_1002.png    optional - base colour, tile 1002
      DesertRat_Specular_1001.png   optional - specular colour, tile 1001
      DesertRat_Specular_1002.png   optional - specular colour, tile 1002
      DesertRat.thumbnail.png       optional - the skin's icon in the menus
```

- PNGs may sit in subfolders of `Airplanes/`, so you can sort them however you like. The game knows a file by its name alone.
- Capitalisation in file names does not matter: `desertrat_basemap_1001.png` is found as well.
- Only the `config.json` directly inside `Airplanes/` is read. A `config.json` in a subfolder is not.
- Any other file type is ignored, with a warning in the log.

## `config.json`

`config.json` lists your skins under `Skins`. Each skin gets an entry, keyed by its **skin id**. The skin id also names the skin's textures and its thumbnail.

```json
{
  "Skins": {
    "DesertRat": {
      "Airplane": "spitfire",
      "Name": "Desert Rat",
      "BaseSkin": "Supermarine-Spitfire_MK09_Day-Fighter_Toon-UDIM"
    }
  }
}
```

| Key | Required | What it does |
|---|---|---|
| `Skins` | yes | One entry per skin. The key of each entry is the skin id (here `DesertRat`). |
| `Airplane` | yes | The airplane the skin is painted on. An id from [Airplane ids](#airplane-ids). |
| `Name` | no | The name the skin selection shows. It is one text for all languages. Without it, the skin id is shown. |
| `BaseSkin` | no | The built-in skin your skin starts from. Its material is copied, and every texture your mod does not ship stays that skin's. Without it, the airplane's first skin is used (see [Airplane ids](#airplane-ids)). |

!!! warning
    Keep the file valid JSON: no comments, no trailing commas.

### When a skin is skipped

A skin is left out, with a warning in the log, when:

- it names no `Airplane`,
- the `Airplane` it names does not exist,
- the folder has no `<skinId>_BaseMap_1001.png`.

## Textures

The texture names follow the naming of the game's own art, with your skin id in front. Bigger airplanes spread their paint over several pictures, called tiles, numbered 1001, 1002 and 1003.

| File | What it paints |
|---|---|
| `<skinId>_BaseMap_1001.png` | Base colour of tile 1001 (UVs with U from 0 to 1). **Required.** |
| `<skinId>_BaseMap_1002.png`, `<skinId>_BaseMap_1003.png` | Base colour of tile 1002 (U from 1 to 2) and tile 1003 (U from 2). |
| `<skinId>_Specular_1001.png`, `<skinId>_Specular_1002.png`, `<skinId>_Specular_1003.png` | Specular colour (the shine) of each tile. |

- Only the base colour of tile 1001 is required.
- A tile you leave out keeps the texture of the base skin. So you can repaint just part of an airplane.
- A tile the base skin's material has no slot for is ignored.
- A texture may be at most 4096 × 4096 pixels and 10 MB, the same limits as for object art (see [Objects and models](objects.md)). A file over the limit is not scaled down; it is skipped with a warning in the log.

### Thumbnail

`<skinId>.thumbnail.png` is the icon the skin selection shows for your skin, at most 512 × 512 pixels and 10 MB. It is optional: without one, the base skin's icon is shown.

## Airplane ids

Use these ids for `Airplane`. The second column is the airplane's first skin, which is used when you leave out `BaseSkin`.

| `Airplane` | First (default) skin |
|---|---|
| `b17raf` | `b17raf_Boeing-B17_MK02_Temperate-Sea_Toon-UDIM` |
| `beaufighter` | `Bristol-Beaufighter_MK01_Temperate-Land_Toon-Opaque` |
| `blenheim` | `Bristol-Blenheim_MK04_Temperate-Land_Toon-Opaque` |
| `defiant` | `BoultonPaul-Defiant_MK01_Night_Toon-Opaque` |
| `flamingo` | `DeHavilland-Flamingo_MK01_Temperate-Land_Toon-Opaque` |
| `gladiator` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-UDIM` |
| `hampden` | `HandleyPage-Hampden_MK01_Night_Toon-Opaque` |
| `hurricane` | `Hawker-Hurricane_MK02_Day-Fighter_Toon-UDIM` |
| `kittyhawk` | `Curtiss-P40_E_Desert-Scheme_Toon-Opaque` |
| `lancaster` | `Avro-Lancaster_MK01_Night_Toon-UDIM` |
| `lysander` | `Westland-Lysander_MK03_Night_Toon-UDIM` |
| `meteor` | `Gloster-Meteor_MK03_Day-Fighter_Toon-Opaque` |
| `mosquito` | `DeHavilland-Mosquito_BMK04_Day-Fighter_Toon-UDIM` |
| `mustangmk1` | `mustangmk1_NorthAmerican-Mustang_MK01_Day-Fighter_Toon-UDIM` |
| `spitfire` | `Supermarine-Spitfire_MK09_Day-Fighter_Toon-UDIM` |
| `stirling` | `Short-Stirling_MK01_Night_Toon-UDIM` |
| `tempest` | `Hawker-Tempest_MK05_Day-Fighter_Toon-UDIM` |
| `typhoon` | `Hawker-Typhoon_MK01B_Day-Fighter_Toon-UDIM` |
| `vampire` | `DeHavilland-Vampire_MK01_Day-Fighter_Toon-Opaque` |

## Saves and disabled mods

The game saves a mod skin under the id `mod_<modId>_<skinId>`, in lower case. Your `DesertRat` in the mod `my_mod` is saved as `mod_my_mod_desertrat`. Because the mod id is part of it, two mods never clash, and your skin id needs no prefix of its own.

- When a save names a skin whose mod is no longer switched on, the airplane falls back to its first skin, and the skin disappears from the fleet's default and randomize settings.
- Scenes that show an airplane away from your base, the scramble interception and crash sites, show the airplane's built-in look. That is the same for the built-in skins.

## Seeing your changes

Skins are read each time a level is loaded. No restart is needed.

| You changed... | To see it |
|---|---|
| A skin PNG or `Airplanes/config.json` in a mod the game already knows | Load a level (loading a save is enough). |
| A new mod folder, or an `Airplanes/` folder that was empty when the game started | Press **Refresh** in the Mods window, then load a level. |

More on the test loop in [Testing and reloading](../basics/testing.md).

## Checking the log

The game writes what it accepted and what it refused to `Player.log` (where to find it: [How mods work](../basics/mods.md)). Lines about your mod start with `[Mod <your mod id>]`. When a skin does not show up, look there for the warnings described above: a skipped skin, an ignored file type or a texture over the size limit.

!!! note
    The released game logs errors only. The detailed `[Mod ...]` lines appear only in development builds. So when the log shows nothing about your mod, check the skin selection in the game itself.
