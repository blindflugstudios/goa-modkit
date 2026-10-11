# Quests { #quests }

Eine Quest ist eine Liste von Zielen, die der Spieler in der Quest-Leiste sieht - im deutschen Spiel heißen Quests "Aufgaben" (Quests): *Bau eine Startbahn, bestell ein Flugzeug, flieg fünf Missionen*. Jedes Ziel (ein **Schritt**) ist ein Zähler, der sich füllt, während der Spieler die Sache erledigt. Sind alle Pflichtschritte voll, ist die Quest abgeschlossen, und die nächste in der Kette kann starten.

Quests sind keine Missionen. Eine Mission ist ein Flug, dessen Ausgang Würfelwürfe entscheiden; eine Quest ist eine Checkliste, die das Spiel beobachtet und Häkchen setzt. Eine Quest ist eine einzige `.json`-Datei, in der nichts "läuft", und die Arten von Zielen, die sie verfolgen kann, sind fest ins Spiel eingebaut - ein Ziel kann aber auf deine eigenen Inhalte zeigen, etwa auf eine Mission aus deiner Mod.

!!! note "Kein Quest-Editor"
    Quests schreibst und änderst du nur in einem Texteditor. Der Mission Editor öffnet sie nicht, und das Spiel prüft sie vor dem Laden nicht - die [Checkliste](#checklist-before-you-ship) am Ende dieser Seite ist deine Prüfung.

| Seite | Inhalt |
|---|---|
| [Missionen](../missions/index.md) | Missionen und die Ereignisse, auf die eine Quest warten kann, wenn eine Mission zurückkehrt |
| [Orte](../missions/locations.md) | die Ortsmerkmale, nach denen ein Missionsschritt filtern kann (`sea`, `enemyterritory`, ...) |
| [CSV-Tabellen](../data/csv.md) | die Datentabellen mit den ids, die du in Quests verwendest - Gebäude, Flugzeuge, Ressourcen, Pflanzen |
| [Beispiel-Quests](#example-quests) | vollständige Quest-Dateien zum Kopieren |

## Woher Quests kommen { #where-quests-come-from }

Das Spiel liest Quests aus zwei Quellen, und die spätere gewinnt, wenn beide dieselbe id haben:

1. **Mitgelieferte Quests** - im Spiel enthalten, schreibgeschützt. Du kannst eine überschreiben, indem du ihren Dateinamen wiederverwendest, aber du kannst sie nicht direkt bearbeiten.
2. **Mods** - `Mods/<your mod>/Quests/` mit `.json`-Dateien. Gelesen werden nur Dateien direkt in `Quests/`; Unterordner werden ignoriert. Nur *aktivierte* Mods werden gelesen - eine im Mods-Fenster ausgeschaltete Mod steuert keine Quests bei.

Anders als bei Missionen gibt es **keinen persönlichen Quest-Ordner** außerhalb einer Mod. Um eine Quest auszuprobieren, leg sie in einen Mod-Ordner ([So funktionieren Mods](../basics/mods.md) erklärt, wo dieser Ordner liegt und wie das Mods-Fenster funktioniert). Die Quests kommen in einen Unterordner `Quests`, neben den anderen Inhaltsarten:

```text
Mods/
  my_campaign/
    config.json                  required - its "Name" is what the Mods screen shows
    Quests/
      mycampaign_first_steps.json
      mycampaign_first_patrol.json
    Missions/                    optional - mission files, and the .py that holds your quest text
    Maps/                        optional - the map that starts your quest line
```

Aus der Art, wie die Dateien gelesen werden, ergeben sich zwei Regeln:

- **Der Dateiname ist die Quest-id.** `mycampaign_first_steps.json` ist die Quest `mycampaign_first_steps`, egal was im Feld `_questId` steht. Halte beide identisch: Das Spiel prüft anhand des *Dateinamens*, ob eine Quest schon im Spielstand existiert, speichert aber das *Feld* im Spielstand. Weichen sie voneinander ab, wird die Quest bei jedem Laden erneut vergeben, und Ketten (Bedingungstyp 1) beziehen sich auf das Feld.
- **Stell deinen ids den Namen deiner Mod voran.** Eine Datei namens `quest3.json` *ersetzt* stillschweigend die mitgelieferte `quest3`. Haben zwei Mods denselben Dateinamen, gewinnt die später geladene (siehe [Welche Mod gewinnt](../basics/mods.md#which-mod-wins)).

!!! note "Wann Änderungen sichtbar werden"
    Quest-Dateien werden bei jedem Laden eines Levels neu eingelesen - geh zurück ins Hauptmenü (Main Menu) und lade erneut (einen Spielstand zu laden reicht). Ein brandneuer Mod-Ordner oder ein `Quests/`-Ordner, der beim Spielstart noch leer war, braucht zuerst **Refresh** im Mods-Fenster oder einen Neustart.

## Eine erste Quest { #a-first-quest }

Das hier ist eine vollständige, funktionierende Quest. Speichere sie als `Mods/my_campaign/Quests/mycampaign_first_steps.json`, starte das Spiel und lade oder starte eine beliebige Karte: Sie erscheint sofort in der Quest-Leiste.

```json
{
    "_questId": "mycampaign_first_steps",
    "_questTitle": "mycampaign/first_steps/title",
    "_questDescription": "",
    "_subQuests": [
        {
            "_subQuestTitle": "mycampaign/first_steps/step0_title",
            "_subQuestDescription": "mycampaign/first_steps/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 7,
                "_parameter": "building_finished,Sickbed",
                "_amount": 1
            },
            "_genericIconKey": "ui_health"
        },
        {
            "_subQuestTitle": "mycampaign/first_steps/step1_title",
            "_subQuestDescription": "",
            "_isOptional": true,
            "_subQuestRequirement": {
                "_type": 4,
                "_parameter": "Bed",
                "_amount": 4
            },
            "_genericIconKey": "ui_bed"
        }
    ],
    "_requirements": [],
    "_isHiddenInUI": false,
    "_questType": 0
}
```

Von oben nach unten gelesen: Die Quest hat zwei Schritte. Der erste wartet, bis ein Krankenbett *fertig gebaut* ist - einmal. Der zweite zählt die Betten auf der Basis und ist bei vier voll, ist aber optional, also ist die Quest abgeschlossen, sobald das Krankenbett steht. `_requirements` ist leer, das heißt, die Quest startet auf jeder Karte, die sie in ihren `StartingQuestIds` aufführt - siehe [Quests und Karten](#quests-and-maps).

Die Titel sind **Lokalisierungsschlüssel**, kein Text - solange du sie nicht registrierst, sieht der Spieler überhaupt keinen Titel. Der Abschnitt [Text](#text) erklärt, wie du ihnen Worte gibst.

## Die Datei, Feld für Feld { #the-file-field-by-field }

| Feld | Bedeutung |
|---|---|
| `_questId` | Die id der Quest. Halte sie gleich dem Dateinamen. |
| `_questTitle` | Lokalisierungsschlüssel des Titels, der in der Quest-Leiste steht. |
| `_questDescription` | Lokalisierungsschlüssel eines längeren Texts unter dem Titel. `""` für keinen - so machen es die mitgelieferten Quests. |
| `_subQuests` | Die Schritte, in der Reihenfolge, in der sie in der Leiste stehen. Mindestens einer. |
| `_requirements` | Wann die Quest vergeben wird - siehe [Wie eine Quest startet](#how-a-quest-starts). Kein Fortschritt. |
| `_isHiddenInUI` | `true` blendet die Quest in der Leiste aus, während sie weiterläuft. Wird von den mitgelieferten Skin-Freischalt-Quests genutzt. |
| `_questType` | `0` eine normale Quest, `1` eine Flugzeug-Skin-Quest, `2` eine Tutorial-Quest. Nimm `0` - siehe [Quest-Typen](#quest-types). |
| `_highlightedUIElements` | Nur Tutorial-Quests: Buttons, auf die das Tutorial zeigt. Wird bei Typ `0` ignoriert. |
| `_cheatsOnStart`, `_completionCheats` | Nur Tutorial-Quests, und **in jeder Mod-Quest ignoriert** - siehe [Quest-Typen](#quest-types). |

Felder, die du weglässt, bekommen ihren Standardwert: `false`, `0` oder leer. Zusätzliche Felder (die mitgelieferten Dateien enthalten ein `"Name"`, das das Spiel nicht mehr liest) werden ignoriert. Es gibt kein Tags-Feld: Quests hängen anders an Karten als Missionen, siehe [Quests und Karten](#quests-and-maps).

Jeder Eintrag in `_subQuests` ist ein Schritt:

| Feld | Bedeutung |
|---|---|
| `_subQuestTitle` | Lokalisierungsschlüssel des Schritt-Titels. Gleichzeitig der Name, unter dem das Spiel den Schritt kennt (andere Quests können über `sub_quest_completed` darauf warten). |
| `_subQuestDescription` | Lokalisierungsschlüssel des Tooltips für den Schritt. `""` für keinen. |
| `_isOptional` | `true` - die Quest kann ohne diesen Schritt abgeschlossen werden. |
| `_subQuestRequirement` | *Was* gezählt wird: ein `_type`, ein `_parameter` und ein `_amount`. Genau eine pro Schritt. |
| `_genericIconKey` | Welches Symbol der Schritt zeigt. Siehe [Symbole](#icons). |

Und die Bedingung darin:

| Feld | Bedeutung |
|---|---|
| `_type` | Eine Zahl, die die Art der Bedingung auswählt - die vollständige Tabelle steht unter [Worauf ein Schritt warten kann](#what-a-step-can-wait-for). |
| `_parameter` | Eine kommagetrennte Liste, deren Bedeutung vom Typ abhängt. **Keine Leerzeichen** um die Kommas. |
| `_amount` | Der Zählerstand, bei dem der Schritt abgeschlossen ist. **Mindestens 1.** |

!!! warning "`_amount` muss mindestens 1 sein"
    Ein Schritt mit `_amount: 0` verhält sich unberechenbar: Je nachdem, ob die Quest beim Laden eines Spielstands oder später im laufenden Spiel entstanden ist, wird er sofort abgeschlossen oder nie - und im zweiten Fall blockiert er seine Quest für immer, außer er ist optional. Wenn du einen Schritt willst, den die Karte schon erfüllt (einen "Du bist hier"-Schritt), gib ihm stattdessen eine echte, bereits erfüllte Bedingung: `_type: 1`, `_parameter: "0"`, `_amount: 1` ist abgeschlossen, sobald die Basis irgendeinen Parkplatz hat.

### Text { #text }

Jedes Textfeld einer Quest ist ein **Lokalisierungsschlüssel** - ein Name, den das Spiel beim Zeichnen der Leiste in seiner Übersetzungstabelle nachschlägt. Ein Schlüssel, der in keiner Sprache registriert ist, wird gar nicht angezeigt: Die Quest-Karte behält den Text, den sie vorher hatte (einen Platzhalter oder den Text der Quest, die diese Karte zuletzt benutzt hat), und der Tooltip bleibt leer. Registriere jeden Schlüssel.

Missionen können ihren Text direkt im JSON tragen. **Quests können das nicht** - es gibt keine Felder für Rohtext, und eine Quest hat kein eigenes Skript. Du hast zwei Möglichkeiten:

**Einen mitgelieferten Schlüssel wiederverwenden.** Die Tutorial- und Hauptquests haben schon übersetzte Titel für Dinge wie "Baue eine Startbahn" oder "Bestelle ein Flugzeug". Öffne die passende mitgelieferte Quest und kopiere ihren Schlüssel. Das kostet nichts und ist in jede Sprache übersetzt, die das Spiel mitbringt, aber du bist auf Sätze beschränkt, die es schon gibt.

**Eigene Schlüssel aus einem Skript registrieren.** Eine `.py`-Datei im Ordner `Missions/` deiner Mod läuft beim Laden eines Levels, für jede aktivierte Mod, und ihre oberste Ebene kann Begriffe registrieren:

```python
TERMS = {
    "mycampaign/first_steps/title":             "First steps",
    "mycampaign/first_steps/step0_title":       "Build a sickbed",
    "mycampaign/first_steps/step0_description": "Injured crew recover faster in a bed of their own.",
    "mycampaign/first_steps/step1_title":       "Build four beds",
}

try:
    for term, text in TERMS.items():
        localization.SetTerm("en", term, text)
except Exception as error:
    print("MyCampaign: could not register quest terms: %s" % error)
```

Die Datei braucht keine Missions-Handler; sie existiert nur, um diesen Block auszuführen. Leg sie in `Missions/`, nicht in `Quests/` - aus `Quests/` werden nur `.json`-Dateien gelesen, und `Missions/` ist der einzige Ordner, aus dem das Spiel Skripte lädt. Ruf `SetTerm` einmal pro Sprache auf, die du unterstützen willst (`"de"`, `"fr"`, ...). Eine Sprache, die du weglässt, zeigt den Text einer Sprache, die du registriert hast - registriere also immer `en`. Das `try`/`except` ist wichtig: Ein Syntaxfehler überspringt nur dein Skript, aber jeder andere Fehler auf der obersten Ebene eines Skripts kann das Laden aller folgenden Skripte stoppen - deiner und die anderer Mods.

Registrierst du einen Schlüssel, den das Spiel schon mitbringt - einen Gebäudenamen, einen mitgelieferten Quest-Titel -, *ersetzt* du den Originaltext des Spiels für diese Sprache. Stell deinen Schlüsseln den Namen deiner Mod voran, damit das nie aus Versehen passiert. Mitgelieferte Quests benennen ihre Schlüssel `quest/<questId>/title`, `quest/<questId>/subQuest0_title` und `quest/<questId>/subQuest0_description`; für deine Quests ist diese Form nicht vorgeschrieben. Mehr zu Begriffen: [Lokalisierung](../scripting/localization.md).

### Symbole { #icons }

`_genericIconKey` wählt das Symbol des Schritts aus einem festen Satz, der ins Spiel eingebaut ist. Ein Schlüssel, den das Spiel nicht kennt, zeigt einfach kein Symbol; nichts wird [geloggt](../start/troubleshooting.md#find-the-playerlog). Aus einer Mod kannst du keine eigenen Symbole hinzufügen.

| Art | Schlüssel |
|---|---|
| Basis | `ui_path_runway`, `ui_runway`, `ui_path_cars`, `ui_functionarea_runway`, `ui_functionarea_parking`, `ui_functionarea_parking_1`, `ui_functionarea_parking_2`, `ui_functionarea_resources`, `ui_functionarea_safety`, `ui_functionarea_gardening`, `ui_hangar_roof`, `roof`, `wall`, `floor`, `door`, `house`, `ui_decoration_wall`, `ui_decoration_poster`, `ui_props_kitchen`, `ui_props_social` |
| Flugzeuge | `ui_plane`, `ui_plane_GlosterGladiator_MKI`, `ui_scramble`, `ui_aagun`, `ui_alarm`, `ui_radio` |
| Ressourcen | `ui_resource_wood`, `ui_resource_planks`, `ui_resource_metal`, `ui_resource_bricks`, `ui_resource_cement`, `ui_resource_fuel`, `ui_resource_gunAmmo`, `ui_resource_repairParts`, `ui_resource_trash`, `ui_resource_rubble`, `ui_resource_victoryPoints`, `ui_seeds_beans`, `ui_harvesting`, `ui_tool_gathering`, `ui_fire` |
| Crew | `ui_crew_person_single`, `ui_crew_people_multiple`, `ui_crewjob_cook`, `ui_crewjob_medic`, `ui_health`, `ui_morale`, `ui_bed`, `ui_prop_bed`, `ui_prestige_full`, `Endurance` |
| Oberfläche | `ui_camera`, `ui_move_tool`, `ui_pause`, `ui_speed_1`, `ui_speed_2`, `ui_speed_3`, `ui_timer_clock`, `ui_clock`, `ui_schedule`, `ui_eventlog`, `ui_notifications_all`, `ui_attention`, `ui_search_looking_glass`, `ui_lock_open`, `ui_headquarters`, `ui_stamp_headquarters_approved`, `ui_repairandcrafting`, `ui_cogwheel`, `ui_crown`, `ui_mark_exclamation`, `ui_assigned`, `ui_trash`, `plus` |
| Werkbänke | `SawStation`, `FieldKitchen`, `IndoorKitchen`, `ElectronicsWorkbench`, `BrickStation`, `CementMixer` |
| Objekt-Vorschaubilder | `PP0151_SickBed_thumbnail`, `PP1101_Bofors40mm_thumbnail`, `PP1002_SirenOnAPole_thumbnail`, `PP1006_LargeFuelTankWithConnector_thumbnail`, `PP1020_Flagpole5m_thumbnail`, `PP1030_Water_Pump_thumbnail`, `PP1000_RadioTower_thumbnail`, `PP0101_WoodenChair_thumbnail`, `PP0102_BarStool_thumbnail`, `PP0911_BarCounter_thumbnail`, `PP0956_DividerCurtains_thumbnail`, `BB0900_Sandbag1mStraightVarA_thumbnail`, `BB1300_Table1x2_thumbnail`, `Simple-Rack_thumbnail`, `GraveStoneWhite_thumbnail` |

`""` ist in Ordnung und bedeutet: kein Symbol. Im Zweifel kopierst du den Schlüssel aus einem mitgelieferten Schritt, der das gewünschte Bild zeigt.

## Worauf ein Schritt warten kann { #what-a-step-can-wait-for }

Jeder Schritt hat genau eine Bedingung, und ihr `_type` entscheidet, was das Spiel zählt. Es gibt zwei Arten:

- **Gezählter Zustand (abgefragt)** - alle paar Sekunden zählt das Spiel etwas auf der Basis (Startbahnen, Betten, Lagerzonen) und schreibt den Stand in den Schritt. Der Stand kann auch wieder *sinken*, wenn der Spieler etwas abreißt - bis zu dem Moment, in dem der Schritt abgeschlossen ist.
- **Gezählte Ereignisse** - der Schritt zählt eins hoch, jedes Mal wenn etwas *passiert* (ein Gebäude wird fertig, ein Flugzeug kehrt von einer Mission zurück). Diese Zähler sinken nie.

Der Fortschritt ist bei `_amount` gedeckelt, und ein abgeschlossener Schritt bleibt abgeschlossen.

### Alle Typen auf einen Blick { #all-types-at-a-glance }

| `_type` | Name | Art | Abschnitt |
|---|---|---|---|
| 0 | Airstrip | abgefragt | [Die Basis bauen](#building-the-base) |
| 1 | Parking | abgefragt | [Die Basis bauen](#building-the-base) |
| 2 | Airplane | abgefragt | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 3 | PropCategory | - tut nichts | [Typen, die nichts tun](#types-that-do-nothing) |
| 4 | Prop | abgefragt | [Die Basis bauen](#building-the-base) |
| 5 | SimpleEvent | Ereignis | [Ereignisse](#events) |
| 6 | Workbench | abgefragt | [Die Basis bauen](#building-the-base) |
| 7 | AnyAttributeEvent | Ereignis | [Ereignisse](#events) |
| 8 | AllAttributesEvent | Ereignis | [Ereignisse](#events) |
| 9 | FunctionArea (Zone) | abgefragt | [Die Basis bauen](#building-the-base) |
| 10 | ShelteredStorage | abgefragt | [Die Basis bauen](#building-the-base) |
| 11 | TrashStorage | abgefragt | [Die Basis bauen](#building-the-base) |
| 12 | SuccessfulMission | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 13 | FlownMission | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 15 | UnluckyMission | - tut nichts | [Typen, die nichts tun](#types-that-do-nothing) |
| 16 | TakePartInScramble | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 17 | FailedMission | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 18 | ScramblePlaneDestroyed | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 19 | ScrambleToSafety | Ereignis | [Flugzeuge und Missionen](#aircraft-and-missions) |
| 20 | CoveredFunctionArea | abgefragt | [Die Basis bauen](#building-the-base) |
| 21 | PlannedAirstrip | abgefragt | [Die Basis bauen](#building-the-base) |
| 22 | CharacterJob | abgefragt | [Crew](#crew) |
| 23 | QuestDismissed (Button) | Ereignis | [Ein Button auf der Quest-Karte](#a-button-on-the-quest-card) |
| 24 | GardeningZone | abgefragt | [Die Basis bauen](#building-the-base) |
| 25 | StorageAllResourcesEnabled | Ereignis | [Die Basis bauen](#building-the-base) |

Einen Typ 14 gibt es nicht.

### Die Basis bauen { #building-the-base }

| `_type` | Zählt | `_parameter` |
|---|---|---|
| 0 | Fertige, freie Startbahnen mindestens dieser Stufe | Die Stufe als Zahl: `"1"` ... `"5"`. Pflicht. |
| 21 | Startbahnen in jedem Stadium - geplant, im Bau oder fertig -, deren geplante Länge, Breite und Material alle diese Stufe erreichen | Die Stufe als Zahl. Pflicht. |
| 1 | Nutzbare Parkplätze mindestens dieser Größe | Die Größe als Zahl; `"0"` ist jeder Parkplatz. Pflicht. |
| 4 | Fertige Objekte mit einer dieser ids | Objekt-ids, z. B. `"Bed"` oder `"Flagpole5,Flagpole10"`. Geplante oder ungebaute Objekte zählen nicht. |
| 6 | Nutzbare Werkbänke mit einer dieser ids | Werkbank-ids, z. B. `"SawStation"`, `"FieldKitchen"`. |
| 9 | Zonen eines Typs, optional einer Größe | `"<Zone>"`, oder `"<Zone>,<min tiles>"`, oder `"<Zone>,<min>,<max>"`. Zonen: `Airstrip`, `Parking`, `SafetyZone`, `Storage`, `GardeningZone`. Beispiel `"Storage,20"` - eine Lagerzone mit mindestens 20 Feldern. |
| 20 | Zonen, bei denen *jedes* Feld von einem bestimmten Gebäude bedeckt ist | `"<Zone>,<building id>"`, optional `,<min>,<max>` Felder. Beispiel `"Storage,roof_tent"` - eine Lagerzone komplett unter Zeltdach. |
| 10 | 1, wenn mindestens eine Lagerzone Boden **und** Dach über jedem Feld hat, sonst 0 | Leer lassen. Eine Größe hier schränkt nicht ein, welches Lager zählt - sie entscheidet nur, ob die Prüfung überhaupt läuft. Nimm `_amount: 1`. |
| 11 | Lagerzonen, die Müll und Schutt annehmen | Leer - jedes Lager, das Müll und Schutt hereinlässt. `"true"` - nur Lager, die für *nichts außer* Müll und Schutt eingerichtet sind. |
| 25 | Abgeschlossen, wenn jede aufgeführte Ressource in mindestens einer Lagerzone erlaubt ist | Ressourcennamen, z. B. `"GunAmmo,AntiAirAmmo,PlaneBombs"`. Wird neu geprüft, wann immer der Spieler die Einstellungen eines Lagers ändert oder eine Zone platziert. Nimm `_amount: 1`. |
| 24 | Gartenzonen, in denen eine Pflanze für einen Zweck wächst | `"<plant>,<Seeds or Food>"`, optional `,<min tiles>,<max tiles>`. Beispiel `"beans,Food,10"`. Pflanzen-ids sind die aus der Garten-Datentabelle. |

!!! warning "Der eine Fehler, der auch anderen Quests schadet"
    Die Typen 0, 1 und 21 **müssen** eine Zahl in `_parameter` haben, und die Typen 20 und 24 **müssen** ihren zweiten Teil haben (die Gebäude-id bzw. den Zweck `Seeds`/`Food`). Alles andere - auch ein leerer String - ist bei jeder Prüfung des Schritts ein Fehler im Spiel und legt jeden anderen Zustands-Schritt lahm, der im selben Durchgang geprüft wird, bis der Spielstand neu geladen wird.

### Flugzeuge und Missionen { #aircraft-and-missions }

| `_type` | Zählt | `_parameter` |
|---|---|---|
| 2 | Flugzeuge, die der Spieler besitzt | Eine oder mehrere Flugzeug-ids, kommagetrennt - `"spitfire"` oder `"spitfire,hurricane"` - oder leer für jedes Flugzeug. |
| 12 | Flugzeuge, die von einer *erfolgreichen* Mission zurückkamen | Siehe unten. |
| 13 | Flugzeuge, die von irgendeiner Mission zurückkamen, gewonnen oder verloren | Siehe unten. |
| 17 | Flugzeuge, die von einer *gescheiterten* Mission zurückkamen | Siehe unten. |
| 16 | Flugzeuge, die an einem Alarmstart (Scramble) teilgenommen haben | Flugzeug-ids, oder leer für jedes. |
| 18 | Feindliche Flugzeuge, die bei einem Alarmstart abgeschossen wurden | Flugzeug-ids der *verteidigenden* Flugzeuge, die getroffen haben, oder leer für jedes. |
| 19 | Flugzeuge, die sich per Alarmstart in Sicherheit gebracht haben | Flugzeug-ids, oder leer für jedes. |

Die Typen 12, 13, 16, 17, 18 und 19 zählen **pro Flugzeug**, nicht pro Mission. Eine erfolgreiche Mission mit drei Flugzeugen zählt bei einem Typ-12-Schritt drei hoch. Für "flieg eine Mission" lässt du `_amount: 1` stehen und nimmst in Kauf, dass der Schritt abgeschlossen ist, sobald das erste Flugzeug zu Hause ist.

**Filter für 12, 13 und 17.** Ein leerer `_parameter` akzeptiert jedes zurückkehrende Flugzeug. Andernfalls wird die Liste als Sammlung von Wörtern gelesen, und das Flugzeug muss alle davon erfüllen:

| Wort | Typen | Bedeutung |
|---|---|---|
| eine Flugzeug-id - `spitfire`, `blenheim`, ... | alle drei | das zurückkehrende Flugzeug muss eine der aufgeführten ids haben. **Pflicht**, sobald die Liste nicht leer ist - ein Filter ohne Flugzeug-id passt auf nichts. |
| eine Fähigkeit - `fight`, `bomb`, `recon`, `transport`, `maneuverability`, `stealthiness` - oder `any_skill_type` | 12, 17 | die Mission wurde mit dieser Fähigkeit ausgewürfelt. **Eines davon ist Pflicht** bei den Typen 12 und 17. |
| `gone_wrong` | 12, 17 | nur Missionen, die *nicht* nach Plan liefen |
| `location` gefolgt von `land`, `sea`, `ownterritory` oder `enemyterritory` | 12, 13 | der Ort der Mission muss jedes aufgeführte Merkmal haben (siehe [Orte](../missions/locations.md#location-flags)) |
| `low_hp` | 13 | das Flugzeug kam mit einem Viertel seiner Lebenspunkte oder weniger zurück |
| `high_success_rate` | 17 | die Mission scheiterte, obwohl die Prognose über 90 % lag |

Flugzeug-ids sind die erste Spalte der Tabelle `VehicleData`: `gladiator`, `hurricane`, `spitfire`, `meteor`, `mustangmk1`, `vampire`, `beaufighter`, `typhoon`, `tempest`, `kittyhawk`, `blenheim`, `hampden`, `stirling`, `lancaster`, `b17raf`, `mosquito`, `defiant`, `flamingo`, `lysander`.

Beispiele, die in einer normalen Quest funktionieren:

```text
"spitfire,hurricane,any_skill_type"                  type 12 - a Spitfire or Hurricane won any mission
"blenheim,bomb,location,enemyterritory"              type 12 - a Blenheim won a bombing mission over enemy land
"lysander,any_skill_type,gone_wrong"                 type 12 - a Lysander pulled through a mission that went wrong
"spitfire,low_hp"                                    type 13 - a Spitfire limped home
""                                                   type 13 - any aircraft flew any mission
```

!!! note
    Die mitgelieferten Skin-Freischalt-Quests schreiben eine Rolle - `fighter`, `bomber`, `multirole` oder `special` - an die Stelle der Flugzeug-id. Das funktioniert **nur** bei `_questType: 1`, wo das Spiel eine Kopie der Quest pro passendem Flugzeug anlegt und die echte id einsetzt. In einer Quest mit `_questType: 0` passt ein Rollenname auf nichts - führ die Flugzeug-ids auf.

**Auf eine bestimmte Mission warten.** Die Typen 12, 13 und 17 können keine Mission benennen. Nimm stattdessen Typ 7 mit dem Rückkehr-Ereignis der Mission - siehe [Ereignisse](#events):

```json
{ "_type": 7, "_parameter": "airplane_on_mission_succeed,mycampaign_channel_sweep", "_amount": 1 }
```

So folgt eine Quest einer Kette deiner eigenen Missionen, ein Schritt pro Mission.

### Crew { #crew }

| `_type` | Zählt | `_parameter` |
|---|---|---|
| 22 | Lebende, nicht schwer verletzte Crewmitglieder mit einem Beruf | Ein Beruf: `RAFAircrew`, `AAFCook`, `FieldMechanic`, `FieldEngineer`, `RAFMedic`, `AAFLabour`. |

### Ereignisse { #events }

Drei Typen beobachten den Strom der Dinge, die auf der Basis passieren (die kleinen Ereignisse des Spiels, vollständig aufgelistet unter [Ereignisse](../scripting/events.md)). Jeder zählt pro passendem Ereignis eins hoch - mit einer Ausnahme: `resource_gained` trägt die Anzahl der gewonnenen Einheiten und zählt um genau diese Zahl hoch, also bedeutet `"resource_gained,Metal"` mit `_amount: 20` zwanzig Einheiten Metall, nicht zwanzig Lieferungen.

| `_type` | Zählt eins hoch, wenn ... | `_parameter` |
|---|---|---|
| 5 | das genannte Ereignis eintritt, egal mit welchen Details | `"<event>"` |
| 7 | das genannte Ereignis eintritt und **irgendeines** seiner Details einer der aufgeführten Werte ist | `"<event>,<value>,<value>,..."`. Ohne Werte zählt jedes Auftreten. |
| 8 | das genannte Ereignis eintritt und **jeder** aufgeführte Wert unter seinen Details ist | `"<event>,<value>,<value>,..."` |

Typ 7 ist das Arbeitspferd - "ein bestimmtes Gebäude wurde fertig", "eine bestimmte Ressource ist angekommen":

```text
"building_finished,Sickbed"                          a sickbed finished building
"building_finished,Flagpole5,Flagpole10"             either flagpole finished
"building_type_finished,PropSocial"                  any social prop finished
"project_finished,SawStation.Planks"                 planks came off the saw station
"harvesting_finished,tree,tree_big"                  a tree was felled
"resource_gained,Metal"                              metal arrived by any route - harvest, workbench, delivery
"shipment_received,Bofors40mm"                       a shipment containing a Bofors gun arrived
"assigned_to_equipment,Bofors40mm"                   someone was posted to a Bofors gun
"airplane_on_mission_succeed,mycampaign_sweep"       your mission "mycampaign_sweep" came back a success
```

Typ 8 grenzt auf Kombinationen ein und wird selten gebraucht:

```text
"project_finished,SawStation,SawStation.Planks"      planks finished, and at a saw station
"harvesting_finished,bs_owen_m,tree"                 one particular crew member felled a tree
```

Typ 8 hat zwei Grenzen, die Typ 7 nicht hat. Er vergleicht die aufgeführten Werte mit den Details des Ereignisses **nur als Text**: Details, die Namen sind (Crew-ids, Gebäude-ids, Projekt-ids, Missions-ids), passen, aber Details, die das Spiel als Zahlen oder Typen führt - die Ressource von `harvesting_finished` und `resource_gained`, die Kategorie von `building_type_finished`, die Zone von `function_area_placed` - passen nie. Nimm dafür Typ 7. Und ein Typ-8-Schritt mit aufgeführten Werten auf einem Ereignis, das gar keine Details trägt (`victory_points_added`, `quest_dismissed`), ist bei jedem Auftreten dieses Ereignisses ein Fehler. Wenn ein Wert reicht, nimm Typ 7.

Ereignisse, die im normalen Spiel verfügbar sind, mit den Details, die jedes trägt:

| Ereignis | Details |
|---|---|
| `building_started`, `building_finished`, `deconstruction_finished` | Arbeiter, Gebäude-id (z. B. `Sickbed`, `roof_concrete`, `wall_tent`) |
| `building_type_finished` | Arbeiter, Gebäudekategorie (z. B. `PropSocial`, `PropPosters`) |
| `project_started`, `project_finished` | Arbeiter, Werkbank-id, Projekt-id (als `SawStation.Planks`) |
| `harvesting_started`, `harvesting_finished` | Arbeiter, geerntetes Objekt (z. B. `tree`, `tree_big`, `berry_bush`), Ressource |
| `resource_gained` | Ressourcenname |
| `resource_picked_up`, `resouce_consumed` | Crewmitglied, Ressourcenname (das zweite wird im Spiel wirklich so geschrieben) |
| `shipment_received` | die ids in der Lieferung |
| `victory_points_added` | - |
| `assigned_to_equipment` | Crewmitglied, Ausrüstungs-id |
| `training_started`, `training_finished` | Crewmitglied, Trainingsobjekt |
| `task_started`, `task_completed` | Crewmitglied, Aufgabenname (z. B. `Harvest`, `Build`, `Repair`, `RepairAirplane`, `Refuel`, `Recover`) |
| `chat_started`, `chat_finished` | die beiden Crewmitglieder |
| `mission_started`, `mission_success`, `mission_failed` | die Orts-ID der Mission |
| `airplane_on_mission_succeed`, `airplane_on_mission_failed` | Flugzeug-id, Flugzeug, **Missions-id**, Fähigkeit, nach Plan gelaufen, Orts-ID, Prognose |
| `airplane_took_part_in_scramble`, `airplane_scramble_fly_to_safety`, `airplane_scramble_airplane_destroyed` | Flugzeug-id |
| `plane_takeoff`, `plane_landing` | die interne Nummer des Flugzeugs (nicht seine id - hier kannst du nicht nach `spitfire` filtern), Pilot |
| `storage_resource_enabled`, `function_area_placed` | Ressourcenname / Zonentyp |
| `day_phase_change` | vorherige Phase, aktuelle Phase |
| `midnight`, `midday` | Jahr, Monat, Tag |
| `sub_quest_completed` | der `_subQuestTitle`-Schlüssel des abgeschlossenen Schritts - eine Quest kann auf einen Schritt einer anderen Quest warten |
| `quest_dismissed` | - |
| `dog_sleep`, `dog_walk_started`, `dog_walk_finished`, `dog_sniff_wait` | der Hund |

!!! warning "Ereignisse nur im Tutorial"
    Eine zweite Gruppe von Ereignissen gibt es **nur, solange das Tutorial läuft**: `camera_moved`, `camera_zoomed`, `camera_rotated`, `character_selected`, `task_created`, `tooltip_shown`, `preview_created`, `building_placed`, `state_entered`, `time_scale_changed`, `window_opened`, `character_job_assigned`, `day_phase_ended`, `plane_ordered`, `plane_selected`, `plane_assigned_to_mission`, `shipment_item_added`, `scramble_started`, `attack_finished`, `storage_resource_disabled`, `button_clicked`, `plane_back_from_mission`, `hour_changed`, `workbench_selected`, `project_planned`.

    Die mitgelieferten Tutorial-Quests nutzen sie ausgiebig, was dazu verleitet, sie zu kopieren. Außerhalb des Tutorials sind sie abgeschaltet, und ein Schritt, der auf eines davon wartet, bewegt sich nie. Nimm lieber `building_finished` statt `building_placed` und `airplane_on_mission_succeed` statt `plane_back_from_mission`.

### Ein Button auf der Quest-Karte { #a-button-on-the-quest-card }

| `_type` | Abgeschlossen, wenn ... | `_parameter` |
|---|---|---|
| 23 | der Spieler den Button anklickt, den dieser Schritt auf die Quest-Karte setzt | Der Lokalisierungsschlüssel der Button-Beschriftung, z. B. `"basic_ui/ok"` oder `"basic_ui/start"`. |

Der Button erscheint auf der Quest-Karte der Quest, zu der der Schritt gehört. Beachte, dass *jeder* solche Button auf *jeder* Quest alle gerade offenen Typ-23-Schritte weiterschaltet - halte dich also an einen zur Zeit. Mit leerem `_parameter` wird kein Button gezeichnet, aber der Schritt wird trotzdem abgeschlossen, wenn ein Button auf einer anderen Quest angeklickt wird.

### Typen, die nichts tun { #types-that-do-nothing }

`_type: 3` und `_type: 15` stehen in alten Dateien, haben aber keine Logik dahinter; ein Schritt mit einem davon kommt nie voran, und nichts wird [geloggt](../start/troubleshooting.md#find-the-playerlog). Dasselbe gilt für jede Zahl, die nicht in der Tabelle steht. Wenn ein Schritt ewig bei null steht, prüf zuerst seinen `_type`.

## Wie eine Quest startet { #how-a-quest-starts }

`_requirements` entscheidet, *wann die Quest dem Spieler gegeben wird*. Mit Fortschritt hat das nichts zu tun. Alle Einträge müssen erfüllt sein (sie sind mit UND verknüpft), und die Prüfung läuft jedes Mal, wenn irgendeine Quest abgeschlossen wird - geprüft werden nur Quests mit einem Eintrag vom Typ 1.

| `_requirementType` | Name | Bedeutung | `_value` |
|---|---|---|---|
| 0 | None | Keine Bedingung. | `""` |
| 1 | CompletedQuestId | Startet, sobald die genannte Quest abgeschlossen ist. | die id der anderen Quest |
| 2, 3 | MinimumDate, MapDependent | **Entfernt.** Der Eintrag wird übersprungen, die Quest verhält sich also, als wäre er nicht da. Nicht verwenden. | |

Eine Quest erreicht den Spieler nur auf einem von drei Wegen:

- die geladene Karte führt sie in ihren `StartingQuestIds` auf - siehe [Quests und Karten](#quests-and-maps);
- sie hat einen Eintrag vom Typ 1, und die genannte Quest wird abgeschlossen;
- sie ist eine Flugzeug-Skin-Quest (`_questType: 1`), die auf jeder Karte vergeben wird.

Eine Quest mit **leerer Liste**, die keine Karte aufführt, startet nie.

Eine **Kette** ist eine Reihe von Quests, von denen jede die vorige voraussetzt:

```json
"_requirements": [
    { "_requirementType": 1, "_value": "mycampaign_first_steps" }
]
```

Eine Quest wird pro Durchgang höchstens einmal vergeben - sobald sie im Spielstand existiert, abgeschlossen oder nicht, wird sie nicht erneut erzeugt, und eine abgeschlossene Quest bleibt abgeschlossen. Eine Kette folgt ihrem ersten Glied: Nur die erste Quest muss in der Liste der Karte stehen, der Rest folgt über Bedingungstyp 1, und auf einer Karte, die die erste Quest nicht aufführt, bleibt die ganze Kette fern.

### Quests und Karten { #quests-and-maps }

Jede Karte nennt die Quests, die sie startet, in der `Metadata.json` in ihrer `.goamap`-Datei:

```json
"StartingQuestIds": ["mycampaign_first_steps"]
```

Diese Quests werden beim Laden der Karte vergeben, egal was ihre `_requirements` sagen. Eine Karte, die keine nennt - eine ältere Karte oder eine, deren Feld leer geblieben ist -, startet die Standard-Questreihe des Spiels, `quest0`, damit keine Karte je ohne Quests ist.

Die mitgelieferte `quest0` hat keine Bedingungen, und jede spätere `questN` setzt die vorige voraus. Sobald eine Karte also *deine* Quest statt `quest0` aufführt, bleibt die komplette mitgelieferte Hauptreihe dieser Karte fern - und genau das will eine Kampagne meistens. Wenn du beides willst, führ beides auf: `["quest0", "mycampaign_first_steps"]`.

Damit eine Quest zu einer Karte gehört, trag ihre id in `StartingQuestIds` dieser Karte ein und lass ihre `_requirements` leer. Keine andere Karte startet sie.

!!! note "Missionen nutzen Tags, Quests nicht"
    Missionen hängen über **Tags** an Karten (das Feld `_tags`, siehe [Missionen](../missions/index.md)). Quests nicht: Eine Quest hat kein Tags-Feld, und die Liste `StartingQuestIds` der Karte ist alles, was zählt. Die beiden Mechanismen sind unabhängig voneinander - eine Kampagnenkarte nutzt typischerweise beide, Tags für ihre Missionen und `StartingQuestIds` für ihre Quests.

**Die Liste der Karte im Spiel bearbeiten.** Öffne die Karte im Karten Editor (Map Editor) und such in den Karteneinstellungen das Feld *Starting quest*, neben den Tags. Gib die Quest-ids durch Kommas getrennt ein - `quest0, mycampaign_first_steps` - und speichere die Karte. Karten, die du so speicherst, landen in deinem Ordner `Maps` (neben dem Ordner `Mods`); kopier die `.goamap` in den Ordner `Maps/` deiner Mod, um sie mitzuliefern. Eine Karte, die schon in einem Mod-Ordner liegt, kann aus dem Editor nicht überschrieben werden - bearbeite die Kopie in `Maps` und ersetze dann die in der Mod. Mehr zu Karten: [Karten](../content/maps.md).

**Die Liste in einem Texteditor bearbeiten.** Eine `.goamap` ist ein ganz normales Zip-Archiv mit anderer Dateiendung. Öffne sie mit einem beliebigen Archivprogramm, bearbeite `Metadata.json` und pack sie unter demselben Namen zurück. Alles andere im Archiv bleibt, wie es ist. `StartingQuestIds` steht am Ende der Datei, neben `_tags`; füg den Schlüssel hinzu, falls er fehlt.

Eine id in der Liste, für die es keine Quest-Datei gibt, wird im veröffentlichten Spiel ohne Meldung übersprungen; die Karte lädt trotzdem.

## Eine mitgelieferte Quest ändern { #changing-a-shipped-quest }

Um eine Quest zu ändern, die das Spiel mitbringt, leg eine Datei mit **demselben Namen** in den Ordner `Quests/` deiner Mod. Deine Kopie ersetzt die mitgelieferte vollständig, also starte mit einer vollständigen Kopie des Originals und ändere, was du brauchst: einen `_amount`, einen `_parameter`, einen Schritt optional machen, einen Schritt hinzufügen oder entfernen.

Die mitgelieferten Dateien sind einfaches JSON im Installationsordner des Spiels, unter `Ground Of Aces_Data/StreamingAssets/Scripts/Quest/` (auf macOS: `Ground of Aces.app/Contents/Resources/Data/StreamingAssets/Scripts/Quest/`) - `quest0` bis `quest14`, die `tutorial_*`-Quests und die `*_skin_unlock`-Quests. Kopier sie von dort; bearbeite sie nie direkt, denn ein Spiel-Update überschreibt diesen Ordner. Die mitgelieferten Karten liegen gleich daneben in `StreamingAssets/Maps/` - dort findest du auch eine echte `Metadata.json` zum Anschauen.

Änderungen erreichen auch **bestehende Spielstände**. Beim Laden eines Spielstands wird jede Quest darin mit der aktuellen Datei verglichen: Schritt-Titel, Schritt-Beschreibungen, Bedingungstypen, Parameter und Mengen werden an Ort und Stelle aktualisiert, neue Schritte werden angehängt, entfernte Schritte gelöscht, und ein Schritt, dessen Fortschritt die neue Menge schon erreicht, wird sofort abgeschlossen. Schritte werden **nach Position** zugeordnet, ein Schritt in der Mitte verschiebt also in einem laufenden Spielstand die Bedeutung aller folgenden - häng neue Schritte ans Ende, wenn eine Quest schon im Umlauf ist. Nicht aktualisiert werden in einem laufenden Spielstand: `_questTitle`, `_questDescription` und `_isHiddenInUI` der Quest selbst sowie `_isOptional` und `_genericIconKey` eines Schritts - die werden festgelegt, wenn die Quest zum ersten Mal vergeben wird.

## Quest-Typen { #quest-types }

`_questType: 0` ist eine normale Quest und genau die, die du willst. Die anderen beiden gibt es für die eigenen Inhalte des Spiels, und beide haben einen Haken.

**Tutorial-Quests (`2`)** lassen zusätzlich die Tutorial-Hervorhebung nacheinander auf die Buttons in `_highlightedUIElements` zeigen und können Konsolenbefehle aus `_cheatsOnStart` und `_completionCheats` ausführen. In einer Mod gilt:

- Die **Befehle werden entfernt**. Eine Mod-Quest mit einer dieser Listen lädt trotzdem, aber die Listen werden ignoriert (Entwickler-Builds schreiben eine Warnung ins [Log](../start/troubleshooting.md#find-the-playerlog)), und nichts wird ausgeführt.
- Die Hervorhebungs-ids sind eine feste Liste im Spiel - die ids in den mitgelieferten Tutorial-Quests (`SawStation`, `Sickbed`, `ParkingSmall`, `CrewRoleDropdown`, ...) sind das Vokabular. Eine unbekannte id bewirkt nichts.
- Die Ereignisse nur im Tutorial (siehe [Ereignisse](#events)) treten nur auf, solange das Tutorial selbst läuft, und das kann nur der Spieler einschalten (das Häkchen im Fenster für ein neues Spiel), keine Mod.

**Flugzeug-Skin-Quests (`1`)** werden einmal pro Flugzeug angelegt, dessen Rolle oder id im `_parameter` des ersten Schritts steht, und die id des Flugzeugs wird an den Parameter jedes Schritts angehängt. Beim Abschluss schalten sie einen Skin frei - aber *welchen* Skin, steht in einer Tabelle im Spiel, die nach den mitgelieferten Quest-ids sortiert ist. Eine neue Quest dieses Typs schaltet also nichts frei.

Dieselbe Tabelle sorgt dafür, dass der Abschluss von `quest2` neue Gebäude freischaltet: **Belohnungen sind nicht Teil der Quest-Datei**. Eine Mod-Quest kann kein Gebäude, kein Flugzeug und keinen Skin freischalten. Was sie kann, ist *sperren*: Bedingungstyp 1 reiht Quests hintereinander, und ein Quest-Schritt kann auf eine Missionskette warten. Umgekehrt geht es nicht - eine Mission kann über Karten-Tags, Startbahnstufe, ein Tagesfenster oder eine *abgeschlossene Mission* gesperrt werden, aber nicht über eine Quest (siehe [Missionen](../missions/index.md)).

## Beispiel-Quests { #example-quests }

Drei vollständige Quest-Dateien zum Öffnen, Kopieren und Ändern. Sie liegen im Modkit-Repository als kleine Mod: [examples/quests](https://github.com/blindflugstudios/goa-modkit/tree/main/examples/quests) (die Dateien selbst sind in dessen Ordner `Quests/`). Jede kommt unter ihrem Dateinamen in `Mods/<your mod>/Quests/`; die Titel sind Lokalisierungsschlüssel, denen du wie unter [Text](#text) beschrieben Worte gibst.

| Datei | Was sie zeigt |
|---|---|
| `example_first_steps.json` | Die Quest aus [Eine erste Quest](#a-first-quest): ein Pflichtschritt, der auf ein fertiges Krankenbett wartet, ein optionaler Schritt, der Betten zählt. Startet auf jeder Karte, die sie in `StartingQuestIds` aufführt. |
| `example_patrol_chain.json` | Eine Folgequest. Sie startet, sobald `example_first_steps` abgeschlossen ist, wartet darauf, dass eine Spitfire im Besitz ist, dann darauf, dass die mitgelieferte Mission `calm_supply_drop` erfolgreich zurückkommt, und zählt optional drei gewonnene Einsätze von Spitfires oder Hurricanes. `calm_supply_drop` taucht erst ab Tag 20 mit einer Startbahn der Stufe 3 auf, der Missionsschritt kann also vorher nicht vorankommen. |
| `example_map_campaign.json` | Eine Quest, die zu einer Karte gehört: Sie hat keine Bedingungen, und nur diese Karte führt sie in `StartingQuestIds` auf (siehe [Quests und Karten](#quests-and-maps)). Ihre Schritte nutzen die Zustands-Typen: eine Startbahn der Stufe 1, zwei Parkplätze, eine Lagerzone mit zwanzig Feldern. |

Installier alle drei zusammen, und du hast eine Kette aus zwei Quests plus eine kartengebundene Quest zum Vergleichen. Benenn die ids um, bevor du darauf aufbaust - `example_` ist nur ein Platzhalter-Präfix.

Hier die verkettete Quest vollständig:

```json
{
    "_questId": "example_patrol_chain",
    "_questTitle": "example/patrol_chain/title",
    "_questDescription": "example/patrol_chain/description",
    "_subQuests": [
        {
            "_subQuestTitle": "example/patrol_chain/step0_title",
            "_subQuestDescription": "example/patrol_chain/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 2,
                "_parameter": "spitfire",
                "_amount": 1
            },
            "_genericIconKey": "ui_plane"
        },
        {
            "_subQuestTitle": "example/patrol_chain/step1_title",
            "_subQuestDescription": "example/patrol_chain/step1_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 7,
                "_parameter": "airplane_on_mission_succeed,calm_supply_drop",
                "_amount": 1
            },
            "_genericIconKey": "ui_plane"
        },
        {
            "_subQuestTitle": "example/patrol_chain/step2_title",
            "_subQuestDescription": "",
            "_isOptional": true,
            "_subQuestRequirement": {
                "_type": 12,
                "_parameter": "spitfire,hurricane,any_skill_type",
                "_amount": 3
            },
            "_genericIconKey": "ui_plane"
        }
    ],
    "_requirements": [
        {
            "Name": "",
            "_requirementType": 1,
            "_value": "example_first_steps"
        }
    ],
    "_isHiddenInUI": false,
    "_questType": 0,
    "_highlightedUIElements": [],
    "_cheatsOnStart": [],
    "_completionCheats": []
}
```

Und die kartengebundene:

```json
{
    "_questId": "example_map_campaign",
    "_questTitle": "example/map_campaign/title",
    "_questDescription": "example/map_campaign/description",
    "_subQuests": [
        {
            "_subQuestTitle": "example/map_campaign/step0_title",
            "_subQuestDescription": "example/map_campaign/step0_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 0,
                "_parameter": "1",
                "_amount": 1
            },
            "_genericIconKey": "ui_path_runway"
        },
        {
            "_subQuestTitle": "example/map_campaign/step1_title",
            "_subQuestDescription": "example/map_campaign/step1_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 1,
                "_parameter": "0",
                "_amount": 2
            },
            "_genericIconKey": "ui_functionarea_parking"
        },
        {
            "_subQuestTitle": "example/map_campaign/step2_title",
            "_subQuestDescription": "example/map_campaign/step2_description",
            "_isOptional": false,
            "_subQuestRequirement": {
                "_type": 9,
                "_parameter": "Storage,20",
                "_amount": 1
            },
            "_genericIconKey": "ui_functionarea_resources"
        }
    ],
    "_requirements": [],
    "_isHiddenInUI": false,
    "_questType": 0,
    "_highlightedUIElements": [],
    "_cheatsOnStart": [],
    "_completionCheats": []
}
```

## Mitgelieferte Quests { #shipped-quests }

Auch die Quest-Dateien des Spiels selbst lohnen einen Blick: Sie zeigen, wie das Original aussieht. Du findest sie im Installationsordner, wie unter [Eine mitgelieferte Quest ändern](#changing-a-shipped-quest) beschrieben. Denk daran: Eine Mod-Datei mit demselben Namen **ersetzt** die mitgelieferte Quest. Benenne deine Kopie also um, bevor du sie änderst.

| Datei | Was sie zeigt |
|---|---|
| `quest0.json` | Die erste Quest der Hauptreihe: keine Bedingungen, sie startet also nur auf Karten, die sie in `StartingQuestIds` aufführen (oder gar keine Start-Quest nennen). Ihre Schritte sind die Typen mit gezähltem Zustand - eine Startbahn der Stufe 1, ein Parkplatz, eine Gladiator, Betten. |
| `quest1.json` | Die zweite Quest, mit Bedingungstyp 1 an `quest0` gehängt. Sie mischt Event-Schritte (`harvesting_finished`, `project_finished`) mit einer Werkbank-Zählung und hat einen optionalen Schritt. |
| `fighter_day_skin_unlock.json` | Eine Errungenschaft für eine Flugzeug-Lackierung: `_questType: 1`, im Quest-Panel versteckt, und die einzige Stelle, an der ein Rollenname (`fighter`) dort stehen darf, wo sonst eine Flugzeug-Id steht - siehe [Quest-Typen](#quest-types). |
| `tutorial_building.json` | Eine Tutorial-Quest: `_questType: 2` mit `_highlightedUIElements`, die den Spieler auf die Oberfläche hinweisen, solange die Schritte offen sind. |

## Eine Quest testen { #testing-a-quest }

Lade nach jeder Änderung erneut ein Level (ein neuer Ordner braucht zuerst **Refresh** im Mods-Fenster), und nutze dann die [Cheat-Konsole](../basics/cheats.md):

| Befehl | Wirkung |
|---|---|
| `quest <id>` | Vergibt die Quest sofort, egal was ihre Bedingungen oder die Karte sagen. Die Konsole schlägt beim Tippen geladene Quest-ids vor - wird deine nie vorgeschlagen, wurde die Datei nicht gelesen. Zweimal ausgeführt entsteht eine zweite Kopie der Quest. |
| `complete_current_quests` | Schließt jede offene normale Quest ab, sodass die nächsten Glieder einer Kette starten. |
| `go_to_quest <id>` | Schließt jede Quest ab, die die genannte voraussetzt (über Bedingungstyp 1, die Kette rückwärts entlang), sodass die genannte Quest vergeben wird. Die genannte Quest selbst wird nicht abgeschlossen, und es funktioniert auch mit Mod-Quests. |
| `start_shipment <Resource> <amount> ...` | Bringt Ressourcen auf die Basis - `start_shipment Wood 12`. |
| `create_mission <mission id>` | Setzt eine Mission auf die Karte, um einen Missions-Rückkehr-Schritt zu testen. |

Wenn eine Quest nicht auftaucht oder ein Schritt sich nicht bewegt, lies die [Log](../start/troubleshooting.md#find-the-playerlog)-Datei des Spiels, `Player.log`.

- Eine Quest-Datei mit ungültigem JSON (ein fehlendes Komma, eine offene Klammer) wird **nicht** übersprungen - sie macht das Laden des Levels kaputt. Prüf dein JSON in einem Editor, bevor du testest.
- Eine Karte, die eine unbekannte Quest-id aufführt, und ein Schritt, der wegen eines falschen `_type` oder einer falsch geschriebenen id nie vorankommt, bekommen **keine** Zeile im [Log](../start/troubleshooting.md#find-the-playerlog) - prüf die Tabellen oben.

Mehr Tipps zum Testen: [Testen und neu laden](../basics/testing.md).

### Checkliste vor der Veröffentlichung { #checklist-before-you-ship }

- Gültiges JSON: Jedes `{` und `[` ist geschlossen, zwischen Einträgen steht ein Komma und nach dem letzten keins.
- Der Dateiname entspricht `_questId`, und beide tragen das Präfix deiner Mod.
- Jeder `_amount` ist mindestens 1.
- Die Typen 0, 1 und 21 haben eine Zahl in `_parameter`; die Typen 20 und 24 haben ihren zweiten Teil.
- Die Typen 12 und 17 enthalten eine Fähigkeit oder `any_skill_type`; jeder nicht leere Typ 12, 13 oder 17 enthält mindestens eine Flugzeug-**id**.
- Kein Tutorial-Ereignis außerhalb eines Tutorials.
- Kein `_requirementType: 2` oder `3`.
- Jede Quest ohne Bedingung vom Typ 1 steht in den `StartingQuestIds` jeder Karte, auf der sie laufen soll.
- Jeder Lokalisierungsschlüssel ist entweder ein mitgelieferter Schlüssel oder von deinem Skript registriert - lade das Spiel und schau in die Leiste.
- Keine Leerzeichen in `_parameter`.

## Spielstände und das Entfernen einer Mod { #saves-and-removing-a-mod }

Eine vergebene Quest lebt im Spielstand - Name, Fortschritt und Bedingung -, unabhängig von deiner Datei. Speichern und Laden mit installierter Mod läuft unauffällig. Eine Quest, die du mit einem Update *hinzufügst*, erscheint in bestehenden Spielständen beim nächsten Laden, sofern ihre Bedingungen erfüllt sind.

**Entfernst du die Mod, bleibt die Quest im Spielstand**, weiterhin sichtbar, eingefroren an der Stelle, wo sie war. Nichts entfernt eine Quest, nur weil ihre Datei fehlt, und der Text, den dein Skript registriert hat, verschwindet mit dem Skript, also zeigt die Karte die nackten Schlüssel. Schritte, die auf deine Missionen warten, können sich nie mehr bewegen, weil es diese Missionen nicht mehr gibt. Legst du die Mod zurück, ist alles wieder da - Text, Fortschritt, keine Duplikate.

Für den Spieler heißt das: Eine Quest, die man abschließen kann, hinterlässt einen sauberen Spielstand; eine, die ihn mitten in einer Kette hängen lässt, nicht - und dagegen kann er im Spiel nichts tun. Bevorzuge Quests, die ein Ende erreichen, und behandle das Entfernen einer Quest aus einer veröffentlichten Mod als inkompatible Änderung für alle, die gerade mitten in einem Durchgang stecken.

## Was eine Quest nicht kann { #what-a-quest-cannot-do }

- **Eine neue Bedingung erfinden.** Die Typen in der Tabelle sind alles. Wenn das, was du zählen willst, nicht dabei ist, lässt es sich nicht ausdrücken - aber ein Skript kann darauf achten und eine Mission vergeben, und eine Quest kann auf die Rückkehr dieser Mission warten.
- **Logik ausführen.** Kein Python, keine Verzweigungen, kein Auslesen des Spielzustands über die Zähler oben hinaus.
- **Text ohne Schlüssel anzeigen.** Siehe [Text](#text).
- **Eine Belohnung vergeben.** Siehe [Quest-Typen](#quest-types).
- **Innerhalb eines laufenden Levels neu laden.** Änderungen zeigen sich nach dem nächsten Laden eines Levels.

Für alles, was etwas *entscheiden* muss, nimm eine Mission oder ein Ereignis-Skript (siehe [Missionen](../missions/index.md) und [Skripting](../scripting/index.md)) und lass die Quest anzeigen, wie weit der Spieler gekommen ist.
