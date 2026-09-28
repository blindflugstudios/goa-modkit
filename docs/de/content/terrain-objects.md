# Landschaftsobjekte

!!! warning "In Arbeit"
    Grafik-Mods sind noch in Arbeit. Die aktuelle Alpha unterstützt das noch nicht. Einen Ordner `TerrainObjects/` gibt es nicht mehr; Bäume, Felsen und andere Kartenobjekte bekommen ihren neuen Look über `Objects/`, siehe [Objekte und Modelle](objects.md).

<!-- OUTDATED (docs audit 2026-09-28): the whole page describes the removed TerrainObjects/ folder and is excluded from the build, see DOCS_AUDIT.md -->

Landschaftsobjekte sind die Dinge, die zur Landschaft gehören und nicht zu deinem Flugplatz: Bäume, Büsche, Felsen, Lehm- und Sandgruben, Teiche, wildes Getreide, alte Zäune und Gräber. Sie werden mit dem Werkzeug **Landschaftsobjekte** (Terrain Objects) im [Karten Editor](maps.md) auf eine Karte gesetzt.

Eine Mod kann jedem von ihnen einen neuen Look geben, auf allen Karten gleichzeitig. Das funktioniert genau wie der [Reskin von Objekten](objects.md), mit einer Ergänzung: Viele Landschaftsobjekte gibt es in mehreren Varianten, und du kannst alle Varianten gemeinsam oder jede einzeln ändern.

## Schnellstart { #quick-start }

Ersetze alle Bäume durch dein eigenes Modell:

```text
Mods/
  my_forest_mod/
    TerrainObjects/
      tree/
        model.glb
```

Ersetze nur den Laubbaum (Variante `2` von `tree`) und lass die anderen Bäume in Ruhe:

```text
Mods/
  my_forest_mod/
    TerrainObjects/
      tree/
        2/
          model.glb
```

Starte das Spiel neu und lade einen Spielstand oder starte eine Karte. Auch die Bäume, die schon auf der Karte stehen, ändern sich.

!!! note
    Wie jede Mod-Grafik werden Landschaftsobjekte einmal gelesen, beim Spielstart. Nachdem du eine Datei geändert oder die Mod ein- oder ausgeschaltet hast, **starte das Spiel neu**.

## So funktioniert es { #how-it-works }

