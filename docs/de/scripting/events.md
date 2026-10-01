# Events

Events (das Spiel nennt sie **Minor Events**) sind der zweite Weg, wie sich ein Skript ins Spiel einklinken kann. Mit dem Besitzen einer Mission haben sie nichts zu tun: Sie feuern aus dem Leben auf der Basis (Bauarbeiten, Crew, Tageszeit, Ressourcen, Flugzeuge, die kommen und gehen), und jedes Skript kann auf sie hören.

Damit sind sie das Werkzeug für kleine Geschichten: Jemandes Patrouille kommt zerschossen zurück, ein Crewmitglied hat eine schlechte Nacht, um Mitternacht machen sich Mäuse über die Rationen her. Das Beispiel `event_script` reagiert auf Missionen, die es nicht selbst geschrieben hat; siehe [Beispiele](../examples.md).

## Ein vollständiges Event-Skript { #a-complete-event-script }

Speichere das als `Mods/my_first_mod/Missions/mymod_quiet_night.py`. Kein JSON, keine Missions-Id, sonst wird nichts gebraucht:

```python
from Blindflug.MinorEvents import MinorEvent

localization.SetTerm("en", "mymod/quiet_night",
                     "A quiet night. The duty officer reports nothing but owls.")


@event_handler(MinorEvent.MIDNIGHT, chance=0.02, max_occurrences=2)
def quiet_night(year, month, day):
    event_log.Create("mymod/quiet_night")
```

Event-Skripte liegen wie Missionsskripte im `Missions/`-Ordner der Mod. Das ist der einzige Skriptordner einer Mod; ein Skript in einem anderen Ordner läuft nie.

## Der Decorator { #the-decorator }

```python
@event_handler(event_name, chance=1.0, max_occurrences=-1)
def handler(argument1, argument2):
    ...
```

- `event_name`: welches Event, meistens geschrieben als `MinorEvent.SOME_NAME` (importiert mit `from Blindflug.MinorEvents import MinorEvent`). Der einfache String, etwa `"midnight"`, funktioniert auch.
- `chance`: die Wahrscheinlichkeit, dass der Handler läuft, wenn das Event feuert, von 0.0 bis 1.0. Standard 1.0 (immer). Das Spiel rechnet zu jedem Handler noch eine globale Grundchance dazu; im normalen Spiel ist sie `0`, es zählt also dein Wert (nur ein Cheat in Entwickler-Builds ändert sie).
- `max_occurrences`: wie oft der Handler in einem Spielstand laufen darf. Der Zähler wird im Spielstand gespeichert, unter dem Namen `<module>.<function>` des Handlers - benennst du eins davon um, fängt er von vorne an. Ein negativer Wert heißt unbegrenzt, das ist der Standard (`-1`); `0` heißt, der Handler läuft nie. Der Zufallswurf für `chance` und die Prüfung des Limits passieren beide, bevor der Handler aufgerufen wird.

**Die Rückgabe von `False` zählt nicht** gegen `max_occurrences`. Nutze das, um eine Bedingung zu prüfen und auszusteigen, ohne das Kontingent zu verbrauchen. Keine Rückgabe, `True` oder jeder andere Wert zählt.

```python
@event_handler(MinorEvent.MIDNIGHT, chance=0.05, max_occurrences=2)
def midnight_mice(year, month, day):
    if resources_api.SpoilPile(ResourceType.FoodRations):
        event_log.Create("mymod/midnight_mice")
    else:
        return False    # nothing to spoil: try again another night
```

Der Zähler wird pro Handler unter dem Namen `<file name>.<function name>` gespeichert. Benennst du die Datei oder die Funktion um, beginnt die Zählung von vorn. Zwei Handler mit demselben Funktionsnamen in derselben Datei teilen sich einen Zähler.

Mehrere Skripte dürfen auf dasselbe Event hören. Für jeden Handler wird einzeln gewürfelt und gezählt.

## Argumente { #arguments }

