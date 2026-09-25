---
name: validate
description: Check a Ground of Aces mod for mistakes that crash the game or stop it loading, and explain every finding in plain words. Use when the user says "check my mod", "validate", "is this correct", "why does my mod not work", and at the end of every build skill.
---

# Validate a mod

## 1. Pick the checker

1. Try `python --version`, then `python3 --version`. Python 3.9 or newer: use
   ```bash
   python tools/validator/goa_validate.py mods/<mod_id>
   ```
   (`python3` on Mac/Linux if `python` is missing).
2. No usable Python: use the prebuilt checker in `tools/bin/`. If it is not there yet, download it once (needs the GitHub CLI `gh`, logged in with `gh auth login`):
   - Windows: `gh release download --repo blindflugstudios/goa-modkit --pattern 'goa-validate-windows-x64*' --dir tools/bin`, then run `tools\bin\goa-validate-windows-x64.exe mods\<mod_id>`
   - Mac: check the chip with `uname -m`. `arm64` -> pattern `goa-validate-macos-arm64*`, `x86_64` -> `goa-validate-macos-x64*`. Download with `gh release download --repo blindflugstudios/goa-modkit --pattern '<pattern>' --dir tools/bin`, then `chmod +x tools/bin/goa-validate-macos-*` and run `tools/bin/goa-validate-macos-<arch> mods/<mod_id>`.
   - Linux: pattern `goa-validate-linux-x64*`, then `chmod +x tools/bin/goa-validate-linux-x64` and run it the same way.
   Tell the user in one sentence what you are downloading and why before you do it.

## 2. Run and read

- Output lines look like `file:line: error|warning|note: message`, followed by a hint. The last line counts files, errors, warnings, notes.
- Exit code `0` = no errors (warnings fail only with `--strict`), `1` = errors, `2` = wrong path.
- **Errors** must be fixed: they crash the game or stop the content loading. **Warnings** usually mean something will silently not work; fix them unless clearly intended. **Notes** are information (e.g. a custom location).
- Explain each finding to the user in one plain sentence ("The mission has three endings, but the game needs exactly four - it would crash when the flight comes back").
- Fix, run again, repeat until 0 errors.
- `--strict` treats warnings as failures; use it before publishing.

## 3. What the checker does not see

Go through `AGENTS.md` section 13 by hand every time: forbidden imports and new Python syntax, id prefixes and clashes with `generated/catalog.json`, event names and signatures, CSV tables and columns, quest text keys, leftover placeholder text. Maps and art are not checked at all.

## 4. Report

Say what was checked, what you fixed, and that the mod is "validated, not yet tested in the game". Then continue with `install-mod` if the user wants to try it.
