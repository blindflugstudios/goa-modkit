# Dein erster Mod

Willkommen an der Startbahn. Ein Mod für Ground of Aces ist **ein Ordner mit ganz normalen Dateien** im `Mods`-Ordner des Spiels: JSON-, CSV- und Python-Dateien für Missionen, Quests, Skripte und Spieldaten, und Modelle (`.fbx`, `.glb`) und PNG-Bilder für neue Grafik. Du brauchst keinen Download, kein Konto und keine Programmierwerkzeuge. Für Missionen, Quests, Skripte und Datenänderungen reicht ein Texteditor. Für neue Grafik brauchst du das Programm, mit dem du Modelle oder Bilder machst.

## Dein erster Mod in fünf Minuten - nur mit dem Spiel { #your-first-mod-in-five-minutes-just-the-game }

Du sorgst dafür, dass die Holzwand eine Planke kostet statt zwei.

1. **Öffne den Mods-Ordner.** Starte Ground of Aces und klick im Hauptmenü auf **Mods → Open folder**. Ein Dateifenster geht auf. (Wenn du ihn lieber selbst suchst: unter Windows ist es `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\`, auf dem Mac `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/`.)
2. **Leg den Mod-Ordner an.** Erstelle in `Mods` einen Ordner namens `my_first_mod`.
3. **Gib dem Mod einen Namen.** Erstelle in `my_first_mod` eine Textdatei namens `config.json` und füge das hier ein:

    ```json
    {
      "Id": "my_first_mod",
      "Name": "Mein erster Mod",
      "Author": "Dein Name",
      "Version": "1.0.0"
    }
    ```

    `Name` zeigt das Mods-Fenster an. An der `Id` unterscheidet das Spiel die Mods: nur Kleinbuchstaben, Ziffern und `_`. Alle Felder erklärt [So funktionieren Mods](mods.md#configjson).

    Nimm einen einfachen Texteditor: den Editor (Notepad) unter Windows oder TextEdit auf dem Mac, umgestellt auf reinen Text (**Format → In reinen Text umwandeln**). Prüf, dass die Datei wirklich auf `.json` endet und nicht auf `.json.txt`.

4. **Mach die Änderung.** Erstelle in `my_first_mod` einen Ordner namens `CSV`. Der Name `CSV` muss genau so lauten, in Großbuchstaben: Das Spiel erkennt Inhalte an ihren Ordnernamen. Erstelle in `CSV` eine Textdatei namens `ResourceCost.json` und füge das hier ein:

    ```json
    {
      "Commands": [
        { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
      ]
    }
    ```

5. **Lade ihn.** Öffne im Spiel **Mods** und drück auf **Refresh**. **Mein erster Mod** erscheint in der Liste, eingeschaltet. Lade deinen Spielstand.
6. **Schau nach.** Öffne das Baumenü: Die Holzwand kostet jetzt eine Planke.

Das ist ein vollständiger Mod. Du hast jetzt das hier:

```text
Mods/
  my_first_mod/
    config.json
    CSV/
      ResourceCost.json
```

Ab jetzt läuft es immer gleich: Datei ändern, **Options → Quit to main menu**, Spielstand neu laden, Ergebnis ansehen. [Testen und neu laden](testing.md) erklärt die Details, und [So funktionieren Mods](mods.md) listet jeden Ordner, den ein Mod haben kann.

!!! tip "Sichere deine Spielstände"
    Modding ist eine Developer Preview. Kopier deine Spielstände an einen sicheren Ort, bevor du einen Mod ausprobierst.

## Wie es von hier weitergeht { #pick-your-way-from-here }

| Dein Ziel | Wohin |
|---|---|
| **Eine Mission im Spiel bauen, ohne Dateien von Hand zu schreiben** | Der **Mission Editor** im Hauptmenü des Spiels. Du füllst Felder aus, und er prüft deine Mission beim Speichern. Siehe [Ohne KI-Agent](../start/without-ai.md#the-easiest-route-the-in-game-mission-editor). |
| **Mods von Hand schreiben** | Ein Texteditor und diese Seiten reichen. Lies eine Themenseite: [Missionen](../missions/index.md), [Quests](../quests/index.md), [Skripte](../scripting/index.md), [CSV-Tabellen](../data/csv.md), [Karten](../content/maps.md), [Objekte](../content/objects.md), [Flugzeug-Skins](../content/airplanes.md). Sie zeigen jede Datei und jedes Feld, mit Beispielen zum Abtippen. [Deine erste Mission schreiben](../missions/first-mission.md) ist ein guter nächster Schritt. |
| **Fertige Beispiele kopieren und deinen Mod auf Fehler prüfen** | Hol dir das [Modkit](../start/index.md) und folge dann [Ohne KI-Agent](../start/without-ai.md). |
| **Einen KI-Agenten den Mod bauen lassen** | Claude Code, Codex oder das quelloffene OpenCode. Fang mit [Loslegen mit KI-Modding](../start/index.md) an. |

Lass das [Glossar](../start/glossary.md) in einem zweiten Tab offen, falls dir ein Wort neu ist.
