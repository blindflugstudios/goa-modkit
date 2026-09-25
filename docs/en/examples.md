# Examples

Complete, working mods to read, copy and change. Each folder in [`examples/`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples) has its own README explaining what to look at.

The fastest way to your own mission: copy `coastal_patrol`, rename the files and the id, and change the numbers and the text.

## The examples, roughly in order of ambition

| Folder | What it is |
|---|---|
| [`coastal_patrol`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/coastal_patrol) | One mission: a JSON file and a small script. Start here. It is the finished result of [Write your first mission](missions/first-mission.md). |
| [`raf_collection`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/raf_collection) | Five standalone missions, each showing a different mechanic. Three carry their text in the JSON and need no script. `night_interception` is the long worked example, with the handler model explained line by line. |
| [`event_script`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/event_script) | Python that reacts to the base and to missions you did not write. No mission of its own. See [Events](scripting/events.md). |
| [`chain_convoy`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/chain_convoy) | A fork: one mission leading to either of two others, depending on how it ended. |
| [`chain_airfield`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/chain_airfield) | A chain four deep, all of it in JSON. |
| [`campaign_kanalkampf`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/campaign_kanalkampf) | A campaign with a memory: conditions JSON cannot express, because they involve counting. |
| [`script_only_scramble`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/script_only_scramble) | A mission with **no JSON at all**, gating and scaling itself from Python. |
| [`quests`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/quests) | Three quest files: a simple starter quest, a follow-up quest, and a quest that belongs to one map. See [Quests](quests/index.md). |

## Chain or campaign?

The two mission sets at the bottom of the list are worth comparing.

| | Chain (`chain_convoy`, `chain_airfield`) | Campaign (`campaign_kanalkampf`) |
|---|---|---|
| Asks | "did mission X succeed?" | "how many times?", "who was aboard?", "what did the player choose?" |
| Built with | JSON requirements (`CompletedMission`) | a script that decides, plus a state file |
| Memory | none: plays the same way every time | remembers across flights, days and sessions |
| Survives save and load | yes, by itself | yes, because the script writes its state to a file |
| Needs Python | no (the scripts in the chain examples only carry text) | yes |

A **chain** asks one yes-or-no question about the mission before, and JSON can do that on its own. A **campaign** asks about the whole run, and that needs a script and somewhere to keep state. [Chains and campaigns](missions/chains.md) explains both.

## Using an example

1. Copy the example folder's files into the `Missions/` folder of a mod: `Mods/my_mod/Missions/`. (The `quests` example is laid out as a whole mod; copy the folder itself into `Mods/`.)
2. Rename the ids. The examples use short ids like `coastal_patrol` because they are documentation. A real mod prefixes every id with its name (`mymod_coastal_patrol`), and changes it everywhere it appears: the file names, `MISSION_ID` in the script, `CompletedMission` values, and `CreateMission` calls.
3. Run the validator over your mod folder (see [Without an AI agent](start/without-ai.md)).
4. Load a save and check the result, see [Testing and reloading](basics/testing.md).

An example id that matches a built-in mission would replace it. None of the examples does, but your renamed copy should not either.

## How far each example has been tested

Every example has been loaded by the game. How far each was taken differs:

| Example | Tested |
|---|---|
| `coastal_patrol` | loaded and created in the game; not yet flown to the end |
| `raf_collection` | all five created in the game; `night_interception` flown to the end |
| `event_script` | handlers confirmed to fire from a mod's `Missions/` folder |
| `chain_convoy` | loaded and created in the game; the branch not yet flown |
| `chain_airfield` | the unlocking confirmed in the game; the flights not yet played through in sequence |
| `campaign_kanalkampf` | flown in the game; the difficulty scaling measured across several raids |
| `script_only_scramble` | not yet tested in the game |

"Loaded" means the game read the files and `create_mission` produced the mission with the written values; "flown" means a squadron took off and the outcome was observed.
