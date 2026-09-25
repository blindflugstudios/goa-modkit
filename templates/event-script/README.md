# Template: event script

A script that reacts to things happening in the game (midnight, a finished building, an aircraft coming home). No mission, no JSON.

```
event-script/
  config.json
  Missions/
    my_mod_reactions.py
```

The script goes in `Missions/` even though it is not a mission: that is the only folder the game loads scripts from. A script in any other folder never runs, and nothing tells you.

## Use it

1. Copy the folder to `mods/<your_mod_id>/` and replace `my_mod` everywhere.
2. Pick events from `docs/en/scripting/events.md`. Arguments arrive in a fixed order - copy the signature from there.
3. Skip events marked tutorial-only: they never fire in a normal game.
4. Run `python tools/validator/goa_validate.py mods/<your_mod_id>`.

`chance` (0.0 to 1.0) and `max_occurrences` (per save game, -1 = no limit) keep a reaction from firing too often. A handler that returns `False` is not counted.
