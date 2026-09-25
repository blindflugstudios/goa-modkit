# Objekte und Modelle

Genug vom Standardfass? Eine Mod kann den Objekten, die du auf deinem Flugplatz baust, einen neuen Look geben: Möbel, Zäune, Geschütze, Schilder, Poster, Werkbänke und Trainingsgeräte. Entweder legst du ein neues 3D-Modell hinein, oder du behältst das Modell des Spiels und bemalst es mit einer neuen Textur.

Nur das Aussehen ändert sich. Größe im Raster, Kosten, was die Mannschaft mit dem Objekt anfangen kann und alle anderen Regeln bleiben so, wie das Spiel sie festlegt. Zahlen änderst du mit [CSV-Tabellen](../data/csv.md).

## Schnellstart { #quick-start }

Gib dem Fass ein neues Modell. Exportiere dein Modell als binäre glTF-Datei namens `model.glb` und lege sie hier ab:

```text
Mods/
  my_barrel_mod/
    Objects/
      Barrel/
        model.glb
```

Starte das Spiel neu und lade einen Spielstand. Jedes Fass, die schon stehenden und die neu gebauten, nutzt jetzt dein Modell.

Du willst das vorhandene Fass nur umfärben? Leg einfach nur eine Textur hinein:

```text
Mods/
  my_barrel_mod/
    Objects/
      Barrel/
        albedo.png
```

Das Spiel behält sein eigenes Fassmodell und malt statt der Originaltextur deine `albedo.png` darauf.

!!! note
    Modelle und Texturen werden einmal gelesen, beim Spielstart. Nachdem du eine Datei geändert, eine Mod ein- oder ausgeschaltet oder einen neuen Objektordner angelegt hast, **starte das Spiel neu**. Einen Spielstand zu laden reicht bei Grafik nicht.

## So funktioniert es { #how-it-works }

