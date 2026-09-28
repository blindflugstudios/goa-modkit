# Ketten und Kampagnen

Eine Mission ist ein Einsatz. Mehrere Missionen, die aufeinander folgen, sind eine Geschichte. Diese Seite behandelt drei Stufen davon, von reinem JSON bis zu einer Kampagne mit Gedächtnis:

1. **Ketten:** Eine Mission erscheint erst, nachdem eine andere auf eine bestimmte Weise ausgegangen ist. Nur JSON.
2. **Historische Missionen:** Story-Momente, die garantiert erscheinen, auf Wunsch an einem echten Datum. Nur JSON.
3. **Kampagnen:** Folgemissionen, die vom Zählen, vom Erinnern an Personen oder von Entscheidungen des Spielers abhängen. Braucht ein Skript.

Funktionierende Beispiele: `chain_convoy` (eine Gabelung), `chain_airfield` (eine gerade Linie mit vier Stufen) und `campaign_kanalkampf` (eine Kampagne). Siehe [Beispiele](../examples.md).

## Auf einen Ausgang verketten { #chaining-on-an-outcome }

Eine Voraussetzung vom Typ 3, `CompletedMission`, lässt eine Mission auf eine andere warten:

```json
{ "Name": "CompletedMission", "_requirementType": 3, "_value": "mymod_convoy_spotted,success" }
```

Der Wert ist eine Missions-Id, optional gefolgt von einem Komma und dem Ausgang, mit dem sie geendet haben muss:

| Wert | Bedeutung |
|---|---|
| `"mymod_convoy_spotted"` | beendet, mit beliebigem Ausgang (auch abgebrochen) |
| `"mymod_convoy_spotted,success"` | erfolgreich beendet |
| `"mymod_convoy_spotted,failure"` | geflogen und gescheitert |
| `"mymod_convoy_spotted,cancelled"` | vom Spieler abgebrochen oder verfallen |

`cancelled` ist ein eigener Ausgang: Eine Mission, die der Spieler abgebrochen hat, zählt nicht als Fehlschlag.

"Erfolg" hängt von der Position des Ausgangs ab, den die Würfel gewählt haben: Index 1 (schiefgelaufen, Fertigkeit bestanden) und Index 3 (wie geplant, Fertigkeit bestanden) zählen als Erfolg, Index 0 und 2 als Fehlschlag.

Das Spiel merkt sich jeden Abschluss für die ganze Kampagne. Ein Spieler, der eine Mission verloren und später gewonnen hat, erfüllt sowohl `,failure` als auch `,success`.

## Verzweigen { #branching }

Zwei Folgemissionen, die an gegensätzliche Ausgänge gebunden sind, ergeben eine Gabelung:

```text
mymod_convoy_spotted
   |
   +-- success --> mymod_convoy_strike
   |
   +-- failure --> mymod_convoy_search
```

Nichts hindert dich daran, mehrere Missionen an denselben Ausgang zu binden oder weitere Schritte an die Folgemissionen zu hängen. Voraussetzungen werden mit UND verknüpft, eine Mission kann also sowohl einen abgeschlossenen Vorgänger als auch eine Landebahnstufe verlangen:

```json
"_missionRequirements": [
    { "Name": "RunwayTier",       "_requirementType": 0, "_value": "2" },
    { "Name": "CompletedMission", "_requirementType": 3, "_value": "mymod_convoy_spotted,success" }
]
```

Es gibt kein ODER. Wenn einer von zwei Vorgängern reichen soll, schreib zwei Versionen der Folgemission.

## Historische Missionen { #historic-missions }

Eine normale Mission liegt in einem Pool und wird über die Woche verteilt zufällig gezogen. Für eine Folgemission ist das meistens falsch: Der Spieler schließt Schritt eins ab und wartet dann, womöglich wochenlang, womöglich für immer, wenn der Pool groß ist.

`"_isHistoric": true` ändert das. Eine historische Mission:

