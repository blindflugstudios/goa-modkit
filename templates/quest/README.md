# Template: quest

A quest is a checklist in the quest panel. It is one `.json` file; its text comes from a small script.

```
quest/
  config.json
  Quests/
    my_mod_first_steps.json     the quest: steps, what they count, when it starts
  Missions/
    my_mod_quest_terms.py       the words for the quest's text keys
```

## Use it

1. Copy the folder to `mods/<your_mod_id>/` and replace `my_mod` everywhere, including the file name.
2. The file name must equal `_questId`.
3. Every `_amount` is at least 1. No spaces inside `_parameter`.
4. Pick step types from `docs/en/quests/index.md`. Types 3 and 15 do nothing.
5. Run `python tools/validator/goa_validate.py mods/<your_mod_id>`.

`_requirements: []` means the quest starts on every map as soon as a game loads. To tie it to one map, see `templates/map-quest-line/`.

Quest files are read every time a level loads: save, quit to the main menu, then load the save again (if the `Quests/` folder is new, open **Mods** and press **Refresh** first). To hand the quest out right away while testing, type `quest my_mod_first_steps` in the cheat console (Options -> Cheats, then the cheat button on the game screen).
