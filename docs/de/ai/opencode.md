# OpenCode

OpenCode ist ein **quelloffener** Coding-Agent fürs Terminal, wie Claude Code und Codex. Er liest
dieselben Regeln und Skills aus diesem Modkit. Der Unterschied: OpenCode ist an keine KI-Firma
gebunden. Du wählst selbst das **KI-Modell**, mit dem er arbeitet - darunter einige, die derzeit
nichts kosten.

!!! warning "Open Source heißt nicht kostenlos"
    **OpenCode ist Open Source und kostenlos zu installieren - das KI-Modell dahinter ist nicht
    immer gratis.** OpenCode Zen bietet einige Gratis-Modelle für begrenzte Zeit an: Deine
    Eingaben dürfen zum Training verwendet werden, und die Modelle können ohne Ankündigung
    verschwinden. Für regelmäßige Nutzung zahlst du pro Nutzung, über Zen-Guthaben oder einen
    eigenen Claude- oder OpenAI-Schlüssel. Die Gratis-Modelle sind außerdem spürbar schwächer als
    Claude oder GPT: gut genug für eine erste einfache Mission, bei größeren Mods musst du mehr
    nachbessern.

## Was es kostet { #what-it-costs }

OpenCode selbst ist freie Software ([MIT-Lizenz](https://github.com/anomalyco/opencode)). Was du
bezahlst - oder eben nicht - ist das Modell, das die Denkarbeit macht. Es gibt vier Wege:

| Modell | Kosten | Deine Daten | Qualität für Mods |
|---|---|---|---|
| **Gratis-Modelle in OpenCode Zen** (Name endet auf `free`, oder `big-pickle`) | Derzeit nichts. Angeboten "for a limited time"; die Liste ändert sich ohne Ankündigung. Zurzeit funktionieren sie ohne Konto. | Bei den meisten: Der Anbieter **darf deine Eingaben und Antworten zum Training seines Modells verwenden**. | Reicht für eine erste einfache Mission (getestet). Schwächer bei Kampagnen, Event-Skripten und Fehlersuche. |
| **Bezahlte Modelle in OpenCode Zen** | Pay-as-you-go: Konto mit Kreditkarte, **20 $ Startguthaben** (plus Kartengebühr), automatisches Nachladen von 20 $, sobald du unter 5 $ fällst (abschaltbar), Monatslimit einstellbar. | Je nach Modell; siehe den Hinweis zu jedem Modell in der Zen-Doku (bei Claude- und OpenAI-Modellen werden Anfragen 30 Tage aufbewahrt). | So gut wie das gewählte Modell - die Spitzenmodelle sind so gut wie Claude Code oder Codex. |
| **Eigener Claude- oder OpenAI-Schlüssel** | Bezahlung pro Nutzung bei dieser Firma (ein API-Schlüssel wird getrennt von einem Claude- oder ChatGPT-Abo abgerechnet). | Die API-Bedingungen dieser Firma. | Dieselben Modelle wie Claude Code oder Codex. |
| **Lokale Modelle** (Ollama, LM Studio) | Nichts zu zahlen, braucht aber einen starken Rechner (viel Arbeitsspeicher, am besten eine gute Grafikkarte). | Bleiben auf deinem Rechner. | Deutlich schwächer. Für Leute, die gern basteln. |

Preise und die Liste der Gratis-Modelle stammen aus OpenCodes
[Zen-Dokumentation](https://opencode.ai/docs/zen/) (Stand September 2026). Schau dort nach, bevor
du Guthaben auflädst - das ändert sich oft.

!!! tip "Unsere Empfehlung für den Einstieg"
    Fang mit einem **Gratis-Modell aus Zen** an, um zu sehen, wie es funktioniert. Bleibst du
    beim Modden, lade ein kleines Zen-Guthaben mit Monatslimit auf oder nimm Claude Code oder
    Codex. Schreib nie etwas in eine Anfrage, das ein Modell-Anbieter nicht lesen soll.

## Qualität { #quality }

Wir haben OpenCode mit dem Gratis-Modell `big-pickle` an diesem Modkit getestet: Auf die Bitte
"eine Mission, in der zwei Spitfires einen beschädigten Bomber über den Ärmelkanal nach Hause
begleiten" hat es die Regeln und Beispiele gelesen, die Mission gebaut, selbstständig den
Validator laufen lassen, bis alles sauber war, und war nach etwa drei Minuten fertig.

Das ist der einfache Fall. Was du darüber hinaus erwarten kannst:

- **Einfache Missionen und Quests:** klappen meistens.
- **Ketten, Kampagnen, Event-Skripte:** mehr Fehler, mehr Runden "das hat nicht funktioniert,
  versuch es noch mal". Teil große Ideen in kleine Schritte.
- **Der Validator findet Abstürze, keine schlechten Ideen.** Er stoppt fehlende Outcomes, falsche
  Ids oder verbotene Importe. Er merkt nicht, wenn Funksprüche langweilig sind, eine Mission viel
  zu leicht ist oder die Logik nicht zum Spiel passt. Lies, was der Agent geschrieben hat.
- **Hol dir eine zweite Meinung:** Tipp `@mod-reviewer review mods/<dein mod>`, bevor du
  veröffentlichst.
- **Kommst du nicht weiter?** Wechsle für diese eine Aufgabe zu einem stärkeren Modell
  (`/models`).

## Installation { #install }

!!! note "Windows: von uns noch nicht getestet"
    OpenCodes eigene Doku empfiehlt WSL (eine Linux-Umgebung in Windows). Wir installieren
    stattdessen direkt mit winget, weil WSL für Einsteiger ein großer zusätzlicher Schritt ist.
    Unter Windows sind wir mit dem Testen noch nicht fertig - wenn etwas schiefgeht, sag uns
    Bescheid im [Discord-Modding-Kanal](https://discord.com/channels/1006159027157356587/1551969822911242240).

Installier zuerst Git und die GitHub CLI, wie in [Installation unter Windows](../start/install-windows.md)
oder [Installation auf dem Mac](../start/install-mac.md) beschrieben. Den Schritt mit Claude Code
kannst du überspringen. Dann:

=== "Windows"

    ```powershell
    winget install --id SST.opencode -e
    ```

=== "Mac"

    ```bash
    brew install anomalyco/tap/opencode
    ```

Schließ das Terminal, öffne ein neues und prüf:

```bash
opencode --version
```

**Das solltest du sehen:** eine Versionsnummer, zum Beispiel `1.18.32`.

## Starten und Modell wählen { #start-it-and-pick-a-model }

```bash
cd goa-modkit
opencode
```

OpenCode öffnet sich im Terminal. Um ein Modell zu wählen, tipp `/models` und drück **Enter**,
dann nimm eins aus **OpenCode Zen**, dessen Name auf `free` endet (oder `big-pickle`). Welche
Gratis-Modelle es gibt, ändert sich von Monat zu Monat - nimm, was gerade angeboten wird.

Für bezahlte Zen-Modelle oder einen eigenen Schlüssel tipp `/connect`, wähl den Anbieter und
folg den Schritten. Für Zen legst du einen API-Schlüssel unter
[opencode.ai/auth](https://opencode.ai/auth) an.

## Was OpenCode in diesem Ordner findet { #what-opencode-finds-in-this-folder }

| Datei | Was sie tut |
|---|---|
| `AGENTS.md` | Wird automatisch gelesen. Das ganze Regelwerk: wie Mods gebaut werden, wo dein Spiel seine Dateien ablegt, jede Falle. |
| `.agents/skills/` | Ein Rezept pro Aufgabe (neue Mission, Quest, Event-Skript, Workshop-Upload ...). OpenCode wählt das, das zu deiner Anfrage passt. |
| `.opencode/agents/mod-reviewer.md` | Ein zweites Paar Augen: `@mod-reviewer` prüft einen fertigen Mod, ohne ihn zu verändern. |
| `.opencode/agents/translator.md` | `@translator` übersetzt die Texte deines Mods und lässt Ids und Platzhalter unangetastet. |

Beim Start meldet OpenCode eventuell eine Warnung wie `duplicate skill name`. Die ist harmlos:
Dieselben Skills liegen für Claude Code auch in `.claude/skills/`, und OpenCode nimmt eine Kopie.

## Gute erste Anfragen { #good-first-requests }

Die Anfragen auf der Seite [Claude Code](claude-code.md#good-first-requests) funktionieren in
OpenCode genauso. Mit einem Gratis-Modell halte sie klein und genau. Du kannst auch auf Deutsch
schreiben:

```text
Mach mir eine Mission, in der zwei Spitfires einen beschädigten Bomber über den Ärmelkanal nach Hause begleiten.
```

```text
@mod-reviewer review mods/channel_escort
```
