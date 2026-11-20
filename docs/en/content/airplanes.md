# Airplane skins and new airplanes

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
- Any other file type is ignored, with a warning in the [log](../start/troubleshooting.md#find-the-playerlog).

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

A skin is left out, with a warning in the [log](../start/troubleshooting.md#find-the-playerlog), when:

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
- A texture may be at most 4096 × 4096 pixels and 10 MB, the same limits as for object art (see [Objects and models](objects.md)). A file over the limit is not scaled down; it is skipped with a warning in the [log](../start/troubleshooting.md#find-the-playerlog).

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

## New airplanes

A mod can also add a whole new airplane type: its own model, paint, name, stats and crew window drawing. Each new airplane is **based on** one of the game's airplanes and copies everything you do not give it from that airplane: stats, crew, crash animation, the look in the scramble result and the serial number blocks. The only thing you must give is the model.

!!! tip "Example mod"
    `examples/airplane_captured_bf109` adds a captured Bf 109 based on the Spitfire. Copy it into your `Mods/` folder to see a complete new airplane in the game.

### The airplane's folder

Every new airplane gets a folder inside `Airplanes/`, named after the airplane's id:

```text
Mods/
  my_mod/
    Airplanes/
      config.json
      Bf109/
        Bf109.fbx                 required - the model (.fbx or .glb)
        Bf109.destroyed.fbx       optional - the wreck
        Bf109_BaseMap_1001.png    optional - the paint, more tiles and specular like a skin
        Bf109.thumbnail.png       optional - the picture in the order window and the airplane lists
        Bf109.blueprint.png       optional - the drawing in the crew window
```

Without a paint the model shows the based-on airplane's first skin; without a wreck, the based-on airplane's wreck is used; without a thumbnail or a blueprint, the based-on airplane's are shown.

### `config.json`

New airplanes go under `Airplanes` in the same `Airplanes/config.json` as your skins:

```json
{
  "Airplanes": {
    "Bf109": {
      "BasedOn": "spitfire",
      "Name": "Captured Bf 109",
      "FullName": "Messerschmitt Bf 109 E (captured)",
      "Stats": { "Health": "90" },
      "CrewSlots": [[0.45, 0.48]]
    }
  }
}
```

| Key | Required | What it does |
|---|---|---|
| `BasedOn` | yes | The game's airplane the new one copies. An id from [Airplane ids](#airplane-ids). |
| `Name` | no | The name the game shows. One text for all languages. Without it, the airplane's id is shown. |
| `FullName`, `ShortName` | no | Longer and shorter name, shown in the order window and the crew window. Without them, `Name` is used. |
| `Manufacturer`, `Armament`, `MaximumSpeed`, `Engine`, `Range`, `Ceiling`, `Dimensions` | no | The details the order window lists. Empty when left out. |
| `Stats` | no | Stats that differ from the based-on airplane, keyed by the column names of the game's airplane table (`Health`, `Crew`, `Fuel Capacity`, ...). Values are text: `"Health": "90"`, `"Crew": "Pilot,Gunner"`. |
| `CrewSlots` | no | Where each crew member's slot sits on the blueprint, in crew order, as `[x, y]` fractions of the drawing: `[0, 0]` is the bottom left corner, `[1, 1]` the top right. Slots you leave out are spread across the middle. |

A skin may be painted on your new airplane too: write the airplane's id from `Airplanes` (here `Bf109`) as the skin's `Airplane`.

### Naming the parts of the model

The game finds the parts of your model by their node names. Capital letters, `-`, `_`, `.` and spaces do not matter, so `Air-Pivot`, `air_pivot` and `AirPivot` are the same. The game's own airplanes use exactly these names, so you can look at one in your 3D program.

| Node name | What the game does with it | Without it |
|---|---|---|
| `Air-Pivot` | The part that tilts in flight. Put everything that moves with the airplane under it. | Your model tilts with the based-on airplane's pivot. |
| `Propeller-Pivot` (one per propeller, e.g. `Propeller-Left-Pivot`) | Spins around its own forward axis while the engine runs. | No propeller spins. |
| `Wheel-Left`, `Wheel-Right`, `Wheel-Tail` | The angle the airplane rests at on the ground is worked out from where these touch the ground. | The based-on airplane's angle is used. |
| `1-Interaction-Pilot`, `2-Interaction-Gunner`, ... | The crew seats, in the order of the number in front. | The based-on airplane's seats. |
| `Interaction-Paint` | Where the crew stand to paint and refuel the airplane. | The based-on airplane's spot. |
| `FireEmitter` | The mesh fire burns on. | The largest part directly under `Air-Pivot` that is not glass or the inside. |

- **Size and facing.** Build the airplane in metres at its real size, standing on the ground at the origin, like the game's own airplanes. Which way the nose points does not matter if the model has a `Propeller...` node and a `Wheel-Tail` node: an airplane whose propeller sits behind its tail wheel is turned around.
- **Landing gear** stays down. Animations in the model file are not played yet.
- **Marking decals** (squadron codes, roundels) are not drawn on new airplanes; paint the markings into your texture.

### Where a new airplane shows up

The game knows a new airplane as `mod_<modId>_<id>`, in lower case: the `Bf109` of the mod `captured_bf109` is `mod_captured_bf109_bf109`. It is unlocked from the start, appears in the order window, and is part of crash sites, the crew window and scrambles like any other airplane. Quests and promo codes do not know it.

## Saves and disabled mods

The game saves a mod skin under the id `mod_<modId>_<skinId>`, in lower case. Your `DesertRat` in the mod `my_mod` is saved as `mod_my_mod_desertrat`. Because the mod id is part of it, two mods never clash, and your skin id needs no prefix of its own.

- When a save names a skin whose mod is no longer switched on, the airplane falls back to its first skin, and the skin disappears from the fleet's default and randomize settings.
- When a save holds a new airplane whose mod is no longer switched on, the airplane becomes the airplane it was based on. Switching the mod back on later does not turn it back.
- Scenes that show an airplane away from your base, the scramble interception and crash sites, show the airplane's built-in look. That is the same for the built-in skins.

## Seeing your changes

Skins are read each time a level is loaded. No restart is needed.

| You changed... | To see it |
|---|---|
| A skin PNG or `Airplanes/config.json` in a mod the game already knows | Load a level (loading a save is enough). |
| A new mod folder, or an `Airplanes/` folder that was empty when the game started | Press **Refresh** in the Mods window, then load a level. |

More on the test loop in [Testing and reloading](../basics/testing.md).

## Checking the log

The game writes what it accepted and what it refused to [`Player.log`](../start/troubleshooting.md#find-the-playerlog). Lines about your mod start with `[Mod <your mod id>]`. When a skin does not show up, look there for the warnings described above: a skipped skin, an ignored file type or a texture over the size limit.

!!! note
    The released game [logs](../start/troubleshooting.md#find-the-playerlog) errors only. The detailed `[Mod ...]` lines appear only in development builds. So when the log shows nothing about your mod, check the skin selection in the game itself.
