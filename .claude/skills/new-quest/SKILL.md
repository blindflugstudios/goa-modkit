---
name: new-quest
description: Build a Ground of Aces quest (checklist in the quest panel) in mods/<mod_id>/Quests/ with its text script. Use when the user says "add a quest", "new quest", "objective", "task list", "quest chain", "the player should build/collect/fly X".
---

# New quest

Read `AGENTS.md` sections 6, 9 and 11. Source of truth: `docs/en/quests/index.md` and `enums.SubQuestRequirementType` in `generated/catalog.json`.

## 1. Understand the idea

Ask one at a time, with defaults:

1. **Mod id** (new or existing mod in `mods/`).
2. **The steps** - what must the player do? Map each step to a step `_type` from `docs/en/quests/index.md`. If nothing fits, say so: quests can only count what the game offers. A mission or event script can fill the gap.
3. **When it starts** - on every map (empty `_requirements`), after another quest (type `1`), or only on a map that lists it (type `3`, see the `new-map` skill).

## 2. Scaffold

New mod: copy `templates/quest/` to `mods/<mod_id>/`. Existing mod: copy the quest JSON into `Quests/` and the text script into `Missions/` (or add to the mod's existing text script).

## 3. Write

- File name = `_questId` = `<mod_id>_<name>`.
- Text fields are keys: `<mod_id>/<quest>/title`, `.../step0_title`, `.../step0_description`. `_questDescription` may be `""`.
- Every key gets words in the text script (`localization.SetTerm("en", key, text)` inside `try/except`).
- Per step: `_amount` >= 1; no spaces in `_parameter`; types `0`, `1`, `21` need a number; `20`, `24` need their second token; `12`/`17` need a skill or `any_skill_type`; a non-empty `12`, `13` or `17` filter needs at least one aircraft id; never `3` or `15`; no tutorial-only events.
- `_genericIconKey` from the icon list in `docs/en/quests/index.md` (or `""`).
- `_questType: 0`. Never `_requirementType: 2`. No cheat fields.
- Steps that wait for your own mission: `_type: 7`, `_parameter: "airplane_on_mission_succeed,<mission_id>"`.

## 4. Validate

`python tools/validator/goa_validate.py mods/<mod_id>` until 0 errors, plus `AGENTS.md` section 13.

## 5. Install and hand over

Follow `install-mod`. Then tell the user:

1. Save, then Options -> Quit to main menu.
2. Main menu -> Mods. If the mod folder is new, or the mod just got its `Quests/` folder, press **Refresh** - opening the window alone does not rescan. The mod is listed and switched on.
3. Load the save again or start a game - quest files are read on every level load. To hand the quest out now: Options -> Cheats on (first time), click the cheat button on the game screen, type `quest <quest_id>`.

Ask what the quest panel shows. Blank titles mean the text script did not run; see `read-log`.
