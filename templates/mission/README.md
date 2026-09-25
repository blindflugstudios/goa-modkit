# Template: mission

A complete mission: one `.json` with the numbers and one `.py` with the text.

```
mission/
  config.json                 mod name and id
  Missions/
    my_mod_patrol.json        stats, location, 4 outcomes, timings, gates
    my_mod_patrol.py          the 9 texts and the radio messages
```

## Use it

1. Copy the whole folder to `mods/<your_mod_id>/`.
2. Replace `my_mod` with your mod id in `config.json`, in both file names and in `MISSION_ID`.
3. The `.json` name, the `.py` name and `MISSION_ID` must be exactly the same.
4. Run the validator: `python tools/validator/goa_validate.py mods/<your_mod_id>`.

## Rules you must keep

- `_missionOutcomes` has exactly 4 entries, in this order: gone wrong + skill failed, gone wrong + skill passed, as planned + skill failed, as planned + skill passed.
- `_missionStats` has at least 2 entries. The first is rolled when the flight goes as planned, the second when it does not.
- `_missionIcon` is one of `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability`, `Stealth`.
- `_enemyPlaneReport` is 18 or lower.

No script at all is also fine: delete the `.py` and put the texts into the `_raw...` fields of the JSON instead. See `docs/en/missions/reference.md`.

The two gates in this template (`RunwayTier` 1, `EarliestAppearanceDay` 3) are low on purpose, so the mission can turn up early. To see it right away while testing, type `create_mission my_mod_patrol` in the cheat console.
