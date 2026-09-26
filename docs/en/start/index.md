# Get started

Welcome to the flight line. This section takes you from "I own Ground of Aces on Steam" to "my own mission shows up in my game". No programming experience needed.

## Pick your door

| You are... | Start here |
|---|---|
| **Never programmed.** You have never opened a terminal and that is fine. | [Install on Windows](install-windows.md) or [Install on Mac](install-mac.md), then [Your first mod in 10 minutes](first-mod.md). Keep the [Glossary](glossary.md) open in a second tab. |
| **Want to dive in.** You know your way around files and a text editor. | [Without an AI agent](without-ai.md): copy an example, edit the JSON, validate, load it. Then [How mods work](../basics/mods.md). |
| **Using an AI agent.** Claude Code, Codex or the open-source OpenCode. | Clone the kit (step 3 of the install pages), start your agent in the folder, and go to [Your first mod in 10 minutes](first-mod.md). |

## Get access first

During the developer preview the modkit is private. Before you install anything, email your
**GitHub username** to [nuria@blindflugstudios.com](mailto:nuria@blindflugstudios.com) or
[moritz@blindflugstudios.com](mailto:moritz@blindflugstudios.com) (no GitHub account yet? The
install pages show how to make one - it is free). You will get an invitation email from GitHub;
accept it, and the download step on the install pages works. GitHub asks you to switch on
**two-factor authentication** before you can accept - the install pages walk you through it. Without the invitation, GitHub
answers "Could not resolve to a Repository".

## What you need

- **Ground of Aces** on Steam, on Windows or Mac.
- **A computer where you can install programs** (admin rights).
- **About 20-30 minutes** for the one-time setup below.
- **A free GitHub account.** GitHub is the website where the modkit lives.

The install pages set up these tools for you, one command at a time:

| Tool | What it does for you | Needed? |
|---|---|---|
| Git | Downloads the modkit and keeps it up to date | Yes |
| GitHub CLI (`gh`) | Logs you in to GitHub from the terminal | Yes |
| Claude Code (or Codex, or OpenCode) | The AI agent that builds your mod | Yes, for the AI route |
| Python | Runs the mod checker (validator) directly | Optional, recommended |

## What it costs

!!! note "Honest up front"
    The modkit, the game's modding and the Steam Workshop are free. **The AI agents are not.**

    - **Claude Code** needs a paid Claude subscription (**Pro or higher**). The free Claude plan does not include it.
    - **Codex** needs a paid ChatGPT plan.
    - **OpenCode** is open source and free to install, but **the AI model behind it is not always free**. Its free models are offered for a limited time, may use your prompts for training and are clearly weaker than Claude or GPT - enough for a first simple mission. For steady use you pay per use. See [OpenCode](../ai/opencode.md).

    Don't want to pay for an AI? Everything also works by hand: see [Without an AI agent](without-ai.md). The in-game **Mission Editor** needs no tools at all.

## The whole journey in 5 steps

1. **Install the tools** once: [Windows](install-windows.md) or [Mac](install-mac.md).
2. **Get the modkit**: `gh repo clone blindflugstudios/goa-modkit`. You do this once. Later, `git pull` fetches updates. Your own mods live in the `mods/` folder and are never touched by updates.
3. **Describe your mod** to the agent in plain English, for example "Make me a mission where two Spitfires escort a damaged bomber home over the Channel."
4. **The agent builds it, checks it and copies it** into the game's `Mods` folder.
5. **Load it in the game**: open the Mods window, load your save, and fly. [Your first mod in 10 minutes](first-mod.md) shows every click.

The 10 minutes count from step 2, once the tools are installed.

Stuck at any point? See [When nothing happens](troubleshooting.md) or ask in the [modding channel on Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).
