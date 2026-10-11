# Missions

A mission is a flight the player sends aircraft on: it appears on the war map, costs time and fuel, and comes back with an outcome. There are two ways to make one:

| | What it is | Best for |
|---|---|---|
| **The Mission Editor** | A window inside the game. Fill in fields, press **Validate**, press **Save**. | A first mission, and anything whose numbers you want to try out quickly. |
| **JSON and Python files** | A `.json` file with the numbers and an optional `.py` file with the text and logic. | Everything else - chains, campaigns, missions that react to what the player did. |

They are the same thing underneath. The editor writes exactly the JSON you would have written by hand, so you can start in the editor and keep going in a text editor.

| Page | Contents |
|---|---|
| [Write your first mission](first-mission.md) | a guided walkthrough from empty folder to a flown mission |
| [Chains and campaigns](chains.md) | missions that follow each other, and campaign maps |
| [Locations](locations.md) | every place a mission can happen, with coordinates |
| [Reference](reference.md) | every JSON field and every handler in detail |
| [How mods work](../basics/mods.md) | where a mod folder lives, and how the game finds it |
| [CSV tables](../data/csv.md) | changing the game's numbers rather than adding missions |

## Where missions come from

The game reads missions from several places, and later ones win when two carry the same id:

1. **Shipped missions** - inside the game (and the Supporter Pack, if you own it), read-only. You can override one by re-using its id, but you cannot edit it in place.
2. **Mods** - `Mods/<your mod>/Missions/`, holding `.json` and `.py` files. This is how you hand a mission to somebody else. See [How mods work](../basics/mods.md).
3. **Your own saved missions** - the folder the in-game Mission Editor writes to:

| Platform | Folder |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Missions\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Missions/` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Missions/` |

That third folder always wins, which makes it a good place to try changes out - and a place to remember to clear when a mission of yours seems to ignore the copy in your mod folder.

## The Mission Editor

Open the game and choose **Mission Editor** in the main menu. That opens the mission list: every shipped mission, every mission from an enabled mod, and every mission you saved yourself. **Create** starts a fresh mission with the id `new_mission` - rename it in the **Mission Id** field before saving. **Edit** opens any mission in the list, shipped ones included. A shipped mission cannot be saved under its own id, so give it a new id and it is saved as your own copy. Your own saved missions carry a delete button, **Refresh** re-reads the list, and the folder button opens your Missions folder in the file browser.

!!! tip "Learn from the game's own missions"
    The shipped missions make good examples, and the Mission Editor lists them all. `calm_supply_drop` is a whole mission in one file, with no script of its own. The four *Blitz* missions (`german_blitz_1_long_nights`, `german_blitz_2_aspirin`, `german_blitz_3_morning_after`, `german_blitz_4_answering_in_kind`) are a historic chain, each one waiting for the one before it to succeed. And `default_mission.py`, the script every mission without its own `.py` runs on, sits in the game's `Scripts/Mission` folder (see [Where scripts live](../scripting/index.md#where-scripts-live)). Open a shipped mission with **Edit** and save it under a new id to get your own copy.

    A copy under a new id shows **no text** at first. A shipped mission keeps its text inside the game, filed under its own id (`missions/<id>/mission_name` and the other text slots), and your copy has a different id. Type the texts in (in the file they are the `_raw...` fields), or register them with `localization.SetTerm` in a script - see [Reference](reference.md). Keeping the shipped id instead replaces the shipped mission, text and all.

<!-- OUTDATED (docs audit 2026-09-28): see DOCS_AUDIT.md
!!! note
    The editor always opens on a single working mission called `new_mission`. It loads yours if you have saved one under that id, and otherwise starts a fresh one. Rename it in the **Mission Id** field before saving, and the next visit starts a new `new_mission`, so you can write one mission after another.

    There is no mission browser yet, so the editor cannot open a shipped mission or reopen one you renamed and saved. To come back to a saved mission, edit its `.json` in the Missions folder above, or start again from a copy.
-->

### What you fill in

**Identity.** The mission id, and the tags that decide which maps the mission can appear on. An id must be lower-case letters, digits and underscores only.

**Tags.** Tags are free-form labels, not map names. A map lists the tags it supports in its `Metadata.json` (the `_tags` field inside the `.goamap` file), a mission lists the tags it is written for (the `_tags` field of the mission JSON), and the mission can only turn up on that map when the two lists share at least one tag. Several tags on a mission mean "any of these" - one match is enough.

Type them into the mission tags field as one comma-separated list without spaces: `naval,atlantic`. A tag follows the same rules as an id - lower-case letters, digits and underscores - and the field enforces that as you type, turning capitals into lower case and dropping anything else. The match against a map ignores capitalisation anyway, so a map that spells its tag `Campaign_Debden` still counts.

