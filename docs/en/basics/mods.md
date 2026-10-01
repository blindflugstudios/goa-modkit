# How mods work

A mod is a folder. The game looks inside it for a handful of fixed subfolders, and whatever those subfolders contain is what the mod changes. There is no packaging step, no manifest you have to write, and nothing to compile: you edit files, load a level, and see the result.

This page covers what every mod has in common: where it lives, how the game finds it, how it is switched on and off, and which mod wins when two change the same thing. What goes *into* the subfolders is on the category pages: [CSV tables](../data/csv.md), [Missions](../missions/index.md), [Quests](../quests/index.md), [Scripting](../scripting/index.md), the [Maps and art](../content/maps.md) pages and [Airplane skins](../content/airplanes.md). How a finished mod reaches other players is on [Steam Workshop](../sharing/workshop.md).

## A mod in one minute

1. Find your `Mods` folder: **Main menu → Mods → Open folder**. On Windows that is `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\`; the other platforms are listed [below](#where-mods-live).
2. Create a folder in it, for example `my_mod`, and inside it one of the content folders: `CSV/`, `Missions/`, `Quests/`, `Maps/`, `Objects/`, `Biomes/` or `Airplanes/`. Put at least one file in it.
3. Optionally add a `config.json` with the mod's name and id, and a `preview.png` (at most 1 MB) as its picture.
4. Press **Refresh** in the Mods window so the game notices the new folder, then load a level.
5. From then on, every change to a file inside the mod is picked up the next time you load a level. Only replacement art (`Objects/`, `Biomes/`) needs a restart of the game.

The folder can have any name - `MyMod` works as well as `my_mod`. Only the optional `Id` inside `config.json` has to be lower-case (`my_mod`, not `MyMod`). Prefix every id you invent with your mod's name, so you never replace something by accident.

!!! tip
    If this is your first mod, the shortest path from an empty folder to a visible change is a one-line [CSV table](../data/csv.md) change. The [first mod walkthrough](../start/first-mod.md) takes you through it step by step.

## Where mods live

The game reads mods from two places: the items you are subscribed to on the Steam Workshop, and your own `Mods` folder. Anything you make yourself goes into the second one.

| Platform | Mods folder |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Mods/` |

The folder is created the first time the game starts. The quickest way to reach it is the **Open folder** button in the Mods window (see below). The game also keeps a small `mod_state.json` in this folder. That file is the game's own record of which mods you switched on or off; it is not part of any mod, and you should not ship it.

### One mod is one folder

The folder can have any name you like - `MyMod`, `my_mod` or `My Campaign` all work. The lower-case rule further down applies only to the optional `Id` inside `config.json`, not to the folder.

Inside your mod's folder, each kind of content has a fixed subfolder. Only the ones you need have to exist:

```text
Mods/
  my_mod/
    config.json        optional - name, id, load order
    preview.png        optional - the picture shown in the Mods window and on the Workshop
    CSV/               data tables
    Missions/          mission .json files and Python .py scripts
      Locations/       new mission locations, .json
    Quests/            quest .json files
    Maps/              .goamap map files
    Objects/           replacement models, textures and icons
    Biomes/            replacement ground textures, one PNG per biome slot
    Airplanes/         new airplane skins
```

