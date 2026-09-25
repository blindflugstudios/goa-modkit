# Claude Code

Claude Code ist der Coding-Agent von Anthropic. Er läuft in einem Terminal-Fenster, in dem Ordner,
in dem du ihn startest, und kann dort Dateien lesen, schreiben und ausführen.

## Einrichten { #set-up }

Wenn du [Installation unter Windows](../start/install-windows.md) oder
[Installation auf dem Mac](../start/install-mac.md) gefolgt bist, bist du startklar. Ansonsten kurz gefasst:

=== "Windows"

    ```powershell
    winget install --id Git.Git -e
    winget install --id GitHub.cli -e
    winget install Anthropic.ClaudeCode
    ```

=== "Mac"

    ```bash
    brew install git gh
    brew install --cask claude-code
    ```

Dann hol dir das Kit und starte Claude darin:

```bash
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
claude
```

Beim ersten Mal öffnet Claude deinen Browser, damit du dich mit deinem Claude-Konto anmelden kannst.

## Was Claude in diesem Ordner findet { #what-claude-finds-in-this-folder }

| Datei | Was sie tut |
|---|---|
| `CLAUDE.md` | Wird automatisch geladen. Sie zieht `AGENTS.md` nach, das vollständige Regelbuch. |
| `.claude/skills/` | Ein Rezept pro Aufgabe. Claude nutzt sie von selbst, wenn deine Bitte dazu passt. |
| `.claude/agents/mod-reviewer.md` | Ein zweites Paar Augen: prüft einen fertigen Mod gegen jede Regel, ohne ihn zu ändern. |
| `.claude/agents/translator.md` | Übersetzt die Texte deines Mods und lässt IDs und Platzhalter unangetastet. |

## Gute erste Bitten {#good-first-requests}

```text
Make me a mission where two Spitfires escort a damaged bomber home over the Channel.
```

```text
Write an event script: when a pilot comes back from a successful mission, the crew's mood goes up a little.
```

```text
Review my mod in mods/channel_escort and tell me what could go wrong.
```

```text
Translate the texts of mods/channel_escort into German.
```

## Tipps { #tips }

- Starte Claude **innerhalb** des Ordners `goa-modkit`. Anderswo gestartet sieht er die Regeln nicht.
- Beschreib mit deinen eigenen Worten, was du im Spiel siehst - gern auch auf Deutsch. "Die Mission taucht nie auf" reicht - Claude weiß, wo er nachschauen muss.
- Halte das Kit aktuell: Bitte Claude, "update the kit", oder führ selbst `git pull` aus. Deine eigenen Mods in `mods/` werden nie angefasst.
