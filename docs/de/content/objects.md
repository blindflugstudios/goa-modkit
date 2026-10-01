# Objekte und Modelle

Genug vom Standardfass? Eine Mod kann den Objekten des Spiels einen neuen Look geben: Möbeln, Zäunen, Geschützen, Schildern, Postern, Werkbänken, Trainingsgeräten und sogar den Bäumen, Büschen und Felsen auf der Karte. Entweder legst du ein eigenes 3D-Modell hinein, oder du behältst das Modell des Spiels und bemalst es mit einer neuen Textur. Außerdem kannst du einem Objekt ein neues Symbol im Baumenü geben.

Nur das Aussehen ändert sich. Größe im Raster, Kosten, Lebenspunkte, wo die Mannschaft steht, um es zu benutzen, und alle anderen Regeln bleiben so, wie das Spiel sie festlegt. Zahlen änderst du mit [CSV-Tabellen](../data/csv.md).

Alles für Objekte kommt in einen einzigen Ordner deiner Mod, `Objects/`:

```text
Mods/
  my_mod/
    Objects/
      Chair.glb               dein Modell für den Stuhl
      Chair.thumbnail.png     das neue Symbol des Stuhls im Baumenü
      Chair_BaseMap_1001.png  eine Textur dafür
      config.json             optionale Einstellungen
```

!!! note "Nach jeder Änderung neu starten"
    Grafik wird **einmal eingelesen, beim Spielstart**. Nachdem du ein Modell, eine Textur oder ein Vorschaubild hinzugefügt oder geändert hast, **beendest du das Spiel ganz und startest es neu**. Einen Spielstand laden, **Refresh** und der Schalter **Enabled** im Mods-Fenster lesen Grafik nicht neu ein.

## Schnellstart { #quick-start }

Gib dem Stuhl ein neues Modell:

1. Baue deinen Stuhl in deinem 3D-Programm in der Größe des Stuhls aus dem Spiel (in Metern) und exportiere ihn als `Chair.glb` (binäres glTF) oder `Chair.fbx`.
2. Gib dem Material des Stuhls in deinem 3D-Programm einen Namen, zum Beispiel `MyChair`, und speichere seine Farbtextur als `MyChair_BaseMap_1001.png`.
3. Lege beide Dateien in `Mods/my_mod/Objects/`.
4. Starte das Spiel neu und lade einen Spielstand. Jeder Stuhl, die schon aufgestellten und neu gebaute, verwendet jetzt dein Modell.

