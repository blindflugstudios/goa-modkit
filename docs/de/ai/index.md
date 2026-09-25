# KI-Agenten

Du kannst jeden Mod auf dieser Seite von Hand bauen. Du musst aber nicht. Dieses Repository ist
so eingerichtet, dass ein KI-Coding-Agent - **Claude Code** oder **Codex** - Mods für dich bauen
kann: Du beschreibst die Idee in einfachen Worten, der Agent schreibt die Dateien, prüft sie und
legt sie in dein Spiel.

!!! warning "Das kostet Geld"
    Claude Code braucht ein bezahltes Claude-Abo (Pro oder höher). Codex braucht einen ChatGPT-Tarif,
    in dem es enthalten ist. Alles andere hier ist kostenlos. Wenn du nicht bezahlen willst, bau deinen
    Mod [ohne KI-Agent](../start/without-ai.md) - der Mission Editor im Spiel ist ein guter Anfang.

## Warum es hier so gut klappt { #why-it-works-well-here }

Eine allgemeine KI weiß nichts über Ground of Aces. Dieses Repository bringt es ihr bei:

- **`AGENTS.md`** ist das Regelbuch, das jeder Agent zuerst liest: wie ein Mod aufgebaut ist, wo das
  Spiel seine Dateien auf deinem Computer ablegt und jede Falle, die das Spiel abstürzen lässt oder
  still scheitert.
- **Skills** sind Schritt-für-Schritt-Rezepte für jeweils eine Aufgabe - eine neue Mission, eine Quest,
  ein Ereignis-Skript, ein Workshop-Upload. Der Agent sucht sich anhand deiner Bitte das passende aus.
- **Der Validator** prüft die Arbeit des Agenten, bevor sie in deinem Spiel landet. Der Agent startet
  ihn selbstständig und behebt, was er findet.
- **Die Doku und die Beispiele** dieser Seite liegen direkt daneben im selben Ordner, also liest der
  Agent die echten Regeln, statt zu raten.

## Der Ablauf { #the-loop }

1. Du: "Mach mir eine Mission, in der ..."
2. Der Agent fragt nach, was er wissen muss, eine Frage nach der anderen.
3. Er schreibt den Mod nach `mods/<your mod>/` und lässt den Validator laufen, bis alles sauber ist.
4. Er kopiert den Mod in den `Mods`-Ordner des Spiels.
5. Du: Geh im Spiel zurück ins Hauptmenü, öffne einmal **Mods** und lade deinen Spielstand (siehe [Testen und neu laden](../basics/testing.md)). Der Befehl `create_mission <id>` in der [Cheat-Konsole](../basics/cheats.md) lässt eine neue Mission sofort erscheinen.
6. Erzähl dem Agenten, was du siehst. Stimmt etwas nicht, liest er dein `Player.log` und behebt es.

Der Agent kann im Spiel keine Knöpfe für dich drücken - Schritt 5 ist immer deiner.

## Wähl deinen Agenten { #pick-your-agent }

| | Claude Code | Codex |
|---|---|---|
| Hersteller | Anthropic | OpenAI |
| Braucht | Claude Pro oder höher | einen ChatGPT-Tarif mit Codex |
| Liest | `CLAUDE.md` (die `AGENTS.md` lädt), `.claude/skills/`, `.claude/agents/` | `AGENTS.md`, `.agents/skills/` |
| Einrichtung | [Claude Code](claude-code.md) | [Codex](codex.md) |

Beide nutzen dieselben Regeln und dieselben Skills. Was alles dabei ist, steht unter [Skills und Agenten](skills.md).
