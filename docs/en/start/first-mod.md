# Your first AI mod in 10 minutes

You will describe a mission in plain English, let the agent build it, and fly it in your own game. The clock starts now, with the tools already installed ([Windows](install-windows.md) / [Mac](install-mac.md)).

## 1. Open the modkit and start the agent

Open the terminal and type:

=== "Windows"

    ```powershell
    cd ~\goa-modkit
    git pull
    claude
    ```

=== "Mac"

    ```bash
    cd ~/goa-modkit
    git pull
    claude
    ```

`git pull` fetches the newest version of the kit. `claude` starts the agent. Always start it **inside** the `goa-modkit` folder: that is where it finds the rules, examples and skills that teach it how Ground of Aces mods work.

## 2. Describe your mission

Type this into Claude Code and press **Enter**:

```text
Make me a mission where two Spitfires escort a damaged bomber home over the Channel.
```

Change anything you like: the planes, the place, the mood. Plain English is fine. The agent may ask a question or two, for example about difficulty. Answer them the same way.

## 3. Watch the agent work

The agent now does three jobs. It tells you what it is doing and asks before it changes files outside the kit. Answer **Yes** when it asks to create files or run the checker.

| Job | What happens |
|---|---|
| **Build** (skill `new-mission`) | Creates your mod in `mods/`, for example `mods/channel_escort/Missions/channel_escort.json` (numbers: stats, location, outcomes) and `channel_escort.py` (texts and radio messages). |
| **Check** (skill `validate`) | Runs the **validator**, which catches the mistakes that would crash the game or hide your mission. It fixes what it finds and runs the check again until it is clean. |
| **Install** (skill `install-mod`) | Copies the finished mod into the game's `Mods` folder. |

The game's `Mods` folder is here:

=== "Windows"

    ```text
    %USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\
    ```

=== "Mac"

    ```text
    ~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/
    ```

When the agent says the mod is installed, note the **mission id** it tells you (for example `channel_escort`). You need it in a moment.

!!! note "The agent cannot press buttons in your game"
    It builds, checks and copies. Loading the mod in the game is your job, and it takes a minute.

## 4. Load the mod in the game

The game reads mods when a game is loaded. So:

1. Start Ground of Aces. If it is already running with a save open, go to **Options → Quit to main menu** first.
2. In the main menu, open **Mods** and press **Refresh**, so the game notices your new folder. Your mod should be listed and switched on.
3. Every mod also shows a **Scripting** switch. It is reserved for a coming opt-in and has no effect at the moment: the game runs a mod's scripts whenever the mod is enabled, so you can leave the switch as it is. See [Python mods and safety](../basics/security.md).
4. Close the Mods window and load your save (or start a new game).

<!-- screenshot: Mods window with the new mod listed, enabled, scripting switched on -->

Restarting the whole game also works and is the safest option if anything looks off.

## 5. Find your mission

Your mission now joins the pool the game draws missions from, so it turns up on the war map when its conditions are met (for example a certain day or runway). To see it **right now**, use the cheat console:

1. Open **Options** and switch on **Cheats**.
2. A cheat button appears on the game screen. Click it to open the console.
3. Type your mission id and press **Enter**:

```text
create_mission channel_escort
```

**You should see** `Mission created!` in the console. Close the console and open the war map. There it is.

<!-- screenshot: war map with the new mission -->

Assign crews and planes, send them off, and wait for the radio messages you asked for. That is your first mod.

More about the console: [Cheat console](../basics/cheats.md).

## 6. Change something

Go back to the terminal and ask for a change, for example:

```text
Make the mission harder and let the bomber crew radio in when they spot the English coast.
```

The agent edits, checks and copies the mod again. Then in the game: **Options → Quit to main menu**, load your save, and check the mission again. (If the change added a new folder to the mod, for example a first `Quests/`, open **Mods** and press **Refresh** before loading.)

## If something goes wrong

- The mission does not show up, the texts look like `missions/...`, or the game complains: see [When nothing happens](troubleshooting.md).
- Or just tell the agent: `read my Player.log and tell me what went wrong`. It knows where the game writes its [log](troubleshooting.md#find-the-playerlog) on your computer.

## Using Codex or OpenCode instead

Both work the same way. They read the kit's `AGENTS.md`, which holds the same rules the skills follow.

1. Install and log in: [Codex](../ai/codex.md) (needs a paid ChatGPT plan) or [OpenCode](../ai/opencode.md) (open source; pick a model with `/models`).
2. In the terminal: `cd` into `goa-modkit`, then type `codex` or `opencode`.
3. Paste the same prompt. The agent builds, validates and copies the mod. Steps 4 and 5 in the game are the same.

With one of OpenCode's free models, expect a first simple mission to work, but more mistakes on bigger mods - read the result and let `@mod-reviewer` check it. Free models are only offered for a limited time and may use your prompts for training.
