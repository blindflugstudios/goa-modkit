---
hide:
  - navigation
  - toc
---

# Ground of Aces Modkit

!!! danger "Developer Preview - use at your own risk"
    This modkit is a **developer preview**. Everything here - the docs, the tools, the rules and
    the modding features of the game itself - is **subject to change** without notice. Anyone can read
    this site, but the kit itself is currently **by invitation only** - see "Get access" below. You use it **at your own risk**: back up your saves before
    you try a mod, and do not rely on anything here staying the way it is.

<div class="hero" markdown>

![Ground of Aces](assets/logos/goa-logo-colored.png)

Build your own missions, quests, events, maps and more for Ground of Aces.
No Unity, no compiler - a mod is a folder of text files. And if you like, an AI agent writes them for you.

</div>

<div class="doors" markdown>

<a class="door" href="start/">
<strong>I have never programmed</strong>
Start here. We install everything together, step by step, and you have your first mod in the game ten minutes later.
</a>

<a class="door" href="missions/first-mission/">
<strong>I want to dive straight in</strong>
You know your way around files and folders. Copy an example, change it, reload - done.
</a>

<a class="door" href="ai/">
<strong>I use Claude Code or Codex</strong>
Clone this repository, start your agent in it, and describe the mod you want. The agent knows the rules.
</a>

</div>

## Get access

The documentation is open to everyone. The modkit itself - the repository with the examples,
templates, validator and AI rules - is private during the preview. To get access, send a short
email with your **GitHub username** to
[nuria@blindflugstudios.com](mailto:nuria@blindflugstudios.com) or
[moritz@blindflugstudios.com](mailto:moritz@blindflugstudios.com). Tell us what you would like to
build - we love to hear it.

## What you can build

| | What it is | Start with |
|---|---|---|
| **Missions** | Flights the player sends planes on, with four possible endings | [Missions](missions/index.md) |
| **Chains and campaigns** | Missions that unlock each other, historic operations on their real date | [Chains and campaigns](missions/chains.md) |
| **Event scripts** | Python that reacts to what happens on the base and in the air | [Scripting](scripting/index.md) |
| **Quests** | Checklists that guide the player | [Quests](quests/index.md) |
| **Game data** | Aircraft, buildings, raids, costs - change the numbers | [CSV tables](data/csv.md) |
| **Maps and art** | Your own maps, models, terrain objects and biomes | [Maps](content/maps.md) |
| **Workshop** | Share your mod with every player | [Steam Workshop](sharing/workshop.md) |

## How it works in one minute

1. Open the game, go to **Main menu → Mods → Open folder**.
2. Put a mod folder there - for example a copy of one of the [examples](examples.md).
3. Back in the game, return to the main menu, open **Mods** once (it rescans the folder) and load your save.

That is the whole loop - see [Testing and reloading](basics/testing.md) for the details. Everything else on this site is about what you put into that folder.

## Join the squadron

- Questions, ideas, showing off: the [Discord modding channel](https://discord.com/channels/1006159027157356587/1551969822911242240)
- Found a mistake on this site? [Open an issue](https://github.com/blindflugstudios/goa-modkit/issues) or improve the page yourself with the pencil icon at the top.
- Finished mod? Put it on the [Steam Workshop](sharing/workshop.md).
