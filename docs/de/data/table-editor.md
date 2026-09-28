# Tabellen-Befehlsdateien

In Ground of Aces gibt es kein Tabellenfenster. Tabellen änderst du mit Dateien: Du schreibst eine kurze Liste von Befehlen, `Add`, `Replace` oder `Remove`, in eine Datei `<Table>.json` im Ordner `CSV/` deiner Mod. Jedes Mal, wenn ein Level lädt, führt das Spiel diese Befehle nacheinander auf seinen Datentabellen aus und prüft jede Änderung, bevor es sie schreibt.

Diese Seite erklärt im Detail, wie sich die Befehle verhalten. Das Format selbst, die Liste der Tabellen und die Regeln für jede Spalte findest du unter [CSV-Tabellen](csv.md); lies das zuerst.

## Schnellstart { #quick-start }

Die Gladiator soll mehr Treibstoff tragen, und die Holzwand soll billiger werden. Zwei Dateien in einer Mod:

```text
Mods/
  my_balance_mod/
    CSV/
      VehicleData.json
      ResourceCost.json
```

`VehicleData.json`:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350 } }
  ]
}
```

`ResourceCost.json`:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
  ]
}
```

Geh zurück ins Hauptmenü (Main Menu) und lade einen Spielstand: Die Änderungen sind drin. Ein Neustart ist nicht nötig.

## So wird ein Befehl ausgeführt { #how-a-command-is-carried-out }

Für jeden Befehl, in der Reihenfolge in der Datei, macht das Spiel Folgendes:

1. Es sucht die Zeile anhand der `Id`. Groß- und Kleinschreibung der Id spielt keine Rolle; die Schreibweise der Tabelle bleibt erhalten.
2. Es baut die komplette Zeile so, wie sie nach der Änderung aussähe, nebenbei, ohne die echte Tabelle schon anzufassen.
3. Die beiden Zellen, die das Spiel für dich ausfüllt, setzt es, falls deine Änderung sie leer gelassen hat: `0` in `ResourceCost`, `None` in `Associated Task` von `BuildingComponents`. Jede andere leere Zelle bleibt für die Prüfung leer.
4. Es prüft die ganze Zeile gegen die Regeln der Tabelle (Werttypen, erlaubte Bereiche, Verweise auf andere Tabellen, siehe [CSV-Tabellen](csv.md)).
5. Nur wenn alles passt, schreibt es die Zeile in die Tabelle. Sonst schreibt es nichts, protokolliert den Grund und macht mit dem nächsten Befehl weiter.

Ein abgelehnter Befehl hinterlässt also nie eine halb geänderte Zeile, und ein fehlerhafter Befehl hält die anderen nicht auf.

## Die drei Befehle { #the-three-commands }

### `Replace`: Zellen einer bestehenden Zeile ändern { #replace-change-cells-of-an-existing-row }

```json
{ "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350, "Movement Speed": 7 } }
```

