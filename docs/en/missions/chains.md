# Chains and campaigns

One mission is a sortie. Several missions that follow from each other are a story. This page covers three levels of that, from pure JSON to a campaign with a memory:

1. **Chains:** a mission appears only after another one has ended a certain way. JSON only.
2. **Historic missions:** story beats that are guaranteed to appear, optionally on a real date. JSON only.
3. **Campaigns:** follow-ups that depend on counting, remembering people or player choices. Needs a script.

Working examples: `chain_convoy` (a fork), `chain_airfield` (a straight line four deep) and `campaign_kanalkampf` (a campaign). See [Examples](../examples.md).

## Chaining on an outcome

A requirement of type 3, `CompletedMission`, makes a mission wait for another one:

```json
{ "Name": "CompletedMission", "_requirementType": 3, "_value": "mymod_convoy_spotted,success" }
```

The value is a mission id, optionally followed by a comma and the outcome it must have ended with:

| Value | Meaning |
|---|---|
| `"mymod_convoy_spotted"` | finished, with any outcome (including cancelled) |
| `"mymod_convoy_spotted,success"` | finished successfully |
| `"mymod_convoy_spotted,failure"` | flown and failed |
| `"mymod_convoy_spotted,cancelled"` | called off by the player |

`cancelled` is its own outcome: a mission the player called off does not count as a failure.

"Success" means the outcome the dice picked has `"_missionSuccess": true` in the JSON. It is not the same as the skill roll: outcome index 1 (gone wrong, skill passed) can be a success if you mark it so. That is what makes a salvaged mission feel different from a clean one.

The game remembers every finish for the whole campaign. A player who failed a mission and later won it satisfies both `,failure` and `,success`.

## Branching

Two follow-ups gated on opposite outcomes give you a fork:

```text
mymod_convoy_spotted
   |
   +-- success --> mymod_convoy_strike
   |
   +-- failure --> mymod_convoy_search
```

Nothing stops you from gating several missions on the same outcome, or from chaining more steps onto the follow-ups. Requirements combine with AND, so a mission can require both a finished predecessor and a runway tier:

```json
"_missionRequirements": [
    { "Name": "RunwayTier",       "_requirementType": 0, "_value": "2" },
    { "Name": "CompletedMission", "_requirementType": 3, "_value": "mymod_convoy_spotted,success" }
]
```

There is no OR. To accept either of two predecessors, write two versions of the follow-up mission.

## Historic missions

A normal mission sits in a pool and is drawn at random across the week. For a follow-up that is usually wrong: the player finishes step one and then waits, possibly for weeks, possibly forever if the pool is large.

`"_isHistoric": true` changes that. A historic mission:

- **never enters the random draw.** The moment its gates pass, it is guaranteed to appear.
- **appears on its date** when it has a `_historicDay`: at the first day change on or after that date where its other gates also pass. This does not use the weekly slots.
- **keeps the normal lead time** when it has no `_historicDay`: it takes the next weekly mission slot instead of a random mission, so a follow-up arrives with the same delay as any other mission rather than dropping onto the map instantly.
- **never expires.** `_timeToStartRange` is ignored, so the player has unlimited time to fly it.
- **is one-shot on success.** Once won, it never appears again. A failed or cancelled attempt brings it back, so a chain gated on `success` can be retried.
- **is never on the map twice.** While one copy is waiting or in flight, no second copy appears.

Its gates combine with AND:

| Has a `CompletedMission` gate | Has a `_historicDay` | Appears |
|---|---|---|
| no | no | at the next weekly slot |
| yes | no | at the next weekly slot after the predecessor ended right |
| no | yes | at the first day change on or after the date |
| yes | yes | on the date if the predecessor already ended right; otherwise at the first day change after it does |

That combination is exactly what a story beat needs. Use it for every step of a chain except, usually, the first.

### Controlling when a chain can start

```json
"_isHistoric": true,
"_historicDay": { "Year": 1940, "Month": 8, "Day": 13, "Hour": 0, "Minute": 0 }
```

The date is a floor: the mission is not available before it, and stays available after it until it is won. A year below 1900 counts as "no date", which is why example files carry `"Year": 1` when they mean none.

To close a mission off after a certain point, use a `LatestAppearanceDay` requirement (type 2), counted in days from the start of the campaign. It works on any mission, historic or not.

Put together, each operation becomes available on its real date, and one that was missed can be closed off.

