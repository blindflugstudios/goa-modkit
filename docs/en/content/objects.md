# Objects and models

!!! warning "Work in progress"
    Art mods are work in progress. The current alpha does not support them yet, so models and textures from a mod do not show up in the game for now.

Tired of the standard-issue barrel? A mod can give the objects you build on your airfield a new look: furniture, fences, guns, signs, posters, workbenches and training equipment. You either drop in a new 3D model, or keep the game's model and paint it with a new texture.

Only the look changes. Size on the grid, cost, what crew can do with the object, and every other rule stay as the game defines them. Changing numbers is done with [CSV tables](../data/csv.md).

## Folder layout (preliminary)

This is how the game will read object art. It is preliminary and may still change.

- `Objects/` holds every model and every texture of the mod in one folder. A model's **file name** is the id of the object it replaces: `Chair.fbx` re-dresses the chair, `Chair.destroyed.fbx` its destroyed look, `tree.2.glb` variant 2 of the tree. Both `.fbx` and `.glb` are accepted.
- A model's materials name their textures, and the PNG of that name in `Objects/` is used: a material that names the image `wood-01` gets `Objects/wood-01.png`. One texture can serve any number of models.
- `Chair.thumbnail.png` (at most 256 × 256) replaces the chair's icon in the build menu. It is only used next to a model of the same id.
- Subfolders below `Objects/` are read too, but their names mean nothing: `Objects/Chair/model.fbx` is a model for an object called `model`, not for the chair.
- Per-object settings live in one `Objects/config.json`, keyed by object id: `{"Objects": {"Chair": {"UseGameMaterial": false}}}`. A `config.json` in a subfolder is ignored.
- Trees, bushes, rocks and the other map objects are re-dressed from `Objects/` too. There is no `TerrainObjects/` folder any more.
- Art is imported once, when the game starts. After a change, **restart the game**; neither **Refresh** nor the **Enabled** switch in the Mods window re-imports it.

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

## Quick start

Give the barrel a new model. Export your model as a binary glTF file named `model.glb` and put it here:

```text
Mods/
  my_barrel_mod/
    Objects/
      Barrel/
        model.glb
```

Restart the game and load a save. Every barrel, the ones already standing and new ones you build, now uses your model.

Just want to recolour the existing barrel? Put a texture next to nothing else:

```text
Mods/
  my_barrel_mod/
    Objects/
      Barrel/
        albedo.png
```

The game keeps its own barrel model and paints your `albedo.png` onto it instead of the original texture.

!!! note
    Models and textures are read once, when the game starts. After you change a file, switching a mod on or off, or adding a new object folder, **restart the game**. Loading a save is not enough for art.

## How it works

