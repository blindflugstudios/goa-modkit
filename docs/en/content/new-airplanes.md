# New airplanes (in progress)

!!! warning "In progress"
    New airplanes are still being built. They are not in the public game yet, and details on this page may change.

A mod can add a whole new airplane type: its own model, paint, name, stats and crew window drawing. Each new airplane is **based on** one of the game's airplanes and copies everything you do not give it from that airplane: stats, crew, crash animation, the flight path in the scramble result and the serial number blocks. The scramble result shows your model, flying the based-on airplane's path. The only thing you must give is the model.

A new paint scheme for an airplane the game already has is a skin, not a new airplane: see [Airplane skins](airplanes.md).

!!! tip "Example mods"
    `examples/airplane_captured_bf109` adds a captured Bf 109 fighter based on the Spitfire. `examples/airplane_captured_he111` adds a captured He 111 bomber based on the Stirling, with two propellers and a crew of five set through `Crew` and `CrewSlots`. Copy one into your `Mods/` folder to see a complete new airplane in the game.

## The airplane's folder

Every new airplane gets a folder inside the mod's `Airplanes/` folder, named after the airplane's id:

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

Without a paint the model shows the based-on airplane's first skin; without a wreck, the based-on airplane's wreck is used; without a thumbnail or a blueprint, the based-on airplane's are shown. The paint's tiles and specular files are named like a skin's, see [Textures](airplanes.md#textures). The thumbnail may be at most 512 × 512 pixels and 10 MB; a larger one is skipped with a warning in the [log](../start/troubleshooting.md#find-the-playerlog) and the based-on airplane's picture is shown.

## `config.json`

