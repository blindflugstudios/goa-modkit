# Your first mod

Welcome to the flight line. A Ground of Aces mod is **a folder of ordinary files** inside the game's `Mods` folder: JSON, CSV and Python files for missions, quests, scripts and game data, and models (`.fbx`, `.glb`) and PNG images for new art. You do not need a download, an account or programming tools. Missions, quests, scripts and data changes need only a text editor. New art needs the program you make models or images with.

## Your first mod in five minutes - just the game

You will make the wooden wall cost one plank instead of two.

1. **Open the Mods folder.** Start Ground of Aces and in the main menu click **Mods → Open folder**. A file window opens. (If you would rather find it yourself: on Windows it is `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\`, on Mac `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/`.)
2. **Make the mod folder.** Inside `Mods`, create a folder called `my_first_mod`.
3. **Give the mod a name.** Inside `my_first_mod`, create a text file called `config.json` and paste this into it:

    ```json
    {
      "Id": "my_first_mod",
      "Name": "My First Mod",
      "Author": "Your name",
      "Version": "1.0.0"
    }
    ```

    `Name` is what the Mods window shows. `Id` is how the game tells mods apart: lower-case letters, digits and `_` only. All the fields are explained on [How mods work](mods.md#configjson).

    Use a plain text editor: Notepad on Windows, or TextEdit on Mac switched to plain text (**Format → Make Plain Text**). Check that the file really ends in `.json` and not in `.json.txt`.

4. **Make the change.** Inside `my_first_mod`, create a folder called `CSV`. The name `CSV` must be exactly that, in capital letters: the game recognises content by its folder names. Inside `CSV`, create a text file called `ResourceCost.json` and paste this into it:

    ```json
    {
      "Commands": [
        { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
      ]
    }
    ```

5. **Load it.** In the game, open **Mods** and press **Refresh**. **My First Mod** appears in the list, switched on. Load your save.
6. **Look.** Open the build menu: the wooden wall now costs one plank.

That is a complete mod. You now have this:

```text
Mods/
  my_first_mod/
    config.json
    CSV/
      ResourceCost.json
```

From now on it always works the same way: change a file, go to **Options → Quit to main menu**, load your save again, and see the result. [Testing and reloading](testing.md) explains the details, and [How mods work](mods.md) lists every folder a mod can have.

!!! tip "Back up your saves"
    Modding is a developer preview. Copy your save files somewhere safe before you try a mod.

## Pick your way from here

| Your goal | Where to go |
|---|---|
| **Build a mission in the game, without writing files by hand** | The **Mission Editor** in the game's main menu. You fill in fields, and it checks your mission when you save it. See [Without an AI agent](../start/without-ai.md#the-easiest-route-the-in-game-mission-editor). |
| **Write mods by hand** | A text editor and these pages are enough. Read a topic page: [Missions](../missions/index.md), [Quests](../quests/index.md), [Scripting](../scripting/index.md), [CSV tables](../data/csv.md), [Maps](../content/maps.md), [Objects](../content/objects.md), [Airplane skins](../content/airplanes.md). They show every file and field, with examples you can type in. [Write your first mission](../missions/first-mission.md) is a good next step. |
| **Copy working examples and check your mod for mistakes** | Get the [modkit](../start/index.md), then follow [Without an AI agent](../start/without-ai.md). |
| **Let an AI agent build the mod for you** | Claude Code, Codex or the open-source OpenCode. Start with [Get started with AI modding](../start/index.md). |

Keep the [Glossary](../start/glossary.md) open in a second tab if a word is new to you.
