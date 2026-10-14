# Loslegen mit KI-Modding

Jeden Mod kannst du von Hand mit einem Texteditor schreiben - siehe [Dein erster Mod](../basics/first-mod.md). Dieser Abschnitt ist für dich, wenn du Hilfe willst: das **Modkit** und einen **KI-Agenten**, der den Mod nach deiner Beschreibung baut.

## Das Modkit { #the-modkit }

Das Modkit ist ein Download. Darin sind:

- **Beispiele und Vorlagen**: vollständige, funktionierende Mods zum Kopieren und Ändern.
- **Der Validator**: ein Prüfer, der die Fehler findet, die das Spiel abstürzen lassen oder deinen Mod verstecken würden, noch bevor du das Spiel startest.
- **Regeln und Skills für KI-Agenten**: alles, was Claude Code, Codex oder OpenCode brauchen, um einen Mod nach deiner Beschreibung zu bauen, zu prüfen und ins Spiel zu kopieren.

Ein Mod aus dem Modkit ist derselbe Ordner mit Dateien wie einer von Hand. Die Beispiele und der Validator helfen auch ohne KI: siehe [Ohne KI-Agent](without-ai.md).

## Zuerst Zugang holen { #get-access-first }

Während der Developer Preview ist das Modkit privat. Diese Seiten kann jeder lesen, den Download nicht. Um ihn zu bekommen, schick deinen
**GitHub-Benutzernamen** per Mail an [jan@blindflugstudios.com](mailto:jan@blindflugstudios.com)
oder [moritz@blindflugstudios.com](mailto:moritz@blindflugstudios.com) (noch kein GitHub-Konto?
Die Installationsseiten zeigen, wie du eins anlegst - es ist kostenlos). Du bekommst dann eine
Einladung von GitHub per Mail; nimm sie an, und der Download-Schritt auf den Installationsseiten
funktioniert. Vor dem Annehmen verlangt GitHub, dass du die **Zwei-Faktor-Anmeldung**
einschaltest - die Installationsseiten führen dich durch. Ohne Einladung antwortet GitHub mit "Could not resolve to a Repository".

## Was du brauchst { #what-you-need }

- **Ground of Aces** auf Steam, unter Windows oder auf dem Mac.
- **Einen Computer, auf dem du Programme installieren darfst** (Admin-Rechte).
- **Etwa 20-30 Minuten** für die einmalige Einrichtung.
- **Ein kostenloses GitHub-Konto.** GitHub ist die Website, auf der das Modkit liegt.

Die Installationsseiten richten diese Werkzeuge für dich ein, einen Befehl nach dem anderen:

| Werkzeug | Was es für dich tut | Nötig? |
|---|---|---|
| Git | Lädt das Modkit herunter und hält es aktuell | Ja |
| GitHub CLI (`gh`) | Meldet dich aus dem Terminal bei GitHub an | Ja |
| Claude Code (oder Codex, oder OpenCode) | Der KI-Agent, der deinen Mod baut | Ja |
| Python | Startet den Mod-Prüfer (Validator) direkt | Optional, empfohlen |

## Was es kostet { #what-it-costs }

!!! note "Ehrlich vorweg"
    Das Modding im Spiel, das Modkit und der Steam Workshop sind kostenlos. **Die KI-Agenten nicht.**

    - **Claude Code** braucht ein bezahltes Claude-Abo (**Pro oder höher**). Im kostenlosen Claude-Tarif ist es nicht enthalten.
    - **Codex** braucht einen bezahlten ChatGPT-Tarif.
    - **OpenCode** ist Open Source und kostenlos zu installieren, aber **das KI-Modell dahinter ist nicht immer gratis**. Die Gratis-Modelle gibt es nur für begrenzte Zeit, sie dürfen deine Eingaben zum Training verwenden und sind deutlich schwächer als Claude oder GPT - genug für eine erste einfache Mission. Für regelmäßige Nutzung zahlst du pro Nutzung. Siehe [OpenCode](../ai/opencode.md).

    Du willst nicht für eine KI bezahlen? Alles funktioniert auch von Hand: siehe [Dein erster Mod](../basics/first-mod.md).

## Der ganze Weg in 5 Schritten { #the-whole-journey-in-5-steps }

1. **Installier die Werkzeuge** einmalig: [Windows](install-windows.md) oder [Mac](install-mac.md).
2. **Hol dir das Modkit**: `gh repo clone blindflugstudios/goa-modkit`. Das machst du einmal. Später holt `git pull` die Updates. Deine eigenen Mods liegen im Ordner `mods/` und werden von Updates nie angefasst.
3. **Beschreib deinen Mod** dem Agenten in ganz normaler Sprache, zum Beispiel "Mach mir eine Mission, in der zwei Spitfires einen beschädigten Bomber über den Ärmelkanal nach Hause eskortieren."
4. **Der Agent baut ihn, prüft ihn und kopiert ihn** in den `Mods`-Ordner des Spiels.
5. **Lade ihn im Spiel**: Öffne das Mods-Fenster und drück auf **Refresh**, lade deinen Spielstand und flieg los. [Dein erster KI-Mod in 10 Minuten](first-mod.md) zeigt jeden Klick.

Die 10 Minuten zählen ab Schritt 2, wenn die Werkzeuge schon installiert sind.

Du hängst irgendwo fest? Schau unter [Wenn nichts passiert](troubleshooting.md) nach oder frag im [Modding-Kanal auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).
