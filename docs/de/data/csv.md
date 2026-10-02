# CSV-Tabellen

Die meisten Zahlen, die Ground of Aces antreiben - was ein Gebäude kostet, wie schnell ein Flugzeug fliegt, wie sehr eine Mahlzeit die Laune eines Crewmitglieds hebt - stehen in Datentabellen. Eine Mod kann jede davon ändern, ohne den Code des Spiels anzufassen: Du legst einfach eine kleine Datei in ihren Ordner.

Diese Seite ist die vollständige Referenz: wohin die Dateien gehören, wie die beiden Dateiformate aussehen, was das Spiel prüft, bevor es einen Wert annimmt, und was jede Tabelle und jede Spalte bedeutet. Jeder Tabellenabschnitt unter [Die Tabellen](#the-tables) beginnt mit einem Link zur eingebauten Datei, sodass du das Original öffnen oder speichern und seine Kopfzeile kopieren kannst.

!!! note
    Nichts hiervon kann dein Spiel dauerhaft beschädigen. Einen Wert, mit dem das Spiel nichts anfangen kann, lehnt es ab und schreibt den Grund ins [Log](../start/troubleshooting.md#find-the-playerlog); der eingebaute Wert bleibt. Wenn du den Mod-Ordner entfernst, ist alles wieder wie vorher.

!!! tip
    Die `<Table>.json`-Befehlsdateien für einzelne Zellen werden Schritt für Schritt und mit mehr Beispielen unter [Tabellen-Befehlsdateien](table-editor.md) erklärt.

Eine Mod ist ein Ordner in deinem `Mods`-Ordner, und die Datentabellen kommen in dessen Unterordner `CSV/`:

```text
Mods/
  my_balance_mod/
    config.json          optional
    CSV/
      VehicleData.csv    whole rows
      Variables.json     single cells
```

Wo der `Mods`-Ordner liegt, was in `config.json` stehen darf und in welcher Reihenfolge mehrere Mods angewendet werden, wird einmal zentral unter [So funktionieren Mods](../basics/mods.md) erklärt. Der Ordner selbst darf beliebig heißen. Die eine Regel, die hier zählt: Wenn du der Mod in `config.json` eine `Id` gibst, muss sie 3–64 Zeichen lang sein und aus Kleinbuchstaben, Ziffern, `_`, `.` oder `-` bestehen, beginnend mit einem Buchstaben oder einer Ziffer. Alles andere wird ohne Meldung ignoriert, und stattdessen wird der Ordnername in Kleinbuchstaben verwendet.

Gelesen werden nur Dateien direkt in `CSV/` - Unterordner werden ignoriert.

## Deine erste Mod { #your-first-mod }

Die Holzwand soll eine Planke statt zwei kosten. Leg `Mods/my_balance_mod/CSV/ResourceCost.json` mit diesem Inhalt an:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } }
  ]
}
```

Starte das Spiel, lade ein Level, und die Wand kostet eine Planke. Das ist schon die ganze Mod - kein Manifest, keine Registrierung.

## Die beiden Dateiformate { #the-two-file-formats }

Eine Datei ist nach der Tabelle benannt, die sie ändert, und zwar **exakt**, inklusive Großbuchstaben: `VehicleData.csv`, niemals `vehicledata.csv`. Eine Datei, deren Name keine existierende Tabelle ist, wird übersprungen, und das [Log](../start/troubleshooting.md#find-the-playerlog) sagt dir das.

Du kannst eines der beiden Formate verwenden oder beide. Innerhalb einer Mod werden zuerst die `.csv`-Dateien angewendet und danach die `.json`-Dateien, sodass ein Befehl eine Zeile verfeinern kann, die eine CSV-Datei hinzugefügt hat.

### Einzelne Zellen - `<Table>.json` { #single-cells-json }

Eine Liste von Befehlen, die von oben nach unten ausgeführt wird. Zu diesem Format solltest du greifen: Es ändert nur die Werte, die du nennst, und lässt alles andere in Ruhe.

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "gladiator", "Cells": { "Fuel Capacity": 350, "Movement Speed": 7 } },
    { "Command": "Add",     "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } },
    { "Command": "Remove",  "Id": "Chair", "Columns": [ "Tarp" ] },
    { "Command": "Remove",  "Id": "Drawer" }
  ]
}
```

