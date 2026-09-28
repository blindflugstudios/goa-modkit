---
name: import-model
description: Bring a user's own 3D model or texture into Ground of Aces as an object or biome art mod (work in progress, not supported by the current alpha). Use when the user says "my own model", "import a 3D model", "reskin", "replace the look of", "custom object", "FBX", "glTF", "terrain object", "biome".
---

# Import a model

**Art mods are work in progress and the current alpha does not support them.** Tell the user this before doing anything else, and do not promise that the art will show up in the game. Only continue if they still want to prepare the files for a later version.

Art mods are the least forgiving mod type and the validator does not check them. Follow the docs exactly and invent nothing.

## 1. Read first

- Objects and models: `docs/en/content/objects.md`
- Biomes: `docs/en/content/biomes.md`

Ignore everything inside `<!-- OUTDATED ... -->` comments on those pages: it describes the old per-folder layout.

If the page for the user's case is missing, say so, do not guess the file layout, and point them to the Discord modding channel: https://discord.com/channels/1006159027157356587/1551969822911242240

## 2. Understand the idea

Ask one at a time: mod id; which game object the art replaces or adds; which file(s) they have (format, where they are). Check the format and size limits against the docs before copying anything.

## 3. Scaffold and write

Create `mods/<mod_id>/` with `config.json` (from `templates/config.json`) and the art folder. Layout (preliminary, see the "Folder layout" section of the docs pages):

- `Objects/` is one flat folder for all models and textures. The model's file name is the id of the object it replaces (`Chair.fbx`, `Chair.destroyed.fbx`, `tree.2.glb`); subfolder names mean nothing. Textures are found by the name the material references (`Objects/wood-01.png`); `Chair.thumbnail.png` (max 256x256) replaces the build-menu icon. Settings go into one `Objects/config.json` keyed by id: `{"Objects": {"Chair": {"UseGameMaterial": false}}}`.
- Trees, rocks and other map objects also go into `Objects/`. There is no `TerrainObjects/` folder.
- `Biomes/<slot>.png`, one PNG per biome slot named by its number (`8.png`), directly inside `Biomes/`.

Copy the user's files in with those names. Prefix new ids with the mod id.

## 4. Validate

Run `python tools/validator/goa_validate.py mods/<mod_id>` for any scripts or missions in the mod. For the art itself, check the file names against the layout above by hand and tell the user it is unchecked until seen in the game.

## 5. Install and hand over

Follow `install-mod`. Tell the user: art is imported once when the game starts, so **quit and restart the game**, check in Main menu -> Mods that the mod is on, load a game and look at the object. Ask what they see; on trouble `read-log`.