Das Spiel übergibt Argumente **nach Position**, in der unten aufgeführten Reihenfolge. Die Namen sind nur Beschreibungen: Nenn deine Parameter, wie du willst, aber nimm die richtige Anzahl entgegen, sonst schlägt der Aufruf fehl.

- Ids von Charakteren, Gebäuden, Werkbänken und so weiter kommen als Strings an.
- Ids von Flugzeugen und Hunden (`...EntityId`, `voxelObjectId`) kommen als Zahlen an. Das sind die Zahlen, die `airplanes_api` und `resources_api` erwarten.
- Werte wie ein Ressourcentyp oder eine Tagesphase kommen als Spielwerte an, die du direkt vergleichen kannst: `if resource == ResourceType.MilitaryConstruction:`. Mit `str(value)` machst du Text daraus.
- Charakter-Argumente sind Charakter-Ids (Strings), Ressourcen-Argumente sind `ResourceType`-Werte und Aufgaben-Argumente (der `taskType` von `task_started` und `task_completed`) sind `Task`-Werte (`from Blindflug.Tasks import Task`).

Nützliche Imports zum Vergleichen:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Game.Characters.Morale import MoraleCategory
from Blindflug.DayPhases import DayPhase
from Blindflug.Tasks import Task
```

### Missionen und Flüge { #missions-and-flights }

| Event | Argumente |
|---|---|
| `mission_started` | `locationName` |
| `mission_success` | `locationName` |
| `mission_failed` | `locationName` |
| `airplane_on_mission_succeed` | `airplaneId, airplaneEntityId, missionId, skillType, isGoingAsPlanned, locationName, successEstimate` |
| `airplane_on_mission_failed` | dieselben sieben |
| `plane_takeoff` | `airplaneEntityId, characterId` |
| `plane_landing` | `airplaneEntityId, characterId` |
| `airplane_took_part_in_scramble` | `airplaneId, airplaneEntityId` |
| `airplane_scramble_fly_to_safety` | `airplaneId, airplaneEntityId` |
| `airplane_scramble_airplane_destroyed` | `airplaneId` |
| `victory_points_added` | keine |

Das Paar mit sieben Argumenten ist der nützlichste Haken im ganzen System: Er feuert einmal für jedes Flugzeug, das von **irgendeiner** Mission zurückkommt, auch von solchen, die du nicht geschrieben hast. `airplaneId` ist der Typname des Flugzeugs, `airplaneEntityId` die Nummer für `airplanes_api`, `skillType` die gewürfelte Fertigkeit als Text (`"Fight"`), `isGoingAsPlanned` ist `True` oder `False`, und `successEstimate` die Erfolgschance in Prozent, die dem Spieler angezeigt wurde (0, wenn keine).

`plane_takeoff` und `plane_landing` feuern einmal pro Crewmitglied an Bord, jedes Mal mit der Id dieser Person.

`mission_success` und `mission_failed` feuern für Missionen, deren Ausgang aus Ausgangsdaten kommt (jede Mission mit JSON-Datei). Eine reine Skript-Mission, die ihr Ergebnis mit `get_mission_result` entscheidet, löst sie nicht aus.

### Zeit { #time }

| Event | Argumente |
|---|---|
| `midnight` | `year, month, day` |
| `midday` | `year, month, day` |
| `day_phase_change` | `previousPhase, newPhase` (Tagesphasen: `DayPhase.Work`, `DayPhase.Leisure`, `DayPhase.Sleep`) |

### Crew

| Event | Argumente |
|---|---|
| `chat_started` | `characterId, targetCharacterId` |
| `chat_finished` | `characterId, targetCharacterId` |
| `training_started` | `characterId, trainingObjectId` |
| `training_finished` | `characterId, trainingObjectId` |
| `assigned_to_equipment` | `characterId, propId` |
| `task_started` | `characterId, taskType` |
| `task_completed` | `characterId, taskType` |

### Bau und Wirtschaft { #construction-and-economy }

| Event | Argumente |
|---|---|
| `building_started` | `characterId, buildingId` |
| `building_finished` | `characterId, buildingId` |
| `building_type_finished` | `characterId, buildType` |
| `deconstruction_finished` | `characterId, buildingId` (oder die Id des Geländeobjekts, das geräumt wurde) |
| `project_started` | `characterId, workbenchId, projectId` |
| `project_finished` | `characterId, workbenchId, projectId` |
| `resource_picked_up` | `characterId, resourceType` |
| `resource_gained` | `resourceType` |
| `resouce_consumed` | `characterId, resourceType` |
| `harvesting_started` | `characterId, harvestableId, resourceType` |
| `harvesting_finished` | `characterId, harvestableId, resourceType` |
| `shipment_received` | eine variable Anzahl von Lieferungs-Ids, je ein Argument |
| `function_area_placed` | `functionAreaType` |
| `storage_resource_enabled` | `resourceType` |

Hinweise:

- `resouce_consumed` wird mit dem fehlenden `r` geschrieben. Das ist der echte Event-Name; `MinorEvent.RESOURCE_CONSUMED` liefert dir den richtigen String.
- `resource_gained` trägt eine Menge, die Quests auslesen, aber ein Skript bekommt nur den Ressourcentyp.
- `harvesting_started` und `harvesting_finished` feuern nur für Ressourcenbehälter, nicht für Kisten.
- `building_type_finished` feuert nicht für Gebäude ohne Typ.
- Für `shipment_received` schreibst du den Handler als `def on_shipment(*shipment_ids):`, damit er beliebig viele Argumente annimmt.

### Quests

| Event | Argumente |
|---|---|
| `sub_quest_completed` | `subQuestName` (der Textschlüssel des Titels der Unterquest) |
| `quest_dismissed` | keine |

### Hunde { #dogs }

| Event | Argumente |
|---|---|
| `dog_walk_started` | `voxelObjectId` |
| `dog_walk_finished` | `voxelObjectId` |
| `dog_sleep` | `voxelObjectId` |
| `dog_sniff_wait` | `voxelObjectId` |

## Events nur im Tutorial { #tutorial-only-events }

25 Events feuern nur, solange das Tutorial eingeschaltet ist. In einem normalen Spiel erreichen sie nie ein Skript, für Inhalts-Mods taugen sie also nichts. Sie stehen hier, damit du dich nicht wunderst, warum dein Handler stumm bleibt:

| Event | Argumente |
|---|---|
| `camera_moved` | keine |
| `camera_zoomed` | keine |
| `camera_rotated` | keine |
| `character_selected` | `characterId` |
| `task_created` | `taskType` (als Text), `targetId` |
| `tooltip_shown` | `id` |
| `preview_created` | `buildingId` |
| `building_placed` | `buildingId` |
| `state_entered` | `stateName, argument` |
| `time_scale_changed` | `timeScale` (als Text) |
| `window_opened` | `windowId` |
| `character_job_assigned` | `jobName` |
| `day_phase_ended` | `endedPhase` |
| `plane_ordered` | `airplaneId` |
| `plane_selected` | `airplaneId` |
| `plane_assigned_to_mission` | `airplaneId` |
| `shipment_item_added` | `shipmentId` |
| `scramble_started` | keine |
| `attack_finished` | keine |
| `storage_resource_disabled` | `resourceType` |
| `button_clicked` | `id` |
| `plane_back_from_mission` | `airplaneEntityId` |
| `hour_changed` | `hour` (0–23) |
| `workbench_selected` | `workbenchId` |
| `project_planned` | `projectId, repetitionCount` (als Text) |

## Ins Ereignisprotokoll schreiben { #writing-to-the-event-log }

```python
event_log.Create("mymod/pilot_tired", {"PILOT": str(character_id)})
```

Das erste Argument ist ein Textschlüssel, das zweite füllt `{[NAME]}`-Platzhalter in diesem Text. Ein Charakter, der im Text als `[character:{[PILOT]}]` steht, wird zu einem anklickbaren Namen. Wie du den Text definierst, und die anderen Inline-Tags, steht auf der Seite [Lokalisierung](localization.md). Alles zu `event_log` steht auf der Seite [API](api.md#event_log).
