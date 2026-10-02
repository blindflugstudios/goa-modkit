---
name: import-model
description: Bring a user's own 3D model, texture, build-menu icon, ground texture or airplane paint scheme into Ground of Aces as an art mod (Objects/, Biomes/, Airplanes/). Use when the user says "my own model", "import a 3D model", "reskin", "replace the look of", "custom object", "new icon", "FBX", "glTF", "biome", "ground texture", "airplane skin", "paint scheme", "livery", "repaint a plane".
---

# Import a model, texture or airplane skin

Art mods are the least forgiving mod type and the validator does not check them. Follow the docs exactly and invent nothing.

## 1. Read first

- Objects (models, textures, icons): `docs/en/content/objects.md`
- Which ids can be changed: `docs/en/content/moddable-objects.md` (build menu, workbenches, training objects)
- Built-in texture names (texture-only repaints): `docs/en/content/texture-names.md`
- Ground types: `docs/en/content/biomes.md`
- Airplane paint schemes: `docs/en/content/airplanes.md`

If something the user wants is not on those pages, say so, do not guess, and point them to the Discord modding channel: https://discord.com/channels/1006159027157356587/1551969822911242240

## 2. Understand the idea

Ask one at a time: mod id; which game object, ground type or airplane the art is for; which file(s) they have (format, size, where they are). Check the id against `moddable-objects.md` before copying anything. Only the look changes: size on the grid, cost, crew spots and collision stay the game's.

## 3. Scaffold and write

Create `mods/<mod_id>/` with `config.json` (from `templates/config.json`) and the art folder:

- **`Objects/`** - one pool for all models, textures and thumbnails; subfolders allowed but their names mean nothing (a file is known by its name alone).
  - Model: `<objectId>[.destroyed].glb|.fbx` - `Chair.glb`, `Chair.destroyed.fbx`. Every model needs its `.destroyed` model: the game always shows the destroyed look. `.glb` beats `.fbx`. Ids are case-insensitive.
  - Textures, tried in this order: (1) `<material>_BaseMap_<UDIM-Tile>.png` / `<material>_Specular_<UDIM-Tile>.png` named after the model's material; (2) a PNG named like the image the material uses; (3) a PNG named like a built-in texture (repaints the game's model, no model needed). UDIM tiles `1001`-`1003`.
  - Thumbnail: `<objectId>.thumbnail.png`, only used next to a model of the same id.
  - Optional `Objects/config.json`: `{"Objects": {"Chair": {"UseGameMaterial": false}}}`. Default (game material) keeps battle damage; `false` keeps the user's own material but loses battle damage and uses only way (2) textures.
  - Trees, rocks and other map objects (terrain objects) cannot be modded yet. If the user asks for that, say so plainly.
- **`Biomes/<number>.png`** - `0` to `23`, no leading zeros, directly inside `Biomes/`.
- **`Airplanes/`** - see section 4.

Copy the user's files in with those names. Do not rename the user's originals outside `mods/`.

## 4. Airplane skins

A skin is a new paint scheme for an existing airplane; it shows up in every skin selection next to the built-in ones. Read `docs/en/content/airplanes.md` first, including its airplane id table.

- `Airplanes/config.json` (required, directly in `Airplanes/`):
  `{"Skins": {"<skinId>": {"Airplane": "<airplane id>", "Name": "...", "BaseSkin": "..."}}}`. `Airplane` is required; `Name` defaults to the skin id; `BaseSkin` defaults to the airplane's first skin.
- `<skinId>_BaseMap_1001.png` is **required** (otherwise the skin is skipped). `<skinId>_BaseMap_1002/1003.png` and `<skinId>_Specular_1001/1002/1003.png` are optional; a missing tile keeps the base skin's texture.
- `<skinId>.thumbnail.png` is optional (the skin's icon).
- Paint on the airplane's existing UV layout; the model stays the same.
- Skins are read on **every level load**: loading a save is enough, no restart needed.

## 5. Pre-install checklist (do every item by hand)

- [ ] Model files at most **32 MB**.
- [ ] Textures at most **4096 × 4096** px and **10 MB**; thumbnails at most **512 × 512** px and **10 MB**; biome PNGs at most **4096 × 4096** px and **10 MB**. Each side counts on its own. Oversized images are skipped, never scaled down.
- [ ] Every image is a **real PNG** (check the file header, not just the extension; a renamed JPEG is refused).
- [ ] No Blender duplicate names like `Chair.001.fbx`.
- [ ] Every model has a `.destroyed` model with the same id.
- [ ] Every thumbnail sits next to a model with the same id.
- [ ] Texture names match the material names in the model (`<material>_BaseMap_1001.png`) or the image names the materials use; for a texture-only repaint, the name is copied exactly from `texture-names.md`.
- [ ] FBX files have no textures embedded that the user relies on: embedded FBX images are never read, so the PNGs must be in `Objects/`. Only the first UV map is read; triangulate concave faces.
- [ ] Each object id exists in `moddable-objects.md`; biome numbers are `0`-`23`; skin `Airplane` ids are from `airplanes.md`.
- [ ] No two files with the same name in different subfolders of `Objects/`.
- [ ] `Objects/config.json` and `Airplanes/config.json` are valid JSON (no comments, no trailing commas).

Run `python tools/validator/goa_validate.py mods/<mod_id>` if the mod also has scripts or missions. Tell the user the art itself is unchecked until they see it in the game.

## 6. Install and hand over

Follow `install-mod`. Then tell the user:

- **Objects and biomes:** art is imported once when the game starts, so **quit the game completely and start it again**, check in Main menu -> Mods that the mod is on, load a game and look at the object or ground.
- **Airplane skins only:** quit to the main menu and load the save again; the skin appears in the airplane's skin selection.

Ask what they see. On trouble, use `read-log` and look for `[Mod <mod_id>]` lines (the detailed lines may only appear in development builds).
