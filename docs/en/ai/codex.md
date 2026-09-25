# Codex

Codex is OpenAI's coding agent. The Codex CLI runs in a terminal inside the folder you start
it in. It reads the same rules as Claude Code.

## Set up

Install Git and the GitHub CLI as described in [Install on Windows](../start/install-windows.md)
or [Install on Mac](../start/install-mac.md), then install the Codex CLI following
[OpenAI's instructions](https://learn.chatgpt.com/docs/codex/cli). On the first start, choose "Sign in with ChatGPT".

```bash
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
codex
```

## What Codex finds in this folder

| File | What it does |
|---|---|
| `AGENTS.md` | Read automatically. The full rulebook: how mods are built, where your game keeps its files, every trap. |
| `.agents/skills/` | One recipe per job (new mission, quest, event script, Workshop upload ...). Codex picks the one that matches your request. |

The requests and tips on the [Claude Code](claude-code.md#good-first-requests) page work the same way in Codex.
