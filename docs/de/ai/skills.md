# Skills und Agenten

Ein **Skill** ist ein schriftliches Rezept für eine Aufgabe. Der Agent liest von jedem Skill nur die
kurze Beschreibung, bis deine Bitte zu einem passt, und folgt ihm dann Schritt für Schritt. Jeder Skill,
der etwas baut, endet gleich: Validator laufen lassen, Gemeldetes beheben, Mod ins Spiel kopieren und
dir sagen, wie du ihn im Spiel zu sehen bekommst.

Die Skills liegen in `.agents/skills/` (lesen Codex und OpenCode) und werden nach `.claude/skills/`
gespiegelt (liest Claude Code). Sie sind identisch.

## Skills

| Skill | Sag etwa | Was er tut |
|---|---|---|
| `new-mission` | "Mach eine Mission, in der ..." | Baut eine Mission (JSON und Python) mit allen vier Ausgängen |
| `new-quest` | "Füg eine Quest hinzu, die den Spieler bittet, ..." | Baut eine Quest mit ihren Teil-Quests |
| `event-script` | "Wenn X auf dem Stützpunkt passiert, mach Y" | Schreibt ein Python-Ereignis-Skript |
| `csv-tweak` | "Mach die Spitfire schneller" | Ändert Spieldaten über eine CSV-Überschreibung |
| `localize-mod` | "Füg meinem Mod deutsche Texte hinzu" | Ergänzt oder korrigiert die Texte eines Mods in weiteren Sprachen |
| `new-map` | "Liefer eine Karte mit meiner eigenen Questreihe aus" | Richtet einen Karten-Ordner und seine Metadaten ein |
| `import-model` | "Nimm mein eigenes Modell für ..." | Bringt ein 3D-Modell oder eine Textur als Grafik-Mod für Objekte oder Biome in einen Mod |
| `publish-workshop` | "Stell meinen Mod in den Workshop" | Prüft den Mod und führt dich durch den Upload im Spiel |
| `validate` | "Prüf meinen Mod" | Startet den Validator und erklärt jeden Fund in einfachen Worten |
| `install-mod` | "Pack meinen Mod ins Spiel" | Kopiert den Mod in den `Mods`-Ordner des Spiels |
| `read-log` | "Irgendwas stimmt nicht, schau ins Log" | Liest dein `Player.log` und erklärt, was schiefgegangen ist |
| `update-kit` | "Aktualisier das Kit" | Holt die neuesten Regeln, Doku und Skills und sagt dir, was sich geändert hat |
| `update-docs` | "/update-docs" | Für Kit-Maintainer: gleicht dieses Handbuch mit dem `Docs/`-Ordner des Spielteams ab (fragt nach einem GitHub-Link oder einem lokalen Pfad) |

## Agenten (Claude Code und OpenCode) { #agents-claude-code-and-opencode }

In Claude Code ruft der Agent diese Helfer selbst oder auf deinen Wunsch auf. In OpenCode rufst du
sie mit `@` auf, zum Beispiel `@mod-reviewer review mods/channel_escort`.

| Agent | Was er tut |
|---|---|
| `mod-reviewer` | Prüft einen fertigen Mod gegen jede Regel und startet den Validator. Berichtet nur, ändert nie etwas. |
| `translator` | Übersetzt die Texte eines Mods, die Spieler sehen, und lässt IDs, Schlüssel und Platzhalter unangetastet. |

## Schreib deinen eigenen Skill { #write-your-own-skill }

Ein Skill ist ein Ordner mit einer `SKILL.md`:

```markdown
---
name: my-skill
description: One sentence saying exactly when to use this skill.
---

# My skill

Step-by-step instructions for the agent.
```

Leg ihn in `.agents/skills/my-skill/` ab, führ `python tools/sync_skills.py` aus, um ihn für Claude Code
zu spiegeln, und probier ihn aus. Gute Skills sind als Pull Request willkommen - siehe
[CONTRIBUTING.md](https://github.com/blindflugstudios/goa-modkit/blob/main/CONTRIBUTING.md).
