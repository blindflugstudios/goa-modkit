# goa-validate

Checks that a Ground of Aces mod will load, without starting the game.

```
python3 goa_validate.py path/to/Mods/my_mod
```

Python 3.9 or newer on your computer (the game itself runs mod scripts on IronPython 3.4). No installation, no dependencies - standard library only. No Python? Ask your agent to fetch the prebuilt `goa-validate` program from the goa-modkit releases.

## What it catches

The game does not validate mission data, so three mistakes fail in ways that are
hard to trace back:

- **`_missionOutcomes` must have exactly 4 entries.** Fewer or more throws
  `ArgumentOutOfRangeException` when the mission *completes* - long after you
  stopped suspecting the JSON.
- **`_missionStats` must have at least 2 entries.** Fewer throws
  `IndexOutOfRangeException` on the skill roll.
- **Two missions must not share an id.** One silently replaces the other, and
  which one wins depends on load order - so this may work on your machine and
  break for other players.

Plus the quieter ones: mismatched file names, a `get_mission_id` that disagrees
with its file, missing localisation keys, dead handlers that look like they do
something, Python that will not parse, and JSON that will not load.

## Output

```
$ python3 goa_validate.py Mods/my_mod

coastal_patrol.json:28: error: 3 entries in _missionOutcomes, expected exactly 4
    Order is mandatory - the game picks the ending from two rolls (skill passed? went as planned?):
      [0] gone wrong + skill failed
      ...
coastal_patrol.py:80: warning: implements get_mission_icon, which the game never calls

2 file(s) checked - 1 error(s), 1 warning(s), 0 note(s)
```

Locations are printed as `file:line:`, so most editors and CI log parsers can
jump to them without configuration.

| Flag | Effect |
|---|---|
| `--json` | machine-readable output, versioned by a `schema` field |
| `--strict` | treat warnings as failures too |

Exit codes: `0` clean, `1` findings, `2` the tool itself failed (bad path).
Warnings alone do not fail - a check nobody can get to zero is a check people
stop running.

## What it accepts

Any of these paths work:

- a mod root containing `Missions/`, `Quests/`, `Maps/` or `Objects/`
- one of those content folders directly
- a folder holding a mission's `.json` and `.py` side by side, which is what you
  get by copying an example
- a folder of several mods

## What it cannot tell you

It checks **loadability, not behaviour**. It cannot say whether IronPython will
accept your script at runtime, whether the mission will spawn, whether the
balance is sensible, or whether the writing is any good. A clean run means the
mod is well-formed, not that it works.

## Safety

Mod scripts are parsed with `ast`, never imported or executed. Running the
validator on an untrusted mod does not run that mod's code.

## Tests

```
python3 -m unittest discover tests
```

The suite checks two things: that every defect fixture produces exactly its
expected finding, and - when `GOA_REPO` points at the game repo - that the
game's own 49 missions and 57 quests produce no errors at all. A failure there
means the validator has a bug, not the content.
