---
name: update-kit
description: Update the goa-modkit (rules, docs, skills, templates, validator) to the newest version with git pull and explain what changed. Use when the user says "update the kit", "get the newest version", "git pull", "is there anything new", "update goa-modkit".
---

# Update the kit

The user's own mods in `mods/` are git-ignored, so an update never touches them. You do not copy, move or re-install anything of the user's.

## 1. Check the state

1. `git status --short`. Anything listed outside `mods/` means the user (or an agent) changed kit files. Tell them which files, in plain words, and ask what to do before pulling: keep the changes aside (`git stash`), or discard them. Never discard without a clear yes.
2. Remember the current version: `git rev-parse --short HEAD`.

## 2. Pull

```bash
git pull --ff-only
```

If it fails because the history diverged, stop and explain; do not force anything. If Git asks for credentials, the user may need `gh auth login`.

## 3. Explain what changed

```bash
git log --oneline <old>..HEAD
git diff --stat <old>..HEAD
```

Summarise for the user in a few plain bullet points, grouped: new or changed rules and skills, new templates or examples, validator changes, new game version (`DOCS_VERSION` and `generated/catalog.json`). Skip internal details.

## 4. Follow-ups

- If the validator or `generated/catalog.json` changed, offer to re-run `validate` on each mod in `mods/`, because new checks may find new problems.
- If a prebuilt validator is in `tools/bin/`, it does not update with `git pull`. Offer to download it again (see the `validate` skill), after deleting the old file.
- Claude Code users: skills are already mirrored in `.claude/skills/`; if `python tools/sync_skills.py --check` fails, run `python tools/sync_skills.py`.
- If `git stash` was used, offer `git stash pop` and help with any conflict.
