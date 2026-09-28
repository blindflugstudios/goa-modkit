# Deine erste Mission

Eine Mission ist ein Einsatz, zu dem der Spieler Flugzeuge schickt. Am Ende dieser Seite hast du eine von Grund auf selbst geschrieben, installiert und auf der Kriegskarte gesehen.

Du brauchst zwei Dateien, beide nach deiner Mission benannt:

- eine `.json`-Datei mit den Zahlen: wann die Mission erscheint, wie schwer sie ist, was sie kostet und was sie einbringt
- eine `.py`-Datei mit dem Text: was die Crew per Funk meldet und wie es sich hinterher liest

Die `.py`-Datei ist optional (du kannst den Text auch ins JSON schreiben, siehe [Lokalisierung](../scripting/localization.md#text-in-the-json-instead-of-a-term)), aber wenn du eine schreibst, lernst du, wie Missionen funktionieren. Deshalb verwendet diese Seite eine.

Das fertige Ergebnis ist das Beispiel `coastal_patrol`: [examples/coastal_patrol](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/coastal_patrol). Es zu kopieren und abzuändern ist der schnellste Einstieg.

## 1. Such dir eine Id aus { #1-pick-an-id }

Die **Id** ist der Name der Mission im Spiel. Sie ist der Dateiname ohne Endung und steckt in jedem Textschlüssel, den die Mission verwendet.

Sie muss unter allen Missionen, die das Spiel kennt, einmalig sein, auch gegenüber den eingebauten und den Mods anderer Leute. Ein Duplikat erzeugt keinen Fehler: Es ersetzt die andere Mission stillschweigend. Setz deshalb deinen Mod-Namen vor deine Ids:

```text
mymod_coastal_patrol
```

Verwende nur Buchstaben, Ziffern und Unterstriche.

## 2. Schreib das JSON { #2-write-the-json }

Leg `mymod_coastal_patrol.json` an. Am einfachsten startest du mit einer Kopie von `coastal_patrol.json` aus dem Beispiel. Über diese Teile solltest du nachdenken.

### Wann sie erscheinen kann { #when-it-can-appear }

```json
"_missionRequirements": [
    { "Name": "RunwayTier",            "_requirementType": 0, "_value": "1" },
    { "Name": "EarliestAppearanceDay", "_requirementType": 1, "_value": "3" }
]
```

Jeder Eintrag ist eine Sperre, und alle müssen erfüllt sein. Typ 0 ist die Landebahnstufe, die die Basis haben muss; Typ 1 ist der früheste Tag, gezählt ab dem Startdatum der Karte. Typ 3 lässt die Mission auf eine andere folgen, siehe [Ketten und Kampagnen](chains.md). Die vollständige Liste steht in der [Referenz](reference.md#requirements).

### Wie die Würfel fallen { #how-the-dice-fall }

Zwei Würfe entscheiden jede Mission:

1. `_asPlannedChance` (0–100) ist die Chance, dass die Mission **wie geplant läuft**.
2. Danach entscheidet ein **Fertigkeitswurf**, ob die Crew es schafft.

Zwei Würfe mit je zwei möglichen Antworten ergeben vier mögliche Enden.

### Die vier Ausgänge: Die Reihenfolge ist Pflicht { #the-four-outcomes-order-is-mandatory }

```text
index 0   gone wrong,  skill failed
index 1   gone wrong,  skill passed
index 2   as planned,  skill failed
index 3   as planned,  skill passed
```

`_missionOutcomes` muss genau vier Einträge haben, in genau dieser Reihenfolge. Das Spiel prüft das nicht: Mit weniger als vier stürzt die Mission ab, wenn sie endet.

Jeder Ausgang legt fest, ob er als Erfolg zählt (`_missionSuccess`), und trägt Effekte: Moral der Crew oder der Basis, Schaden an den Flugzeugen, Siegpunkte.

```json
{
    "Name": "3 - as planned, skill passed",
    "_missionSuccess": true,
    "_outcomeEffect": [
        { "_outcomeEffectType": 7, "_effectValue": "1",  "_effectIcon": "ui_resource_victoryPoints" },
        { "_outcomeEffectType": 5, "_effectValue": "15", "_effectIcon": "ui_confidence" }
    ]
}
```

`_effectValue` steht immer in Anführungszeichen. Bei `Damage` (Typ 3) ist es ein Bereich wie `"20-60"`, der pro Flug gewürfelt wird. Bei allem anderen ist es eine ganze Zahl wie `"-40"`. Alle Effekttypen stehen in der [Referenz](reference.md#outcomes).

### Die Stats: mindestens zwei { #the-stats-at-least-two }

```json
"_missionStats": [
    { "Name": "Recon",           "_missionSkillType": 2, "_statRange": { "x": 10.0, "y": 45.0 } },
    { "Name": "Maneuverability", "_missionSkillType": 4, "_statRange": { "x": 20.0, "y": 60.0 } }
]
```

Der erste Eintrag gilt, wenn die Mission wie geplant läuft, der zweite, wenn sie schiefgeht. Der Bereich ist die Schwierigkeit: Das Spiel würfelt darin einen Zielwert, und die zusammengezählte Fertigkeit der Staffel muss ihn erreichen. Mit weniger als zwei Einträgen stürzt der Fertigkeitswurf ab.

### Wo sie stattfindet { #where-it-happens }

`_potentialLocations` listet mögliche Orte auf der Kriegskarte. Jedes Mal, wenn die Mission erscheint, wird einer davon gezogen. Kopier die Einträge von der Seite [Einsatzorte](locations.md), inklusive der Koordinaten: Das Spiel berechnet Entfernung und Treibstoff aus den Koordinaten in deiner Datei.

## Wie ein Missionsskript wirklich läuft { #how-a-mission-script-actually-runs }

Bevor es an den Code geht, eine Idee, die alles Weitere einfach macht: Ein Missionsskript ist **kein Programm, das von oben nach unten durchläuft**. Es ist eine Sammlung von Funktionen, die das Spiel zu festen Zeitpunkten aufruft. Du rufst sie nie selbst auf, und du schreibst nie eine Schleife, die auf etwas wartet.

Die Zeile `@event_handler(...)` über einer Funktion sagt, *wann* das Spiel sie aufrufen soll:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    ...
```

Das registriert `send_mission_event` für "im Flug ist ein Fortschrittsschritt passiert". Das Spiel ruft sie auf, übergibt ihr die Nummer der betreffenden Mission und macht etwas mit dem, was sie zurückgibt. Zwischen den Aufrufen tut dein Skript überhaupt nichts. So eine Funktion heißt **Handler**.

Alles außerhalb eines Handlers (Textdefinitionen, Konstanten, Hilfsfunktionen) läuft **einmal**, wenn das Spiel die Datei lädt. Deshalb wird Text auf der obersten Ebene der Datei registriert und nicht in einem Handler.

### Die Reihenfolge, in der das Spiel Handler aufruft { #the-order-the-game-calls-handlers-in }

Für einen Flug einer Mission:

| Wann | Handler | Typische Aufgabe |
|---|---|---|
| die Mission wird erstellt | `initialize_mission` | Zustand einrichten |
| im Flug, einmal pro Fortschrittsschritt | `send_mission_event` | würfeln und per Funk melden, was passiert |
| der Flug endet | `set_mission_impact` | auf den Ausgang reagieren |
| die Flugzeuge sind zurück | `send_mission_result_event` | eine Abschlusszeile im Ereignisprotokoll |
| der Spieler öffnet das Ergebnisfenster | `get_mission_result_text` | welchen Text dieses Fenster zeigt |

`send_mission_event` ist der Handler, der mehrmals feuert: dreimal bei einer Mission mit JSON-Datei, nach einem Drittel, nach zwei Dritteln und am Ende des Flugs. Er erfährt nicht, welcher Schritt gerade dran ist, also fragt das Skript nach:

```python
events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

if events_sent == 1:      # first step: roll whether it goes to plan
    ...
elif events_sent == 2:    # second step: roll whether the crew pulls it off
    ...
```

Mehr bedeuten die `events_sent`-Abfragen in Missionsskripten nicht: "Welcher meiner drei Momente in diesem Flug ist das?"

### Einmal würfeln, danach nur lesen { #roll-once-read-afterwards }

Jeder der beiden Würfe wird genau einmal gemacht:

- `MakeAsPlannedRoll` würfelt, ob es wie geplant läuft, und speichert das Ergebnis.
- `MakeSkillRoll` macht den Fertigkeitswurf und speichert ihn.

`GetAsPlannedRoll` und `GetSkillRoll` lesen das gespeicherte Ergebnis wieder aus. Jeder Handler nach dem Wurf verwendet `Get...`. Ein zweiter Wurf würde dem Spieler eine Geschichte erzählen und ihm den Ausgang einer anderen präsentieren.

### Welche Mission bin ich? { #which-mission-am-i }

Jeder Handler bekommt `mission_entity_id`: die Nummer der einen Mission, um die es bei diesem Aufruf geht. Dasselbe Skript kann gleichzeitig für zwei Flüge derselben Mission laufen, also speichere niemals Informationen zu einem einzelnen Flug in einer Variablen oben in der Datei. Frag `missions_api` nach der Nummer, die du bekommen hast.

## 3. Schreib das Python { #3-write-the-python }

Leg `mymod_coastal_patrol.py` neben das JSON. Das Skript hat zwei Aufgaben: den Text definieren und entscheiden, welcher Text wann erscheint.

### Die neun Texte definieren { #define-the-nine-texts }

Eine Mission verwendet neun Text-Slots, alle nach dem Muster `missions/<id>/<slot>` benannt. Registriere sie auf der obersten Ebene der Datei mit `localization.SetTerm`, damit sie existieren, sobald das Skript geladen ist:

```python
from Blindflug.FlightMission import MissionEvent

MISSION_ID = "mymod_coastal_patrol"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Coastal Patrol")
_term("mission_description", "Fly the shoreline. Report anything that moves.")
_term("intel_threat_report", "Low. No enemy activity reported.")
_term("ap_transmission", "Patrol is airborne. Clear skies along the coast.")
_term("gw_transmission", "Cloud came in thicker than forecast.")
_term("ap_success_transmission", "Patrol complete. Nothing to report.")
_term("ap_failure_transmission", "The patrol flew its route but came back with nothing usable.")
_term("gw_success_transmission", "Despite the weather the flight brought back a full report.")
_term("gw_failure_transmission", "The flight lost the coastline in the murk and turned back early.")
```

`ap` steht für "as planned" (wie geplant), `gw` für "gone wrong" (schiefgelaufen). Die ersten drei Namen liest das Spiel selbst, sie lassen sich nicht ändern; fehlt einer, bleibt dieser Platz im Spiel leer. Die anderen sechs verwendet das Skript, und jede mitgelieferte Mission nutzt genau diese Namen, also bleib dabei. Mehr unter [Lokalisierung](../scripting/localization.md).

### Drei Handler reichen { #three-handlers-are-enough }

**Die Id.** Gib genau den Dateinamen zurück:

```python
@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID
```

**Der Flug.** Würfle in den ersten beiden Schritten und melde per Funk, was passiert ist:

```python
@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        slot = "ap_transmission" if going_as_planned else "gw_transmission"
        event_log.Create("missions/{}/{}".format(MISSION_ID, slot))

    elif events_sent == 2:
        going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        event_log.Create("missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed)))
```

**Das Ergebnisfenster.** Hier nur die Würfe lesen, niemals würfeln:

```python
@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)
    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"
    return "{}_{}_transmission".format(prefix, suffix)
```

Für jeden Handler, den du nicht schreibst, springt das gemeinsame Standard-Missionsskript des Spiels ein. Deshalb fliegt auch eine Mission mit JSON-Datei und ganz ohne Skript: Das Standardskript macht genau das, was der Code oben macht.

## 4. Installieren und starten { #4-install-and-run }

Leg beide Dateien in den `Missions`-Ordner einer Mod:

```text
Mods/my_first_mod/Missions/mymod_coastal_patrol.json
Mods/my_first_mod/Missions/mymod_coastal_patrol.py
```

Wo `Mods/` auf deinem Computer liegt, erklärt [So funktionieren Mods](../basics/mods.md); im Spiel bringt dich **Hauptmenü** (Main menu) **→ Mods → Open folder** dorthin.

Starte dann das Spiel und lade einen Spielstand. Das Spiel liest Missionsdateien und Skripte bei jedem Laden eines Spielstands. Lief das Spiel schon, geh also zurück ins Hauptmenü und lade den Spielstand erneut.

Um die Mission zu sehen, ohne auf die wöchentliche Ziehung zu warten, öffne die Cheat-Konsole (siehe [Cheat-Konsole](../basics/cheats.md)) und tippe:

```text
create_mission mymod_coastal_patrol
```

Die Mission erscheint sofort auf der Kriegskarte. [Testen und neu laden](../basics/testing.md) erklärt die Bearbeitungsschleife und was du prüfen solltest, wenn nichts auftaucht.

## Was du nicht schreiben solltest { #what-not-to-write }

Vier Handler-Namen gibt es im Spiel, sie werden aber nie aufgerufen: `get_mission_icon`, `calculate_mission_modifiers`, `calculate_airplane_modifiers` und `calculate_pilot_modifiers`. Alte Skripte implementieren sie ausführlich. Dieser Code tut nichts. Das Symbol kommt aus `_missionIcon` im JSON.

## Wie es weitergeht { #going-further }

- Missionen, die andere Missionen freischalten: [Ketten und Kampagnen](chains.md)
- Skripte, die auf die Basis reagieren, statt eine Mission zu besitzen: [Events](../scripting/events.md)
- Jeder Handler, jedes Feld und jede Zahl: [Referenz](reference.md)
