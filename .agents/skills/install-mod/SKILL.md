---
name: install-mod
description: Copy a mod from mods/<mod_id>/ into the game's Mods folder and tell the user how to load it in Ground of Aces. Use when the user says "install", "put it in the game", "copy to the game", "try it in the game", and at the end of every build skill.
---

# Install a mod into the game

Only install a mod that has passed `validate` with 0 errors.

## 1. Find the Mods folder

1. Read `.goa-modkit.local.json` in the repo root. If it has a confirmed `mods_folder` that still exists, use it and skip to step 2.
2. Otherwise detect the OS (`uname -s` on Mac/Linux; on Windows `$env:OS` is `Windows_NT`) and build the default path:

| OS | Mods folder | Player.log |
|---|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods` | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods` | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Mods` | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

3. Check the folder exists. If not: the game has never been started on this computer (or it is installed differently) - ask the user to start the game once, or to open **Main menu -> Mods -> Open folder** and tell you the path.
4. **Ask the user to confirm the path** the first time ("I will copy your mod into this folder: ... Is that right?").
5. Save it:
   ```json
   { "os": "macos", "mods_folder": "/Users/name/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods", "player_log": "/Users/name/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log" }
   ```
   This file is git-ignored and only on this computer.

## 2. Copy (never symlink)

Replace only this one mod's folder, so files deleted in `mods/<mod_id>/` also disappear from the game. First delete any `__pycache__` folder or `.DS_Store` file inside `mods/<mod_id>/` - they do not belong in a mod:

- Mac/Linux:
  ```bash
  rm -rf "<mods_folder>/<mod_id>" && cp -R "mods/<mod_id>" "<mods_folder>/<mod_id>"
  ```
- Windows (PowerShell):
  ```powershell
  Remove-Item -Recurse -Force "<mods_folder>\<mod_id>" -ErrorAction SilentlyContinue; Copy-Item -Recurse "mods\<mod_id>" "<mods_folder>\<mod_id>"
  ```

Double-check `<mod_id>` is not empty before running the delete. Never delete anything else, never touch other mods or Workshop items. The game does not follow symbolic links or junctions, so a link would silently load nothing.

Check the result: `<mods_folder>/<mod_id>/` directly contains `config.json` and the content folders (not one folder too deep).

## 3. Tell the user how to load it

There is no `reload_mods` in the public game. In plain steps:

1. If the game is running with a save open: save, then **Options -> Quit to main menu**. If it is not running, start it.
2. Main menu -> **Mods**. If the mod folder is new (first install) or renamed, its `config.json` changed, or the mod got a new content folder such as `Quests/`, press **Refresh** - opening the window alone does not rescan. The mod should be listed and switched on.
3. Load the save again, or start a new game.
4. **If the mod has art** (`Objects/`, `Biomes/`): restart the whole game instead - art is imported only at game start (a future update adds a reload option in the main menu). Missions, scripts, quests, maps, airplane skins (`Airplanes/`) and CSV only need steps 1-3: they are read each time a level is loaded.
5. To test right away: switch on **Options -> Cheats** once; with a game loaded, click the cheat button on the game screen and type e.g. `create_mission <mission_id>` or `quest <quest_id>`, then Enter.

The Mods window shows a **Scripting** switch on every mod. It is reserved for a coming opt-in and currently changes nothing - scripts in an enabled mod run either way - so do not present it as protection.

## 4. Ask

"What do you see?" Wait for the answer. If something is wrong, use `read-log`.
