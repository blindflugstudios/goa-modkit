# When nothing happens

Most mod problems come from a handful of causes. Find your symptom, then try the fix. If you use an agent, the fastest fix is often one sentence: `read my Player.log and tell me what went wrong`.

## First, always

1. **Run the validator** on your mod. It catches most of the problems below before the game ever sees them. Ask the agent to `validate my mod`, or see [Without an AI agent](without-ai.md#4-check-it-with-the-validator).
2. **Reload properly**: **Options → Quit to main menu**, then load your save. If you added a new mod folder (or a new content folder such as `Quests/`), open **Mods** and press **Refresh** first. If in doubt, restart the game.

## Symptom, cause, fix

| Symptom | Likely cause | Fix |
|---|---|---|
| **`gh repo clone` says "To get started with GitHub CLI, please run: gh auth login"** | The GitHub login was not finished - usually the terminal was closed or used before it showed `✓ Logged in`. No `goa-modkit` folder was created, so `cd goa-modkit` fails too. | Run `gh auth login` again and follow the browser steps on the install page to the end. `gh auth status` shows whether you are logged in. |
| **`gh repo clone` says "Could not resolve to a Repository"** | You are logged in, but you have no access to the private modkit yet, or you have not accepted the invitation. | Accept it at [github.com/blindflugstudios/goa-modkit/invitations](https://github.com/blindflugstudios/goa-modkit/invitations). No invitation? See [Get access first](index.md#get-access-first). |
| **"Python was not found" although Python is installed (Windows)** | A fake `python` from the Microsoft Store hides the real one. | Use `py` instead of `python`, or switch off the App execution aliases - see [Install on Windows](install-windows.md). |
| **My mod is not in the Mods window** | The mod is not where the game looks, or its content is not in a content folder. The game only sees `Mods/<your mod>/Missions/...` (or `Quests/`, `Maps/`, `CSV/` ...). A `Missions` folder with nothing in it counts as empty. | Open **Mods → Open folder** and check the structure. The mod folder must sit directly in `Mods`, and the files inside a folder named exactly `Missions`. |
| **My mod is listed but switched off** | It was switched off in the Mods window. | Switch it on, then load your save again. |
| **My mod folder is there but ignored** | It is a shortcut, alias or linked folder. The game skips those on purpose. | Copy the real folder into `Mods`. The agent's `install-mod` skill always copies. |
| **The mission never appears** | Its appearance rules are not met yet: `_missionRequirements` such as a minimum day (`EarliestAppearanceDay`) or runway tier (`RunwayTier`), or the mission's `_tags` do not match the map you play. Or the game has simply not drawn it yet. | Test with the console: `create_mission <your_mission_id>` creates it right away. If that says `Unknown mission ID`, the mission did not load: check the [Player.log](#find-the-playerlog). |
| **The game breaks when my mission ends** (error in the [log](#find-the-playerlog), no result) | `_missionOutcomes` does not have **exactly 4** entries. The game only notices when it picks the result. | Give it exactly 4 outcomes in the fixed order. The validator reports this as an error. |
| **The mission breaks when the crew's skill is rolled** | `_missionStats` has fewer than **2** entries. | Add a second stat. The first is rolled when the mission goes as planned, the second when it goes wrong. |
| **My changes to the mission are ignored** | A mission with the same id is saved in the `Missions` folder (next to `Mods`), for example from the in-game Mission Editor. That folder is loaded last and wins over every mod. | Delete or rename that copy in the `Missions` folder, or give your mod mission a different id. |
| **One of two missions is missing, or the wrong one shows** | Two missions share an id. One silently replaces the other, and which one wins can differ between computers. | Give every mission a unique id. The validator reports duplicates. |
| **I changed a function in my script, nothing changed** | When a mission has a JSON file, the JSON supplies the numbers, and some script functions (for example the one for the icon) are never called. | Change the value in the JSON instead. The validator warns about functions the game never calls. |
| **Texts show things like `missions/my_mission/mission_name`, or `null`** | The text for that key was never set: a typo in the key, a missing `localization.SetTerm` line, or the script did not load at all. | Compare the key in the text with the key in `SetTerm`. If all texts are missing, the script failed to load: check the [Player.log](#find-the-playerlog). |
| **The whole script seems to be skipped** | It uses Python syntax newer than the game's Python (IronPython 3.4) understands: the walrus `:=`, a `match` statement, or positional-only `/` parameters. The game skips the entire file. | Rewrite those lines in older syntax. f-strings are fine. The validator reports these as errors. |
| **My new or changed quest does not show up** | Quests are read each time a save loads, but a brand-new `Quests/` folder is only noticed after you press **Refresh** in the Mods window (or restart the game). | **Options → Quit to main menu**, open **Mods** and press **Refresh**, then load your save. |
| **My CSV changes do not apply** | Table changes are merged when a game is loaded. | Quit to main menu and load your save again. |
| **The console says `Unknown cheat`** | A typo, or a command that does not exist in your version. | Type `help` to list all commands. Press **Tab** to complete a command name. |

## Find the Player.log

The game writes its errors into a text file called `Player.log`. (The detailed `[Mod ...]` lines about everything it loads appear only in development builds; the released game logs errors only.) It is rewritten each time the game starts, and the previous run is kept as `Player-prev.log`. Look at it right after the problem, before restarting the game.

| System | Where |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| Mac | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

=== "Windows"

    Press **Windows+R**, paste `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces`, press **Enter**, and open `Player.log` with Notepad or VS Code.

=== "Mac"

    In Finder, press **Cmd+Shift+G**, paste `~/Library/Logs/Blindflug Studios/Ground Of Aces/`, press **Return**, and open `Player.log` with TextEdit or VS Code.

Search it (**Ctrl+F** / **Cmd+F**) for your mod's name, your mission id, `Error` or `Exception`.

## Hand it to the agent

You do not need to read the log yourself. In Claude Code (or Codex), inside the `goa-modkit` folder, type:

```text
read my Player.log and tell me what went wrong with my mod
```

The agent knows where the log lives on your system, finds the lines about your mod and suggests a fix.

## Still stuck?

Ask in the [modding channel on Discord](https://discord.com/channels/1006159027157356587/1551969822911242240). Attach your [`Player.log`](#find-the-playerlog), the validator output, and your mod folder as a zip.