- **kommt nie in die Zufallsziehung.** Sobald ihre Sperren erfüllt sind, erscheint sie garantiert.
- **erscheint an ihrem Datum**, wenn sie einen `_historicDay` hat: genau an diesem Tag, wenn auch ihre anderen Sperren erfüllt sind. Dafür werden die Wochen-Slots nicht genutzt.
- **behält die normale Vorlaufzeit**, wenn sie keinen `_historicDay` hat: Sie erscheint zusammen mit der nächsten Wochenmission und belegt keinen der Slots dieser Woche. So kommt eine Folgemission mit derselben Verzögerung wie jede andere Mission an, statt sofort auf der Karte zu landen.
- **läuft nie ab.** `_timeToStartRange` wird ignoriert, der Spieler hat also unbegrenzt Zeit, sie zu fliegen.
- **gibt es bei Erfolg nur einmal.** Einmal gewonnen, erscheint sie nie wieder. Ein gescheiterter oder abgebrochener Versuch bringt sie zurück, eine Kette, die an `success` gebunden ist, lässt sich also wiederholen.
- **ist nie zweimal auf der Karte.** Solange eine Kopie wartet oder in der Luft ist, erscheint keine zweite.

Ihre Sperren werden mit UND verknüpft:

| Hat eine `CompletedMission`-Sperre | Hat einen `_historicDay` | Erscheint |
|---|---|---|
| nein | nein | zusammen mit der nächsten Wochenmission |
| ja | nein | zusammen mit der nächsten Wochenmission, nachdem der Vorgänger richtig ausgegangen ist |
| nein | ja | genau an diesem Tag |
| ja | ja | genau an diesem Tag, sobald der Vorgänger richtig ausgegangen ist |

Genau diese Kombination braucht ein Story-Moment. Verwende sie für jeden Schritt einer Kette, meistens außer dem ersten.

### Steuern, wann eine Kette beginnen kann { #controlling-when-a-chain-can-start }

```json
"_isHistoric": true,
"_historicDay": { "Year": 1940, "Month": 8, "Day": 13, "Hour": 0, "Minute": 0 }
```

Die Mission erscheint genau an diesem Tag. Ein Jahr unter 1900 zählt als "kein Datum". Deshalb tragen Beispieldateien `"Year": 1`, wenn sie keins meinen.

Um eine Mission ab einem bestimmten Zeitpunkt zu sperren, verwende eine `LatestAppearanceDay`-Voraussetzung (Typ 2), gezählt in Tagen ab dem Startdatum der Karte. Das funktioniert bei jeder Mission, ob historisch oder nicht.

Zusammengesetzt wird so jede Operation an ihrem echten Datum verfügbar, und eine verpasste kann wieder geschlossen werden.

## Stolperfallen { #pitfalls }

**Doppelte Ids.** Zwei Missionen mit derselben Id bedeuten, dass eine die andere stillschweigend ersetzt, abhängig von der Ladereihenfolge. Setz deinen Mod-Namen vor jede Id und denk beim Umbenennen daran, die Ids in jedem `CompletedMission`-Wert anzupassen.

**`_isHistoric` bei Folgemissionen vergessen.** Die Kette funktioniert, aber Schritte tauchen womöglich erst nach sehr langer Zeit auf, und ein abgeschlossener Schritt kann erneut gezogen werden.

**Mehrere historische Missionen gleichzeitig fällig.** Sie erscheinen alle zusammen: die datierten an ihrem Tag, die undatierten zusammen mit derselben Wochenmission. Wenn sie nacheinander kommen sollen, verkette sie über ihre Ausgänge oder gib ihnen verschiedene Tage.

**Verketten auf eine Mission, die nie erscheint.** Eine Sperre auf eine Mission, deren eigene Voraussetzungen nie erfüllt sind oder die für eine andere Karte getaggt ist, blockiert stillschweigend den Rest der Kette. Teste jeden Schritt einzeln, bevor du sie verbindest.

