---
name: publish-workshop
description: Prepare a finished Ground of Aces mod for the Steam Workshop and walk the user through the in-game upload. Use when the user says "publish", "upload to the Workshop", "share my mod", "put it on Steam", "update my Workshop item".
---

# Publish to the Steam Workshop

Source: `docs/en/sharing/workshop.md`. You cannot press the upload button; the user does it in the game.

## 1. Check the mod is ready

1. It has been tested in the game by the user. If not, stop and test first.
2. Run `python tools/validator/goa_validate.py mods/<mod_id>`: 0 errors.
3. In Claude Code, have the `mod-reviewer` subagent review `mods/<mod_id>/`; otherwise go through `AGENTS.md` section 13 yourself. Fix every finding.
4. `config.json` has a valid `Id` and a `Name` (the Workshop title; without it subscribers see a number).
5. Optional `preview.png` in the mod root: PNG, at most 1 MB, 512x512 recommended.
6. The **whole folder is uploaded.** Remove test files, backups, notes and anything private. A short `README.md` is fine.
7. Design check: players who subscribe may have scripts switched off at first. Say whether the mod still makes sense with only its JSON (missions with `_raw...` texts do; event scripts and quest texts do not).

## 2. Install the final version

Follow `install-mod` so the copy in the game's `Mods` folder is exactly the reviewed version. The upload takes the folder from there.

## 3. Walk the user through the upload

1. Start the game **through Steam** (DRM-free builds have no Workshop).
2. Main menu -> Mods -> press **Upload** on the mod.
3. First time: pick **Create new Workshop item...**. Update: pick their existing item instead, so players get an update rather than a second item.
4. Confirm, wait for the progress to finish, open the item page from the button.
5. Write the description on the Steam page (the game sends none). Accept the Workshop legal agreement there if Steam asks, or the item stays hidden.

## 4. Warn about updates

Removing a quest, renaming a mission id or reordering quest steps can strand players mid-playthrough. Append, do not rename.
