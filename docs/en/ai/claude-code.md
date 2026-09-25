# Claude Code

Claude Code is Anthropic's coding agent. It runs in a terminal window, inside the folder you
start it in, and can read, write and run files there.

## Set up

If you followed [Install on Windows](../start/install-windows.md) or
[Install on Mac](../start/install-mac.md), you are ready. Otherwise, in short:

=== "Windows"

    ```powershell
    winget install --id Git.Git -e
    winget install --id GitHub.cli -e
    winget install Anthropic.ClaudeCode
    ```

=== "Mac"

    ```bash
    brew install git gh
    brew install --cask claude-code
    ```

Then get the kit and start Claude in it:

```bash
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
claude
```

The first time, Claude opens your browser so you can log in with your Claude account.

## What Claude finds in this folder

| File | What it does |
|---|---|
| `CLAUDE.md` | Loaded automatically. It pulls in `AGENTS.md`, the full rulebook. |
| `.claude/skills/` | One recipe per job. Claude uses them on its own when your request matches. |
| `.claude/agents/mod-reviewer.md` | A second pair of eyes: checks a finished mod against every rule without changing it. |
| `.claude/agents/translator.md` | Translates your mod's texts, keeping ids and placeholders intact. |

## Good first requests

```text
Make me a mission where two Spitfires escort a damaged bomber home over the Channel.
```

```text
Write an event script: when a pilot comes back from a successful mission, the crew's mood goes up a little.
```

```text
Review my mod in mods/channel_escort and tell me what could go wrong.
```

```text
Translate the texts of mods/channel_escort into German.
```

## Tips

- Start Claude **inside** the `goa-modkit` folder. Started anywhere else, it does not see the rules.
- Say what you see in the game, in your own words. "The mission never shows up" is enough - Claude knows where to look.
- Keep the kit current: ask Claude to "update the kit", or run `git pull` yourself. Your own mods in `mods/` are never touched.