- Ändert nur die Spalten, die in `Cells` stehen. Alle anderen Zellen behalten ihren aktuellen Wert.
- Eine Zelle mit `""`, nur Leerzeichen oder `null` wird geleert. Das ist nur in einer Spalte erlaubt, in der das Spiel schon selbst irgendeine Zeile leer lässt; sonst wird der Befehl abgelehnt. Nur `ResourceCost`-Zellen (sie werden zu `0`) und `Associated Task` (wird zu `None`) werden stattdessen ausgefüllt.
- Die Zeile muss schon existieren. Sonst: `'...' is not a built-in row; use Add to create one`.
- Jeder Schlüssel in `Cells` muss eine Spalte der Tabelle sein, exakt geschrieben. Sonst listet die Meldung die Spalten der Tabelle auf.
- Geprüft wird die ganze resultierende Zeile, nicht nur die Zellen, die du genannt hast. Eine Zeile, die vorher in Ordnung war, bleibt es, solange deine Werte keine Regel brechen.
- Einige eingebaute Zeilen erstrecken sich in der Tabelle des Spiels über mehrere Zeilen. Sie werden abgelehnt, egal ob du sie Zelle für Zelle änderst oder als ganze Zeile mitlieferst. Nur in `ResourceCost` hilft eine `<Table>.csv` mit der ganzen Zeile (siehe [Zeilen, die mehrere Zeilen belegen](csv.md#rows-that-take-up-several-lines)); die mehrzeiligen Zeilen von `MoraleInfluenceValues` und `TaskValues` lassen sich überhaupt nicht ändern.

### `Add`: eine neue Zeile anlegen { #add-create-a-new-row }

```json
{ "Command": "Add", "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } }
```

- Nur in den Tabellen, die neue Zeilen erlauben (siehe [CSV-Tabellen](csv.md)). Anderswo: `new rows are not supported in '...'; only built-in rows can be changed`.
- Die Id darf noch nicht existieren. Sonst: `'...' already exists; use Replace to change it`.
- Spalten, die du weglässt, bekommen den Standardwert der Tabelle oder bleiben leer; die Zeilenprüfung entscheidet dann, ob das in Ordnung ist.

### `Remove`: Zellen leeren oder eine Zeile löschen { #remove-clear-cells-or-delete-a-row }

```json
{ "Command": "Remove", "Id": "Chair", "Columns": [ "Tarp" ] }
{ "Command": "Remove", "Id": "Drawer" }
```

- Mit `Columns`: leert die aufgelisteten Zellen, genau wie ein `Replace` mit leeren Werten.
- Ohne `Columns`: löscht die ganze Zeile. Nur in den Tabellen, die das erlauben; anderswo sagt das Log, dass die Zeilen nicht entfernt werden können, weil Spielstände und andere Inhalte ihre Ids verwenden.
- `Remove` nimmt nie `Cells`.

## Reihenfolge { #order }

- Innerhalb einer Datei laufen die Befehle von oben nach unten. Auf ein `Add` kann ein `Replace` derselben Zeile folgen.
- Innerhalb einer Mod werden alle `.csv`-Dateien vor allen `.json`-Dateien angewendet, sodass Befehle Zeilen verfeinern können, die deine CSV-Dateien mitgebracht haben.
- Zwischen Mods arbeitet die später angewendete Mod auf dem Ergebnis der früheren und gewinnt, wo beide dieselbe Zelle anfassen. Die Reihenfolge ist unter [So funktionieren Mods](../basics/mods.md) beschrieben.

## Wann Änderungen wirken { #when-changes-take-effect }

Die Tabellen werden bei jedem Laden eines Levels aus den Daten des Spiels und allen aktivierten Mods neu aufgebaut. Nachdem du eine Befehlsdatei bearbeitet hast, speichere dein Spiel, wähle **Einstellungen (Options) → Quit to main menu** und lade den Spielstand erneut. Ein Neustart ist nicht nötig; im Zweifel starte trotzdem neu. Siehe [Testen und Neuladen](../basics/testing.md). Einen ganz neuen `CSV/`-Ordner oder eine neue Mod bemerkt das Spiel erst, nachdem du im Hauptmenü **Mods** geöffnet hast (drück **Refresh**) oder das Spiel neu startest.

Weil die Tabellen von Grund auf neu gebaut werden, stellt das Entfernen eines Befehls oder das Abschalten der Mod beim nächsten Laden den ursprünglichen Wert wieder her. Ausnahme sind Flugzeuge, die schon auf deiner Basis stehen: Sie behalten die Gesundheit, Integrität und Treibstoffkapazität, mit der sie gebaut wurden, ein Spielstand mit aktiver Mod behält also ihre Zahlen (siehe [`VehicleData`](csv.md#vehicledata-aircraft)).

## Referenz { #reference }

### Datei { #file }

| Regel | Wert |
|---|---|
| Ort | `Mods/<mod>/CSV/<Table>.json`, direkt in `CSV/` |
| Dateiname | Exakt der Name der Tabelle: `VehicleData.json`, nicht `vehicledata.json` |
| Wurzel | Ein Objekt mit einem Schlüssel, `Commands`, der eine Liste enthält |
| Befehle pro Datei | Höchstens 200. Eine längere Datei wird komplett übersprungen. |
| Syntax | Reines JSON: keine Kommentare, keine abschließenden Kommas |

### Befehlsfelder { #command-fields }

| Feld | Typ | Verwendet von | Hinweise |
|---|---|---|---|
| `Command` | Text | alle | `Add`, `Replace` oder `Remove`, beliebige Groß- und Kleinschreibung. |
| `Id` | Text | alle | Die Zeilen-Id, beliebige Groß- und Kleinschreibung. Pflicht. |
| `Cells` | Objekt: Spaltenname zu Wert | `Add`, `Replace` | Für diese beiden Pflicht. Werte dürfen Strings, Zahlen oder `true`/`false` sein; sie werden als Text gelesen. |
| `Columns` | Liste von Spaltennamen | `Remove` | Optional. Ohne sie wird die ganze Zeile entfernt. |

### Log-Meldungen { #log-messages }

Jede Meldung beginnt mit `[Mod <mod id>] CSV/<Table>.json`. Angewendete Befehle:

```text
[Mod my_balance_mod] CSV/VehicleData.json command 1 replaced cells Fuel Capacity of row 'gladiator'.
[Mod my_balance_mod] CSV/ResourceCost.json command 2 added row 'storage_box'.
[Mod my_balance_mod] CSV/ResourceCost.json command 3 cleared cells Tarp of row 'Chair'.
[Mod my_balance_mod] CSV/PropsInfluence.json command 4 removed row 'Drawer'.
```

Probleme mit der ganzen Datei (nichts davon wird angewendet):

| Meldung endet mit | Bedeutung |
|---|---|
| `skipped: could not be parsed (...)` | Kein gültiges JSON. Der Teil in Klammern zeigt auf die Stelle. |
| `skipped: it holds no "Commands".` | Der Wurzelschlüssel fehlt, ist falsch geschrieben, oder die Liste ist leer. |
| `skipped: 250 commands exceed the limit of 200.` | Verteile die Befehle auf mehrere Mods oder nimm eine `<Table>.csv`. |
| `skipped: ...` (andere Gründe) | Der Dateiname ist keine Tabelle, die Mods ändern dürfen. |

Probleme mit einem Befehl (nur dieser Befehl wird übersprungen):

| Meldung endet mit | Bedeutung |
|---|---|
| `rejected: it is empty.` | Ein `null` in der Liste `Commands`. |
| `rejected: '...' is not a command; use Add, Replace or Remove.` | `Command` falsch geschrieben. |
| `rejected: it has no "Id".` | `Id` fehlt oder ist leer. |
| `rejected: Replace needs "Cells".` / `Add needs "Cells".` | `Cells` fehlt oder ist leer. |
| `rejected: Remove lists the cells to clear in "Columns", not in "Cells".` | Nimm bei `Remove` das Feld `Columns`. |
| `rejected: '...' is not a column of ...; available: ...` | Spaltenname falsch geschrieben. Kopier ihn aus der Liste in der Meldung. |
| `rejected: '...' is not a built-in row ...` | Keine Zeile mit dieser Id. |
| `rejected: '...' already exists; use Replace to change it.` | `Add` mit einer Id, die schon existiert. |
| `rejected:` gefolgt von einer Regel | Der Wert bricht eine der Regeln der Tabelle, siehe [CSV-Tabellen](csv.md). |

Das veröffentlichte Spiel schreibt nur Fehler in `Player.log`; die vollständige Liste der Zeilen erscheint in einem Entwickler-Build oder im Unity-Editor.
