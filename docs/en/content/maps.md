# Maps

A map is the patch of English countryside your airfield is built on: the shape of the ground, the fields and roads painted on it, the trees and rocks, anything already standing there, plus a few settings such as the start date and the crew you begin with. Every map is one file ending in `.goamap`.

You build maps with the **Map Editor** that comes with the game, and you ship them in a mod's `Maps/` folder. A map can also decide which missions may turn up on it (through tags) and which quest line it starts with.

## Quick start

1. In the main menu, click **Map Editor**, then **New Map**. Shape the ground, paint it, place some trees.
2. Open **Map settings** and fill in at least **Name of Location**. Save the map with **Save as...** and call it `my_airfield`.
3. The editor writes `my_airfield.goamap` into the `Maps` folder inside your game data folder (the folder that also holds `Mods/`, see the table below).
4. Copy that file into a mod with a `config.json`:

    ```text
    Mods/
      my_map_mod/
        config.json
        Maps/
          my_airfield.goamap
    ```

5. Open **Main menu → Mods** and press **Refresh** so the game finds the new mod folder, make sure **my_map_mod** is switched on, then start a new game. Your map is listed under **Custom maps**.

That is a complete map mod. The `config.json` gives the mod its id and name, as every mod needs (see [How mods work](../basics/mods.md#configjson)).

| Platform | Game data folder (holds `Mods/` and `Maps/`) |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/` |

!!! tip
    Give the file a name nobody else will pick, for example with your mod's name in front: `my_map_mod_airfield.goamap`. The file name is the map's id (see [Map ids](#map-ids)).

## The Map Editor

Click **Map Editor** in the main menu. A window lets you start a **New Map** or load an existing one.

The editor has a tool for each part of the map:

| Tool | What you do with it |
|---|---|
| **Terrain Height** | Raise and lower the ground. |
| **Biomes** | Paint the ground type: grass, dirt, road, rock, sand, gravel. The ground type also affects gameplay, see [Biomes](biomes.md). |
| **Grass** | Paint grass on the ground, or remove it. |
| **Terrain Objects** | Place trees, bushes, rocks, ponds and so on, one by one or with a brush. |
| **Map settings** | The name, description, tags, starting quests, start date and starting supplies of the map (see below). |

**Undo** and **Redo** work as you would expect. The editor lists its keyboard shortcuts under **Shortcuts**.

### Saving

**Save** writes over the map you loaded, **Save as...** asks for a new name. Maps are saved into the `Maps` folder in your game data folder.

The shipped maps and maps that come from a mod are write-protected: you can load them in the editor, but you can only store your changes with **Save as...** under a new name. To update a map in your mod, edit the copy in your `Maps` folder and copy it over the one in `Mods/<your mod>/Maps/` again.

### Map settings

Every field in **Map settings** is stored in the map's `Metadata.json` (see [Reference](#metadatajson-reference)):

| Field in the editor | Key in `Metadata.json` | Notes |
|---|---|---|
| **Name of Location:** | `Name` | Shown in the map list. |
| **Description:** | `Description` | Shown when the map is selected. |
| **Tags** | `_tags` | Comma-separated: `default, my_campaign`. Decides which missions may appear, see [Tags and missions](#tags-and-missions). |
| **Starting Quest** | `StartingQuestIds` | Comma-separated quest ids: `quest0, my_first_quest`. See [Starting quests](#starting-quests). |
| **Designation** | `AirplaneDesignation` | The squadron code used in your aircraft designations, for example `DB`. |
| **Coordinates** | `Coordinates` | Latitude and longitude of the airfield. |
| **Starting Date (dd.mm.yyyy)** | `StartDatetime` | Day first, digits and dots only: `15.08.1940`. The time of day is kept. |
| **Amount of Crew Members:** | `InitialCrewCount` | Crew you start with. |
| Resource list | `InitialResources` | Supplies in stock at the start. |

In the comma-separated fields, spaces around the commas are ignored and empty entries are dropped.

## What is inside a `.goamap`

A `.goamap` file is an ordinary zip archive with a different ending. Rename a copy to `.zip` (or open it with any archive tool such as 7-Zip) and you see:

| File | What it holds |
|---|---|
| `Metadata.json` | Name, description, tags, starting quests, dates, starting supplies. The only file you should edit by hand. |
| `Icon.png` | The picture shown for the map. |
| `Heightmap.bytes` | The shape of the ground. |
| `TerrainBiomeTexture.png` | Which ground type is painted where. |
| `TerrainGrassTexture.png` | Where grass grows. |
| `TerrainObjects.json` | Trees, rocks, bushes and other terrain objects. |
| `Props.json`, `Buildings.json`, `Roof.json`, `Workbenches.json`, `TrainingObjects.json`, `FunctionAreas.json` | Everything already built on the map. |
| `Airplanes.json`, `Characters.json` | Aircraft and people placed on the map. |

Leave everything except `Metadata.json` to the Map Editor.

### Editing `Metadata.json` by hand

You can change tags and starting quests without opening the editor:

1. Open the `.goamap` with an archive tool.
2. Extract `Metadata.json`, edit it in a text editor, and put it back into the archive under the same name.
3. Keep the archive's file name and the `.goamap` ending.

Here are the keys you would typically touch, with a tag and a quest line of your own. The real file holds more keys; leave those as they are:

```json
{
  "Name": "Little Snoring",
  "Description": "A grass strip in Norfolk, two fields and a pub.",
  "AirplaneDesignation": "LS",
  "_tags": [
    "my_campaign"
  ],
  "StartingQuestIds": [
    "my_campaign_arrival"
  ]
}
```

!!! warning
    Keep the file valid JSON: no comments, no trailing commas. A map whose `Metadata.json` cannot be read is left out of the map list.

## Tags and missions

Tags are free-form labels that link maps and missions. A map lists the tags it supports in `_tags`, a mission lists the tags it is written for in its own `_tags`, and the mission can only appear on the map when the two lists share at least one tag.

- Tags ignore capitalisation: `My_Campaign` and `my_campaign` match.
- A missing or empty list counts as the single tag `default`, on the map and on the mission alike.
- Every shipped map lists `default` and its own name: `debden`, `duxford`, `lichfield`, `perranporth`. So an untagged mission appears on all of them, and a mission tagged only `duxford` appears only on Duxford.

What that means for your map:

| Your map's `_tags` | Missions that can appear |
|---|---|
| missing or `[]` | Every untagged mission and every mission tagged `default`. |
| `["default", "my_campaign"]` | All of the above, plus missions tagged `my_campaign`. |
| `["my_campaign"]` | Only missions tagged `my_campaign`. The regular missions stay away. |

Tags only affect missions. Quests are not tagged; a map chooses its quests with `StartingQuestIds`. How to tag a mission is explained in [Missions](../missions/index.md).

## Starting quests

`StartingQuestIds` lists the quests the map hands out when it is loaded, whatever those quests' own requirements say. When the list is missing or empty, the map starts the game's default quest line, `quest0`, so no map is ever without quests.

```json
"StartingQuestIds": ["my_campaign_arrival"]
```

As soon as you list your own quest, `quest0` is no longer started on that map, and the shipped main quest line stays away. If you want both, list both:

```json
"StartingQuestIds": ["quest0", "my_campaign_arrival"]
```

An id that no quest file provides is skipped; the map still loads. How to write the quests themselves is covered in [Quests](../quests/index.md).

## Map ids

A map's id is its file name without `.goamap`. `my_airfield.goamap` has the id `my_airfield`, and saves remember the map by that id.

- Only files directly inside `Maps/` are read. Subfolders are ignored.
- Two maps with the same id do not both appear. The one read last replaces the other. Maps are read in this order: the shipped maps, the enabled mods in load order, then your own `Maps` folder next to `Mods`, which wins over every mod. So a mod map named `Debden.goamap` replaces the shipped Debden. Pick a unique name unless that is exactly what you want.
- If a mod map replaces a map, saves made on that map load the mod's version.

## Seeing your changes

| You changed... | To see it |
|---|---|
| A map file inside a mod the game already knows | Switch the mod off and on again in **Main menu → Mods**. Maps are re-read at once. |
| A new mod folder, or a `Maps/` folder that was empty when the game started | Press **Refresh** in the Mods window, or restart the game. |
| A map you saved in the Map Editor | Nothing to do, the map list is re-read when you save. |
| A `.goamap` in your own `Maps` folder that you edited by hand | Restart the game. |

If in doubt, restart the game. More on the test loop in [Testing and reloading](../basics/testing.md).

## Reference

### `Metadata.json` reference

Keys you may edit, by hand or through **Map settings**:

| Key | Type | Default when missing | What it does |
|---|---|---|---|
| `Name` | text | none | Name shown in the map list. Plain text, or a localization key. |
| `Description` | text | none | Description shown when the map is selected. Plain text, or a localization key. |
| `_tags` | list of text | `["default"]` | Tags this map supports. Matched against the `_tags` of missions. |
| `StartingQuestIds` | list of text | `["quest0"]` | Quests handed out when the map loads. An empty list also means `["quest0"]`. |
| `AirplaneDesignation` | text | none | Squadron code for your aircraft designations. |
| `Coordinates` | object `{ "x": latitude, "y": longitude }` | none | Where the airfield is on the globe. |
| `InitialCrewCount` | whole number | `0` | Crew at the start. |
| `StartDatetime` | date and time, `"1940-08-15T07:00:00"` | 15 August 1940, 07:00 | When the game starts. |
| `BaseOpeningDatetime` | date and time | 1 August 1940, 00:00 | Opening date of the base, shown before the game starts. |
| `InitialResources` | object, resource name to amount | none | Supplies at the start, for example `{ "Planks": 50, "Fuel": 15 }`. |

The editor also writes keys such as `CreatedDatetime`, `ModifiedDatetime`, `AirCrewCount`, `AirplanesCount`, `AirstripsCount`, `DeliveryTruckWaypoints`, `ShipmentSpawningLocation` and `DogSpawnPositions`. Leave them as the editor wrote them.

### Sharing a map

Your own maps can be uploaded to the Steam Workshop straight from the map list in the Map Editor. You do not need to build a mod folder for that: the game creates the `config.json` for you when it uploads the map. A map that ships with missions, quests or other content goes up as a whole mod from the Mods window. See [Steam Workshop](../sharing/workshop.md).
