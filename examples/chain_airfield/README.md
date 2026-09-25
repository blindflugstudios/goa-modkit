# The Airfield Chain

Four missions in sequence, each one unlocked by the previous one succeeding. Where `chain_convoy` branches (one mission leading to either of two others), this one is a straight line four deep.

| # | Mission | You are | Rolled skills |
|---|---|---|---|
| 1 | `airfield_raid` | defending: bombers over your own field, scramble everything | Fight / Maneuverability |
| 2 | `airfield_pursuit` | reacting: follow them home and see where they land | Fight / Maneuverability |
| 3 | `airfield_search` | hunting: photograph the strip they came from | Recon / Stealthiness |
| 4 | `airfield_strike` | attacking: destroy it | Bomb / Fight |

The arc is deliberate. Stage 1 gives the player no choice at all: the mission comes to them, with a ten-minute window to get airborne. By stage 4 they are choosing the hour and bringing four aircraft. The stakes rise with the player's freedom: `airfield_raid` pays 7 victory points at best, `airfield_strike` pays 15 and moves base mood and confidence with it.

## How the chaining works

Entirely in the JSON. Each mission after the first carries one requirement:

```json
"_missionRequirements": [
    { "Name": "CompletedMission", "_requirementType": 3, "_value": "airfield_raid,success" }
]
```

Type 3 is `CompletedMission`; the value is `<mission_id>,<outcome>` where outcome is `success`, `failure` or `cancelled`. The scripts here do not touch the chain at all: they carry the text and the rolls, nothing else.

The follow-ups here are ordinary missions, not historic ones, so once unlocked they join the random draw and may take a while to turn up. Add `"_isHistoric": true` to them if each stage should arrive at the next mission slot; `chain_convoy` shows that.

`chain_convoy` also shows the other shape: two missions requiring the *same* predecessor with opposite outcomes, so the story forks instead of continuing.

## Text

Each mission keeps its text in its own script rather than in the JSON's `_raw*` fields. Both work. The reason to use scripts here is that the four share a voice (one squadron over four days), and having the lines in Python keeps them together and lets a later version vary them by what happened in flight. A mission whose text is fixed is simpler with `_raw*`; see `raf_collection`.

## Tested

The unlocking was checked in the game against different mission histories:

| Mission history | raid | pursuit | search | strike |
|---|---|---|---|---|
| nothing finished | available | locked | locked | locked |
| raid succeeded | available | **available** | locked | locked |
| pursuit *failed* | available | available | **still locked** | locked |
| pursuit and search succeeded | available | available | available | **available** |

The third row is the one worth having: finishing a mission is not enough, it has to be finished *successfully*, which makes a failed stage a dead end rather than a detour.

Not yet played through in sequence: the unlocking is confirmed, the flights themselves and their outcomes are not.

## Ids

Unprefixed because this is a documentation example. A real mod should prefix them (`mymod_airfield_raid`) and update the `_value` in each requirement to match, or the chain points at ids that do not exist.
