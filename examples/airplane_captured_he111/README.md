# Captured He 111

A new bomber: a captured Heinkel He 111 flown by the RAF. It is based on the Short Stirling, so it flies bombing missions, crashes and scrambles like one, but it has its own model, wreck, paint, crew window drawing, name and texts, a crew of five instead of seven and a little less health.

Next to `airplane_captured_bf109` (a single-seat fighter), this example shows a twin-engined airplane with a crew of its own.

## Installing

Copy this folder into your `Mods/` folder, switch the mod on in **Main menu → Mods** and load a save. The He 111 is in the order window next to the RAF's own airplanes.

## What is in it

```text
config.json                     the mod's id and name
Airplanes/
  config.json                   declares the airplane "He111", based on "stirling"
  He111/
    He111.fbx                   the model
    He111.destroyed.fbx         the wreck at crash sites and after it is shot to pieces
    He111_BaseMap_1001.png      its paint (the default skin)
    He111.thumbnail.png         its picture in the order window and the airplane lists
    He111.blueprint.png         its drawing in the crew window
```

## How the model is set up

The node names in `He111.fbx` tell the game which part is which. The game's own airplanes use the same names:

| Node | What the game does with it |
|---|---|
| `Air-Pivot` | Tilts in flight; everything under it tilts with it. |
| `Propeller-Left-Pivot`, `Propeller-Right-Pivot` | One per engine; each spins when the engines run. |
| `Wheel-Left`, `Wheel-Right`, `Wheel-Tail` | The angle the airplane rests at on the ground is worked out from them. |
| `1-Interaction-Pilot` ... `5-Interaction-Gunner` | The five crew seats, in the order of the number in front. |
| `Interaction-Paint` | Where the crew stand to paint and refuel the airplane: on the ground below it, facing the fuselage. |
| `He111-Mesh` | The largest part, so fire burns on it. |

The model and the wreck were made from the game's placeholder He 111; they are rough on purpose. The placeholder flies with its main gear retracted, so the main wheels are simple added cylinders. Replace them with your own and keep the names.

The model has no effect points and no marking points yet. Its effects (wheel dust, smoke, sparks, explosion) sit where the Stirling has them, and it shows no marking decals: its crosses are painted into the texture. The Stirling has no wing trails, so neither does this airplane. To place the effects and markings on your model, add `Effect-...` and `Marking-<Port|Starboard>-<slot>` nodes; the airplanes page of the docs lists them.

## Based on and crew

`"BasedOn": "stirling"` copies everything the mod does not ship from the Stirling: stats, crash animation, the airplane the scramble result shows and the serial number blocks. Two stats are changed under `Stats`:

- `"Health": "90"` - a little less than the Stirling's 100.
- `"Crew": "Pilot,BombAimer,Navigator,RadioOperator,Gunner"` - five crew members instead of the Stirling's seven. The roles are `Pilot`, `Gunner`, `Navigator`, `BombAimer`, `FlightEngineer` and `RadioOperator`.

`CrewSlots` places the five crew members on the crew window drawing, in the same order as `Crew`, as `[x, y]` fractions of the drawing with `[0, 0]` at the bottom left. The seats in the model follow the same order.
