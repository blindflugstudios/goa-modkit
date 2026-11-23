# Captured Bf 109

A new airplane type: a captured Messerschmitt Bf 109 flown by the RAF. It is based on the Spitfire, so it flies, crashes and scrambles like one, but it has its own model, wreck, paint, crew window drawing, name, texts and a little less health.

## Installing

Copy this folder into your `Mods/` folder, switch the mod on in **Main menu → Mods** and load a save. The Bf 109 is in the order window next to the RAF's own airplanes.

## What is in it

```text
config.json                     the mod's id and name
Airplanes/
  config.json                   declares the airplane "Bf109", based on "spitfire"
  Bf109/
    Bf109.fbx                   the model
    Bf109.destroyed.fbx         the wreck at crash sites and after it is shot to pieces
    Bf109_BaseMap_1001.png      its paint (the default skin)
    Bf109.thumbnail.png         its picture in the order window and the airplane lists
    Bf109.blueprint.png         its drawing in the crew window
```

## How the model is set up

The node names in `Bf109.fbx` tell the game which part is which. The game's own airplanes use the same names:

| Node | What the game does with it |
|---|---|
| `Air-Pivot` | Tilts in flight; everything under it tilts with it. |
| `Propeller-Pivot` | Spins when the engine runs. |
| `Wheel-Left`, `Wheel-Right`, `Wheel-Tail` | The angle the airplane rests at on the ground is worked out from them. |
| `1-Interaction-Pilot` | Where the pilot sits. |
| `Interaction-Paint` | Where the crew stand to paint and refuel the airplane: on the ground below it, facing the fuselage. |
| `Bf109-Mesh` | The largest part, so fire burns on it. |

The model and the wreck were made from the game's placeholder Bf 109; they are rough on purpose. Replace them with your own and keep the names.

The model has no effect points and no marking points yet. Its effects (wheel dust, smoke, sparks, explosion) sit where the Spitfire has them, and it shows no marking decals: its crosses are painted into the texture. To place them on your model, add `Effect-...` and `Marking-<Port|Starboard>-<slot>` nodes; the airplanes page of the docs lists them.

## Based on

`"BasedOn": "spitfire"` copies everything the mod does not ship from the Spitfire: stats, crew, crash animation, the airplane the scramble result shows and the serial number blocks. Only `"Health": "90"` is changed under `Stats`.
