# Example quests

Three complete quest files, laid out as a mod: the `.json` files sit in `examples/quests/Quests/`. Copy this whole `quests` folder into your `Mods` folder (or copy the three files into the `Quests/` folder of your own mod), press **Refresh** in the Mods window and load a level.

| File | What it shows |
|---|---|
| `Quests/example_first_steps.json` | One required step waiting for a finished sickbed (`_type` 7, `building_finished,Sickbed`), one optional step counting four beds (`_type` 4). No requirements, so it starts on every map that lists it in `StartingQuestIds`. |
| `Quests/example_patrol_chain.json` | A follow-up quest. It starts once `example_first_steps` is complete (requirement type 1), waits for a Spitfire to be owned (`_type` 2), then for the shipped mission `calm_supply_drop` to come back a success (`_type` 7, `airplane_on_mission_succeed`), and optionally counts three winning sorties by Spitfires or Hurricanes (`_type` 12). `calm_supply_drop` only appears from day 20 with a tier-3 runway, so that step cannot progress before then. |
| `Quests/example_map_campaign.json` | A quest that belongs to one map: it has no requirements, and only that map lists it in `StartingQuestIds`. Its steps are counted state: a tier-1 airstrip (`_type` 0), two parking spots (`_type` 1), a storage zone of at least 20 tiles (`_type` 9). |

Things to know before you build on them:

- The titles and descriptions are localization keys (`example/first_steps/title` ...). `Missions/example_quest_terms.py` gives them their English and German words with `localization.SetTerm`. Without such a script the quest panel shows no text. The Quests page explains how.
- `example_map_campaign` only starts on a map whose `Metadata.json` lists it in `StartingQuestIds`, or through the console command `quest example_map_campaign`.
- Rename the ids (file name and `_questId`) to your own prefix before you ship anything. `example_` is only a placeholder.

Full documentation: the Quests page of the modkit docs (`docs/en/quests/index.md`).
