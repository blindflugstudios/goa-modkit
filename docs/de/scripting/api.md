# API

Alles, was ein Mod-Skript aufrufen kann. Acht Objekte stehen in jedem Skript ohne Import bereit, dazu der Decorator `event_handler`:

| Name | Zweck |
|---|---|
| `event_handler` | der Decorator, der einen Handler registriert, siehe [Events](events.md#the-decorator) und [Missionen](../missions/reference.md#handlers) |
| `event_log` | Zeilen ins Ereignisprotokoll im Spiel schreiben |
| `localization` | Text definieren oder überschreiben |
| `missions_api` | Missionszustand, Würfelwürfe, Missionen aus einem Skript heraus schreiben |
| `characters_api` | Moral, Gesundheit und Zustand der Crew |
| `airplanes_api` | Gesundheit, Strukturintegrität, Treibstoff und Pilot eines Flugzeugs |
| `resources_api` | Ressourcen erzeugen und verderben lassen |
| `game_api` | Identität des Spielstands und ein Ordner für deine eigenen Dateien |
| `logger` | Debug-Zeilen in [`Player.log`](../start/troubleshooting.md#find-the-playerlog) schreiben |

Namen von Spielwerten kommen aus Imports:

| Import | Wofür |
|---|---|
| `from Blindflug.FlightMission import MissionEvent` | Namen der Missions-Handler, `MissionEvent.SEND_MISSION_EVENT` |
| `from Blindflug.MinorEvents import MinorEvent` | Event-Namen, `MinorEvent.MIDNIGHT` |
| `from Blindflug.MinorEvents import EventLogType` | das Aussehen einer Zeile im Ereignisprotokoll |
| `from Blindflug.GameResources import ResourceType` | Ressourcentypen, `ResourceType.FoodRations` |
| `from Blindflug.Game.Characters.Morale import MoraleCategory` | `MoraleCategory.Mood`, `.Confidence`, `.Energy` |
| `from Blindflug.Game.Characters.Morale import CharacterMoraleStateFlag` | vorübergehende Moralzustände |
| `from Blindflug.DayPhases import DayPhase` | `DayPhase.Work`, `.Leisure`, `.Sleep` |

Mod-Skripte laufen auf IronPython 3.4. Vermeide Syntax, die neuer als Python 3.6 ist (`:=`, `match`), und halte dich an die Module der Standardbibliothek, die die Beispiele verwenden (`json`, `os`). Mod-Skripte können einander über den Dateinamen importieren, wenn sie im selben `Missions/`-Ordner liegen.

## event_log

```python
event_log.Create(loc_key, parameters=None, event_log_type=EventLogType.Default)
```

Schreibt eine Zeile ins Ereignisprotokoll. `loc_key` ist ein Textschlüssel (siehe [Lokalisierung](localization.md)). `parameters` ist ein Dictionary, das `{[NAME]}`-Platzhalter in diesem Text füllt; alle Werte müssen Strings sein.

```python
event_log.Create("mymod/pilot_returned", {"PILOT": str(character_id)})
```

Charaktere, die im Text als `[character:<id>]` stehen, werden zu anklickbaren Namen und mit der Protokollzeile verknüpft.

`event_log_type` ändert, wie die Zeile aussieht: `EventLogType.Default`, `EventLogType.Warning`, `EventLogType.Error` oder `EventLogType.Success`.

## localization

```python
localization.SetTerm(language_code, key, text)
```

Definiert einen Text für eine Sprache oder ersetzt ihn. Ruf es auf der obersten Ebene deines Skripts auf, damit der Text existiert, sobald das Skript geladen ist. Die Seite [Lokalisierung](localization.md) erklärt Schlüssel, Sprachen, Platzhalter und was passiert, wenn deine Mod entfernt wird.

## missions_api

Missionszustand und Würfelwürfe. Jeder Aufruf nimmt die `mission_entity_id`, die dein Handler bekommen hat.

| Aufruf | Gibt zurück |
|---|---|
| `GetMissionId(id)` | die Id der Mission (ihr Dateiname), oder `None`, wenn die Mission nicht mehr existiert |
| `GetMissionAirplaneFormation(id)` | die Nummern der Flugzeuge, die der Mission zugewiesen sind |
| `GetEnemyCount(id)` | gemeldete feindliche Flugzeuge |
| `IsMissionSuccessful(id)` | ob die Mission erfolgreich war; aussagekräftig ab `set_mission_impact` |
| `GetNumberOfEventsSent(id)` | wie viele Schritte im Flug gefeuert haben, den aktuellen mitgezählt |
| `MakeAsPlannedRoll(id)` | **würfelt**, ob die Mission wie geplant läuft, speichert das Ergebnis und gibt es zurück |
| `GetAsPlannedRoll(id)` | liest diesen Wurf wieder aus |
| `MakeSkillRoll(id)` | **würfelt** die Fertigkeitsprobe der Staffel, speichert das Ergebnis und gibt es zurück; bei Erfolg sammelt die Crew Erfahrung |
| `GetSkillRoll(id)` | liest diesen Wurf wieder aus |
| `CreateMission(mission_id)` | setzt jetzt eine andere Mission auf die Kriegskarte, siehe unten |

**Einmal würfeln, danach nur lesen.** `Make...` würfelt; `Get...` liest. Mach den Wie-geplant-Wurf vor dem Fertigkeitswurf: Der Fertigkeitswurf entscheidet damit, gegen welchen der beiden Missions-Stats gewürfelt wird. Zweimal zu würfeln erzählt dem Spieler eine Geschichte und liefert einen anderen Ausgang.

`GetMissionId` gibt es, weil sich viele Missionen ein Skript teilen: Ein Handler kann am Dateinamen nicht erkennen, für welche Mission er läuft, also fragt er nach. Das gemeinsame Standard-Missionsskript baut damit seine Textschlüssel.

### Eine Mission erstellen { #creating-a-mission }

```python
missions_api.CreateMission("mymod_airfield_pursuit")
```

Setzt eine Mission sofort auf die Kriegskarte und überspringt die wöchentliche Ziehung. Gibt `True` zurück, wenn eine Mission erstellt wurde.

Die eigenen Voraussetzungen und die Karten-Tags der Zielmission werden trotzdem geprüft. Scheitert eins davon, wird nichts erstellt, es gibt `False` zurück, und eine Warnung mit dem Namen der Mission wird in [`Player.log`](../start/troubleshooting.md#find-the-playerlog) geschrieben. Bei einer unbekannten Id gibt es ebenfalls `False` zurück. Eine reine Skript-Mission, die noch nie erstellt wurde, hat noch nichts zu prüfen und ist immer erlaubt.

Ruf es aus `set_mission_impact` auf, wo der Ausgang bekannt ist. Aus `initialize_mission` wird es abgelehnt und [protokolliert](../start/troubleshooting.md#find-the-playerlog), weil dieser Handler mitten in der Erstellung einer Mission läuft.

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    if missions_api.IsMissionSuccessful(mission_entity_id):
        missions_api.CreateMission("mymod_pursuit")
    else:
        missions_api.CreateMission("mymod_regroup")
```

Wenn die Bedingung einfach "die vorherige Mission war erfolgreich" lautet, ist eine JSON-Voraussetzung besser: `"_requirementType": 3` mit `"<id>,success"`, ganz ohne Skript. Siehe [Ketten und Kampagnen](../missions/chains.md).

### Eine Mission aus einem Skript schreiben { #authoring-a-mission-from-a-script }

Diese Aufrufe schreiben, was sonst das JSON einer Mission festlegen würde. Eine reine Skript-Mission braucht sie, weil nichts anderes ihre Stats, ihren Ort oder ihre Ausgänge setzt. Ruf sie aus `initialize_mission` auf.

| Aufruf | Setzt |
|---|---|
| `SetMissionStat(id, skill, min, max)` | den Zielbereich einer Fertigkeit. `skill` ist `"Fight"`, `"Bomb"`, `"Recon"`, `"Transport"`, `"Maneuverability"` oder `"Stealthiness"`. Die erste Fertigkeit, die du setzt, wird gewürfelt, wenn die Mission wie geplant läuft, die zweite, wenn nicht. Setzt du dieselbe Fertigkeit erneut, wird ihr Bereich ersetzt. |
| `SetAsPlannedChance(id, chance)` | 0–100. Standard für eine reine Skript-Mission: 50. |
| `SetMissionLocation(id, location_id)` | platziert die Mission auf der Kriegskarte und berechnet Entfernung und Treibstoff. `location_id` ist die ID eines mitgelieferten Orts aus [Einsatzorte](../missions/locations.md) oder eines Orts, den ein aktivierter Mod hinzufügt, nie Koordinaten. |
| `SetMaxAirplaneSlots(id, slots)` | wie viele Flugzeuge zugewiesen werden dürfen, mindestens 1. Standard: 1. |
| `SetDifficulty(id, rating)` | die Sternebewertung, 1–3. Standard: 1. |
| `SetOutcome(id, index, is_success)` | ob Ausgang `index` (0–3, in der [vorgeschriebenen Reihenfolge](../missions/reference.md#the-two-rolls-and-the-outcome-index)) als Erfolg zählt |
| `AddOutcomeEffect(id, index, type, value)` | fügt Ausgang `index` einen Effekt hinzu. `type` ist `"CrewMood"`, `"CrewConfidence"`, `"CrewEnergy"`, `"Damage"`, `"BaseMood"`, `"BaseConfidence"`, `"BaseEnergy"` oder `"VictoryPoints"`. `value` ist eine ganze Zahl wie `"-40"` oder ein Bereich wie `"70-140"` für `Damage`. |
| `AddMissionRequirement(id, type, value)` | eine Sperre für das Erscheinen. `type` ist `"RunwayTier"`, `"EarliestAppearanceDay"`, `"LatestAppearanceDay"` oder `"CompletedMission"`. Sperren werden mit UND verknüpft. |
| `SetTags(id, tag, ...)` | zu welchen Karten die Mission gehört, wie `_tags` im JSON. Ersetzt, was vorher gesetzt war. |

Alle geben bei Erfolg `True` zurück und `False`, wenn die Mission, der Index oder ein Name unbekannt ist. Keiner wirft einen Fehler, prüf beim Entwickeln also den Rückgabewert.

Verwende `"MaxVictoryPoints"` nicht mit `AddOutcomeEffect`. Es wird angenommen, bringt die Mission aber beim Ende zum Absturz.

Eine reine Skript-Mission beginnt jede Erstellung mit geleerten Effekten und Voraussetzungen, `initialize_mission` kann sie also jedes Mal hinzufügen, ohne dass sich Duplikate stapeln. Bei einer Mission mit JSON-Datei ändern die Aufrufe dagegen die geladenen Dateidaten für den Rest der Sitzung: Effekte und Voraussetzungen, die du hinzufügst, sammeln sich mit jeder Kopie der Mission an. Stats und Chancen kannst du dort gern anpassen; Effekte und Sperren fügst du nur in reinen Skript-Missionen hinzu.

### Eine reine Skript-Mission sperren { #gating-a-script-only-mission }

Ohne Sperren erscheint eine reine Skript-Mission überall, sobald sie einmal erstellt wurde: Die wöchentliche Ziehung kennt jetzt ihre Daten, und ohne Voraussetzungen besteht sie jede Prüfung. Setz sie in `initialize_mission` zusammen mit dem Rest:

```python
@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    missions_api.AddMissionRequirement(mission_entity_id, "RunwayTier", "2")
    missions_api.AddMissionRequirement(mission_entity_id, "EarliestAppearanceDay", "14")
    missions_api.AddMissionRequirement(mission_entity_id, "LatestAppearanceDay", "40")
    missions_api.AddMissionRequirement(mission_entity_id, "CompletedMission", "mymod_convoy_spotted,success")
    missions_api.SetTags(mission_entity_id, "campaign_debden")
```

`CompletedMission` nimmt `"<missionId>"` oder `"<missionId>,success"`, `",failure"` bzw. `",cancelled"`, um einen bestimmten Ausgang zu verlangen. Tageszahlen zählen ab Beginn der Kampagne.

Tags funktionieren wie `_tags` im JSON: Die Mission kann nur auf Karten erscheinen, die einen ihrer Tags teilen. Ohne gesetzte Tags gilt `"default"`, das jede eingebaute Karte unterstützt. Das ist richtig für eine Mission, die überall erscheinen soll, und falsch für eine, die zu einer einzigen Kampagne gehört. Siehe [Karten-Tags](../missions/reference.md#map-tags).

## characters_api

Charakter-Ids sind Strings, so wie sie in Event-Argumenten oder von `airplanes_api.GetPilot` ankommen. Mehrere Aufrufe gibt es in zwei Formen: eine für alle Charaktere, eine für einen einzelnen.

| Aufruf | Wirkung |
|---|---|
| `GetMorale(character_id, category)` | einen Moralwert lesen |
| `SetMorale(category, value)` | für **alle** setzen |
| `SetMorale(character_id, category, value)` | für einen Charakter setzen |
| `ModifyMorale(category, delta)` | für **alle** ändern |
| `ModifyMorale(character_id, category, delta)` | für einen Charakter ändern |
| `TriggerEffect(character_id, category)` | löst die Belastungsgrenzen-Reaktion dieses Charakters für diese Kategorie aus, als wäre die Moral auf dem Tiefpunkt; gibt zurück, ob der Charakter gefunden wurde |
| `SetTemporaryMoraleState(character_id, state, duration)` | versetzt einen Charakter in einen vorübergehenden Zustand, siehe unten |
| `ModifyHealth(character_id, delta, notify=True)` | Gesundheit ändern; mit `notify=True` bekommt der Spieler die übliche Gesundheitsmeldung |
| `HealthEventsBlocked()` | `True`, solange das Spiel eine junge Basis vor Gesundheitsereignissen schützt, siehe unten |
| `SetFire(character_id, fires)` | einen Charakter in Brand setzen, mit `fires` Feuern um ihn herum |
| `GetPilotMissionCount(character_id)` | geflogene Missionen |
| `GetPilotSuccessfulMissionCount(character_id)` | gewonnene Missionen |
| `DestroyCarriedResource(character_id)` | zerstört, was er trägt; gibt zurück, ob er etwas getragen hat |
| `DropCarriedResource(character_id)` | lässt fallen, was er trägt; gibt zurück, ob er etwas getragen hat |
| `GetVoxelObjectId(character_id)` | die Nummer des Objekts des Charakters in der Welt, für `resources_api.SpawnNextTo`; 0, wenn nicht gefunden |

Moral reicht von -100 bis 100. `category` ist `MoraleCategory.Mood`, `MoraleCategory.Confidence` oder `MoraleCategory.Energy`.

`SetTemporaryMoraleState` nimmt ein `CharacterMoraleStateFlag`: `Happy`, `Sad`, `Injured`, `Sick`, `Exhausted`, `Fearful`, `Angry`, `Panic`, `Collapse`, `Rage` oder `HeavilyInjured`, und eine Dauer.

`HealthEventsBlocked()` gibt in den ersten Tagen einer Kampagne `True` zurück, während ein Mitglied der Bodencrew schon verletzt ist, damit eine junge Basis nicht doppelt getroffen wird. Ein Skript, das jemanden verletzt, sollte das zuerst prüfen und `return False` machen, wenn es gesetzt ist:

```python
@event_handler(MinorEvent.TASK_COMPLETED, chance=0.01, max_occurrences=1)
def twisted_ankle(character_id, task_type):
    if characters_api.HealthEventsBlocked():
        return False

    characters_api.ModifyHealth(character_id, -10)
    event_log.Create("mymod/twisted_ankle", {"CHARACTER": str(character_id)})
```

## airplanes_api

Flugzeuge werden über eine Nummer identifiziert: die Werte, die `missions_api.GetMissionAirplaneFormation` zurückgibt, und die `airplaneEntityId`-Argumente von Events.

| Aufruf | Gibt zurück oder tut |
|---|---|
| `GetPilot(airplane_id)` | die Charakter-Id des ersten Crewmitglieds |
| `GetAirplaneHealth(airplane_id)` | Gesundheit als Anteil, 0.0–1.0 |
| `SetAirplaneHealth(airplane_id, value)` | Gesundheit in Punkten setzen (ganze Zahl), begrenzt auf das Maximum des Flugzeugs |
| `AddAirplaneHealth(airplane_id, value)` | Gesundheit um so viele Punkte ändern; negative Werte beschädigen |
| `GetAirplaneIntegrity(airplane_id)` | Strukturintegrität als Anteil, 0.0–1.0 |
| `GetAirplaneParkingLot(airplane_id)` | die Nummer des Parkplatzes des Flugzeugs; wirft einen Fehler, wenn es keinen hat |
| `ReduceAirplaneFuel(airplane_id, fuel)` | Treibstoff verbrauchen; ein Flugzeug, das leer läuft, gilt als vermisst |

Für Schaden durch eine Mission nimm lieber den Ausgangseffekt `Damage` im JSON. Der kümmert sich auch um Verletzungen der Crew.

```python
@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
    for airplane_id in missions_api.GetMissionAirplaneFormation(mission_entity_id):
        pilot = airplanes_api.GetPilot(airplane_id)
        characters_api.ModifyMorale(pilot, MoraleCategory.Energy, -10)
```

## resources_api

| Aufruf | Wirkung |
|---|---|
| `SpawnNextTo(voxel_object_id, resource_type, amount)` | legt einen Ressourcenstapel auf den nächsten freien Platz neben einem Objekt |
| `SpoilPile(resource_type)` | lässt einen Stapel dieser Ressource verderben |

Beide geben `True` oder `False` zurück. `SpoilPile` schlägt fehl, wenn es nichts zu verderben gibt, ein natürlicher Moment für `return False` in einem Event-Handler. Eine `voxel_object_id` für einen Charakter bekommst du mit `characters_api.GetVoxelObjectId`; Hunde-Events liefern sie direkt.

```python
from Blindflug.GameResources import ResourceType

resources_api.SpawnNextTo(characters_api.GetVoxelObjectId(character_id), ResourceType.FoodRations, 2)
```

## game_api

| Aufruf | Gibt zurück |
|---|---|
| `GetAirBaseGuid()` | eine eindeutige Id für den aktuellen Spielstand |
| `GetScriptDataPath(id)` | einen Ordner, in dem dein Skript lesen und schreiben darf |

`GetScriptDataPath` legt bei Bedarf den Ordner `Scripts/<id>` im Spieldatenordner an und gibt seinen Pfad zurück. Das ist der vorgesehene Weg, eigene Daten über Sitzungen hinweg zu behalten. `id` darf nur Buchstaben, Ziffern, `_`, `-` und `.` enthalten, höchstens 64 Zeichen; alles andere wirft einen Fehler.

Zwei Dinge solltest du wissen:

- Der Ordner gehört zur **Id**, nicht zu einer Mission. Mehrere Missionen, die sich Zustand teilen wollen, müssen dieselbe Id verwenden.
- Er ist **nicht pro Spielstand**. Nimm `GetAirBaseGuid()` in deinen Dateinamen auf, damit sich getrennte Spielstände nicht gegenseitig überschreiben.

```python
import os

def _path():
    return os.path.join(
        game_api.GetScriptDataPath("mymod_campaign"),
        "campaign_{}.json".format(game_api.GetAirBaseGuid())
    )
```

Das macht eine Kampagne erst möglich: Eine Mission kann fragen, wie viele Angriffe verloren gingen, wer den ersten gewonnen hat oder was der Spieler vor zwei Missionen gewählt hat. [Ketten und Kampagnen](../missions/chains.md#from-a-chain-to-a-campaign) zeigt das vollständige Muster und die drei Arten, es falsch zu machen.

## logger

Schreibt in [`Player.log`](../start/troubleshooting.md#find-the-playerlog).

```python
logger.Log("mymod: campaign state loaded")
```

Nimm `event_log` für alles, was der Spieler sehen soll; `logger` ist für dich, beim Debuggen. Setz deinen Mod-Namen vor deine Zeilen, damit du nach ihnen suchen kannst.

## Was nicht verfügbar ist { #what-is-not-available }

- `eval` ist aus den eingebauten Funktionen der Skripte entfernt.
- Die Handler `get_mission_icon` und `calculate_*_modifiers` werden nie aufgerufen, es gibt also keinen Weg, aus einem Skript Erfolgsmodifikatoren hinzuzufügen. Ändere stattdessen Stats und Chancen mit den Schreib-Aufrufen oben.