In deiner Mod enthält der Ordner `Objects/` einen Unterordner pro Objekt, das du ändern willst. Der Name des Unterordners ist die Id des Objekts (siehe [Welche Objekte sich ändern lassen](#which-objects-can-be-changed)); Groß- und Kleinschreibung spielt keine Rolle.

Jeder Objektordner darf diese Dateien enthalten. Alle sind optional, aber ein Ordner braucht mindestens eine der ersten vier:

| Datei | Was sie bewirkt |
|---|---|
| `model.glb` oder `model.fbx` | Ersetzt das Modell des Objekts. |
| `albedo.png` | Die Farbtextur. Mit Modell: wird auf dein Modell gemalt. Ohne Modell: wird auf das Modell des Spiels gemalt. |
| `destroyed.glb` oder `destroyed.fbx` | Ersetzt das Modell, das nach der Zerstörung des Objekts erscheint, zum Beispiel nach einem Bombenangriff. |
| `destroyed_albedo.png` | Die Farbtextur für den zerstörten Look, nach denselben Regeln wie `albedo.png`. |
| `config.json` | Einstellungen für dieses Objekt (siehe [config.json](#configjson)). |

Alles andere am Objekt bleibt, wie das Spiel es gebaut hat: wo die Mannschaft zum Benutzen steht, der Platz, den es einnimmt, Feuer- und Raucheffekte, Geräusche. Die Geistervorschau beim Platzieren zeigt bereits dein Modell.

### Zwei Wege zum Reskin { #two-ways-to-reskin }

**Neues Modell.** Dein Modell ersetzt das Modell des Spiels komplett. Sein Ursprung wird genau dorthin gesetzt, wo das Originalmodell sitzt, ohne zusätzliche Drehung oder Skalierung. Baue dein Objekt in derselben Größe und Ausrichtung wie das Original: Schau dir das Original im Spiel an und baue deins auf derselben Grundfläche.

**Nur Textur.** Ohne Modelldatei ersetzt `albedo.png` die Farbtextur auf jedem Material des Spielmodells. Das Spielmodell ist auf sein eigenes Texturlayout abgestimmt, deine Textur muss also diesem Layout folgen, damit es gut aussieht. Das eignet sich am besten zum Umfärben: ein dunklerer Ton, ein anderer Anstrich, Verwitterung.

### Der zerstörte Look { #the-destroyed-look }

Viele Objekte wechseln zu einem Wrack-Look, wenn sie zerstört werden. `destroyed.glb` / `destroyed.fbx` und `destroyed_albedo.png` ändern diesen Look auf dieselben zwei Arten. Hat ein Objekt gar keinen zerstörten Look, werden diese Dateien übersprungen und das Log sagt das. Lässt du sie weg, behält das Objekt den zerstörten Look des Spiels.

## Modellformate { #model-formats }

| Format | Dateiname | Hinweise |
|---|---|---|
| glTF binär | `model.glb`, `destroyed.glb` | Empfohlen. Materialien und eingebettete Texturen werden so verwendet, wie du sie angelegt hast. |
| FBX | `model.fbx`, `destroyed.fbx` | Nur Meshes und Materialfarben. Texturen in der FBX werden nicht gelesen; leg eine `albedo.png` daneben. |

Enthält ein Ordner sowohl `model.glb` als auch `model.fbx`, wird die `.glb` verwendet und das Log erwähnt die ignorierte `.fbx`.

### glTF (`.glb`)

- Nur die binäre Form `.glb` wird gelesen. Eine `.gltf`-Textdatei mit separaten `.bin`- und Bilddateien nicht.
- Die Datei muss **eigenständig** sein. Verweist eine `.glb` auf externe Dateien oder Webadressen, werden diese Verweise abgelehnt. Bette Texturen beim Export in die `.glb` ein (der glTF-Exporter von Blender macht das, wenn das Format auf *glTF Binary* steht).
- Materialien nutzen das übliche glTF-Metallic-Roughness-Modell. Ein solches Material behält sein eigenes Aussehen, solange es eine Farbtextur hat. Die Ausnahmen stehen unter [Materialien](#materials).

### FBX (`.fbx`)

- Das Spiel rechnet die Datei selbst auf Y nach oben und Meter um, anhand der Achsen- und Einheiteneinstellungen in der Datei. Eine FBX, die auf dem üblichen Weg aus Blender exportiert wurde, zeigt in dieselbe Richtung wie die Grafik des Spiels.
- Nur Meshes werden gelesen: keine Animation, kein Skinning, keine Kameras oder Lichter.
- Ausgeblendete Objekte in der Datei werden übersprungen.
- Eine UV-Map (die erste) wird gelesen.
- Flächen mit mehr als drei Ecken werden in Dreiecke zerlegt. Bei flachen, konvexen Flächen klappt das exakt; ungewöhnliche Flächen triangulierst du vor dem Export in deinem 3D-Programm.
- Von jedem Material wird nur die Grundfarbe gelesen (Diffuse-Farbe mal Diffuse-Faktor). Verlinkte oder eingebettete Texturen in der FBX werden ignoriert, und das Log erinnert dich daran, stattdessen eine `albedo.png` mitzuliefern.

### Größe, Ausrichtung und Detailstufen { #size-facing-and-levels-of-detail }

- Einheiten sind Meter, Y zeigt nach oben.
- Der Ursprung deines Modells landet auf dem Ursprung des Originalobjekts. Setz den Ursprung deines Modells dorthin, wo ihn das Original hat, meist auf den Boden in der Mitte des Objekts.
- **Detailstufen.** Wo das Originalobjekt in der Ferne auf einfachere Modelle wechselt, kann deins das auch. Benenne die Knoten in deiner Datei `LOD0`, `LOD1`, `LOD2` und so weiter (Groß- und Kleinschreibung egal, `LOD1_Barrel` zählt als `LOD1`). Das Spiel nutzt sie in dieser Reihenfolge bei den Umschaltentfernungen des Originals. Hast du weniger Stufen als das Original, bleibt deine letzte Stufe bis zum Schluss. Ohne `LOD`-Knoten wird das ganze Modell auf jede Entfernung gezeigt, und das Objekt verschwindet trotzdem dort, wo auch das Original verschwinden würde.

## Materialien { #materials }

Wie dein Modell im Spiel aussieht, hängt von seinen Materialien ab:

| Dein Material | Was das Spiel macht |
|---|---|
| glTF-Metallic-Roughness-Material **mit** Farbtextur | Bleibt genau so, wie du es angelegt hast. |
| Material **ohne** jede Farbtextur | Wird auf das Material des Originalobjekts übertragen, deine Grundfarbe bleibt erhalten. |
| Unlit- oder Specular-Glossiness-glTF-Material | Wird auf das Material des Originalobjekts übertragen, deine Farbtextur und Grundfarbe bleiben erhalten. |
| FBX-Material | Dieselben Regeln; da FBX-Texturen nicht gelesen werden, hat es keine Textur, außer du lieferst `albedo.png` mit. |
| Jedes Material, mit `"UseGameMaterial": true` in `config.json` | Wird auf das Material des Originalobjekts übertragen, deine Farbtextur und Grundfarbe bleiben erhalten. |

Eine `albedo.png` neben einem Modell ersetzt die Farbtextur auf allen seinen Materialien.

**Warum `UseGameMaterial`?** Das Spiel malt zur Laufzeit Effekte auf seine eigenen Materialien, am sichtbarsten die Risse von Kampfschäden. Ein Material, das du in deinem Modell angelegt hast, kann sie nicht zeigen. Setz `UseGameMaterial`, wenn dein Objekt Schäden zeigen soll wie die Originale; dafür gibst du die eigene Schattierung deines Modells auf (Metallic, Roughness, Normal Maps).

## `config.json`

Optional, im Ordner des Objekts:

```json
{
  "UseGameMaterial": true
}
```

| Schlüssel | Typ | Standard | Was er bewirkt |
|---|---|---|---|
| `UseGameMaterial` | true / false | `false` | Schattiert das Modell mit dem Material des Originalobjekts statt mit den Materialien in deiner Modelldatei. So funktionieren Kampfschäden und andere Spieleffekte weiter. |

Eine `config.json`, die nicht gelesen werden kann, wird im Log gemeldet, und jede Einstellung fällt auf ihren Standard zurück. Dein Modell und deine Texturen laden trotzdem.

## Texturen { #textures }

| Regel | Grenze |
|---|---|
| Format | Nur PNG. Andere Formate werden abgelehnt, auch wenn sie in `.png` umbenannt sind. |
| Größe | Höchstens 2048 × 2048 Pixel. |
| Dateigröße | Höchstens 8 MB. |
| Dateinamen | Genau `albedo.png` und `destroyed_albedo.png`. |

Texturen in einer `.glb` gehören zur Modelldatei und zählen stattdessen zur Modellgrenze.

## Grenzen { #limits }

| Was | Grenze |
|---|---|
| Modelldatei (`.glb` / `.fbx`) | 32 MB |
| PNG-Textur | 8 MB, 2048 × 2048 Pixel |

Eine Datei über einer Grenze wird mit einer Meldung im Log übersprungen; der Rest des Objektordners lädt trotzdem.

## Mehrere Mods ändern dasselbe Objekt { #several-mods-changing-the-same-object }

Haben zwei eingeschaltete Mods einen Ordner für dasselbe Objekt, gewinnt die zuletzt angewendete Mod und ersetzt die Grafik der anderen komplett; das Log vermerkt, welche Mod welche überschrieben hat. Die Reihenfolge ist unter [So funktionieren Mods](../basics/mods.md) beschrieben.

Objekte, [Landschaftsobjekte](terrain-objects.md) und [Biome](biomes.md) sind getrennt: Ein Ordner `Objects/tree` und ein Ordner `TerrainObjects/tree` beeinflussen sich nie gegenseitig.

## Welche Objekte sich ändern lassen { #which-objects-can-be-changed }

Der Ordnername ist die Id des Objekts, dieselbe Id, die das Objekt in der Spalte `ID` der Tabelle `BuildingComponents` hat (siehe [CSV-Tabellen](../data/csv.md)).

**Werkbänke:**

```text
Brickstation, CanningStation, CementMixer, Distillery, ElectronicsWorkbench, EspionageRadio, FieldKitchen,
HerbDryer, IndoorKitchen, MetalworksWorkbench, SawStation, TailorStation, WaterCooker
```

**Trainingsgeräte:**

```text
BombingAdvancedSimulator, BombingSimpleBench, EnduranceAdvancedBikeExerciser, EnduranceSimpleRack,
EngineeringAdvancedEngine, EngineeringSimpleMechanicWorkstation, FlyingAdvancedLinkTrainer,
FlyingSimpleWoodenConstruction, NavigationAdvancedNaviTrainer, NavigationSimpleBoard, ShootingAdvancedTurret,
ShootingSimpleTargetRange
```

**Möbel, Dekoration, Verteidigung und andere platzierbare Objekte:**

```text
AntitankPimple, BarbedWire, BarbedWireCorner, BarCounter, Barrel, BarStool, Bed, BedMetal, BedWood,
BilliardTable, BloodPackRack, Bofors40mm, Chair, Chalkboard, Clock, Clothesline, ClothingRack, ClothingStand,
ComfyChair, ComfyChairLarge, ControlTowerBrick, ControlTowerConcrete, ControlTowerMetal, CookingFire,
CrateEmpty, Cross, CurtainsClosedSmall, CurtainsOpenSmall, Dartboard, DividerCurtains, door_hangar, Drawer,
Flagpole10, Flagpole5, FlagpoleFloor, FlagpoleWall, Flowerbed01, Flowerbed02, FuelTank, Gramophone,
Gravestone, GravestoneWhite, Guitar, HandwashBowls, Hangers, Jukebox, KickstarterBackerMonument,
KickstarterCustomMonument, LiquorShelf, Lookout, MedicineCabinet, MetalBoxSmall, MetalFence,
MetalFenceCorner, MetalFenceEdge, MetalShelf, MetalShelfClosedClothes, MetalShelfClosedFiles, NightTable,
OerlikonGun, OxygenBottle, Piano, PilotBoard, PlanningBoard, PolishPilotsFlag, Poster, Poster01, Poster02,
Poster03, Poster04, Poster05, Poster06, Poster07, Poster08, Poster09, Poster10, Poster11, Poster12, Poster13,
Poster14, Poster15, Poster16, Poster17, Poster18, Poster19, Poster20, Poster21, Radio, RadioTower, Roadblock,
RollableScaffolding, RollableToolTable, RugBedrug, RugBedrugSmall, RugCubismrug, RugDoormat, RugJuterug,
RugKitchenrug, RugPersian, SandbagFence1mCorner, SandbagFence1mStraight, ScrambleBell, Searchlight, Shelf,
ShelfBooks, ShelfFolders, ShelfPersonalStuff, Sickbed, Siren, SirenOnPole, SmallFuelTank, SmallLoungeTable,
Stepladder, StoveSmall, TableMetal, TableOutdoor, TableTypewriter, Toilet, Toolbox, VickersGunAA, WallPhone,
WallSign1, WallSign2, WallSign3, WallSign4, WallSign5, WarningSign1, WarningSign2, WarningSign3,
WarningSign4, WarningSign5, WaterPump, WaterTower, WaySign1, WaySign2, WaySign3, WaySign4, WaySign5,
WickerChair, Windhose, WoodenChair, WoodenFenceSimple, WoodenFenceSimplePole, WoodenFenceSturdy,
WoodenFenceSturdyEdge, WoodenFenceSturdyPole, WoodenTableLarge, WoodenTableMedium, WoodenTableSmall
```

**Noch nicht möglich:** Wände, Böden, Dächer, Türen und Fenster von Gebäuden (`wall_wood`, `floor_brick` und so weiter), Parkplätze, Flugzeuge, Fahrzeuge und Figuren. Ein Ordner für eines davon wird gelesen, hat aber keine Wirkung. Bäume, Felsen und andere natürliche Objekte sind [Landschaftsobjekte](terrain-objects.md); der Boden selbst ist ein [Biom](biomes.md).

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

Was das Spiel mit deiner Grafik gemacht hat, schreibt es in `Player.log`:

| Plattform | Player-Log |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

Jede Zeile beginnt mit `[Mod <your mod id>]`, gefolgt vom Ordner, zum Beispiel `Objects/Barrel`. Zeilen, die du sehen kannst:

| Log-Zeile (gekürzt) | Bedeutung |
|---|---|
| `Objects/Barrel: replaced 3 built-in renderer(s) on the regular view with ...` | Dein Modell wird verwendet. |
| `Objects/Barrel: re-textured 2 material slot(s) on the regular view ...` | Dein reiner Textur-Reskin wird verwendet. |
| `Objects/Barrel contains none of model.glb or model.fbx, albedo.png, ... and is ignored` | Der Ordner enthält keine Datei mit einem Namen, nach dem das Spiel sucht. Prüfe die Schreibweise. |
| `Objects/Barrel ships both model.glb and model.fbx; model.glb is used.` | Entferne eine der beiden. |
| `Objects/Barrel/model.glb is 40 MB, over the 32 MB limit` | Mach die Datei kleiner. |
| `Objects/Barrel/albedo.png is 4096x4096, over the 2048x2048 limit` | Verkleinere die Textur. |
| `Objects/Barrel/albedo.png is not a PNG` | Speichere sie als echte PNG. |
| `Objects/Barrel/model.glb could not be read` | Die Datei ist kaputt oder kein binäres glTF. Exportiere sie neu. |
| `Objects/Barrel/model.fbx contains no mesh` | Die FBX hat keine sichtbare Geometrie. |
| `Objects/Barrel/config.json could not be read (...); every setting falls back to its default.` | Korrigiere das JSON. |
| `Objects/Barrel: this object has no destroyed view slot, its destroyed art is skipped.` | Dieses Objekt hat keinen zerstörten Look, der sich ersetzen ließe. |
| `Objects/Barrel cannot be re-dressed: ...` | Dieses Objekt unterstützt keinen Reskin. |
| `Objects/Barrel overrides the same skin from mod '...'` | Eine andere Mod ändert dasselbe Objekt; deine wird später angewendet und gewinnt. |
| `Imported art for 4 object(s).` | Zusammenfassung nach dem Spielstart (beginnt mit `[Mods]`). |

Gibt es gar keine Zeile für deinen Ordner, prüfe, ob der Ordnername einer Id aus der Liste oben entspricht und ob die Mod eingeschaltet ist.

!!! note
    Das veröffentlichte Spiel schreibt eventuell nur Fehler in `Player.log`, manche dieser Zeilen erscheinen also nur in Entwickler-Builds. Taucht nichts auf und das Aussehen ändert sich nicht, geh die Checkliste durch: Dateinamen, Ordnername, Dateigröße, Neustart.