Leaving the list empty is the normal case. An empty list on either side counts as the single tag `default`, and every shipped map lists `default`, so an untagged mission is available on all of them. Each shipped map also lists its own name (`debden`, `duxford`, `lichfield`, `perranporth`), so a mission tagged `debden` and nothing else appears only there - see [Maps](../content/maps.md). Tag a mission `campaign_debden` and it appears only on maps that also list `campaign_debden` - and nowhere else, not even on the shipped maps, unless you add `default` alongside it. A map made for a campaign usually lists only its own tag, precisely to keep the regular missions out.

!!! note "Quests have no tags"
    Tags are for missions only. A quest has no tags field. A map picks its quests through the `StartingQuestIds` list in its `Metadata.json`; with none listed it starts the game's default quest line (`quest0`). See [Quests and maps](../quests/index.md#quests-and-maps).

**Validate** warns you when a mission carries a tag that no known map declares. That mission can never appear anywhere, which is only what you want if a script hands it out directly.

**Timing and size.** How many aircraft the player may send, how long the mission waits on the map before it expires, and how long the flight itself takes. Both times are ranges in game minutes - the game rolls a value between the two numbers. A time-to-start maximum of `0` means the mission never expires, and a historic mission (below) never expires, whatever you enter.

**Difficulty.** The chance the mission goes as planned and a difficulty rating from 1 to 3.

**Text.** The mission name and description, the intel threat report with the enemy strength it shows the player (flavour only - it does not affect the outcome), two radio messages during the flight (one for a flight going to plan, one for a flight that has gone wrong), and one closing message for each of the four endings. Type them straight in. A mission written in the editor does not need a script, because every mission without one runs on the game's shared default mission script.

**Locations.** Where on the war map the mission can appear. Pick from the list and add as many as you like; the game chooses one when the mission is created. The full list, with coordinates, is on [Locations](locations.md).

**Requirements.** Conditions that must hold before the mission shows up at all - a runway tier, a date window, or another mission having been completed.

**Stats.** The skills the mission rolls against. You need exactly two: the first is used when the flight goes to plan, the second when it does not.

**Outcomes.** Exactly four endings, and what each one gives or costs - morale, victory points, damage. The editor shows them from top to bottom from the best ending to the worst, not in the order of the slots below. Which ending counts as a success is fixed by its position and cannot be edited: slot 1 (gone wrong, skill check failed) is a failure, slot 2 (gone wrong, skill check passed) a success, slot 3 (as planned, skill check failed) a failure, slot 4 (as planned, skill check passed) a success.

**Is Historic.** Tick this to make the mission part of the storyline. A historic mission is never part of the random weekly draw. The game checks every in-game hour, so it shows up within the hour after its requirements pass. It never waits for the weekly schedule and never takes up one of that week's slots.

- **With a date**, it appears on that day - or later, if its other requirements only pass later.
- **Without a date**, it appears as soon as its requirements pass. A follow-up that waits for another mission's success shows up within the hour after that success.

A historic mission never expires. It is gone for good once it has succeeded. If it fails or is cancelled, it is back on the map at the next hourly check, even while its result report is still waiting to be read.

### Validate before you save

**Validate** lists everything it can find. **Save** runs the same check and refuses if anything is an error.

**Errors block saving:**

| Error | Meaning |
|---|---|
| Mission id empty, or has characters other than `a-z`, `0-9` and `_` | |
| Mission id is reserved | a shipped mission already uses it |
| Mission id is in use | renaming onto another mission you saved would silently replace it |
| A tag has invalid characters | tags follow the same rules as ids |
| Not exactly four outcomes | the game picks one of four and never checks the count |
| Not exactly two stats | the skill roll reads both |
| Time to start: minimum above maximum | |
| Time to complete: minimum above maximum, or under 5 minutes | |
| A runway tier or date requirement that is not a whole number | |
| A completed-mission requirement the game cannot read | |

**Warnings let you save**, and are worth reading anyway:

| Warning | Meaning |
|---|---|
| No locations | the game places the mission at a random location from the shipped list |
| Duplicate location IDs | |
| Unknown map tag | no known map carries this tag, so the mission is unavailable everywhere - intended only if a script hands it out |
| Difficulty rating outside 1–3 | |
| Fewer than one aircraft slot | nobody can fly it |
| Time to start never expires | the mission sits on the map forever |
| Is Historic ticked but the date is empty, impossible or before 1900 | the mission behaves like an undated historic mission - fine if that is what you intended |
| A stat whose minimum is above its maximum | |
| An outcome effect the game cannot read | that one effect silently never applies |
| An outcome uses Max Victory Points | the game works that value out itself and ignores it when you write it |
| Missing narrative text | that text slot shows nothing in game |

The missing-text warning does not appear for shipped missions, which carry translated text rather than text typed into the editor.

### What the editor cannot do

<!-- OUTDATED (docs audit 2026-09-28): see DOCS_AUDIT.md
- Open or copy a shipped mission.
-->
- Write the Python side. Anything that has to *decide* something - react to the crew that flew, hand out a follow-up mission, change the text depending on what happened - needs a script.
- Show a chain as a whole. Each mission only lists its own requirements; how several missions link up is easier to follow in the files. See [Chains and campaigns](chains.md).
<!-- OUTDATED (docs audit 2026-09-28): see DOCS_AUDIT.md
- Build a chain beyond a single "this mission must have been completed" requirement. Longer chains are easier to see and manage in the files. See [Chains and campaigns](chains.md).
-->

