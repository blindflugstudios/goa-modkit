# Biome

Ein Biom ist ein Bodentyp: das Gras, die Erde, Straße, Fels, Sand oder Kies, die mit dem Werkzeug **Biomes** im [Karten Editor](maps.md) über eine Karte gemalt werden. Das Spiel hat 24 davon. Eine Mod kann jedes davon mit einer neuen Textur übermalen, und die Änderung zeigt sich auf jeder Karte, ob mitgeliefert oder selbst gebaut.

Eine Biom-Mod ändert nur das **Aussehen**. Wie schnell sich Leute und Flugzeuge über den Boden bewegen, als welche Startbahnstufe er zählt und ähnliche Regeln stehen in der Tabelle `Biomes` und werden mit [CSV-Tabellen](../data/csv.md) geändert.

## Schnellstart { #quick-start }

Gib dem ersten Gras eine neue Textur:

```text
Mods/
  my_ground_mod/
    Biomes/
      Terrain-Type_Grass_A/
        albedo.png
```

Starte das Spiel neu und lade einen Spielstand oder starte eine Karte. Überall, wo die Karte dieses Gras verwendet, siehst du jetzt deine Textur.

!!! note
    Biom-Texturen werden einmal gelesen, beim Spielstart. Nachdem du eine Textur geändert oder die Mod ein- oder ausgeschaltet hast, **starte das Spiel neu**.

## So funktioniert es { #how-it-works }

