---
name: import-model
description: Bring a user's own 3D model or texture into Ground of Aces as an object, terrain object or biome art mod. Use when the user says "my own model", "import a 3D model", "reskin", "replace the look of", "custom object", "FBX", "glTF", "terrain object", "biome".
---

# Import a model

Art mods are the least forgiving mod type and the validator does not check them. Follow the docs exactly and invent nothing.

## 1. Read first

- Objects and models: `docs/en/content/objects.md`
- Terrain objects: `docs/en/content/terrain-objects.md`
- Biomes: `docs/en/content/biomes.md`

If the page for the user's case is missing, say so, do not guess the file layout, and point them to the Discord modding channel: https://discord.com/channels/1006159027157356587/1551969822911242240

## 2. Understand the idea

Ask one at a time: mod id; which game object the art replaces or adds; which file(s) they have (format, where they are). Check the format and size limits against the docs before copying anything.

## 3. Scaffold and write

Create `mods/<mod_id>/` with `config.json` (from `templates/config.json`) and the folder the docs name (`Objects/`, `TerrainObjects/` or `Biomes/`). Copy the user's files in and write any settings file exactly as the docs show. Prefix new ids with the mod id.

## 4. Validate

Run `python tools/validator/goa_validate.py mods/<mod_id>` for any scripts or missions in the mod. For the art itself, go through the checklist in the docs page by hand and tell the user it is unchecked until seen in the game.

## 5. Install and hand over

Follow `install-mod`. Tell the user: art is imported once when the game starts, so **quit and restart the game**, check in Main menu -> Mods that the mod is on, load a game and look at the object. Ask what they see; on trouble `read-log`.
