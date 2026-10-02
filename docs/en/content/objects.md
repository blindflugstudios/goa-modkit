# Objects and models

Tired of the standard-issue barrel? A mod can give the game's objects a new look: furniture, fences, guns, signs, posters, workbenches and training equipment. You either drop in your own 3D model, or keep the game's model and paint it with a new texture. You can also give an object a new icon in the build menu.

Only the look changes. Size on the grid, cost, health, where crew stand to use it, and every other rule stay as the game defines them. Changing numbers is done with [CSV tables](../data/csv.md).

!!! tip "Example files"
    Ready-made example models, textures, thumbnails and export presets are in the [example folder on Google Drive](https://drive.google.com/open?id=15fkBMoUdIB0wkL8wjuqEwflo2xZqbXni&usp=drive_fs). Use them as a reference for how your own files should look.

Everything for objects goes into one folder in your mod, `Objects/`:

```text
Mods/
  my_mod/
    Objects/
      Chair.glb               your model for the chair
      Chair.destroyed.glb     the chair when it is destroyed
      Chair.thumbnail.png     the chair's new icon in the build menu
      Chair_BaseMap_1001.png  a texture for it
      config.json             optional settings
```

!!! note "Restart after every change"
    Art is imported **once, when the game starts**. After you add or change a model, texture or thumbnail, **quit the game completely and start it again**. Loading a save, **Refresh** and the **Enabled** switch in the Mods window do not re-import art.

## Quick start

Give the chair a new model:

1. Build your chair in your 3D program at the size of the game's chair (in metres) and export it as `Chair.glb` (binary glTF) or `Chair.fbx`. Build its destroyed look too and export it as `Chair.destroyed.glb` or `Chair.destroyed.fbx`.
2. Name the chair's material in your 3D program, for example `MyChair`, and save its colour texture as `MyChair_BaseMap_1001.png`.
3. Put all three files into `Mods/my_mod/Objects/`.
4. Restart the game and load a save. Every chair, the ones already standing and new ones you build, now uses your model.

Just want to recolour the game's own chair? You do not need a model at all: see [Re-painting without a model](#re-painting-without-a-model).

## Which objects can be changed

A model's **file name** is the id of the object it replaces. You can change the objects you place from the build menu, including workbenches and training objects, for example `Chair`, `FieldKitchen` or `ShootingSimpleTargetRange`. Every object you can change is listed in our [moddable objects table](https://airtable.com/appvUVR7eS3bq1S8f/shrKPxjhkGlHRUmpO), together with how we built it ourselves: material naming and usage, texture resolution, UDIM information and its destroyed view.

Ids are matched without regard to capital letters, so `chair.fbx` changes the chair too.

Only these objects can be re-dressed with `Objects/`. Trees, rocks and the other things placed on a map cannot be changed by a mod yet. Airplanes get new paint schemes another way: see [Airplane skins](airplanes.md). The ground is changed with [biomes](biomes.md).

## File names

Every file that belongs to one object is named `<objectId>`, `<objectId>.destroyed` or `<objectId>.thumbnail`, plus its extension:

| File | What it is |
|---|---|
| `Chair.fbx` or `Chair.glb` | the chair's model |
| `Chair.destroyed.fbx` | the model the chair switches to when it is destroyed |
| `Chair.thumbnail.png` | the chair's icon in the build menu |

- **Models** may be `.glb` (binary glTF) or `.fbx`. If both exist for the same object, the `.glb` is used and the `.fbx` is reported in the [log](../start/troubleshooting.md#find-the-playerlog) as ignored.
- **Blender's duplicate names** such as `Chair.001.fbx` are refused. Rename the file before you copy it in.
- **A destroyed model** is required. The game always shows an object's destroyed look, so every model you ship needs a `.destroyed` model next to it. The [moddable objects table](https://airtable.com/appvUVR7eS3bq1S8f/shrKPxjhkGlHRUmpO) shows the destroyed view of each object.
- **Anything else** in the folder that is not a model, a PNG or the `config.json` directly inside `Objects/` is reported in the [log](../start/troubleshooting.md#find-the-playerlog) and ignored.

## Subfolders

You may sort your files into subfolders of `Objects/` as you like, but **subfolder names mean nothing**: a file is known by its name alone. `Objects/Chair/model.fbx` is a model for an object called `model`, not for the chair. Name it `Objects/Chair/Chair.fbx` instead.

Because `Objects/` and all its subfolders count as one pool, two files with the same name in different subfolders clash: the game keeps one and reports the other. Shortcuts (symbolic links and junctions) are never followed.

## Building the model

- **Size and facing.** Build the model at the game's scale, in metres, facing the same way as the game's own object. Your model is placed at the original object's origin and is not scaled to fit, so put its origin where the original has it, usually on the ground at the object's centre. An FBX is converted to Y-up and metres on import, and an FBX exported from Blender the usual way faces the same direction as the game's own art.
- **Only the look changes.** The object's footprint on the grid, where crew stand to use it and what it bumps into all stay the game's. A model much larger than the original pokes through walls and neighbours.
- **Effects** of the original object, such as a workbench's sawdust, keep playing on your model.
- **Static models only.** Animation in an FBX is not imported, and the game never animates a mod model.
- **At most 32 MB** per model file. A larger file is skipped with a warning, and the object keeps its built-in look.

### What an FBX may contain

The game reads FBX files itself, so it understands less of the format than Blender can write:

- Meshes and the hierarchy above them, with position, rotation and scale. Hidden objects are left out, and a file without any mesh is ignored.
- Normals as exported. A mesh exported without normals gets smooth normals.
- **Only the first UV map.** Every further UV map is ignored, so put the UVs your textures use on the first one.
- Faces with more than three corners are split into triangles. That is only exact for flat, convex faces. Triangulate unusual faces before exporting, or tick **Triangulate Faces** in Blender's FBX export.
- Per material: the base colour only. Textures connected to the material, vertex colours and all other material settings are not read.
- **Images embedded in the FBX are never read.** Ship the textures as PNG files in `Objects/` (see [Textures](#textures)).

## Textures

Textures are PNG files anywhere in `Objects/`, found by their names. There are three ways to name them. The game tries them in this order, and each one only fills what the one before left empty:

| | Name the PNG after | Example | Needs a model |
|---|---|---|---|
| 1 | the **material** in your model: `<material>_BaseMap_<UDIM-Tile>` and `<material>_Specular_<UDIM-Tile>` | `MyChair_BaseMap_1001.png` for a material called `MyChair` | yes |
| 2 | the **texture your model's material uses** | `wood-01.png` for a material painted with an image called `wood-01` | yes |
| 3 | a **built-in texture** of the game | `BedMetal_Toon-Main_BaseMap_1001.png` | no |

Way 1 is the simplest for a model: you do not have to connect any image to the material in your 3D program. Just give the material and the PNG matching names. Ways 1 and 3 only work with the game's material, which is the default (see [Game material or your own](#game-material-or-your-own)).

### The texture a model names

A model's materials name the images they use, and the game looks for a **PNG of that name anywhere in `Objects/`**. A material that uses an image called `wood-01` gets `Objects/wood-01.png` (or `Objects/any/subfolder/wood-01.png`). Folders and the file extension in the stored name are ignored, so a material painted with `C:\art\wood-01.jpg` still finds `wood-01.png`. One PNG can serve any number of models and is loaded only once.

The two model formats differ when no matching PNG is there:

| | `.glb` | `.fbx` |
|---|---|---|
| Texture slots read | base colour | base colour |
| No PNG of that name in `Objects/` | the image embedded in the `.glb` is used | the slot stays untextured, and the [log](../start/troubleshooting.md#find-the-playerlog) names the texture it looked for |
| Images outside the file | refused: a `.glb` has to be self-contained | never read: only the PNGs in `Objects/` count |

Every PNG in `Objects/` whose name does not end in `.thumbnail` counts as a texture. A texture that no model and no built-in object uses is simply never loaded.

## Re-painting without a model

A PNG named exactly like one of the game's own textures **replaces that texture**, no model needed. `Objects/BedMetal_Toon-Main_BaseMap_1001.png` re-paints the metal bed wherever it appears, including its destroyed look. Every object that uses the same texture changes with it.

- Paint over the original image at the same size and layout, because the model stays the game's own.
- The game's texture names usually look like `<Material>_Toon-Main_BaseMap_<UDIM-Tile>` and `<Material>_Toon-Main_Specular_<UDIM-Tile>`. Every object's texture names are listed on [Built-in texture names](texture-names.md).
- Only the object's own art is re-painted. Things every object shares, such as the construction crate, placement markers and range indicators, keep their look. Airplanes (see [Airplane skins](airplanes.md)) and the ground (see [Biomes](biomes.md)) are not changed this way.
- If two mods ship the same texture name, the one later in the load order wins.

## UDIM tiles and specular maps

A model on the game's material can spread its UVs over up to three texture tiles (called UDIM tiles), the way the game's own art does, with a specular map (how shiny each spot is) per tile. For a material called `Crate`:

| Base colour | Specular | Used for UVs with U in |
|---|---|---|
| `Crate_BaseMap_1001.png` | `Crate_Specular_1001.png` | 0 to 1 |
| `Crate_BaseMap_1002.png` | `Crate_Specular_1002.png` | 1 to 2 |
| `Crate_BaseMap_1003.png` | `Crate_Specular_1003.png` | 2 and above |

- Names after the material (way 1) are tried first, for the base colour and for each specular map on its own. A mod may ship only `Crate_Specular_1001.png`.
- If no base colour is named after the material, the texture your model uses (way 2) becomes tile 1001, and the other tiles and specular maps are named after it. The tile number follows a `_` or a `.`: `crate_1001` and `crate.1001` both start a set, and a Blender tile set saved as `crate.<UDIM>.png` finds `crate.1001.png`. The specular map has the same name with `_BaseMap` replaced by `_Specular`, so it only works when the texture name contains `_BaseMap`.
- Tiles switch on when the `1001` base colour has at least one more tile. A single texture is drawn as usual. A missing tile in between is drawn white.
- A specular map or base colour your mod does not ship leaves the original object's own one in place.
- A base colour named after the material is drawn as it is: the colour the material has in your model is ignored, because an FBX material without an image still carries Blender's grey default.

## Game material or your own

By default your model is drawn with **the game's own material** for that object, using your model's base colour texture and base colour. That is what makes battle damage and the other effects the game paints onto objects show on your model too. Specular maps and UDIM tiles are used too.

To keep the material exactly as you made it instead, switch the game's material off for that object in `Objects/config.json`. Only the `config.json` directly inside `Objects/` is read:

```json
{
  "Objects": {
    "Chair": { "UseGameMaterial": false }
  }
}
```

- The keys are object ids as in the file names, without regard to capitals.
- An object with `"UseGameMaterial": false` keeps its full look from your 3D program, but **does not show battle damage**. It also only uses the texture its material names (way 2), without specular maps or UDIM tiles.
- Even with `false`, a material without a base colour texture uses the game's material anyway, keeping the colour you gave it.
- A `config.json` the game cannot read is reported in the [log](../start/troubleshooting.md#find-the-playerlog), and every object falls back to the default.

## Thumbnails

`<objectId>.thumbnail.png` replaces the object's icon in the build menu and everywhere else that icon is shown.

- **At most 512 × 512 pixels**, and at most 10 MB. Each side counts on its own, so 512 × 256 is fine. A larger thumbnail is **not scaled down**: it is skipped with a warning in the [log](../start/troubleshooting.md#find-the-playerlog), and the game's own icon stays.
- A thumbnail is only used **next to a model with the same id**. It cannot change the icon of an object your mod does not give a new model; a thumbnail on its own is reported and ignored.
- One thumbnail per object. A second file with the same name in another subfolder is ignored.

## File limits

Every file in `Objects/` and `Biomes/` is checked before it is loaded:

| File | Largest picture | Largest file |
|---|---|---|
| Model (`.glb`, `.fbx`) | - | 32 MB |
| Texture | 4096 × 4096 | 10 MB |
| Thumbnail | 512 × 512 | 10 MB |
| Biome | 4096 × 4096 | 10 MB |

- Every image has to be a real PNG. A JPEG renamed to `.png` is refused.
- The picture limit applies to each side on its own.
- An image over its limit is **never scaled down**. It is skipped with a warning in the [log](../start/troubleshooting.md#find-the-playerlog), and the game falls back: a skipped thumbnail leaves the game's own icon, a skipped biome the game's own ground, and a material whose texture was skipped is drawn without it.

## Several mods changing the same object

If two enabled mods change the same object, the mod applied **last** wins, following the load order (see [How mods work](../basics/mods.md#which-mod-wins)). The [log](../start/troubleshooting.md#find-the-playerlog) says which mod overrode which. An object is decided as a whole: one mod's model is never combined with another mod's thumbnail for the same object.

## When something does not show up

- Did you **restart the game**? Art is only imported at game start.
- Is the mod switched on in **Main menu -> Mods**?
- Does the file name match an id exactly (apart from capitals)? Is the subfolder name doing nothing you rely on?
- Is every file within the limits above, and every image a real PNG?
- For an FBX: are the textures shipped as PNGs in `Objects/`, named after the material or the image the material uses?

The game writes what it refused and why (a wrong name, a missing texture, an image that is too big) to [`Player.log`](../start/troubleshooting.md#find-the-playerlog), on lines that start with `[Mod <your mod id>]`. The detailed lines may only appear in development builds, so if the log is silent, check the list above and look at the object in the game.
