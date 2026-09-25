# Loslegen

Willkommen an der Startbahn. Dieser Abschnitt bringt dich von "Ich habe Ground of Aces auf Steam" zu "Meine eigene Mission taucht in meinem Spiel auf". Programmiererfahrung brauchst du nicht.

## Wähl deinen Weg { #pick-your-door }

| Du hast... | Fang hier an |
|---|---|
| **Noch nie programmiert.** Du hast noch nie ein Terminal geöffnet, und das ist völlig in Ordnung. | [Installation unter Windows](install-windows.md) oder [Installation auf dem Mac](install-mac.md), danach [Dein erster Mod in 10 Minuten](first-mod.md). Lass das [Glossar](glossary.md) in einem zweiten Tab offen. |
| **Lust, direkt loszulegen.** Du kennst dich mit Dateien und einem Texteditor aus. | [Ohne KI-Agent](without-ai.md): Beispiel kopieren, JSON bearbeiten, prüfen, laden. Danach [So funktionieren Mods](../basics/mods.md). |
| **Schon Claude oder Codex.** Du hast bereits einen KI-Coding-Agenten. | Klone das Kit (Schritt 3 der Installationsseiten), starte deinen Agenten im Ordner und geh zu [Dein erster Mod in 10 Minuten](first-mod.md). |

## Zuerst Zugang holen { #get-access-first }

Während der Developer Preview ist das Modkit privat. Bevor du etwas installierst, schick deinen
**GitHub-Benutzernamen** per Mail an [nuria@blindflugstudios.com](mailto:nuria@blindflugstudios.com)
oder [moritz@blindflugstudios.com](mailto:moritz@blindflugstudios.com) (noch kein GitHub-Konto?
Die Installationsseiten zeigen, wie du eins anlegst - es ist kostenlos). Du bekommst dann eine
Einladung von GitHub per Mail; nimm sie an, und der Download-Schritt auf den Installationsseiten
funktioniert. Ohne Einladung antwortet GitHub mit "Could not resolve to a Repository".

## Was du brauchst { #what-you-need }

- **Ground of Aces** auf Steam, unter Windows oder auf dem Mac.
- **Einen Computer, auf dem du Programme installieren darfst** (Admin-Rechte).
- **Etwa 20-30 Minuten** für die einmalige Einrichtung unten.
- **Ein kostenloses GitHub-Konto.** GitHub ist die Website, auf der das Modkit liegt.

Die Installationsseiten richten diese Werkzeuge für dich ein, einen Befehl nach dem anderen:

| Werkzeug | Was es für dich tut | Nötig? |
|---|---|---|
| Git | Lädt das Modkit herunter und hält es aktuell | Ja |
| GitHub CLI (`gh`) | Meldet dich aus dem Terminal bei GitHub an | Ja |
| Claude Code | Der KI-Agent, der deinen Mod baut | Ja, für den KI-Weg |
| Python | Startet den Mod-Prüfer (Validator) direkt | Optional, empfohlen |

## Was es kostet { #what-it-costs }

!!! note "Ehrlich vorweg"
    Das Modkit, das Modding im Spiel und der Steam Workshop sind kostenlos. **Die KI-Agenten nicht.**

    - **Claude Code** braucht ein bezahltes Claude-Abo (**Pro oder höher**). Im kostenlosen Claude-Tarif ist es nicht enthalten.
    - **Codex** braucht einen bezahlten ChatGPT-Tarif.

    Du willst nicht für eine KI bezahlen? Alles funktioniert auch von Hand: siehe [Ohne KI-Agent](without-ai.md). Der **Mission Editor** im Spiel braucht überhaupt keine Werkzeuge.

## Der ganze Weg in 5 Schritten { #the-whole-journey-in-5-steps }

1. **Installier die Werkzeuge** einmalig: [Windows](install-windows.md) oder [Mac](install-mac.md).
2. **Hol dir das Modkit**: `gh repo clone blindflugstudios/goa-modkit`. Das machst du einmal. Später holt `git pull` die Updates. Deine eigenen Mods liegen im Ordner `mods/` und werden von Updates nie angefasst.
3. **Beschreib deinen Mod** dem Agenten in ganz normaler Sprache, zum Beispiel "Mach mir eine Mission, in der zwei Spitfires einen beschädigten Bomber über den Ärmelkanal nach Hause eskortieren."
4. **Der Agent baut ihn, prüft ihn und kopiert ihn** in den `Mods`-Ordner des Spiels.
5. **Lade ihn im Spiel**: Öffne das Mods-Fenster, lade deinen Spielstand und flieg los. [Dein erster Mod in 10 Minuten](first-mod.md) zeigt jeden Klick.

Die 10 Minuten zählen ab Schritt 2, wenn die Werkzeuge schon installiert sind.

Du hängst irgendwo fest? Schau unter [Wenn nichts passiert](troubleshooting.md) nach oder frag im [Modding-Kanal auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).
