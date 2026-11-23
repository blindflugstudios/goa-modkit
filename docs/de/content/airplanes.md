# Flugzeug-Skins und neue Flugzeuge

Eine Lackierung (Skin) ist ein neuer Anstrich für ein Flugzeug, das es im Spiel schon gibt. Das Modell bleibt genau gleich; deine Mod bringt nur neue Bilder mit, die darauf gemalt werden. Du malst also auf das vorhandene UV-Layout des Flugzeugs (die flache Abwicklung, die festlegt, welcher Teil des Bildes wo auf dem Modell landet), dasselbe, das auch die eingebauten Lackierungen nutzen.

Eine Mod-Lackierung verhält sich wie eine eingebaute:

- Sie erscheint in jeder Lackierungsauswahl neben den eingebauten: im Panel des Flugzeugs, in den Standard- und Zufallseinstellungen der Flotte und im Bestellfenster.
- Sie ist von Anfang an freigeschaltet.
- Sie kommt mit der Aufgabe **Paint Airplane** aufs Flugzeug, wie jede andere Lackierung.
- Sie gehört zu dem Pool, aus dem die Zufallseinstellung wählt.

!!! tip "Beispieldateien"
    Beispieldateien für Flugzeug-Skins findest du im [Beispielordner auf Google Drive](https://drive.google.com/open?id=15fkBMoUdIB0wkL8wjuqEwflo2xZqbXni&usp=drive_fs). Nimm sie als Vorlage dafür, wie deine eigenen Dateien aussehen sollen.

## Schnellstart { #quick-start }

1. Lege einen Mod-Ordner mit einem Ordner `Airplanes/` darin an:

    ```text
    Mods/
      my_mod/
        Airplanes/
          config.json
          DesertRat_BaseMap_1001.png
    ```

2. Schreib das hier in `Airplanes/config.json`:

    ```json
    {
      "Skins": {
        "DesertRat": {
          "Airplane": "spitfire"
        }
      }
    }
    ```

3. Male `DesertRat_BaseMap_1001.png` auf das UV-Layout der Spitfire und speichere es als PNG.
4. Öffne **Hauptmenü → Mods** und drücke **Refresh**, damit das Spiel den neuen Mod-Ordner findet. Prüfe, dass **my_mod** eingeschaltet ist, und lade einen Spielstand.

Die Lackierung **DesertRat** steht jetzt in der Lackierungsauswahl der Spitfire.

## Der Ordner `Airplanes/` { #the-airplanes-folder }

Alles für deine Lackierungen liegt im Ordner `Airplanes/` der Mod:

```text
Mods/
  my_mod/
    Airplanes/
      config.json                   required - which skins the folder adds
      DesertRat_BaseMap_1001.png    required - base colour, tile 1001
      DesertRat_BaseMap_1002.png    optional - base colour, tile 1002
      DesertRat_Specular_1001.png   optional - specular colour, tile 1001
      DesertRat_Specular_1002.png   optional - specular colour, tile 1002
      DesertRat.thumbnail.png       optional - the skin's icon in the menus
```

- PNGs dürfen in Unterordnern von `Airplanes/` liegen, du kannst sie also sortieren, wie du willst. Das Spiel erkennt eine Datei allein an ihrem Namen.
- Groß- und Kleinschreibung spielt bei Dateinamen keine Rolle: `desertrat_basemap_1001.png` wird ebenfalls gefunden.
- Gelesen wird nur die `config.json`, die direkt in `Airplanes/` liegt. Eine `config.json` in einem Unterordner nicht.
- Jeder andere Dateityp wird ignoriert, mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog).

## `config.json` { #configjson }

`config.json` listet deine Lackierungen unter `Skins`. Jede Lackierung bekommt einen Eintrag, benannt nach ihrer **Skin-Id**. Die Skin-Id gibt auch den Texturen und dem Vorschaubild der Lackierung ihren Namen.

