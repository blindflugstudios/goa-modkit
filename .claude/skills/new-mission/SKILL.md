---
name: new-mission
description: Build a new Ground of Aces mission (JSON plus optional Python) in mods/<mod_id>/. Use when the user says "make a mission", "new mission where...", "add a flight/sortie/raid/patrol/escort", "mission chain", "follow-up mission" or "campaign".
---

# New mission

Read `AGENTS.md` sections 6, 7 and 11 first. Sources of truth: `docs/en/missions/reference.md`, `docs/en/missions/locations.md`, `generated/catalog.json`.

## 1. Understand the idea (one question at a time)

Find out, offering defaults:

1. **Mod id** - new mod or an existing one in `mods/`? Suggest an id from the idea (`channel_escort`), only `a-z 0-9 _`.
2. **What happens** - the story in one sentence. Map it to a skill pair: first stat rolled when it goes as planned, second when it goes wrong (`Fight`, `Bomb`, `Recon`, `Transport`, `Maneuverability`, `Stealthiness`).
3. **Where** - pick 1-3 places from `locations` in the catalog (sea missions need sea places). If the user wants a place that is not there, add it with the mod (see step 3, Locations).
4. **How hard** - `_difficultyRating` 1-3, `_asPlannedChance`, `_enemyPlaneReport` (max 18).
5. **Consequences** - what each of the four endings gives or costs (morale, victory points, damage).

Do not ask about things with a sensible default (timings, slots). Tell the user what you picked.

## 2. Scaffold

- New mod: copy `templates/mission/` to `mods/<mod_id>/`. Existing mod: copy only the two files from `templates/mission/Missions/` into its `Missions/`.
- Rename `my_mod_patrol.json` / `.py` to `<mod_id>_<name>`; set `MISSION_ID` to exactly that; set `config.json` `Id` and `Name`.
- Chains: start from `examples/chain_convoy/` or `examples/chain_airfield/`. Campaign with memory: `examples/campaign_kanalkampf/` (its `os`/`open` use is fine only because it goes through `game_api.GetScriptDataPath`; never use file access for anything else).

## 3. Write

JSON (field meanings in `docs/en/missions/reference.md`):

- `_missionOutcomes`: **exactly 4**, order gone wrong/fail, gone wrong/pass, as planned/fail, as planned/pass. `_missionSuccess` true on the two "skill passed" entries unless the story says otherwise.
- `_outcomeEffect` types from `enums.OutcomeEffectType`; keep the `_effectIcon` values used in the templates for the same type.
- `_missionStats`: **at least 2**, `_missionSkillType` from `enums.MissionSkillType`.
- `_missionIcon`: `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability` or `Stealth`.
- `_missionRequirements`: numeric `_value` as a string (`"1"`). Chain: `{"_requirementType": 3, "_value": "<prev_id>,success"}` and `"_isHistoric": true` on the follow-up (it then appears within the in-game hour after the gate passes, once; leave it off only for a repeatable follow-up that may come back through the weekly draw).
- `_potentialLocations`: copy id, name and coordinates from the catalog.
- `_tags`: leave `[]` unless the mission belongs to a tagged map.

Locations of the mod's own (only when the user wants a place the catalog lacks; `docs/en/missions/locations.md`, section "Adding locations with a mod"):

- One or more `.json` files directly in `mods/<mod_id>/Missions/Locations/` (no deeper folders), e.g. `<mod_id>_locations.json`: `{"Locations": [{"_locationId": "<mod_id>_scapa_flow", "_locationName": "<mod_id>_scapa_flow", "_coordinates": {"x": <latitude>, "y": <longitude>}, "_flags": 2}]}`.
- `_locationId` is required and is the lookup key; `_flags` a number. Keep id and name identical and prefixed with the mod id (shipped IDs win, a clash between two mods is silent). Keep coordinates inside the war map (latitude 40.75-61.25, longitude -11.75-21.64).
- In the mission's `_potentialLocations`, refer to it by ID only: `{"_locationId": "<mod_id>_scapa_flow"}`. A mission entry never carries coordinates, name or flags. The player sees the raw `_locationName` unless a script registers `mission_location/<name>` with `localization.SetTerm`.
- The validator only knows the catalog's places and warns about the new ID; tell the user that warning is expected.

Python (optional; delete it and use the `_raw...` JSON fields for a text-only mission):

- Define all nine `missions/<id>/<slot>` texts with `localization.SetTerm("en", ...)` at top level.
- Roll once in the first `send_mission_event` call; read afterwards.
- No dead handlers, no forbidden imports, nothing newer than Python 3.6.
- Text style: terse 1940s radio log, no exclamation marks.

## 4. Validate

Run `python tools/validator/goa_validate.py mods/<mod_id>` (see the `validate` skill if Python is missing). Fix until 0 errors, then the manual checks in `AGENTS.md` section 13.

## 5. Install and hand over

Follow the `install-mod` skill: copy `mods/<mod_id>/` into the game's `Mods` folder (confirm the path the first time), then tell the user:

1. Save, then Options -> Quit to main menu.
2. Main menu -> Mods. If the mod folder is new (first install) or renamed, press **Refresh** - opening the window alone does not rescan. The mod is listed and switched on.
3. Load the save again.
4. To see the mission now: Options -> Cheats on (first time only), click the cheat button on the game screen, type `create_mission <mission_id>`, press Enter, open the war map.

Ask what they see. On trouble use the `read-log` skill.