Inside your mod, the `Objects/` folder holds one subfolder per object you want to change. The subfolder's name is the object's id (see [Which objects can be changed](#which-objects-can-be-changed)); capitalisation does not matter.

Each object folder may contain these files. All of them are optional, but a folder needs at least one of the first four:

| File | What it does |
|---|---|
| `model.glb` or `model.fbx` | Replaces the object's model. |
| `albedo.png` | The colour texture. With a model: painted onto your model. Without a model: painted onto the game's own model. |
| `destroyed.glb` or `destroyed.fbx` | Replaces the model shown after the object has been destroyed, for example by a bombing raid. |
| `destroyed_albedo.png` | The colour texture for the destroyed look, following the same rules as `albedo.png`. |
| `config.json` | Settings for this object (see [config.json](#configjson)). |

Everything else on the object stays as the game made it: where crew stand to use it, the space it takes, fire and smoke effects, sounds. The ghost preview you see while placing the object already shows your model.

### Two ways to reskin

**New model.** Your model replaces the game's model entirely. Its origin is placed exactly where the original model sits, with no rotation or scaling added. Model your object to the same size and facing as the original: look at the original in the game, and build yours on the same footprint.

**Texture only.** Without a model file, `albedo.png` replaces the colour texture on every material of the game's model. The game's model is mapped to its own texture layout, so your texture has to follow that layout to look right. This is best for recolouring: a darker tint, a different paint scheme, weathering.

### The destroyed look

Many objects switch to a wrecked look when they are destroyed. `destroyed.glb` / `destroyed.fbx` and `destroyed_albedo.png` change that look in the same two ways. If an object has no destroyed look at all, those files are skipped and the log says so. If you leave them out, the object keeps the game's own destroyed look.

## Model formats

| Format | File name | Notes |
|---|---|---|
| glTF binary | `model.glb`, `destroyed.glb` | Recommended. Materials and embedded textures are used as authored. |
| FBX | `model.fbx`, `destroyed.fbx` | Meshes and material colours only. Textures inside the FBX are not read; ship an `albedo.png` next to it. |

If a folder has both `model.glb` and `model.fbx`, the `.glb` is used and the log mentions the `.fbx` it ignored.

### glTF (`.glb`)

- Only the binary form, `.glb`, is read. A `.gltf` text file with separate `.bin` and image files is not.
- The file must be **self-contained**. A `.glb` that points to outside files or web addresses has those references refused. Embed textures into the `.glb` when you export (Blender's glTF exporter does this with the format set to *glTF Binary*).
- Materials use the standard glTF metallic-roughness model. Such a material keeps its own look as long as it has a colour texture. See [Materials](#materials) for the exceptions.

### FBX (`.fbx`)

- The game converts the file to Y-up and metres itself, following the axis and unit settings stored in the file. An FBX exported from Blender the usual way faces the same direction as the game's own art.
- Only meshes are read: no animation, no skinning, no cameras or lights.
- Hidden objects in the file are skipped.
- One UV map (the first) is read.
- Faces with more than three corners are split into triangles. This is exact for flat, convex faces; triangulate unusual faces in your 3D program before exporting.
- Of each material, only the base colour (diffuse colour times diffuse factor) is read. Textures linked or embedded in the FBX are ignored, and the log reminds you to ship an `albedo.png` instead.

### Size, facing and levels of detail

- Units are metres, Y is up.
- Your model's origin lands on the original object's origin. Put the origin of your model where the original has it, usually on the ground at the object's centre.
- **Levels of detail.** Where the original object switches to simpler models in the distance, your model can do the same. Name the nodes in your file `LOD0`, `LOD1`, `LOD2` and so on (capitalisation does not matter, `LOD1_Barrel` counts as `LOD1`). The game uses them in that order at the original's switching distances. With fewer levels than the original, your last level is kept to the end. With no `LOD` nodes, the whole model is shown at every distance, and the object still disappears where the original would.

## Materials

What your model looks like in the game depends on its materials:

| Your material | What the game does |
|---|---|
| glTF metallic-roughness material **with** a colour texture | Kept exactly as authored. |
| Material **without** any colour texture | Moved onto the original object's material, keeping your base colour. |
| Unlit or specular-glossiness glTF material | Moved onto the original object's material, keeping your colour texture and base colour. |
| FBX material | Same rules; since FBX textures are not read, it has no texture unless you ship `albedo.png`. |
| Any material, with `"UseGameMaterial": true` in `config.json` | Moved onto the original object's material, keeping your colour texture and base colour. |

`albedo.png` next to a model replaces the colour texture on all of its materials.

**Why `UseGameMaterial`?** The game paints effects onto its own materials at runtime, most visibly the cracks of battle damage. A material you authored in your model cannot show them. Set `UseGameMaterial` if your object should show damage like the originals do; you give up your model's own shading (metalness, roughness, normal maps) in exchange.

## `config.json`

Optional, inside the object's folder:

```json
{
  "UseGameMaterial": true
}
```

| Key | Type | Default | What it does |
|---|---|---|---|
| `UseGameMaterial` | true / false | `false` | Shade the model with the original object's material instead of the materials in your model file. Keeps battle damage and other game effects working. |

A `config.json` that cannot be read is reported in the log, and every setting falls back to its default. Your model and textures still load.

## Textures

| Rule | Limit |
|---|---|
| Format | PNG only. Other formats, even renamed to `.png`, are refused. |
| Size | At most 2048 × 2048 pixels. |
| File size | At most 8 MB. |
| File names | Exactly `albedo.png` and `destroyed_albedo.png`. |

Textures inside a `.glb` are part of the model file and count toward the model limit instead.

## Limits

| What | Limit |
|---|---|
| Model file (`.glb` / `.fbx`) | 32 MB |
| PNG texture | 8 MB, 2048 × 2048 pixels |

A file over a limit is skipped with a message in the log; the rest of the object folder still loads.

## Several mods changing the same object

If two enabled mods both have a folder for the same object, the mod applied last wins and replaces the other's art completely, and the log notes which mod overrode which. The order is described in [How mods work](../basics/mods.md).

Objects, [terrain objects](terrain-objects.md) and [biomes](biomes.md) are separate: a folder `Objects/tree` and a folder `TerrainObjects/tree` never affect each other.

-->

## Which objects can be changed

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

The folder name is the object's id, the same id the object has in the `ID` column of the `BuildingComponents` table (see [CSV tables](../data/csv.md)).

-->

The model's file name is the object's id, the same id the object has in the `ID` column of the `BuildingComponents` table (see [CSV tables](../data/csv.md)).

**Workbenches:**

```text
Brickstation, CanningStation, CementMixer, Distillery, ElectronicsWorkbench, EspionageRadio, FieldKitchen,
HerbDryer, IndoorKitchen, MetalworksWorkbench, SawStation, TailorStation, WaterCooker
```

**Training equipment:**

```text
BombingAdvancedSimulator, BombingSimpleBench, EnduranceAdvancedBikeExerciser, EnduranceSimpleRack,
EngineeringAdvancedEngine, EngineeringSimpleMechanicWorkstation, FlyingAdvancedLinkTrainer,
FlyingSimpleWoodenConstruction, NavigationAdvancedNaviTrainer, NavigationSimpleBoard, ShootingAdvancedTurret,
ShootingSimpleTargetRange
```

**Furniture, decoration, defences and other placeable objects:**

```text
AntitankPimple, BarbedWire, BarbedWireCorner, BarCounter, Barrel, BarStool, Bed, BedMetal, BedWood,
BilliardTable, BloodPackRack, Bofors40mm, Chair, Chalkboard, Clock, Clothesline, ClothingRack, ClothingStand,
ComfyChair, ComfyChairLarge, ControlTowerBrick, ControlTowerConcrete, ControlTowerMetal, CookingFire,
CrateEmpty, Cross, CurtainsClosedSmall, CurtainsOpenSmall, Dartboard, DividerCurtains, door_hangar, Drawer,
Flagpole10, Flagpole5, FlagpoleFloor, FlagpoleWall, Flowerbed01, Flowerbed02, FuelTank, Gramophone,
Gravestone, GravestoneWhite, Guitar, HandwashBowls, Hangers, Jukebox, KickstarterBackerMonument,
KickstarterCustomMonument, LiquorShelf, Lookout, MedicineCabinet, MetalBoxSmall, MetalFence,
MetalFenceCorner, MetalFenceEdge, MetalShelf, MetalShelfClosedClothes, MetalShelfClosedFiles, NightTable,
OerlikonGun, OxygenBottle, Piano, PilotBoard, PlanningBoard, PolishPilotsFlag, Poster, Poster01, Poster02,
Poster03, Poster04, Poster05, Poster06, Poster07, Poster08, Poster09, Poster10, Poster11, Poster12, Poster13,
Poster14, Poster15, Poster16, Poster17, Poster18, Poster19, Poster20, Poster21, Radio, RadioTower, Roadblock,
RollableScaffolding, RollableToolTable, RugBedrug, RugBedrugSmall, RugCubismrug, RugDoormat, RugJuterug,
RugKitchenrug, RugPersian, SandbagFence1mCorner, SandbagFence1mStraight, ScrambleBell, Searchlight, Shelf,
ShelfBooks, ShelfFolders, ShelfPersonalStuff, Sickbed, Siren, SirenOnPole, SmallFuelTank, SmallLoungeTable,
Stepladder, StoveSmall, TableMetal, TableOutdoor, TableTypewriter, Toilet, Toolbox, VickersGunAA, WallPhone,
WallSign1, WallSign2, WallSign3, WallSign4, WallSign5, WarningSign1, WarningSign2, WarningSign3,
WarningSign4, WarningSign5, WaterPump, WaterTower, WaySign1, WaySign2, WaySign3, WaySign4, WaySign5,
WickerChair, Windhose, WoodenChair, WoodenFenceSimple, WoodenFenceSimplePole, WoodenFenceSturdy,
WoodenFenceSturdyEdge, WoodenFenceSturdyPole, WoodenTableLarge, WoodenTableMedium, WoodenTableSmall
```

<!-- OUTDATED (docs audit 2026-09-28): describes the old per-folder layout, see DOCS_AUDIT.md

**Not available yet:** walls, floors, roofs, doors and windows of buildings (`wall_wood`, `floor_brick` and so on), parking spots, aircraft, vehicles and characters. A folder for one of those is read but has no effect. Trees, rocks and other natural objects are [terrain objects](terrain-objects.md); the ground itself is a [biome](biomes.md).

## When something does not show up

The game writes what it did with your art to `Player.log`:

| Platform | Player log |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

Every line starts with `[Mod <your mod id>]` followed by the folder, for example `Objects/Barrel`. Lines you may see:

| Log line (shortened) | Meaning |
|---|---|
| `Objects/Barrel: replaced 3 built-in renderer(s) on the regular view with ...` | Your model is in use. |
| `Objects/Barrel: re-textured 2 material slot(s) on the regular view ...` | Your texture-only reskin is in use. |
| `Objects/Barrel contains none of model.glb or model.fbx, albedo.png, ... and is ignored` | The folder holds no file with a name the game looks for. Check the spelling. |
| `Objects/Barrel ships both model.glb and model.fbx; model.glb is used.` | Remove one of them. |
| `Objects/Barrel/model.glb is 40 MB, over the 32 MB limit` | Make the file smaller. |
| `Objects/Barrel/albedo.png is 4096x4096, over the 2048x2048 limit` | Scale the texture down. |
| `Objects/Barrel/albedo.png is not a PNG` | Save it as a real PNG. |
| `Objects/Barrel/model.glb could not be read` | The file is broken or not a binary glTF. Re-export it. |
| `Objects/Barrel/model.fbx contains no mesh` | The FBX has no visible geometry. |
| `Objects/Barrel/config.json could not be read (...); every setting falls back to its default.` | Fix the JSON. |
| `Objects/Barrel: this object has no destroyed view slot, its destroyed art is skipped.` | This object has no destroyed look to replace. |
| `Objects/Barrel cannot be re-dressed: ...` | This object does not support reskinning. |
| `Objects/Barrel overrides the same skin from mod '...'` | Another mod changes the same object; yours is applied later and wins. |
| `Imported art for 4 object(s).` | Summary after the game started (starts with `[Mods]`). |

If there is no line at all for your folder, check that the folder name matches an id from the list above and that the mod is switched on.

!!! note
    The released game may write only errors to `Player.log`, so some of these lines appear only in development builds. If nothing shows up and the look does not change, work through the checklist: file names, folder name, file size, restart.

-->
