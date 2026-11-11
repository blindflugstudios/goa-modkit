---
hide:
  - navigation
  - toc
---

# Ground of Aces Modkit

!!! danger "Developer Preview - use at your own risk"
    This modkit is a **developer preview**. Everything here - the docs, the tools, the rules and
    the modding features of the game itself - is **subject to change** without notice. You use it **at your own risk**: back up your saves before
    you try a mod, and do not rely on anything here staying the way it is.

<div class="hero" markdown>

![Ground of Aces](assets/logos/goa-logo-colored.png)

Build your own missions, quests, events, maps and more for Ground of Aces.
No Unity, no compiler - a mod is a folder of ordinary files: JSON, CSV, Python, models and images. And if you like, an AI agent writes them for you.

</div>

<div class="doors" markdown>

<a class="door" href="basics/first-mod/">
<strong>I have never programmed</strong>
Start here. Your first mod takes five minutes and needs nothing but the game and a text editor. Tools and AI come later, if you want them.
</a>

<a class="door" href="missions/first-mission/">
<strong>I want to dive straight in</strong>
You know your way around files and folders. Copy an example, change it, reload - done.
</a>

<a class="door" href="start/">
<strong>I use an AI agent</strong>
Claude Code, Codex or the open-source OpenCode: clone this repository, start your agent in it, and describe the mod you want. The agent knows the rules.
</a>

</div>

## What you can build

| | What it is | Start with |
|---|---|---|
| **Missions** | Flights the player sends planes on, with four possible endings | [Missions](missions/index.md) |
| **Chains and campaigns** | Missions that unlock each other, historic operations on their real date | [Chains and campaigns](missions/chains.md) |
| **Event scripts** | Python that reacts to what happens on the base and in the air | [Scripting](scripting/index.md) |
| **Quests** | Checklists that guide the player | [Quests](quests/index.md) |
| **Game data** | Aircraft, buildings, raids, costs - change the numbers | [CSV tables](data/csv.md) |
| **Maps** | Your own airfields, with their own quest line | [Maps](content/maps.md) |
| **Objects** | New models, textures and icons for objects, and new ground textures | [Objects and models](content/objects.md) |
| **Airplane skins** | New paint schemes for the game's airplanes | [Airplane skins](content/airplanes.md) |
| **Workshop** | Share your mod with every player | [Steam Workshop](sharing/workshop.md) |

## How it works in one minute

1. Open the game, go to **Main menu → Mods → Open folder**.
2. Put a mod folder there - for example a copy of one of the [examples](examples.md).
3. Back in the game, return to the main menu, open **Mods**, press **Refresh** (so the game notices the new folder) and load your save.

That is the whole loop - see [Testing and reloading](basics/testing.md) for the details. Everything else on this site is about what you put into that folder.

## Join the squadron

- Questions, ideas, showing off: the [Discord modding channel](https://discord.com/channels/1006159027157356587/1551969822911242240)
- Found a mistake on this site? [Open an issue](https://github.com/blindflugstudios/goa-modkit/issues) or improve the page yourself with the pencil icon at the top.
- Finished mod? Put it on the [Steam Workshop](sharing/workshop.md).
