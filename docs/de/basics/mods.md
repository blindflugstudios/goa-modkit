# So funktionieren Mods

Eine Mod ist ein Ordner. Das Spiel sucht darin nach ein paar fest benannten Unterordnern, und was in diesen Unterordnern liegt, ist das, was die Mod verändert. Es gibt keinen Verpackungsschritt, kein Manifest, das du schreiben musst, und nichts zu kompilieren: Du bearbeitest Dateien, lädst ein Level und siehst das Ergebnis.

Diese Seite behandelt, was alle Mods gemeinsam haben: wo sie liegen, wie das Spiel sie findet, wie man sie ein- und ausschaltet und welche Mod gewinnt, wenn zwei dasselbe ändern. Was *in* die Unterordner gehört, steht auf den Themenseiten: [CSV-Tabellen](../data/csv.md), [Missionen](../missions/index.md), [Quests](../quests/index.md), [Scripting](../scripting/index.md) und die Seiten zu [Karten und Grafik](../content/maps.md). Wie eine fertige Mod zu anderen Spielern kommt, steht unter [Steam Workshop](../sharing/workshop.md).

## Eine Mod in einer Minute { #a-mod-in-one-minute }

1. Finde deinen `Mods`-Ordner: **Hauptmenü (Main menu) → Mods → Open folder**. Unter Windows ist das `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\`; die anderen Plattformen findest du [weiter unten](#where-mods-live).
2. Leg darin einen Ordner an, zum Beispiel `my_mod`, und darin einen der Inhaltsordner: `CSV/`, `Missions/`, `Quests/`, `Maps/`, `Objects/`, `TerrainObjects/` oder `Biomes/`. Leg mindestens eine Datei hinein.
3. Optional: Füge eine `config.json` mit Name und Id der Mod hinzu und eine `preview.png` (höchstens 1 MB) als Vorschaubild.
4. Drück im Mods-Fenster auf **Refresh**, damit das Spiel den neuen Ordner bemerkt, und lade dann ein Level.
5. Ab dann wird jede Änderung an einer Datei in der Mod beim nächsten Laden eines Levels übernommen.

Der Ordner darf beliebig heißen - `MyMod` funktioniert genauso wie `my_mod`. Nur die optionale `Id` in der `config.json` muss kleingeschrieben sein (`my_mod`, nicht `MyMod`). Stell jeder Id, die du dir ausdenkst, den Namen deiner Mod voran, damit du nie versehentlich etwas ersetzt.

!!! tip
    Wenn das deine erste Mod ist, führt der kürzeste Weg vom leeren Ordner zu einer sichtbaren Änderung über eine einzeilige Änderung an einer [CSV-Tabelle](../data/csv.md). Die [Anleitung zur ersten Mod](../start/first-mod.md) führt dich Schritt für Schritt hindurch.

## Wo Mods liegen { #where-mods-live }

Das Spiel liest Mods aus zwei Orten: aus den Items, die du im Steam Workshop abonniert hast, und aus deinem eigenen `Mods`-Ordner. Alles, was du selbst baust, gehört in den zweiten.

| Plattform | Mods-Ordner |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Mods/` |

Der Ordner wird beim ersten Spielstart angelegt. Am schnellsten erreichst du ihn über den Button **Open folder** im Mods-Fenster (siehe unten). Das Spiel legt in diesem Ordner außerdem eine kleine `mod_state.json` ab. Diese Datei ist die eigene Notiz des Spiels darüber, welche Mods du ein- oder ausgeschaltet hast; sie gehört zu keiner Mod, und du solltest sie nicht mitliefern.

### Eine Mod ist ein Ordner { #one-mod-is-one-folder }

Der Ordner darf heißen, wie du willst - `MyMod`, `my_mod` oder `My Campaign` funktionieren alle. Die Kleinschreibungsregel weiter unten gilt nur für die optionale `Id` in der `config.json`, nicht für den Ordner.

