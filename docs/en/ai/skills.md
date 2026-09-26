# Skills and agents

A **skill** is a written recipe for one job. The agent reads only the short description of each
skill until your request matches one, then follows it step by step. Every skill that builds
something ends the same way: run the validator, fix what it reports, copy the mod into the game,
and tell you how to see it in the game.

The skills live in `.agents/skills/` (read by Codex and OpenCode) and are mirrored to
`.claude/skills/` (read by Claude Code). They are identical.

## Skills

| Skill | Say something like | What it does |
|---|---|---|
| `new-mission` | "Make a mission where ..." | Builds a mission (JSON and Python), with all four endings |
| `new-quest` | "Add a quest that asks the player to ..." | Builds a quest with its sub-quests |
| `event-script` | "When X happens on the base, do Y" | Writes a Python event script |
| `csv-tweak` | "Make the Spitfire faster" | Changes game data through a CSV override |
| `localize-mod` | "Add German texts to my mod" | Adds or fixes the texts of a mod in more languages |
| `new-map` | "Ship a map with my own quest line" | Sets up a map folder and its metadata |
| `import-model` | "Use my own model for ..." | Brings a 3D model into a mod |
| `publish-workshop` | "Put my mod on the Workshop" | Checks the mod and walks you through the in-game upload |
| `validate` | "Check my mod" | Runs the validator and explains every finding in plain words |
| `install-mod` | "Put my mod into the game" | Copies the mod into the game's `Mods` folder |
| `read-log` | "Something is wrong, look at the log" | Reads your `Player.log` and explains what failed |
| `update-kit` | "Update the kit" | Pulls the newest rules, docs and skills, and tells you what changed |

## Agents (Claude Code and OpenCode)

In Claude Code, the agent calls these helpers on its own or when you ask. In OpenCode, call them
with `@`, for example `@mod-reviewer review mods/channel_escort`.

| Agent | What it does |
|---|---|
| `mod-reviewer` | Checks a finished mod against every rule and runs the validator. Reports, never edits. |
| `translator` | Translates a mod's player-facing texts and keeps ids, keys and placeholders untouched. |

## Write your own skill

A skill is a folder with a `SKILL.md`:

```markdown
---
name: my-skill
description: One sentence saying exactly when to use this skill.
---

# My skill

Step-by-step instructions for the agent.
```

Put it in `.agents/skills/my-skill/`, run `python tools/sync_skills.py` to mirror it for Claude
Code, and try it. Good skills are welcome as a pull request - see
[CONTRIBUTING.md](https://github.com/blindflugstudios/goa-modkit/blob/main/CONTRIBUTING.md).