**Testen mit dem Cheat.** `create_mission` ignoriert jede Sperre. Es beweist, dass eine Mission lädt, nicht, dass die Kette freigeschaltet wird. Siehe [Testen und neu laden](../basics/testing.md#testing-a-chain).

## Wenn JSON nicht reicht { #when-json-is-not-enough }

Eine Voraussetzung kann nur nach dem Ausgang einer vorherigen Mission fragen. Wenn die Bedingung etwas anderes ist (wer geflogen ist, wie die Basis aussieht, wie oft das schon passiert ist), kann ein Skript die Folgemission selbst erstellen:

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
```

`CreateMission` setzt die Mission sofort auf die Kriegskarte und überspringt die wöchentliche Ziehung. Die eigenen Voraussetzungen und Karten-Tags der Zielmission prüft es trotzdem: Sind sie nicht erfüllt, wird nichts erstellt und eine Warnung in `Player.log` geschrieben. Ruf es aus `set_mission_impact` auf, wo der Ausgang bekannt ist; aus `initialize_mission` wird es abgelehnt.

Wovor es dich nicht schützt: Nichts hindert ein Skript daran, dieselbe Mission zweimal zu vergeben, und eine historische Mission, die so erstellt wird, wird nicht so blockiert wie beim automatischen Erscheinen.

Nimm den JSON-Weg, wo immer er passt. Er übersteht Speichern und Laden, der Validator kann ihn prüfen, und er kann keine Mission vergeben, die die Basis nicht fliegen kann. Greif zu `CreateMission`, wenn die Entscheidung wirklich von etwas abhängt, das nur ein Skript sehen kann.

## Von der Kette zur Kampagne { #from-a-chain-to-a-campaign }

Eine Kette hat kein Gedächtnis. Flieg `chain_airfield` zweimal, und es spielt sich beide Male gleich, weil jede Bedingung darin ein einzelnes Ja oder Nein über die Mission davor ist.

Eine Kampagne erinnert sich. `game_api.GetScriptDataPath(id)` gibt deinem Skript einen eigenen Ordner im Spieldatenordner; eine JSON-Datei darin übersteht den Flug, den Tag und die Sitzung.

```python
import json
import os

CAMPAIGN_ID = "mymod_campaign"

DEFAULTS = {
    "raids_survived": 0,
    "raids_lost": 0,
    "first_blood": None,
}


def _path():
    # The folder belongs to the id, NOT to the save game. Without the save's
    # guid in the file name, a second save would continue - and overwrite -
    # the first one's campaign.
    return os.path.join(
        game_api.GetScriptDataPath(CAMPAIGN_ID),
        "campaign_{}.json".format(game_api.GetAirBaseGuid())
    )


def load():
    state = dict(DEFAULTS)

    try:
        with open(_path(), "r") as handle:
            state.update(json.load(handle))
    except (IOError, OSError, ValueError):
        pass          # no file yet, or a half-written one: start clean

    return state


def save(state):
    try:
        with open(_path(), "w") as handle:
            json.dump(state, handle)
    except (IOError, OSError):
        pass          # the mission must still fly
```

Die Id, die du an `GetScriptDataPath` übergibst, darf nur Buchstaben, Ziffern, `_`, `-` und `.` enthalten, höchstens 64 Zeichen.

Drei Dinge gehen leicht schief, und alle drei rächen sich erst später, nicht sofort:

1. **Gib jedem Schlüssel einen Standardwert.** Sonst scheitert ein Spielstand, der geschrieben wurde, bevor du einen Schlüssel ergänzt hast, beim Laden mit einem `KeyError`, in einem Handler, mitten im Flug.
2. **Nimm die Guid des Spielstands in den Dateinamen auf.** `GetScriptDataPath` liefert einen Ordner pro Id, den sich alle Spielstände teilen.
3. **Pack jedes Lesen und Schreiben in try/except.** Eine Kampagne, die ihren Zustand nicht schreiben kann, muss die Mission trotzdem fliegen lassen.

Mod-Skripte können einander importieren. Pack den Zustand also in ein Modul (etwa `mymod_campaign_state.py` im selben `Missions/`-Ordner), das jede Mission importiert. Dann können sie sich nicht darüber uneinig sein, was passiert ist.

### Was dir das Gedächtnis bringt { #what-the-memory-buys-you }

Bedingungen, die keine Voraussetzung ausdrücken kann:

```python
state = campaign_state.load()

if state["raids_lost"] >= 3:
    missions_api.CreateMission("mymod_regroup")     # counting
elif state["first_blood"] is not None:
    pass                                            # remembering a person
```

Außerdem kann sich eine Mission in `initialize_mission` an der bisherigen Kampagne ausrichten:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    state = campaign_state.load()

    if state["raids_survived"] >= 2:
        # The enemy has seen this squadron before.
        missions_api.SetMissionStat(mission_entity_id, "Fight", 76, 115)
        missions_api.SetAsPlannedChance(mission_entity_id, 35)
```

Dieselbe Mission, dasselbe JSON, beim fünften Mal messbar schwerer als beim ersten.

Das Beispiel `campaign_kanalkampf` ist die ausgearbeitete Fassung: fünf Missionen, von denen zwei Bedingungen auf Zählungen beruhen. Die Seite [Beispiele](../examples.md) vergleicht es mit den Ketten.
