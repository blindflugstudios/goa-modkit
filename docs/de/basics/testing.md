# Testen und neu laden

Für Mods gibt es kein Vorschaufenster. Du testest eine Mod, indem du sie ins Spiel lädst und schaust, was passiert. Diese Seite zeigt dir, wie du diese Schleife kurz hältst: Datei ändern, neu laden, nachsehen, ohne das Spiel neu zu starten.

## Die Kurzfassung { #the-short-version }

1. Bearbeite deine Dateien im Mod-Ordner.
2. Speichere im Spiel und geh dann auf **Einstellungen** (Options) **→ Verlassen zum Hauptmenü** (Quit to main menu).
3. Wenn du einen neuen Mod-Ordner angelegt hast (oder einen Inhaltsordner wie `Quests/`, der beim Spielstart leer war), öffne im Hauptmenü **Mods** und drück auf **Refresh**. Das bloße Öffnen des Fensters durchsucht den `Mods`-Ordner nicht neu.
4. Lade deinen Spielstand. Missionen, Skripte, Quests, CSV-Tabellen, Karten und Flugzeug-Skins werden bei jedem Laden eines Spielstands frisch eingelesen. Nur Grafik (`Objects/`, `Biomes/`) braucht einen kompletten Neustart.
5. Für eine Mission öffnest du die Cheat-Konsole und tippst `create_mission <your_mission_id>`, damit sie sofort auf der Kriegskarte erscheint.
6. Irgendwas stimmt nicht? Öffne `Player.log` (siehe [unten](#reading-playerlog)).

## Neu laden, ohne das Spiel neu zu starten { #reloading-without-restarting-the-game }

Jedes Mal, wenn du einen Spielstand lädst, liest das Spiel die Inhalte deiner Mod neu ein: Missionsdateien, Python-Skripte, Quests, CSV-Tabellen, Karten und Flugzeug-Skins, aus dem Spiel selbst und aus jeder aktivierten Mod. Deine Bearbeitungsschleife lautet also: Datei ändern, zurück ins Hauptmenü, **Mods** öffnen, Spielstand erneut laden.

Zwei Dinge brauchen mehr:

- **Grafik wird nur beim Spielstart importiert.** Modelle, Texturen und andere Dateien in `Objects/` und `Biomes/` brauchen einen kompletten Neustart des Spiels. Ein künftiges Update bringt eine Option, Mods im Hauptmenü neu zu laden; dann ist der Neustart nicht mehr nötig.
- **Neue Mods**: Ein Mod-Ordner, den du gerade angelegt hast, taucht erst auf, wenn du im Mods-Fenster auf **Refresh** drückst (oder das Spiel neu startest). Dasselbe gilt für einen Inhaltsordner wie `Quests/`, der beim Spielstart leer war. Prüfe, dass die Mod eingeschaltet ist.

Eine Mission, die in deinem Spielstand schon auf der Kriegskarte lag, behält die Werte, mit denen sie erstellt wurde. Wenn du das JSON einer Mission geändert hast, erstelle mit `create_mission` eine frische Kopie, um die Änderung zu sehen.

## Eine Mission sofort erscheinen lassen { #making-a-mission-appear-now }

Missionen werden über die Woche verteilt zufällig gezogen, auf eine bestimmte zu warten dauert also lange.

```text
create_mission mymod_coastal_patrol
```

setzt die Mission sofort auf die Kriegskarte. Die Cheat-Konsole braucht ein geladenes Spiel: Schalte sie unter **Einstellungen → Cheats** ein und nutze dann den Cheat-Button auf dem Spielbildschirm (siehe [Cheat-Konsole](cheats.md)). Sie ignoriert die Voraussetzungen, Datumssperren und Karten-Tags der Mission. Sie beweist also, dass die Mission **lädt und fliegt**, nicht, dass sie von selbst erscheinen würde. Beim Tippen schlägt dir die Konsole Missions-Ids vor.

Lautet die Antwort `Unknown mission ID`, hat das Spiel deine Dateien nicht gelesen: Geh die Checkliste unten durch. Lautet sie `Mission ... has neither mission data nor a script`, wurde die Datei gefunden, konnte aber nicht verwendet werden, meistens eine reine Skript-Mission ohne `get_mission_id`-Handler.

Weitere Cheats, die beim Testen von Missionen helfen:

| Befehl | Wofür |
|---|---|
| `skip_day` | zum nächsten Tag springen; historische Missionen werden jede Spielstunde geprüft, eine für diesen Tag datierte erscheint also innerhalb der Stunde |
| `freeze_time off` | falls die Uhr stehen geblieben ist (manche Cheats frieren die Zeit als Nebenwirkung ein) |

Die vollständige Liste steht auf der Seite [Cheat-Konsole](cheats.md).

### Eine Kette testen { #testing-a-chain }

`create_mission` überspringt jede Sperre, kann also nicht zeigen, dass eine Kette freigeschaltet wird. So testest du das Freischalten:

1. Senk die Sperren für den Test: `RunwayTier` 1 und `EarliestAppearanceDay` 1 räumen die zwei häufigsten Gründe aus dem Weg, warum eine Mission nie auftaucht.
2. Mach die Folgemission historisch (`"_isHistoric": true`). Historische Missionen überspringen die Zufallsziehung. Das Spiel prüft sie jede Spielstunde, sie erscheinen also innerhalb der Stunde, nachdem ihre Sperren erfüllt sind (oder an ihrem Datum); auf einen Wochen-Slot warten sie nie.
3. Flieg die erste Mission bis zu dem Ausgang, den du testest, und warte bis zu einer Spielstunde.

Denk daran: Eine historische Mission gibt es nur einmal, sobald sie gewonnen wurde. Schalte `_isHistoric` danach wieder aus, wenn die Mission kein Story-Moment sein soll.

## Wenn nichts auftaucht { #when-nothing-shows-up }

Arbeite diese Liste ab, bevor du an deiner Logik zweifelst.

**1. Liegt die Datei am richtigen Ort?**
Missionsdateien, Event-Skripte und Hilfsmodule gehören alle nach `Mods/<your_mod>/Missions/`. Für Mods gibt es keinen `Events/`- oder `Scripts/`-Ordner; ein Skript an einem anderen Ort läuft nie, und zwar ohne Meldung. Die Endung muss genau `.py` oder `.json` sein (Vorsicht vor `coastal_patrol.json.txt`, wenn dein System Dateiendungen ausblendet).

**2. Ist die Mod aktiviert?**
Eine im Mods-Fenster ausgeschaltete Mod wird gar nicht geladen. Ein Mod-Ordner, den du angelegt hast, während das Spiel lief, erscheint erst, wenn du im Mods-Fenster auf **Refresh** drückst (oder das Spiel neu startest).

**3. Wurde das Skript geladen?**
In Entwicklungs-Builds steht jedes erfolgreich geladene Skript mit seinem Dateinamen in `Player.log`, gefolgt von den Handlern, die es registriert hat. Das veröffentlichte Spiel schreibt nur Fehler ins Log, dort beweist eine fehlende Zeile also nichts: Prüf stattdessen, ob die Wirkung des Skripts im Spiel sichtbar wird.

**4. Gibt es einen Syntaxfehler?**
Ein Python-Syntaxfehler erscheint in `Player.log` so:

```text
Python syntax error: <message> (line N, column M)
```

Dann wird die ganze Datei übersprungen; nichts darin wird registriert. Mods laufen auf IronPython 3.4: Halte dich an die Python-Features, die die [Beispiele](../examples.md) nutzen, und vermeide alles, was neuer als Python 3.6 ist (`:=`, `match`).

**5. Wurde das JSON gelesen?**
Eine kaputte Missionsdatei wird mit dieser Zeile in `Player.log` übersprungen:

```text
Mission file at <path> could not be parsed, skipping it: <reason>
```

Meistens liegt es an einem fehlenden Komma oder einem überzähligen am Ende einer Liste.

**6. Passen die Namen zusammen?**
Der Name der `.py`-Datei, der Name der `.json`-Datei und die Id, die `get_mission_id` zurückgibt, müssen identisch sein. Weichen sie ab, führt das Spiel statt deines Skripts das Standardskript aus.

**7. Ist die Id schon vergeben?**
Eine Mission mit derselben Id wie eine eingebaute Mission oder eine aus einer anderen Mod ersetzt diese (oder wird von ihr ersetzt). Benenne deine mit einem Präfix um.

**8. Sind die Sperren erfüllt?**
Eine Mission kommt nur in den Pool, wenn alle ihre Voraussetzungen erfüllt sind. Vergleiche `RunwayTier` mit deiner Basis, `EarliestAppearanceDay` mit dem Tag der Kampagne, `CompletedMission` mit dem, was tatsächlich geflogen wurde, und `_tags` mit der Karte. Ein Kettenschritt braucht zusätzlich einen Vorgänger, der mit dem richtigen Ausgang beendet wurde.

## Die zwei Abstürze, die du kennen solltest { #the-two-crashes-worth-knowing }

Beide kommen von Prüfungen, die das Spiel nicht macht, deshalb gibt es keine freundliche Meldung:

- **Nicht genau vier `_missionOutcomes`:** Die Mission stürzt ab, wenn sie endet, lange nachdem du aufgehört hast, das JSON zu verdächtigen.
- **Weniger als zwei `_missionStats`:** Die Mission stürzt beim Fertigkeitswurf ab, mitten im Flug.

Wenn eine Mission fliegt, aber am Ende in die Luft geht, zähl zuerst die Ausgänge.

## Prüfungen vor dem Start { #checks-you-can-run-before-launching }

Alles hier kannst du prüfen, ohne das Spiel zu starten, und es lohnt sich nach jeder Änderung. Der Validator erledigt das alles für dich (siehe [Ohne KI-Agent](../start/without-ai.md)):

- das JSON lässt sich lesen
- genau 4 Ausgänge, in dieser Reihenfolge: schiefgelaufen + gescheitert, schiefgelaufen + bestanden, wie geplant + gescheitert, wie geplant + bestanden
- mindestens 2 Missions-Stats
- `_missionIcon` ist einer von `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability`, `Stealth`, `Luxury`, `Success`, `Failure`, `Cancel`
- `_enemyPlaneReport` ist 18 oder kleiner
- `.py` und `.json` haben denselben Namen, und `get_mission_id` gibt diesen Namen zurück
- die Id doppelt keine vorhandene Missions-Id
- jeder Textschlüssel, den das Skript schreibt, folgt `missions/<id>/<slot>`
- kein nie aufgerufener Handler ist implementiert (`get_mission_icon`, `calculate_*_modifiers`)

Ein sauberer Validator-Lauf heißt, dass die Mod korrekt aufgebaut ist, nicht, dass sie sich gut spielt. Das verrät dir nur ein Flug im Spiel.

## Wo Text verloren geht { #where-text-goes-missing }

Wenn die Mission erscheint, aber ein Feld wie ihr Name im Missionsfenster leer bleibt, wurde dieser Text nie definiert. Drei Schlüssel baut das Spiel selbst und erwartet, dass es sie gibt:

```text
missions/<id>/mission_name
missions/<id>/mission_description
missions/<id>/intel_threat_report
```

Sie lassen sich nicht umbenennen. Definiere sie mit `localization.SetTerm` oder füll die passenden `_raw*`-Felder im JSON (siehe [Lokalisierung](../scripting/localization.md)). Die anderen sechs Schlüssel verwendet dein eigenes Skript, ein Tippfehler dort zeigt sich also als roher Schlüssel im Ereignisprotokoll statt im Missionsfenster.

## Player.log lesen { #reading-playerlog }

Das Spiel schreibt, was ihm auffällt, in eine Textdatei namens `Player.log`. Das veröffentlichte Spiel schreibt nur Fehler ins Log; die ausführlichen `[Mod ...]`-Zeilen erscheinen nur in Entwicklungs-Builds. Sie wird bei jedem Spielstart neu geschrieben, schau sie dir also an, während das Spiel läuft, oder direkt nachdem du es geschlossen hast.

| Plattform | Ort |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

Öffne sie mit einem beliebigen Texteditor und such nach deinem Mod-Namen oder deiner Missions-Id. Deine eigenen Skripte können mit `logger.Log("...")` hineinschreiben, siehe [API](../scripting/api.md#logger).
