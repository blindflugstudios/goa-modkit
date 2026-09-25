# Contributing to goa-modkit

Thank you for helping other people build mods. Fixes, new examples, better explanations and
translations are all welcome. Moritz and Jan review every pull request.

## The short version

1. Fork the repository and create a branch.
2. Make your change. Run the checks below.
3. Commit with a sign-off: `git commit -s -m "Explain how biome colors work"`.
4. Open a pull request and fill in the template.

Not comfortable with git? Open an issue instead and describe what is wrong or missing. That
helps just as much.

## Sign-off (DCO)

Every commit needs a `Signed-off-by:` line. `git commit -s` adds it for you. By signing off
you confirm the [Developer Certificate of Origin](https://developercertificate.org/): you wrote
the change, or have the right to submit it, under this repository's licenses.

## AI-assisted contributions

Welcome. Tick the "made with AI" box in the pull request template if an AI agent wrote a
meaningful part of the change. It is information for the reviewer, not a reason to reject.
You are responsible for what you submit: check it, run it, and make sure it is true.

## What goes where

| Change | Where | License |
|---|---|---|
| Documentation | `docs/en/` (English is the source), `docs/de/` | CC BY 4.0 |
| Example mods | `examples/<name>/` with a `README.md` | CC0 |
| Templates | `templates/<type>/` | CC0 |
| Skills and agents | `.agents/skills/<name>/SKILL.md`, `.claude/agents/` | CC BY 4.0 |
| Validator | `tools/validator/` with a test fixture per rule | MIT |
| Generated data | `generated/` - do not edit, it is exported from the game | - |

## Checks before you open a pull request

```bash
python tools/validator/goa_validate.py examples     # 0 errors, 0 warnings
python -m pytest tools/validator/tests              # validator tests
python tools/sync_skills.py                         # after editing a skill
python tools/check_docs.py                          # no em dashes, EN/DE pages in step
python tools/sync_anchors.py                        # after translating: keep English anchors
mkdocs serve                                        # look at the site locally
```

## Writing rules

**Audience.** Write for someone who owns the game and has never programmed. Every page starts
with the simplest path and ends with the reference. Explain a technical word the first time it
appears, or link to the glossary. A full working file beats a description of one.

**Truth.** The game is the truth. Never invent a field, command, path or UI label - if you
cannot check it in the game, leave it out or ask in the Discord. Describe what a modder sees
(folders, files, JSON fields, Python functions, console commands, log lines), not how the game
does it inside.

**Facts that are easy to get wrong:**

- There is no `reload_mods` in the public game. To see a change: save, back to the main menu,
  open **Mods** (it rescans the folder), load the save. Models and textures need a full restart.
- Mod Python runs on IronPython 3.4: f-strings are fine, nothing newer than Python 3.6
  (no `:=`, no `match`).
- Imports from the game's `Blindflug.*` namespaces are the normal scripting API.
- Only missions have tags (`_tags`). Quests have none; a map picks its quest lines with
  `StartingQuestIds`.
- German is the language code `de`.

**Format.** Plain Markdown: headings, lists, tables, fenced code blocks with a language. The
only extras are admonitions (`!!! note`, `!!! warning`, `!!! tip`) and Windows/Mac tabs
(`=== "Windows"`), so the site can move to another tool later. One H1 per page. Relative links
to `.md` files. Never an em dash - use " - ".

**Translations** keep exactly the same headings as the English page (a check enforces it).
Run `python tools/sync_anchors.py` afterwards; it gives every translated heading the English
anchor so links keep working.

## Translations

English (`docs/en/`) is the source. To add a language, copy `docs/en/` to `docs/<code>/`,
translate, add the language to `mkdocs.yml` under the `i18n` plugin, and open a pull request.
A translation does not have to be complete - missing pages fall back to English.

## Questions

Ask in the [Discord modding channel](https://discord.com/channels/1006159027157356587/1551969822911242240).
