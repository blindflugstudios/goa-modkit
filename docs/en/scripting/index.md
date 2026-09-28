# Scripting

The game runs Python scripts for random events and mission logic, and your mod can add its own. A script can react to things that happen on the base - a day phase changing, a building being finished, a mission coming back - and change the game in return: lift the crew's mood, write an entry to the event log, put a mission on the map.

Scripts run on **IronPython 3.4**, a version of Python 3.4 that runs inside the game. Everyday Python works, including f-strings (the game's own scripts use them). Avoid syntax that came after Python 3.6 - no walrus operator `:=`, no `match`, no positional-only `/` parameters - and packages built for regular Python with compiled parts (numpy and the like) do not work. The standard library that ships with the game is in its `Scripts/Lib` folder; not every module is there, so stick to what the examples use.

| Page | Contents |
|---|---|
| [Events](events.md) | every event a script can subscribe to, with its arguments |
| [API](api.md) | the objects a script uses to talk to the game (`characters_api`, `missions_api`, ...) |
| [Localization](localization.md) | adding and changing text with `localization.SetTerm` |
| [Missions](../missions/index.md) | mission scripts and their handlers |
| [Python mods and safety](../basics/security.md) | what scripts in a mod can do, and what to check before installing one |

## Where scripts live

**Your own scripts belong in a mod**, in its `Missions/` folder:

```text
Mods/
  my_mod/
    Missions/
      morale_boost.py
```

The game's own scripts sit in the installation folder, under `Ground Of Aces_Data/StreamingAssets/Scripts` (on macOS: `Ground of Aces.app/Contents/Resources/Data/StreamingAssets/Scripts`). That is read-only shipped content - read it for ideas, but do not change it, because a game update overwrites it. The shipped folders are:

| Folder | Contents |
|---|---|
| `Default` | the random events (`random_events.py`, `random_health_events.py`) |
| `Mission` | the mission scripts, including the shared `default_mission.py` |
| `Lib` | the Python standard library - not a script folder |

## How scripts are loaded

Scripts are loaded every time a level is loaded, in this order:

1. the game's `Scripts/Default` folder
2. the Supporter Pack's event scripts, if you own it
3. the game's `Scripts/Mission` folder
4. the Supporter Pack's mission scripts
5. the `Missions/` folder of every enabled mod, in mod load order (see [Which mod wins](../basics/mods.md#which-mod-wins))
6. your own `Missions` folder next to `Mods` (on Windows `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Missions\`; the other platforms are on [Missions](../missions/index.md#where-missions-come-from))

Rules worth knowing:

- Only `.py` files directly inside a folder are read - subfolders are ignored.
- Each file becomes a Python module named after the file.
- A file with a **syntax error** is skipped, with the error in the game's log, and the other files still load.
- Any **other error at the top level** of a file (a failing import, an exception while the file runs) is not caught and can stop the folders after it from loading - including other mods' scripts. Wrap risky top-level code in `try`/`except`.

Every handler is identified by `<module>.<function>`, that is the file name plus the function name. If two files define a handler with the same module and function name, the one loaded **later** replaces the earlier one. This is how a mod can override one of the game's random events: copy `random_events.py` into your mod's `Missions/` folder and change the functions you want changed.

### Seeing your changes

Edit your script, return to the main menu and load a level again - loading a save is enough. If the mod folder itself is new, press **Refresh** in the Mods window first (see [How mods work](../basics/mods.md#seeing-your-changes)). More in [Testing and reloading](../basics/testing.md).

## Scripts in a mod

Every `.py` file in a mod's `Missions/` folder is a full event script, not only mission logic: it can subscribe to any event exactly like the game's own `random_events.py`. The scripts of every enabled mod are loaded. A player who does not want a mod's scripts to run disables the mod in the Mods window; the per-mod **Scripting** switch there does not change this at the moment. See [Python mods and safety](../basics/security.md).

## Mission scripts

Mission scripts are a special kind of script that decides how a mission plays out. They are covered on [Missions](../missions/index.md), together with the in-game Mission Editor and the JSON file behind every mission. Mission handlers use the same `event_handler` decorator as the scripts on this page, with the constants from `MissionEvent`:

```python
from Blindflug.FlightMission import MissionEvent

@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return "mymod_coastal_patrol"
```

The full list of mission handlers is on [Reference](../missions/reference.md).

## Your first event script

Let's write a script that runs every time a day phase changes and lifts the whole crew's mood by 10.

To do this, we subscribe to the `DAY_PHASE_CHANGE` event. This is just one of the events you can use - the full list is on [Events](events.md).

Create a mod folder (see [How mods work](../basics/mods.md)), give it a `Missions/` subfolder and create a new file named `morale_boost.py` in it. Paste the following code into it:

```python
# Import MinorEvent to have access to built-in event names
from Blindflug.MinorEvents import MinorEvent
# Import MoraleCategory to have access to morale type constants
from Blindflug.Game.Characters.Morale import MoraleCategory

# Define a localization term that can be displayed in the game.
# This term contains a single placeholder value named "MOOD".
# Since this is outside any function, it runs when the script is loaded.
localization.SetTerm("en", "mymod/morale_up", f"New day phase, [morale:{MoraleCategory.Mood}] improves by {{[MOOD]}}!")

# Use a decorator to mark the function `on_day_phase` as an event handler.
# The function is called when the event happens.
# The arguments are specific to the day phase change event:
# the previous and the current phase.
@event_handler(MinorEvent.DAY_PHASE_CHANGE)
def on_day_phase(previous_phase, current_phase):

    # The amount of mood to add
    mood_boost = 10

    # Change the mood of all characters
    characters_api.ModifyMorale(MoraleCategory.Mood, mood_boost)

    # Create an event log entry, using the localization term defined above.
    # The "MOOD" placeholder is replaced with the value of str(mood_boost).
    event_log.Create("mymod/morale_up", {"MOOD": str(mood_boost)})
```

Now launch the game (or press **Refresh** in the Mods window if the game was already running when you made the folder), load a level and wait until a day phase changes. You should see the message in the event log, and the mood of the whole crew should go up by 10. Congratulations - you have written your first script!

!!! note
    `DAY_PHASE_CHANGE` is not fired for the very first phase of a game, nor while an air-raid alert is running.

!!! note "What is `@event_handler`?"
    `event_handler` is a *decorator*, marked by the `@` sign in front of it. A decorator changes the function written right after it - here, it registers the function so the game calls it when the event happens. You do not need to understand more than that to use it.

!!! tip "Why the doubled braces?"
    In an f-string, `{MoraleCategory.Mood}` is replaced by Python right away, while `{{` and `}}` produce single braces. So the term ends up containing `{[MOOD]}`, which is the placeholder the game fills in later.

### Adding more logic

Everyone at the base likes their work, but they probably enjoy a well-deserved break more. Let's make the effect depend on which day phase has just started.

First, import `DayPhase` to have access to the day phase constants:

```python
from Blindflug.DayPhases import DayPhase
```

Inside the `on_day_phase` function, change the value assigned to `mood_boost`:

```python
    mood_boost = 10 if current_phase == DayPhase.Leisure else 5 if current_phase == DayPhase.Sleep else 0
```

If the day phase is neither leisure nor sleep, we do not want to do anything, so add an early return:

```python
    if mood_boost == 0:
        return False
```

The returned value matters: `False` means this run does not count towards the maximum number of runs (see below). Returning nothing, or `True`, counts it normally.

### Chance and maximum number of runs

Without further settings, the handler runs every time the event happens, as often as it happens. That is great for testing, but for real use some randomness is a good idea. This gives the function a 10 % chance to run when the day phase changes, at most 4 times in one game:

```python
@event_handler(MinorEvent.DAY_PHASE_CHANGE, chance=0.1, max_occurrences=4)
def on_day_phase(previous_phase, current_phase):
    ...
```

Only the decorator line changes; the body of the function (shown here as `...`) stays as it is.

### Adding translations

If you want your script to support several languages, register the term for each of them. Here is the message in Polish:

```python
localization.SetTerm("pl", "mymod/morale_up", f"Nowa faza dnia, [morale:{MoraleCategory.Mood}] wzrasta o {{[MOOD]}}!")
```

Switch the game language between English and Polish, and the message in the event log follows. The language code must be one the game offers in its options (`pl` is).

!!! note
    A language you leave out shows the text of a language you did register, so always register `en`. A key registered in no language at all is shown as the raw key in the event log.

!!! warning
    `SetTerm` on a key the game already ships - a building name, a menu label - **replaces the game's own text** for that language. That is a useful way to retext the game, and an easy way to break it by accident. Prefix your own keys with your mod's name, as in `mymod/morale_up`. More on [Localization](localization.md).

### The finished script

After all the changes above, the script looks like this:

```python
from Blindflug.MinorEvents import MinorEvent
from Blindflug.Game.Characters.Morale import MoraleCategory
from Blindflug.DayPhases import DayPhase

localization.SetTerm("en", "mymod/morale_up", f"New day phase, [morale:{MoraleCategory.Mood}] improves by {{[MOOD]}}!")
localization.SetTerm("pl", "mymod/morale_up", f"Nowa faza dnia, [morale:{MoraleCategory.Mood}] wzrasta o {{[MOOD]}}!")

@event_handler(MinorEvent.DAY_PHASE_CHANGE, chance=0.1, max_occurrences=4)
def on_day_phase(previous_phase, current_phase):

    mood_boost = 10 if current_phase == DayPhase.Leisure else 5 if current_phase == DayPhase.Sleep else 0

    if mood_boost == 0:
        return False

    characters_api.ModifyMorale(MoraleCategory.Mood, mood_boost)

    event_log.Create("mymod/morale_up", {"MOOD": str(mood_boost)})
```

### Next steps

A good way to get a feeling for what is possible is to read the game's own scripts: `random_events.py` and `random_health_events.py` in `Scripts/Default` (the second one shows event log types, icons and the health API), and `default_mission.py` in `Scripts/Mission`. The [Examples](../examples.md) page has complete mods to copy, including an event script.

## Global variables

Every script can use a few ready-made objects, without importing anything, to talk to the game:

| Name | What it is for |
|---|---|
| `logger` | the game's logger; `logger.Log("text")` writes a line to the game's log file |
| `event_log` | create event log entries |
| `localization` | add or change localization terms |
| `resources_api` | spawn a resource pile next to an object, or spoil a pile |
| `characters_api` | read and change crew state: health, morale, carried resources, fire, breaking-point effects |
| `missions_api` | manage missions |
| `airplanes_api` | manage airplanes |
| `game_api` | get general game data |

Every function of these objects is described on [API](api.md).

These names are available everywhere, so they also work inside any helper module your script imports. The game's own types are available to Python as well, so any public enum or type can be imported by its full name, for example:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Tasks import Task
from Blindflug.Game.Characters.Morale import MoraleCategory
```

`eval` is removed and cannot be used.

### Event log entries

`event_log.Create(term, parameters=None, event_log_type=EventLogType.Default)` takes an optional third argument that colours the entry: `from Blindflug.MinorEvents import EventLogType` gives `Default`, `Warning`, `Error` and `Success`. The parameter key `"icon"` is reserved: its value names a picture from the game's generic icon set (for example `"ui_health"`) shown next to the entry. `random_health_events.py` uses both:

```python
from Blindflug.MinorEvents import EventLogType

event_log.Create("random_events/" + id, {"CHARACTER": character, "icon": "ui_health"}, EventLogType.Warning)
```

## Events

The events a script can subscribe to, and the arguments each one passes to your function, are listed on [Events](events.md). Character arguments are character ids (text), resource arguments are `ResourceType` values, and task arguments are `Task` values (`from Blindflug.Tasks import Task`). Some events are fired without arguments; a few exist only for the game's interface and tutorial.

## Event handler functions

Event handlers are normal Python functions, marked with the `event_handler` decorator:

```python
@event_handler(event_name, chance=1.0, max_occurrences=-1)
def handler_function(arg1, arg2):
    pass
```

- `event_name` - the name of the event to handle. This can be any text that matches an existing event, but the easier way is `from Blindflug.MinorEvents import MinorEvent` and the constants defined there, such as `MinorEvent.DAY_PHASE_CHANGE`.
- `chance` - the chance, from `0.0` to `1.0`, that the handler is called when the event happens. `0.5` gives it a 50 % chance. The default is `1.0` (always).
- `max_occurrences` - the maximum number of times the handler can run in one save game. The count is stored in the save, keyed by the handler's `<module>.<function>` name, so renaming the file or the function resets it. A negative value means "no limit" and is the default (`-1`); `0` means the handler never runs. The chance roll and the limit check both happen before the handler is called.

The name of the function can be any valid Python name. Together with the file name, it identifies the handler when the game counts how often it ran.

The function's arguments depend on the event (see [Events](events.md)). The function can return `False` so that this run does not count towards `max_occurrences`. That is useful when a handler should run a limited number of times, but only under certain conditions. Returning nothing, or `True`, counts the run normally.

## String formatting

Text in the event log (and other terms you register) understands a few tags that turn a name into a coloured link or icon:

| Tag | What it shows | Where the names come from |
|---|---|---|
| `[character:<id>]` | a clickable link to the crew member with that id | character ids, as passed to your handler |
| `[resource:<name>]` | the resource's icon and colour | `from Blindflug.GameResources import ResourceType` |
| `[morale:<name>]` | the morale category's icon and colour | `from Blindflug.Game.Characters.Morale import MoraleCategory` |
| `[CharacterStat:<name>]` | a crew skill's icon and colour (`Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating`) | `from BlindGame.CharacterStats.Data import CharacterStatType` |

`CharacterStat` is written with a capital `C` and `S` - this tag is case-sensitive.

The name inside a tag must be the exact name of the enum member; a name the game does not know is left in the text as it is. Writing the enum value into an f-string, as the examples above do, produces exactly that name.

Tags are resolved after the term's placeholders are filled in, so a tag can wrap a placeholder:

```python
localization.SetTerm("en", "mymod/found", "Found some [resource:{[RESOURCE]}]!")
event_log.Create("mymod/found", {"RESOURCE": str(resource)})
```

Here `resource` is a `ResourceType` value your handler received, for example from the `resource_gained` event.
