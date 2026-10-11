# Template: map with its own quest line

A map that starts your quests instead of the game's main quest line (`quest0`).

```
map-quest-line/
  config.json
  Maps/
    <your map>.goamap                you make this in the map editor
  Quests/
    my_mod_campaign_start.json       first quest - starts only on maps that list it
    my_mod_campaign_next.json        follows once the first one is complete
  Missions/
    my_mod_campaign_terms.py         words for the quests' text keys
```

## How the pieces connect

1. **The map names its first quest.** A `.goamap` is a zip archive. Inside it, `Metadata.json` has a `StartingQuestIds` list. Put your first quest there:

    ```json
    "StartingQuestIds": ["my_mod_campaign_start"]
    ```

    You can also type the ids into the *Starting quest* field in the map editor's map settings. With the list empty the map starts `quest0`. List both (`["quest0", "my_mod_campaign_start"]`) to keep the main line too.

2. **The first quest only starts where a map lists it.** Leave its `_requirements` empty; no map that leaves it out of `StartingQuestIds` starts it.

3. **Later quests follow the chain.** `{"_requirementType": 1, "_value": "my_mod_campaign_start"}` starts the next quest when the first is complete.

## Missions for this map (optional)

Quests have no tags. Missions do: a mission appears on a map only when the mission's `_tags` and the map's `_tags` share a tag. Both lists empty count as `default`. To keep ordinary missions off your map and add your own:

- in the map's `Metadata.json`: `"_tags": ["my_mod_campaign"]`
- in each of your mission JSONs: `"_tags": ["my_mod_campaign"]`

Add `"default"` to the map's list if the ordinary missions should appear there too.

## Use it

1. Copy the folder to `mods/<your_mod_id>/` and replace `my_mod` everywhere.
2. Save your map in the map editor, copy the `.goamap` into `Maps/`, then delete `PUT_YOUR_MAP_HERE.md`.
3. Run `python tools/validator/goa_validate.py mods/<your_mod_id>` (it checks quests and scripts, not the map file).

Details: `docs/en/content/maps.md` and `docs/en/quests/index.md`.