In deiner Mod enthält `TerrainObjects/` einen Ordner pro Landschaftsobjekt, benannt nach seiner Id (siehe [Ids der Landschaftsobjekte](#terrain-object-ids)). Groß- und Kleinschreibung spielt keine Rolle.

- Dateien direkt in `TerrainObjects/<id>/` gelten für **jede** Variante dieses Objekts.
- Dateien in einem nummerierten Unterordner, `TerrainObjects/<id>/<variant>/`, gelten **nur für diese Variante** und haben für sie Vorrang vor dem übergeordneten Ordner.
- Ein Unterordner, dessen Name keine Zahl ist (`0`, `1`, `2`, ...), wird mit einer Warnung im Log ignoriert.
- Nutzt du nur Varianten-Unterordner, liegen im übergeordneten Ordner keine Dateien. Das Log vermerkt dann, dass `TerrainObjects/<id>` keine Dateien enthält und ignoriert wird; das ist harmlos, die Variantenordner laden trotzdem.

Jeder Ordner nimmt dieselben Dateien wie ein Objektordner:

| Datei | Was sie bewirkt |
|---|---|
| `model.glb` oder `model.fbx` | Ersetzt das Modell. |
| `albedo.png` | Die Farbtextur. Mit Modell: wird auf dein Modell gemalt. Ohne Modell: wird auf das Modell des Spiels gemalt. |
| `destroyed.glb` oder `destroyed.fbx` | Ersetzt den Look nach der Zerstörung, sofern das Objekt einen hat. |
| `destroyed_albedo.png` | Die Farbtextur für den zerstörten Look. |
| `config.json` | `{ "UseGameMaterial": true }`, um dein Modell mit dem Material des Spiels zu schattieren. |

Modellformate, Materialregeln, Texturregeln, die Knotennamen für Detailstufen (`LOD0`, `LOD1`, ...) und die Dateigrößengrenzen sind dieselben wie bei Objekten. Sie sind einmal erklärt, unter [Objekte und Modelle](objects.md#model-formats).

Nur das Aussehen ändert sich. Ob die Mannschaft einen Baum für Holz fällen, einen Busch absammeln, eine Grube ausheben oder aus einem Teich trinken kann, bleibt gleich.

### Bäume und Detailstufen { #trees-and-levels-of-detail }

Bäume wechseln auf einfachere Modelle und in weiter Ferne auf flache Ausschnitte, wenn sich die Kamera entfernt. Ersetzt du das Modell eines Baums, werden all diese ausgeblendet und dein Modell übernimmt. Gib deiner Datei Knoten `LOD0`, `LOD1`, ..., damit deine eigenen einfacheren Versionen bei denselben Entfernungen verwendet werden; ohne sie wird dein volles Modell gezeichnet, bis der Baum ohnehin verschwinden würde. Bei vielen Bäumen auf einer Karte macht eine einfache Fernstufe einen echten Unterschied für die Leistung.

Effekte, die am Objekt hängen, etwa fallende Blätter beim Fällen eines Baums, funktionieren weiter.

## Ids der Landschaftsobjekte { #terrain-object-ids }

| Id | Varianten | Was sie sind |
|---|---|---|
| `tree` | 0–4 | 0 Nadelbaum, 1 kahler Nadelbaum, 2 Laubbaum, 3 kahler Nadelbaum (zweiter), 4 Nadelbaum (zweiter) |
| `tree_big` | 0–1 | zwei große Eichen |
| `young_tree` | 0–1 | 0 junger Nadelbaum, 1 junger Laubbaum |
| `young_tree_big` | 0–1 | zwei junge große Eichen |
| `tree_big_log` | 0–1 | zwei umgestürzte Stämme |
| `tree_big_stump` | 0–1 | zwei Baumstümpfe |
| `bush` | 0–5 | 0–4 Büsche, 5 Wiesenkerbel |
| `bush_big` | 0 | Schlehe |
| `berry_bush` | 0 | Beerenstrauch |
| `herbs_plant` | 0 | Kräuterpflanze |
| `mushroom_patch` | 0 | Pilzstelle |
| `flowers` | 0–2 | drei Blumensorten |
| `small_rock` | 0–1 | 0 kleiner Felsen, 1 bemooster Felsen |
| `large_rock` | 0–1 | 0 großer Felsen, 1 großer bemooster Felsen |
| `long_rock` | 0 | langer bemooster Felsen |
| `sand_pit` | 0 | Sandgrube |
| `clay_pit` | 0 | Lehmgrube |
| `water_pond` | 0 | Teich |
| `wild_grain` | 0 | wildes Getreide |
| `wild_beans` | 0 | wilde Bohnen |
| `wild_potato` | 0 | wilde Kartoffeln |
| `wild_tomato` | 0 | wilde Tomaten |
| `damaged_car` | 0 | Autowrack |
| `old_fence` | 0 | alter Zaun |
| `old_fence_pole` | 0 | alter Zaunpfahl |
| `old_grave` | 0–1 | 0 Grabstein, 1 einfaches Kreuz |
| `old_headstone` | 0 | weißer Grabstein |
| `ocean` | 0 | das Meer |

Die Variantennummern sind die, die der Karten Editor setzt. Ein Objekt mit nur einer Variante nutzt `0`; bei ihm bewirken `TerrainObjects/<id>/` und `TerrainObjects/<id>/0/` dasselbe.

## Mehrere Mods, dasselbe Landschaftsobjekt { #several-mods-same-terrain-object }

Ändern zwei eingeschaltete Mods denselben Ordner, zum Beispiel haben beide `TerrainObjects/tree/`, gewinnt die zuletzt angewendete Mod, und das Log vermerkt, welche welche überschrieben hat. `TerrainObjects/tree/` und `TerrainObjects/tree/2/` zählen als verschiedene Ordner: Eine Mod kann alle Bäume ändern, während eine andere nur den Laubbaum ändert, und die Laubbaum-Mod gewinnt für Variante 2.

Landschaftsobjekte sind eine eigene Liste, getrennt von [Objekten](objects.md): `Objects/tree` würde die Bäume auf der Karte nicht berühren.

## Wenn etwas nicht auftaucht { #when-something-does-not-show-up }

Suche in `Player.log` nach Zeilen, die mit `[Mod <your mod id>] TerrainObjects/...` beginnen. Die Meldungen sind dieselben wie bei Objekten (siehe [die Tabelle auf der Objekte-Seite](objects.md#when-something-does-not-show-up)), plus eine eigene:

| Log-Zeile (gekürzt) | Bedeutung |
|---|---|
| `TerrainObjects/tree/broadleaf is not a variant index (0, 1, 2, …) and is ignored.` | Benenne Variantenordner nur mit der Zahl. |

Ein Variantenordner mit einer Nummer, die das Objekt nicht hat (etwa `tree/7`), wird nie verwendet, und es wird keine Zeile dafür geschrieben.
