# Referenz

Alles, was eine Mission enthalten kann, an einem Ort: wie das Spiel deine Dateien findet, in welcher Reihenfolge es dein Skript aufruft, jeder Handler, jedes JSON-Feld und jede Zahl, die das JSON erwartet.

Neu bei Missionen? Fang mit [Deine erste Mission](first-mission.md) an und komm hierher zurück, wenn du ein Detail brauchst.

## Zwei Wege, eine Mission zu bauen { #two-ways-to-build-a-mission }

Eine Mission wird an ihrer **Id** erkannt, und die ist einfach ihr Dateiname ohne Endung. `coastal_patrol.json` ist die Mission `coastal_patrol`.

| | Mit JSON-Datei (der normale Weg) | Nur Skript (kein JSON) |
|---|---|---|
| Dateien | `<id>.json`, optional `<id>.py` | `<id>.py` |
| Grundwerte (Zeitfenster, Flugzeit, Gegner) | aus dem JSON | aus den Getter-Handlern, jeder optional |
| Fertigkeits-Stats | `_missionStats` | `missions_api.SetMissionStat` in `initialize_mission` |
| Ort auf der Karte | `_potentialLocations` | `missions_api.SetMissionLocation` |
| Wie-geplant-Chance | `_asPlannedChance` | `missions_api.SetAsPlannedChance` |
| Ausgänge | vier `_missionOutcomes` | `missions_api.SetOutcome` und `AddOutcomeEffect`, dazu `get_mission_result` (Pflicht) |
| Ereignisse im Flug pro Flug | immer 3 | `get_mission_events_count` (Standard 3) |
| Erscheint von selbst (wöchentliche Ziehung, historisches Erscheinen) | ja | nein, siehe [Reine Skript-Missionen](#script-only-missions) |

Nimm den JSON-Weg, außer du hast einen Grund dagegen. Er übersteht Speichern und Laden, der Validator kann ihn prüfen, und die Mission erscheint im Spiel, ohne dass ein anderes Skript sie vergeben muss.

### Welches Skript läuft { #which-script-runs }

Jede Mission läuft auf einem Skript, aber du musst selten eins schreiben:

- Gibt es eine `.py`-Datei, die genau wie die Mission heißt, verwendet das Spiel ihre Handler.
- Für jeden Handler, den diese Datei nicht definiert, und für jede Mission ohne eigene Datei verwendet das Spiel das gemeinsame **Standard-Missionsskript**, das mit dem Spiel ausgeliefert wird. Es liest die Id der Mission und gibt die Standard-Funksprüche aus den neun Text-Slots aus (siehe [Lokalisierung](../scripting/localization.md#mission-texts)).

Eine JSON-Datei plus ihr Text ist also eine vollständige Mission. Schreib `<id>.py` nur, um zu ändern, was im Flug passiert oder welcher Text erscheint. Verglichen wird der exakte Dateiname: Ein Skript namens `recon.py` hängt sich nie an eine Mission namens `dangerous_recon`.

### Wo das Spiel sucht { #where-the-game-looks }

Missionsdateien werden an mehreren Orten gelesen, in dieser Reihenfolge. Wenn zwei Orte dieselbe Id enthalten, **gewinnt der letzte** und ersetzt die frühere Mission vollständig:

1. die eigenen Missionen des Spiels
2. DLC-Missionen
3. der `Missions/`-Ordner jeder aktivierten Mod (zuerst Workshop-Mods, dann Mods, die du von Hand installiert hast)
4. der `Missions/`-Ordner im Spieldatenordner (siehe [So funktionieren Mods](../basics/mods.md))

Deshalb ersetzt eine Id, die mit einer eingebauten Mission übereinstimmt, diese Mission, und deshalb schlägt eine lokale Kopie einer Mod die Workshop-Version, die du abonniert hast. Setz deinen Mod-Namen vor deine Ids (`mymod_coastal_patrol`), außer du willst wirklich etwas ersetzen.

Der `Missions/`-Ordner einer Mod ist auch ihr einziger Skriptordner. Event-Skripte, Hilfsmodule und Quest-Textskripte gehören alle dorthin. Siehe [Scripting](../scripting/index.md).

### Reine Skript-Missionen { #script-only-missions }

Eine Mission mit `.py` und ohne `.json` taucht nie von selbst auf. Die wöchentliche Ziehung und das historische Erscheinen berücksichtigen nur Missionen, deren Daten das Spiel schon kennt, und eine reine Skript-Mission hat keine Daten, bis sie einmal erstellt wurde.

Sie lässt sich auf zwei Wegen erstellen:

- `missions_api.CreateMission("<id>")` aus einem anderen Skript. So vergibt eine Kampagne eine Folgemission.
- der Cheat `create_mission <id>`, zum Testen.

Drei Folgen, mit denen du planen solltest:

- **Nach der ersten Erstellung kann die Ziehung sie wählen.** Die Daten, die dein Skript geschrieben hat, existieren jetzt, also behandelt die wöchentliche Ziehung die Mission wie jede andere. Hat dein Skript keine Sperren hinzugefügt, kann die Mission auf jeder Karte und an jedem Datum erscheinen. Ruf in `initialize_mission` immer `AddMissionRequirement` auf (und `SetTags`, wenn sie zu einer Kampagne gehört).
- **Ab der zweiten Erstellung werden die Getter nicht mehr gefragt.** Das Spiel baut die Mission jetzt aus den beim ersten Mal geschriebenen Daten, wie eine JSON-Mission: Name, Beschreibung und Bedrohungszeile kommen aus den Text-Slots `missions/<id>/mission_name`, `missions/<id>/mission_description` und `missions/<id>/intel_threat_report`, und der Flug hat 3 Ereignisse. Registriere diese drei Terms auch in einer reinen Skript-Mission.
- **Die geschriebenen Daten werden nicht gespeichert.** Sie liegen nur für die aktuelle Sitzung im Speicher. Lädt der Spieler einen Spielstand mit so einer Mission in der Luft, sind die geschriebenen Ausgänge weg, und das Spiel fragt stattdessen [`get_mission_result`](#get_mission_result). Fehlt dieser Handler, scheitert die Mission beim Ende mit einem Fehler. Jede reine Skript-Mission sollte ihn definieren.

Siehe das Beispiel `script_only_scramble` auf der Seite [Beispiele](../examples.md).

## Lebenszyklus { #lifecycle }

Was mit einer Mission passiert, von der Woche, in der sie geplant wird, bis zum Ergebnisfenster:

| # | Schritt | Was passiert |
|---|---|---|
| 1 | Wochenplan | Zu Beginn jeder Woche verteilt das Spiel eine Anzahl Missions-Slots über die Woche. Die Anzahl hängt vom Rang der Basis ab. |
| 2 | Historische Missionen mit Datum | Bei jedem Tageswechsel wird jede historische Mission mit `_historicDay`, deren Sperren erfüllt sind, erstellt, außerhalb der Wochen-Slots. |
| 3 | Ein Slot ist fällig | Jede historische Mission ohne Datum, deren Sperren erfüllt sind, erscheint zusammen mit dieser Wochenmission und belegt den Slot nicht. Den Slot selbst füllt die Zufallsziehung. |
| 4 | Zufallsziehung | Alle nicht-historischen Missionen, deren Sperren erfüllt sind, bilden einen Pool. Eine wird gezogen und aus dem Pool entfernt. Ist der Pool leer, wird er wieder aufgefüllt. |
| 5 | Sperren | Eine Mission kommt infrage, wenn alle `_missionRequirements` erfüllt sind, die aktuelle Karte einen ihrer `_tags` teilt und sie (bei historischen Missionen) noch nicht gewonnen wurde und nicht schon auf der Karte ist. |
| 6 | Erstellung | Das Spiel wählt einen Ort (eine Ziehung plus bis zu fünf weitere, um zwei Missionen am selben Fleck zu vermeiden), berechnet daraus Entfernung und Treibstoff und richtet die Mission aus JSON oder Skript ein. Dann ruft es [`initialize_mission`](#initialize_mission) auf. |
| 7 | Warten | Die Mission liegt auf der Kriegskarte, bis der Spieler Flugzeuge schickt oder ihr Startfenster abläuft. Historische Missionen laufen nie ab. |
| 8 | Flug | Die Uhr startet, sobald **alle** zugewiesenen Flugzeuge in der Luft sind. [`send_mission_event`](#send_mission_event) feuert jedes Mal, wenn der Flug einen weiteren Schritt erreicht (standardmäßig nach einem Drittel, nach zwei Dritteln und am Ende). |
| 9 | Ausgang | Mit Daten: Die Würfe wählen einen der vier Ausgänge, seine Effekte werden angewendet, dann läuft [`set_mission_impact`](#set_mission_impact). Ohne Daten: [`get_mission_result`](#get_mission_result) entscheidet, dann läuft `set_mission_impact`. |
| 10 | Rückkehr | Die Flugzeuge landen, die Akten der Crew werden aktualisiert, Events feuern. Dann [`send_mission_result_event`](#send_mission_result_event) oder [`send_mission_cancelled_event`](#send_mission_cancelled_event), falls der Spieler die Mission abgebrochen hat oder sie verfallen ist. |
| 11 | Ergebnisfenster | Wenn der Spieler es öffnet, liefert [`get_mission_result_text`](#get_mission_result_text) den Text. |

### Die zwei Würfe und der Ausgang-Index { #the-two-rolls-and-the-outcome-index }

Zwei Würfelwürfe entscheiden jede Mission:

1. **Wie geplant?** Ein Wurf gegen `_asPlannedChance` (0–100). Hat sich die Lage so entwickelt wie bei der Einsatzbesprechung?
2. **Fertigkeit bestanden?** Das Spiel würfelt einen Zielwert im Bereich eines Missions-Stats und zählt dann die Fertigkeit der Staffel zusammen. Erreicht die Staffel den Zielwert, ist der Wurf bestanden. Der erste Stat gilt, wenn die Mission wie geplant lief, der zweite, wenn nicht.

Die beiden Antworten wählen den Ausgang:

| Index | Wie geplant | Fertigkeitswurf | Bedeutung |
|---|---|---|---|
| 0 | nein | gescheitert | Schiefgelaufen und gescheitert |
| 1 | nein | bestanden | Schiefgelaufen, aber gerettet |
| 2 | ja | gescheitert | Nach Plan gelaufen, trotzdem gescheitert |
| 3 | ja | bestanden | Voller Erfolg |

Für Programmierer: `index = (skillPassed ? 1 : 0) | (asPlanned ? 2 : 0)`.

!!! warning "Genau vier Ausgänge, in dieser Reihenfolge"
    Das Spiel prüft nicht, wie viele Ausgänge du geschrieben hast. Mit weniger als vier stürzt die Mission in dem Moment ab, in dem sie endet, lange nachdem du aufgehört hast, das JSON zu verdächtigen. Mit mehr als vier werden die zusätzlichen nie verwendet.

!!! warning "Mindestens zwei Missions-Stats"
    Der Fertigkeitswurf liest direkt den ersten und den zweiten Eintrag von `_missionStats`. Mit nur einem stürzt die Mission beim Fertigkeitswurf ab.

"Erfolg" in einer Kette oder einer Quest bedeutet nicht Index 3. Welcher Ausgang als Erfolg zählt, ist durch seine Position festgelegt: Index 0 und 2 sind Fehlschläge, Index 1 (schiefgelaufen, aber gerettet) und Index 3 sind Erfolge.

## Handler { #handlers }

Ein Handler ist eine Python-Funktion, die das Spiel zu einem festen Zeitpunkt aufruft. Du markierst sie mit dem Decorator `@event_handler(...)` und dem Namen des Zeitpunkts:

```python
from Blindflug.FlightMission import MissionEvent

@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    ...
```

Den Funktionsnamen wählst du selbst; was zählt, ist der Decorator. Jeder Handler bekommt genau ein Argument, `mission_entity_id`: die Nummer der Mission, um die es bei diesem Aufruf geht. Gib sie an jeden `missions_api`-Aufruf weiter. Dasselbe Skript kann gleichzeitig für zwei Flüge derselben Mission laufen, also speichere niemals Zustand eines einzelnen Flugs in einer Variablen auf Modulebene.

| Handler | `MissionEvent`-Konstante | Gibt zurück | Aufgerufen |
|---|---|---|---|
| `get_mission_id` | `GET_MISSION_ID` | str | in beiden Modi |
| `initialize_mission` | `INITIALIZE_MISSION` | nichts | in beiden Modi |
| `send_mission_event` | `SEND_MISSION_EVENT` | nichts | in beiden Modi |
| `set_mission_impact` | `SET_MISSION_IMPACT` | nichts | in beiden Modi |
| `send_mission_result_event` | `SEND_MISSION_RESULT_EVENT` | nichts | in beiden Modi, außer bei Abbruch |
| `send_mission_cancelled_event` | `SEND_MISSION_CANCELLED_EVENT` | nichts | in beiden Modi |
| `get_mission_result_text` | `GET_MISSION_RESULT_TEXT` | str | in beiden Modi |
| `get_mission_name` | `GET_MISSION_NAME` | str | nur Skript |
| `get_mission_description_text` | `GET_MISSION_DESCRIPTION_TEXT` | str | nur Skript |
| `get_time_to_start` | `GET_TIME_TO_START` | int | nur Skript |
| `get_completion_time` | `GET_COMPLETION_TIME` | int | nur Skript |
| `get_threat_level` | `GET_THREAT_LEVEL` | str | nur Skript |
| `get_enemy_count` | `GET_ENEMY_COUNT` | int | nur Skript |
| `get_mission_events_count` | `GET_MISSION_EVENTS_COUNT` | int | nur Skript |
| `get_fuel_level` | `GET_FUEL_LEVEL` | int | nur Skript |
| `get_mission_result` | `GET_MISSION_RESULT` | bool | nur Skript - **Pflicht** |
| `get_mission_icon` | `GET_MISSION_ICON` | - | **nie aufgerufen** |
| `calculate_mission_modifiers` | `CALCULATE_MISSION_MODIFIERS` | - | **nie aufgerufen** |
| `calculate_airplane_modifiers` | `CALCULATE_AIRPLANE_MODIFIERS` | - | **nie aufgerufen** |
| `calculate_pilot_modifiers` | `CALCULATE_PILOT_MODIFIERS` | - | **nie aufgerufen** |

Handler für "nur Skript" werden einmal gefragt, wenn eine Mission ohne JSON-Datei zum ersten Mal erstellt wird (siehe [Reine Skript-Missionen](#script-only-missions)). Eine Mission mit JSON-Datei ignoriert sie.

### get_mission_id

Gibt die Id der Mission als String zurück.

```python
MISSION_ID = "mymod_coastal_patrol"

@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID
```

Eine reine Skript-Mission muss ihn definieren: Daran erkennt das Spiel die Datei als eigenständige Mission. Gib genau den Dateinamen zurück. In einem Skript neben einer JSON-Datei liest das Spiel den Wert nicht, aber dein eigener Code baut meistens Textschlüssel daraus, halte ihn also auch dort identisch mit dem Dateinamen. Das gemeinsame Standardskript gibt `missions_api.GetMissionId(mission_entity_id)` zurück, was für jede Mission funktioniert.

### initialize_mission

Wird einmal aufgerufen, direkt nachdem die Mission erstellt wurde und bevor sie auf der Kriegskarte erscheint.

Hier schreibt eine reine Skript-Mission alles, was sonst in einer JSON-Datei stünde: Sperren, Stats, Ort, Slots, Schwierigkeit, Ausgänge. Eine Mission mit JSON-Datei kann ihn auch nutzen, etwa um die Schwierigkeit an die bisherige Kampagne anzupassen:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    if campaign_state.get("raids_survived") >= 2:
        missions_api.SetMissionStat(mission_entity_id, "Fight", 76, 115)
        missions_api.SetAsPlannedChance(mission_entity_id, 35)
```

`missions_api.CreateMission` von hier aus aufzurufen wird abgelehnt und protokolliert, weil dieser Handler mitten in der Erstellung einer Mission läuft.

!!! note
    Bei einer Mission mit JSON-Datei ändern `SetMissionStat`, `SetOutcome`, `AddOutcomeEffect`, `AddMissionRequirement` und `SetTags` die Daten, die das Spiel aus dieser Datei geladen hat, für den Rest der Sitzung. Jede spätere Kopie der Mission sieht die Änderung, und Effekte, die du hinzufügst, stapeln sich. Stats und Chancen kannst du frei anpassen; Effekte und Sperren fügst du nur in reinen Skript-Missionen hinzu.

### send_mission_event

Wird aufgerufen, während die Mission in der Luft ist, einmal pro Fortschrittsschritt. Eine Mission mit JSON-Datei hat immer drei Schritte; eine reine Skript-Mission so viele, wie [`get_mission_events_count`](#get_mission_events_count) zurückgibt. Die Schritte verteilen sich gleichmäßig über die Flugzeit, der letzte liegt am Ende.

Der Handler erfährt nicht, welcher Schritt gerade dran ist. Frag nach:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        ...
    elif events_sent == 2:
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        ...
```

`GetNumberOfEventsSent` gibt beim ersten Aufruf 1 zurück, beim zweiten 2 und so weiter.

**Einmal würfeln, danach nur lesen.** `MakeAsPlannedRoll` und `MakeSkillRoll` würfeln und speichern das Ergebnis; `GetAsPlannedRoll` und `GetSkillRoll` lesen das gespeicherte Ergebnis. Mach den Wie-geplant-Wurf zuerst, denn der Fertigkeitswurf entscheidet damit, gegen welchen Stat gewürfelt wird. Jeder spätere Handler liest nur. Ein zweiter Wurf würde dem Spieler eine Geschichte erzählen und ihm den Ausgang einer anderen präsentieren.

Wenn du diesen Handler überschreibst, musst du beide Würfe selbst machen. Der Ausgangsschritt liest sie.

### set_mission_impact

Wird aufgerufen, wenn der Flug vorbei ist und der Ausgang feststeht. Effekte aus dem JSON-Ausgang sind schon angewendet, und `missions_api.IsMissionSuccessful` liefert bereits die Antwort.

Nutze ihn für Folgen, die das JSON nicht ausdrücken kann, und um Folgemissionen zu vergeben:

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
```

Siehe [Ketten und Kampagnen](chains.md#when-json-is-not-enough).

### send_mission_result_event

Wird aufgerufen, nachdem die Flugzeuge von einer Mission zurückgekommen sind, die bis zum Ende geflogen wurde - immer, außer wenn die Mission abgebrochen wurde. Die übliche Aufgabe ist eine Abschlusszeile im Ereignisprotokoll mit `event_log.Create`. Die Python-Konstante ist `MissionEvent.SEND_MISSION_RESULT_EVENT`, der Event-String `send_mission_result_text`.

### send_mission_cancelled_event

Wird statt `send_mission_result_event` aufgerufen, wenn der Spieler die Mission abbricht oder sie verfällt. Die Python-Konstante ist `MissionEvent.SEND_MISSION_CANCELLED_EVENT`, der Event-String `send_mission_cancelled_text`. Eine abgebrochene Mission wendet keinen Ausgang an und zählt für Ketten als `cancelled`, nicht als Fehlschlag.

### get_mission_result_text

Wird aufgerufen, wenn der Spieler das Ergebnisfenster einer Mission öffnet, die bis zum Ende geflogen wurde. Gib den Textschlüssel der Zeile zurück, die das Fenster zeigen soll. Lies hier nur die Würfe; würfle nie selbst.

```python
@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"
    return "missions/{}/{}_{}_transmission".format(MISSION_ID, prefix, suffix)
```

Ein Schlüssel der Form `missions/<id>/<slot>` greift auch auf den `_raw*`-Text der Mission aus dem JSON zurück (siehe [Lokalisierung](../scripting/localization.md#text-in-the-json-instead-of-a-term)).

### get_mission_name

Reine Skript-Missionen. Gibt den Textschlüssel des Missionsnamens zurück. Standard, wenn er fehlt: die Missions-Id.

### get_mission_description_text

Reine Skript-Missionen. Gibt den Textschlüssel der Beschreibung im Missionsfenster zurück. Standard, wenn er fehlt: leer.

### get_time_to_start

Reine Skript-Missionen. Gibt zurück, wie viele Spielminuten die Mission auf der Kriegskarte wartet, bevor sie abläuft. Standard, wenn er fehlt: 60.

### get_completion_time

Reine Skript-Missionen. Gibt die Flugzeit in Spielminuten zurück. Standard, wenn er fehlt: 120.

### get_threat_level

Reine Skript-Missionen. Gibt den Textschlüssel der Bedrohungszeile im Missionsfenster zurück. Standard, wenn er fehlt: `Low`.

### get_enemy_count

Reine Skript-Missionen. Gibt die Anzahl der gemeldeten feindlichen Flugzeuge zurück. Standard, wenn er fehlt: 0. Es gibt keinen API-Aufruf, um sie später zu ändern, bei der zweiten und jeder weiteren Erstellung einer reinen Skript-Mission ist die Anzahl also 0.

### get_mission_events_count

Reine Skript-Missionen. Gibt zurück, wie oft [`send_mission_event`](#send_mission_event) während des Flugs feuert. Standard, wenn er fehlt: 3.

### get_fuel_level

Reine Skript-Missionen. Gibt den Treibstoff zurück, den der Flug kostet. Standard, wenn er fehlt: 100. Ruft das Skript `SetMissionLocation` auf, wird der Treibstoff aus der Entfernung zu diesem Ort neu berechnet.

### get_mission_result

Gibt `True` zurück, wenn die Mission erfolgreich war, sonst `False`. Jede reine Skript-Mission muss ihn definieren: Er entscheidet über das Ende, und ohne ihn scheitert die Mission beim Abschluss mit einem Fehler.

```python
@event_handler(MissionEvent.GET_MISSION_RESULT)
def get_mission_result(mission_entity_id):
    return missions_api.GetAsPlannedRoll(mission_entity_id) and missions_api.GetSkillRoll(mission_entity_id)
```

### get_mission_icon

Wird nie aufgerufen. Das Symbol kommt aus `_missionIcon` im JSON. Alte Beispielskripte implementieren diesen Handler ausführlich; dieser Code tut nichts.

### calculate_mission_modifiers

Wird nie aufgerufen. Implementiere ihn nicht.

### calculate_airplane_modifiers

Wird nie aufgerufen. Implementiere ihn nicht.

### calculate_pilot_modifiers

Wird nie aufgerufen. Implementiere ihn nicht.

`get_mission_fatalities`, das in sehr alter Dokumentation auftaucht, gibt es überhaupt nicht mehr. Verluste kommen aus dem Ausgangseffekt `Damage`.

## JSON-Schema

Die Missionsdatei wird Feld für Feld gelesen. Feldnamen beginnen mit einem Unterstrich und müssen exakt geschrieben sein; ein unbekanntes oder falsch geschriebenes Feld wird stillschweigend ignoriert. Zum Laden ist jedes Feld optional, aber eine spielbare Mission braucht die mit **Pflicht** markierten.

| Feld | Typ | Bedeutung |
|---|---|---|
| `_maxPlaneSlots` | int | Wie viele Flugzeuge der Spieler zuweisen darf. |
| `_timeToStartRange` | `{"x": min, "y": max}` | Minuten, die die Mission auf der Kriegskarte wartet, bevor sie abläuft, gewürfelt zwischen min und max. Wird bei historischen Missionen ignoriert. |
| `_timeToCompleteRange` | `{"x": min, "y": max}` | Flugzeit in Minuten, gewürfelt zwischen min und max. |
| `_missionRequirements` | Liste | Sperren, die alle erfüllt sein müssen, bevor die Mission erscheinen kann. Siehe [Voraussetzungen](#requirements). |
| `_missionOutcomes` | Liste | **Pflicht, genau 4**, in der festen Reihenfolge. Siehe [Ausgänge](#outcomes). |
| `_asPlannedChance` | int | Chance in Prozent (0–100), dass die Mission wie geplant läuft. |
| `_missionStats` | Liste | **Pflicht, mindestens 2.** Der erste wird gewürfelt, wenn die Mission wie geplant läuft, der zweite, wenn nicht. Siehe [Missions-Stats](#mission-stats). |
| `_enemyPlaneReport` | int | Feindliche Flugzeuge, die im Missionsfenster angezeigt werden. Bleib bei 18 oder darunter; darüber warnt der Validator. |
| `_missionIcon` | String | Das Symbol auf der Kriegskarte. Siehe [Symbole](#icons). |
| `_potentialLocations` | Liste | Mögliche Orte auf der Kriegskarte; pro Mission wird einer gezogen. Entfernung und Treibstoff ergeben sich daraus. Bei einer leeren Liste wählt das Spiel einen zufälligen Ort. Siehe [Einsatzorte](locations.md). |
| `_difficultyRating` | int | Sterne, die dem Spieler angezeigt werden, 1–3. Standard 1. |
| `_tags` | Liste von Strings | Zu welchen Karten die Mission gehört. Siehe [Karten-Tags](#map-tags). |
| `_isHistoric` | bool | Macht die Mission zu einem Story-Moment. Siehe [Ketten und Kampagnen](chains.md#historic-missions). |
| `_historicDay` | Datum | Der genaue Tag, an dem eine historische Mission erscheint. Ein Jahr unter 1900 zählt als "kein Datum". |
| `_rawMissionName` ... `_rawGwFailureTransmission` | String | Neun optionale Textfelder. Siehe [Lokalisierung](../scripting/localization.md#text-in-the-json-instead-of-a-term). |
| `_distanceLocationDependant` | `{"x", "y"}` | Wird von Blindflugs eigenem Missionswerkzeug geschrieben. Das Spiel liest es nicht; lass es in Ruhe oder weg. |

Daten werden als Objekt geschrieben:

```json
"_historicDay": { "Year": 1940, "Month": 8, "Day": 13, "Hour": 0, "Minute": 0 }
```

Felder, die ältere Dateien und ältere Dokumentation enthalten und die das Spiel nicht mehr liest: `_distanceRange`, `_hasMaximumDay`, `_maximumDay`, `_mapId`, `_mapIds`, `_mapTags`, `_missionTags`. Eine Mission, die sich noch auf `_mapTags` verlässt, verliert ihre Kartenbeschränkung ohne jede Warnung und erscheint überall. Verwende `_tags`.

Die `"Name"`-Einträge in Listen (`"Name": "RunwayTier"`) sind Beschriftungen für Menschen. Das Spiel ignoriert sie.

### Voraussetzungen { #requirements }

Jeder Eintrag in `_missionRequirements` ist eine Sperre. Alle Sperren müssen erfüllt sein.

```json
"_missionRequirements": [
    { "Name": "RunwayTier",            "_requirementType": 0, "_value": "1" },
    { "Name": "EarliestAppearanceDay", "_requirementType": 1, "_value": "3" }
]
```

`_value` ist immer ein String, auch bei Zahlen.

| `_requirementType` | Name | `_value` | Erfüllt, wenn |
|---|---|---|---|
| 0 | `RunwayTier` | Stufe als Zahl, `"2"` | die Basis eine Landebahn mindestens dieser Stufe hat |
| 1 | `EarliestAppearanceDay` | Tage, `"14"` | die Tageszahl, gezählt ab dem Startdatum der Karte, diesen Wert erreicht hat |
| 2 | `LatestAppearanceDay` | Tage, `"40"` | die Tageszahl, gezählt ab dem Startdatum der Karte, diesen Wert noch nicht überschritten hat |
| 3 | `CompletedMission` | `"<missionId>"` oder `"<missionId>,<outcome>"` | der Spieler diese Mission mindestens einmal mit diesem Ausgang beendet hat |

Bei `CompletedMission` ist der Ausgang `success`, `failure` oder `cancelled`. Ohne Ausgang zählt jeder Abschluss, auch ein abgebrochener. Das Spiel merkt sich jeden Abschluss, nach einem gescheiterten und einem späteren erfolgreichen Versuch sind also sowohl `,failure` als auch `,success` erfüllt. Siehe [Ketten und Kampagnen](chains.md).

### Ausgänge { #outcomes }

Genau vier Einträge, in der Reihenfolge des [Ausgang-Index](#the-two-rolls-and-the-outcome-index):

```json
{
    "Name": "3 - as planned, skill passed",
    "_missionSuccess": true,
    "_outcomeEffect": [
        { "_outcomeEffectType": 7, "_effectValue": "5",     "_effectIcon": "ui_resource_victoryPoints" },
        { "_outcomeEffectType": 5, "_effectValue": "15",    "_effectIcon": "ui_confidence" },
        { "_outcomeEffectType": 3, "_effectValue": "10-40", "_effectIcon": "ui_health_poor_injured" }
    ]
}
```

| Feld | Bedeutung |
|---|---|
| `_missionSuccess` | Ob dieses Ende als Erfolg zählt, für Ketten, Quests und die Akten des Spielers. |
| `_outcomeEffect` | Liste von Effekten, die angewendet werden, wenn die Mission so endet. Darf leer sein. |
| `_outcomeEffectType` | Welcher Effekt, siehe die Tabelle unten. |
| `_effectValue` | Ein String. Eine ganze Zahl für alles außer `Damage`; ein Bereich `"min-max"` für `Damage`. |
| `_effectIcon` | Symbol neben dem Effekt im Ergebnisfenster. Kopier es aus einem Beispiel; ein leerer String zeigt kein Symbol. |

| `_outcomeEffectType` | Name | `_effectValue` | Effekt |
|---|---|---|---|
| 0 | `CrewMood` | Zahl, `"-20"` | Stimmung aller, die geflogen sind |
| 1 | `CrewConfidence` | Zahl | Selbstvertrauen aller, die geflogen sind |
| 2 | `CrewEnergy` | Zahl | Energie aller, die geflogen sind |
| 3 | `Damage` | Bereich, `"20-60"` | Schaden an den Flugzeugen, pro Flug gewürfelt; schwerer Schaden verletzt auch die Crew |
| 4 | `BaseMood` | Zahl | Stimmung der ganzen Basis |
| 5 | `BaseConfidence` | Zahl | Selbstvertrauen der ganzen Basis |
| 6 | `BaseEnergy` | Zahl | Energie der ganzen Basis |
| 7 | `VictoryPoints` | Zahl | Siegpunkte, begrenzt auf das aktuelle Limit |
| 8 | `MaxVictoryPoints` | - | **nicht verwenden.** Das Spiel nutzt ihn intern, um "Siegpunktlimit erreicht" anzuzeigen; in einer Missionsdatei bringt er die Mission beim Ende zum Absturz. |

Eine Zahl, wo ein Bereich erwartet wird, oder umgekehrt, ist kein Absturz: Das Spiel schreibt einen Fehler in `Player.log` und überspringt diesen einen Effekt.

### Missions-Stats { #mission-stats }

```json
"_missionStats": [
    { "Name": "Recon",           "_missionSkillType": 2, "_statRange": { "x": 10.0, "y": 45.0 } },
    { "Name": "Maneuverability", "_missionSkillType": 4, "_statRange": { "x": 20.0, "y": 60.0 } }
]
```

`_statRange` ist der Bereich, in dem der Zielwert gewürfelt wird. Die zusammengezählte Fertigkeit der Staffel muss ihn erreichen. Die mitgelieferten Missionen liegen bei einer gewöhnlichen Patrouille um 40–70; ab 85 soll eine Mission öfter verloren als gewonnen werden.

| `_missionSkillType` | Name |
|---|---|
| 0 | `Fight` |
| 1 | `Bomb` |
| 2 | `Recon` |
| 3 | `Transport` |
| 4 | `Maneuverability` |
| 5 | `Stealthiness` |

### Symbole { #icons }

Werte für `_missionIcon`:

| Wert | Verwendung |
|---|---|
| `Fight`, `Recon`, `Bomb`, `Transport`, `Maneuverability`, `Stealth`, `Luxury` | Symbole für Missionstypen |
| `Success`, `Failure` | Ergebnismarkierungen |
| `Cancel` | Markierung für abgebrochen |

Achte auf die Schreibweise: Das Symbol heißt `Stealth`, der Fertigkeitstyp `Stealthiness`.

### Orts-Flags { #location-flags }

Jeder Ort auf der Kriegskarte trägt Flags, die ihn beschreiben. Sie sind eine Bitmaske: Addiere die Zahlen (`10` = See und Feindgebiet).

| Wert | Flag |
|---|---|
| 0 | `None` |
| 1 | `Land` |
| 2 | `Sea` |
| 4 | `OwnTerritory` |
| 8 | `EnemyTerritory` |

Die Liste der Orte mit ihren Koordinaten steht auf der Seite [Einsatzorte](locations.md). Kopier die Koordinaten exakt: Das Spiel misst Entfernung und Treibstoff an den Koordinaten in deiner Datei, nicht am Namen.

### Karten-Tags { #map-tags }

```json
"_tags": ["campaign_debden"]
```

Eine Karte listet in ihrer `Metadata.json` die Tags, die sie unterstützt, und eine Mission listet die Tags, für die sie geschrieben ist. Die Mission kann nur auf einer Karte erscheinen, wenn beide Listen mindestens einen Tag gemeinsam haben (Groß- und Kleinschreibung spielt keine Rolle). Eine leere oder fehlende Liste auf einer der beiden Seiten zählt als `["default"]`, und jede eingebaute Karte unterstützt `default`, eine Mission ohne Tags erscheint also überall.

Eine Mission, die nur mit `campaign_debden` getaggt ist, erscheint nur auf Karten, die diesen Tag listen. Eine Mission, die auf deiner Kampagnenkarte und überall sonst erscheinen soll, listet beide: `["campaign_debden", "default"]`.

Tags werden von der wöchentlichen Ziehung, vom historischen Erscheinen und von `missions_api.CreateMission` geprüft. Der Cheat `create_mission` ignoriert sie. Quests haben keine Tags; eine Karte wählt ihre Quests auf andere Weise (siehe [Quests](../quests/index.md)).

## Bekannte Stolperfallen { #known-pitfalls }

| Problem | Was du siehst | Lösung |
|---|---|---|
| Nicht genau 4 `_missionOutcomes` | Absturz, wenn die Mission endet | immer 4, in Index-Reihenfolge |
| Weniger als 2 `_missionStats` | Absturz beim Fertigkeitswurf | immer mindestens 2 |
| `.py` anders benannt als die `.json` | das Skript wird ignoriert, das Standardskript läuft | identische Dateinamen |
| Id schon von einer eingebauten Mission oder einer anderen Mod belegt | eine Mission ersetzt die andere stillschweigend | Ids mit deinem Mod-Namen versehen |
| Ein nie aufgerufener Handler ist implementiert | nichts passiert | lösch ihn |
| `MaxVictoryPoints` in einem Ausgang | Absturz, wenn die Mission endet | `VictoryPoints` verwenden |
| `_coordinates` auf 0, 0 gelassen | die Mission liegt weit weg, mit riesigen Treibstoffkosten | Koordinaten von [Einsatzorte](locations.md) kopieren |
| Altes Feld `_mapTags` statt `_tags` | Kartenbeschränkung geht stillschweigend verloren | in `_tags` umbenennen |
| Reine Skript-Mission ohne Sperren | erscheint überall, sobald sie einmal erstellt wurde | `AddMissionRequirement` in `initialize_mission` |