New airplanes go under `Airplanes` in the mod's `Airplanes/config.json`, the same file that lists [skins](airplanes.md#configjson):

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
| `BasedOn` | yes | The game's airplane the new one copies. An id from [Airplane ids](airplanes.md#airplane-ids). |
| `Name` | no | The name the game shows. One text for all languages. Without it, the airplane's id is shown. |
| `FullName`, `ShortName` | no | Longer and shorter name, shown in the order window and the crew window. Without them, `Name` is used. |
| `Manufacturer`, `Armament`, `MaximumSpeed`, `Engine`, `Range`, `Ceiling`, `Dimensions` | no | The details the order window lists. Empty when left out. |
| `Stats` | no | Stats that differ from the based-on airplane, keyed by the column names of the game's airplane table (`Health`, `Crew`, `Fuel Capacity`, ...). Values are text: `"Health": "90"`, `"Crew": "Pilot,Gunner"`. |
| `CrewSlots` | no | Where each crew member's slot sits on the blueprint, in crew order, as `[x, y]` fractions of the drawing: `[0, 0]` is the bottom left corner, `[1, 1]` the top right. Slots you leave out are spread across the middle. |
| `HiddenMarkings` | no | The markings the game should not draw on the airplane's own skins, because their textures already paint them, e.g. `["LeftText", "RightText"]`. Same names as for a skin, see [Hiding the game's markings](airplanes.md#hiding-the-games-markings). Without it, every marking that has a [marking point](#marking-points) is shown. |
| `PropellerDirection` | no | The way the propellers turn, as seen from the pilot's seat. `"CounterClockwise"` turns them counter-clockwise; any other value, or none, turns them clockwise. It is not taken from the based-on airplane. |

A skin may be painted on your new airplane too: write the airplane's id from `Airplanes` (here `Bf109`) as the skin's `Airplane`.

## Naming the parts of the model

The game finds the parts of your model by their node names. Capital letters, `-`, `_`, `.` and spaces do not matter, so `Air-Pivot`, `air_pivot` and `AirPivot` are the same. The game's own airplanes use exactly these names, so you can look at one in your 3D program.

| Node name | What the game does with it | Without it |
|---|---|---|
| `Air-Pivot` | The part that tilts in flight. Put everything that moves with the airplane under it. | Your model tilts with the based-on airplane's pivot. |
| `Propeller-Pivot` (one per propeller, e.g. `Propeller-Left-Pivot`) | Spins around the airplane's nose axis while the engine runs. Which way it turns is set by `PropellerDirection` in `config.json`. Its rotation does not matter. | No propeller spins. |
| `Wheel-Left`, `Wheel-Right`, `Wheel-Tail` | The angle the airplane rests at on the ground is worked out from where these touch the ground. For a nose wheel, use `Wheel-Front` instead of `Wheel-Tail`: the airplane then rests level, as modelled. The wheels also roll while the airplane moves on the ground: see [Wheel pivots](#wheel-pivots). | The based-on airplane's angle is used, and no wheel rolls. |
| `1-Interaction-Pilot`, `2-Interaction-Gunner`, ... | The crew seats, one per crew member. See [Crew seats](#crew-seats). | The based-on airplane's seats. |
| `Interaction-Paint` | Where the crew stand to paint and refuel the airplane. Put it beside the fuselage. Only its spot on the ground counts: the crew stand on the ground below it, facing the fuselage, however far the airplane tilts back on its wheels when parked. Its height and rotation do not matter. | The based-on airplane's spot. |
| `FireEmitter` | The mesh fire burns on. | The largest part directly under `Air-Pivot` that is not glass or the inside. |

- **Size and facing.** Build the airplane in metres at its real size, standing on the ground at the origin, like the game's own airplanes. Export it the way they are made: Blender's default FBX export, with the nose along Blender's +Y and up along +Z. The rotation of `Air-Pivot`, the propeller pivots and the seats does not matter: the game puts them on the airplane's own axes. Only marking points use their own rotation (see [Marking points](#marking-points)). Which way the nose points does not matter if the model has a `Propeller...` node and a `Wheel-Tail` node: an airplane whose propeller sits behind its tail wheel is turned around. A model without them, such as a jet, must face that way.
- **Landing gear.** A retractable gear needs one animation (take) in the model file that keys only the gear parts. Its first frame is the gear down, as modelled; its last frame is the gear fully up. The game holds the take between the two by the airplane's height: down on the ground, up from 10 m. Do not key the propellers or `Air-Pivot`; the game moves them itself. Fixed gear: no animation.
- **Marking decals** (squadron codes, roundels, serial number) show only where your model has marking points, see [Marking points](#marking-points).

## Crew seats

Every crew member sits on a seat node while the airplane flies, waits on the runway or is shown in the order window. Put one empty node (no mesh) in your model per crew member, where that crew member sits, and name it `<number>-Interaction-<role>`:

```text
1-Interaction-Pilot
2-Interaction-BombAimer
3-Interaction-Navigator
4-Interaction-RadioOperator
5-Interaction-Gunner
```

- **The number decides who sits where.** Seat `1` belongs to the first crew member in the airplane's `Crew` list, seat `2` to the second, and so on. The list is the based-on airplane's crew, or the one you set under `Stats` (`"Crew": "Pilot,BombAimer,Navigator,RadioOperator,Gunner"`). Number the seats in the same order as that list.
- **The role word is only for you.** The game does not read it: `3-Interaction-Navigator` is simply seat 3. Write the role that sits there, so the model stays readable.
- **One seat per crew member.** With fewer seats than crew members, the crew members without a seat of their own are all put at one spot taken from the based-on airplane instead of sitting in the model. Extra seats are not used.
- **Numbers count, gaps do not.** The seats are sorted by their number, so `1`, `2`, `5` work like `1`, `2`, `3`. A seat without a number comes after the numbered ones.
- **Names to avoid.** Every node with `Interaction` in its name is a seat, except `Interaction-Paint` (the paint spot, see the table above) and names that contain `Main`. Do not use `Interaction` in the name of anything else.
- **Facing.** Every crew member sits upright and faces the nose, whatever the seat's rotation. Only the seat's position counts.
- **Tilting.** Put the seats under `Air-Pivot`, so the crew tilt with the airplane in flight.
- **Crew window.** The crew window drawing places its slots through `CrewSlots`, in the same order as the seats (see [`config.json`](#configjson)).

## Wheel pivots

Every wheel rolls while the airplane moves on the ground: taxiing, the take-off and landing roll, being pushed by the crew. Give each wheel a pivot node of its own, with only the wheel under it:

```text
Air-Pivot
  Wheel-Retractor-Left-Pivot      gear leg, does not roll
    Wheel-Retractor-Left-Mesh
    Wheel-Left-Pivot              rolls
      Wheel-Left-Mesh             tyre and hub
  Wheel-Tail-Pivot                rolls
    Wheel-Tail-Mesh
```

- **Only the wheel under the pivot.** A wheel rolls when its node's name starts with `Wheel` and every mesh under it is round, like a tyre seen from the side. A gear leg, a fork, a mudguard or a gear door under the same node stops that node from rolling: put them next to the wheel pivot, not under it. If the tyre mesh itself is named `Wheel-...` (e.g. `Wheel-Tail-Mesh` beside a `Wheel-Tail-Fork`), that mesh rolls on its own.
- **Names that never roll.** Nodes with `Retractor` or `Flapdoor` in their name are gear legs and doors; they move only with the gear animation.
- **Rotation and origin do not matter.** The game turns each wheel around the airplane's side axis through the middle of the tyre mesh, so the pivot's own axes and its exact position on the axle do not count.
- **Size counts.** How fast a wheel turns comes from the size of its tyre mesh, so a small tail wheel turns faster than the main wheels, as it should.
- **Retractable gear.** The wheels roll only on the ground. The gear animation can still fold them away: key the wheel pivots in the gear take as before (see **Landing gear** under [Naming the parts of the model](#naming-the-parts-of-the-model)).
- **Without wheel pivots** the airplane still drives on the ground, its wheels just do not turn.

## Jets

A jet works like any other new airplane, with these differences:

- **Base it on `meteor` or `vampire`.** Only they have the jet exhaust (see [Effect points](#effect-points)), and a jet based on them also rests at a jet's angle when it has no `Wheel-Front`.
- **No propeller nodes.** Leave out every `Propeller-...-Pivot`. Nothing spins, and nothing else needs them.
- **Nose wheel.** Name it `Wheel-Front` and leave out `Wheel-Tail`, so the jet rests level, standing on all its wheels as modelled. Without either, it rests at the based-on airplane's angle.
- **Facing.** Without a propeller the game cannot tell the nose from the tail, so build the jet facing like the game's own airplanes (see **Size and facing** above).

## Effect points

The airplane's effects come from the based-on airplane, and they sit where they sit on that airplane. On a model of a different size, wheel dust ends up beside the wheels and smoke away from the engine. Put an empty node (no mesh) in your model at each spot where an effect belongs and name it as below; the game moves the effect there. All of them are optional: an effect without a point stays where the based-on airplane has it. Only the position counts, so the node's rotation and its place in the hierarchy do not matter: the effects always move with `Air-Pivot`.

| Node name | Effect | When it shows | One or many |
|---|---|---|---|
| `Effect-WheelDust-...` (e.g. `Effect-WheelDust-Left`, `-Right`, `-Tail`) | Dust thrown up by a wheel. Put it where the tyre touches the ground. | While the airplane rolls on the ground. | One per point |
| `Effect-WingTrail-...` (e.g. `Effect-WingTrail-Left`, `-Right`) | The thin trail behind a wing tip. | In flight. | One per point |
| `Effect-Exhaust-...` | Jet engine exhaust. Put it at the nozzle. Only shows when the based-on airplane is a jet (`meteor`, `vampire`). | While the engine runs. | One per point |
| `Effect-Sparks` | Sparks of a damaged airplane. | Below half health. | One |
| `Effect-Smoke` | Smoke from a hit engine. | On a landing with a smoking engine. | One |
| `Effect-SmokeTrail` | A thick smoke trail. | While the airplane is disabled. | One |
| `Effect-Explosion` | The explosion of a crash. Put it on the ground in front of the airplane. | When the airplane crashes on landing or while being moved. | One |
| `Effect-FireSmoke` | The smoke above a burning airplane. | While the airplane burns. | One |

- **One per point:** the game makes one copy of the effect for every point you give, so a twin-engine airplane can have `Effect-Exhaust-Left` and `Effect-Exhaust-Right`. All copies are the same effect: the based-on airplane's first one of that kind.
- **One:** only the first node with exactly that name is used.
- **Fire** needs no point: it burns on the `FireEmitter` mesh (see the table above).
- **Only the based-on airplane's effects.** The points move effects; they cannot add one. A new airplane has exactly the effects of the airplane it is based on: jet exhaust only when it is based on `meteor` or `vampire`, wing trails only when the based-on airplane has them. Choose `BasedOn` with this in mind.

## Marking points

A new airplane carries the marking decals of the airplane it is based on, in that airplane's style, sizes and colours: the squadron code, the airplane's own letter, the roundels, the fin flash and the serial number. The game cannot know where they belong on your model, so it shows a marking only where your model names a spot for it. Put an empty node (no mesh) in your model for each marking you want and name it `Marking-<side>-<slot>`, for example `Marking-Port-Image`. Every point is optional: a marking without a point is not shown, and a model without any marking point shows no markings at all. Painting the markings into your texture instead still works.

| Slot | What it shows |
|---|---|
| `LeftText` | The squadron code, the part of the designation before the `-` (`U5` of `U5-G`). |
| `Image` | The roundel on the fuselage. |
| `RightText` | The airplane's own letter, the part of the designation after the `-` (`G` of `U5-G`). |
| `Nose` | Nothing on a new airplane yet: nose art comes from the skin of a built-in airplane, not from the based-on airplane. Paint nose art into your texture. |
| `Wing` | The roundel on top of the wing. |
| `UnderWing` | The roundel under the wing. |
| `FinFlash` | The fin flash on the tail fin. |
| `SerialNumber` | The airplane's serial number, e.g. `PT255`. |

- **Sides.** `<side>` is `Port` (the left side, seen from the pilot's seat) or `Starboard` (the right side). Each side needs its own points: `Marking-Port-Wing` and `Marking-Starboard-Wing` for the two wings.
- **Placing a point.** Put the point on the surface. With Blender's default FBX export, the point's local **-Z** axis points into the airplane, along the direction the marking is projected; its local **+X** axis is the direction the text reads and its local **+Y** axis is up for the text. An empty left at zero rotation therefore projects straight down: turn it so -Z points into the surface. For the fuselage on the `Port` side that is -Z toward the pilot's right with +X toward the tail; on the `Starboard` side -Z toward the pilot's left with +X toward the nose. For `Wing`, -Z points down into the wing, for `UnderWing` up into it. Blender's "Apply Transform" export option does not help: it moves every empty to the origin. Check the result in the game.
- **Size.** The markings keep the based-on airplane's sizes; the point's scale does not change them.
- **Depth.** A marking is projected through a box a few tens of centimetres deep, centred on the point, and paints everything inside it, a crew member standing next to the fuselage included. Put the point exactly on the surface, so the box reaches the skin and as little else as possible.
- **Codes and serial numbers** come from the game: every airplane gets its squadron code, its letter and a serial number when it arrives. If you give points for them, do not also paint them into your texture, or both show.

## Where a new airplane shows up

The game knows a new airplane as `mod_<modId>_<id>`, in lower case: the `Bf109` of the mod `captured_bf109` is `mod_captured_bf109_bf109`. It is unlocked from the start, appears in the order window, and is part of crash sites, the crew window and scrambles like any other airplane. Quests and promo codes do not know it.

## Saves and disabled mods

When a save holds a new airplane whose mod is no longer switched on, the airplane becomes the airplane it was based on. Switching the mod back on later does not turn it back.

## Seeing your changes

New airplanes are read each time a level is loaded, like skins: load a save to see a changed model, texture or `config.json`. For a new mod folder, press **Refresh** in the Mods window first. More in [Seeing your changes](airplanes.md#seeing-your-changes) and [Testing and reloading](../basics/testing.md).
