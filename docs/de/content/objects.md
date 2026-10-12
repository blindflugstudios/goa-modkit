# Objekte und Modelle

Genug vom Standardfass? Eine Mod kann den Objekten des Spiels einen neuen Look geben: Möbeln, Zäunen, Geschützen, Schildern, Postern, Werkbänken und Trainingsgeräten, und auch den Bäumen, Felsen und Teichen auf der Karte. Entweder legst du ein eigenes 3D-Modell hinein, oder du behältst das Modell des Spiels und bemalst es mit einer neuen Textur. Außerdem kannst du einem Objekt ein neues Symbol im Baumenü geben.

Nur das Aussehen ändert sich. Größe im Raster, Kosten, Lebenspunkte, wo die Mannschaft steht, um es zu benutzen, und alle anderen Regeln bleiben so, wie das Spiel sie festlegt. Zahlen änderst du mit [CSV-Tabellen](../data/csv.md).

!!! tip "Beispieldateien"
    Fertige Beispielmodelle, Texturen, Vorschaubilder und Export-Presets findest du im [Beispielordner auf Google Drive](https://drive.google.com/open?id=15fkBMoUdIB0wkL8wjuqEwflo2xZqbXni&usp=drive_fs). Nimm sie als Vorlage dafür, wie deine eigenen Dateien aussehen sollen.

Alles für Objekte kommt in einen einzigen Ordner deiner Mod, `Objects/`:

```text
Mods/
  my_mod/
    Objects/
      Chair.glb               dein Modell für den Stuhl
      Chair.destroyed.glb     der Stuhl, wenn er zerstört ist
      Chair.thumbnail.png     das neue Symbol des Stuhls im Baumenü
      Chair_BaseMap_1001.png  eine Textur dafür
      config.json             optionale Einstellungen
```

!!! note "Nach jeder Änderung neu starten"
    Grafik wird **einmal eingelesen, beim Spielstart**. Nachdem du ein Modell, eine Textur oder ein Vorschaubild hinzugefügt oder geändert hast, **beendest du das Spiel ganz und startest es neu**. Einen Spielstand laden, **Refresh** und der Schalter **Enabled** im Mods-Fenster lesen Grafik nicht neu ein.

## Schnellstart { #quick-start }

Gib dem Stuhl ein neues Modell:

1. Baue deinen Stuhl in deinem 3D-Programm in der Größe des Stuhls aus dem Spiel (in Metern) und exportiere ihn als `Chair.glb` (binäres glTF) oder `Chair.fbx`. Baue auch seinen zerstörten Look und exportiere ihn als `Chair.destroyed.glb` oder `Chair.destroyed.fbx`.
2. Gib dem Material des Stuhls in deinem 3D-Programm einen Namen, zum Beispiel `MyChair`, und speichere seine Farbtextur als `MyChair_BaseMap_1001.png`.
3. Lege alle drei Dateien in `Mods/my_mod/Objects/`.
4. Starte das Spiel neu und lade einen Spielstand. Jeder Stuhl, die schon aufgestellten und neu gebaute, verwendet jetzt dein Modell.

Willst du nur den Stuhl des Spiels umfärben? Dafür brauchst du gar kein Modell: siehe [Übermalen ohne Modell](#re-painting-without-a-model).

## Welche Objekte sich ändern lassen { #which-objects-can-be-changed }

Der **Dateiname** eines Modells ist die Id des Objekts, das es ersetzt. Du kannst die Objekte ändern, die du aus dem Baumenü platzierst, auch Werkbänke und Trainingsobjekte, zum Beispiel `Chair`, `FieldKitchen` oder `ShootingSimpleTargetRange`. Jedes Objekt, das du ändern kannst, steht in unserer [Tabelle der veränderbaren Objekte](https://airtable.com/appvUVR7eS3bq1S8f/shrKPxjhkGlHRUmpO), zusammen mit dem, wie wir es selbst gebaut haben: Benennung und Verwendung der Materialien, Texturauflösung, UDIM-Angaben und seine zerstörte Ansicht.

Bei den Ids spielt Groß- und Kleinschreibung keine Rolle, `chair.fbx` ändert also auch den Stuhl.

Die Bäume, Felsen, Teiche und anderen Dinge, die auf einer Karte platziert sind, änderst du auf dieselbe Weise, zum Beispiel `tree`, `sand_pit` oder `large_rock`. Für sie gelten ein paar eigene Regeln: siehe [Kartenobjekte](#map-objects). Die Id jedes Objekts, das du ändern kannst, Kartenobjekte eingeschlossen, steht unter [Veränderbare Objekte](moddable-objects.md).

Flugzeuge bekommen neue Lackierungen auf anderem Weg: siehe [Flugzeug-Skins](airplanes.md). Den Boden änderst du mit [Biomen](biomes.md).

## Dateinamen { #file-names }

Jede Datei, die zu einem Objekt gehört, heißt `<objectId>`, `<objectId>.destroyed` oder `<objectId>.thumbnail`, plus Dateiendung. Ein Kartenobjekt kann zusätzlich eine Variantennummer tragen: `<objectId>.<variant>`.

| Datei | Was sie ist |
|---|---|
| `Chair.fbx` oder `Chair.glb` | das Modell des Stuhls |
| `Chair.destroyed.fbx` | das Modell, zu dem der Stuhl wechselt, wenn er zerstört wird |
| `Chair.thumbnail.png` | das Symbol des Stuhls im Baumenü |
| `tree.glb` | jede Variante des Kartenobjekts `tree`, die keine eigene Datei hat |
| `tree.2.glb` | nur Variante 2 von `tree` |

- **Varianten** gibt es nur bei Kartenobjekten. Sie werden ab `0` gezählt und ohne führende Nullen geschrieben: `tree.2`, nie `tree.02`.

- **Modelle** dürfen `.glb` (binäres glTF) oder `.fbx` sein. Gibt es beide für dasselbe Objekt, wird die `.glb` verwendet und die `.fbx` im [Log](../start/troubleshooting.md#find-the-playerlog) als ignoriert gemeldet.
- **Blenders Duplikatnamen** wie `Chair.001.fbx` werden abgelehnt. Benenne die Datei um, bevor du sie hineinkopierst.
- **Ein zerstörtes Modell** ist Pflicht. Das Spiel zeigt immer den zerstörten Look eines Objekts, deshalb braucht jedes Modell, das du mitlieferst, ein `.destroyed`-Modell daneben. Die [Tabelle der veränderbaren Objekte](https://airtable.com/appvUVR7eS3bq1S8f/shrKPxjhkGlHRUmpO) zeigt die zerstörte Ansicht jedes Objekts.
- **Alles andere** im Ordner, das weder Modell noch PNG noch die `config.json` direkt in `Objects/` ist, wird im [Log](../start/troubleshooting.md#find-the-playerlog) gemeldet und ignoriert.

## Unterordner { #subfolders }

Du darfst deine Dateien beliebig in Unterordner von `Objects/` sortieren, aber **die Namen der Unterordner bedeuten nichts**: Eine Datei zählt nur über ihren Namen. `Objects/Chair/model.fbx` ist ein Modell für ein Objekt namens `model`, nicht für den Stuhl. Nenne sie stattdessen `Objects/Chair/Chair.fbx`.

Weil `Objects/` mit allen Unterordnern als ein einziger Topf zählt, kollidieren zwei Dateien mit demselben Namen in verschiedenen Unterordnern: Das Spiel behält eine und meldet die andere. Verknüpfungen (symbolische Links und Junctions) werden nie verfolgt.

## Das Modell bauen { #building-the-model }

- **Größe und Ausrichtung.** Baue das Modell im Maßstab des Spiels, in Metern, und in dieselbe Richtung ausgerichtet wie das Objekt des Spiels. Dein Modell wird auf den Ursprung des Originals gesetzt und nicht passend skaliert, setze seinen Ursprung also dorthin, wo ihn das Original hat, meist auf den Boden in die Mitte des Objekts. Eine FBX wird beim Einlesen auf Y nach oben und Meter umgerechnet, und eine auf dem üblichen Weg aus Blender exportierte FBX schaut in dieselbe Richtung wie die Grafik des Spiels.
- **Nur das Aussehen ändert sich.** Die Grundfläche des Objekts im Raster, wo die Mannschaft steht, um es zu benutzen, und womit es zusammenstößt, bleiben die des Spiels. Ein Modell, das viel größer ist als das Original, ragt durch Wände und Nachbarn.
- **Detailstufen.** Nenne die Teile deines Modells `LOD0`, `LOD1`, `LOD2` und so weiter (`LOD1_Trunk` zählt auch), dann wechselt das Spiel bei denselben Entfernungen zwischen ihnen wie beim Original. Hast du weniger Stufen als das Original, bleibt deine letzte stehen, bis das Objekt verschwindet. Ein Modell ohne `LOD`-Namen sieht auf jede Entfernung gleich aus. Stufen wechseln nur bei Objekten, die selbst welche haben, etwa Bäumen; bei jedem anderen Objekt werden alle `LOD`-Teile gleichzeitig gezeichnet, gib ihm also nur eine Stufe.
- **Effekte** des Originals, etwa das Sägemehl einer Werkbank oder die Blätter eines Baums, der gefällt wird, laufen auf deinem Modell weiter.
- **Nur unbewegte Modelle.** Animationen in einer FBX werden nicht eingelesen, und das Spiel animiert ein Mod-Modell nie.
- **Höchstens 32 MB** pro Modelldatei. Eine größere Datei wird mit einer Warnung übersprungen, und das Objekt behält seinen eingebauten Look.

### Was eine FBX enthalten darf { #what-an-fbx-may-contain }

Das Spiel liest FBX-Dateien selbst, versteht also weniger vom Format, als Blender schreiben kann:

- Meshes und die Hierarchie darüber, mit Position, Drehung und Skalierung. Versteckte Objekte werden weggelassen, und eine Datei ganz ohne Mesh wird ignoriert.
- Normalen so, wie sie exportiert wurden. Ein Mesh ohne Normalen bekommt weiche Normalen.
- **Nur die erste UV-Map.** Jede weitere UV-Map wird ignoriert, lege die UVs, die deine Texturen verwenden, also auf die erste.
- Flächen mit mehr als drei Ecken werden in Dreiecke zerlegt. Das ist nur bei flachen, konvexen Flächen exakt. Trianguliere ungewöhnliche Flächen vor dem Export, oder setze im FBX-Export von Blender den Haken bei **Triangulate Faces**.
- Pro Material: nur die Grundfarbe. Texturen, die am Material hängen, Vertex-Farben und alle anderen Materialeinstellungen werden nicht gelesen.
- **In die FBX eingebettete Bilder werden nie gelesen.** Liefere die Texturen als PNG-Dateien in `Objects/` mit (siehe [Texturen](#textures)).

## Texturen { #textures }

Texturen sind PNG-Dateien irgendwo in `Objects/`, gefunden über ihren Namen. Es gibt drei Arten, sie zu benennen. Das Spiel probiert sie in dieser Reihenfolge, und jede füllt nur, was die vorige leer gelassen hat:

| | Benenne die PNG nach | Beispiel | Braucht ein Modell |
|---|---|---|---|
| 1 | dem **Material** in deinem Modell: `<material>_BaseMap_<UDIM-Tile>` und `<material>_Specular_<UDIM-Tile>` | `MyChair_BaseMap_1001.png` für ein Material namens `MyChair` | ja |
| 2 | der **Textur, die das Material deines Modells verwendet** | `wood-01.png` für ein Material, das mit einem Bild namens `wood-01` bemalt ist | ja |
| 3 | einer **eingebauten Textur** des Spiels | `BedMetal_Toon-Main_BaseMap_1001.png` | nein |

Weg 1 ist für ein Modell der einfachste: Du musst in deinem 3D-Programm gar kein Bild mit dem Material verbinden. Gib Material und PNG einfach passende Namen. Wege 1 und 3 funktionieren nur mit dem Material des Spiels, und das ist die Voreinstellung (siehe [Material des Spiels oder dein eigenes](#game-material-or-your-own)).

### Die Textur, die ein Modell nennt { #the-texture-a-model-names }

Die Materialien eines Modells nennen die Bilder, die sie verwenden, und das Spiel sucht **irgendwo in `Objects/` nach einer PNG mit diesem Namen**. Ein Material, das ein Bild namens `wood-01` verwendet, bekommt `Objects/wood-01.png` (oder `Objects/irgendein/unterordner/wood-01.png`). Ordner und Dateiendung im gespeicherten Namen werden ignoriert, ein Material, das mit `C:\art\wood-01.jpg` bemalt ist, findet also trotzdem `wood-01.png`. Eine PNG kann beliebig vielen Modellen dienen und wird nur einmal geladen.

Die beiden Modellformate verhalten sich unterschiedlich, wenn keine passende PNG da ist:

| | `.glb` | `.fbx` |
|---|---|---|
| Gelesene Textur-Slots | Grundfarbe | Grundfarbe |
| Keine PNG mit diesem Namen in `Objects/` | das in die `.glb` eingebettete Bild wird verwendet | der Slot bleibt ohne Textur, und das [Log](../start/troubleshooting.md#find-the-playerlog) nennt die Textur, nach der gesucht wurde |
| Bilder außerhalb der Datei | abgelehnt: Eine `.glb` muss alles selbst enthalten | nie gelesen: Nur die PNGs in `Objects/` zählen |

Jede PNG in `Objects/`, deren Name nicht auf `.thumbnail` endet, zählt als Textur. Eine Textur, die weder ein Modell noch ein eingebautes Objekt verwendet, wird einfach nie geladen.

## Übermalen ohne Modell { #re-painting-without-a-model }

Eine PNG, die genauso heißt wie eine der Texturen des Spiels, **ersetzt diese Textur**, ganz ohne Modell. `Objects/BedMetal_Toon-Main_BaseMap_1001.png` übermalt das Metallbett überall, wo es auftaucht, auch seinen zerstörten Look. Jedes Objekt, das dieselbe Textur verwendet, ändert sich mit.

- Male über das Originalbild in derselben Größe und Aufteilung, denn das Modell bleibt das des Spiels.
- Die Texturnamen des Spiels sehen meist so aus: `<Material>_Toon-Main_BaseMap_<UDIM-Tile>` und `<Material>_Toon-Main_Specular_<UDIM-Tile>`. Die Texturnamen jedes Objekts stehen unter [Eingebaute Texturnamen](texture-names.md).
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

Standardmäßig wird dein Modell mit **dem Material des Spiels** für dieses Objekt gezeichnet, mit der Grundfarbtextur und der Grundfarbe deines Modells. Nur so zeigen sich Kampfschäden und die anderen Effekte, die das Spiel auf Objekte malt, auch auf deinem Modell. Specular Maps und UDIM-Kacheln werden ebenfalls verwendet.

Willst du das Material stattdessen genau so behalten, wie du es gebaut hast, schaltest du das Material des Spiels für dieses Objekt in `Objects/config.json` aus. Gelesen wird nur die `config.json` direkt in `Objects/`:

```json
{
  "Objects": {
    "Chair": { "UseGameMaterial": false }
  }
}
```

- Die Schlüssel sind Objekt-Ids wie in den Dateinamen, Groß- und Kleinschreibung egal.
- Ein Objekt mit `"UseGameMaterial": false` behält seinen vollen Look aus deinem 3D-Programm, **zeigt aber keine Kampfschäden**. Außerdem verwendet es nur die Textur, die sein Material nennt (Weg 2), ohne Specular Maps und UDIM-Kacheln.
- Auch mit `false` verwendet ein Material ohne Grundfarbtextur trotzdem das Material des Spiels und behält die Farbe, die du ihm gegeben hast.
- Eine `config.json`, die das Spiel nicht lesen kann, wird im [Log](../start/troubleshooting.md#find-the-playerlog) gemeldet, und jedes Objekt fällt auf die Voreinstellung zurück.

## Vorschaubilder { #thumbnails }

`<objectId>.thumbnail.png` ersetzt das Symbol des Objekts im Baumenü und überall sonst, wo dieses Symbol gezeigt wird.

- **Höchstens 512 × 512 Pixel** und höchstens 10 MB. Jede Seite zählt für sich, 512 × 256 geht also. Ein größeres Vorschaubild wird **nicht verkleinert**: Es wird mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog) übersprungen, und das Symbol des Spiels bleibt.
- Ein Vorschaubild wird nur **neben einem Modell mit derselben Id** verwendet. Es kann nicht das Symbol eines Objekts ändern, dem deine Mod kein neues Modell gibt; ein Vorschaubild allein wird gemeldet und ignoriert.
- Ein Vorschaubild pro Objekt. Eine zweite Datei mit demselben Namen in einem anderen Unterordner wird ignoriert.
- Kartenobjekte stehen nicht im Baumenü, und der Karteneditor behält die Symbole des Spiels. Ein Vorschaubild für ein Kartenobjekt wird deshalb nicht verwendet.

## Kartenobjekte { #map-objects }

Bäume, Felsen, Teiche und die anderen Objekte auf einer Karte bekommen einen neuen Look wie jedes andere Objekt: mit einer Datei in `Objects/`, die nach der Id des Objekts benannt ist. Jede Id eines Kartenobjekts und wie viele Varianten es hat, steht unter [Veränderbare Objekte](moddable-objects.md#map-objects). Ein paar Dinge laufen anders:

- **Varianten.** `flowers.glb` ändert alle drei Blumenbeete, `flowers.1.glb` nur das zweite. Varianten können ganz verschieden aussehen: `tree` umfasst die Nadelbäume und den Laubbaum gleichermaßen, und `tree.2` ist nur der Laubbaum.
- **Jede Baumgröße ist ein eigenes Objekt.** `tree_big`, `young_tree`, `young_tree_big`, `tree_big_log` und `tree_big_stump` brauchen jeweils eine eigene Datei. Ein junger Baum, der heranwächst, wird zu einem `tree` oder `tree_big` und trägt ab dann den Look dieses Objekts.
- **Ein Look für voll und leer.** `sand_pit`, `clay_pit`, `water_pond`, `berry_bush`, `herbs_plant`, `wild_grain`, `wild_beans`, `wild_potato` und `wild_tomato` wechseln zwischen einem vollen und einem leeren Modell, während deine Mannschaft sie aberntet. Dein Modell ersetzt beide, es sieht also gleich aus, egal wie viel noch übrig ist.
- **Geteilte Texturen.** Viele Kartenobjekte sind mit einer gemeinsamen Textur bemalt. Sandgrube, Lehmgrube, Teich, Beerenstrauch und andere verwenden alle `T_PP_ResourceMap_O4`. Wenn du eine geteilte Textur [übermalst](#re-painting-without-a-model), änderst du jedes Objekt, das sie verwendet. Um nur ein Objekt zu ändern, gib ihm ein Modell. Welche Texturen jedes Kartenobjekt verwendet, steht unter [Eingebaute Texturnamen](texture-names.md#map-objects).
- **Kein Ordner `TerrainObjects/`.** Kartenobjekte kommen wie alles andere in `Objects/`, und der Name des Unterordners bedeutet dort nichts: `Objects/sand_pit/model.fbx` ist ein Modell für ein Objekt namens `model`. Nenne es `sand_pit.fbx`.

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
- Ein Bild über seiner Grenze wird **nie verkleinert**. Es wird mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog) übersprungen, und das Spiel fällt zurück: Ein übersprungenes Vorschaubild lässt das Symbol des Spiels stehen, ein übersprungenes Biom den Boden des Spiels, und ein Material, dessen Textur übersprungen wurde, wird ohne sie gezeichnet.

## Mehrere Mods ändern dasselbe Objekt { #several-mods-changing-the-same-object }

Ändern zwei eingeschaltete Mods dasselbe Objekt, gewinnt die Mod, die **zuletzt** angewendet wird, nach der Ladereihenfolge (siehe [So funktionieren Mods](../basics/mods.md#which-mod-wins)). Das [Log](../start/troubleshooting.md#find-the-playerlog) vermerkt, welche Mod welche überschrieben hat. Ein Objekt wird als Ganzes entschieden: Das Modell einer Mod wird nie mit dem Vorschaubild einer anderen Mod für dasselbe Objekt kombiniert.

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

- Hast du **das Spiel neu gestartet**? Grafik wird nur beim Spielstart eingelesen.
- Ist die Mod unter **Hauptmenü -> Mods** eingeschaltet?
- Passt der Dateiname genau zu einer Id (abgesehen von Groß- und Kleinschreibung)? Verlässt du dich auf einen Unterordnernamen, der nichts bedeutet?
- Liegt jede Datei innerhalb der Grenzen oben, und ist jedes Bild eine echte PNG?
- Bei einer FBX: Liegen die Texturen als PNGs in `Objects/`, benannt nach dem Material oder nach dem Bild, das das Material verwendet?

Das Spiel schreibt, was es abgelehnt hat und warum (ein falscher Name, eine fehlende Textur, ein zu großes Bild), in die [`Player.log`](../start/troubleshooting.md#find-the-playerlog), in Zeilen, die mit `[Mod <your mod id>]` beginnen. Die ausführlichen Zeilen erscheinen eventuell nur in Entwicklungsversionen. Ist das Log still, geh die Liste oben durch und schau dir das Objekt im Spiel an.

Ein Modell, das nach einer Id benannt ist, die es nicht gibt (`sandpit.fbx` statt `sand_pit.fbx`), wird geladen, aber nie verwendet, und im Log steht nichts dazu. Bekommt ein Objekt dein Modell, steht im Log eine Zeile wie `[Mod my_mod] Objects/sand_pit: replaced 2 built-in renderer(s) on the regular view with ...`, sobald das erste davon im Spiel auftaucht. Fehlt diese Zeile, prüfe den Dateinamen anhand von [Veränderbare Objekte](moddable-objects.md).
