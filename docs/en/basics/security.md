# Python mods and safety

Short version: **a mod with Python scripts is a small program running on your computer.** Install script mods only from people you trust, and as a modder, never write scripts that reach outside the game.

## What the risk is

Mods that only contain JSON, CSV, maps or models are data. The game reads them, and the worst a broken one can do is break your game.

Mods with Python scripts (`.py` files) are different. The game runs them with IronPython, and **there is no sandbox**: the game does not stop a script from importing whatever it likes. A script can reach the .NET runtime and the file system, which means a badly meant script could read, change or delete files on your computer.

We are telling you this plainly because you should know it, not because Workshop mods are dangerous as a rule. The same is true for mods in most games that allow scripting.

## For players

- **Know which mods have scripts.** The **Mods** window shows which mods contain scripts.
- **Only use script mods from authors you trust**: people you know from the community, with a history of mods, comments and a Workshop page that explains what the mod does.
- **Subscribed Workshop mods are switched on by default.** You can switch any mod off in the **Mods** window.
- **The game asks before you turn on scripting for a mod.** Take that question seriously. If you are not sure about the author, say no, or unsubscribe.
- **Something odd?** Unsubscribe, and report the mod on its Workshop page and in the [modding channel on Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).

!!! tip "Check a mod before you trust it"
    Every Workshop mod is a folder of plain-text files. You can open its `.py` files in a text editor, or run the modkit's validator on the folder: it reads the scripts **without running them** and warns about anything that reaches outside the game.

## For modders

Your mod never needs anything outside the game's scripting API. Stick to it, and your players never have to wonder.

**Normal and fine**: the game's own scripting API, including imports from the game's `Blindflug.*` namespaces and the objects the game hands every script:

```python
from Blindflug.FlightMission import MissionEvent
from Blindflug.GameResources import ResourceType

localization.SetTerm("en", "missions/my_mission/mission_name", "Dawn Patrol")
```

**Never use** these. The validator warns about each of them:

| Import or call | Why it is off limits |
|---|---|
| `import clr` | The bridge into .NET, and from there to everything on the computer |
| `import System`, `from System.IO import ...` (anything under `System` or `Microsoft`) | Direct .NET access: files, processes, network |
| `import os`, `shutil`, `io`, `open(...)` | File system access (the validator only notes it, because of the one exception below) |
| `import sys`, `subprocess`, `ctypes`, `importlib` | Interpreter internals, starting programs, loading native code |
| `socket`, `urllib`, `http`, `ftplib`, `smtplib` | Network access |
| `pickle`, `marshal`, `exec`, `eval`, `compile`, `__import__` | Running code that is not visible in your file |

One exception for files: if a script needs to keep its own small state between sessions, the scripting API hands out a folder for that (`game_api.GetScriptDataPath`). Use only that folder.

### Before you publish

1. Run the validator and make sure there are **no** "reaches outside the game" warnings.
2. Say in your Workshop description that the mod contains scripts and what they do.
3. Keep your scripts readable. Players and reviewers can open them, and clear code builds trust.

The modkit's skills and examples follow these rules. If an agent ever suggests one of the imports above, tell it no.
