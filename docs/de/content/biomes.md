# Biome

Ein Biom ist ein Bodentyp: das Gras, die Erde, Straße, Fels, Sand oder Kies, die mit dem Werkzeug **Biomes** im [Karten Editor](maps.md) über eine Karte gemalt werden. Das Spiel hat 24 davon, nummeriert von `0` bis `23`. Eine Mod kann jedes davon mit einer neuen Textur übermalen, und die Änderung zeigt sich auf jeder Karte, ob mitgeliefert oder selbst gebaut.

Eine Biom-Mod ändert nur das **Aussehen**. Wie schnell sich Leute und Flugzeuge über den Boden bewegen, als welche Startbahnstufe er zählt und ähnliche Regeln stehen in der Tabelle `Biomes` und werden mit [CSV-Tabellen](../data/csv.md) geändert.

## Schnellstart { #quick-start }

Gib dem ersten Gras eine neue Textur:

```text
Mods/
  my_ground_mod/
    Biomes/
      8.png
```

Starte das Spiel neu und lade einen Spielstand oder starte eine Karte. Überall, wo die Karte dieses Gras verwendet, siehst du jetzt deine Textur.

!!! note "Nach jeder Änderung neu starten"
    Biom-Texturen werden **einmal eingelesen, beim Spielstart**. Nachdem du eine PNG hinzugefügt oder geändert oder die Mod ein- oder ausgeschaltet hast, **beendest du das Spiel ganz und startest es neu**. Einen Spielstand laden, **Refresh** und der Schalter **Enabled** im Mods-Fenster lesen sie nicht neu ein.

## So funktioniert es { #how-it-works }

- `Biomes/` enthält eine PNG pro Bodentyp, benannt nach seiner Nummer: `8.png` übermalt Bodentyp 8, das erste Gras (siehe die [Liste](#biome-names)).
- Die Nummer schreibst du als einfache Ziffern ohne führende Nullen: `8.png`, nicht `08.png`. Eine Nummer außerhalb von `0` bis `23` wird im Log zusammen mit dem gültigen Bereich gemeldet.
- Nur Dateien direkt in `Biomes/` zählen. Unterordner, andere Dateitypen und andere Namen werden im Log gemeldet und ignoriert.
- Eine Mod kann keine neuen Biome hinzufügen, nur die 24 vorhandenen übermalen. Eine Karte merkt sich über eine Nummer, welches Biom wo gemalt ist, es gibt also nichts, woran ein neues angehängt werden könnte.
- Die Oberflächendetails des Bioms und sein verbrannter Look nach einem Feuer werden nicht ersetzt.
- Die Texturen des Spiels auf der Festplatte bleiben unangetastet. Wenn du die Mod ausschaltest (und neu startest), ist der Originalboden überall wieder da.
- Der übermalte Boden wird auf der Grafikkarte zusammengesetzt. Auf einem Computer, dessen Grafikkarte dort keine Texturen kopieren kann, werden Biom-PNGs nicht angewendet, und das Log sagt das. An der Mod gibt es dann nichts zu reparieren.

### Die Textur { #the-texture }

| Regel | Grenze |
|---|---|
| Format | Eine echte PNG. Ein in `.png` umbenanntes JPEG wird abgelehnt. |
| Größe | Höchstens 4096 × 4096 Pixel (jede Seite einzeln) |
| Dateigröße | Höchstens 10 MB |

Eine PNG über einer Grenze wird **nicht verkleinert**: Sie wird mit einer Warnung im Log übersprungen, und der Boden des Spiels bleibt. Innerhalb der Grenzen bringt das Spiel deine Textur auf die Größe seiner eigenen Bodentexturen, jede Größe funktioniert also; ein quadratisches Bild vermeidet Verzerrung. Die Textur wiederholt sich über den Boden, sie sollte also nahtlos kacheln: Der linke Rand muss in den rechten übergehen, der obere in den unteren.

## Biom-Namen { #biome-names }

Die Nummer ist die Zeile des Bioms in der Tabelle `Biomes`. Zeilen mit derselben Nummer beschreiben, wie sich dieser Boden spielt.

| Nummer | Dateiname | Boden |
|---|---|---|
| 0 | `0.png` | Erde |
| 1 | `1.png` | Erde |
| 2 | `2.png` | Erde |
| 3 | `3.png` | Erde |
| 4 | `4.png` | Erde |
| 5 | `5.png` | Erde |
| 6 | `6.png` | Erde, liegt auch unter Parkplätzen, Gartenbeeten und Erdpisten |
| 7 | `7.png` | Erde |
| 8 | `8.png` | Gras |
| 9 | `9.png` | Gras |
| 10 | `10.png` | Gras |
| 11 | `11.png` | Gras |
| 12 | `12.png` | Gras |
| 13 | `13.png` | Straße, liegt auch unter Asphaltpisten |
| 14 | `14.png` | Straße |
| 15 | `15.png` | Straße, liegt auch unter Betonpisten |
| 16 | `16.png` | Fels |
| 17 | `17.png` | Fels |
| 18 | `18.png` | Fels |
| 19 | `19.png` | Sand |
| 20 | `20.png` | Sand, liegt auch unter Sandpisten |
| 21 | `21.png` | Sand |
| 22 | `22.png` | Kies, liegt auch unter Kiespisten |
| 23 | `23.png` | Gras |

Die Pistenbeläge sind die eingebauten Werte der Tabelle `AirstripTiers` (Spalte `Biome Id`); eine Mod, die diese Tabelle ändert, ändert, welcher Boden gelegt wird.

## Biome und die Tabelle `Biomes` { #biomes-and-the-biomes-table }

Die beiden sind unabhängig und lassen sich frei kombinieren:

| Du willst ändern... | Verwende |
|---|---|
| Wie ein Bodentyp aussieht | `Biomes/<number>.png` (diese Seite) |
| Wie sich ein Bodentyp spielt: Bewegungstempo, Startbahnstufe, Verschleiß gelagerter Waren, Feuerausbreitung | Die Tabelle `Biomes`, Zeile `<number>` ([CSV-Tabellen](../data/csv.md)) |
| Welcher Boden wo auf einer Karte gemalt ist | Das Werkzeug **Biomes** im [Karten Editor](maps.md) |

## Mehrere Mods, dasselbe Biom { #several-mods-same-biome }

Übermalen zwei eingeschaltete Mods dasselbe Biom, gewinnt die zuletzt angewendete Mod, und das Log vermerkt, welche welche überschrieben hat. Die Reihenfolge steht unter [So funktionieren Mods](../basics/mods.md#which-mod-wins).

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

- Hast du **das Spiel neu gestartet**? Biom-Texturen werden nur beim Spielstart eingelesen.
- Liegt die Datei direkt in `Biomes/`, benannt mit einer Nummer von `0` bis `23` ohne führende Null?
- Ist sie eine echte PNG, höchstens 4096 × 4096 Pixel und 10 MB groß?

Probleme stehen in der `Player.log` in Zeilen, die mit `[Mod <your mod id>]` beginnen. Die ausführlichen Zeilen erscheinen eventuell nur in Entwicklungsversionen. Ist das Log still, geh die Liste oben durch. Die Größengrenzen für alle Grafik stehen auch unter [Objekte und Modelle](objects.md#file-limits).
