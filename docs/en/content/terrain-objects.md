# Terrain objects

Terrain objects are the things that belong to the land rather than to your airfield: trees, bushes, rocks, clay and sand pits, ponds, wild crops, old fences and graves. They are placed on a map with the **Terrain Objects** tool of the [Map Editor](maps.md).

A mod can give any of them a new look, on every map at once. It works exactly like [reskinning objects](objects.md), with one addition: many terrain objects come in several variants, and you can change all variants together or one at a time.

## Quick start

Replace all trees with your own model:

```text
Mods/
  my_forest_mod/
    TerrainObjects/
      tree/
        model.glb
```

Replace only the broadleaf tree (variant `2` of `tree`) and leave the other trees alone:

```text
Mods/
  my_forest_mod/
    TerrainObjects/
      tree/
        2/
          model.glb
```

Restart the game and load a save or start a map. Trees already on the map change too.

!!! note
    Like all mod art, terrain objects are read once, when the game starts. After changing a file or switching the mod on or off, **restart the game**.

## How it works

Inside your mod, `TerrainObjects/` holds one folder per terrain object, named after its id (see [Terrain object ids](#terrain-object-ids)). Capitalisation does not matter.

- Files directly in `TerrainObjects/<id>/` apply to **every** variant of that object.
- Files in a numbered subfolder, `TerrainObjects/<id>/<variant>/`, apply to **that variant only** and win over the parent folder for it.
- A subfolder whose name is not a number (`0`, `1`, `2`, ...) is ignored with a warning in the log.
- If you only use variant subfolders, the parent folder holds no files. The log then notes that `TerrainObjects/<id>` contains no files and is ignored; that is harmless, the variant folders still load.

Each folder takes the same files as an object folder:

| File | What it does |
|---|---|
| `model.glb` or `model.fbx` | Replaces the model. |
| `albedo.png` | The colour texture. With a model: painted onto your model. Without a model: painted onto the game's own model. |
| `destroyed.glb` or `destroyed.fbx` | Replaces the look after the object has been destroyed, where it has one. |
| `destroyed_albedo.png` | The colour texture for the destroyed look. |
| `config.json` | `{ "UseGameMaterial": true }` to shade your model with the game's own material. |

The model formats, material rules, texture rules, level-of-detail node names (`LOD0`, `LOD1`, ...) and file size limits are the same as for objects. They are explained once, in [Objects and models](objects.md#model-formats).

Only the look changes. Whether crew can chop a tree for wood, forage a bush, dig a pit or drink from a pond stays the same.

### Trees and levels of detail

Trees switch to simpler models, and in the far distance to flat cut-outs, as the camera moves away. When you replace a tree's model, all of those are hidden and your model takes over. Give your file `LOD0`, `LOD1`, ... nodes to have your own simpler versions used at the same distances; without them, your full model is drawn until the tree would disappear anyway. With many trees on a map, a simple far level makes a real difference to performance.

Effects wired to the object, such as falling leaves when a tree is felled, keep working.

## Terrain object ids

| Id | Variants | What they are |
|---|---|---|
| `tree` | 0–4 | 0 conifer, 1 bare conifer, 2 broadleaf, 3 bare conifer (second), 4 conifer (second) |
| `tree_big` | 0–1 | two big oaks |
| `young_tree` | 0–1 | 0 young conifer, 1 young broadleaf |
| `young_tree_big` | 0–1 | two young big oaks |
| `tree_big_log` | 0–1 | two fallen logs |
| `tree_big_stump` | 0–1 | two stumps |
| `bush` | 0–5 | 0–4 bushes, 5 cow parsley |
| `bush_big` | 0 | blackthorn |
| `berry_bush` | 0 | berry bush |
| `herbs_plant` | 0 | herb plant |
| `mushroom_patch` | 0 | mushroom patch |
| `flowers` | 0–2 | three kinds of flowers |
| `small_rock` | 0–1 | 0 small rock, 1 mossy rock |
| `large_rock` | 0–1 | 0 big rock, 1 big mossy rock |
| `long_rock` | 0 | long mossy rock |
| `sand_pit` | 0 | sand pit |
| `clay_pit` | 0 | clay pit |
| `water_pond` | 0 | pond |
| `wild_grain` | 0 | wild grain |
| `wild_beans` | 0 | wild beans |
| `wild_potato` | 0 | wild potatoes |
| `wild_tomato` | 0 | wild tomatoes |
| `damaged_car` | 0 | wrecked car |
| `old_fence` | 0 | old fence |
| `old_fence_pole` | 0 | old fence pole |
| `old_grave` | 0–1 | 0 gravestone, 1 simple cross |
| `old_headstone` | 0 | white headstone |
| `ocean` | 0 | the sea |

Variant numbers are the ones the Map Editor places. An object with a single variant uses `0`; for it, `TerrainObjects/<id>/` and `TerrainObjects/<id>/0/` do the same thing.

## Several mods, same terrain object

If two enabled mods both change the same folder, for example both have `TerrainObjects/tree/`, the mod applied last wins, and the log notes which one overrode which. `TerrainObjects/tree/` and `TerrainObjects/tree/2/` count as different folders: one mod can change all trees while another changes only the broadleaf, and the broadleaf mod wins for variant 2.

Terrain objects are a separate list from [objects](objects.md): `Objects/tree` would not touch trees on the map.

## When something does not show up

Check `Player.log` for lines starting with `[Mod <your mod id>] TerrainObjects/...`. The messages are the same as for objects (see [the table on the objects page](objects.md#when-something-does-not-show-up)), plus one of its own:

| Log line (shortened) | Meaning |
|---|---|
| `TerrainObjects/tree/broadleaf is not a variant index (0, 1, 2, …) and is ignored.` | Name variant folders with the number only. |

A variant folder with a number the object does not have (say `tree/7`) is never used, and no line is written for it.
