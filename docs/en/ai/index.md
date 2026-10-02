# AI agents

You can build every mod on this site by hand. But you do not have to. This repository is set
up so that an AI coding agent - **Claude Code**, **Codex** or the open-source **OpenCode** - can build mods for you: you
describe the idea in plain words, the agent writes the files, checks them and puts them into
your game.

!!! warning "AI agents cost money"
    Claude Code needs a paid Claude subscription (Pro or higher). Codex needs a ChatGPT plan
    that includes it. **OpenCode** is open source and free to install, but the AI model behind
    it is not always free: its free models are offered for a limited time, may use your prompts
    for training and are clearly weaker - for steady use you pay per use. Details on the
    [OpenCode](opencode.md) page. Everything else here is free. If you do not want to pay for an
    AI at all, build your mod [without an AI agent](../start/without-ai.md) - the in-game
    Mission Editor is a good start.

## Why it works well here

A general AI knows nothing about Ground of Aces. This repository teaches it:

- **`AGENTS.md`** is the rulebook every agent reads first: how a mod is built, where the game
  keeps its files on your computer, and every trap that crashes the game or fails silently.
- **Skills** are step-by-step recipes for one job each - a new mission, a quest, an event
  script, a Workshop upload. The agent picks the right one from what you ask.
- **The validator** checks the agent's work before it reaches your game. The agent runs it on
  its own and fixes what it finds.
- **The docs and examples** on this site sit right next to it in the same folder, so the agent
  reads the real rules instead of guessing.

## The loop

1. You: "Make me a mission where ..."
2. The agent asks what it needs to know, one question at a time.
3. It writes the mod into `mods/<your mod>/` and runs the validator until it is clean.
4. It copies the mod into the game's `Mods` folder.
5. You: in the game, go back to the main menu, open **Mods** once and load your save (see [Testing and reloading](../basics/testing.md)). The [cheat console](../basics/cheats.md) command `create_mission <id>` makes a new mission appear right away.
6. Tell the agent what you see. If something is off, it reads your [`Player.log`](../start/troubleshooting.md#find-the-playerlog) and fixes it.

The agent cannot press buttons in the game for you - step 5 is always yours.

## Pick your agent

| | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Made by | Anthropic | OpenAI | an open-source project ([anomalyco/opencode](https://github.com/anomalyco/opencode)) |
| Costs | Claude Pro or higher | a ChatGPT plan with Codex | the program is free; the model is paid per use, or one of the free models (limited time, may train on your prompts) |
| Model | Claude | GPT | your choice |
| Quality for mods | very good | very good | depends on the model; free models are clearly weaker |
| Reads | `CLAUDE.md` (which loads `AGENTS.md`), `.claude/skills/`, `.claude/agents/` | `AGENTS.md`, `.agents/skills/` | `AGENTS.md`, `.agents/skills/`, `.opencode/agents/` |
| Setup | [Claude Code](claude-code.md) | [Codex](codex.md) | [OpenCode](opencode.md) |

All three use the same rules and the same skills. See [Skills and agents](skills.md) for what is included.
