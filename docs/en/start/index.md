# Get started with AI modding

Every mod can be written by hand with a text editor - see [Your first mod](../basics/first-mod.md). This section is for when you want help: the **modkit** and an **AI agent** that builds the mod from your description.

## The modkit

The modkit is a download that holds:

- **Examples and templates**: complete, working mods to copy and change.
- **The validator**: a checker that finds the mistakes which would crash the game or hide your mod, before you start the game.
- **Rules and skills for AI agents**: everything Claude Code, Codex or OpenCode needs to build a mod from your description, check it and copy it into the game.

A mod made with the modkit is the same folder of files as one made by hand. The examples and the validator are useful without an AI too: see [Without an AI agent](without-ai.md).

## Get access first { #get-access-first }

During the developer preview the modkit is private. These pages are open to everyone; the download is not. To get it, email your
**GitHub username** to [jan@blindflugstudios.com](mailto:jan@blindflugstudios.com) or
[moritz@blindflugstudios.com](mailto:moritz@blindflugstudios.com) (no GitHub account yet? The
install pages show how to make one - it is free). You will get an invitation email from GitHub;
accept it, and the download step on the install pages works. GitHub asks you to switch on
**two-factor authentication** before you can accept - the install pages walk you through it. Without the invitation, GitHub
answers "Could not resolve to a Repository".

## What you need

- **Ground of Aces** on Steam, on Windows or Mac.
- **A computer where you can install programs** (admin rights).
- **About 20-30 minutes** for the one-time setup.
- **A free GitHub account.** GitHub is the website where the modkit lives.

The install pages set up these tools for you, one command at a time:

| Tool | What it does for you | Needed? |
|---|---|---|
| Git | Downloads the modkit and keeps it up to date | Yes |
| GitHub CLI (`gh`) | Logs you in to GitHub from the terminal | Yes |
| Claude Code (or Codex, or OpenCode) | The AI agent that builds your mod | Yes |
| Python | Runs the mod checker (validator) directly | Optional, recommended |

## What it costs

!!! note "Honest up front"
    The game's modding, the modkit and the Steam Workshop are free. **The AI agents are not.**

    - **Claude Code** needs a paid Claude subscription (**Pro or higher**). The free Claude plan does not include it.
    - **Codex** needs a paid ChatGPT plan.
    - **OpenCode** is open source and free to install, but **the AI model behind it is not always free**. Its free models are offered for a limited time, may use your prompts for training and are clearly weaker than Claude or GPT - enough for a first simple mission. For steady use you pay per use. See [OpenCode](../ai/opencode.md).

    Don't want to pay for an AI? Everything works by hand: see [Your first mod](../basics/first-mod.md).

## The whole journey in 5 steps

1. **Install the tools** once: [Windows](install-windows.md) or [Mac](install-mac.md).
2. **Get the modkit**: `gh repo clone blindflugstudios/goa-modkit`. You do this once. Later, `git pull` fetches updates. Your own mods live in the `mods/` folder and are never touched by updates.
3. **Describe your mod** to the agent in plain English, for example "Make me a mission where two Spitfires escort a damaged bomber home over the Channel."
4. **The agent builds it, checks it and copies it** into the game's `Mods` folder.
5. **Load it in the game**: open the Mods window and press **Refresh**, load your save, and fly. [Your first AI mod in 10 minutes](first-mod.md) shows every click.

The 10 minutes count from step 2, once the tools are installed.

Stuck at any point? See [When nothing happens](troubleshooting.md) or ask in the [modding channel on Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).
