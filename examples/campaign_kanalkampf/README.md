# Kanalkampf: a campaign with a memory

`chain_airfield` is a chain: four missions, each unlocked by the last one succeeding. All of it fits in JSON, and none of it remembers anything. Fly the chain twice and it plays identically both times.

This is a campaign: the same raid, flown repeatedly, that is not the same raid twice.

## What the JSON cannot do

A mission's JSON declares four fixed outcomes and flat numbers. It has no way to know:

- how many times this has already happened
- who was in the cockpit last time
- what the player chose two missions ago
- whether the squadron is winning or being ground down

A campaign is made of exactly those things, which is why this one is in Python.

## Installing

Copy all eleven files into `Mods/<your_mod>/Missions/`, including `campaign_state.py`: the four other mission scripts import it.

## The memory

`campaign_state.py` is the whole trick, and it is short. `game_api.GetScriptDataPath(id)` gives the script a folder of its own inside the game data folder; a JSON file in it survives the flight, the day and the session.

```python
import campaign_state

campaign_state.bump("raids_survived")
if campaign_state.get("airfield_found"):
    ...
```

Mod scripts can import one another, so the five missions share one state file and cannot disagree about what has happened.

Details worth copying:

- every key the missions read has a default, so a save made before a key existed picks it up instead of failing with a `KeyError`
- every read and write is wrapped, because a campaign that cannot write its state still has to let the mission fly
- the save's guid is part of the file name, because the folder is shared by every save game

## What the memory is used for

| Remembered | Effect |
|---|---|
| raids flown | from the third on, the enemy has learned: the skill target rises and the chance of a clean intercept falls |
| raids lost | three defeats open a regroup mission instead of the counterattack |
| who won the first one | that pilot is remembered by name for later missions to refer to |
| airfield found / struck | the arc's progress, so a later mission knows which stage it is |

The difficulty scaling is the clearest example, and it was measured in the game:

| Campaign state | Skill target | As-planned chance |
|---|---|---|
| no raids yet | 55–90 | 45% |
| four raids flown | **76–115** | **35%** |

Same mission, same JSON. The script read its own history in `initialize_mission` and raised the bar.

## Branching without requirements

`set_mission_impact` picks the follow-up directly:

```python
if state["raids_lost"] >= DEFEATS_BEFORE_REGROUP:
    missions_api.CreateMission("kanalkampf_regroup")
elif successful:
    missions_api.CreateMission("kanalkampf_pursuit")
```

A JSON requirement can ask one question: did mission X end with outcome Y. This asks a question about the whole campaign, which is the difference between a chain and a story.

`CreateMission` skips the weekly draw, but still checks the target mission's own requirements and map tags. Nothing stops a script handing out the same mission twice, so the script itself has to keep track.

## The arc

| Mission | Handed out by | Condition |
|---|---|---|
| `kanalkampf_raid` | the weekly draw | a runway of tier 1 |
| `kanalkampf_pursuit` | the raid | a raid was won |
| `kanalkampf_regroup` | the raid | **three** raids have been lost |
| `kanalkampf_search` | the pursuit | **two** pursuits have succeeded |
| `kanalkampf_strike` | the search | the airfield was found |

Two of those conditions are counts, and counting is precisely what a JSON requirement cannot do. `_requirementType: 3` asks whether mission X ended with outcome Y. It has no way to ask "three times" or "twice".

`kanalkampf_regroup` is the one worth reading. Three defeats is not a loss condition, it is a different mission: a quiet flight close to home for a squadron that has stopped believing. Winning it gives one defeat back, so the campaign has a way out of the hole rather than being a trap.

## Known limitation

All five missions carry the same single gate (runway tier 1) and are not historic, so the four follow-ups can also turn up through the normal weekly draw, not only when a script hands them out. They cannot simply be tagged away or gated harder in JSON, because `CreateMission` checks the same requirements and tags before it creates a mission. Keep this in mind when you build your own campaign on this pattern.

## Tested

All five missions load and create in the game, and the branching was driven through `set_mission_impact` with the campaign state set by hand:

| Campaign state | Raid ends | What the script handed out |
|---|---|---|
| 3 raids lost | failure | `kanalkampf_regroup` |
| 1 raid won, none lost | success | `kanalkampf_pursuit` |
| first pursuit succeeds | success | nothing yet |
| second pursuit succeeds | success | `kanalkampf_search` |
| search succeeds | success | `kanalkampf_strike` |
| strike succeeds | success | nothing, the arc ends |

The third and fourth rows are the point: the same mission, the same outcome, and a different result because the campaign counted.

`kanalkampf_raid` was also flown for real: a crew was assigned and took off, all three in-flight steps fired, the raid was lost, and the campaign recorded `raids_lost: 1` with the "gone wrong, failed" transmission in the log. The state file was written under the save's own guid.

With the pilot remembered from the first raid aboard, `kanalkampf_pursuit` emitted its veteran line, which names that pilot in the event log.

## Ids

Unprefixed because this is a documentation example. A real mod should prefix them (`mymod_kanalkampf_raid`). `CreateMission` calls the ids by name, so every one of those strings has to be updated together with the file names.
