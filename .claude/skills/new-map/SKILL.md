---
name: new-map
description: Ship a Ground of Aces map in a mod, optionally with its own quest line and its own missions (tags, StartingQuestIds). Use when the user says "my own map", "custom airfield", "map with a campaign", "quest line for my map", "only these missions on my map".
---

# New map

Read `AGENTS.md` sections 6, 7 (tags) and 9. Sources: `docs/en/content/maps.md`, `docs/en/quests/index.md`, `templates/map-quest-line/README.md`.

## 1. Understand the idea

Ask one at a time:

1. **Mod id**.
2. **Does the map exist yet?** Maps are made in the game's map editor, not by you. If there is none, walk the user through `docs/en/content/maps.md` and wait until they have saved one.
3. **Quest line?** The game's main line (`quest0`), their own, or both.
4. **Missions?** All normal missions, only their own, or both.

## 2. Scaffold

Copy `templates/map-quest-line/` to `mods/<mod_id>/`. Ask the user to copy their saved `.goamap` into `mods/<mod_id>/Maps/` (or copy it for them once they tell you where it is), then delete `PUT_YOUR_MAP_HERE.md`. The map id is the file name: make it distinctive (`<mod_id>_<name>.goamap`) so it does not replace a built-in map.

## 3. Write

- **Quests:** first quest gets `"_requirements": []` and is listed in the map's `StartingQuestIds` (that list alone ties it to the map); later ones chain with type `1`. Text keys registered in the text script.
- **Map metadata:** a `.goamap` is a zip archive with `Metadata.json` inside. The keys that matter here:
  - `StartingQuestIds`: e.g. `["<mod_id>_campaign_start"]`, or `["quest0", "<mod_id>_campaign_start"]` for both.
  - `_tags`: e.g. `["<mod_id>_campaign"]` to keep ordinary missions away; add `"default"` to keep them.
  Prefer that the user sets both in the map editor's map settings (fields for tags and starting quests) and saves again. Only edit the zip yourself if they ask, and then change nothing else in it.
- **Missions for this map:** build them with `new-mission` and give each `"_tags": ["<mod_id>_campaign"]`.

## 4. Validate

`python tools/validator/goa_validate.py mods/<mod_id>` until 0 errors. It checks quests, missions and scripts, not the map file itself. Check by hand that every id in `StartingQuestIds` has a quest file (an unknown id is skipped without a message).

## 5. Install and hand over

Follow `install-mod`. Tell the user: go to the main menu (save and quit if a game is open), open Mods (press **Refresh** if the mod folder is new - opening the window alone does not rescan; check the mod is on), then start a new game on the map. Ask what they see; on trouble `read-log`.
