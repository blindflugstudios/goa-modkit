# Karten

Eine Karte ist das Stück englische Landschaft, auf dem dein Flugplatz steht: die Form des Geländes, die Felder und Wege, die darauf gemalt sind, Bäume und Felsen, alles, was dort schon steht, dazu ein paar Einstellungen wie das Startdatum und die Mannschaft, mit der du beginnst. Jede Karte ist eine einzelne Datei mit der Endung `.goamap`.

Karten baust du mit dem **Karten Editor** (Map Editor), der im Spiel enthalten ist, und du lieferst sie im Ordner `Maps/` einer Mod aus. Eine Karte kann außerdem festlegen, welche Missionen auf ihr auftauchen dürfen (über Tags) und mit welcher Questreihe sie startet.

## Schnellstart { #quick-start }

1. Klicke im Hauptmenü (Main menu) auf **Karten Editor**, dann auf **Neue Karte** (New Map). Forme das Gelände, bemale es, setze ein paar Bäume.
2. Öffne die **Karteneinstellungen** (Map settings) und fülle mindestens **Ortsname:** (Name of Location) aus. Speichere die Karte mit **Speichern als...** (Save as...) und nenne sie `my_airfield`.
3. Der Editor schreibt `my_airfield.goamap` in den Ordner `Maps` in deinem Spieldatenordner (dem Ordner, in dem auch `Mods/` liegt, siehe Tabelle unten).
4. Kopiere diese Datei in eine Mod:

    ```text
    Mods/
      my_map_mod/
        Maps/
          my_airfield.goamap
    ```

5. Öffne **Hauptmenü → Mods** und drücke **Refresh**, damit das Spiel den neuen Mod-Ordner findet. Prüfe, dass **my_map_mod** eingeschaltet ist, und starte ein neues Spiel. Deine Karte steht unter **Custom maps**.

Das ist schon eine vollständige Karten-Mod. Eine `config.json` brauchst du nicht, du kannst aber eine hinzufügen (siehe [So funktionieren Mods](../basics/mods.md)).

