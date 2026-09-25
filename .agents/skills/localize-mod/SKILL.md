---
name: localize-mod
description: Add or fix player-facing texts of a Ground of Aces mod in more languages (German, Polish, French...). Use when the user says "translate my mod", "add German texts", "localize", "Übersetzung", "texts show as missions/...", "raw keys instead of text".
---

# Localize a mod

Read `AGENTS.md` sections 7 (text slots), 9 (quest text) and 11. Source: `docs/en/scripting/localization.md`.

## 1. Find every text

In `mods/<mod_id>/`:

- `localization.SetTerm("<lang>", "<key>", "<text>")` calls in any `.py`.
- `_raw...` fields in mission JSONs (one language only - to add languages, move those texts into `SetTerm` calls in the mission's script or a text script).
- Quest keys (`_questTitle`, `_subQuestTitle`, `_subQuestDescription`) and whether each is registered.

List the keys that have **no** English text: those show as raw keys or blanks in the game. Fix those first.

## 2. Ask

One question: which language(s)? Use the short code of a language the game offers in its options, e.g. `en`, `de`, `pl`. Always keep `en` - a missing language falls back to a registered one.

## 3. Translate

For more than a handful of texts, and in Claude Code, hand the work to the `translator` subagent with the mod path and target language. Otherwise do it yourself with the same rules:

- Add one `SetTerm` per key and language, next to the English one. Never change a key.
- Keep placeholders `{[NAME]}`, tags like `[character:...]`, `[resource:...]`, `[morale:...]`, `[CharacterStat:...]` and `{}`/`%s` format markers exactly as they are.
- Mission text stays terse 1940s radio style in every language.
- Never register a key that belongs to the game (anything not prefixed with the mod id or `missions/<mod mission id>/`): that replaces the game's own text.

## 4. Validate

`python tools/validator/goa_validate.py mods/<mod_id>` until 0 errors, plus the Python checks in `AGENTS.md` section 13.

## 5. Install and hand over

Follow `install-mod`. Tell the user to switch the game language in the options, then save, quit to the main menu, open Mods and load the save again, and check the texts. Ask what they see.
