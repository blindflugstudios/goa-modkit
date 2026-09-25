# Scripting

Das Spiel führt Python-Skripte für Zufallsereignisse und Missionslogik aus, und dein Mod kann eigene hinzufügen. Ein Skript kann auf Dinge reagieren, die auf dem Stützpunkt passieren - ein Wechsel der Tagesphase, ein fertiges Gebäude, eine zurückkehrende Mission - und das Spiel daraufhin verändern: die Stimmung der Crew heben, einen Eintrag ins Ereignisprotokoll schreiben, eine Mission auf die Karte setzen.

Skripte laufen mit **IronPython 3.4**, einer Version von Python 3.4, die im Spiel läuft. Alltägliches Python funktioniert, auch f-Strings (die Skripte des Spiels nutzen sie). Vermeide Syntax, die nach Python 3.6 kam - keinen Walross-Operator `:=`, kein `match`, keine rein positionellen `/`-Parameter. Pakete für normales Python mit kompilierten Teilen (numpy und Ähnliches) funktionieren nicht. Die Standardbibliothek, die mit dem Spiel kommt, liegt im Ordner `Scripts/Lib`; nicht jedes Modul ist dabei, halte dich also an das, was die Beispiele verwenden.

| Seite | Inhalt |
|---|---|
| [Events](events.md) | jedes Event, das ein Skript abonnieren kann, mit seinen Argumenten |
| [API](api.md) | die Objekte, mit denen ein Skript mit dem Spiel spricht (`characters_api`, `missions_api`, ...) |
| [Lokalisierung](localization.md) | Texte mit `localization.SetTerm` hinzufügen und ändern |
| [Missionen](../missions/index.md) | Missionsskripte und ihre Handler |
| [Python-Mods und Sicherheit](../basics/security.md) | was Skripte in einem Mod können und was du vor der Installation prüfen solltest |

## Wo Skripte liegen { #where-scripts-live }

**Deine eigenen Skripte gehören in einen Mod**, in dessen Ordner `Missions/`:

```text
Mods/
  my_mod/
    Missions/
      morale_boost.py
```

Die Skripte des Spiels liegen im Installationsordner unter `GroundOfAces_Data/StreamingAssets/Scripts` (auf macOS: `GroundOfAces.app/Contents/Resources/Data/StreamingAssets/Scripts`). Das sind mitgelieferte Inhalte, die du nur lesen solltest - lies sie für Ideen, aber ändere sie nicht, denn ein Spiel-Update überschreibt sie. Die mitgelieferten Ordner sind:

| Ordner | Inhalt |
|---|---|
| `Default` | die Zufallsereignisse (`random_events.py`, `random_health_events.py`) |
| `Mission` | die Missionsskripte, einschließlich des gemeinsamen `default_mission.py` |
| `Lib` | die Python-Standardbibliothek - kein Skriptordner |

## Wie Skripte geladen werden { #how-scripts-are-loaded }

Skripte werden bei jedem Laden eines Levels geladen, in dieser Reihenfolge:

