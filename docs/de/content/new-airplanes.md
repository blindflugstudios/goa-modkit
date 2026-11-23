# Neue Flugzeuge (in Arbeit)

!!! warning "In Arbeit"
    Neue Flugzeuge sind noch im Bau. Sie sind noch nicht im veröffentlichten Spiel, und Einzelheiten auf dieser Seite können sich ändern.

Eine Mod kann einen ganz neuen Flugzeugtyp hinzufügen: mit eigenem Modell, eigener Lackierung, eigenem Namen, eigenen Werten und eigener Zeichnung im Crew-Fenster. Jedes neue Flugzeug ist **an eines der Flugzeuge des Spiels angelehnt** und übernimmt von diesem alles, was du ihm nicht mitgibst: Werte, Besatzung, Absturzanimation, das Aussehen im Scramble-Ergebnis und die Seriennummern-Blöcke. Mitgeben musst du nur das Modell.

Ein neuer Anstrich für ein Flugzeug, das es im Spiel schon gibt, ist eine Lackierung, kein neues Flugzeug: siehe [Flugzeug-Skins](airplanes.md).

!!! tip "Beispiel-Mods"
    `examples/airplane_captured_bf109` fügt einen erbeuteten Jäger Bf 109 hinzu, angelehnt an die Spitfire. `examples/airplane_captured_he111` fügt einen erbeuteten Bomber He 111 hinzu, angelehnt an die Stirling, mit zwei Propellern und einer fünfköpfigen Besatzung, die `Crew` und `CrewSlots` festlegen. Kopiere eine davon in deinen Ordner `Mods/`, um ein vollständiges neues Flugzeug im Spiel zu sehen.

## Der Ordner des Flugzeugs { #the-airplanes-folder }

Jedes neue Flugzeug bekommt im Ordner `Airplanes/` der Mod einen Ordner, der nach der Id des Flugzeugs heißt:

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

Ohne Lackierung zeigt das Modell die erste Lackierung des Vorbilds; ohne Wrack wird das Wrack des Vorbilds verwendet; ohne Vorschaubild oder Zeichnung werden die des Vorbilds gezeigt. Die Kacheln und Specular-Dateien der Lackierung heißen wie bei einem Skin, siehe [Texturen](airplanes.md#textures). Das Vorschaubild darf höchstens 512 × 512 Pixel und 10 MB groß sein; ein größeres wird mit einer Warnung im [Log](../start/troubleshooting.md#find-the-playerlog) übersprungen, und das Bild des Vorbilds wird gezeigt.

## `config.json` { #configjson }

Neue Flugzeuge stehen unter `Airplanes` in der `Airplanes/config.json` der Mod, derselben Datei, die die [Lackierungen](airplanes.md#configjson) auflistet:

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
| `BasedOn` | ja | Das Flugzeug des Spiels, an das das neue angelehnt ist. Eine Id aus den [Flugzeug-Ids](airplanes.md#airplane-ids). |
| `Name` | nein | Der Name, den das Spiel zeigt. Ein Text für alle Sprachen. Ohne ihn wird die Id des Flugzeugs gezeigt. |
| `FullName`, `ShortName` | nein | Langer und kurzer Name, gezeigt im Bestell- und im Crew-Fenster. Ohne sie wird `Name` verwendet. |
| `Manufacturer`, `Armament`, `MaximumSpeed`, `Engine`, `Range`, `Ceiling`, `Dimensions` | nein | Die Angaben, die das Bestellfenster auflistet. Ohne Angabe leer. |
| `Stats` | nein | Werte, die vom Vorbild abweichen, mit den Spaltennamen der Flugzeugtabelle des Spiels als Schlüssel (`Health`, `Crew`, `Fuel Capacity`, ...). Die Werte sind Text: `"Health": "90"`, `"Crew": "Pilot,Gunner"`. |
| `CrewSlots` | nein | Wo der Platz jedes Besatzungsmitglieds auf der Zeichnung liegt, in Besatzungsreihenfolge, als `[x, y]`-Anteile der Zeichnung: `[0, 0]` ist die Ecke unten links, `[1, 1]` die oben rechts. Plätze, die du weglässt, werden in der Mitte verteilt. |

Auch eine Lackierung kann für dein neues Flugzeug gelten: Schreib die Id des Flugzeugs aus `Airplanes` (hier `Bf109`) als `Airplane` der Lackierung.

## Die Teile des Modells benennen { #naming-the-parts-of-the-model }

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

## Effektpunkte { #effect-points }

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

## Markierungspunkte { #marking-points }

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

## Wo ein neues Flugzeug auftaucht { #where-a-new-airplane-shows-up }

Das Spiel kennt ein neues Flugzeug als `mod_<modId>_<id>`, in Kleinbuchstaben: Die `Bf109` der Mod `captured_bf109` ist `mod_captured_bf109_bf109`. Es ist von Anfang an freigeschaltet, erscheint im Bestellfenster und ist bei Absturzstellen, im Crew-Fenster und bei Scrambles dabei wie jedes andere Flugzeug. Quests und Promo-Codes kennen es nicht.

## Spielstände und ausgeschaltete Mods { #saves-and-disabled-mods }

Enthält ein Spielstand ein neues Flugzeug, dessen Mod nicht mehr eingeschaltet ist, wird daraus das Flugzeug, an das es angelehnt war. Schaltest du die Mod später wieder ein, wird es nicht zurückverwandelt.

## Änderungen sehen { #seeing-your-changes }

Neue Flugzeuge werden wie Lackierungen bei jedem Laden eines Levels gelesen: Lade einen Spielstand, um ein geändertes Modell, eine geänderte Textur oder `config.json` zu sehen. Bei einem neuen Mod-Ordner drücke vorher im Mods-Fenster auf **Refresh**. Mehr unter [Änderungen sehen](airplanes.md#seeing-your-changes) und [Testen und neu laden](../basics/testing.md).
