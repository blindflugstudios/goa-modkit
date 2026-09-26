# OpenCode

OpenCode is an **open-source** coding agent that runs in your terminal, like Claude Code and
Codex. It reads the same rules and skills from this modkit. The difference: OpenCode is not tied
to one AI company. You choose the **AI model** it uses - including a few that currently cost
nothing.

!!! warning "Open source does not mean free of charge"
    **OpenCode is open source and free to install - the AI model behind it is not always free.**
    OpenCode Zen offers a few free models for a limited time: your prompts may be used to train
    them, and they can disappear without notice. For steady use you pay per use, through Zen
    credits or your own Claude or OpenAI key. Free models are also noticeably weaker than Claude
    or GPT: fine for a first simple mission, expect more fixing on bigger mods.

## What it costs

OpenCode itself is free software ([MIT license](https://github.com/anomalyco/opencode)). What
you pay for - or not - is the model that does the thinking. There are four ways:

| Model | Cost | Your data | Quality for mods |
|---|---|---|---|
| **Free models in OpenCode Zen** (names end in `free`, or `big-pickle`) | Nothing, for now. Offered "for a limited time"; the list changes without notice. At the time of writing they work without an account. | Most of them: the provider **may use your prompts and answers to train its model**. | Enough for a first simple mission (tested). Weaker on campaigns, event scripts and bug hunting. |
| **Paid models in OpenCode Zen** | Pay as you go: account with a credit card, **$20 starting balance** (plus a card fee), automatic top-up of $20 when you drop below $5 (can be switched off), monthly limit adjustable. | Depends on the model; see each model's note in the Zen documentation (for Claude and OpenAI models, requests are kept for 30 days). | As good as the model you pick - the top models match Claude Code or Codex. |
| **Your own Claude or OpenAI key** | Pay per use with that company (an API key is billed separately from a Claude or ChatGPT subscription). | That company's API terms. | Same models as Claude Code or Codex. |
| **Local models** (Ollama, LM Studio) | Nothing to pay, but needs a strong computer (a lot of memory, ideally a good graphics card). | Stays on your computer. | Clearly weaker. For people who like to tinker. |

Prices and the list of free models are from OpenCode's
[Zen documentation](https://opencode.ai/docs/zen/) (checked September 2026). Check there before
you add credits - it changes often.

!!! tip "Our recommendation for getting started"
    Start with a **free Zen model** to see how it works. If you stay with modding, add a small
    Zen balance with a monthly limit, or use Claude Code or Codex. Never put anything into a
    prompt you would not want a model provider to read.

## Quality

We tested OpenCode with the free model `big-pickle` on this modkit: asked for "a mission where
two Spitfires escort a damaged bomber home over the Channel", it read the rules and examples,
built the mission, ran the validator on its own until it was clean, and finished in about three
minutes.

That is the easy case. What to expect beyond it:

- **Simple missions and quests:** usually fine.
- **Chains, campaigns, event scripts:** more mistakes, more rounds of "that did not work, try
  again". Break big ideas into small steps.
- **The validator catches crashes, not bad ideas.** It stops missing outcomes, wrong ids or
  forbidden imports. It does not notice dull radio messages, a mission that is far too easy or
  logic that does not fit the game. Read what the agent wrote.
- **Get a second opinion:** type `@mod-reviewer review mods/<your mod>` before you publish.
- **Stuck?** Switch to a stronger model (`/models`) for that one task.

## Install

!!! note "Windows: not yet tested by us"
    OpenCode's own documentation recommends WSL (a Linux environment inside Windows). We install
    it natively with winget instead, because WSL is a big extra step for beginners. We have not
    finished testing this on Windows yet - if something fails, tell us in the
    [Discord modding channel](https://discord.com/channels/1006159027157356587/1551969822911242240).

Install Git and the GitHub CLI first, as described in [Install on Windows](../start/install-windows.md)
or [Install on Mac](../start/install-mac.md). You can skip the Claude Code step. Then:

=== "Windows"

    ```powershell
    winget install --id SST.opencode -e
    ```

=== "Mac"

    ```bash
    brew install anomalyco/tap/opencode
    ```

Close the terminal, open a new one, and check:

```bash
opencode --version
```

**You should see** a version number, for example `1.18.32`.

## Start it and pick a model

```bash
cd goa-modkit
opencode
```

OpenCode opens in the terminal. To choose a model, type `/models` and press **Enter**, then pick
one from **OpenCode Zen** whose name ends in `free` (or `big-pickle`). Which free models exist
changes from month to month - take whichever is listed.

To use paid Zen models or your own key, type `/connect`, choose the provider and follow the
steps. For Zen you create an API key at [opencode.ai/auth](https://opencode.ai/auth).

## What OpenCode finds in this folder

| File | What it does |
|---|---|
| `AGENTS.md` | Read automatically. The full rulebook: how mods are built, where your game keeps its files, every trap. |
| `.agents/skills/` | One recipe per job (new mission, quest, event script, Workshop upload ...). OpenCode picks the one that matches your request. |
| `.opencode/agents/mod-reviewer.md` | A second pair of eyes: `@mod-reviewer` checks a finished mod without changing it. |
| `.opencode/agents/translator.md` | `@translator` translates your mod's texts and keeps ids and placeholders intact. |

OpenCode may print a warning like `duplicate skill name` when it starts. That is harmless: the
same skills are also stored for Claude Code in `.claude/skills/`, and OpenCode uses one copy.

## Good first requests

The requests on the [Claude Code](claude-code.md#good-first-requests) page work the same way in
OpenCode. With a free model, keep them small and specific:

```text
Make me a mission where two Spitfires escort a damaged bomber home over the Channel.
```

```text
@mod-reviewer review mods/channel_escort
```
