# Dein erster Mod in 10 Minuten

Du beschreibst eine Mission in ganz normaler Sprache, lässt den Agenten sie bauen und fliegst sie in deinem eigenen Spiel. Die Uhr läuft ab jetzt, die Werkzeuge sind schon installiert ([Windows](install-windows.md) / [Mac](install-mac.md)).

## 1. Öffne das Modkit und starte den Agenten { #1-open-the-modkit-and-start-the-agent }

Öffne das Terminal und tippe:

=== "Windows"

    ```powershell
    cd ~\goa-modkit
    git pull
    claude
    ```

=== "Mac"

    ```bash
    cd ~/goa-modkit
    git pull
    claude
    ```

`git pull` holt die neueste Version des Kits. `claude` startet den Agenten. Starte ihn immer **innerhalb** des Ordners `goa-modkit`: Dort findet er die Regeln, Beispiele und Skills, die ihm beibringen, wie Mods für Ground of Aces funktionieren.

## 2. Beschreib deine Mission { #2-describe-your-mission }

Tippe das in Claude Code und drück **Enter**:

```text
Make me a mission where two Spitfires escort a damaged bomber home over the Channel.
```

Ändere, was du willst: die Flugzeuge, den Ort, die Stimmung. Du kannst auch einfach auf Deutsch schreiben, zum Beispiel "Mach mir eine Mission, in der zwei Spitfires einen beschädigten Bomber über den Ärmelkanal nach Hause eskortieren." Vielleicht stellt dir der Agent ein, zwei Rückfragen, etwa zum Schwierigkeitsgrad. Antworte genauso locker.

## 3. Schau dem Agenten bei der Arbeit zu { #3-watch-the-agent-work }

Der Agent erledigt jetzt drei Aufgaben. Er sagt dir, was er gerade tut, und fragt nach, bevor er Dateien außerhalb des Kits ändert. Antworte mit **Yes**, wenn er Dateien anlegen oder den Prüfer starten will.

| Aufgabe | Was passiert |
|---|---|
| **Bauen** (Skill `new-mission`) | Legt deinen Mod in `mods/` an, zum Beispiel `mods/channel_escort/Missions/channel_escort.json` (Zahlen: Werte, Ort, Ausgänge) und `channel_escort.py` (Texte und Funksprüche). |
| **Prüfen** (Skill `validate`) | Startet den **Validator**, der die Fehler findet, die das Spiel zum Absturz bringen oder deine Mission verstecken würden. Er behebt, was er findet, und prüft erneut, bis alles sauber ist. |
| **Installieren** (Skill `install-mod`) | Kopiert den fertigen Mod in den `Mods`-Ordner des Spiels. |

Der `Mods`-Ordner des Spiels liegt hier:

=== "Windows"

    ```text
    %USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\
    ```

=== "Mac"

    ```text
    ~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/
    ```

Wenn der Agent meldet, dass der Mod installiert ist, merk dir die **Missions-ID**, die er dir nennt (zum Beispiel `channel_escort`). Die brauchst du gleich.

!!! note "Der Agent kann in deinem Spiel keine Knöpfe drücken"
    Er baut, prüft und kopiert. Den Mod im Spiel zu laden ist deine Aufgabe, und das dauert eine Minute.

## 4. Lade den Mod im Spiel { #4-load-the-mod-in-the-game }

Das Spiel liest Mods ein, wenn ein Spiel geladen wird. Also:

1. Starte Ground of Aces. Läuft es schon mit einem offenen Spielstand, geh zuerst auf **Einstellungen** (Options) **→ Verlassen zum Hauptmenü** (Quit to main menu).
2. Öffne im Hauptmenü **Mods**. Die Liste wird beim Öffnen des Fensters aktualisiert. Dein Mod sollte dort stehen und eingeschaltet sein.
3. Dein Mod hat eine Python-Datei (die `.py`), deshalb zeigt er auch einen **Scripting**-Schalter. Schalte ihn ein und bestätige - die Skripte hast du selbst geschrieben. (Die aktuelle Spielversion führt die Skripte einer Mod ohnehin aus, der Schalter schadet also nicht; siehe [Python-Mods und Sicherheit](../basics/security.md).)
4. Schließ das Mods-Fenster und lade deinen Spielstand (oder starte ein neues Spiel).