In deinem Mod-Ordner hat jede Art von Inhalt einen festen Unterordner. Es müssen nur die existieren, die du brauchst:

```text
Mods/
  my_mod/
    config.json        optional - name, id, load order
    preview.png        optional - the picture shown in the Mods window and on the Workshop
    CSV/               data tables
    Missions/          mission .json files and Python .py scripts
    Quests/            quest .json files
    Maps/              .goamap map files
    Objects/           replacement models for buildings and objects
    TerrainObjects/    replacement models for trees, rocks and other map objects
    Biomes/            biome definitions
```

| Ordner | Was hineingehört | Mehr dazu |
|---|---|---|
| `CSV/` | Änderungen an den Datentabellen des Spiels | [CSV-Tabellen](../data/csv.md) |
| `Missions/` | Missionen (`.json`) und Python-Skripte (`.py`) | [Missionen](../missions/index.md), [Scripting](../scripting/index.md) |
| `Quests/` | Quests (`.json`) | [Quests](../quests/index.md) |
| `Maps/` | Karten (`.goamap`) | [Karten](../content/maps.md) |
| `Objects/` | Ersatzmodelle für Gebäude und Objekte | [Objekte und Modelle](../content/objects.md) |
| `TerrainObjects/` | Ersatzmodelle für Bäume, Felsen und andere Kartenobjekte | [Geländeobjekte](../content/terrain-objects.md) |
| `Biomes/` | Biom-Definitionen | [Biome](../content/biomes.md) |

Drei Regeln entscheiden, ob das Spiel den Ordner überhaupt bemerkt:

- Ein Unterordner zählt nur, wenn etwas darin liegt. Ein leerer `CSV/`-Ordner ist dasselbe wie gar kein `CSV/`-Ordner.
- Ein Mod-Ordner ohne einen der obigen Unterordner (oder nur mit leeren) wird ohne Meldung ignoriert.
- Symbolische Links und Junctions (Verknüpfungen, die auf einen anderen Ordner zeigen) werden nie verfolgt, weder als Mod-Ordner noch als einer seiner Unterordner. Das Spiel überspringt sie mit einer Warnung im Log.

Bei `CSV`, `Missions`, `Quests` und `Maps` werden nur Dateien gelesen, die direkt im Unterordner liegen; alles, was tiefer liegt, wird ignoriert. `Objects`, `TerrainObjects` und `Biomes` funktionieren andersherum: Jedes Objekt bekommt einen eigenen Unterordner, benannt nach dem, was es ersetzt. Die jeweiligen Seiten erklären den Aufbau.

### `config.json`

Optional. Ohne sie wird der Ordnername als Name der Mod angezeigt, die Id wird aus dem Ordnernamen gebildet, und die Ladereihenfolge ist 100.

```json
{
  "Id": "my_mod",
  "Name": "My Mod",
  "Author": "Your Name",
  "Version": "1.0.0",
  "LoadOrder": 100
}
```