For any of those, open the mission file in a text editor, straight from the file browser.

## JSON and Python

A mission is a `.json` file holding the numbers, and optionally a `.py` file of the same name holding the text and any logic. The file name is the mission id. Both go into your mod's `Missions/` folder (or, while you try things out, into your own `Missions` folder above).

```text
Mods/
  my_mod/
    Missions/
      mymod_coastal_patrol.json
      mymod_coastal_patrol.py
```

Three things catch people out, and all three are limits of the game rather than of your files:

- **Exactly four outcomes, in order.** The game picks one by position and never checks how many there are. Three entries crash the mission when it finishes - long after you have stopped suspecting the JSON.
- **At least two mission stats.** The first is used when the mission goes to plan, the second when it does not. One entry crashes the skill roll.
- **Prefix your ids with your mod name.** A duplicate id silently replaces the mission it duplicates, and which one wins depends on load order.

The Mission Editor's **Validate** button catches the first two, and a clash with a shipped id, before you ever launch. A clash with another mod's id, or with the Supporter Pack, it cannot see. Every field of the JSON is described on [Reference](reference.md), and complete, working missions are collected on [Examples](../examples.md).

### The two modes

How much of the script the game uses depends on whether the mission has a `.json` beside it.

- **With JSON** - the numbers come from the file. The script supplies text and reactions only, and the handlers that report numbers are never called.
- **Without JSON** - the script supplies everything, including the numbers. Every handler below is called. What the JSON would otherwise carry - stats, location, slots, tags - is set from `initialize_mission` through `missions_api` (for example `missions_api.SetMissionLocation` and `missions_api.SetTags`).

This is the single most common source of confusion: a handler that works perfectly in a script-only mission is simply ignored once you add a `.json`.

### Mission event handlers

A handler is a Python function the game calls at a certain moment of the mission's life. Each name below links to its full description on [Reference](reference.md). Where the event string differs from the handler name, it is given in brackets.

| Handler | What it does | When it runs |
|---|---|---|
| [`get_mission_id`](reference.md#get_mission_id) | the identifier of the mission | always - **required for a mission without JSON**, inherited from the default script otherwise |
| [`initialize_mission`](reference.md#initialize_mission) | set the mission up as it is created | always |
| [`send_mission_event`](reference.md#send_mission_event) | report progress while the flight is in the air | always |
| [`set_mission_impact`](reference.md#set_mission_impact) | apply consequences once the outcome is known | always |
| [`send_mission_result_event`](reference.md#send_mission_result_event) (`send_mission_result_text`) | react when the mission ends | always, except when cancelled |
| [`send_mission_cancelled_event`](reference.md#send_mission_cancelled_event) (`send_mission_cancelled_text`) | react when the player aborts or the mission expires | always |
| [`get_mission_result_text`](reference.md#get_mission_result_text) | the text in the result window | always |
| [`get_mission_name`](reference.md#get_mission_name) | the name in the mission info window | script-only missions |
| [`get_mission_description_text`](reference.md#get_mission_description_text) | the description in the info window | script-only missions |
| [`get_time_to_start`](reference.md#get_time_to_start) | how long the player has to start it | script-only missions |
| [`get_completion_time`](reference.md#get_completion_time) | how long the flight lasts | script-only missions |
| [`get_threat_level`](reference.md#get_threat_level) | the threat level in the info window | script-only missions |
| [`get_enemy_count`](reference.md#get_enemy_count) | how many enemies are present | script-only missions |
| [`get_mission_events_count`](reference.md#get_mission_events_count) | how many progress reports to send | script-only missions |
| [`get_fuel_level`](reference.md#get_fuel_level) | the fuel the mission needs | script-only missions |
| [`get_mission_result`](reference.md#get_mission_result) | whether the mission succeeded | script-only missions - **required** there |

In a script-only mission, the getters from `get_mission_name` to `get_fuel_level` are optional: leave one out and the game uses a default value instead. For a mission with JSON, the number of progress reports is fixed at 3, so `get_mission_events_count` is ignored there.

!!! warning "Handlers that are never called"
    Do not implement `get_mission_icon`, `calculate_mission_modifiers`, `calculate_airplane_modifiers` or `calculate_pilot_modifiers`. Their names still exist, but nothing calls them - the game works out mission modifiers by itself now. Older example scripts implement them at length; that code never runs.

    `get_mission_fatalities` no longer exists either. Losses are handled through the `Damage` outcome effect.

## Where to go next

- [Write your first mission](first-mission.md) - build and fly one, step by step.
- [Reference](reference.md) - every field, handler and outcome effect.
- [Examples](../examples.md) - complete missions to copy, from a single patrol to a five-part campaign. Start with the coastal patrol.
- [Scripting](../scripting/index.md) - how Python scripts are loaded, and event scripts that are not missions.