## Pitfalls

**Duplicate ids.** Two missions with the same id means one silently replaces the other, decided by load order. Prefix every id with your mod name, and remember to update the ids inside every `CompletedMission` value when you rename.

**Forgetting `_isHistoric` on follow-ups.** The chain works, but steps may take a very long time to surface, and a finished step can be drawn again.

**Several historic missions due at once.** They all appear together: dated ones on their day, undated ones in the same slot. If you want them one after another, chain them on each other's outcome or give them different days.

**Chaining on a mission that never appears.** A gate on a mission whose own requirements never pass, or which is tagged for a different map, silently blocks the rest of the chain. Test each step on its own before linking them.

**Testing with the cheat.** `create_mission` ignores every gate. It proves a mission loads, not that the chain unlocks. See [Testing and reloading](../basics/testing.md#testing-a-chain).

## When JSON is not enough

A requirement can only ask about a previous mission's outcome. When the condition is something else (who flew it, what the base looks like, how many times this has already happened), a script can create the follow-up itself:

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
```

`CreateMission` puts the mission on the war map at once, skipping the weekly draw. It still checks the target mission's own requirements and map tags: if they do not pass, nothing is created and a warning is written to `Player.log`. Call it from `set_mission_impact`, where the outcome is known; from `initialize_mission` it is refused.

What it does not protect you from: nothing stops a script handing out the same mission twice, and a historic mission created this way is not blocked the way the automatic spawn blocks it.

Use the JSON route wherever it fits. It survives saving and loading, the validator can check it, and it cannot hand out a mission the base cannot fly. Reach for `CreateMission` when the decision genuinely depends on something only a script can see.

## From a chain to a campaign

A chain has no memory. Fly `chain_airfield` twice and it plays identically both times, because every condition in it is a single yes or no about the mission before.

A campaign remembers. `game_api.GetScriptDataPath(id)` gives your script a folder of its own inside the game data folder; a JSON file in it survives the flight, the day and the session.

```python
import json
import os

CAMPAIGN_ID = "mymod_campaign"

DEFAULTS = {
    "raids_survived": 0,
    "raids_lost": 0,
    "first_blood": None,
}


def _path():
    # The folder belongs to the id, NOT to the save game. Without the save's
    # guid in the file name, a second save would continue - and overwrite -
    # the first one's campaign.
    return os.path.join(
        game_api.GetScriptDataPath(CAMPAIGN_ID),
        "campaign_{}.json".format(game_api.GetAirBaseGuid())
    )


def load():
    state = dict(DEFAULTS)

    try:
        with open(_path(), "r") as handle:
            state.update(json.load(handle))
    except (IOError, OSError, ValueError):
        pass          # no file yet, or a half-written one: start clean

    return state


def save(state):
    try:
        with open(_path(), "w") as handle:
            json.dump(state, handle)
    except (IOError, OSError):
        pass          # the mission must still fly
```

The id you pass to `GetScriptDataPath` may contain only letters, digits, `_`, `-` and `.`, up to 64 characters.

Three things are easy to get wrong, and all three bite later rather than at once:

1. **Give every key a default.** A save written before you added a key will otherwise fail with a `KeyError` on load, inside a handler, mid-flight.
2. **Put the save's guid in the file name.** `GetScriptDataPath` gives one folder per id, shared by every save game.
3. **Wrap every read and write.** A campaign that cannot write its state still has to let the mission fly.

Mod scripts can import one another, so put the state in one module (say `mymod_campaign_state.py` in the same `Missions/` folder) that every mission imports. Then they cannot disagree about what has happened.

### What the memory buys you

Conditions no requirement can express:

```python
state = campaign_state.load()

if state["raids_lost"] >= 3:
    missions_api.CreateMission("mymod_regroup")     # counting
elif state["first_blood"] is not None:
    pass                                            # remembering a person
```

It also lets a mission tune itself against the campaign's history, in `initialize_mission`:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    state = campaign_state.load()

    if state["raids_survived"] >= 2:
        # The enemy has seen this squadron before.
        missions_api.SetMissionStat(mission_entity_id, "Fight", 76, 115)
        missions_api.SetAsPlannedChance(mission_entity_id, 35)
```

Same mission, same JSON, measurably harder the fifth time than the first.

The `campaign_kanalkampf` example is the worked version: five missions, two of whose conditions are counts. The [Examples](../examples.md) page compares it with the chains.