| Feld | Bedeutung |
|---|---|
| `Id` | Damit unterscheidet das Spiel Mods und löst Gleichstände in der Ladereihenfolge auf. 3–64 Zeichen aus Kleinbuchstaben, Ziffern, `_`, `.` oder `-`, beginnend mit einem Buchstaben oder einer Ziffer. |
| `Name` | Das, was Spieler im Mods-Fenster sehen. Beliebiger Text. Beim ersten Upload wird er auch zum Workshop-Titel. |
| `LoadOrder` | Eine ganze Zahl, die festlegt, in welcher Reihenfolge Mods angewendet werden (siehe [Welche Mod gewinnt](#which-mod-wins)). Kleinere Zahlen werden zuerst angewendet. Standard `100`. |
| `Author`, `Version` | Für dich und alle, die die Datei lesen. Das Spiel liest sie nicht. |

Was passiert, wenn etwas nicht stimmt:

- Eine `Id`, die gegen die Regel verstößt, wird ohne Meldung ignoriert, und stattdessen wird der Ordnername verwendet - kleingeschrieben, wobei jedes Zeichen außer Buchstaben, Ziffern, `_`, `.` und `-` durch `_` ersetzt wird. Log-Zeilen zu deiner Mod sind mit dieser Id gekennzeichnet, eine abgelehnte Id fällt also als unerwartete Kennzeichnung auf. Die Detailansicht der Mod im Mods-Fenster zeigt außerdem die Id, die das Spiel tatsächlich verwendet.
- Eine `config.json`, die das Spiel nicht lesen kann (ein fehlendes Komma, eine überzählige Klammer), wird im Log gemeldet und so behandelt, als gäbe es sie nicht.

### `preview.png`

Optional. Ein PNG im Hauptverzeichnis des Mod-Ordners, höchstens 1 MB groß. Das Mods-Fenster zeigt es neben dem Namen der Mod an, und es wird zum Bild des Items, wenn du die Mod in den Workshop hochlädst. Ohne Vorschaubild zeigt das Mods-Fenster ein Platzhalterbild.

## Das Mods-Fenster { #the-mods-window }

**Hauptmenü → Mods** listet jede Mod auf, die das Spiel gefunden hat - Workshop-Abos und deine eigenen Ordner - mit Vorschaubild, einer Markierung, ob sie aus dem Workshop oder aus deinem `Mods`-Ordner stammt, und einem Abzeichen pro Art von Inhalt, den sie mitbringt.

| Element | Was es tut |
|---|---|
| Schalter **Enabled** (pro Mod) | Schaltet die Mod ein oder aus. Eine ausgeschaltete Mod trägt nichts bei: Ihre Tabellen, Quests, Missionen, Skripte und Karten werden alle übersprungen. Karten wirken sofort, alles andere beim nächsten Laden eines Levels. Neue Mods sind standardmäßig eingeschaltet. |
| Button **Upload** (pro Mod, nur deine eigenen Mods) | Veröffentlicht die Mod im Steam Workshop. Siehe [Steam Workshop](../sharing/workshop.md). |
| **Refresh** | Durchsucht die Workshop-Items und deinen `Mods`-Ordner erneut. Drück ihn, nachdem du einen neuen Mod-Ordner angelegt, einen umbenannt, eine `config.json` geändert oder während des Spiels etwas im Workshop abonniert hast. |
| **Open folder** | Öffnet deinen `Mods`-Ordner im Dateibrowser und legt ihn an, falls es ihn noch nicht gibt. |
| **Workshop** | Öffnet die Steam-Workshop-Seite des Spiels im Steam-Overlay (nur Steam-Version). |

Jede Mod hat außerdem eine Detailansicht mit ihrem Namen, der Id, die das Spiel verwendet, ihrer Ladereihenfolge und dem Ordner, aus dem sie gelesen wurde, samt einem Button, der diesen Ordner öffnet.

Mods mit Python-Dateien zeigen zusätzlich einen Schalter **Scripting**. Wenn du ihn einschaltest, musst du das bestätigen. Derzeit setzt das Spiel diesen Schalter nicht durch, er ist also kein Schutz: Die Skripte einer Mod laufen immer, wenn die Mod eingeschaltet ist, egal was der Schalter sagt. Die einzige Möglichkeit, die Skripte einer Mod zu stoppen, ist, die ganze Mod auszuschalten. Lies [Python-Mods und Sicherheit](security.md), bevor du eine Mod mit Skripten von jemandem einschaltest, den du nicht kennst.

## Welche Mod gewinnt { #which-mod-wins }

Zuerst werden die Workshop-Items angewendet, dann die Mods in deinem `Mods`-Ordner, und innerhalb jeder Gruppe in `LoadOrder`-Reihenfolge - kleinere Zahlen zuerst, bei Gleichstand entscheidet die Id. Wenn zwei Mods dasselbe liefern - eine Zeile in derselben Tabelle, eine Quest mit demselben Dateinamen, eine Mission mit derselben Id - gewinnt die, die **zuletzt** angewendet wird. Zwei Folgen daraus:

- Deine eigene Kopie einer Mod schlägt immer die Workshop-Kopie derselben Mod. Du kannst also an einer bereits veröffentlichten Mod weiterarbeiten und deine Änderungen testen, während die veröffentlichte Version weiter abonniert ist.
- Zwei Mods vom selben Ort (beide aus dem Workshop oder beide in deinem `Mods`-Ordner) mit derselben Id werden nicht beide geladen. Die zweite gefundene wird mit einer Warnung im Log übersprungen.

Die praktische Regel daraus: **Stell jeder Id, die du dir ausdenkst, den Namen deiner Mod voran**, damit du nie versehentlich etwas ersetzt.

Deine eigenen Ordner `Missions` und `Maps` neben `Mods` - dort speichern der Missionseditor im Spiel und der Karteneditor - folgen anderen Regeln:

- **Missionen:** Dein eigener `Missions`-Ordner wird nach allen Mods gelesen und gewinnt gegen alle. Denk an diesen Ordner, wenn eine deiner Missionen die Kopie in deiner Mod zu ignorieren scheint.
- **Karten:** Hier ist die Reihenfolge umgekehrt. Karten werden so gelesen: zuerst die mitgelieferten Karten, dann dein eigener `Maps`-Ordner, dann die eingeschalteten Mods in Ladereihenfolge. Eine Mod-Karte mit demselben Dateinamen ersetzt also sowohl deine eigene als auch die mitgelieferte Karte. Siehe [Karten](../content/maps.md).

## Deine Änderungen sehen { #seeing-your-changes }

Alles, was eine Mod enthält, wird beim Laden eines Levels gelesen. Geh zurück ins Hauptmenü und lade einen Spielstand oder starte eine Karte, dann übernimmt das Spiel alles, was du inzwischen geändert hast - Tabellen, Quests, Missionen, Skripte und Karten gleichermaßen. Die *Liste* der Mods wird beim Spielstart durchsucht, jedes Mal, wenn du das Mods-Fenster öffnest, und wenn du dort auf **Refresh** drückst.

Der Alltagsablauf, während du an einer Mod arbeitest:

1. Speichere dein Spiel.
2. **Einstellungen (Options) → Quit to main menu.**
3. Öffne **Mods**, wenn du einen Mod-Ordner hinzugefügt oder umbenannt hast (beim Öffnen des Fensters wird neu gesucht).
4. Lade den Spielstand.

| Du hast geändert ... | So siehst du es |
|---|---|
| Eine Datei in einer Mod, die das Spiel schon kennt | Ein Level laden (einen Spielstand laden reicht) |
| Eine Karte in einer Mod | Auch sofort, wenn du den Schalter **Enabled** der Mod umschaltest |
| Einen neuen Mod-Ordner, einen umbenannten Ordner, eine geänderte `config.json`, einen Unterordner, der beim Spielstart leer war | Das Mods-Fenster öffnen (oder dort **Refresh** drücken) und dann ein Level laden - oder das Spiel neu starten |
| Ein neues Workshop-Abo, während das Spiel läuft | **Refresh** im Mods-Fenster, sobald Steam den Download abgeschlossen hat |

[Testen und neu laden](testing.md) erklärt mehr zu diesem Ablauf und zu den Werkzeugen, die beim Testen helfen.

Das Spiel schreibt in seine Log-Datei `Player.log`, was es angenommen und was es abgelehnt hat:

| Plattform | Log-Datei |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| macOS | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

Das Log des vorherigen Durchlaufs bleibt daneben als `Player-prev.log` erhalten. Das veröffentlichte Spiel schreibt hauptsächlich Fehler ins Log, daher tauchen manche der ausführlichen `[Mod ...]`-Zeilen, die auf den Themenseiten beschrieben sind, dort eventuell nicht auf; prüf im Zweifel die Wirkung direkt im Spiel. Mehr dazu in [Testen und neu laden](testing.md) und [Wenn nichts passiert](../start/troubleshooting.md).
