# Beispiele

Vollständige, funktionierende Mods zum Lesen, Kopieren und Verändern. Jeder Ordner in [`examples/`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples) hat eine eigene README, die erklärt, worauf du achten solltest.

Der schnellste Weg zu deiner eigenen Mission: Kopier `coastal_patrol`, benenne die Dateien und die Id um und ändere die Zahlen und den Text.

## Die Beispiele, grob nach Anspruch sortiert { #the-examples-roughly-in-order-of-ambition }

| Ordner | Was es ist |
|---|---|
| [`coastal_patrol`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/coastal_patrol) | Eine Mission: eine JSON-Datei und ein kleines Skript. Fang hier an. Es ist das fertige Ergebnis von [Deine erste Mission](missions/first-mission.md). |
| [`raf_collection`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/raf_collection) | Fünf eigenständige Missionen, jede zeigt eine andere Mechanik. Drei tragen ihren Text im JSON und brauchen kein Skript. `night_interception` ist das lange ausgearbeitete Beispiel, in dem das Handler-Modell Zeile für Zeile erklärt wird. |
| [`event_script`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/event_script) | Python, das auf die Basis und auf Missionen reagiert, die du nicht geschrieben hast. Keine eigene Mission. Siehe [Events](scripting/events.md). |
| [`chain_convoy`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/chain_convoy) | Eine Gabelung: Eine Mission führt zu einer von zwei anderen, je nachdem, wie sie ausgegangen ist. |
| [`chain_airfield`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/chain_airfield) | Eine Kette mit vier Stufen, komplett in JSON. |
| [`campaign_kanalkampf`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/campaign_kanalkampf) | Eine Kampagne mit Gedächtnis: Bedingungen, die JSON nicht ausdrücken kann, weil dabei gezählt wird. |
| [`script_only_scramble`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/script_only_scramble) | Eine Mission **ganz ohne JSON**, die sich selbst aus Python heraus sperrt und skaliert. |
| [`quests`](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/quests) | Drei Quest-Dateien: eine einfache Einstiegsquest, eine Folgequest und eine Quest, die zu einer bestimmten Karte gehört. Siehe [Quests](quests/index.md). |

## Kette oder Kampagne? { #chain-or-campaign }

Die zwei Missionssets unten in der Liste lohnen einen Vergleich.

| | Kette (`chain_convoy`, `chain_airfield`) | Kampagne (`campaign_kanalkampf`) |
|---|---|---|
| Fragt | "War Mission X erfolgreich?" | "Wie oft?", "Wer war an Bord?", "Was hat der Spieler gewählt?" |
| Gebaut mit | JSON-Voraussetzungen (`CompletedMission`) | einem Skript, das entscheidet, plus einer Zustandsdatei |
| Gedächtnis | keins: spielt sich jedes Mal gleich | merkt sich Dinge über Flüge, Tage und Sitzungen hinweg |
| Übersteht Speichern und Laden | ja, von selbst | ja, weil das Skript seinen Zustand in eine Datei schreibt |
| Braucht Python | nein (die Skripte in den Ketten-Beispielen tragen nur Text) | ja |

Eine **Kette** stellt eine Ja-oder-Nein-Frage über die Mission davor, und das kann JSON allein. Eine **Kampagne** fragt nach dem ganzen Spieldurchlauf, und dafür braucht es ein Skript und einen Ort, an dem der Zustand gespeichert wird. [Ketten und Kampagnen](missions/chains.md) erklärt beides.

## Ein Beispiel verwenden { #using-an-example }

1. Kopier die Dateien des Beispielordners in den `Missions/`-Ordner einer Mod: `Mods/my_mod/Missions/`. (Das `quests`-Beispiel ist als ganze Mod aufgebaut; kopier den Ordner selbst nach `Mods/`.)
2. Benenne die Ids um. Die Beispiele verwenden kurze Ids wie `coastal_patrol`, weil sie Dokumentation sind. Eine echte Mod setzt ihren Namen vor jede Id (`mymod_coastal_patrol`) und ändert sie überall, wo sie vorkommt: in den Dateinamen, bei `MISSION_ID` im Skript, in `CompletedMission`-Werten und in `CreateMission`-Aufrufen.
3. Lass den Validator über deinen Mod-Ordner laufen (siehe [Ohne KI-Agent](start/without-ai.md)).
4. Lade einen Spielstand und prüfe das Ergebnis, siehe [Testen und neu laden](basics/testing.md).

Eine Beispiel-Id, die mit einer eingebauten Mission übereinstimmt, würde diese ersetzen. Keines der Beispiele tut das, aber deine umbenannte Kopie sollte es auch nicht.

## Wie weit jedes Beispiel getestet ist { #how-far-each-example-has-been-tested }

Jedes Beispiel wurde vom Spiel geladen. Wie weit es jeweils getestet wurde, ist unterschiedlich:

| Beispiel | Getestet |
|---|---|
| `coastal_patrol` | im Spiel geladen und erstellt; noch nicht bis zum Ende geflogen |
| `raf_collection` | alle fünf im Spiel erstellt; `night_interception` bis zum Ende geflogen |
| `event_script` | bestätigt, dass die Handler aus dem `Missions/`-Ordner einer Mod feuern |
| `chain_convoy` | im Spiel geladen und erstellt; die Verzweigung noch nicht geflogen |
| `chain_airfield` | das Freischalten im Spiel bestätigt; die Flüge noch nicht der Reihe nach durchgespielt |
| `campaign_kanalkampf` | im Spiel geflogen; die Schwierigkeitsanpassung über mehrere Angriffe gemessen |
| `script_only_scramble` | noch nicht im Spiel getestet |

"Geladen" heißt, das Spiel hat die Dateien gelesen und `create_mission` hat die Mission mit den geschriebenen Werten erzeugt; "geflogen" heißt, eine Staffel ist gestartet und der Ausgang wurde beobachtet.
