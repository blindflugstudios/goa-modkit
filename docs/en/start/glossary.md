# Glossary

Every technical word used in this handbook, in plain language.

## Computer basics

**Terminal** - A window where you type commands instead of clicking. On Windows it is called Terminal or PowerShell, on Mac it is called Terminal.

**Command** - One line you type into the terminal and confirm with Enter, for example `git pull`. The first word is the program, the rest tells it what to do.

**Prompt** - The text at the start of the terminal line (ending in `>` on Windows or `%` on Mac). It means the terminal is ready for the next command.

**Folder / path** - A folder is a directory on your disk. A path is its address, written as folder names joined by `\` (Windows) or `/` (Mac), for example `~/goa-modkit/mods`. The `~` is short for your personal home folder.

**`cd`** - "Change directory". Moves the terminal into a folder, so the next commands work there. `cd ~/goa-modkit` goes into the modkit.

**PATH** - The list of places where the terminal looks for programs. That is why you sometimes need to reopen the terminal after installing something.

**Package manager** - A program that installs other programs with one command. On Windows this handbook uses **winget**, on Mac **Homebrew** (`brew`).

**Admin rights** - Permission to install programs on a computer. Your own PC or Mac usually has them. A work or school computer may not.

## File types

**JSON** - A plain-text format for data, with `"name": value` pairs in curly braces. Mission numbers (stats, outcomes, timings) are JSON files ending in `.json`.

**Python** - A programming language. Mods use it for texts and for logic that reacts to what happens in the game. Script files end in `.py`. The game runs them with **IronPython 3.4**, an older Python built for .NET, so very new Python syntax does not work.

**CSV** - A table saved as plain text, one row per line, values separated by commas. Mods use CSV files to change game data such as building or plane stats.

**Text editor** - A program for editing plain-text files like JSON and Python. This handbook recommends Visual Studio Code. Word processors like Word are not text editors.

## Git and GitHub

**Git** - A program that downloads a project and keeps track of every change to it.

**GitHub** - The website where the modkit is published. You need a free account to use the GitHub CLI.

**Repository (repo)** - A project folder that Git tracks, with its full history. The modkit is a repository.

**Clone** - Downloading a repository to your computer for the first time: `gh repo clone blindflugstudios/goa-modkit`.

**Pull** - Fetching the latest changes of a repository you already cloned: `git pull`. Your own mods in `mods/` are never touched.

**CLI** - "Command-line interface". A program you use by typing commands in the terminal instead of clicking.

**GitHub CLI (`gh`)** - GitHub's own terminal program. You use it to log in (`gh auth login`) and to clone the modkit.

**Release** - A published, numbered version of a project on GitHub, with ready-made files to download. The ready-made validator comes from the modkit's releases.

## AI agents

**Agent** - An AI program that can read files, write files and run commands on your computer to finish a task you describe. Claude Code, Codex and OpenCode are agents.

**Claude Code** - Anthropic's agent that runs in the terminal. Needs a paid Claude subscription (Pro or higher).

**Codex** - OpenAI's agent that runs in the terminal. Needs a paid ChatGPT plan.

**OpenCode** - An open-source agent that runs in the terminal. Free to install; you choose the AI model, which usually costs money per use. A few free models are offered for a limited time.

**Model** - The AI that does the thinking inside an agent, for example Claude or GPT. Stronger models make fewer mistakes; many cost money per use.

**Prompt (for an agent)** - What you type to the agent: a request in plain English, like "make me a mission where...".

**Skill** - A written set of instructions in the modkit that teaches the agent one job, for example `new-mission`, `validate` or `install-mod`. The agent picks the right skill by itself.

**`AGENTS.md`** - The rulebook for agents in the modkit: folders, pitfalls, and the build, check, copy routine.

## Modding

**Mod** - A folder of files that adds to or changes the game: missions, quests, scripts, maps, objects, airplane skins or data tables.

**`Mods` folder** - Where the game looks for installed mods. Open it from the main menu: **Mods → Open folder**.

**`mods/` folder (in the modkit)** - Where you and your agent build your own mods before they are copied to the game's `Mods` folder. Git ignores it, so updates never change it.

**Content folder** - A folder inside a mod whose name tells the game what is in it: `Missions`, `Quests`, `Maps`, `Objects`, `CSV`, `Biomes`, `Airplanes`. New mission locations go one level deeper, in `Missions/Locations`.

**Id** - The unique name of a thing in the game, for example the mission id `coastal_patrol`. Ids must not contain spaces and must be unique: two missions with the same id replace each other.

**Localization key** - The name of a text, like `missions/coastal_patrol/mission_name`. The game looks up the key to find the text in the player's language. If the text is missing, you see the key itself.

**Validator** - The modkit's checker (`goa_validate`). It reads your mod and reports what would break in the game, without starting the game and without running your scripts.

**Outcome** - One of the four possible results of a mission (as planned or gone wrong, skill passed or failed). Every mission has exactly four.

**Handler** - A function in a mission or event script that the game calls at a certain moment, for example when a mission sends a radio message.

**Mission Editor** - The in-game tool, in the main menu, for creating missions without any files or tools.

**Console / cheat console** - A small window in the game where you type commands such as `create_mission`. Switch it on in **Options → Cheats**. See [Cheat console](../basics/cheats.md).

**Player.log** - The text file where the game writes its errors (development builds also write what it does). The first place to look when a mod misbehaves. See [When nothing happens](troubleshooting.md#find-the-playerlog).

**Steam Workshop** - Steam's page for sharing mods. Players subscribe to a mod there and Steam installs it for them.

**Subscribe** - Clicking **Subscribe** on a Workshop mod. Steam downloads it, and the game loads it next time.