```json
{
  "Skins": {
    "DesertRat": {
      "Airplane": "spitfire",
      "Name": "Desert Rat",
      "BaseSkin": "Supermarine-Spitfire_MK09_Day-Fighter_Toon-UDIM"
    }
  }
}
```

| Schlüssel | Pflicht | Was er bewirkt |
|---|---|---|
| `Skins` | ja | Ein Eintrag pro Lackierung. Der Schlüssel jedes Eintrags ist die Skin-Id (hier `DesertRat`). |
| `Airplane` | ja | Das Flugzeug, auf das die Lackierung gemalt wird. Eine Id aus [Flugzeug-Ids](#airplane-ids). |
| `Name` | nein | Der Name, den die Lackierungsauswahl zeigt. Ein Text für alle Sprachen. Ohne ihn wird die Skin-Id angezeigt. |
| `BaseSkin` | nein | Die eingebaute Lackierung, von der deine ausgeht. Ihr Material wird kopiert, und jede Textur, die deine Mod nicht mitbringt, bleibt die dieser Lackierung. Ohne ihn wird die erste Lackierung des Flugzeugs genommen (siehe [Flugzeug-Ids](#airplane-ids)). |

!!! warning
    Die Datei muss gültiges JSON bleiben: keine Kommentare, keine Kommas am Ende.

### Wann eine Lackierung übersprungen wird { #when-a-skin-is-skipped }

Eine Lackierung wird weggelassen, mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog), wenn:

- sie kein `Airplane` nennt,
- das genannte `Airplane` nicht existiert,
- im Ordner keine `<skinId>_BaseMap_1001.png` liegt.

## Texturen { #textures }

Die Texturnamen folgen der Benennung der Spielgrafik, mit deiner Skin-Id davor. Größere Flugzeuge verteilen ihren Anstrich auf mehrere Bilder, sogenannte Kacheln (Tiles), nummeriert 1001, 1002 und 1003.

| Datei | Was sie bemalt |
|---|---|
| `<skinId>_BaseMap_1001.png` | Grundfarbe von Kachel 1001 (UVs mit U von 0 bis 1). **Pflicht.** |
| `<skinId>_BaseMap_1002.png`, `<skinId>_BaseMap_1003.png` | Grundfarbe von Kachel 1002 (U von 1 bis 2) und Kachel 1003 (U ab 2). |
| `<skinId>_Specular_1001.png`, `<skinId>_Specular_1002.png`, `<skinId>_Specular_1003.png` | Glanzfarbe (Specular) jeder Kachel. |

- Pflicht ist nur die Grundfarbe von Kachel 1001.
- Eine Kachel, die du weglässt, behält die Textur der Basis-Lackierung. So kannst du auch nur einen Teil eines Flugzeugs neu bemalen.
- Eine Kachel, für die das Material der Basis-Lackierung keinen Platz hat, wird ignoriert.
- Eine Textur darf höchstens 4096 × 4096 Pixel und 10 MB groß sein, dieselben Grenzen wie bei Objekt-Grafik (siehe [Objekte und Modelle](objects.md)). Eine Datei über der Grenze wird nicht verkleinert, sondern mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog) übersprungen.

### Vorschaubild { #thumbnail }

`<skinId>.thumbnail.png` ist das Symbol, das die Lackierungsauswahl für deine Lackierung zeigt, höchstens 512 × 512 Pixel und 10 MB. Es ist optional: Ohne eines wird das Symbol der Basis-Lackierung gezeigt.

## Flugzeug-Ids { #airplane-ids }

Diese Ids trägst du bei `Airplane` ein. Die zweite Spalte ist die erste Lackierung des Flugzeugs, die genommen wird, wenn du `BaseSkin` weglässt.

| `Airplane` | Erste (Standard-)Lackierung |
|---|---|
| `b17raf` | `b17raf_Boeing-B17_MK02_Temperate-Sea_Toon-UDIM` |
| `beaufighter` | `Bristol-Beaufighter_MK01_Temperate-Land_Toon-Opaque` |
| `blenheim` | `Bristol-Blenheim_MK04_Temperate-Land_Toon-Opaque` |
| `defiant` | `BoultonPaul-Defiant_MK01_Night_Toon-Opaque` |
| `flamingo` | `DeHavilland-Flamingo_MK01_Temperate-Land_Toon-Opaque` |
| `gladiator` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-UDIM` |
| `hampden` | `HandleyPage-Hampden_MK01_Night_Toon-Opaque` |
| `hurricane` | `Hawker-Hurricane_MK02_Day-Fighter_Toon-UDIM` |
| `kittyhawk` | `Curtiss-P40_E_Desert-Scheme_Toon-Opaque` |
| `lancaster` | `Avro-Lancaster_MK01_Night_Toon-UDIM` |
| `lysander` | `Westland-Lysander_MK03_Night_Toon-UDIM` |
| `meteor` | `Gloster-Meteor_MK03_Day-Fighter_Toon-Opaque` |
| `mosquito` | `DeHavilland-Mosquito_BMK04_Day-Fighter_Toon-UDIM` |
| `mustangmk1` | `mustangmk1_NorthAmerican-Mustang_MK01_Day-Fighter_Toon-UDIM` |
| `spitfire` | `Supermarine-Spitfire_MK09_Day-Fighter_Toon-UDIM` |
| `stirling` | `Short-Stirling_MK01_Night_Toon-UDIM` |
| `tempest` | `Hawker-Tempest_MK05_Day-Fighter_Toon-UDIM` |
| `typhoon` | `Hawker-Typhoon_MK01B_Day-Fighter_Toon-UDIM` |
| `vampire` | `DeHavilland-Vampire_MK01_Day-Fighter_Toon-Opaque` |

## Neue Flugzeuge (in Arbeit) { #new-airplanes }

Eine Mod kann auch einen ganz neuen Flugzeugtyp hinzufügen: mit eigenem Modell, eigener Lackierung, eigenem Namen, eigenen Werten und eigener Zeichnung im Crew-Fenster. Jedes neue Flugzeug ist **an eines der Flugzeuge des Spiels angelehnt** und übernimmt von diesem alles, was du ihm nicht mitgibst: Werte, Besatzung, Absturzanimation, das Aussehen im Scramble-Ergebnis und die Seriennummern-Blöcke. Mitgeben musst du nur das Modell.

!!! tip "Beispiel-Mods"
    `examples/airplane_captured_bf109` fügt einen erbeuteten Jäger Bf 109 hinzu, angelehnt an die Spitfire. `examples/airplane_captured_he111` fügt einen erbeuteten Bomber He 111 hinzu, angelehnt an die Stirling, mit zwei Propellern und einer fünfköpfigen Besatzung, die `Crew` und `CrewSlots` festlegen. Kopiere eine davon in deinen Ordner `Mods/`, um ein vollständiges neues Flugzeug im Spiel zu sehen.

### Der Ordner des Flugzeugs { #the-airplanes-own-folder }

Jedes neue Flugzeug bekommt in `Airplanes/` einen Ordner, der nach der Id des Flugzeugs heißt:

```text
Mods/
  my_mod/
    Airplanes/
      config.json
      Bf109/
        Bf109.fbx                 Pflicht - das Modell (.fbx oder .glb)
        Bf109.destroyed.fbx       optional - das Wrack
        Bf109_BaseMap_1001.png    optional - die Lackierung, weitere Kacheln und Specular wie bei einem Skin
        Bf109.thumbnail.png       optional - das Bild im Bestellfenster und in den Flugzeuglisten
        Bf109.blueprint.png       optional - die Zeichnung im Crew-Fenster
```

Ohne Lackierung zeigt das Modell die erste Lackierung des Vorbilds; ohne Wrack wird das Wrack des Vorbilds verwendet; ohne Vorschaubild oder Zeichnung werden die des Vorbilds gezeigt. Das Vorschaubild darf höchstens 512 × 512 Pixel und 10 MB groß sein; ein größeres wird mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog) übersprungen, und das Bild des Vorbilds wird gezeigt.

### `config.json` { #airplane-configjson }

Neue Flugzeuge stehen unter `Airplanes` in derselben `Airplanes/config.json` wie deine Lackierungen:

```json
{
  "Airplanes": {
    "Bf109": {
      "BasedOn": "spitfire",
      "Name": "Captured Bf 109",
      "FullName": "Messerschmitt Bf 109 E (captured)",
      "Stats": { "Health": "90" },
      "CrewSlots": [[0.45, 0.48]]
    }
  }
}
```

| Schlüssel | Pflicht | Was er bewirkt |
|---|---|---|
| `BasedOn` | ja | Das Flugzeug des Spiels, an das das neue angelehnt ist. Eine Id aus den [Flugzeug-Ids](#airplane-ids). |
| `Name` | nein | Der Name, den das Spiel zeigt. Ein Text für alle Sprachen. Ohne ihn wird die Id des Flugzeugs gezeigt. |
| `FullName`, `ShortName` | nein | Langer und kurzer Name, gezeigt im Bestell- und im Crew-Fenster. Ohne sie wird `Name` verwendet. |
| `Manufacturer`, `Armament`, `MaximumSpeed`, `Engine`, `Range`, `Ceiling`, `Dimensions` | nein | Die Angaben, die das Bestellfenster auflistet. Ohne Angabe leer. |
| `Stats` | nein | Werte, die vom Vorbild abweichen, mit den Spaltennamen der Flugzeugtabelle des Spiels als Schlüssel (`Health`, `Crew`, `Fuel Capacity`, ...). Die Werte sind Text: `"Health": "90"`, `"Crew": "Pilot,Gunner"`. |
| `CrewSlots` | nein | Wo der Platz jedes Besatzungsmitglieds auf der Zeichnung liegt, in Besatzungsreihenfolge, als `[x, y]`-Anteile der Zeichnung: `[0, 0]` ist die Ecke unten links, `[1, 1]` die oben rechts. Plätze, die du weglässt, werden in der Mitte verteilt. |

Auch eine Lackierung kann für dein neues Flugzeug gelten: Schreib die Id des Flugzeugs aus `Airplanes` (hier `Bf109`) als `Airplane` der Lackierung.

### Die Teile des Modells benennen { #naming-the-parts-of-the-model }

Das Spiel findet die Teile deines Modells über die Namen der Knoten. Groß- und Kleinschreibung, `-`, `_`, `.` und Leerzeichen spielen keine Rolle, `Air-Pivot`, `air_pivot` und `AirPivot` sind also dasselbe. Die Flugzeuge des Spiels verwenden genau diese Namen, du kannst dir also eines in deinem 3D-Programm ansehen.

| Knotenname | Was das Spiel damit macht | Ohne ihn |
|---|---|---|
| `Air-Pivot` | Der Teil, der sich im Flug neigt. Hänge alles darunter, was sich mit dem Flugzeug bewegt. | Dein Modell neigt sich mit dem Pivot des Vorbilds. |
| `Propeller-Pivot` (einer pro Propeller, z. B. `Propeller-Left-Pivot`) | Dreht sich um seine eigene Vorwärtsachse, solange der Motor läuft. | Kein Propeller dreht sich. |
| `Wheel-Left`, `Wheel-Right`, `Wheel-Tail` | Aus der Stelle, an der sie den Boden berühren, wird der Winkel berechnet, in dem das Flugzeug am Boden steht. | Der Winkel des Vorbilds wird verwendet. |
| `1-Interaction-Pilot`, `2-Interaction-Gunner`, ... | Die Sitze der Besatzung, in der Reihenfolge der vorangestellten Zahl. | Die Sitze des Vorbilds. |
| `Interaction-Paint` | Wo die Crew steht, um das Flugzeug zu lackieren und zu betanken. Setze ihn neben den Rumpf. Nur seine Stelle am Boden zählt: Die Crew steht auf dem Boden darunter, zum Rumpf gewandt, egal wie weit sich das Flugzeug geparkt auf seinen Rädern nach hinten neigt. Seine Höhe und Drehung spielen keine Rolle. | Die Stelle des Vorbilds. |
| `FireEmitter` | Das Mesh, auf dem Feuer brennt. | Das größte Teil direkt unter `Air-Pivot`, das weder Glas noch Innenraum ist. |

- **Größe und Ausrichtung.** Baue das Flugzeug in Metern in seiner echten Größe, am Ursprung auf dem Boden stehend, wie die Flugzeuge des Spiels. In welche Richtung die Nase zeigt, ist egal, wenn das Modell einen Knoten `Propeller...` und einen Knoten `Wheel-Tail` hat: Ein Flugzeug, dessen Propeller hinter dem Spornrad liegt, wird umgedreht.
- **Fahrwerk.** Ein einziehbares Fahrwerk braucht eine Animation (Take) in der Modelldatei, die nur die Fahrwerksteile animiert. Ihr erstes Bild ist das ausgefahrene Fahrwerk, so wie modelliert; ihr letztes Bild das ganz eingezogene. Das Spiel hält die Animation je nach Flughöhe dazwischen: am Boden ausgefahren, ab 10 m eingezogen. Animiere weder die Propeller noch `Air-Pivot`; die bewegt das Spiel selbst. Festes Fahrwerk: keine Animation.
- **Markierungs-Decals** (Staffelkennungen, Kokarden, Seriennummer) erscheinen nur, wo dein Modell Markierungspunkte hat, siehe [Markierungspunkte](#marking-points).

### Effektpunkte { #effect-points }

Die Effekte des Flugzeugs kommen vom Vorbild und sitzen dort, wo sie am Vorbild sitzen. Bei einem Modell anderer Größe landet der Radstaub neben den Rädern und der Rauch weit weg vom Motor. Setze an jede Stelle, an die ein Effekt gehört, einen leeren Knoten (ohne Mesh) in dein Modell und benenne ihn wie unten; das Spiel verschiebt den Effekt dorthin. Alle sind optional: Ein Effekt ohne Punkt bleibt, wo das Vorbild ihn hat. Nur die Position zählt, die Drehung des Knotens und seine Stelle in der Hierarchie spielen keine Rolle: Die Effekte bewegen sich immer mit `Air-Pivot`.

| Knotenname | Effekt | Wann er erscheint | Einer oder mehrere |
|---|---|---|---|
| `Effect-WheelDust-...` (z. B. `Effect-WheelDust-Left`, `-Right`, `-Tail`) | Staub, den ein Rad aufwirbelt. Setze ihn dorthin, wo der Reifen den Boden berührt. | Solange das Flugzeug am Boden rollt. | Einer pro Punkt |
| `Effect-WingTrail-...` (z. B. `Effect-WingTrail-Left`, `-Right`) | Die dünne Spur hinter einer Flügelspitze. | Im Flug. | Einer pro Punkt |
| `Effect-Exhaust-...` | Abgasstrahl eines Düsentriebwerks. Setze ihn an die Düse. Erscheint nur, wenn das Vorbild ein Düsenflugzeug ist (`meteor`, `vampire`). | Solange das Triebwerk läuft. | Einer pro Punkt |
| `Effect-Sparks` | Funken eines beschädigten Flugzeugs. | Unter der Hälfte der Gesundheit. | Einer |
| `Effect-Smoke` | Rauch aus einem getroffenen Motor. | Bei einer Landung mit rauchendem Motor. | Einer |
| `Effect-SmokeTrail` | Eine dicke Rauchfahne. | Solange das Flugzeug außer Gefecht ist. | Einer |
| `Effect-Explosion` | Die Explosion eines Absturzes. Setze sie vor dem Flugzeug auf den Boden. | Wenn das Flugzeug bei der Landung oder beim Verschieben verunglückt. | Einer |
| `Effect-FireSmoke` | Der Rauch über einem brennenden Flugzeug. | Solange das Flugzeug brennt. | Einer |

- **Einer pro Punkt:** Das Spiel macht für jeden Punkt eine Kopie des Effekts, ein zweimotoriges Flugzeug kann also `Effect-Exhaust-Left` und `Effect-Exhaust-Right` haben. Alle Kopien sind derselbe Effekt: der erste dieser Art am Vorbild.
- **Einer:** Nur der erste Knoten mit genau diesem Namen wird verwendet.
- **Feuer** braucht keinen Punkt: Es brennt auf dem Mesh `FireEmitter` (siehe Tabelle oben).
- **Nur die Effekte des Vorbilds.** Die Punkte verschieben Effekte; sie können keinen hinzufügen. Ein neues Flugzeug hat genau die Effekte des Flugzeugs, auf dem es basiert: einen Abgasstrahl nur, wenn es auf `meteor` oder `vampire` basiert, Flügelspuren nur, wenn das Vorbild welche hat. Wähle `BasedOn` danach aus.

### Markierungspunkte { #marking-points }

Ein neues Flugzeug trägt die Markierungs-Decals des Flugzeugs, auf dem es basiert, in dessen Stil, Größen und Farben: die Staffelkennung, den eigenen Buchstaben des Flugzeugs, die Kokarden, den Seitenleitwerksstreifen und die Seriennummer. Das Spiel kann nicht wissen, wohin sie auf deinem Modell gehören, deshalb zeigt es eine Markierung nur dort, wo dein Modell eine Stelle dafür nennt. Setze für jede gewünschte Markierung einen leeren Knoten (ohne Mesh) in dein Modell und nenne ihn `Marking-<Seite>-<Platz>`, zum Beispiel `Marking-Port-Image`. Jeder Punkt ist optional: Eine Markierung ohne Punkt wird nicht gezeigt, und ein Modell ganz ohne Markierungspunkte zeigt keine Markierungen. Die Markierungen stattdessen in die Textur zu malen geht weiterhin.

| Platz | Was er zeigt |
|---|---|
| `LeftText` | Die Staffelkennung, der Teil der Kennung vor dem `-` (`U5` von `U5-G`). |
| `Image` | Die Kokarde am Rumpf. |
| `RightText` | Den eigenen Buchstaben des Flugzeugs, der Teil der Kennung nach dem `-` (`G` von `U5-G`). |
| `Nose` | Das Nasenbild des Stils, falls er eines hat. |
| `Wing` | Die Kokarde oben auf dem Flügel. |
| `UnderWing` | Die Kokarde unter dem Flügel. |
| `FinFlash` | Den Streifen am Seitenleitwerk. |
| `SerialNumber` | Die Seriennummer des Flugzeugs, z. B. `PT255`. |

- **Seiten.** `<Seite>` ist `Port` (die linke Seite, vom Pilotensitz aus gesehen) oder `Starboard` (die rechte Seite). Jede Seite braucht eigene Punkte: `Marking-Port-Wing` und `Marking-Starboard-Wing` für die beiden Flügel.
- **Einen Punkt setzen.** Setze den Punkt auf die Oberfläche. Seine Vorwärtsachse (+Z in Unity) zeigt ins Flugzeug hinein, in die Richtung, in die die Markierung projiziert wird; seine rechte Achse (+X in Unity) ist die Leserichtung des Textes. Bei `Wing` zeigt die Vorwärtsachse nach unten in den Flügel, bei `UnderWing` nach oben hinein. Dein 3D-Programm benennt diese Achsen womöglich anders, prüfe das Ergebnis daher im Spiel.
- **Größe.** Die Markierungen behalten die Größen des Vorbilds; die Skalierung des Punkts ändert sie nicht.
- **Kennungen und Seriennummern** kommen vom Spiel: Jedes Flugzeug bekommt bei seiner Ankunft seine Staffelkennung, seinen Buchstaben und eine Seriennummer. Wenn du Punkte dafür setzt, male sie nicht zusätzlich in deine Textur, sonst erscheinen beide.

### Wo ein neues Flugzeug auftaucht { #where-a-new-airplane-shows-up }

Das Spiel kennt ein neues Flugzeug als `mod_<modId>_<id>`, in Kleinbuchstaben: Die `Bf109` der Mod `captured_bf109` ist `mod_captured_bf109_bf109`. Es ist von Anfang an freigeschaltet, erscheint im Bestellfenster und ist bei Absturzstellen, im Crew-Fenster und bei Scrambles dabei wie jedes andere Flugzeug. Quests und Promo-Codes kennen es nicht.

## Spielstände und ausgeschaltete Mods { #saves-and-disabled-mods }

Das Spiel speichert eine Mod-Lackierung unter der Id `mod_<modId>_<skinId>`, in Kleinbuchstaben. Dein `DesertRat` in der Mod `my_mod` wird also als `mod_my_mod_desertrat` gespeichert. Weil die Mod-Id darin steckt, kommen sich zwei Mods nie in die Quere, und deine Skin-Id braucht kein eigenes Präfix.

- Nennt ein Spielstand eine Lackierung, deren Mod nicht mehr eingeschaltet ist, bekommt das Flugzeug wieder seine erste Lackierung, und die Lackierung verschwindet aus den Standard- und Zufallseinstellungen der Flotte.
- Enthält ein Spielstand ein neues Flugzeug, dessen Mod nicht mehr eingeschaltet ist, wird daraus das Flugzeug, an das es angelehnt war. Schaltest du die Mod später wieder ein, wird es nicht zurückverwandelt.
- Szenen, die ein Flugzeug außerhalb deines Stützpunkts zeigen, also das Abfangen beim Scramble und Absturzstellen, zeigen das eingebaute Aussehen des Flugzeugs. Das gilt genauso für die eingebauten Lackierungen.

## Änderungen sehen { #seeing-your-changes }

Lackierungen werden bei jedem Laden eines Levels gelesen. Ein Neustart ist nicht nötig.

| Du hast geändert... | So siehst du es |
|---|---|
| Ein Lackierungs-PNG oder `Airplanes/config.json` in einer Mod, die das Spiel schon kennt | Lade ein Level (einen Spielstand laden reicht). |
| Einen neuen Mod-Ordner oder einen `Airplanes/`-Ordner, der beim Spielstart leer war | Drücke im Mods-Fenster auf **Refresh** und lade dann ein Level. |

Mehr zum Testablauf unter [Testen und neu laden](../basics/testing.md).

## Das Log prüfen { #checking-the-log }

Das Spiel schreibt in [`Player.log`](../start/troubleshooting.md#find-the-playerlog), was es angenommen und was es abgelehnt hat. Zeilen zu deiner Mod beginnen mit `[Mod <deine Mod-Id>]`. Taucht eine Lackierung nicht auf, such dort nach den oben beschriebenen Warnungen: eine übersprungene Lackierung, ein ignorierter Dateityp oder eine Textur über der Größengrenze.

!!! note
    Das veröffentlichte Spiel schreibt nur Fehler ins Log. Die ausführlichen `[Mod ...]`-Zeilen erscheinen nur in Entwickler-Builds. Steht im [Log](../start/troubleshooting.md#find-the-playerlog) also nichts zu deiner Mod, prüfe die Lackierungsauswahl direkt im Spiel.
