# Python-Mods und Sicherheit

Kurz gesagt: **Eine Mod mit Python-Skripten ist ein kleines Programm, das auf deinem Computer läuft.** Installiere Skript-Mods nur von Leuten, denen du vertraust, und schreib als Modder niemals Skripte, die über das Spiel hinausgreifen.

## Worin das Risiko besteht { #what-the-risk-is }

Mods, die nur JSON, CSV, Karten oder Modelle enthalten, sind reine Daten. Das Spiel liest sie ein, und das Schlimmste, was eine kaputte Mod anrichten kann, ist ein kaputtes Spiel.

Mods mit Python-Skripten (`.py`-Dateien) sind etwas anderes. Das Spiel führt sie mit IronPython aus, und **es gibt keine Sandbox**: Das Spiel hindert ein Skript nicht daran, zu importieren, was es will. Ein Skript kann auf die .NET-Laufzeitumgebung und das Dateisystem zugreifen. Ein böswilliges Skript könnte also Dateien auf deinem Computer lesen, ändern oder löschen.

Wir sagen dir das so deutlich, weil du es wissen solltest, nicht weil Workshop-Mods grundsätzlich gefährlich sind. Das gilt genauso für Mods in den meisten Spielen, die Skripte erlauben.

## Für Spieler { #for-players }

- **Wisse, welche Mods Skripte enthalten.** Das Fenster **Mods** zeigt dir, welche Mods Skripte mitbringen.
- **Nutze Skript-Mods nur von Autoren, denen du vertraust**: Leute, die du aus der Community kennst, mit bisherigen Mods, Kommentaren und einer Workshop-Seite, die erklärt, was die Mod tut.
- **Abonnierte Workshop-Mods sind standardmäßig eingeschaltet.** Im Fenster **Mods** kannst du jede Mod ausschalten.
- **Der Schalter Scripting schützt dich noch nicht.** Jede Mod zeigt ihn im Fenster **Mods**, aber er ist für eine kommende Zustimmungsfunktion reserviert und hat derzeit keine Wirkung: Die Skripte einer Mod laufen immer, wenn die Mod eingeschaltet ist. Um die Skripte einer Mod zu stoppen, schalte die ganze Mod aus oder kündige das Abo.
- **Kommt dir etwas komisch vor?** Kündige das Abo und melde die Mod auf ihrer Workshop-Seite und im [Modding-Channel auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240).

!!! tip "Prüf eine Mod, bevor du ihr vertraust"
    Jede Workshop-Mod ist ein Ordner mit reinen Textdateien. Du kannst ihre `.py`-Dateien in einem Texteditor öffnen oder den Validator des Modkits auf den Ordner loslassen: Er liest die Skripte, **ohne sie auszuführen**, und warnt vor allem, was über das Spiel hinausgreift.

## Für Modder { #for-modders }

Deine Mod braucht nie etwas außerhalb der Scripting-API des Spiels. Bleib dabei, dann müssen sich deine Spieler nie Gedanken machen.

**Normal und völlig in Ordnung**: die Scripting-API des Spiels, einschließlich Imports aus den `Blindflug.*`-Namespaces des Spiels und den Objekten, die das Spiel jedem Skript mitgibt:

```python
from Blindflug.FlightMission import MissionEvent
from Blindflug.GameResources import ResourceType

localization.SetTerm("en", "missions/my_mission/mission_name", "Dawn Patrol")
```

**Verwende niemals** Folgendes. Der Validator warnt vor jedem davon:

| Import oder Aufruf | Warum er tabu ist |
|---|---|
| `import clr` | Die Brücke zu .NET und von dort zu allem auf dem Computer |
| `import System`, `from System.IO import ...` (alles unter `System` oder `Microsoft`) | Direkter .NET-Zugriff: Dateien, Prozesse, Netzwerk |
| `import os`, `shutil`, `io`, `open(...)` | Zugriff aufs Dateisystem |
| `import sys`, `subprocess`, `ctypes`, `importlib` | Interna des Interpreters, Programme starten, nativen Code laden |
| `socket`, `urllib`, `http`, `ftplib`, `smtplib` | Netzwerkzugriff |
| `pickle`, `marshal`, `exec`, `eval`, `compile`, `__import__` | Code ausführen, der in deiner Datei nicht sichtbar ist |

Eine Ausnahme bei Dateien: Wenn ein Skript zwischen Spielsitzungen einen kleinen eigenen Zustand speichern muss, stellt die Scripting-API dafür einen Ordner bereit (`game_api.GetScriptDataPath`). Nutze nur diesen Ordner.

### Bevor du veröffentlichst { #before-you-publish }

1. Lass den Validator laufen und stell sicher, dass es **keine** Warnungen gibt, die über das Spiel hinausgreifen.
2. Schreib in deine Workshop-Beschreibung, dass die Mod Skripte enthält und was sie tun.
3. Halte deine Skripte lesbar. Spieler und Prüfer können sie öffnen, und klarer Code schafft Vertrauen.

Die Skills und Beispiele des Modkits halten sich an diese Regeln. Falls dir ein Agent jemals einen der Imports oben vorschlägt, sag ihm Nein.
