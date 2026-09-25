# RAF Collection

Five missions built from scenario ideas, each written to show a different part of the system. Read them side by side with the mission reference: between them they use every mechanic a mission can reach.

| Mission | Idea | What it shows |
|---|---|---|
| `lost_bombers` | Own bombers limping home from France, fighters on their tail | A short start window as pressure; Fight and Maneuverability as the two rolled skills |
| `greenhorn_watch` | The ace is in hospital; the new intake has to fly | A script that reads *who is aboard* and tells the story accordingly |
| `high_flyer` | A single fast reconnaissance aircraft over the airfield | A deliberately low as-planned chance and a very high skill target: one pass, no second chance |
| `false_alarm` | A faulty radar station scrambles the squadron for nothing | A mission that costs energy on every branch, including success |
| `night_interception` | Finding bombers in the dark, on instruments | The long worked example: reads how tired the crew is, and hands out consequences per pilot |

## Installing

Copy the files you want into `Mods/<your_mod>/Missions/`. A mission's `.json` and `.py` always go together; `lost_bombers`, `high_flyer` and `false_alarm` have no `.py` and need none.

## Two ways to ship text

Three of the five carry their text in the JSON's `_raw*` fields. That covers the nine standard slots (name, description, threat report and the six transmissions) without a script and without a single localization term.

`greenhorn_watch` needs more than nine, because it says something different depending on who is flying. It registers its own terms with `localization.SetTerm` when the script loads. That is the same way the game's own event scripts supply their text, and there is no limit on how many terms a mod adds.

The rule of thumb: `_raw*` for text that is fixed, `SetTerm` for text that varies. Anything beyond the nine standard slots needs `SetTerm`, because the `_raw*` fields cover those nine and nothing else.

## Balance, and where the numbers come from

The skill target is rolled from `_missionStats`, and the squadron has to reach it with the summed skill of the pilots aboard. For orientation: the shipped missions sit around 40–70 for an ordinary patrol. `high_flyer` asks 85–120 on purpose. It is meant to be lost more often than won, and its outcomes reflect that: a failure costs energy and base mood, not aircraft.

`false_alarm` is the one that never really goes well. Every branch drains crew energy; the best outcome merely drains it less and hands back a few victory points for a properly flown sweep. It is a mission about attrition, not about winning.

## Tested

All five were created in the game, drew their locations, and their text resolved: `The Lost Bombers` shows its name and threat report from its `_raw*` fields rather than a raw key.

`night_interception` was flown to the end. It read both pilots' energy, classified the crew as rested and emitted the matching departure line. The as-planned roll failed and it emitted the "gone wrong" transmission to match. After the flight both pilots had lost energy while the pilot who stayed behind had lost none, which is `set_mission_impact` doing per-pilot work the JSON cannot express.

`greenhorn_watch`'s own terms resolve to their text. Its flight, and the crew-experience check itself, have not yet been confirmed in a real flight.

## Ids

The ids here are unprefixed because this is a documentation example. A real mod should prefix them with the mod name (`mymod_lost_bombers`). An id that matches a shipped mission replaces it completely.
