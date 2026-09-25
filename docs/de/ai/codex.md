# Codex

Codex ist der Coding-Agent von OpenAI. Die Codex CLI läuft in einem Terminal, in dem Ordner, in dem
du sie startest. Sie liest dieselben Regeln wie Claude Code.

## Einrichten { #set-up }

Installier Git und die GitHub CLI wie unter [Installation unter Windows](../start/install-windows.md)
oder [Installation auf dem Mac](../start/install-mac.md) beschrieben, dann installier die Codex CLI nach
[der Anleitung von OpenAI](https://learn.chatgpt.com/docs/codex/cli). Wähl beim ersten Start "Sign in with ChatGPT".

```bash
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
codex
```

## Was Codex in diesem Ordner findet { #what-codex-finds-in-this-folder }

| Datei | Was sie tut |
|---|---|
| `AGENTS.md` | Wird automatisch gelesen. Das vollständige Regelbuch: wie Mods aufgebaut sind, wo dein Spiel seine Dateien ablegt, jede Falle. |
| `.agents/skills/` | Ein Rezept pro Aufgabe (neue Mission, Quest, Ereignis-Skript, Workshop-Upload ...). Codex nimmt das, das zu deiner Bitte passt. |

Die Bitten und Tipps auf der Seite [Claude Code](claude-code.md#good-first-requests) funktionieren in Codex genauso.