Willst du nur den Stuhl des Spiels umfärben? Dafür brauchst du gar kein Modell: siehe [Übermalen ohne Modell](#re-painting-without-a-model).

## Welche Objekte sich ändern lassen { #which-objects-can-be-changed }

Der **Dateiname** eines Modells ist die Id des Objekts, das es ersetzt. Vier Arten von Objekten teilen sich den einen Ordner, und ihre Ids überschneiden sich nie:

| Art | Woher die Ids kommen | Beispiele |
|---|---|---|
| Objekte, die du aus dem Baumenü platzierst | die Spalte `ID` der Tabelle `BuildingComponents` | `Chair`, `Shelf`, `WoodenChair` |
| Werkbänke | die Liste unter [Veränderbare Objekte](moddable-objects.md) | `FieldKitchen`, `SawStation` |
| Trainingsobjekte | die Liste unter [Veränderbare Objekte](moddable-objects.md) | `ShootingSimpleTargetRange` |
| Kartenobjekte: Bäume, Felsen, Teiche und andere Dinge, die du erntest | die Spalte `ID` der Tabelle `MapObjects` | `tree`, `bush_big`, `large_rock` |

Jedes Objekt aus dem Baumenü, jede Werkbank und jedes Trainingsobjekt, das du ändern kannst, steht unter [Veränderbare Objekte](moddable-objects.md). Die Kartenobjekte stehen unter [Eingebaute Texturnamen](texture-names.md#map-objects).

Bei den Ids spielt Groß- und Kleinschreibung keine Rolle, `chair.fbx` ändert also auch den Stuhl.

Mit `Objects/` lassen sich nur diese vier Arten von Objekten neu gestalten. Flugzeuge bekommen neue Lackierungen auf anderem Weg: siehe [Flugzeug-Skins](airplanes.md). Den Boden änderst du mit [Biomen](biomes.md).

## Dateinamen { #file-names }

Jede Datei, die zu einem Objekt gehört, heißt `<objectId>[.<variant>][.destroyed|.thumbnail]` plus Dateiendung. Die Teile in eckigen Klammern sind optional:

| Datei | Was sie ist |
|---|---|
| `Chair.fbx` oder `Chair.glb` | das Modell des Stuhls |
| `Chair.destroyed.fbx` | das Modell, zu dem der Stuhl wechselt, wenn er zerstört wird |
| `Chair.thumbnail.png` | das Symbol des Stuhls im Baumenü |
| `tree.2.glb` | nur Variante 2 des Kartenobjekts `tree` |
| `tree.glb` | jede Variante von `tree`, die keine eigene Datei hat |

- **Modelle** dürfen `.glb` (binäres glTF) oder `.fbx` sein. Gibt es beide für dasselbe Objekt, wird die `.glb` verwendet und die `.fbx` im Log als ignoriert gemeldet.
- **Varianten** gibt es nur bei Kartenobjekten, und sie werden ab `0` gezählt: `tree.0` ist die erste Variante von `tree`, `tree.1` die zweite.
- **Variantennummern** sind einfache Ziffern ohne führende Nullen: `tree.2`, niemals `tree.02`. Deshalb werden auch Blenders Duplikatnamen wie `Chair.001.fbx` abgelehnt. Benenne die Datei um, bevor du sie hineinkopierst.
- **Ein zerstörtes Modell** ist optional. Manche Objekte werden nie zerstört gezeigt; ein zerstörtes Modell für so ein Objekt wird mit einer Warnung im Log übersprungen.
- **Alles andere** im Ordner, das weder Modell noch PNG noch die `config.json` direkt in `Objects/` ist, wird im Log gemeldet und ignoriert.

## Unterordner { #subfolders }

Du darfst deine Dateien beliebig in Unterordner von `Objects/` sortieren, aber **die Namen der Unterordner bedeuten nichts**: Eine Datei zählt nur über ihren Namen. `Objects/Chair/model.fbx` ist ein Modell für ein Objekt namens `model`, nicht für den Stuhl. Nenne sie stattdessen `Objects/Chair/Chair.fbx`.

Weil `Objects/` mit allen Unterordnern als ein einziger Topf zählt, kollidieren zwei Dateien mit demselben Namen in verschiedenen Unterordnern: Das Spiel behält eine und meldet die andere. Verknüpfungen (symbolische Links und Junctions) werden nie verfolgt.

## Das Modell bauen { #building-the-model }

- **Größe und Ausrichtung.** Baue das Modell im Maßstab des Spiels, in Metern, und in dieselbe Richtung ausgerichtet wie das Objekt des Spiels. Dein Modell wird auf den Ursprung des Originals gesetzt und nicht passend skaliert, setze seinen Ursprung also dorthin, wo ihn das Original hat, meist auf den Boden in die Mitte des Objekts. Eine FBX wird beim Einlesen auf Y nach oben und Meter umgerechnet, und eine auf dem üblichen Weg aus Blender exportierte FBX schaut in dieselbe Richtung wie die Grafik des Spiels.
- **Nur das Aussehen ändert sich.** Die Grundfläche des Objekts im Raster, wo die Mannschaft steht, um es zu benutzen, und womit es zusammenstößt, bleiben die des Spiels. Ein Modell, das viel größer ist als das Original, ragt durch Wände und Nachbarn.
- **Detailstufen.** Nenne die Teile deines Modells `LOD0`, `LOD1`, `LOD2` und so weiter (Groß- und Kleinschreibung egal; `LOD1_Trunk` und `lod2.001` zählen auch). Sie werden zu seinen Detailstufen und wechseln bei denselben Entfernungen wie beim Original. Hast du weniger Stufen als das Original, bleibt deine letzte bis zu der Entfernung, in der das Objekt verschwindet. Ein Modell ohne `LOD`-Namen sieht in jeder Entfernung gleich aus. Stufen wechseln nur bei Objekten, die eingebaute Detailstufen haben. Bei allen anderen werden alle `LOD`-Teile gleichzeitig übereinander gezeichnet, gib so einem Objekt also nur eine Stufe.
- **Effekte** des Originals, etwa das Sägemehl einer Werkbank oder die Blätter eines Baums, der gefällt wird, laufen auf deinem Modell weiter.
- **Nur unbewegte Modelle.** Animationen in einer FBX werden nicht eingelesen, und das Spiel animiert ein Mod-Modell nie.
- **Höchstens 32 MB** pro Modelldatei. Eine größere Datei wird mit einer Warnung übersprungen, und das Objekt behält seinen eingebauten Look.

### Was eine FBX enthalten darf { #what-an-fbx-may-contain }

Das Spiel liest FBX-Dateien selbst, versteht also weniger vom Format, als Blender schreiben kann:

- Meshes und die Hierarchie darüber, mit Position, Drehung und Skalierung. Versteckte Objekte werden weggelassen, und eine Datei ganz ohne Mesh wird ignoriert.
- Normalen so, wie sie exportiert wurden. Ein Mesh ohne Normalen bekommt weiche Normalen.
- **Nur die erste UV-Map.** Jede weitere UV-Map wird ignoriert, lege die UVs, die deine Texturen verwenden, also auf die erste.
- Flächen mit mehr als drei Ecken werden in Dreiecke zerlegt. Das ist nur bei flachen, konvexen Flächen exakt. Trianguliere ungewöhnliche Flächen vor dem Export, oder setze im FBX-Export von Blender den Haken bei **Triangulate Faces**.
- Pro Material: die Grundfarbe und die Texturen, die an Grundfarbe, Normal Map (oder Bump) und Emission hängen. Vertex-Farben, Metallic, Roughness und alle anderen Slots werden nicht gelesen.
- **In die FBX eingebettete Bilder werden nie gelesen.** Liefere die Texturen als PNG-Dateien in `Objects/` mit (siehe [Texturen](#textures)).

## Texturen { #textures }

Texturen sind PNG-Dateien irgendwo in `Objects/`, gefunden über ihren Namen. Es gibt drei Arten, sie zu benennen. Das Spiel probiert sie in dieser Reihenfolge, und jede füllt nur, was die vorige leer gelassen hat:

| | Benenne die PNG nach | Beispiel | Braucht ein Modell |
|---|---|---|---|
| 1 | dem **Material** in deinem Modell: `<material>_BaseMap_<tile>` und `<material>_Specular_<tile>` | `MyChair_BaseMap_1001.png` für ein Material namens `MyChair` | ja |
| 2 | der **Textur, die das Material deines Modells verwendet** | `wood-01.png` für ein Material, das mit einem Bild namens `wood-01` bemalt ist | ja |
| 3 | einer **eingebauten Textur** des Spiels | `BedMetal_Toon-Main_BaseMap_1001.png` | nein |

Weg 1 ist für ein Modell der einfachste: Du musst in deinem 3D-Programm gar kein Bild mit dem Material verbinden. Gib Material und PNG einfach passende Namen. Wege 1 und 3 funktionieren nur mit dem Material des Spiels, und das ist die Voreinstellung (siehe [Material des Spiels oder dein eigenes](#game-material-or-your-own)).

### Die Textur, die ein Modell nennt { #the-texture-a-model-names }

Die Materialien eines Modells nennen die Bilder, die sie verwenden, und das Spiel sucht **irgendwo in `Objects/` nach einer PNG mit diesem Namen**. Ein Material, das ein Bild namens `wood-01` verwendet, bekommt `Objects/wood-01.png` (oder `Objects/irgendein/unterordner/wood-01.png`). Ordner und Dateiendung im gespeicherten Namen werden ignoriert, ein Material, das mit `C:\art\wood-01.jpg` bemalt ist, findet also trotzdem `wood-01.png`. Eine PNG kann beliebig vielen Modellen dienen und wird nur einmal geladen.

Die beiden Modellformate verhalten sich unterschiedlich, wenn keine passende PNG da ist:

| | `.glb` | `.fbx` |
|---|---|---|
| Gelesene Textur-Slots | Grundfarbe, Metallic-Roughness, Normal, Occlusion, Emissive | Grundfarbe, Normal (oder Bump), Emissive |
| Keine PNG mit diesem Namen in `Objects/` | das in die `.glb` eingebettete Bild wird verwendet | der Slot bleibt ohne Textur, und das Log nennt die Textur, nach der gesucht wurde |
| Bilder außerhalb der Datei | abgelehnt: Eine `.glb` muss alles selbst enthalten | nie gelesen: Nur die PNGs in `Objects/` zählen |

Jede PNG in `Objects/`, deren Name nicht auf `.thumbnail` endet, zählt als Textur. Eine Textur, die weder ein Modell noch ein eingebautes Objekt verwendet, wird einfach nie geladen.

## Übermalen ohne Modell { #re-painting-without-a-model }

Eine PNG, die genauso heißt wie eine der Texturen des Spiels, **ersetzt diese Textur**, ganz ohne Modell. `Objects/BedMetal_Toon-Main_BaseMap_1001.png` übermalt das Metallbett überall, wo es auftaucht, auch seinen zerstörten Look. Jedes Objekt, das dieselbe Textur verwendet, ändert sich mit.

- Male über das Originalbild in derselben Größe und Aufteilung, denn das Modell bleibt das des Spiels.
- Die Texturnamen des Spiels sehen meist so aus: `<Material>_Toon-Main_BaseMap_<tile>` und `<Material>_Toon-Main_Specular_<tile>`. Die Texturnamen jedes Objekts stehen unter [Eingebaute Texturnamen](texture-names.md).
- Übermalt wird nur die Grafik des Objekts selbst. Was sich alle Objekte teilen, etwa die Baukiste, Platzierungsmarkierungen und Reichweitenanzeigen, behält seinen Look. Flugzeuge (siehe [Flugzeug-Skins](airplanes.md)) und der Boden (siehe [Biome](biomes.md)) werden so nicht geändert.
- Liefern zwei Mods denselben Texturnamen, gewinnt die, die später in der Ladereihenfolge kommt.

## UDIM-Kacheln und Specular Maps { #udim-tiles-and-specular-maps }

Ein Modell mit dem Material des Spiels kann seine UVs auf bis zu drei Texturkacheln (UDIM-Kacheln genannt) verteilen, so wie die Grafik des Spiels selbst, mit einer Specular Map (wie stark jede Stelle glänzt) pro Kachel. Für ein Material namens `Crate`:

| Grundfarbe | Specular | Verwendet für UVs mit U von |
|---|---|---|
| `Crate_BaseMap_1001.png` | `Crate_Specular_1001.png` | 0 bis 1 |
| `Crate_BaseMap_1002.png` | `Crate_Specular_1002.png` | 1 bis 2 |
| `Crate_BaseMap_1003.png` | `Crate_Specular_1003.png` | 2 und mehr |

- Namen nach dem Material (Weg 1) werden zuerst probiert, für die Grundfarbe und für jede Specular Map einzeln. Eine Mod darf auch nur `Crate_Specular_1001.png` mitliefern.
- Ist keine Grundfarbe nach dem Material benannt, wird die Textur, die dein Modell verwendet (Weg 2), zur Kachel 1001, und die anderen Kacheln und Specular Maps werden nach ihr benannt. Die Kachelnummer folgt auf ein `_` oder einen `.`: `crate_1001` und `crate.1001` beginnen beide einen Satz, und ein in Blender als Kachelsatz gespeichertes Bild `crate.<UDIM>.png` findet `crate.1001.png`. Die Specular Map hat denselben Namen, nur mit `_Specular` statt `_BaseMap`, sie funktioniert also nur, wenn der Texturname `_BaseMap` enthält.
- Kacheln schalten sich ein, wenn es zur Grundfarbe `1001` mindestens eine weitere Kachel gibt. Eine einzelne Textur wird wie gewohnt gezeichnet. Eine fehlende Kachel dazwischen wird weiß gezeichnet.
- Eine Specular Map oder Grundfarbe, die deine Mod nicht mitliefert, lässt die des Originals an ihrem Platz.
- Eine nach dem Material benannte Grundfarbe wird so gezeichnet, wie sie ist: Die Farbe, die das Material in deinem Modell hat, wird ignoriert, weil ein FBX-Material ohne Bild trotzdem Blenders graue Voreinstellung mitträgt.

## Material des Spiels oder dein eigenes { #game-material-or-your-own }

Standardmäßig wird dein Modell mit **dem Material des Spiels** für dieses Objekt gezeichnet, mit der Grundfarbtextur und der Grundfarbe deines Modells. Nur so zeigen sich Kampfschäden und die anderen Effekte, die das Spiel auf Objekte malt, auch auf deinem Modell. Normal-, Metallic-Roughness-, Occlusion- und Emissive-Maps deines Modells werden dabei nicht verwendet; Specular Maps und UDIM-Kacheln schon.

Willst du das Material stattdessen genau so behalten, wie du es gebaut hast, schaltest du das Material des Spiels für dieses Objekt in `Objects/config.json` aus. Gelesen wird nur die `config.json` direkt in `Objects/`:

```json
{
  "Objects": {
    "Chair": { "UseGameMaterial": false },
    "tree":  { "UseGameMaterial": false }
  }
}
```

- Die Schlüssel sind Objekt-Ids wie in den Dateinamen, Groß- und Kleinschreibung egal. Ein Eintrag für `tree` gilt auch für `tree.2`, außer `tree.2` hat einen eigenen Eintrag.
- Ein Objekt mit `"UseGameMaterial": false` behält seinen vollen Look aus deinem 3D-Programm, **zeigt aber keine Kampfschäden**. Außerdem verwendet es nur die Textur, die sein Material nennt (Weg 2), ohne Specular Maps und UDIM-Kacheln.
- Auch mit `false` verwendet ein Material ohne Grundfarbtextur trotzdem das Material des Spiels und behält die Farbe, die du ihm gegeben hast. Genauso ein `.glb`-Material, das kein normales Metallic-Roughness-Material ist (ein unbeleuchtetes oder ein Specular-Glossiness-Material).
- Eine `config.json`, die das Spiel nicht lesen kann, wird im Log gemeldet, und jedes Objekt fällt auf die Voreinstellung zurück.

## Vorschaubilder { #thumbnails }

`<objectId>.thumbnail.png` ersetzt das Symbol des Objekts im Baumenü und überall sonst, wo dieses Symbol gezeigt wird.

- **Höchstens 512 × 512 Pixel** und höchstens 10 MB. Jede Seite zählt für sich, 512 × 256 geht also. Ein größeres Vorschaubild wird **nicht verkleinert**: Es wird mit einer Warnung im Log übersprungen, und das Symbol des Spiels bleibt.
- Ein Vorschaubild wird nur **neben einem Modell mit derselben Id** verwendet. Es kann nicht das Symbol eines Objekts ändern, dem deine Mod kein neues Modell gibt; ein Vorschaubild allein wird gemeldet und ignoriert.
- Ein Vorschaubild pro Objekt. Eine zweite Datei mit demselben Namen in einem anderen Unterordner wird ignoriert.
- Kartenobjekte stehen nicht im Baumenü, ein Vorschaubild für eins kann also nirgends auftauchen.

## Bäume, Felsen und andere Kartenobjekte { #trees-rocks-and-other-map-objects }

Bäume, Büsche, Felsen, Teiche und die anderen Dinge, die auf einer Karte platziert sind, änderst du über `Objects/` genauso wie Objekte aus dem Baumenü. Einen eigenen Ordner `TerrainObjects/` gibt es nicht mehr; eine Mod, die nur einen Ordner `TerrainObjects/` hat, wird gar nicht bemerkt.

- Die Id kommt aus der Spalte `ID` der Tabelle `MapObjects`, zum Beispiel `tree`, `bush_big` oder `large_rock`. Alle stehen mit ihren Texturnamen unter [Eingebaute Texturnamen](texture-names.md#map-objects).
- Viele Kartenobjekte gibt es in mehreren Varianten. `tree.glb` ersetzt jede Variante des Baums; `tree.0.glb`, `tree.1.glb` und so weiter ersetzen nur eine, gezählt ab `0`.
- Was du von ihnen erntest, wie lange es dauert und wo sie wachsen, bleibt gleich.

## Dateigrenzen { #file-limits }

Jede Datei in `Objects/` und `Biomes/` wird geprüft, bevor sie geladen wird:

| Datei | Größtes Bild | Größte Datei |
|---|---|---|
| Modell (`.glb`, `.fbx`) | - | 32 MB |
| Textur | 4096 × 4096 | 10 MB |
| Vorschaubild | 512 × 512 | 10 MB |
| Biom | 4096 × 4096 | 10 MB |

- Jedes Bild muss eine echte PNG sein. Ein in `.png` umbenanntes JPEG wird abgelehnt.
- Die Bildgrenze gilt für jede Seite einzeln.
- Ein Bild über seiner Grenze wird **nie verkleinert**. Es wird mit einer Warnung im Log übersprungen, und das Spiel fällt zurück: Ein übersprungenes Vorschaubild lässt das Symbol des Spiels stehen, ein übersprungenes Biom den Boden des Spiels, und ein Material, dessen Textur übersprungen wurde, wird ohne sie gezeichnet.

## Mehrere Mods ändern dasselbe Objekt { #several-mods-changing-the-same-object }

Ändern zwei eingeschaltete Mods dasselbe Objekt, gewinnt die Mod, die **zuletzt** angewendet wird, nach der Ladereihenfolge (siehe [So funktionieren Mods](../basics/mods.md#which-mod-wins)). Das Log vermerkt, welche Mod welche überschrieben hat. Ein Objekt wird als Ganzes entschieden: Das Modell einer Mod wird nie mit dem Vorschaubild einer anderen Mod für dasselbe Objekt kombiniert.

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

- Hast du **das Spiel neu gestartet**? Grafik wird nur beim Spielstart eingelesen.
- Ist die Mod unter **Hauptmenü -> Mods** eingeschaltet?
- Passt der Dateiname genau zu einer Id (abgesehen von Groß- und Kleinschreibung)? Verlässt du dich auf einen Unterordnernamen, der nichts bedeutet?
- Liegt jede Datei innerhalb der Grenzen oben, und ist jedes Bild eine echte PNG?
- Bei einer FBX: Liegen die Texturen als PNGs in `Objects/`, benannt nach dem Material oder nach dem Bild, das das Material verwendet?

Das Spiel schreibt, was es abgelehnt hat und warum (ein falscher Name, eine fehlende Textur, ein zu großes Bild), in die `Player.log`, in Zeilen, die mit `[Mod <your mod id>]` beginnen. Wo das Log liegt, steht unter [So funktionieren Mods](../basics/mods.md). Die ausführlichen Zeilen erscheinen eventuell nur in Entwicklungsversionen. Ist das Log still, geh die Liste oben durch und schau dir das Objekt im Spiel an.
