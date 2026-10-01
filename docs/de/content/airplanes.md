# Flugzeug-Skins

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
- Jeder andere Dateityp wird ignoriert, mit einer Warnung im Log.

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

Eine Lackierung wird weggelassen, mit einer Warnung im Log, wenn:

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
- Eine Textur darf höchstens 4096 × 4096 Pixel und 10 MB groß sein, dieselben Grenzen wie bei Objekt-Grafik (siehe [Objekte und Modelle](objects.md)). Eine Datei über der Grenze wird nicht verkleinert, sondern mit einer Warnung im Log übersprungen.

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

## Spielstände und ausgeschaltete Mods { #saves-and-disabled-mods }

Das Spiel speichert eine Mod-Lackierung unter der Id `mod_<modId>_<skinId>`, in Kleinbuchstaben. Dein `DesertRat` in der Mod `my_mod` wird also als `mod_my_mod_desertrat` gespeichert. Weil die Mod-Id darin steckt, kommen sich zwei Mods nie in die Quere, und deine Skin-Id braucht kein eigenes Präfix.

- Nennt ein Spielstand eine Lackierung, deren Mod nicht mehr eingeschaltet ist, bekommt das Flugzeug wieder seine erste Lackierung, und die Lackierung verschwindet aus den Standard- und Zufallseinstellungen der Flotte.
- Szenen, die ein Flugzeug außerhalb deines Stützpunkts zeigen, also das Abfangen beim Scramble und Absturzstellen, zeigen das eingebaute Aussehen des Flugzeugs. Das gilt genauso für die eingebauten Lackierungen.

## Änderungen sehen { #seeing-your-changes }

Lackierungen werden bei jedem Laden eines Levels gelesen. Ein Neustart ist nicht nötig.

| Du hast geändert... | So siehst du es |
|---|---|
| Ein Lackierungs-PNG oder `Airplanes/config.json` in einer Mod, die das Spiel schon kennt | Lade ein Level (einen Spielstand laden reicht). |
| Einen neuen Mod-Ordner oder einen `Airplanes/`-Ordner, der beim Spielstart leer war | Drücke im Mods-Fenster auf **Refresh** und lade dann ein Level. |

Mehr zum Testablauf unter [Testen und neu laden](../basics/testing.md).

## Das Log prüfen { #checking-the-log }

Das Spiel schreibt in `Player.log`, was es angenommen und was es abgelehnt hat (wo die Datei liegt: [So funktionieren Mods](../basics/mods.md)). Zeilen zu deiner Mod beginnen mit `[Mod <deine Mod-Id>]`. Taucht eine Lackierung nicht auf, such dort nach den oben beschriebenen Warnungen: eine übersprungene Lackierung, ein ignorierter Dateityp oder eine Textur über der Größengrenze.

!!! note
    Das veröffentlichte Spiel schreibt nur Fehler ins Log. Die ausführlichen `[Mod ...]`-Zeilen erscheinen nur in Entwickler-Builds. Steht im Log also nichts zu deiner Mod, prüfe die Lackierungsauswahl direkt im Spiel.
