# Your mods

This folder is yours. Build every mod in its own subfolder here:

```
mods/
  my_first_mod/
    config.json
    Missions/
    Quests/
    ...
```

- **Git ignores everything in here** except this README. Your mods are never uploaded when you work on the kit, and `git pull` (updating the kit) never changes or deletes them.
- Because Git ignores this folder, it is **not backed up** by the kit. Keep your own copy (for example in your own Git repository or a cloud folder) of mods you care about.
- The folder name should be your mod id: 3-64 characters of lower-case letters, digits and `_` (the game also allows `.` and `-`).
- To try a mod, it is **copied** (never linked) into the game's `Mods` folder. Your AI agent does that for you with the `install-mod` skill, or copy it by hand - see `docs/en/basics/mods.md`.

Start from a template in `templates/` or an example in `examples/`: copy it here, never edit the originals.
