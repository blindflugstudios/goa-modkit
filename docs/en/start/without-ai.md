# Without an AI agent

Everything an agent does, you can do by hand. There are two routes.

## The easiest route: the in-game Mission Editor

No tools, no terminal. In the main menu, open the **Mission Editor**, create a mission, fill in the fields and save. The editor checks your mission when you save and refuses to save one that would break. Missions you save there land in the `Missions` folder next to the game's `Mods` folder and are loaded with your next game.

See [Write your first mission](../missions/first-mission.md) for a guided tour.

## The hand-made route: copy an example and edit it

This gives you a real mod folder you can share on the Steam Workshop later. You need a text editor and, for the check in step 4, Python (see the install pages for [Windows](install-windows.md#6-optional-install-python-recommended) or [Mac](install-mac.md#5-optional-install-python-recommended)). You also need the modkit on your computer, either with `gh repo clone blindflugstudios/goa-modkit` or by downloading it from [the GitHub page](https://github.com/blindflugstudios/goa-modkit) (green **Code** button → **Download ZIP**, then unzip).

### 1. Get a proper text editor

Use **[Visual Studio Code](https://code.visualstudio.com/)** (free, Windows and Mac). It colors JSON and Python, shows mistakes like a missing comma, and lets you open the whole modkit folder with **File → Open Folder**. Notepad and TextEdit work in a pinch, but TextEdit must be in plain text mode (**Format → Make Plain Text**).

### 2. Copy the example

Inside the modkit, make this folder structure and copy the two files from `examples/coastal_patrol/` into it:

```text
goa-modkit/
  mods/
    my_first_mod/
      Missions/
        coastal_patrol.json
        coastal_patrol.py
```

The folder name `Missions` matters: the game looks for content by folder name. The mod folder name (`my_first_mod`) is up to you.

### 3. Edit it

Open `coastal_patrol.json`. Try small changes first, save, and check each one:

```json
"_maxPlaneSlots": 2,
"_asPlannedChance": 80,
```

Raise `_maxPlaneSlots` to `3` to allow three planes, or lower `_asPlannedChance` to make things go wrong more often.

Open `coastal_patrol.py` and change the texts inside the quotes, for example the mission name:

```python
_term("mission_name", "Coastal Patrol")
```

!!! warning "Three things not to break"
    - `_missionOutcomes` must have **exactly 4** entries, in their order.
    - `_missionStats` must have **at least 2** entries.
    - The file names and the id returned by `get_mission_id` in the `.py` must match. If you rename the mission, rename both files and the `MISSION_ID` line together.

    [Missions reference](../missions/reference.md) explains every field.

### 4. Check it with the validator

The **validator** reads your mod and tells you what would go wrong in the game, without starting the game. Open the terminal in the modkit folder and run:

=== "Windows"

    ```powershell
    cd ~\goa-modkit
    python tools\validator\goa_validate.py mods\my_first_mod
    ```

=== "Mac"

    ```bash
    cd ~/goa-modkit
    python3 tools/validator/goa_validate.py mods/my_first_mod
    ```

**You should see** a summary line like `2 file(s) checked - 0 error(s), 0 warning(s), 0 note(s)`.

Each problem is printed as `file:line: error: ...` with a hint underneath. Fix the line it names, save, run again. Errors must go. Warnings are worth reading.

### 5. Copy it into the game

Copy the whole `my_first_mod` folder into the game's `Mods` folder. The quickest way to open that folder: in the game's main menu, **Mods → Open folder**. Or paste the path into Explorer or Finder:

=== "Windows"

    Paste into the Explorer address bar:

    ```text
    %USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\
    ```

=== "Mac"

    In Finder, press **Cmd+Shift+G** and paste:

    ```text
    ~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/
    ```

Copy the folder, do not create a shortcut or alias: the game skips linked folders.

### 6. Load it and fly

1. If a save is open, **Options → Quit to main menu**.
2. Open **Mods**. Your mod is listed. It has a `.py` file, so it also shows a **Scripting** switch: switch it on and confirm (the current game runs the scripts either way).
3. Load your save.
4. Turn on **Options → Cheats**, open the console with the cheat button and type `create_mission coastal_patrol`. The mission appears on the war map.

After each later change: validate, copy again (replace the old files), **Quit to main menu**, load your save (open **Mods** first if you added a new folder such as `Quests/`).

Nothing happening? See [When nothing happens](troubleshooting.md).
