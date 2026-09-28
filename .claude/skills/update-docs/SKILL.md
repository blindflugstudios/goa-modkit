---
name: update-docs
description: For kit maintainers only. Sync the modkit handbook (docs/en, docs/de, AGENTS.md, skills, templates) with the game team's Docs/ folder, which is always the up-to-date reference - list every difference in DOCS_AUDIT.md, then fix, add or hide handbook content so it matches Docs/. Use when the user says "update the docs", "sync the docs with the game", "compare with the game docs", "/update-docs". Not for players building mods.
---

# Update the handbook from the game docs

The game team's `Docs/` folder (in the `SquadronLeader_Demo` repo, branch `develop`) is the **source of truth and always the most up-to-date reference**. The goal is to bring the handbook in this repo in line with it. Whenever the handbook and `Docs/` disagree, `Docs/` wins, even if the handbook text is newer, longer or sounds more certain. This skill changes kit files, so it is for people working on the kit itself (see `AGENTS.md` section 2), not for players.

Tell the user once what will happen: you read the game docs, list every difference in `DOCS_AUDIT.md`, and after their go-ahead sync the handbook to it in English and German. Nothing is committed or pushed.

## 1. Ask where the game docs are

Ask exactly one question:

> Where should I read the game docs from? Paste either the GitHub link to the `Docs/` folder on the develop branch (for example `https://github.com/blindflugstudios/SquadronLeader_Demo/tree/develop/Docs`) or the path of a `Docs` folder on your computer (for example `D:\Projects\BlindflugStudios\SquadronLeader_Demo\Docs`).

Do not guess a source and do not go on without an answer.

## 2. Get the docs

The repo is **private**. Never use web fetch or an anonymous download for it; they fail (GitHub answers 404). Only git with the user's own credentials works.

**If the answer is a GitHub link** (`https://github.com/<owner>/<repo>/tree/<branch>/<path>`):

1. Split it into repo URL `https://github.com/<owner>/<repo>`, branch and folder path. If the branch is not `develop`, say so and ask whether that is intended.
2. Check access: `git ls-remote --heads https://github.com/<owner>/<repo> <branch>`. If it fails, explain in one sentence that the repo is private and their git login has no access to it. Offer two ways out: sign in (`gh auth login`, or the Git Credential Manager prompt) or give a local path instead. Stop here until they choose.
3. Fetch only the docs folder into the scratchpad or a temporary folder outside this repo, never into the repo:

    ```bash
    git clone --depth 1 --filter=blob:none --sparse --branch <branch> https://github.com/<owner>/<repo> <tmp>/game-docs
    git -C <tmp>/game-docs sparse-checkout set <path>
    ```

4. Note the commit: `git -C <tmp>/game-docs log -1 --format="%h %ad %s" --date=short`.

**If the answer is a local path:**

1. Check the folder exists and looks like the game docs (`mainpage.md`, `scripting.md`, a `Modding/` folder). If not, say what you found and ask again.
2. If it is inside a git checkout, report the branch and commit (`git -C <path> log -1 --format="%h %ad %s" --date=short -- .`). Check whether it is behind: `git -C <path> fetch origin develop` then `git -C <path> rev-list --count HEAD..origin/develop -- .`. If it is behind, tell the user and ask whether to compare with `origin/develop` instead. Read those files with `git -C <path> show origin/develop:<file>` rather than pulling their checkout. Never pull, switch branches or change anything in their checkout.

Also look at what changed recently: `git log -10 --format="%h %ad %s" --date=short -- <Docs path>`. Commit messages such as "trim", "remove" or "rename" point to handbook text that is now outdated.

## 3. Which pages to compare

| Game docs (`Docs/`) | Handbook (`docs/en/`, then the same page in `docs/de/`) |
|---|---|
| `mainpage.md`, `Modding/mods.md` | `index.md`, `basics/*.md`, `start/*.md`, `sharing/workshop.md`, `content/*.md`; `AGENTS.md` sections 5, 6, 14, 15 |
| `Modding/missions.md`, `Modding/locations.md`, `Modding/missions/*.md` | `missions/*.md`; `AGENTS.md` section 7 |
| `Modding/quests.md`, `Modding/examples/quests/*.json` | `quests/index.md`, `examples.md`, `templates/quest/`, `templates/map-quest-line/`, `examples/quests/`; `AGENTS.md` section 9 |
| `scripting.md` | `scripting/*.md`, `basics/security.md`; `AGENTS.md` sections 8, 11 |
| `Modding/csv-data.md` | `data/csv.md`, `data/table-editor.md`, `docs/assets/csv/*.csv`; `AGENTS.md` section 10 |

