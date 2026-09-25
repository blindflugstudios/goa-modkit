# Missionen

Eine Mission ist ein Flug, auf den der Spieler Flugzeuge schickt: Sie erscheint auf der Kriegskarte, kostet Zeit und Treibstoff und kommt mit einem Ergebnis zurück. Du hast zwei Wege, eine zu bauen:

| | Was es ist | Am besten für |
|---|---|---|
| **Der Mission Editor** | Ein Fenster im Spiel. Felder ausfüllen, **Validate** drücken, **Save** drücken. | Deine erste Mission und alles, bei dem du Zahlen schnell ausprobieren willst. |
| **JSON- und Python-Dateien** | Eine `.json`-Datei mit den Zahlen und eine optionale `.py`-Datei mit Text und Logik. | Alles andere - Ketten, Kampagnen, Missionen, die darauf reagieren, was der Spieler getan hat. |

Unter der Haube ist beides dasselbe. Der Editor schreibt genau das JSON, das du auch von Hand geschrieben hättest. Du kannst also im Editor anfangen und dann im Texteditor weitermachen.

| Seite | Inhalt |
|---|---|
| [Deine erste Mission](first-mission.md) | eine geführte Anleitung vom leeren Ordner bis zur geflogenen Mission |
| [Ketten und Kampagnen](chains.md) | Missionen, die aufeinander folgen, und Kampagnenkarten |
| [Orte](locations.md) | jeder Ort, an dem eine Mission stattfinden kann, mit Koordinaten |
| [Referenz](reference.md) | jedes JSON-Feld und jeder Handler im Detail |
| [So funktionieren Mods](../basics/mods.md) | wo ein Mod-Ordner liegt und wie das Spiel ihn findet |
| [CSV-Tabellen](../data/csv.md) | die Zahlen des Spiels ändern, statt Missionen hinzuzufügen |

## Woher Missionen kommen { #where-missions-come-from }

Das Spiel liest Missionen aus mehreren Quellen. Haben zwei dieselbe Id, gewinnt die spätere:

1. **Mitgelieferte Missionen** - im Spiel (und im Supporter Pack, falls du es besitzt), nur lesbar. Du kannst eine überschreiben, indem du ihre Id wiederverwendest, aber du kannst sie nicht direkt bearbeiten.
2. **Mods** - `Mods/<dein Mod>/Missions/` mit `.json`- und `.py`-Dateien. So gibst du eine Mission an andere weiter. Siehe [So funktionieren Mods](../basics/mods.md).
3. **Deine eigenen gespeicherten Missionen** - der Ordner, in den der Mission Editor im Spiel schreibt:

| Plattform | Ordner |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Missions\` |
| macOS | `~/Library/Application Support/Blindflug Studios/Ground Of Aces/Missions/` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Missions/` |

Dieser dritte Ordner gewinnt immer. Das macht ihn zu einem guten Ort, um Änderungen auszuprobieren - und zu einem Ort, den du leeren solltest, wenn eine deiner Missionen die Kopie in deinem Mod-Ordner scheinbar ignoriert.

## Der Mission Editor { #the-mission-editor }

Starte das Spiel und wähle im Hauptmenü **Mission Editor**.

!!! note
    Der Editor öffnet immer eine einzige Arbeitsmission namens `new_mission`. Hast du eine unter dieser Id gespeichert, lädt er sie, sonst beginnt er eine neue. Benenne sie vor dem Speichern im Feld **Mission Id** um, dann beginnt der nächste Besuch mit einer frischen `new_mission`. So kannst du eine Mission nach der anderen schreiben.

    Einen Missions-Browser gibt es noch nicht. Der Editor kann also weder eine mitgelieferte Mission öffnen noch eine, die du umbenannt und gespeichert hast, wieder aufrufen. Um an einer gespeicherten Mission weiterzuarbeiten, bearbeite ihre `.json` im Missions-Ordner oben oder fang mit einer Kopie neu an.

### Was du ausfüllst { #what-you-fill-in }

**Identität.** Die Missions-Id und die Tags, die entscheiden, auf welchen Karten die Mission erscheinen kann. Eine Id darf nur Kleinbuchstaben, Ziffern und Unterstriche enthalten.

**Tags.** Tags sind frei wählbare Etiketten, keine Kartennamen. Eine Karte listet die Tags, die sie unterstützt, in ihrer `Metadata.json` (das Feld `_tags` in der `.goamap`-Datei). Eine Mission listet die Tags, für die sie geschrieben ist (das Feld `_tags` im Missions-JSON). Die Mission kann nur auf dieser Karte auftauchen, wenn beide Listen mindestens einen Tag gemeinsam haben. Mehrere Tags an einer Mission bedeuten "einer davon" - ein Treffer genügt.