1. der Ordner `Scripts/Default` des Spiels
2. die Event-Skripte des Supporter Packs, falls du es besitzt
3. der Ordner `Scripts/Mission` des Spiels
4. die Missionsskripte des Supporter Packs
5. der Ordner `Missions/` jedes aktivierten Mods, in Mod-Ladereihenfolge (siehe [Welcher Mod gewinnt](../basics/mods.md#which-mod-wins))
6. dein eigener Ordner `Missions` neben `Mods` (unter Windows `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Missions\`; die anderen Plattformen stehen unter [Missionen](../missions/index.md#where-missions-come-from))

Regeln, die du kennen solltest:

- Nur `.py`-Dateien direkt in einem Ordner werden gelesen - Unterordner werden ignoriert.
- Jede Datei wird zu einem Python-Modul, das nach der Datei benannt ist.
- Eine Datei mit einem **Syntaxfehler** wird übersprungen, der Fehler landet im Log des Spiels, und die anderen Dateien laden trotzdem.
- Jeder **andere Fehler auf oberster Ebene** einer Datei (ein fehlschlagender Import, eine Exception beim Ausführen der Datei) wird nicht abgefangen und kann verhindern, dass die nachfolgenden Ordner geladen werden - auch die Skripte anderer Mods. Pack riskanten Code auf oberster Ebene in `try`/`except`.

Jeder Handler wird über `<module>.<function>` erkannt, also Dateiname plus Funktionsname. Definieren zwei Dateien einen Handler mit demselben Modul- und Funktionsnamen, ersetzt der **später** geladene den früheren. So kann ein Mod eines der Zufallsereignisse des Spiels überschreiben: Kopiere `random_events.py` in den Ordner `Missions/` deines Mods und ändere die Funktionen, die du anders haben willst.

### Deine Änderungen sehen { #seeing-your-changes }

Bearbeite dein Skript, geh zurück ins Hauptmenü und lade erneut ein Level - einen Spielstand zu laden reicht. Ist der Mod-Ordner selbst neu, drück zuerst **Refresh** im Mods-Fenster (siehe [So funktionieren Mods](../basics/mods.md#seeing-your-changes)). Mehr dazu unter [Testen und Neuladen](../basics/testing.md).

## Skripte in einem Mod { #scripts-in-a-mod }

Jede `.py`-Datei im Ordner `Missions/` eines Mods ist ein vollwertiges Event-Skript, nicht nur Missionslogik: Sie kann jedes Event abonnieren, genau wie das `random_events.py` des Spiels. Die Skripte jedes aktivierten Mods werden geladen. Wer die Skripte eines Mods nicht laufen lassen will, deaktiviert den Mod im Mods-Fenster; der Schalter **Scripting** pro Mod ändert daran derzeit nichts. Siehe [Python-Mods und Sicherheit](../basics/security.md).

## Missionsskripte { #mission-scripts }

Missionsskripte sind eine besondere Art von Skript, die entscheidet, wie eine Mission abläuft. Sie werden unter [Missionen](../missions/index.md) behandelt, zusammen mit dem Mission Editor im Spiel und der JSON-Datei hinter jeder Mission. Missions-Handler nutzen denselben `event_handler`-Decorator wie die Skripte auf dieser Seite, mit den Konstanten aus `MissionEvent`:

```python
from Blindflug.FlightMission import MissionEvent

@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return "mymod_coastal_patrol"
```

Die vollständige Liste der Missions-Handler steht unter [Referenz](../missions/reference.md).

## Dein erstes Event-Skript { #your-first-event-script }

Schreiben wir ein Skript, das bei jedem Wechsel der Tagesphase läuft und die Stimmung der ganzen Crew um 10 hebt.

Dafür abonnieren wir das Event `DAY_PHASE_CHANGE`. Das ist nur eines der Events, die du nutzen kannst - die vollständige Liste steht unter [Events](events.md).

Leg einen Mod-Ordner an (siehe [So funktionieren Mods](../basics/mods.md)), gib ihm einen Unterordner `Missions/` und erstelle darin eine neue Datei namens `morale_boost.py`. Füge folgenden Code ein:

```python
# Import MinorEvent to have access to built-in event names
from Blindflug.MinorEvents import MinorEvent
# Import MoraleCategory to have access to morale type constants
from Blindflug.Game.Characters.Morale import MoraleCategory

# Define a localization term that can be displayed in the game.
# This term contains a single placeholder value named "MOOD".
# Since this is outside any function, it runs when the script is loaded.
localization.SetTerm("en", "mymod/morale_up", f"New day phase, [morale:{MoraleCategory.Mood}] improves by {{[MOOD]}}!")

# Use a decorator to mark the function `on_day_phase` as an event handler.
# The function is called when the event happens.
# The arguments are specific to the day phase change event:
# the previous and the current phase.
@event_handler(MinorEvent.DAY_PHASE_CHANGE)
def on_day_phase(previous_phase, current_phase):

    # The amount of mood to add
    mood_boost = 10

    # Change the mood of all characters
    characters_api.ModifyMorale(MoraleCategory.Mood, mood_boost)

    # Create an event log entry, using the localization term defined above.
    # The "MOOD" placeholder is replaced with the value of str(mood_boost).
    event_log.Create("mymod/morale_up", {"MOOD": str(mood_boost)})
```

Starte jetzt das Spiel (oder drück **Refresh** im Mods-Fenster, falls das Spiel schon lief, als du den Ordner angelegt hast), lade ein Level und warte, bis die Tagesphase wechselt. Du solltest die Nachricht im Ereignisprotokoll sehen, und die Stimmung der ganzen Crew sollte um 10 steigen. Glückwunsch - du hast dein erstes Skript geschrieben!

!!! note
    `DAY_PHASE_CHANGE` wird weder für die allererste Phase eines Spiels ausgelöst noch während eines laufenden Luftalarms.

!!! note "Was ist `@event_handler`?"
    `event_handler` ist ein *Decorator*, erkennbar am `@` davor. Ein Decorator verändert die Funktion, die direkt danach steht - hier registriert er die Funktion, damit das Spiel sie aufruft, wenn das Event eintritt. Mehr musst du nicht verstehen, um ihn zu benutzen.

!!! tip "Warum die doppelten geschweiften Klammern?"
    In einem f-String ersetzt Python `{MoraleCategory.Mood}` sofort, während `{{` und `}}` einfache Klammern ergeben. Der Term enthält am Ende also `{[MOOD]}`, den Platzhalter, den das Spiel später ausfüllt.

### Mehr Logik hinzufügen { #adding-more-logic }

Alle auf dem Stützpunkt mögen ihre Arbeit, aber eine wohlverdiente Pause genießen sie wahrscheinlich noch mehr. Lassen wir den Effekt davon abhängen, welche Tagesphase gerade begonnen hat.

Importiere zuerst `DayPhase`, um Zugriff auf die Konstanten der Tagesphasen zu haben:

```python
from Blindflug.DayPhases import DayPhase
```

Ändere in der Funktion `on_day_phase` den Wert, der `mood_boost` zugewiesen wird:

```python
    mood_boost = 10 if current_phase == DayPhase.Leisure else 5 if current_phase == DayPhase.Sleep else 0
```

Ist die Tagesphase weder Freizeit noch Schlaf, wollen wir nichts tun, also fügen wir ein frühes Return ein:

```python
    if mood_boost == 0:
        return False
```

Der Rückgabewert ist wichtig: `False` bedeutet, dass dieser Durchlauf nicht zur maximalen Anzahl an Durchläufen zählt (siehe unten). Gibst du nichts oder `True` zurück, zählt er ganz normal.

### Chance und maximale Anzahl an Durchläufen { #chance-and-maximum-number-of-runs }

Ohne weitere Einstellungen läuft der Handler jedes Mal, wenn das Event eintritt, so oft es eintritt. Zum Testen ist das super, im echten Einsatz ist etwas Zufall aber eine gute Idee. So bekommt die Funktion eine Chance von 10 %, beim Wechsel der Tagesphase zu laufen, höchstens 4-mal pro Spiel:

```python
@event_handler(MinorEvent.DAY_PHASE_CHANGE, chance=0.1, max_occurrences=4)
def on_day_phase(previous_phase, current_phase):
    ...
```

Nur die Decorator-Zeile ändert sich; der Rumpf der Funktion (hier als `...` dargestellt) bleibt, wie er ist.

### Übersetzungen hinzufügen { #adding-translations }

Soll dein Skript mehrere Sprachen unterstützen, registriere den Term für jede davon. Hier ist die Nachricht auf Polnisch:

```python
localization.SetTerm("pl", "mymod/morale_up", f"Nowa faza dnia, [morale:{MoraleCategory.Mood}] wzrasta o {{[MOOD]}}!")
```

Stell die Spielsprache zwischen Englisch und Polnisch um, und die Nachricht im Ereignisprotokoll folgt. Der Sprachcode muss einer sein, den das Spiel in seinen Optionen anbietet (`pl` gehört dazu).

!!! note
    Eine Sprache, die du auslässt, zeigt den Text einer Sprache, die du registriert hast - registriere also immer `en`. Ein Schlüssel, der in gar keiner Sprache registriert ist, erscheint im Ereignisprotokoll als roher Schlüssel.

!!! warning
    `SetTerm` auf einen Schlüssel, den das Spiel schon mitbringt - einen Gebäudenamen, eine Menübeschriftung - **ersetzt den eigenen Text des Spiels** für diese Sprache. Das ist ein nützlicher Weg, das Spiel umzutexten, und ein leichter Weg, es versehentlich kaputt zu machen. Stell deinen eigenen Schlüsseln den Namen deines Mods voran, wie in `mymod/morale_up`. Mehr unter [Lokalisierung](localization.md).

### Das fertige Skript { #the-finished-script }

Nach allen Änderungen oben sieht das Skript so aus:

```python
from Blindflug.MinorEvents import MinorEvent
from Blindflug.Game.Characters.Morale import MoraleCategory
from Blindflug.DayPhases import DayPhase

localization.SetTerm("en", "mymod/morale_up", f"New day phase, [morale:{MoraleCategory.Mood}] improves by {{[MOOD]}}!")
localization.SetTerm("pl", "mymod/morale_up", f"Nowa faza dnia, [morale:{MoraleCategory.Mood}] wzrasta o {{[MOOD]}}!")

@event_handler(MinorEvent.DAY_PHASE_CHANGE, chance=0.1, max_occurrences=4)
def on_day_phase(previous_phase, current_phase):

    mood_boost = 10 if current_phase == DayPhase.Leisure else 5 if current_phase == DayPhase.Sleep else 0

    if mood_boost == 0:
        return False

    characters_api.ModifyMorale(MoraleCategory.Mood, mood_boost)

    event_log.Create("mymod/morale_up", {"MOOD": str(mood_boost)})
```

### Nächste Schritte { #next-steps }

Ein guter Weg, ein Gefühl dafür zu bekommen, was möglich ist, ist das Lesen der Skripte des Spiels: `random_events.py` und `random_health_events.py` in `Scripts/Default` (das zweite zeigt Ereignisprotokoll-Typen, Icons und die Gesundheits-API) und `default_mission.py` in `Scripts/Mission`. Auf der Seite [Beispiele](../examples.md) findest du vollständige Mods zum Kopieren, darunter ein Event-Skript.

## Globale Variablen { #global-variables }

Jedes Skript kann ein paar fertige Objekte nutzen, ohne etwas zu importieren, um mit dem Spiel zu sprechen:

| Name | Wofür es da ist |
|---|---|
| `logger` | der Logger des Spiels; `logger.Log("text")` schreibt eine Zeile in die Logdatei des Spiels |
| `event_log` | Einträge im Ereignisprotokoll erstellen |
| `localization` | Lokalisierungs-Terme hinzufügen oder ändern |
| `resources_api` | einen Ressourcenhaufen neben einem Objekt erzeugen oder einen Haufen verderben lassen |
| `characters_api` | Crew-Zustand lesen und ändern: Gesundheit, Moral, getragene Ressourcen, Feuer, Belastungsgrenzen-Effekte |
| `missions_api` | Missionen verwalten |
| `airplanes_api` | Flugzeuge verwalten |
| `game_api` | allgemeine Spieldaten abrufen |

Jede Funktion dieser Objekte ist unter [API](api.md) beschrieben.

Diese Namen stehen überall zur Verfügung, sie funktionieren also auch in jedem Hilfsmodul, das dein Skript importiert. Auch die Typen des Spiels stehen Python zur Verfügung, jedes öffentliche Enum und jeder öffentliche Typ lässt sich also mit vollem Namen importieren, zum Beispiel:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Tasks import Task
from Blindflug.Game.Characters.Morale import MoraleCategory
```

`eval` ist entfernt und kann nicht benutzt werden.

### Einträge im Ereignisprotokoll { #event-log-entries }

`event_log.Create(term, parameters=None, event_log_type=EventLogType.Default)` nimmt ein optionales drittes Argument, das den Eintrag einfärbt: `from Blindflug.MinorEvents import EventLogType` liefert `Default`, `Warning`, `Error` und `Success`. Der Parameterschlüssel `"icon"` ist reserviert: Sein Wert benennt ein Bild aus dem allgemeinen Icon-Satz des Spiels (zum Beispiel `"ui_health"`), das neben dem Eintrag erscheint. `random_health_events.py` nutzt beides:

```python
from Blindflug.MinorEvents import EventLogType

event_log.Create("random_events/" + id, {"CHARACTER": character, "icon": "ui_health"}, EventLogType.Warning)
```

## Events

Die Events, die ein Skript abonnieren kann, und die Argumente, die jedes davon an deine Funktion übergibt, stehen unter [Events](events.md). Charakter-Argumente sind Charakter-Ids (Text), Ressourcen-Argumente sind `ResourceType`-Werte und Aufgaben-Argumente sind `Task`-Werte (`from Blindflug.Tasks import Task`). Manche Events werden ohne Argumente ausgelöst; ein paar gibt es nur für die Oberfläche und das Tutorial des Spiels.

## Event-Handler-Funktionen { #event-handler-functions }

Event-Handler sind normale Python-Funktionen, markiert mit dem Decorator `event_handler`:

```python
@event_handler(event_name, chance=1.0, max_occurrences=-1)
def handler_function(arg1, arg2):
    pass
```

- `event_name` - der Name des Events, das behandelt werden soll. Das kann jeder Text sein, der zu einem existierenden Event passt, einfacher ist aber `from Blindflug.MinorEvents import MinorEvent` mit den dort definierten Konstanten, etwa `MinorEvent.DAY_PHASE_CHANGE`.
- `chance` - die Chance von `0.0` bis `1.0`, dass der Handler beim Eintreten des Events aufgerufen wird. `0.5` ergibt 50 %. Standard ist `1.0` (immer).
- `max_occurrences` - wie oft der Handler in einem Spielstand höchstens laufen darf. Der Zähler wird im Spielstand gespeichert, unter dem Namen `<module>.<function>` des Handlers - benennst du Datei oder Funktion um, beginnt er von vorn. Ein negativer Wert bedeutet "kein Limit" und ist der Standard (`-1`); `0` bedeutet, dass der Handler nie läuft. Chance-Wurf und Limit-Prüfung passieren beide, bevor der Handler aufgerufen wird.

Der Name der Funktion kann jeder gültige Python-Name sein. Zusammen mit dem Dateinamen identifiziert er den Handler, wenn das Spiel zählt, wie oft er gelaufen ist.

Die Argumente der Funktion hängen vom Event ab (siehe [Events](events.md)). Die Funktion kann `False` zurückgeben, damit dieser Durchlauf nicht zu `max_occurrences` zählt. Das ist praktisch, wenn ein Handler nur begrenzt oft laufen soll, aber nur unter bestimmten Bedingungen. Gibst du nichts oder `True` zurück, zählt der Durchlauf ganz normal.

## Textformatierung { #string-formatting }

Text im Ereignisprotokoll (und andere Terme, die du registrierst) versteht ein paar Tags, die einen Namen in einen farbigen Link oder ein Icon verwandeln:

| Tag | Was er zeigt | Woher die Namen kommen |
|---|---|---|
| `[character:<id>]` | einen anklickbaren Link zum Crewmitglied mit dieser Id | Charakter-Ids, wie sie an deinen Handler übergeben werden |
| `[resource:<name>]` | Icon und Farbe der Ressource | `from Blindflug.GameResources import ResourceType` |
| `[morale:<name>]` | Icon und Farbe der Moralkategorie | `from Blindflug.Game.Characters.Morale import MoraleCategory` |
| `[CharacterStat:<name>]` | Icon und Farbe einer Crew-Fähigkeit (`Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating`) | `from BlindGame.CharacterStats.Data import CharacterStatType` |

`CharacterStat` wird mit großem `C` und `S` geschrieben - bei diesem Tag zählt die Groß- und Kleinschreibung.

Der Name in einem Tag muss exakt der Name des Enum-Werts sein; einen Namen, den das Spiel nicht kennt, lässt es unverändert im Text stehen. Schreibst du den Enum-Wert in einen f-String, wie in den Beispielen oben, entsteht genau dieser Name.

Tags werden aufgelöst, nachdem die Platzhalter des Terms ausgefüllt sind, ein Tag kann also einen Platzhalter umschließen:

```python
localization.SetTerm("en", "mymod/found", "Found some [resource:{[RESOURCE]}]!")
event_log.Create("mymod/found", {"RESOURCE": str(resource)})
```

Hier ist `resource` ein `ResourceType`-Wert, den dein Handler erhalten hat, zum Beispiel vom Event `resource_gained`.
