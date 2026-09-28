# Lokalisierung

Jeder Text, den der Spieler sieht, wird über einen **Schlüssel** nachgeschlagen, einen kurzen Namen wie `missions/coastal_patrol/mission_name`. Das Spiel sucht den Text für diesen Schlüssel in der Sprache des Spielers. Diese Seite zeigt, wie eine Mod ihren Schlüsseln Text gibt, in einer Sprache oder in vielen, ohne eine einzige Datei des Spiels anzufassen.

## Der einfachste Weg: Text im Missions-JSON { #the-simplest-way-text-in-the-mission-json }

Eine Mission kann ihren Text direkt in ihrer JSON-Datei tragen. Kein Skript, keine Schlüssel:

```json
{
    "_rawMissionName": "The Lost Bombers",
    "_rawMissionDescription": "A flight of our own bombers is limping home from France."
}
```

Das ist nur eine Sprache und deckt genau neun Slots pro Mission ab. Siehe [Text im JSON statt eines Terms](#text-in-the-json-instead-of-a-term) weiter unten. Für alles andere registrierst du Text aus einem Skript.

## Text aus einem Skript definieren { #defining-text-from-a-script }

```python
localization.SetTerm("en", "mymod/greeting", "Good morning, gentlemen.")
```

`SetTerm(language_code, key, text)` gibt einem Schlüssel seinen Text in einer Sprache. Ein Schlüssel mit seinen Texten heißt **Term**.

Ruf es auf der **obersten Ebene** eines Skripts auf, nicht in einem Handler. Die oberste Ebene läuft einmal, wenn das Spiel das Skript lädt, der Text existiert also, bevor irgendetwas ihn braucht.

Ein Skript, das nur Text definiert, ist völlig in Ordnung. Es braucht keinen Handler, kein JSON und keine Missions-Id. Leg es wie jedes andere Skript in den `Missions/`-Ordner der Mod; das Spiel führt jedes Skript aus, das es dort findet.

### Warum das sicher ist { #why-this-is-safe }

Text, den du registrierst, landet nicht in den Übersetzungsdateien des Spiels. Das Spiel führt einen eigenen Speicher für Text aus Skripten, fügt ihm Schlüssel hinzu, sobald Skripte sie registrieren, und schaut dort ebenfalls nach. Nichts, was du mit `SetTerm` machst, ändert eine Datei auf der Festplatte, und es gibt keinen Übersetzungsschritt, den du ausführen musst.

Gibt es den Schlüssel schon in den eigenen Texten des Spiels, ersetzt `SetTerm` diesen Text, solange deine Mod geladen ist. So kann eine Mod eine eingebaute Zeile umformulieren. Deshalb solltest du auch jeden eigenen Schlüssel mit deinem Mod-Namen versehen: Ein versehentlicher Treffer überschreibt den Text des Spiels stillschweigend.

## Missionstexte { #mission-texts }

Eine Mission verwendet neun Schlüssel, alle nach dem Muster `missions/<missionId>/<slot>`.

**Drei liest das Spiel selbst**, und sie lassen sich nicht umbenennen:

| Schlüssel | Angezeigt in |
|---|---|
| `missions/<id>/mission_name` | der Missionsliste und dem Ergebnisfenster |
| `missions/<id>/mission_description` | dem Missionsfenster |
| `missions/<id>/intel_threat_report` | der Bedrohungszeile im Missionsfenster |

Fehlt einer, erscheint im Spiel der rohe Schlüssel.

**Sechs verwendet das Missionsskript.** Das gemeinsame Standard-Missionsskript verwendet genau diese Namen, also braucht auch eine Mission ohne eigenes Skript sie:

| Schlüssel | Wann |
|---|---|
| `missions/<id>/ap_transmission` | im Flug, läuft nach Plan |
| `missions/<id>/gw_transmission` | im Flug, schiefgelaufen |
| `missions/<id>/ap_success_transmission` | wie geplant, Fertigkeit bestanden |
| `missions/<id>/ap_failure_transmission` | wie geplant, Fertigkeit gescheitert |
| `missions/<id>/gw_success_transmission` | schiefgelaufen, Fertigkeit bestanden |
| `missions/<id>/gw_failure_transmission` | schiefgelaufen, Fertigkeit gescheitert |

`ap` steht für "as planned" (wie geplant), `gw` für "gone wrong" (schiefgelaufen). Die vier Schlüssel `*_success` und `*_failure` entsprechen eins zu eins den vier Ausgangs-Slots im Missions-JSON.

Eine kleine Hilfsfunktion hält ein Missionsskript lesbar:

```python
MISSION_ID = "mymod_coastal_patrol"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Coastal Patrol")
_term("mission_description", "Fly the shoreline. Report anything that moves.")
```

Ein Missionsskript darf beliebig viele zusätzliche Schlüssel registrieren (zum Beispiel `missions/<id>/veteran_departure`) und sie mit `event_log.Create` verwenden.

## Text im JSON statt eines Terms { #text-in-the-json-instead-of-a-term }

Die neun `_raw*`-Felder eines Missions-JSON bedienen die neun Slots oben direkt. Ist ein Raw-Feld gefüllt, verwendet das Spiel es, bevor es den Schlüssel nachschlägt. Eine Mission mit Raw-Text braucht also keinen `SetTerm`-Aufruf und überhaupt kein Skript.

| JSON-Feld | Slot, den es bedient |
|---|---|
| `_rawMissionName` | `mission_name` |
| `_rawMissionDescription` | `mission_description` |
| `_rawIntelThreatReport` | `intel_threat_report` |
| `_rawApTransmission` | `ap_transmission` |
| `_rawGwTransmission` | `gw_transmission` |
| `_rawApSuccessTransmission` | `ap_success_transmission` |
| `_rawApFailureTransmission` | `ap_failure_transmission` |
| `_rawGwSuccessTransmission` | `gw_success_transmission` |
| `_rawGwFailureTransmission` | `gw_failure_transmission` |

Ein leeres Feld zählt als nicht gefüllt, und das Spiel greift auf den Schlüssel zurück.

**Nur diese neun Slots funktionieren so.** Es gibt kein zehntes `_raw*`-Feld: `event_log.Create("missions/mymod_patrol/my_own_line")` ohne Term dahinter gibt den rohen Schlüssel aus.

### Was du verwenden solltest { #which-to-use }

| | `_raw*` im JSON | `SetTerm` in einem Skript |
|---|---|---|
| Braucht ein Skript | nein | ja |
| Anzahl der Texte | genau neun | unbegrenzt |
| Sprachen | eine | alle, die das Spiel in seinen Einstellungen anbietet |
| Gut für | eine Mission mit festem Text | Text, der sich danach richtet, was im Flug passiert ist |

Beides lässt sich kombinieren: Raw-Text deckt die neun Standard-Slots ab, und ein Skript ergänzt eigene Terms für alles darüber hinaus. Das Beispiel `raf_collection` macht genau das: Drei Missionen liefern nur Raw-Text, und `greenhorn_watch` fügt eigene Terms hinzu, damit es je nach Erfahrung der Crew eine andere Geschichte erzählen kann.

## Questtexte { #quest-texts }

Quest-Dateien tragen Schlüssel, keinen Text: `_questTitle`, `_subQuestTitle` und `_subQuestDescription` enthalten Schlüssel, und das Spiel schlägt sie nach. Die eigenen Quests des Spiels verwenden dieses Muster:

```text
quest/<questId>/title
quest/<questId>/subQuest<N>_title
quest/<questId>/subQuest<N>_description
```

Um einer Mod-Quest ihren Text zu geben, liefere ein kleines Skript im `Missions/`-Ordner der Mod mit, das diese Schlüssel registriert:

```python
QUEST_ID = "mymod_first_steps"

localization.SetTerm("en", "quest/{}/title".format(QUEST_ID), "First Steps")
localization.SetTerm("en", "quest/{}/subQuest0_title".format(QUEST_ID), "Clear the field")
localization.SetTerm("en", "quest/{}/subQuest0_description".format(QUEST_ID), "Fell five trees.")
```

Die Schlüssel müssen nur mit dem übereinstimmen, was in der Quest-Datei steht. Siehe [Quests](../quests/index.md).

## Platzhalter { #placeholders }

`event_log.Create` nimmt ein Dictionary, das `{[NAME]}`-Platzhalter füllt:

```python
localization.SetTerm("en", "mymod/pilot_tired",
                     "{[PILOT]} came back exhausted after {[HOURS]} hours in the air.")

event_log.Create("mymod/pilot_tired", {"PILOT": str(pilot_id), "HOURS": "6"})
```

Bei Platzhalternamen zählt Groß- und Kleinschreibung, und sie müssen exakt übereinstimmen. Werte müssen Strings sein, pack Zahlen und Ids also in `str(...)`.

## Inline-Formatierung { #inline-formatting }

Vier Tags funktionieren in jedem Text:

| Tag | Wirkung |
|---|---|
| `[character:<id>]` | ein anklickbarer Link zu diesem Charakter, angezeigt als sein Name |
| `[resource:<name>]` | Symbol und Farbe der Ressource |
| `[morale:<name>]` | Symbol und Farbe der Moralkategorie |
| `[CharacterStat:<name>]` | Symbol und Farbe einer Crew-Fähigkeit (`Flying`, `Shooting`, `Bombing`, `Endurance`, `Engineering`, `Navigating`) |

`CharacterStat` schreibt sich mit großem `C` und `S` - bei diesem Tag kommt es auf Groß- und Kleinschreibung an.

Kombiniere sie mit Platzhaltern, um einen Charakter aus einem Event zu nennen:

```python
localization.SetTerm("en", "mymod/chat",
                     "[character:{[FIRST]}] talked to [character:{[SECOND]}] until dawn.")

event_log.Create("mymod/chat", {"FIRST": str(first_id), "SECOND": str(second_id)})
```

Für Ressourcen, Moral und Crew-Fähigkeiten setzt du den Spielwert beim Laden des Skripts in den Text ein:

```python
from Blindflug.GameResources import ResourceType
from Blindflug.Game.Characters.Morale import MoraleCategory
from BlindGame.CharacterStats.Data import CharacterStatType

localization.SetTerm("en", "mymod/mice",
                     "Mice got into the [resource:{}] again.".format(ResourceType.FoodRations))
localization.SetTerm("en", "mymod/good_chat",
                     "Their [morale:{}] improved.".format(MoraleCategory.Mood))
```

f-Strings funktionieren auch, und die eigenen Skripte des Spiels verwenden sie. Denk daran, die geschweiften Klammern eines Platzhalters in einem f-String zu verdoppeln: `f"[character:{{[FIRST]}}] shared the [resource:{ResourceType.FoodRations}]"`.

## Sprachen { #languages }

Definiere immer Englisch (`"en"`). Hat ein Term keinen Text in der Sprache des Spielers, zeigt das Spiel den Text einer Sprache, die du registriert hast - mit `en` bist du also auf der sicheren Seite. Ein Schlüssel, der in keiner einzigen Sprache registriert ist, erscheint als roher Schlüssel.

Zum Übersetzen rufst du `SetTerm` einmal pro Sprache auf:

```python
localization.SetTerm("en", "mymod/greeting", "Good morning, gentlemen.")
localization.SetTerm("de", "mymod/greeting", "Guten Morgen, meine Herren.")
localization.SetTerm("fr", "mymod/greeting", "Bonjour, messieurs.")
```

Das Spiel liefert diese Sprachcodes mit:

`en`, `en-GB`, `de-DE`, `de`, `ar`, `bg`, `ca`, `zh-CN`, `zh-TW`, `cs`, `da`, `nl`, `fi`, `fr`, `el`, `hu`, `id`, `it`, `ja`, `ko`, `ms`, `nb`, `fa`, `pl`, `pt`, `pt-BR`, `ro`, `ru`, `es`, `es-419`, `sv`, `gsw-CH`, `th`, `tr`, `uk`, `vi`

Deutsch ist `de` - das ist die Sprache, die Spieler in den Einstellungen wählen (`de-DE` in der Liste ist eine Testsprache, die du ignorieren kannst). Der Sprachcode muss einer sein, den das Spiel in seinen Einstellungen anbietet.

Ein praktisches Muster für mehrere Sprachen:

```python
TEXTS = {
    "mymod/greeting": {
        "en": "Good morning, gentlemen.",
        "de": "Guten Morgen, meine Herren.",
    },
}

for key, translations in TEXTS.items():
    for language, text in translations.items():
        localization.SetTerm(language, key, text)
```

## Wenn die Mod entfernt wird { #when-the-mod-is-removed }

Text, der mit `SetTerm` registriert wurde, existiert nur, solange das Skript geladen ist, das ihn registriert hat. Er wird nie in den Spielstand oder in die Dateien des Spiels geschrieben.

Wenn ein Spieler deine Mod entfernt oder ausschaltet und einen Spielstand lädt:

- Deine Terms sind weg. Alles im Spielstand, was noch auf einen deiner Schlüssel verweist, zeigt statt des Texts den **rohen Schlüssel**. Das gilt für alte Zeilen im Ereignisprotokoll, die deine Skripte geschrieben haben, und für Missionen aus deiner Mod, die noch auf der Kriegskarte warteten.
- Ein Schlüssel des Spiels, den deine Mod umformuliert hatte, zeigt wieder den Originaltext des Spiels.
- Nichts geht kaputt; wenn du die Mod neu installierst, ist der Text wieder da.

Missionstext aus `_raw*`-Feldern wird beim Erstellen in die Mission kopiert. Eine Mission, die schon auf der Kriegskarte lag, behält ihren Namen also auch, nachdem die Mod weg ist.

## Deine Schlüssel benennen { #naming-your-keys }

Setz deinen Mod-Namen vor jeden Schlüssel (`mymod/...`), damit er nicht mit dem Spiel oder einer anderen Mod kollidieren kann: Ein vorhandener Schlüssel wird stillschweigend überschrieben. Missionsschlüssel sind die Ausnahme, weil sie `missions/<missionId>/...` folgen müssen. Mach stattdessen die Missions-Id selbst unverwechselbar, was du ohnehin tun solltest.