Tippe sie als eine kommagetrennte Liste ohne Leerzeichen ins Tag-Feld der Mission: `naval,atlantic`. Für Tags gelten dieselben Regeln wie für Ids - Kleinbuchstaben, Ziffern und Unterstriche. Das Feld setzt das schon beim Tippen durch: Großbuchstaben werden zu Kleinbuchstaben, alles andere fällt weg. Der Abgleich mit einer Karte ignoriert Groß- und Kleinschreibung ohnehin, eine Karte mit dem Tag `Campaign_Debden` zählt also trotzdem.

Eine leere Liste ist der Normalfall. Eine leere Liste auf einer der beiden Seiten zählt als der einzelne Tag `default`, und jede mitgelieferte Karte listet `default`. Eine Mission ohne Tags ist also auf allen verfügbar. Gibst du einer Mission den Tag `campaign_debden`, erscheint sie nur auf Karten, die ebenfalls `campaign_debden` listen - und sonst nirgends, nicht einmal auf den mitgelieferten Karten, es sei denn, du fügst `default` hinzu. Eine Karte für eine Kampagne listet meist nur ihren eigenen Tag, genau damit die normalen Missionen draußen bleiben.

!!! note "Quests haben keine Tags"
    Tags gibt es nur für Missionen. Eine Quest hat kein Tag-Feld. Eine Karte wählt ihre Quests über die Liste `StartingQuestIds` in ihrer `Metadata.json`; steht dort nichts, startet sie die Standard-Questreihe des Spiels (`quest0`). Siehe [Quests und Karten](../quests/index.md#quests-and-maps).

**Validate** warnt dich, wenn eine Mission einen Tag trägt, den keine bekannte Karte angibt. Eine solche Mission kann nirgends erscheinen - das willst du nur, wenn ein Skript sie direkt vergibt.

**Zeit und Größe.** Wie viele Flugzeuge der Spieler schicken darf, wie lange die Mission auf der Karte wartet, bevor sie verfällt, und wie lange der Flug selbst dauert. Beide Zeiten sind Bereiche - das Spiel würfelt einen Wert zwischen den beiden Zahlen.

**Schwierigkeit.** Die Chance, dass die Mission nach Plan läuft, eine Schwierigkeitsstufe von 1 bis 3 und die Feindstärke, die der Aufklärungsbericht dem Spieler zeigt.

**Text.** Missionsname und Beschreibung, der Bedrohungsbericht der Aufklärung und die Funksprüche für jedes Ende. Tipp sie einfach direkt ein. Eine im Editor geschriebene Mission braucht kein Skript, denn jede Mission ohne eigenes Skript läuft mit dem gemeinsamen Standard-Missionsskript des Spiels.

**Orte.** Wo auf der Kriegskarte die Mission erscheinen kann. Wähle aus der Liste und füge so viele hinzu, wie du willst; das Spiel sucht einen aus, wenn die Mission erstellt wird. Die vollständige Liste mit Koordinaten steht unter [Orte](locations.md).

**Voraussetzungen.** Bedingungen, die erfüllt sein müssen, bevor die Mission überhaupt auftaucht - eine Startbahnstufe, ein Datumsfenster oder eine andere abgeschlossene Mission.

**Werte.** Die Fähigkeiten, gegen die die Mission würfelt. Du brauchst genau zwei: Die erste zählt, wenn der Flug nach Plan läuft, die zweite, wenn nicht.

**Ergebnisse.** Genau vier Enden und was jedes davon bringt oder kostet - Moral, Siegpunkte, Schaden.

**Historischer Tag.** Setz hier einen Haken, damit die Mission Teil der Geschichte wird: Sie erscheint an oder nach einem Datum deiner Wahl, belegt einen festen Platz, wenn sie fällig ist, und verschwindet für immer, sobald sie erfolgreich war.

### Vor dem Speichern prüfen { #validate-before-you-save }

**Validate** listet alles auf, was es finden kann. **Save** macht dieselbe Prüfung und verweigert das Speichern, wenn etwas ein Fehler ist.

**Fehler verhindern das Speichern:**

| Fehler | Bedeutung |
|---|---|
| Missions-Id leer oder mit anderen Zeichen als `a-z`, `0-9` und `_` | |
| Missions-Id ist reserviert | eine mitgelieferte Mission nutzt sie schon |
| Mission mit dieser Id existiert bereits | Speichern würde eine andere gespeicherte Mission stillschweigend ersetzen |
| Ein Tag hat ungültige Zeichen | für Tags gelten dieselben Regeln wie für Ids |
| Nicht genau vier Ergebnisse | das Spiel wählt eines von vieren und prüft die Anzahl nie |
| Nicht genau zwei Werte | der Fähigkeitswurf liest beide |
| Zeit bis zum Start: Minimum über Maximum | |
| Dauer: Minimum über Maximum oder unter 5 Minuten | |
| Eine Startbahnstufe oder Datumsvoraussetzung, die keine ganze Zahl ist | |
| Eine Voraussetzung "abgeschlossene Mission", die das Spiel nicht lesen kann | |

**Warnungen lassen das Speichern zu**, sind aber trotzdem lesenswert:

| Warnung | Bedeutung |
|---|---|
| Keine Orte | die Mission kann nie auf der Karte platziert werden |
| Doppelte Ortsnamen | |
| Unbekannter Karten-Tag | keine bekannte Karte trägt diesen Tag, die Mission ist also nirgends verfügbar - nur gewollt, wenn ein Skript sie vergibt |
| Schwierigkeitsstufe außerhalb von 1–3 | |
| Weniger als ein Flugzeugplatz | niemand kann sie fliegen |
| Zeit bis zum Start läuft nie ab | die Mission bleibt für immer auf der Karte |
| Ein unbrauchbarer historischer Tag | das Datum ist fehlerhaft, leer oder unplausibel früh, die Mission hat also gar kein frühestes Datum |
| Ein Wert, dessen Minimum über dem Maximum liegt | |
| Ein Ergebnis-Effekt, den das Spiel nicht lesen kann | dieser eine Effekt wird stillschweigend nie angewendet |
| Ein Ergebnis nutzt Max Victory Points | diesen Wert berechnet das Spiel selbst und ignoriert ihn, wenn du ihn einträgst |
| Fehlender Erzähltext | dieser Textplatz zeigt im Spiel nichts an |

Die Warnung über fehlenden Text erscheint nicht bei mitgelieferten Missionen, denn die tragen übersetzte Texte statt im Editor eingetippter.

### Was der Editor nicht kann { #what-the-editor-cannot-do }

- Eine mitgelieferte Mission öffnen oder kopieren.
- Die Python-Seite schreiben. Alles, was etwas *entscheiden* muss - auf die geflogene Crew reagieren, eine Folgemission vergeben, den Text je nach Geschehen ändern -, braucht ein Skript.
- Eine Kette über eine einzelne Voraussetzung "diese Mission muss abgeschlossen sein" hinaus bauen. Längere Ketten sind in den Dateien leichter zu überblicken und zu pflegen. Siehe [Ketten und Kampagnen](chains.md).

Für all das öffnest du die Missionsdatei in einem Texteditor, direkt aus dem Dateibrowser.

## JSON und Python { #json-and-python }

Eine Mission ist eine `.json`-Datei mit den Zahlen und optional eine gleichnamige `.py`-Datei mit dem Text und etwaiger Logik. Der Dateiname ist die Missions-Id. Beide kommen in den Ordner `Missions/` deines Mods (oder, solange du ausprobierst, in deinen eigenen `Missions`-Ordner von oben).

```text
Mods/
  my_mod/
    Missions/
      mymod_coastal_patrol.json
      mymod_coastal_patrol.py
```

Drei Dinge bringen Leute regelmäßig ins Stolpern, und alle drei sind Grenzen des Spiels, nicht deiner Dateien:

- **Genau vier Ergebnisse, in der richtigen Reihenfolge.** Das Spiel wählt eines nach Position und prüft nie, wie viele es gibt. Drei Einträge lassen die Mission abstürzen, wenn sie endet - lange nachdem du das JSON nicht mehr im Verdacht hast.
- **Mindestens zwei Missionswerte.** Der erste zählt, wenn die Mission nach Plan läuft, der zweite, wenn nicht. Ein einziger Eintrag lässt den Fähigkeitswurf abstürzen.
- **Stell deinen Ids den Namen deines Mods voran.** Eine doppelte Id ersetzt stillschweigend die Mission, die sie dupliziert, und welche gewinnt, hängt von der Ladereihenfolge ab.

Der **Validate**-Knopf des Mission Editors fängt alle drei ab, bevor du überhaupt startest. Jedes Feld des JSON ist unter [Referenz](reference.md) beschrieben, und vollständige, funktionierende Missionen findest du unter [Beispiele](../examples.md).

### Die zwei Modi { #the-two-modes }

Wie viel vom Skript das Spiel nutzt, hängt davon ab, ob neben der Mission eine `.json` liegt.

- **Mit JSON** - die Zahlen kommen aus der Datei. Das Skript liefert nur Text und Reaktionen, und die Handler, die Zahlen melden, werden nie aufgerufen.
- **Ohne JSON** - das Skript liefert alles, auch die Zahlen. Jeder Handler unten wird aufgerufen. Was sonst im JSON stünde - Werte, Ort, Plätze, Tags -, wird in `initialize_mission` über `missions_api` gesetzt (zum Beispiel `missions_api.SetMissionLocation` und `missions_api.SetTags`).

Das ist mit Abstand die häufigste Quelle für Verwirrung: Ein Handler, der in einer reinen Skript-Mission perfekt funktioniert, wird einfach ignoriert, sobald du eine `.json` hinzufügst.

### Missions-Event-Handler { #mission-event-handlers }

Ein Handler ist eine Python-Funktion, die das Spiel zu einem bestimmten Zeitpunkt im Leben der Mission aufruft. Jeder Name unten verlinkt auf seine vollständige Beschreibung unter [Referenz](reference.md).

| Handler | Was er tut | Wann er läuft |
|---|---|---|
| [`get_mission_id`](reference.md#get_mission_id) | die Kennung der Mission | **immer** - Pflicht |
| [`initialize_mission`](reference.md#initialize_mission) | die Mission beim Erstellen einrichten | immer |
| [`send_mission_event`](reference.md#send_mission_event) | Fortschritt melden, während der Flug in der Luft ist | immer |
| [`set_mission_impact`](reference.md#set_mission_impact) | Folgen anwenden, sobald das Ergebnis feststeht | immer |
| [`send_mission_result_text`](reference.md#send_mission_result_text) | der Text, der beim Ende der Mission erscheint | immer |
| [`send_mission_cancelled_text`](reference.md#send_mission_cancelled_text) | der Text, der erscheint, wenn der Spieler abbricht | immer |
| [`get_mission_result_text`](reference.md#get_mission_result_text) | der Text im Ergebnisfenster | immer |
| [`get_mission_name`](reference.md#get_mission_name) | der Name im Missions-Infofenster | reine Skript-Missionen |
| [`get_mission_description_text`](reference.md#get_mission_description_text) | die Beschreibung im Infofenster | reine Skript-Missionen |
| [`get_time_to_start`](reference.md#get_time_to_start) | wie lange der Spieler Zeit hat, sie zu starten | reine Skript-Missionen |
| [`get_completion_time`](reference.md#get_completion_time) | wie lange der Flug dauert | reine Skript-Missionen |
| [`get_threat_level`](reference.md#get_threat_level) | die Bedrohungsstufe im Infofenster | reine Skript-Missionen |
| [`get_enemy_count`](reference.md#get_enemy_count) | wie viele Feinde da sind | reine Skript-Missionen |
| [`get_mission_events_count`](reference.md#get_mission_events_count) | wie viele Fortschrittsmeldungen gesendet werden | reine Skript-Missionen |
| [`get_fuel_level`](reference.md#get_fuel_level) | der Treibstoff, den die Mission braucht | reine Skript-Missionen |
| [`get_mission_result`](reference.md#get_mission_result) | ob die Mission erfolgreich war | reine Skript-Missionen |

In einer reinen Skript-Mission sind die Getter von `get_mission_name` bis `get_fuel_level` optional: Lässt du einen weg, nimmt das Spiel stattdessen einen Standardwert. Bei einer Mission mit JSON ist die Zahl der Fortschrittsmeldungen fest auf 3 gesetzt, `get_mission_events_count` wird dort also ignoriert.

!!! warning "Handler, die nie aufgerufen werden"
    Implementiere `get_mission_icon`, `calculate_mission_modifiers`, `calculate_airplane_modifiers` oder `calculate_pilot_modifiers` nicht. Die Namen gibt es noch, aber nichts ruft sie auf - das Spiel berechnet Missionsmodifikatoren inzwischen selbst. Ältere Beispielskripte implementieren sie ausführlich; dieser Code läuft nie.

    `get_mission_fatalities` gibt es auch nicht mehr. Verluste laufen über den Ergebnis-Effekt `Damage`.

## Wie es weitergeht { #where-to-go-next }

- [Deine erste Mission](first-mission.md) - Schritt für Schritt eine bauen und fliegen.
- [Referenz](reference.md) - jedes Feld, jeder Handler und jeder Ergebnis-Effekt.
- [Beispiele](../examples.md) - vollständige Missionen zum Kopieren, von einer einzelnen Patrouille bis zu einer fünfteiligen Kampagne. Fang mit der Küstenpatrouille an.
- [Scripting](../scripting/index.md) - wie Python-Skripte geladen werden, und Event-Skripte, die keine Missionen sind.
