@AGENTS.md

# Claude Code notes

Everything in `AGENTS.md` applies. On top of that:

- **Skills** live in `.claude/skills/` (a mirror of `.agents/skills/`). Use the matching skill for every mod task: `new-mission`, `new-quest`, `event-script`, `csv-tweak`, `localize-mod`, `new-map`, `import-model`, `publish-workshop`, `validate`, `install-mod`, `read-log`, `update-kit`. Kit maintainers use `update-docs` to sync the handbook with the game team's `Docs/` folder.
- **Subagents** live in `.claude/agents/`:
  - `mod-reviewer` - before telling the user a mod is ready (and always before `publish-workshop`), have it review `mods/<mod_id>/`. It reports, it does not edit. Fix what it finds yourself.
  - `translator` - when the user wants their mod's texts in another language (English and German first). It keeps ids, keys and placeholders intact.
- Editing skills: change `.agents/skills/`, then run `python tools/sync_skills.py`. Never edit `.claude/skills/` by hand; `python tools/sync_skills.py --check` fails when the two differ.
- Ask before running commands that write outside this repo (installing into the game's `Mods` folder counts). Once the user has confirmed the `Mods` path, it is stored in `.goa-modkit.local.json`.