- `Biomes/` enthält einen Ordner pro Biom, das du übermalen willst, genau nach dem Biom benannt (siehe die [Liste](#biome-names)). Groß- und Kleinschreibung spielt keine Rolle.
- Jeder Ordner braucht eine Datei: `albedo.png`, die Farbtextur.
- Eine Mod kann keine neuen Biome hinzufügen, nur die 24 vorhandenen übermalen. Eine Karte merkt sich über eine Nummer, welches Biom wo gemalt ist, es gibt also nichts, woran ein neues angehängt werden könnte.
- Die Oberflächendetails des Bioms und sein verbrannter Look nach einem Feuer werden nicht ersetzt.
- Die Texturen des Spiels auf der Festplatte bleiben unangetastet. Verlässt du eine Karte, kehrt der Originalboden zurück, und wenn du die Mod ausschaltest (und neu startest), ist er überall wieder da.

### Die Textur { #the-texture }

| Regel | Grenze |
|---|---|
| Format | Nur PNG |
| Größe | Höchstens 2048 × 2048 Pixel |
| Dateigröße | Höchstens 8 MB |
| Dateiname | `albedo.png` |

Das Spiel skaliert deine Textur auf die Größe seiner eigenen Bodentexturen, jede Größe innerhalb der Grenze funktioniert also; ein quadratisches Bild vermeidet Verzerrungen. Die Textur wiederholt sich über den Boden, sie sollte also nahtlos kacheln: Der linke Rand muss in den rechten übergehen, der obere in den unteren.

Andere Dateien in einem Biom-Ordner (`model.glb`, `destroyed_albedo.png`, ...) haben hier keine Bedeutung. Das Log sagt das, und `albedo.png` lädt trotzdem.

## Biom-Namen { #biome-names }

Die Nummer ist die Zeile des Bioms in der Tabelle `Biomes`. Zeilen mit derselben Nummer beschreiben, wie sich dieser Boden spielt.

| Nummer | Ordnername | Boden |
|---|---|---|
| 0 | `Terrain-Type_Dirt_A` | Erde |
| 1 | `Terrain-Type_Dirt_B` | Erde |
| 2 | `Terrain-Type_Dirt_C` | Erde |
| 3 | `Terrain-Type_Dirt_D` | Erde |
| 4 | `Terrain-Type_Dirt_E` | Erde |
| 5 | `Terrain-Type_Dirt_F` | Erde |
| 6 | `Terrain-Type_Dirt_G` | Erde, liegt auch unter Parkplätzen, Gartenbeeten und Erdstartbahnen |
| 7 | `Terrain-Type_Dirt_H` | Erde |
| 8 | `Terrain-Type_Grass_A` | Gras |
| 9 | `Terrain-Type_Grass_B` | Gras |
| 10 | `Terrain-Type_Grass_C` | Gras |
| 11 | `Terrain-Type_Grass_D` | Gras |
| 12 | `Terrain-Type_Grass_E` | Gras |
| 13 | `Terrain-Type_Road_A` | Straße, liegt auch unter Asphaltstartbahnen |
| 14 | `Terrain-Type_Road_B` | Straße |
| 15 | `Terrain-Type_Road_C` | Straße, liegt auch unter Betonstartbahnen |
| 16 | `Terrain-Type_Rock_A` | Fels |
| 17 | `Terrain-Type_Rock_B` | Fels |
| 18 | `Terrain-Type_Rock_C` | Fels |
| 19 | `Terrain-Type_Sand_A` | Sand |
| 20 | `Terrain-Type_Sand_B` | Sand, liegt auch unter Sandstartbahnen |
| 21 | `Terrain-Type_Sand_C` | Sand |
| 22 | `Terrain-Type_Gravel_A` | Kies, liegt auch unter Kiesstartbahnen |
| 23 | `Terrain-Type_Grass_B3` | Gras |

Die Startbahnbeläge sind die eingebauten Werte der Tabelle `AirstripTiers` (Spalte `Biome Id`); eine Mod, die diese Tabelle ändert, ändert auch, welcher Boden verlegt wird.

## Biome und die Tabelle `Biomes` { #biomes-and-the-biomes-table }

Die beiden sind unabhängig und lassen sich frei kombinieren:

| Du willst ändern... | Nutze |
|---|---|
| Wie ein Bodentyp aussieht | `Biomes/<name>/albedo.png` (diese Seite) |
| Wie sich ein Bodentyp spielt: Bewegungsgeschwindigkeit, Startbahnstufe, Verschleiß gelagerter Waren, Feuerausbreitung | Die Tabelle `Biomes`, Zeile `<number>` ([CSV-Tabellen](../data/csv.md)) |
| Welcher Boden wo auf einer Karte gemalt ist | Das Werkzeug **Biomes** im [Karten Editor](maps.md) |

## Mehrere Mods, dasselbe Biom { #several-mods-same-biome }

Übermalen zwei eingeschaltete Mods dasselbe Biom, gewinnt die zuletzt angewendete Mod, und das Log vermerkt, welche welche überschrieben hat. Die Reihenfolge steht unter [So funktionieren Mods](../basics/mods.md).

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

Suche in `Player.log` nach Zeilen, die mit `[Mod <your mod id>] Biomes/...` beginnen:

| Log-Zeile (gekürzt) | Bedeutung |
|---|---|
| `Biomes/Terrain-Type_Grass_A: replaced biome slot 8 (Terrain-Type_Grass_A).` | Deine Textur wird verwendet. Wird beim Laden einer Karte geschrieben. |
| `Biomes/Grass_A names no biome of this game. Known biomes: Terrain-Type_Dirt_A, ...` | Der Ordnername passt nicht. Kopiere ihn aus der Liste oben. |
| `Biomes/Terrain-Type_Grass_A has no albedo.png and is ignored` | Füge die Textur hinzu oder korrigiere ihren Namen. |
| `Biomes/Terrain-Type_Grass_A: only albedo.png is used for a biome; the other files are ignored.` | Harmlos; entferne die zusätzlichen Dateien, wenn du magst. |
| `Biomes/Terrain-Type_Grass_A/albedo.png is 4096x4096, over the 2048x2048 limit` | Verkleinere die Textur. |
| `Biomes/Terrain-Type_Grass_A/albedo.png is not a PNG` | Speichere sie als echte PNG. |
| `[Mods] This device cannot copy textures on the GPU; biome textures from mods are not applied.` | Deine Grafikhardware unterstützt keine Biom-Mods. In der Mod gibt es nichts zu reparieren. |
