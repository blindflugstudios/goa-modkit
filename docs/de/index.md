---
hide:
  - navigation
  - toc
---

# Ground of Aces Modkit

!!! danger "Developer Preview - Nutzung auf eigene Gefahr"
    Dieses Modkit ist eine **Developer Preview**. Alles hier - die Doku, die Werkzeuge, die Regeln
    und die Modding-Funktionen des Spiels selbst - **kann sich jederzeit ohne Ankündigung ändern**.
    Du nutzt es **auf eigene Gefahr**: Sichere
    deine Spielstände, bevor du eine Mod ausprobierst, und verlass dich nicht darauf, dass etwas so
    bleibt, wie es ist.

<div class="hero" markdown>

![Ground of Aces](assets/logos/goa-logo-colored.png)

Bau deine eigenen Missionen, Quests, Ereignisse, Karten und vieles mehr für Ground of Aces.
Kein Unity, kein Compiler - ein Mod ist ein Ordner mit ganz normalen Dateien: JSON, CSV, Python, Modelle und Bilder. Und wenn du magst, schreibt ein KI-Agent sie für dich.

</div>

<div class="doors" markdown>

<a class="door" href="basics/first-mod/">
<strong>Ich habe noch nie programmiert</strong>
Fang hier an. Dein erster Mod dauert fünf Minuten und braucht nur das Spiel und einen Texteditor. Werkzeuge und KI kommen später, wenn du sie willst.
</a>

<a class="door" href="missions/first-mission/">
<strong>Ich will direkt loslegen</strong>
Du kennst dich mit Dateien und Ordnern aus. Beispiel kopieren, ändern, neu laden - fertig.
</a>

<a class="door" href="start/">
<strong>Ich nutze einen KI-Agenten</strong>
Claude Code, Codex oder das quelloffene OpenCode: Klone dieses Repository, starte deinen Agenten darin und beschreib den Mod, den du willst. Der Agent kennt die Regeln.
</a>

</div>

## Was du bauen kannst { #what-you-can-build }

| | Was es ist | Einstieg |
|---|---|---|
| **Missionen** | Flüge, auf die der Spieler Flugzeuge schickt, mit vier möglichen Ausgängen | [Missionen](missions/index.md) |
| **Ketten und Kampagnen** | Missionen, die sich gegenseitig freischalten, historische Operationen an ihrem echten Datum | [Ketten und Kampagnen](missions/chains.md) |
| **Ereignis-Skripte** | Python, das auf das reagiert, was auf dem Stützpunkt und in der Luft passiert | [Scripting](scripting/index.md) |
| **Quests** | Checklisten, die den Spieler anleiten | [Quests](quests/index.md) |
| **Spieldaten** | Flugzeuge, Gebäude, Angriffe, Kosten - dreh an den Zahlen | [CSV-Tabellen](data/csv.md) |
| **Karten** | Eigene Flugplätze, mit eigener Questreihe | [Karten](content/maps.md) |
| **Objekte** | Neue Modelle, Texturen und Symbole für Objekte, und neue Bodentexturen | [Objekte und Modelle](content/objects.md) |
| **Flugzeug-Skins** | Neue Lackierungen für die Flugzeuge des Spiels | [Flugzeug-Skins](content/airplanes.md) |
| **Workshop** | Teil deinen Mod mit allen Spielern | [Steam Workshop](sharing/workshop.md) |

## So funktioniert es in einer Minute { #how-it-works-in-one-minute }

1. Öffne das Spiel und geh auf **Hauptmenü** (Main menu) **→ Mods → Open folder**.
2. Leg dort einen Mod-Ordner ab - zum Beispiel eine Kopie eines der [Beispiele](examples.md).
3. Zurück im Spiel: Geh ins Hauptmenü, öffne **Mods**, drück auf **Refresh** (damit das Spiel den neuen Ordner bemerkt) und lade deinen Spielstand.

Das ist schon die ganze Runde - die Details stehen unter [Testen und neu laden](basics/testing.md). Alles andere auf dieser Seite dreht sich darum, was du in diesen Ordner legst.

## Komm zur Staffel { #join-the-squadron }

- Fragen, Ideen, Angeben: der [Modding-Kanal auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240)
- Einen Fehler auf dieser Seite gefunden? [Öffne ein Issue](https://github.com/blindflugstudios/goa-modkit/issues) oder verbessere die Seite selbst mit dem Stift-Symbol oben.
- Mod fertig? Stell ihn in den [Steam Workshop](sharing/workshop.md).