| Plattform | Spieldatenordner (enthält `Mods/` und `Maps/`) |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/` |

!!! tip
    Gib der Datei einen Namen, den sonst niemand wählt, zum Beispiel mit dem Namen deiner Mod davor: `my_map_mod_airfield.goamap`. Der Dateiname ist die Id der Karte (siehe [Karten-Ids](#map-ids)).

## Der Karten Editor { #the-map-editor }

Klicke im Hauptmenü auf **Karten Editor**. In einem Fenster startest du eine **Neue Karte** oder lädst eine vorhandene.

Der Editor hat für jeden Teil der Karte ein eigenes Werkzeug:

| Werkzeug | Was du damit machst |
|---|---|
| **Landschaftshöhe** (Terrain Height) | Gelände anheben und absenken. |
| **Biomes** | Den Bodentyp malen: Gras, Erde, Straße, Fels, Sand, Kies. Der Bodentyp wirkt sich auch aufs Spiel aus, siehe [Biome](biomes.md). |
| **Gras** (Grass) | Gras auf den Boden malen oder entfernen. |
| **Landschaftsobjekte** (Terrain Objects) | Bäume, Büsche, Felsen, Teiche und mehr setzen, einzeln oder mit einem Pinsel. |
| **Karteneinstellungen** | Name, Beschreibung, Tags, Start-Quests, Startdatum und Startvorräte der Karte (siehe unten). |

**Rückgängig machen** (Undo) und **Wiederholen** (Redo) funktionieren wie gewohnt. Die Tastenkürzel listet der Editor unter **Shortcuts** auf.

### Speichern { #saving }

**Speichern** (Save) überschreibt die geladene Karte, **Speichern als...** fragt nach einem neuen Namen. Karten landen im Ordner `Maps` in deinem Spieldatenordner.

Die mitgelieferten Karten und Karten aus einer Mod sind schreibgeschützt: Du kannst sie im Editor laden, deine Änderungen aber nur mit **Speichern als...** unter neuem Namen sichern. Um eine Karte in deiner Mod zu aktualisieren, bearbeitest du die Kopie in deinem Ordner `Maps` und kopierst sie wieder über die Datei in `Mods/<deine Mod>/Maps/`.

### Karteneinstellungen { #map-settings }

Jedes Feld in den **Karteneinstellungen** wird in der `Metadata.json` der Karte gespeichert (siehe [Referenz](#metadatajson-reference)):

| Feld im Editor | Schlüssel in `Metadata.json` | Hinweise |
|---|---|---|
| **Ortsname:** | `Name` | Wird in der Kartenliste angezeigt. |
| **Beschreibung:** (Description:) | `Description` | Wird angezeigt, wenn die Karte ausgewählt ist. |
| **Tags** | `_tags` | Durch Kommas getrennt: `default, my_campaign`. Legt fest, welche Missionen auftauchen dürfen, siehe [Tags und Missionen](#tags-and-missions). |
| **Starting Quest** | `StartingQuestIds` | Quest-Ids, durch Kommas getrennt: `quest0, my_first_quest`. Siehe [Start-Quests](#starting-quests). |
| **Designation** | `AirplaneDesignation` | Das Staffelkürzel in den Kennungen deiner Flugzeuge, zum Beispiel `DB`. |
| **Koordinaten** (Coordinates) | `Coordinates` | Breiten- und Längengrad des Flugplatzes. |
| **Starting Date (dd.mm.yyyy)** | `StartDatetime` | Tag zuerst, nur Ziffern und Punkte: `15.08.1940`. Die Uhrzeit bleibt erhalten. |
| **Anzahl der Mannschaftsmitglieder:** (Amount of Crew Members:) | `InitialCrewCount` | Mannschaft, mit der du startest. |
| Ressourcenliste | `InitialResources` | Vorräte, die zu Beginn im Lager sind. |

In den durch Kommas getrennten Feldern werden Leerzeichen um die Kommas ignoriert und leere Einträge weggelassen.

## Was in einer `.goamap` steckt { #what-is-inside-a-goamap }

Eine `.goamap`-Datei ist ein ganz normales Zip-Archiv mit anderer Endung. Benenne eine Kopie in `.zip` um (oder öffne sie mit einem Archivprogramm wie 7-Zip) und du siehst:

| Datei | Was sie enthält |
|---|---|
| `Metadata.json` | Name, Beschreibung, Tags, Start-Quests, Daten, Startvorräte. Die einzige Datei, die du von Hand bearbeiten solltest. |
| `Icon.png` | Das Bild, das für die Karte angezeigt wird. |
| `Heightmap.bytes` | Die Form des Geländes. |
| `TerrainBiomeTexture.png` | Welcher Bodentyp wo gemalt ist. |
| `TerrainGrassTexture.png` | Wo Gras wächst. |
| `TerrainObjects.json` | Bäume, Felsen, Büsche und andere Landschaftsobjekte. |
| `Props.json`, `Buildings.json`, `Roof.json`, `Workbenches.json`, `TrainingObjects.json`, `FunctionAreas.json` | Alles, was auf der Karte schon gebaut ist. |
| `Airplanes.json`, `Characters.json` | Flugzeuge und Personen, die auf der Karte stehen. |

Alles außer `Metadata.json` überlässt du dem Karten Editor.

### `Metadata.json` von Hand bearbeiten { #editing-metadatajson-by-hand }

Tags und Start-Quests kannst du ändern, ohne den Editor zu öffnen:

1. Öffne die `.goamap` mit einem Archivprogramm.
2. Entpacke `Metadata.json`, bearbeite sie in einem Texteditor und lege sie unter demselben Namen wieder ins Archiv.
3. Behalte den Dateinamen des Archivs und die Endung `.goamap` bei.

Hier sind die Schlüssel, die du typischerweise anfasst, mit einem eigenen Tag und einer eigenen Questreihe. Die echte Datei enthält noch mehr Schlüssel; die lässt du, wie sie sind:

```json
{
  "Name": "Little Snoring",
  "Description": "A grass strip in Norfolk, two fields and a pub.",
  "AirplaneDesignation": "LS",
  "_tags": [
    "my_campaign"
  ],
  "StartingQuestIds": [
    "my_campaign_arrival"
  ]
}
```

!!! warning
    Die Datei muss gültiges JSON bleiben: keine Kommentare, keine Kommas am Ende. Eine Karte, deren `Metadata.json` nicht gelesen werden kann, fehlt in der Kartenliste.

## Tags und Missionen { #tags-and-missions }

Tags sind frei wählbare Etiketten, die Karten und Missionen verbinden. Eine Karte listet in `_tags` die Tags, die sie unterstützt, eine Mission listet in ihrem eigenen `_tags` die Tags, für die sie geschrieben ist, und die Mission kann nur auf der Karte auftauchen, wenn beide Listen mindestens einen Tag gemeinsam haben.

- Groß- und Kleinschreibung spielt bei Tags keine Rolle: `My_Campaign` und `my_campaign` passen zusammen.
- Eine fehlende oder leere Liste zählt als der einzelne Tag `default`, bei der Karte genauso wie bei der Mission.
- Jede mitgelieferte Karte listet `default` und ihren eigenen Namen: `debden`, `duxford`, `lichfield`, `perranporth`. Eine Mission ohne Tags taucht also auf allen auf, und eine Mission, die nur `duxford` trägt, nur auf Duxford.

Was das für deine Karte bedeutet:

| `_tags` deiner Karte | Missionen, die auftauchen können |
|---|---|
| fehlt oder `[]` | Jede Mission ohne Tags und jede Mission mit dem Tag `default`. |
| `["default", "my_campaign"]` | Alle oben genannten, plus Missionen mit dem Tag `my_campaign`. |
| `["my_campaign"]` | Nur Missionen mit dem Tag `my_campaign`. Die normalen Missionen bleiben weg. |

Tags wirken nur auf Missionen. Quests haben keine Tags; eine Karte wählt ihre Quests mit `StartingQuestIds`. Wie du eine Mission taggst, steht unter [Missionen](../missions/index.md).

## Start-Quests { #starting-quests }

`StartingQuestIds` listet die Quests, die die Karte beim Laden vergibt, egal was die Voraussetzungen dieser Quests selbst sagen. Fehlt die Liste oder ist sie leer, startet die Karte die Standard-Questreihe des Spiels, `quest0`, damit keine Karte je ohne Quests dasteht.

```json
"StartingQuestIds": ["my_campaign_arrival"]
```

Sobald du eine eigene Quest einträgst, wird `quest0` auf dieser Karte nicht mehr gestartet, und die mitgelieferte Hauptquestreihe bleibt weg. Willst du beides, trägst du beides ein:

```json
"StartingQuestIds": ["quest0", "my_campaign_arrival"]
```

Eine Id, zu der es keine Quest-Datei gibt, wird übersprungen; die Karte lädt trotzdem. Wie du die Quests selbst schreibst, erklärt [Quests](../quests/index.md).

## Karten-Ids { #map-ids }

Die Id einer Karte ist ihr Dateiname ohne `.goamap`. `my_airfield.goamap` hat die Id `my_airfield`, und Spielstände merken sich die Karte über diese Id.

- Gelesen werden nur Dateien, die direkt in `Maps/` liegen. Unterordner werden ignoriert.
- Zwei Karten mit derselben Id erscheinen nicht beide. Die zuletzt gelesene ersetzt die andere. Karten werden in dieser Reihenfolge gelesen: die mitgelieferten Karten, die eingeschalteten Mods in Ladereihenfolge, dann dein eigener Ordner `Maps` neben `Mods`, der sich gegen jede Mod durchsetzt. Eine Mod-Karte namens `Debden.goamap` ersetzt also das mitgelieferte Debden. Wähle einen eindeutigen Namen, außer genau das ist deine Absicht.
- Ersetzt eine Mod-Karte eine Karte, laden Spielstände auf dieser Karte die Version der Mod.

## Änderungen sehen { #seeing-your-changes }

| Du hast geändert... | So siehst du es |
|---|---|
| Eine Kartendatei in einer Mod, die das Spiel schon kennt | Schalte die Mod unter **Hauptmenü → Mods** aus und wieder ein. Karten werden sofort neu gelesen. |
| Einen neuen Mod-Ordner oder einen `Maps/`-Ordner, der beim Spielstart leer war | Drücke im Mods-Fenster auf **Refresh** oder starte das Spiel neu. |
| Eine Karte, die du im Karten Editor gespeichert hast | Nichts zu tun, die Kartenliste wird beim Speichern neu gelesen. |
| Eine `.goamap` in deinem eigenen Ordner `Maps`, die du von Hand bearbeitet hast | Starte das Spiel neu. |

Im Zweifel startest du das Spiel neu. Mehr zum Testablauf unter [Testen und neu laden](../basics/testing.md).

## Referenz { #reference }

### `Metadata.json`-Referenz { #metadatajson-reference }

Schlüssel, die du bearbeiten darfst, von Hand oder über die **Karteneinstellungen**:

| Schlüssel | Typ | Standard, wenn er fehlt | Was er bewirkt |
|---|---|---|---|
| `Name` | Text | keiner | Name in der Kartenliste. Normaler Text oder ein Lokalisierungsschlüssel. |
| `Description` | Text | keiner | Beschreibung, die bei ausgewählter Karte erscheint. Normaler Text oder ein Lokalisierungsschlüssel. |
| `_tags` | Liste von Texten | `["default"]` | Tags, die diese Karte unterstützt. Werden mit den `_tags` der Missionen verglichen. |
| `StartingQuestIds` | Liste von Texten | `["quest0"]` | Quests, die beim Laden der Karte vergeben werden. Eine leere Liste bedeutet ebenfalls `["quest0"]`. |
| `AirplaneDesignation` | Text | keiner | Staffelkürzel für die Kennungen deiner Flugzeuge. |
| `Coordinates` | Objekt `{ "x": latitude, "y": longitude }` | keiner | Wo auf der Welt der Flugplatz liegt. |
| `InitialCrewCount` | ganze Zahl | `0` | Mannschaft zu Beginn. |
| `StartDatetime` | Datum und Uhrzeit, `"1940-08-15T07:00:00"` | 15. August 1940, 07:00 | Wann das Spiel beginnt. |
| `BaseOpeningDatetime` | Datum und Uhrzeit | 1. August 1940, 00:00 | Eröffnungsdatum des Stützpunkts, wird vor Spielbeginn angezeigt. |
| `InitialResources` | Objekt, Ressourcenname zu Menge | keiner | Vorräte zu Beginn, zum Beispiel `{ "Planks": 50, "Fuel": 15 }`. |

Der Editor schreibt außerdem Schlüssel wie `CreatedDatetime`, `ModifiedDatetime`, `AirCrewCount`, `AirplanesCount`, `AirstripsCount`, `DeliveryTruckWaypoints`, `ShipmentSpawningLocation` und `DogSpawnPositions`. Lass sie so, wie der Editor sie geschrieben hat.

### Eine Karte teilen { #sharing-a-map }

Eigene Karten kannst du direkt aus der Kartenliste im Karten Editor in den Steam Workshop hochladen, ganze Mods aus dem Mods-Fenster. Siehe [Steam Workshop](../sharing/workshop.md).