| Folder | What goes in it | Read more |
|---|---|---|
| `CSV/` | changes to the game's data tables | [CSV tables](../data/csv.md) |
| `Missions/` | missions (`.json`) and Python scripts (`.py`) | [Missions](../missions/index.md), [Scripting](../scripting/index.md) |
| `Missions/Locations/` | new mission locations (`.json`) | [Adding locations with a mod](../missions/locations.md#adding-locations-with-a-mod) |
| `Quests/` | quests (`.json`) | [Quests](../quests/index.md) |
| `Maps/` | maps (`.goamap`) | [Maps](../content/maps.md) |
| `Objects/` | replacement models, textures and icons - buildings, workbenches, trainers and map objects alike | [Objects and models](../content/objects.md) |
| `Biomes/` | replacement ground textures, one PNG per biome slot | [Biomes](../content/biomes.md) |
| `Airplanes/` | new airplane skins: a `config.json` and the skins' PNGs | [Airplane skins](../content/airplanes.md) |

Three rules decide whether the game notices the folder at all:

- A subfolder only counts when there is something in it. An empty `CSV/` folder is the same as no `CSV/` folder.
- A mod folder with none of the subfolders above (or only empty ones) is ignored without a message.
- Symbolic links and junctions (shortcuts that point to another folder) are never followed, neither as the mod folder nor as one of its subfolders. The game skips them with a warning in the log.

For `CSV`, `Missions`, `Quests` and `Maps` only files directly inside the subfolder are read; anything deeper is ignored, with one exception: `Missions/Locations/` is read as well. `Objects` and `Biomes` hold replacement art and follow their own rules: in `Objects/` a model's *file name* is the id of the object it replaces (`Chair.fbx` replaces the chair), and subfolder names mean nothing. `Biomes/` holds one PNG per biome slot, named after the slot's number (`8.png`), directly inside the folder. `Airplanes/` holds new airplane skins, described on [Airplane skins](../content/airplanes.md).

### `config.json`

Optional. Without it, the folder name is shown as the mod's name, its id is made from the folder name, and the load order is 100.

```json
{
  "Id": "my_mod",
  "Name": "My Mod",
  "Author": "Your Name",
  "Version": "1.0.0",
  "LoadOrder": 100
}
```

| Field | Meaning |
|---|---|
| `Id` | What the game uses to tell mods apart and to break load-order ties. 3–64 characters of lower-case letters, digits, `_`, `.` or `-`, starting with a letter or digit. |
| `Name` | What players see in the Mods window. Any text. It also becomes the Workshop title on a first upload. |
| `LoadOrder` | A whole number that decides the order in which mods are applied (see [Which mod wins](#which-mod-wins)). Lower numbers are applied first. Default `100`. |
| `Author`, `Version` | Kept for you and for the Workshop page. The game does not read them. |

What happens when something is off:

- An `Id` that breaks the rule is ignored without a message, and the folder name is used instead - lower-cased, with every character other than letters, digits, `_`, `.` and `-` replaced by `_`. Log lines about your mod are labelled with this id, so a rejected id shows up as a label you did not expect. The mod's details view in the Mods window also shows the id the game actually uses.
- A `config.json` the game cannot read (a missing comma, a stray bracket) is reported in the log and treated as if it were absent.

### `preview.png`

Optional. A PNG at the root of the mod folder, at most 1 MB. The Mods window shows it next to the mod's name, and it becomes the item's picture when you upload the mod to the Workshop. Without one the Mods window shows a placeholder picture, and the Workshop item has no picture until you add one on its Steam page.

## The Mods window

**Main menu → Mods** lists every mod the game found - Workshop subscriptions and your own folders - with its preview picture, a marker that says whether it came from the Workshop or from your `Mods` folder, and one badge per kind of content it carries.

| Control | What it does |
|---|---|
| **Enabled** switch (per mod) | Switches the mod on or off. A mod that is off contributes nothing: its tables, quests, missions, scripts, maps and art are all skipped. Maps take effect at once; tables, quests, missions and scripts the next time a level is loaded; replacement art (`Objects/`, `Biomes/`) after a restart, because art is imported once when the game starts. New mods are on by default. |
| **Upload** button (per mod, your own mods only) | Publishes the mod to the Steam Workshop. See [Steam Workshop](../sharing/workshop.md). |
| **Refresh** | Scans the Workshop items and your `Mods` folder again. Press it after you create a new mod folder, rename one, change a `config.json`, or subscribe to something on the Workshop while the game is running. |
| **Open folder** | Opens your `Mods` folder in the file browser, creating it if it does not exist yet. |
| **Workshop** | Opens the game's Steam Workshop page in the Steam overlay (Steam version only). |

Each mod also has a details view that shows its name, the id the game uses, its load order and the folder it was read from, with a button to open that folder.

Every mod also shows a **Scripting** switch. Turning it on asks you to confirm. The switch is reserved for a coming opt-in and has no effect at the moment, so it is no protection: a mod's scripts run whenever the mod is enabled, whatever the switch says. The only way to keep a mod's scripts from running is to switch the whole mod off. Read [Python mods and safety](security.md) before you enable a mod with scripts from someone you do not know.

## Which mod wins

Mods are applied Workshop items first, then the ones in your `Mods` folder, and inside each group in `LoadOrder` order - lower numbers first, ties broken by id. When two mods provide the same thing - a row in the same table, a quest with the same file name, a mission with the same id - the one applied **last** wins. Two consequences:

- Your own copy of a mod always beats the Workshop copy of the same mod. You can keep working on a mod you have already published and test your changes with the published version still subscribed.
- Two mods from the same place (both Workshop, or both in your `Mods` folder) with the same id are not both loaded. The second one found is skipped with a warning in the log.

The practical rule that follows: **prefix every id you invent with your mod's name**, so you never replace something by accident.

Your own `Missions` and `Maps` folders next to `Mods` - where the in-game Mission Editor and the map editor save - are read after every mod and win over all of them:

- **Missions:** a mission in your own `Missions` folder beats a mission with the same id in any mod. Remember that folder when a mission of yours seems to ignore the copy in your mod.
- **Maps:** a map in your own `Maps` folder beats a mod map with the same file name. See [Maps](../content/maps.md).

## Seeing your changes

Almost everything a mod contains is read when a level is loaded. Return to the main menu and load a save or start a map, and the game picks up whatever you changed in the meantime - tables, quests, missions, scripts and maps alike. Two things are read only once, when the game starts: the *list* of mods, and the replacement art in `Objects/` and `Biomes/`. Opening the Mods window does not scan again; press **Refresh** there when you add a mod folder.

The everyday loop while you work on a mod:

1. Save your game.
2. **Options → Quit to main menu.**
3. Open **Mods** and press **Refresh** if you added or renamed a mod folder or changed its `config.json`.
4. Load the save.

| You changed... | To see it |
|---|---|
| A file inside a mod the game already knows | Load a level (loading a save is enough) |
| A map inside a mod | Also at once, when you toggle the mod's **Enabled** switch |
| A new mod folder, a renamed folder, a changed `config.json`, a subfolder that was empty when the game started | **Refresh** in the Mods window, then load a level - or restart the game |
| A new Workshop subscription while the game is running | **Refresh** in the Mods window once Steam has finished downloading it |
| An airplane skin PNG or the `Airplanes/config.json` | Load a level - skins are read each time a level is loaded |
| A model, texture, thumbnail or biome PNG | Restart the game - art is imported once at startup, and neither **Refresh** nor the **Enabled** switch re-imports it |

!!! note
    For now, any change to the 3D art in `Objects/` and `Biomes/` needs a restart of the game. A future update adds an option to reload mods from the main menu, which will make the restart unnecessary.

[Testing and reloading](testing.md) has more on this loop and on the tools that help while testing.

The game writes what it accepted and what it refused to its log file, `Player.log`:

| Platform | Log file |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

The previous run's log is kept next to it as `Player-prev.log`. The released game logs errors only; the detailed `[Mod ...]` lines described on the category pages appear only in development builds. So when in doubt, check the effect in the game itself. More on this in [Testing and reloading](testing.md) and [When nothing happens](../start/troubleshooting.md).