| Befehl | Felder | Was er macht |
|---|---|---|
| `Replace` | `Id`, `Cells` | Ändert nur die aufgelisteten Zellen einer bestehenden Zeile. Alles andere behält seinen Wert. |
| `Add` | `Id`, `Cells` | Fügt eine neue Zeile hinzu. Nur in `ResourceCost` und `PropsInfluence` möglich (siehe [Zeilen hinzufügen und entfernen](#adding-and-removing-rows)). |
| `Remove` mit `Columns` | `Id`, `Columns` | Leert die aufgelisteten Zellen einer Zeile. |
| `Remove` ohne `Columns` | `Id` | Entfernt die ganze Zeile. Nur in `ResourceCost` und `PropsInfluence`. |

Regeln des Formats:

- Reines JSON - keine Kommentare, keine abschließenden Kommas.
- Bei `Command` und `Id` ist die Groß- und Kleinschreibung egal. Die Schlüssel in `Cells` und die Einträge in `Columns` sind Spaltenüberschriften und müssen **exakt** passen, inklusive Leerzeichen.
- Werte dürfen als JSON-Strings, Zahlen oder Booleans geschrieben werden - `300`, `1.5`, `true` und `"300"` funktionieren alle.
- Ein leerer String, ein String nur aus Leerzeichen oder `null` in `Cells` leert diese Zelle, genauso als würdest du sie in einem `Remove` unter `Columns` aufführen.
- `Remove` nimmt kein `Cells`; liste die zu leerenden Zellen in `Columns` auf.
- Höchstens 200 Befehle pro Datei. Eine Datei, die sich nicht lesen lässt oder kein `Commands` hat, wird komplett übersprungen.
- Jeder Befehl wird für sich beurteilt - ein fehlerhafter wird mit einer Warnung übersprungen, der Rest gilt trotzdem.

### Ganze Zeilen - `<Table>.csv` { #whole-rows-csv }

Eine Tabellendatei mit vollständigen Zeilen. Nimm sie, wenn du eine Tabelle lieber in einem Tabellenkalkulationsprogramm bearbeitest und die fertigen Zeilen mitlieferst.

```text
Name,Value
TurboTimeScaleMultiplier,20
RandomActionChatProbability,0.6
```

- Die Kopfzeile muss **exakt** die Spalten der Tabelle aufführen: zuerst die Id-Spalte, dann jede Wertspalte, in beliebiger Reihenfolge, keine fehlt und keine zu viel. Die Überschrift der Id-Spalte selbst wird ignoriert, also müssen nur die Wertspalten passen.
- Nimm nur die Zeilen auf, die du ändern willst - eine Datei muss nicht die ganze Tabelle abdecken.
- Eine Zeile, deren Id zu einer eingebauten Zeile passt, ersetzt diese Zeile vollständig. Bei Ids ist die Groß- und Kleinschreibung egal.
- Gib jeder Zeile genauso viele Zellen wie der Kopfzeile. Eine zu kurze Zeile macht die Datei unlesbar, und die ganze Datei wird übersprungen; zusätzliche Zellen hinter der Kopfzeile werden stillschweigend ignoriert.
- Eine Zelle, die ein Komma enthält, muss in Anführungszeichen stehen, so wie es ein Tabellenkalkulationsprogramm macht: `"Sleep,Chill"`. Ein Zeilenumbruch innerhalb einer Zelle in Anführungszeichen wird nicht unterstützt - er beendet die Zeile.
- Höchstens 200 Zeilen pro Datei. Komplett leere Zeilen und Zeilen, die mit `#` beginnen, werden ignoriert, du kannst also Notizen hinterlassen. Eine Zeile, die mit einer leeren Id-Zelle beginnt, aber weitere Zellen hat, wird als Fortsetzung der Zeile darüber gelesen, und diese Zeile wird dann abgelehnt, weil sie sich über mehrere Zeilen erstreckt.
- Dieselbe Id auf zwei getrennten Zeilen macht die Datei unlesbar; auf zwei benachbarten Zeilen wird sie als eine Zeile behandelt und abgelehnt.
- Jede Zeile wird für sich beurteilt - eine fehlerhafte wird übersprungen und die eingebaute Zeile bleibt.

## Regeln, die überall gelten { #rules-that-apply-everywhere }

### Spalten nehmen nur die Art von Wert, die sie schon enthalten { #columns-only-take-the-kind-of-value-they-already-hold }

Eine Spalte, die in jeder eingebauten Zeile Zahlen enthält, nimmt nur Zahlen; eine mit `TRUE`/`FALSE` nimmt nur diese. `Movement Speed = fast` wird abgelehnt. Textspalten sind freier, aber die meisten haben trotzdem eine eigene Regel - die Tabellen weiter unten sagen dir, welche Werte jede Spalte akzeptiert.

### Leere Zellen { #empty-cells }

Eine Zelle darf nur in einer Spalte leer bleiben, in der das Spiel schon selbst irgendeine Zeile leer lässt. Überall sonst wird das Leeren einer Zelle abgelehnt, weil das Spiel dort keinen Fall "kein Wert" kennt.

Zwei Spalten sind besonders und werden für dich ausgefüllt, statt leer zu bleiben:

- Jede `ResourceCost`-Zelle, die du weglässt, leerst oder auf `""` setzt, wird zu `0`. Ein `Add` braucht also nur die Ressourcen, die wirklich etwas kosten.
- `Associated Task` in `BuildingComponents` wird zu `None`, was bedeutet "dieses Objekt vergibt keine Aufgabe".

### Zeilen hinzufügen und entfernen { #adding-and-removing-rows }

Normalerweise änderst du Zellen von Zeilen, die schon existieren. Ganze Zeilen lassen sich nur in zwei Tabellen hinzufügen oder entfernen, weil das Spiel und deine Spielstände überall sonst eine feste Menge an Ids erwarten:

| Tabelle | Zeilen können hinzugefügt oder entfernt werden |
|---|---|
| `ResourceCost` | ja, für jede eingebaute Objekt- oder Flugzeug-Id |
| `PropsInfluence` | ja, für jede eingebaute Objekt- oder Flugzeug-Id |
| jede andere Tabelle | nein |

Eine hinzugefügte Zeile muss eine Id verwenden, die es schon als Bauobjekt oder Flugzeug gibt - du gibst einem vorhandenen Ding Baukosten oder einen Stimmungseffekt, den es vorher nicht hatte, du erfindest kein neues Ding.

### Zeilen, die mehrere Zeilen belegen { #rows-that-take-up-several-lines }

Einige Tabellen verteilen eine Zeile auf mehrere Zeilen, weil diese Zeile eine Liste enthält - eine Aufgabe mit mehreren Einstellungen, ein Stimmungseffekt mit einer Variante pro Bettart. Eine einzelne Mod-Zeile kann keine Liste ausdrücken, deshalb werden solche Zeilen abgelehnt. Die Tabellenabschnitte weiter unten nennen sie.

Nur in `ResourceCost` tragen einige Zeilen eine übrig gebliebene Überschrift in ihrer `Money`-Zelle und zählen deshalb als mehrere Zeilen. Dort hilft eine CSV mit der ganzen Zeile: Sie schreibt jede Zelle neu und räumt die Zeile dabei gleich auf. Betroffen sind die Ids `KickstarterCustomMonument`, `RadioTower`, `window_wood`, `window_tent`, `window_brick`, `window_hangar`, `window_concrete`, `Distillery`, `ParkingLarge` und `gravel`.

## Nachsehen, was passiert ist { #checking-what-happened }

Jede angenommene Änderung und jede Ablehnung ist eine Zeile im [Log](../start/troubleshooting.md#find-the-playerlog) des Spiels, `Player.log`. Unter Windows gibt es im selben Ordner auch eine HTML-Version, die sich leichter lesen lässt. Die Kennung am Anfang jeder Zeile ist die Id der Mod.

```text
[Mod my_balance_mod] CSV/ResourceCost.json command 1 replaced cells Planks of row 'wall_wood'.
[Mod my_balance_mod] CSV/VehicleData.csv overrides built-in row 'gladiator'.
[Mod my_balance_mod] CSV/PropsInfluence.json command 4 removed row 'Drawer'.
```

Eine Ablehnung nennt die Datei, die Zeilen- oder Befehlsnummer und den Grund:

```text
[Mod my_balance_mod] CSV/VehicleData.json command 3 rejected: 'Fight Power' exceeds 2x the highest built-in value (60).
[Mod my_balance_mod] CSV/AirBaseData.json command 1 rejected: 'Missions Per Week' holds numbers in every built-in row; 'seven' is not one.
```

!!! note
    Diese Zeilen werden als Informationen und Warnungen geschrieben. Das veröffentlichte Spiel schreibt nur Fehler in sein [Log](../start/troubleshooting.md#find-the-playerlog), du siehst sie also nur in einem Entwickler-Build oder im Unity-Editor. Im veröffentlichten Spiel prüfst du stattdessen die Wirkung im Spiel - lade ein Level und schau dir den geänderten Wert an.

Ein falsch geschriebener Tabellenname oder eine nicht passende Kopfzeile erzeugt trotzdem eine `skipped:`-Zeile mit dem Dateinamen. **Wenn du gar keine `[Mod ...]`-Zeilen siehst und die Änderung nicht auftaucht**, hat das Spiel die Mod nicht erkannt: Der `CSV/`-Ordner war beim Spielstart noch leer (drück **Refresh** im Mods-Fenster), die Mod ist im Mods-Fenster ausgeschaltet, oder der Mod-Ordner ist ein symbolischer Link oder eine Junction, denen das Spiel nie folgt.

### Die Spaltenüberschriften einer Tabelle finden { #finding-a-tables-column-headers }

Das Spiel liefert Kopfzeilen-Vorlagen für vier Tabellen (`BuildingComponents`, `PropsInfluence`, `ResourceCost` und `VehicleData`) in `Ground Of Aces_Data/StreamingAssets/Modding/Templates/` im Installationsordner mit (unter macOS: `Ground of Aces.app/Contents/Resources/Data/StreamingAssets/Modding/Templates/`). Für den Rest steht die Spaltenliste auf dieser Seite, und jeder Tabellenabschnitt verlinkt die eingebaute Datei. Oder frag das Spiel: Schreib absichtlich eine falsche Kopfzeile, lade einmal, und das [Log](../start/troubleshooting.md#find-the-playerlog) gibt die erwarteten Spalten aus.

## Ladereihenfolge { #load-order }

Mods werden in der Reihenfolge angewendet, die unter [Welche Mod gewinnt](../basics/mods.md#which-mod-wins) beschrieben ist - zuerst Workshop, dann deine eigenen, niedrigere `LoadOrder` zuerst. Wenn zwei Mods dieselbe Zeile ändern, gewinnt die spätere bei den Zellen, die sie anfasst: Eine CSV mit der ganzen Zeile ersetzt alles, was eine frühere Mod an dieser Zeile gemacht hat, ein `Replace` nur die Zellen, die es nennt. Eine im Mods-Fenster ausgeschaltete Mod trägt nichts bei.

## Wann Änderungen wirken { #when-changes-take-effect }

CSV-Tabellen werden bei jedem Laden eines Levels neu aufgebaut - geh zurück ins Hauptmenü (Main Menu) und lade erneut. Dasselbe passiert, wenn sich das Hauptmenü oder der Karteneditor öffnet. Bearbeitest du eine Datei, während ein Level läuft, erscheint die Änderung beim nächsten Laden, du kannst also Werte ausprobieren, ohne neu zu starten. Eine Datei, die du in einem Tabellenkalkulationsprogramm offen hast, wird trotzdem gelesen.

Ein ganz neuer Mod-Ordner, ein `CSV/`-Ordner, der beim Spielstart noch leer war, oder eine geänderte `config.json` erfordern, dass das Spiel die Mod-Liste neu einliest: Drück **Refresh** im Mods-Fenster (Hauptmenü → Mods) und lade dann ein Level, oder starte das Spiel neu.

## Die Tabellen { #the-tables }

Dreißig Tabellen lassen sich modden. Drei Dateien, die es im Spiel gibt, die aber nicht geladen werden - `ResourceDegradation`,
`StartTimeValues` und `StateInfluence` - lassen sich nicht modden.

Jeder Abschnitt listet die Spalten auf, welche Werte sie nehmen und was die eingebauten Zeilen verwenden. Wo eine Spalte keine
besondere Regel hat, gelten nur die allgemeinen Regeln von oben.

Die eingebauten Werte sind immer vollständig, nie nur eine Auswahl:

- `a–b` ist der volle Bereich: der niedrigste und der höchste Wert, den irgendeine eingebaute Zeile verwendet.
- Eine mit "oder" verbundene Liste enthält jeden verschiedenen Wert, den die eingebauten Zeilen verwenden.
- Eine mit "pro Zeile" markierte Liste nennt den Wert jeder Zeile, in der Reihenfolge, in der die Zeilen in der Datei stehen.
- "in jeder Zeile" bedeutet, dass alle eingebauten Zeilen genau diesen einen Wert haben.
- Bei einer `min-max`-Spalte bekommt jede Hälfte ihren eigenen Bereich: "min 0–43, max 0–60" bedeutet, dass die erste Zahl
  über die Zeilen von 0 bis 43 reicht und die zweite von 0 bis 60.
- Eine leere Eingebaut-Zelle bedeutet, dass die eingebauten Zeilen jeden Wert verwenden, der unter Wert aufgeführt ist.

### Flugzeuge und Basis { #aircraft-and-base }

#### `VehicleData` - Flugzeuge { #vehicledata-aircraft }

Eingebaute Datei: [VehicleData.csv](../assets/csv/VehicleData.csv)

Eine Zeile pro Flugzeug. Zeilen können nicht hinzugefügt oder entfernt werden.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Name` | Lokalisierungsschlüssel | `airplane/<Zeilen-Id>` in jeder Zeile, z. B. `airplane/spitfire` | darf nicht leer sein |
| `Type` | `Fighter`, `Bomber`, `MultiRole`, `Special` | | |
| `Crew` | Kommaliste der Sitze; wiederhole eine Rolle für zwei Sitze | 1–8 Sitze, von `Pilot` allein bis `Pilot,Pilot,BombAimer,Navigator,FlightEngineer,RadioOperator,Gunner,Gunner`; jede Zeile beginnt mit `Pilot`, und alle sechs Rollen kommen vor | in einer CSV-Datei setzt du eine Zelle mit mehr als einem Sitz in Anführungszeichen: `"Pilot,Gunner,Navigator"`. Rollen: `Pilot`, `Gunner`, `Navigator`, `BombAimer`, `FlightEngineer`, `RadioOperator` |
| `Runway Tier` | ganze Zahl | 1–5 | über 5 kann keine Startbahn es bedienen |
| `Parking Size` | ganze Zahl | 0–2 | über 2 kann es nie parken |
| `Victory Points Cost` | ganze Zahl | 0–12 | 0 macht es kostenlos |
| `Movement Speed` | ganze Zahl | 5 in jeder Zeile | Rollgeschwindigkeit; bei 0 erreicht es nie die Startbahn |
| `Landing Length` | ganze Zahl | 60–170 | länger als jede baubare Bahn, und es kann nie landen |
| `Health` | ganze Zahl | 100 in jeder Zeile | |
| `Initial Integrity` | ganze Zahl | 1000 in jeder Zeile | Stunden Verschleiß, die das Flugzeug aushält, bevor es verbraucht ist (1000 h ≈ 41 Tage) |
| `Fuel Capacity` | ganze Zahl | 200–1260 | |
| `Voxel Size` | `AxBxC` | `10x0x10` in jeder Zeile | |
| `Fight Power` | `min-max` | min 0–43, max 0–60 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Bomb Power` | `min-max` | min 0–50, max 0–80 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Recon Power` | `min-max` | min 5–42, max 10–60 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Manoeuvrability` | `min-max` | min 2–28, max 8–50 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Transport Capacity` | `min-max` | min 1–60, max 5–90 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Stealthiness` | `min-max` | min 10–88, max 48–98 | `0 ≤ min ≤ max`, und `max` höchstens **doppelt so hoch wie der höchste eingebaute Wert** |
| `Wreck Resource Type` | `/`-Liste von Ressourcen | `Metal/RepairParts` in jeder Zeile | beide Wrack-Spalten gesetzt oder beide leer |
| `Wreck Resource Amount` | `/`-Liste ganzer Zahlen | `10/5` in jeder Zeile | eine Menge pro Eintrag in `Wreck Resource Type`, in der dort aufgeführten Reihenfolge |
| `Low Caliber Ammo Capacity` | ganze Zahl | 0–3300 | mitgeführte `GunAmmo`; 0 = keine |
| `High Caliber Ammo Capacity` | ganze Zahl | 0–300 | mitgeführte `AntiAirAmmo`; 0 = keine |
| `Plane Bombs Capacity` | ganze Zahl | 0–32 | mitgeführte `PlaneBombs`; 0 = keine |

!!! warning
    Ein Flugzeug, das schon auf deiner Basis steht, behält die Gesundheit, Integrität und Treibstoffkapazität, mit der es gebaut wurde.
    Nur neu gelieferte Flugzeuge übernehmen geänderte Werte - ein Spielstand, der mit aktiver Mod gespeichert wurde, behält also
    die Zahlen dieser Mod, auch nachdem du sie entfernt hast.

#### `AirBaseData` - die Rangleiter des HQ { #airbasedata-the-hq-rank-ladder }

Eingebaute Datei: [AirBaseData.csv](../assets/csv/AirBaseData.csv)

Zeilen `1`–`6`, eine pro Basiskategorie. Alle sechs müssen existieren, und ihre Ids können nicht geändert werden.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Airstrip Tier` | ganze Zahl | pro Zeile: 1, 2, 3, 4, 5, 5 | nötig, um den Rang zu erreichen |
| `Minimum Airstrip Count` | ganze Zahl | 1–5 | |
| `Minimum Parking Count` | ganze Zahl | 1–20 | |
| `Missions Per Week` | ganze Zahl | 6–18 | Plätze, die die Woche anbietet; bei 0 werden keine Missionen geplant |
| `Minimum Missions Per Week` | ganze Zahl | 2–10 | die wöchentliche HQ-Quote: wie viele Missionen die Basis jede Woche bis zu einem Ergebnis fliegen muss. Gewonnene und verlorene Missionen zählen, abgebrochene und gescheiterte historische Missionen nicht. Verfehlst du diesen Wert oder `Minimum Success Rate`, halbieren sich die Plätze der nächsten Lieferung (aufgerundet), und bei der normalen Einstellung für HQ-Verwarnungen gibt es eine Verwarnung - drei verfehlte Wochen in Folge beenden den Durchgang. Trainingswochen und die HQ-Einstellung "keine Anforderungen" überspringen die Prüfung. Über `Missions Per Week` ist die Quote unerfüllbar |
| `Minimum Success Rate` | Bruchteil, kein Prozentwert | 0.4–0.8 | Anteil der von `Minimum Missions Per Week` gezählten Missionen, der gewonnen werden muss; über 1 ist unerreichbar |
| `Available Shipment Slots` | ganze Zahl | 4–8 | 0 schaltet den Nachschub ab |

#### `AirstripTiers`

Eingebaute Datei: [AirstripTiers.csv](../assets/csv/AirstripTiers.csv)

Zeilen `1`–`5`.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Length` | ganze Zahl | pro Zeile: 80, 120, 140, 160, 200 | Stufen gelten nach "Länge oder mehr", halte sie also aufsteigend |
| `Width` | ganze Zahl | pro Zeile: 12, 14, 18, 22, 26 | Stufen gelten nach "Breite oder mehr", halte sie also aufsteigend |
| `Material` | Text | pro Zeile: `dirt`, `sand`, `gravel`, `concrete`, `tarmac` | **darf das Material einer anderen Stufe nicht wiederholen** und muss eine vorhandene `ResourceCost`-Zeile nennen - diese Zeile bestimmt, was jede Kachel dieser Startbahn kostet. `ResourceCost` nimmt keine neuen Belagszeilen an, bleib also in der Praxis bei `dirt`, `sand`, `gravel`, `concrete` und `tarmac` (sie zwischen den Stufen zu tauschen, ist in Ordnung). Ein Material ohne `ResourceCost`-Zeile wird hier angenommen, und dann schlägt das Verlegen einer Startbahn dieser Stufe mit einem Fehler fehl |
| `Biome Id` | ganze Zahl | pro Zeile: 6, 20, 22, 15, 13 | Boden, der unter die fertige Bahn gemalt wird |
| `Build Time` | ganze Zahl | pro Zeile: 5, 2, 2, 2, 2 | Spielminuten Arbeit pro Kachel. An jeder Kachel arbeitet immer nur ein Crewmitglied, mehr Crew verlegt also mehr Kacheln gleichzeitig, aber keine Kachel schneller |

#### `Biomes`

Eingebaute Datei: [Biomes.csv](../assets/csv/Biomes.csv)

Zeilen `0`–`23`, die Bodenarten. Alle Spalten sind Zahlen, daher lässt sich diese Tabelle gefahrlos anpassen.

| Spalte | Eingebaut | Hinweise |
|---|---|---|
| `Airstrip Tier` | 0–5 | Stufe, als die eine Startbahn auf diesem Boden zählt |
| `Character Speed Modifier` | 1–1.2 | 0 friert jeden ein, der darauf steht |
| `Airplane Speed Modifier` | 0.5–1.2 | |
| `Degradation Penalty` | 0–0.2 | zusätzlicher Verschleiß für hier gelagerte Güter |
| `Fire Spread Modifier` | 0.5 oder 1 | |

#### `ScrambleData` - feindliche Flugzeuge beim Alarmstart { #scrambledata-enemy-aircraft-in-a-scramble }

Eingebaute Datei: [ScrambleData.csv](../assets/csv/ScrambleData.csv)

Zeilen `Fighter`, `Diver`, `Bomber`. Die Namen können nicht geändert werden. Alle Spalten sind ganze Zahlen.

| Spalte | Eingebaut | Hinweise |
|---|---|---|
| `PlaneHealth` | pro Zeile: 18, 26, 34 | |
| `PlanePower` | pro Zeile: 23, 17, 14 | |
| `PlaneWinDealDamageMin` | pro Zeile: 20, 20, 15 | Schaden an deinem Flugzeug, wenn der Feind gewinnt |
| `PlaneWinDealDamageMax` | pro Zeile: 120, 70, 50 | |
| `PlaneLooseDealDamageMin` | pro Zeile: 10, 5, 5 | Schaden an deinem Flugzeug, wenn der Feind verliert |
| `PlaneLooseDealDamageMax` | pro Zeile: 25, 20, 15 | |

#### `AttacksComposition` - woraus ein Luftangriff besteht { #attackscomposition-what-an-air-raid-is-made-of }

Eingebaute Datei: [AttacksComposition.csv](../assets/csv/AttacksComposition.csv)

Die Zeilen-Id ist die Schwere des Angriffs. Im normalen Spiel werden **1–25** erreicht; die Zeilen `99`, `101`, `200` und `300` erreicht
die normale Schwereleiter nicht, sie sind für besondere Angriffe reserviert. Die Bereiche unten beschreiben die Zeilen 1–25.
Die vier Sonderzeilen verweisen in den letzten beiden Spalten auf sich selbst und enthalten:

| Zeile | `Bombers` | `Divers` | `Fighters` |
|---|---|---|---|
| `99` | `9-9` | `6-6` | `8-8` |
| `200` | `10-10` | `0-0` | `0-0` |
| `300` | `0-0` | `10-10` | `0-0` |
| `101` | `0-0` | `3-3` | `2-2` |

| Spalte | Wert | Eingebaut (Zeilen 1–25) | Hinweise |
|---|---|---|---|
| `Bombers` | `min-max` | min 0–4, max 0–6 | ganze Zahlen, `0 ≤ min ≤ max` |
| `Divers` | `min-max` | min 0–6, max 0–6 | ganze Zahlen, `0 ≤ min ≤ max` |
| `Fighters` | `min-max` | min 1–8, max 2–8 | ganze Zahlen, `0 ≤ min ≤ max` |
| `LowAttacks` | ganze Zahl | 1–14 | Schwere, die stattdessen verwendet wird, wenn die Karte auf leichtere Angriffe eingestellt ist - **muss eine Zeile dieser Tabelle nennen** |
| `HighAttacks` | ganze Zahl | 2–25 | Schwere, wenn die Karte auf härtere Angriffe eingestellt ist - **muss eine Zeile dieser Tabelle nennen** |

#### `EquipmentData` - Flak, Suchscheinwerfer, Türme { #equipmentdata-aa-guns-searchlights-towers }

Eingebaute Datei: [EquipmentData.csv](../assets/csv/EquipmentData.csv)

Die Zeilen sind Ausrüstungs-Ids: `Bofors40mm`, `Searchlight`, `RadioTower`, `VickersGunAA`, `OerlikonGun`, `Lookout`,
`ControlTowerMetal`, `ControlTowerBrick`, `ControlTowerConcrete`.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Range` | Zahl | 10–70 | 0 macht das Teil nutzlos |
| `Damage` | Zahl | 0–6 | `0` macht das Teil zu einer Station, die nicht schießt, wie `Searchlight` oder `Lookout`: Es lässt sich weiterhin platzieren und besetzen, feuert aber nie, und alle Spalten ab `Fire Rate` werden dafür nicht gelesen |
| `Fire Rate` | ganze Zahl | 0–720 | Schuss pro Minute |
| `Ammo Type` | Ressourcenname oder `None` | `GunAmmo`, `AntiAirAmmo`, `None` oder `0` | alles, was kein Ressourcenname ist (`None`, `0`), bedeutet, dass das Teil keine Munition lagert |
| `Ammo Capacity` | ganze Zahl | 0–80 | auf einmal geladene Schuss |
| `Ammo Load Time` | Zahl | 0–6.5 | Sekunden zum Nachladen |
| `Ammo Storage` | ganze Zahl | 0–500 | **`0` bedeutet, dass es nie Munition holt** |
| `Damage Bonus` | Zahl | 0 oder 0.25 | wird anderen in Reichweite gewährt (Suchscheinwerfer) |
| `Firing Angle` | Zahl | 0, 140 oder 360 | `0` wird als Vollkreis gelesen |
| `Aiming Speed` | Zahl | 0–170 | Grad pro Sekunde |
| `Range Bonus` | Zahl | 0 oder 16 | wird anderen in Reichweite gewährt (Ausguck) |
| `Attacker Priority` | `Bombers`, `Divers`, `Fighters`, `Nearest`, `None` | `Bombers`, `Divers`, `Fighters` oder `None`; keine Zeile verwendet `Nearest` | alles andere fällt auf `None` zurück |

### Bauen und Objekte { #building-and-objects }

#### `BuildingComponents` - Objekte und Gebäudeteile { #buildingcomponents-objects-and-building-parts }

Eingebaute Datei: [BuildingComponents.csv](../assets/csv/BuildingComponents.csv)

Eine Zeile pro Objekt, Wandteil, Boden, Dach, Werkbank und Ausrüstungsteil. Zeilen können nicht hinzugefügt oder
entfernt werden.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Dimensions` | `WxHxD`, oder `dynamic/1x0x1` für Dächer | Breite 1–32, Höhe 0–6, Tiefe 1–32 (von `1x0x1` bis `32x1x32`), `dynamic/1x0x1` bei den Dächern, leer in 9 Zeilen (unten aufgeführt) | |
| `Build Time` | ganze Zahl | 0–420 | Spielminuten Arbeit. An einem Objekt baut immer nur ein Crewmitglied; zusätzliche Crew macht es nicht schneller |
| `Health` | ganze Zahl | 0–10000 | der riesige Wert kennzeichnet die unzerstörbaren Teile |
| `Associated Task` | Aufgabenname oder `None` | `None`, `Sleep`, `Chill`, `UseEquipment`, `PlayPiano`, `UseTrainingObject`, `MonitorAirspace`, `UseRadio`, `SaluteTheFlag`, `Grieve`, `ListenToMusic`, `PlayDartboard`, `PlayGuitar`, `PlayBilliardTable` oder `UsePlanningBoard` | ein Objekt auf eine Aufgabe zu setzen, zu der seine Grafik nicht passt, ist erlaubt und sieht falsch aus |
| `Users Limit` | ganze Zahl | 0–5 | 0 bei einem benutzbaren Objekt bedeutet, dass niemand es benutzen kann |
| `Is Wall Deco` | `TRUE`/`FALSE` | | |
| `Is Floor Deco` | `TRUE`/`FALSE` | | |
| `Is Fireproof` | `TRUE`/`FALSE` | | |
| `Placement Requirement` | `None`, `Indoors`, `Outdoors` | | |

!!! note
    Ein `Replace` wird gegen die fertige Zeile geprüft. Eine Zeile, die `Dimensions` oder `Users Limit` leer lässt,
    kannst du also nur ändern, wenn du diese Zelle im selben Befehl mit setzt - oder die Zeile als CSV mitlieferst.
    Leere `Dimensions`: `PropagandaPoster`, `MusicPoster`, `AirplanePoster`, `CompanyMascotPoster`,
    `CurtainsClosed`, `CurtainsOpen`, `EntranceSign`, `tombstone`, `storage_box`.
    Leeres `Users Limit`: die Werkbänke und die drei Parkplatzgrößen.

#### `ResourceCost` - was der Bau von etwas kostet { #resourcecost-what-something-costs-to-build }

Eingebaute Datei: [ResourceCost.csv](../assets/csv/ResourceCost.csv)

Eine Zeile pro Objekt- oder Flugzeug-Id, eine Spalte pro Ressource. **Zeilen können hinzugefügt und entfernt werden.** Eine entfernte Zeile
bedeutet "keine Baukosten". Kosten von `0` bedeuten "nicht benötigt", jede Spalte auf null zu setzen hat also dieselbe Wirkung. Die Id
einer hinzugefügten Zeile muss eine vorhandene `BuildingComponents`- oder `VehicleData`-Id sein; alles andere wird abgelehnt als
"neither a built-in prop nor a built-in plane".

Jede Zelle ist eine ganze Zahl, null oder mehr. Die Spalten sind:

```text
Money  VictoryPoints  Trash  Wood  Clay  Sandbags  Stone  Food  RawWater  Herbs  Metal  Bricks
Planks  Tarp  Cement  Fuel  PurifiedWater  Meals  SimpleMedicine  Intel  Machinery  Electronics
LuxuryGoods  MilitaryConstruction  Camouflage  FoodRations  StrongMedicine  RepairParts  GunAmmo
AntiAirAmmo  PlaneBombs
```

Auch die Startbahnbeläge sind hier Zeilen - `dirt`, `sand`, `gravel`, `concrete`, `tarmac` - wenn du also `gravel` änderst,
änderst du, was eine Startbahn der Stufe 3 pro Kachel kostet. **Entferne keine Belagszeile**: Anders als ein Objekt wird ein Belag
ohne Zeile nicht kostenlos - das Verlegen einer Startbahn dieser Stufe schlägt dann mit einem Fehler fehl. Soll ein Belag nichts kosten,
setz jede Zelle seiner Zeile auf `0`.

#### `PropsInfluence` - der Stimmungseffekt, den ein Objekt ausstrahlt { #propsinfluence-the-mood-effect-an-object-radiates }

Eingebaute Datei: [PropsInfluence.csv](../assets/csv/PropsInfluence.csv)

Eine Zeile pro Objekt, das die Stimmung der Crew in der Nähe hebt oder senkt. **Zeilen können hinzugefügt und entfernt werden**; ein Objekt
ohne Zeile hat einfach keine Wirkung.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Buff Name` | Lokalisierungsschlüssel | ein `prop_effects/<effect>`-Schlüssel in jeder Zeile (31 verschiedene Schlüssel), z. B. `prop_effects/organised_sleep` | darf nicht leer sein |
| `Radius` | Zahl | 0.5–50 | in Kacheln; die Kontrolltürme reichen 20, 30 und 50 weit |
| `Associated Tasks Or Action` | Kommaliste von Aufgabennamen | 1–4 Namen pro Zeile, z. B. `Sleep` oder `"Sleep,Chill"`, aus `AidInjured`, `BoardAirplane`, `BringResources`, `Bury`, `Chill`, `Cook`, `Eat`, `Grieve`, `HarvestGardeningTile`, `Landing`, `Loiter`, `MaintainAirplane`, `PlayGuitar`, `PlayPiano`, `Recover`, `RecoverInBed`, `Repair`, `RepairAirplane`, `Sleep`, `Stockpile`, `UseEquipment`, `UsePlanningBoard`, `UseRadio`, `UseTrainingObject`, `Water` oder `WorkOnWorkbench` | darf nicht leer sein. In einer CSV-Datei setzt du eine Zelle mit mehr als einer Aufgabe in Anführungszeichen: `"Sleep,Chill"`. Ein Name, der zu keiner Aufgabe passt, wird angenommen, und der Effekt **greift einfach nie** |
| `Effect 1` | `<Zahl mit Vorzeichen> <Name>` | `-1 Mood` bis `+3 Mood`, `+1 Energy` bis `+2 Energy`, `+0.5 Confidence` bis `+10 Confidence` oder `-1 Accident` | Namen: `Mood`, `Confidence`, `Energy` |
| `Effect 2` | `<Zahl mit Vorzeichen> <Name>` oder leer | `-1.5 Energy`, `+1 Energy`, `+0.5 Mood`, `+10 Mood` oder `+1 Confidence` in 9 Zeilen; in den übrigen leer | |
| `Effect 3` | `<Zahl mit Vorzeichen> <Name>` oder leer | leer in jeder Zeile | |

Das Vorzeichen gehört zur Zahl, `1 Mood` bedeutet also `+1`. Namen werden locker abgeglichen, `+1 mood` funktioniert also. Ein anderer Name
als die drei oben wird als Spezialeffekt gespeichert (das Spiel verwendet `-1 Accident` bei den drei Kontrolltürmen);
ein erfundener Name wird angenommen und bewirkt nichts.

#### `MapObjects` - Bäume, Felsen, Teiche und andere Rohstoffquellen { #mapobjects-trees-rocks-ponds-and-other-harvestables }

Eingebaute Datei: [MapObjects.csv](../assets/csv/MapObjects.csv)

Eine Zeile pro Weltobjekt. Die Ids werden von Kartendateien verwendet und können nicht geändert werden.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `LocKey_Name` | Lokalisierungsschlüssel | `map.obj.<object>.name` in 20 Zeilen, z. B. `map.obj.tree.name`; `map.obj.<object>` ohne `.name` in den übrigen 13, z. B. `map.obj.crate` | |
| `LocKey_Description` | Lokalisierungsschlüssel | `map.obj.<object>.description` in 18 Zeilen, z. B. `map.obj.tree.description`; `map.obj.<object>` ohne `.description` in den übrigen 15, z. B. `map.obj.crate` | |
| `Dimensions` | `WxHxD` | Breite 1–4, Höhe 1–6, Tiefe 1–6 (von `1x1x1` bis `4x6x4`) | |
| `Resource Harvested` | Ressourcenname oder leer | `Wood`, `Stone`, `Herbs`, `Food`, `RawWater`, `Clay`, `Sandbags`, `Metal`, `Planks`, `Fuel`, `GrainSeeds`, `BeansSeeds`, `PotatoSeeds` oder `TomatoSeeds`; leer in 9 Zeilen | leer bedeutet, dass es nichts zu ernten gibt |
| `Farming Time` | ganze Zahl | 0–400 | Spielminuten Arbeit pro Ernte, immer von einem Crewmitglied zur Zeit |
| `Resource Amount` | ganze Zahl | 0–50 | Ertrag pro Ernte |
| `Resource Total` | ganze Zahl | 0–500 | Gesamtmenge, bevor die Quelle erschöpft ist |
| `Limited Harvest Amount` | ganze Zahl | 0, 20, 30 oder 100 | Obergrenze für endlose Quellen; 0 = unbegrenzt |
| `Destroyed On Depletion` | `TRUE`/`FALSE` | | `FALSE` mit `Refresh Time` 0 hinterlässt etwas, das nie wieder geerntet werden kann |
| `Refresh Time` | ganze Zahl | 0–21600 | Minuten, bis es nachwächst |
| `Health` | ganze Zahl | 1–2147483647 | der riesige Wert kennzeichnet die unzerstörbaren |
| `Is Fireproof` | `TRUE`/`FALSE` | `TRUE` bei den Felsen, Gruben, dem Teich, dem Meer, `WaterPump` und `WaterTower` | `TRUE` macht das Objekt zu einer Brandschneise: Auf den Kacheln, die es belegt, kann Feuer weder entstehen noch sich dorthin ausbreiten. Über den freien Boden drumherum läuft Feuer weiterhin |

#### `GrowingData` - Setzlinge werden zu Bäumen { #growingdata-saplings-becoming-trees }

Eingebaute Datei: [GrowingData.csv](../assets/csv/GrowingData.csv)

Zwei Zeilen, `young_tree` und `young_tree_big`.

| Spalte | Wert | Eingebaut |
|---|---|---|
| `To` | eine `MapObjects`-Id | pro Zeile: `tree`, `tree_big` |
| `Min Hours` | ganze Zahl | 672 in jeder Zeile |
| `Max Hours` | ganze Zahl | 840 in jeder Zeile |

Ein Setzling, der beim Laden eines Spielstands schon auf der Karte steht, würfelt seine Restzeit zwischen der Hälfte von
`Min Hours` und `Max Hours`; nur frisch gepflanzte verwenden das volle Minimum.

#### `GardeningData` - die vier Feldfrüchte { #gardeningdata-the-four-crops }

Eingebaute Datei: [GardeningData.csv](../assets/csv/GardeningData.csv)

Zeilen `grain`, `beans`, `potato`, `tomato`.

| Spalte | Eingebaut | Hinweise |
|---|---|---|
| `Growth` | pro Zeile: 3, 6, 15, 10 | gegossene Tage bis zur Ernte - die Pflanze gewinnt um Mitternacht einen Punkt für jeden Tag, an dem ihre Kachel gegossen wurde; bei 0 ist sie sofort erntereif |
| `Food` | pro Zeile: 3, 4, 20, 7 | `Food` pro abgeernteter Kachel, wenn die Zone auf Anbau für Nahrung eingestellt ist |
| `Seeds` | pro Zeile: 2, 5, 3, 1 | die eigene Saatgut-Ressource der Feldfrucht (`GrainSeeds`, `BeansSeeds`, `PotatoSeeds`, `TomatoSeeds`) pro abgeernteter Kachel, wenn die Zone auf Anbau für Saatgut eingestellt ist; 0 macht die Feldfrucht nicht nachhaltig |
| `Regrowth` | nur `tomato` ist `TRUE` | wächst nach, statt verbraucht zu werden |

### Ressourcen und Herstellung { #resources-and-crafting }

#### `ResourceData` - was eine Ressource ist { #resourcedata-what-a-resource-is }

Eingebaute Datei: [ResourceData.csv](../assets/csv/ResourceData.csv)

Eine Zeile pro Ressource, exakt so benannt, wie das Spiel sie nennt.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Initial Integrity` | ganze Zahl | 0–50000 | Stunden, bevor ein Stapel verdirbt; 0 verrottet sofort |
| `Carry Limit` | ganze Zahl | 0–250 | wie viel eine Person trägt; 0 bedeutet, dass es nie bewegt werden kann |
| `Stack Limit` | ganze Zahl | 0–2000 | Stapelgrenze im Freien |
| `Double Stack Limit` | ganze Zahl | 0–3000 | Stapelgrenze in einem richtigen Lager; unter `Stack Limit` verkleinert es das Lager |
| `Resource Tier` | `Meta`, `Basic`, `Advanced`, `Military`, `Trash` | | |
| `Category` | `Food`, `Seeds` oder leer | | wenn du `Food` bei allem Essbaren entfernst, kann die Crew nie essen |
| `Always Degrades` | `TRUE`/`FALSE` | | verdirbt sogar unter einem Dach |
| `Explosiveness` | ganze Zahl | 0, 2 oder 3 | 0 ist harmlos |
| `Flammable` | `TRUE`/`FALSE` | | |
| `VariantAmountMapping` | `/`-Liste ganzer Zahlen | `1/2` oder `1` | wählt das Aussehen des Stapels |

#### `WorkbenchProjectData` - Herstellungsrezepte { #workbenchprojectdata-crafting-recipes }

Eingebaute Datei: [WorkbenchProjectData.csv](../assets/csv/WorkbenchProjectData.csv)

Die Zeilen-Id ist `<Workbench>.<Output>`. Zeilen können nicht hinzugefügt werden, hiermit änderst du also bestehende Rezepte, statt
neue einzuführen.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Workbench Type` | Werkbankname | `FieldKitchen`, `IndoorKitchen`, `SawStation`, `Brickstation`, `CementMixer`, `MetalworksWorkbench`, `CanningStation`, `ElectronicsWorkbench`, `TailorStation`, `EspionageRadio`, `WaterCooker`, `HerbDryer` oder `Distillery` | |
| `Output Resource Type` | Ressourcenname | `AntiAirAmmo`, `Bricks`, `Camouflage`, `Cement`, `Electronics`, `FoodRations`, `Fuel`, `GunAmmo`, `Intel`, `LuxuryGoods`, `Machinery`, `Meals`, `Metal`, `PlaneBombs`, `Planks`, `PurifiedWater`, `RepairParts`, `SimpleMedicine`, `StrongMedicine` oder `Tarp` | |
| `Output Resource Amount` | ganze Zahl | 1–200 | |
| `Input Resource Type` | `/`-Liste von Ressourcen oder `None` | `None` in 3 Zeilen; sonst 1–3 aus `Clay`, `Electronics`, `Food`, `Herbs`, `LuxuryGoods`, `Machinery`, `Meals`, `Metal`, `PurifiedWater`, `RawWater`, `Sandbags`, `SimpleMedicine`, `Tarp` oder `Wood`, z. B. `Food/RawWater` | `None` bedeutet: aus nichts hergestellt |
| `Input Resource Amount` | `/`-Liste ganzer Zahlen | 1–3 Einträge, jeder 1–10, z. B. `2/2`; `0` in den 3 `None`-Zeilen | **muss genauso viele Einträge haben wie die Typliste** |
| `Time To Craft` | ganze Zahl | 10–180 | Spielminuten Arbeit, immer von einem Crewmitglied zur Zeit |
| `Valid Entry` | `TRUE`/`FALSE` | `TRUE` in jeder Zeile | Überbleibsel; das Spiel liest es nicht |

#### `ShipmentData` - der Nachschubkatalog { #shipmentdata-the-supply-catalogue }

Eingebaute Datei: [ShipmentData.csv](../assets/csv/ShipmentData.csv)

Eine Zeile pro bestellbarem Artikel.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Shipment Type` | `Resource` oder `Prop` | | |
| `Category` | `Military`, `Miscellaneous` oder `Large` | | **Groß- und Kleinschreibung zählt** - `military` wird abgelehnt |
| `Amount` | ganze Zahl | 1–5000 | gelieferte Einheiten pro Platz |
| `Slots` | ganze Zahl | 1–4 | mehr Plätze, als irgendein Rang bietet, machen den Artikel unbestellbar |

### Crew

#### `CharactersInitialStats` - Startfähigkeiten pro Beruf { #charactersinitialstats-starting-skills-per-job }

Eingebaute Datei: [CharactersInitialStats.csv](../assets/csv/CharactersInitialStats.csv)

Die Zeilen sind Berufe und Crewrollen: `Pilot`, `Gunner`, `BombAimer`, `FlightEngineer`, `Navigator`,
`RadioOperator`, `RAFAirCrew`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`, `AAFLabour`, `None`,
`Custom`.

Die Spalten sind die sechs Fähigkeiten - `Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating` - und
der Wert ist ein **Rang von 0 bis 6**, keine Punktzahl. `0` ist Untrained und `6` ist Ace. Bleib innerhalb dieses
Bereichs; die eingebauten Zeilen verwenden 0–2. `Endurance` legt auch die maximale Gesundheit fest, deshalb hat jede Zeile dort mindestens `1`.

#### `CharactersStatsRankProgression` - Punkte pro Rang { #charactersstatsrankprogression-points-per-rank }

Eingebaute Datei: [CharactersStatsRankProgression.csv](../assets/csv/CharactersStatsRankProgression.csv)

Die Zeilen müssen `Untrained`, `Rank1`, `Rank2`, `Rank3`, `Rank4`, `Rank5`, `Ace` bleiben. `LevelUpPoints` (0, 10, 14, 22, 36, 58, 90) ist die
Punktzahl, bei der dieser Rang erreicht wird, und gewählt wird der höchste Rang, den ein Charakter überschritten hat
- also **müssen die Werte aufsteigen**. Außer der Reihe bleibt die Crew niedrig hängen oder springt direkt zu Ace.

#### `CharacterStatsCheck` - was ein Rang wert ist { #characterstatscheck-what-a-rank-is-worth }

Eingebaute Datei: [CharacterStatsCheck.csv](../assets/csv/CharacterStatsCheck.csv)

Die Zeilen sind die sieben Ränge `Untrained`, `Rank1`, `Rank2`, `Rank3`, `Rank4`, `Rank5`, `Ace`. Für jede der sechs Fähigkeiten gibt es zwei Spalten: `<Skill>Value` ist ein fester
Bonus auf einen Missionswurf, `<Skill>Percentage` ist ein **Bruchteil** - `0.25` bedeutet 25 %. Schreibst du `25`, ergibt das
einen Bonus von 2500 %. Die Spaltennamen können nicht umbenannt werden.

#### `CharacterJobPriority` - was jeder Beruf zu tun bereit ist { #characterjobpriority-what-each-job-is-willing-to-do }

Eingebaute Datei: [CharacterJobPriority.csv](../assets/csv/CharacterJobPriority.csv)

Die Zeilen sind die Berufsnamen: `None`, `Custom`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`,
`AAFLabour`, `RAFAircrew`.

Es gibt eine Spalte pro Arbeitsart - `Building`, `Gardening`, `CraftingAndRepairs`, `Labor`, `Cooking`,
`Medicine`, `PlaneWork`, `Harvest`, `BaseSafety`, `Leisure`, `UseRecreationalItem`, `Socialize`,
`ConsumeLuxuryGood`, `Train`, `Sleep`, `PilotPlane`, `FunctionalGroup`, `Emergency` - mit einer Priorität:
`0` bedeutet, dass der Beruf diese Arbeit nie macht, `1` ist die höchste Priorität und `3` die niedrigste. (Ein Sanitäter hat
`Building 0` und `Medicine 1`.) Keine Spalte darf wegfallen oder umbenannt werden.

Diese Zahlen **bestimmen** auch einen Beruf: Ein Crewmitglied, dessen Prioritäten genau zu einer Zeile passen, hat diesen Beruf, und eines,
das zu keiner passt, ist `Custom`. Gibst du zwei Berufen identische Prioritäten, kann das Spiel sie nicht mehr unterscheiden.

#### `CharactersData` - Namen, Spitznamen und Ränge { #charactersdata-names-nicknames-and-ranks }

Eingebaute Datei: [CharactersData.csv](../assets/csv/CharactersData.csv)

Sechs der acht Zeilen sind lange Listen - Vornamen, Nachnamen, Spitznamen, Ränge der Bodencrew, Pilotenränge - und
können nicht geändert werden.

Ändern kannst du die beiden Pilotenränge selbst, wobei `Goal` angibt, wie viele erfolgreiche Missionen die
Beförderung bringen:

| Zeile | `Value` | `Goal` |
|---|---|---|
| `OfficerCadet` | 2 | 3 |
| `PilotOfficer` | 3 | 10 |

#### `MoraleValues`

Eingebaute Datei: [MoraleValues.csv](../assets/csv/MoraleValues.csv)

Name und Wert, alles Zahlen: `BaseMoraleBufferDays`, `MoraleLevelMin` (-100), `MoraleLevelMax` (100),
`LeisureThreshold`, `MoraleTrendTreshold`, `MoraleBreakingThreshold`, `MoraleEffectPositiveThreshold`,
`MoraleEffectNegativeThreshold`, `AirBaseMoraleGameOverThreshold`.

Setzt du `AirBaseMoraleGameOverThreshold` über `MoraleLevelMax`, ist das Spiel sofort verloren; setzt du
`MoraleLevelMin` über `MoraleLevelMax`, sind alle Grenzen vertauscht.

#### `MoraleInfluenceValues` - was die Stimmung eines Crewmitglieds verändert { #moraleinfluencevalues-what-changes-a-crew-members-mood }

Eingebaute Datei: [MoraleInfluenceValues.csv](../assets/csv/MoraleInfluenceValues.csv)

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Itentifier` | Zeilen-Id (beachte die Schreibweise) | `Sleep`, `Eat`, `WorkOnWorkbench`, `Stockpile`, `Build`, `Harvest`, `Chill`, `ConsumeLuxuryGoods`, `UseRadio`, `SaluteTheFlag`, `UsePlanningBoard`, `Panic`, `Rage`, `Collapse`, `Grieve`, `Bury`, `UseTrainingObject`, `Socialize`, `UseRecreationalItem`, `Work`, `Train`, `Early`, `Mid`, `Late`, `Living`, `MissionCancelled`, `MissionCompleted`, `WarNews`, `BaseAttacked`, `Death`, `Recover` oder `RecoverInBed` | |
| `IdentifierType` | `Task`, `TaskGroup`, `TaskCategory`, `WarPhase`, `GameEvent`, `-` | | ein Typ, der nicht zur Id passt, bedeutet, dass die Zeile ignoriert wird |
| `Parameter` | der Variantenschlüssel; Aliase durch Kommas getrennt | `default`; `Prop.Bed`, `Prop.BedMetal`, `Prop.BedWood`, `Prop.BilliardTable`, `Prop.Dartboard`, `Prop.Guitar`, `Prop.Piano`; `ResourceType.Food`, `ResourceType.FoodRations`, `ResourceType.Intel`, `ResourceType.LuxuryGoods`, `ResourceType.Meals`, `ResourceType.PurifiedWater`, `ResourceType.RawWater`; `CharacterClass.AirCrew`, `CharacterClass.BaseCrew`; `InfluenceOutcome.Good`, `InfluenceOutcome.Bad`; und eine Zeile mit zwei Aliasen, `Prop.Jukebox, Prop.Gramophone` | **kein Alias darf doppelt vorkommen** |
| `Raw Parameter` | eine Notiz | | wird vom Spiel nicht gelesen |
| `Confidence` / `Mood` / `Energy` | Zahlen | `Confidence` -10 bis 50, `Mood` -30 bis 50, `Energy` -20 bis 50 | |
| `Influence Type` | `Timed` oder `OnEventTrigger` | | |

`Timed`-Werte wirken bei jedem Tick und sind deshalb viel kleiner als `OnEventTrigger`-Werte. Kopierst du einen Ereigniswert von `+20`
in eine `Timed`-Zeile, klebt die Stimmung eines Crewmitglieds innerhalb einer Minute an der Obergrenze.

Sechs Zeilen enthalten eine Variante pro Zeile und können überhaupt nicht geändert werden: `Sleep`, `Eat`, `WorkOnWorkbench`,
`UseRecreationalItem`, `MissionCompleted`, `Death`.

### Missionen und Zeit { #missions-and-time }

#### `FlightMissionData` - die Missionsmodifikatoren { #flightmissiondata-the-mission-modifiers }

Eingebaute Datei: [FlightMissionData.csv](../assets/csv/FlightMissionData.csv)

Diese Tabelle legt fest, wie sich der Zustand eines Flugzeugs und seiner Crew auf eine Mission auswirkt. Das Spiel prüft jedes
Flugzeug und jedes Crewmitglied gegen diese Zeilen. Liegt ein gemessener Wert innerhalb der `ThresholdRange` einer Zeile, gilt
deren Modifikator für das Flugzeug. Das Missionsbriefing listet jeden davon auf, und sie fließen in die Erfolgsschätzung ein.
Es gibt zwei Arten:

- Ein `SkillRollModifier` verschiebt die Missionswerte des Flugzeugs (Kampf, Bomben, Aufklärung und die übrigen). Seine
  `ModifierRange` wird zum niedrigsten und höchsten Wert addiert, den jeder Wert würfeln kann: `0/-10` senkt also den
  bestmöglichen Wurf um 10, und `2/0` hebt den schlechtesten um 2.
- Ein `NoFlightModifier` verhindert, dass das Flugzeug überhaupt losgeschickt werden kann.

Die Zeilen-Id benennt, was gemessen wird:

- `AirplaneIntegrity` - wie viel Prozent der Start-Integrität des Flugzeugs noch übrig sind
- `AirplaneHealth` - seine Gesundheit
- `AirplaneFuel` - sein Treibstoffstand; `0` bedeutet einen leeren Tank
- `Mood`, `Energy`, `Confidence` - der Wert jedes Crewmitglieds, von -100 bis 100, abgeglichen mit `Parameter` nach
  Crewrolle
- `SeatsConfiguration`, `CrewHealth`, `CrewOnFire` - Ja/Nein-Prüfungen, bei denen `1` bedeutet, dass das Problem vorliegt: ein
  Crewmitglied auf einem Sitz, der nicht zu seiner Rolle passt, eines, das verletzt ist, oder eines, das brennt

Für jeden gemessenen Wert gilt die erste Zeile, deren Bereich und Rolle passen.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `ModifierCategory` | eine Bezeichnung | `low`, `high`, `zero`, `critical` oder `mismatch` | |
| `ModifierType` | `SkillRollModifier` oder `NoFlightModifier` | | |
| `ModifierRange` | `min/max` ganze Zahlen | `0/-10`, `0/-5`, `0/-3`, `0/-2`, `0/0`, `1/0` oder `2/0` | wird zum niedrigsten/höchsten Wurf der Werte addiert; von `NoFlightModifier`-Zeilen ignoriert |
| `Parameter` | durch Leerzeichen getrennte Crewrollen oder `Default` | `Default`, `CrewRole.Pilot`, alle sechs Rollen oder die fünf Rollen außer `CrewRole.Pilot` | jede Rolle braucht das Präfix `CrewRole.` - ein bloßes `Pilot` passt nie, eine unbekannte Rolle ebenso wenig |
| `ThresholdRange` | `min/max` ganze Zahlen | `-100/-90`, `-89/-50`, `0/0`, `1/1`, `1/40` oder `50/100` | der Bereich gemessener Werte, den diese Zeile abdeckt |

`NoFlightModifier` ist die harte Sperre, die ein Flugzeug am Boden hält - kein Treibstoff mehr oder ein Crewmitglied mit Stimmung am
Tiefpunkt. Erweiterst du seine `ThresholdRange`, bleibt deine ganze Staffel am Boden; setzt du sie auf etwas Unerreichbares wie
`-1000/-999`, schaltest du sie praktisch ab.

Zeilen, die sich über mehrere Zeilen erstrecken und deshalb nicht änderbar sind: `AirplaneIntegrity`, `AirplaneHealth`, `Mood`,
`Energy`, `Confidence`.

#### `TaskValues` - Dauern und Schwellenwerte pro Aufgabe { #taskvalues-durations-and-thresholds-per-task }

Eingebaute Datei: [TaskValues.csv](../assets/csv/TaskValues.csv)

Drei Spalten: die Aufgaben-Id, ein `Variable Name` und ein `Value`.

`Variable Name` ist der Schlüssel, unter dem das Spiel die Einstellung nachschlägt, deshalb **kann nur `Value` geändert werden**. Verwendete
Namen sind `Duration` (Minuten), `Distance`, `Chance`, `ExperienceGain`, `HealthAmount`, `IntegrityAmount`,
`IntegrityPenalty`, `ScheduleThreshold`, `ScheduleThresholdPercentage`, `ResourceToFuelRatio`, `Targets`,
`Initiation` und `Active`.

Aufgaben mit mehreren Einstellungen belegen mehrere Zeilen und können nicht geändert werden. Das sind: `Chat`, `Chill`, `Panic`,
`AirAttackPanic`, `CelebrateSuccessfulMission`, `BreakThings`, `RepairAirplane`, `MaintainAirplane`, `Refuel`,
`RepairEquipment`, `RefillAirplaneAmmo`, `UseTrainingObject`, die sechs `…Simple…`- und sechs `…Advanced…`-Trainingsaufgaben
und `BeOnFire`. Alles andere - `UseRadio`, `Eat`, `Salute`, `Bury`, `Recover`, `MonitorAirspace` und
der Rest - hat eine einzige Einstellung, fast immer `Duration` (`RefillEquipmentAmmo` hat nur
`ScheduleThresholdPercentage`), und kann ganz normal geändert werden.

`Value` akzeptiert auch Text (eine eingebaute Zeile nennt einen Stuhl), deshalb wird eine Nicht-Zahl in einer Zahleneinstellung angenommen
und schlägt erst fehl, wenn die Aufgabe läuft. Das ist die einzige Stelle in dieser Tabelle, an der du noch Unsinn schreiben kannst.

#### `DaySchedule` - die Phasen eines Tages { #dayschedule-the-phases-of-a-day }

Eingebaute Datei: [DaySchedule.csv](../assets/csv/DaySchedule.csv)

Vier Zeilen, `0`–`3`.

| Spalte | Wert | Eingebaut | Hinweise |
|---|---|---|---|
| `Phase` | `Work`, `Leisure`, `Sleep` | pro Zeile: `Sleep`, `Leisure`, `Work`, `Leisure` | `Alert` und `None` werden auch akzeptiert, sind aber nicht für den Tagesplan gedacht |
| `StartHour` | ganze Zahl, einschließlich | pro Zeile: 0, 5, 7, 22 | |
| `EndHour` | ganze Zahl, ausschließlich | pro Zeile: 5, 7, 22, 24 | |

Die vier Zeitspannen werden Stunde für Stunde aufgeschlüsselt, und **jede Stunde von 0 bis 23 muss von genau einer Zeile abgedeckt sein**.
Bei einer Lücke oder Überschneidung wirft die stündliche Abfrage der Phase einen Fehler, und die Basis bleibt in der Phase, in der sie
vorher war - ein kaputter Zustand, kein definiertes "keine Phase". Eine Zeile mit falsch geschriebener `Phase` wird mit einer Warnung
übersprungen und hinterlässt so eine Lücke. Halte die Spannen lückenlos von 0 bis 24, ohne Überschneidungen.

#### `DayNightSystemData` - Sonne und Schatten { #daynightsystemdata-sun-and-shadows }

Eingebaute Datei: [DayNightSystemData.csv](../assets/csv/DayNightSystemData.csv)

Name und Wert, alles Zahlen, rein optisch.

| Zeile | Bedeutung | Eingebaut |
|---|---|---|
| `Morning Time`, `Dawn Time`, `Day Time`, `Evening Time`, `Dusk Time`, `Night Time` | Stunde, in der jede Lichtstufe beginnt | pro Zeile: 4, 7, 10, 17, 22, 23 |
| `Sun Min Rotation` / `Sun Max Rotation` | Bogen der Sonnenhöhe, Grad | 15 / 165 |
| `Sun Yaw Offset` | Kompassdrehung | -90 |
| `Sun Tilt` | Grad | 10 |
| `Shadow Day Intens` / `Shadow Night Intens` | Schattenstärke | 0.85 / 0 |

Halte die sechs Zeitzeilen aufsteigend und innerhalb von 0–23, sonst springen die Lichtstufen hin und her.

#### `GameGoalAlerts` - wann das Spiel den Spieler warnt { #gamegoalalerts-when-the-game-warns-the-player }

Eingebaute Datei: [GameGoalAlerts.csv](../assets/csv/GameGoalAlerts.csv)

Name und Wert, alles Zahlen, nur Warnungen: `LowMoraleThreshold` (-50), `CriticalMoraleThreshold` (-65),
`LowFoodThreshold` (20), `FewLeisureItemsThreshold` (5), `MissionTimerMinutesThreshold` (150),
`LowWaterThreshold` (20).

### Allgemein { #general }

#### `Variables` - der globale Zahlensack { #variables-the-global-number-bag }

Eingebaute Datei: [Variables.csv](../assets/csv/Variables.csv)

Name und Wert, 86 Einträge, jeder gelesen von dem Teil des Spiels, der ihn braucht.

Diese Spalte akzeptiert **alles**, weil ein paar Einträge Text oder einen `min-max`-Bereich statt einer Zahl enthalten.
Schreibst du `abc`, wo eine Zahl hingehört, wird das angenommen und dann als `0` gelesen - die Funktion hört still auf zu arbeiten,
und im [Log](../start/troubleshooting.md#find-the-playerlog) steht ein Fehler. Bei dieser Tabelle solltest du am vorsichtigsten sein.

Einträge, die du kennen solltest, bevor du sie änderst:

- `TimeTickInterval` (0.6666) - echte Sekunden pro Spielminute. Halbierst du den Wert, läuft das ganze Spiel doppelt so schnell,
  inklusive jedes Timers, der darauf abgestimmt ist.
- `AirplanesLimit` (24) - wie viele Flugzeuge eine Basis besitzen darf.
- `CharacterBaseHealth` (7) - plus der Endurance-Rang ergibt das die maximale Gesundheit eines Crewmitglieds. Unter
  `CharacterHeavyInjuryThreshold` (3) startet jeder schwer verletzt.
- `MaxVictoryPoints` (12) - das Budget für Flugzeugbestellungen.
- `ScrambleFuelNeeded` (80) - pauschaler Treibstoff pro Alarmstart, egal welches Flugzeug.
- `AttackHourMin` / `AttackHourMax` (12/23) - werden in 1–23 zurückgeholt, wenn du diesen Bereich verlässt.
- `DiverBombFiresCount`, `BomberBombFiresCount`, `CharredTerrainRevertTimeDays` - diese drei sind `min-max`-Bereiche,
  keine einzelnen Zahlen.

Acht Einträge sind Überbleibsel, und **nichts liest sie**, sie zu ändern bewirkt also überhaupt nichts:
`AttackedCharacterId`, `BikeMovementSpeedMultiplier`, `LichfieldIntroCrewMembersCount`,
`AirplaneIntegrityModifierTreshold`, `AirplaneHealthModifierTreshold`, `AirAttackFighterHealth`,
`AirAttackDiverHealth`, `AirAttackBomberHealth`.

#### `FeedbackVariables`

Eingebaute Datei: [FeedbackVariables.csv](../assets/csv/FeedbackVariables.csv)

Das Feedback-Formular im Spiel: `API Endpoint`, `Feedback Character Limit`, `Screenshot Height`, `Survey Link`,
`Survey Link Demo`, `Survey Opened Player Prefs`. Eine Gameplay-Mod hat keinen Grund, das anzufassen, und wenn du
`API Endpoint` woandershin zeigen lässt, geht das Feedback der Spieler an diese Adresse.

---

## Ausführliches Beispiel { #worked-example }

`Mods/my_balance_mod/CSV/ResourceCost.json` - gib der Lagerkiste Baukosten, mach Holzwände billiger und
streich die Planenkosten des Stuhls:

```json
{
  "Commands": [
    { "Command": "Add", "Id": "storage_box", "Cells": { "Planks": 3, "Metal": 1 } },
    { "Command": "Replace", "Id": "wall_wood", "Cells": { "Planks": 1 } },
    { "Command": "Remove", "Id": "Chair", "Columns": [ "Tarp" ] }
  ]
}
```

`Mods/my_balance_mod/CSV/Variables.json` - beschleunige den Turbo-Modus und lass die Crew häufiger plaudern. `Value`
nimmt in dieser Tabelle jeden Text, ein Tippfehler wie `0,6` wird also still angenommen und dann als `0` gelesen - prüf die
Zahl doppelt:

```json
{
  "Commands": [
    { "Command": "Replace", "Id": "TurboTimeScaleMultiplier", "Cells": { "Value": 20 } },
    { "Command": "Replace", "Id": "RandomActionChatProbability", "Cells": { "Value": 0.6 } }
  ]
}
```

Dieselben zwei Änderungen als `Mods/my_balance_mod/CSV/Variables.csv`:

```text
Name,Value
TurboTimeScaleMultiplier,20
RandomActionChatProbability,0.6
```