Also grep the skills in `.agents/skills/`, `CONTRIBUTING.md` and the `templates/*/README.md` files for anything a finding touches. If the game docs gained a new page, say so and ask whether it needs a handbook page.

When your agent can run subagents, give each row of the table to its own read-only subagent and collect their reports. Otherwise work through the rows one by one.

## 4. Sort every difference

For each difference, note the handbook file, the line and the exact quote, plus what the game docs say (file, line, quote). Then give it exactly one verdict:

- **Wrong**: the handbook contradicts the game docs. Plan to reword it.
- **Outdated**: it describes something the game docs say is gone or has changed. Plan to hide it, or reword it if a short correct sentence exists.
- **Missing**: the game docs have a rule, value, field, event, warning or section the handbook lacks. Plan to add it to the matching handbook page.
- **Less detailed**: the handbook is correct but vaguer, for example sample values where the game docs now list full ranges. Plan to update it to the game docs' detail.
- **Open**: the game docs contradict themselves, so there is no single reference answer. Plan to leave it and have the game team decide. If the game docs are clear but you suspect the game code differs, follow the game docs anyway and add a note in the audit.
- **Unverifiable**: the game docs say nothing about it. Plan to leave it and list it briefly. The fact that the game docs are silent does not make handbook text wrong.

Check every finding against the game docs yourself before you act on it. Subagent reports can be wrong.

## 5. Write it down

Write `DOCS_AUDIT.md` in the repo root (outside `docs/`, so it is not published). If it already exists, replace it with the new state. Include:

- the date, the source and its commit
- one section per row of the table above
- a table per section: Where | Handbook says | Game docs say | Action
- the Open list and the unverifiable list at the end

Show the user a short summary (counts per verdict, plus the Open items in one line each). Then ask one question: shall I apply the fixes now?

## 6. Apply the fixes (after a yes)

- **Every change goes into `docs/en/` and `docs/de/`.** Write the German naturally, in the du-form the German pages already use. Keep ids, keys, anchors and code identical.
- **Wrong** and **Less detailed**: rewrite to match the game docs, in the page's own tone. The handbook is written for players who have never programmed, so explain rather than copy developer wording.
- **Missing**: add the content where a reader of that page would look for it, in the page's style (the same tables, admonitions and examples). Keep the handbook's structure; do not paste whole game-docs pages. A brand-new game-docs topic gets a new page only after the user agrees; then add it to `nav` in `mkdocs.yml` with its German translation.
- **Outdated passage**: hide it, do not delete it:

    ```markdown
    <!-- OUTDATED (docs audit YYYY-MM-DD): see DOCS_AUDIT.md
    ...original text, unchanged...
    -->
    ```

    No `-->` may appear inside the hidden text. Hide any heading that is left with nothing visible under it.
- **Outdated page**: add it to `exclude_docs` in `mkdocs.yml`, remove its `nav` entry and its German nav translation, and point every link to it at a page that still exists.
- **Open** and unverifiable findings: do not change them.
- **Art mods** (`Objects/`, `Biomes/`, models, textures) stay marked as work in progress for as long as the game docs or the user say the current alpha does not support them. Every page and skill about them keeps the warning under its heading:

    ```markdown
    !!! warning "Work in progress"
        Art mods are work in progress. The current alpha does not support them yet, ...
    ```

    Remove the warning only when the user confirms that art mods now work.
- **Files other than pages**:
    - `AGENTS.md`, `.agents/skills/` and `templates/` are fixed by the same rules.
    - Edit skills only in `.agents/skills/`, then run `python tools/sync_skills.py`.
    - When the game docs link a built-in file the handbook lacks (for example a CSV in `docs/assets/csv/`), copy it from the game repo byte for byte.
    - Before copying any file, look inside it for URLs, keys or endpoints and tell the user. The site is public.
- **Never copy the game docs themselves into this repo.** They come from a private repository.

## 7. Check

Run all of these and fix what they report:

```bash
python tools/sync_skills.py --check
python tools/check_docs.py
python tools/sync_anchors.py --check
mkdocs build --strict -d <tmp>/site
```

If `mkdocs` is missing, ask before installing: `pip install -r requirements-docs.txt`, ideally into a virtual environment outside the repo. Open one hidden page in the built site and make sure the hidden text does not show.

## 8. Hand over

- Tell the user in a few bullets what was fixed, added, updated and hidden, and what is still Open, with the audit file as the full list.
- Say plainly that nothing is committed. A push to `main` republishes the public site (`.github/workflows/docs.yml`). Offer to commit, or to put the changes on a branch for a pull request.
- Delete the temporary clone if you made one.