<!-- screenshot: Mods window with the new mod listed, enabled, scripting switched on -->

Das ganze Spiel neu zu starten funktioniert auch und ist die sicherste Variante, wenn dir irgendetwas komisch vorkommt.

## 5. Finde deine Mission { #5-find-your-mission }

Deine Mission landet jetzt in dem Topf, aus dem das Spiel Missionen zieht. Sie taucht also auf der Kriegskarte auf, sobald ihre Bedingungen erfüllt sind (zum Beispiel ein bestimmter Tag oder eine bestimmte Startbahn). Um sie **sofort** zu sehen, nimm die Cheat-Konsole:

1. Öffne die **Einstellungen** und schalte **Cheats** ein.
2. Auf dem Spielbildschirm erscheint ein Cheat-Knopf. Klick darauf, um die Konsole zu öffnen.
3. Tippe deine Missions-ID ein und drück **Enter**:

```text
create_mission channel_escort
```

**Das solltest du sehen:** `Mission created!` in der Konsole. Schließ die Konsole und öffne die Kriegskarte. Da ist sie.

<!-- screenshot: war map with the new mission -->

Teil Crews und Flugzeuge ein, schick sie los und warte auf die Funksprüche, die du dir gewünscht hast. Das ist dein erster Mod.

Mehr zur Konsole: [Cheat-Konsole](../basics/cheats.md).

## 6. Ändere etwas { #6-change-something }

Geh zurück ins Terminal und wünsch dir eine Änderung, zum Beispiel:

```text
Make the mission harder and let the bomber crew radio in when they spot the English coast.
```

Der Agent bearbeitet, prüft und kopiert den Mod erneut. Dann im Spiel: **Einstellungen → Verlassen zum Hauptmenü**, Spielstand laden und die Mission noch einmal anschauen. (Hat die Änderung einen neuen Ordner in den Mod gebracht, zum Beispiel ein erstes `Quests/`, öffne vor dem Laden einmal **Mods**.)

## Wenn etwas schiefgeht { #if-something-goes-wrong }

- Die Mission taucht nicht auf, die Texte sehen aus wie `missions/...` oder das Spiel beschwert sich: siehe [Wenn nichts passiert](troubleshooting.md).
- Oder sag dem Agenten einfach: `read my Player.log and tell me what went wrong`. Er weiß, wo das Spiel auf deinem Computer sein Log schreibt.

## Codex oder OpenCode statt Claude Code { #using-codex-or-opencode-instead }

Beide funktionieren genauso. Sie lesen die Datei `AGENTS.md` des Kits, in der dieselben Regeln stehen, denen auch die Skills folgen.

1. Installieren und anmelden: [Codex](../ai/codex.md) (braucht einen bezahlten ChatGPT-Tarif) oder [OpenCode](../ai/opencode.md) (Open Source; Modell mit `/models` wählen).
2. Im Terminal: mit `cd` in `goa-modkit` wechseln, dann `codex` oder `opencode` tippen.
3. Füg denselben Prompt ein. Der Agent baut, prüft und kopiert den Mod. Die Schritte 4 und 5 im Spiel sind dieselben.

Mit einem der Gratis-Modelle von OpenCode klappt eine erste einfache Mission in der Regel, bei größeren Mods gibt es mehr Fehler - lies das Ergebnis und lass `@mod-reviewer` drüberschauen. Die Gratis-Modelle gibt es nur für begrenzte Zeit, und sie dürfen deine Eingaben zum Training verwenden.
