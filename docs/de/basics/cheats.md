# Cheat-Konsole

Die Cheat-Konsole ist ein kleines Befehlsfenster im Spiel. Für Modder ist sie der schnellste Weg zum Testen: Erstelle deine Mission sofort, statt tagelang auf sie zu warten, spring zu der Quest, an der du gerade arbeitest, oder spul die Zeit vor.

## Einschalten und öffnen { #switch-it-on-and-open-it }

1. Lade einen Spielstand oder starte ein Spiel. Die Konsole funktioniert nur, während ein Spiel läuft.
2. Öffne **Einstellungen** (Options) und schalte **Cheats** ein.
3. Auf dem Spielbildschirm erscheint ein Cheat-Button. Klick darauf, um die Konsole zu öffnen.

<!-- screenshot: Options window with the Cheats toggle, and the cheat button on the game screen -->

Tipp einen Befehl in das Feld **Cheat eingeben...** (Enter cheat...) und drück **Enter**. Die Antwort erscheint über dem Feld.

| Taste | Wirkung |
|---|---|
| **Enter** | Führt den Befehl aus |
| **Tab** | Vervollständigt den Befehlsnamen und bei vielen Befehlen auch das nächste Argument (Missions-Ids, Quest-Ids, Ressourcen ...) |
| **Hoch / Runter** | Blättert durch die Befehle, die du vorher eingegeben hast |

Tipp `help` für die vollständige Liste mit einem Beispiel zu jedem Befehl, oder `help create_mission` für einen einzelnen Befehl. Bei Befehlsnamen spielt Groß- und Kleinschreibung keine Rolle.

!!! warning "Cheats verändern deinen Spielstand"
    Was ein Cheat bewirkt, wird mit deinem Spiel gespeichert. Teste Mods auf einem Ersatz-Spielstand, nicht auf deiner Lieblingskampagne.

!!! note "Deine Mod neu laden ist kein Konsolenbefehl"
    Nach einer Änderung an einer Mod: **Einstellungen → Verlassen zum Hauptmenü**, dann deinen Spielstand laden (wenn du einen neuen Mod-Ordner angelegt hast, drück vorher im Fenster **Mods** auf **Refresh**). Auch Quests werden dabei neu eingelesen, nur Modelle und Texturen brauchen einen kompletten Neustart - und Grafik-Mods sind noch in Arbeit und werden von der aktuellen Alpha noch nicht unterstützt. Siehe [Testen und neu laden](testing.md).

## Die Befehle { #the-commands }

Argumente in `[eckigen Klammern]` sind Platzhalter: Ersetze sie, ohne die Klammern. Mit ★ markierte Befehle wirst du beim Testen von Mods am häufigsten brauchen.

### Missionen und Quests { #missions-and-quests }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| ★ | `create_mission [mission_id]` | Erstellt diese Mission sofort, sodass sie ohne Wartezeit auf der Kriegskarte erscheint. Antwortet mit `Unknown mission ID`, wenn das Spiel sie nicht geladen hat. | `create_mission coastal_patrol` |
| ★ | `quest [quest_id]` | Startet die Quest mit dieser Id. | `quest quest3` |
| ★ | `go_to_quest [quest_id]` | Schließt Quests nacheinander ab, bis diese Quest erreicht ist. | `go_to_quest quest5` |
| ★ | `complete_current_quests` | Schließt die laufenden Quests ab (keine Tutorial- oder Skin-Quests). | `complete_current_quests` |
| | `enable_tutorial [true/false]` | Schaltet das Tutorial ein oder aus. | `enable_tutorial false` |
| | `set_game_goals_visibility [ShowAll/ShowPriority/Minimized]` | Ändert, wie die Zielanzeige dargestellt wird. | `set_game_goals_visibility ShowAll` |

### Zeit und Tage { #time-and-days }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| ★ | `skip_day` | Springt zum nächsten Tag. Praktisch für Missionen mit Mindesttag. | `skip_day` |
| ★ | `set_day [day of week] [hour] [minute]` | Springt zu einem Tag der aktuellen Woche. | `set_day Friday` |
| | `go_to_day_phase [Work/Leisure/Sleep]` | Springt zum Beginn der nächsten Tagesphase. Das friert auch die Uhr ein: Lass danach `freeze_time off` folgen. | `go_to_day_phase Leisure` |
| | `force_day_phase [Work/Leisure/Sleep/off]` | Hält die Basis in einer Tagesphase, bis du `off` übergibst. | `force_day_phase Work` |
| | `freeze_time [hour] [minute]` | Hält die Tageszeit fest, während die Tage weiterzählen. `off` hebt das auf. | `freeze_time 12 0` |

### Basis, Rang und Freischaltungen { #base-rank-and-unlocks }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| ★ | `list_airstrips` | Listet deine Start- und Landebahnen und ihre Ids auf. | `list_airstrips` |
| ★ | `set_airstrip_tier [airstrip_id] [tier]` | Setzt die Stufe einer Landebahn. Missionen können eine bestimmte Landebahnstufe verlangen. | `set_airstrip_tier [id] 2` |
| ★ | `set_all_airstrips_tier [tier]` | Setzt die Stufe aller Landebahnen. | `set_all_airstrips_tier 3` |
| ★ | `set_air_base_rank [rank]` | Setzt den Rang des Flugplatzes. | `set_air_base_rank 2` |
| | `set_victory_points [amount]` | Setzt deine Siegpunkte. | `set_victory_points 50` |
| | `unlock [id]` | Schaltet einen Eintrag per Id frei. Tab schlägt Ids vor. | `unlock [id]` |
| | `unlock_all_skins` | Schaltet alle Flugzeug-Skins frei. | `unlock_all_skins` |
| | `add_resource_pile [resource] [x] [y] [true/false]` | Legt einen unendlichen Stapel einer Ressource am Mauszeiger oder an einer Kartenposition ab. Übergib zuletzt `false` für einen normalen Stapel. | `add_resource_pile Tarp 10 30 false` |
| | `start_shipment [type] [amount] ...` | Schickt einen Lieferwagen. Ohne Argumente bringt er die Lieferung, die im HQ-Fenster eingestellt ist. | `start_shipment Tarp 20` |
| | `storage_blacklist_override [true/false]` | Wenn eingeschaltet, blockieren Lager standardmäßig alle Ressourcen. | `storage_blacklist_override false` |
| | `enable_crates_interaction [true/false]` | Erlaubt oder verbietet das Ernten und Abbauen von Kisten. | `enable_crates_interaction true` |
| | `enable_equipment_deconstruction [true/false]` | Erlaubt oder verbietet das Abbauen von Ausrüstung. | `enable_equipment_deconstruction true` |
| | `set_growing_time [hours] [x] [y]` | Setzt die verbleibende Wachstumszeit einer Pflanze unter dem Mauszeiger oder an einer Position. | `set_growing_time 1` |
| | `fill_grave` | Füllt ein zufälliges leeres Grab. | `fill_grave` |

### Flugzeuge { #planes }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| ★ | `spawn_plane [plane_id] [x] [y]` | Fügt ein neues Flugzeug mit Pilot hinzu. Ohne Position kommt es zur Landung herein. | `spawn_plane [plane_id]` |
| | `set_airplane_fuel [0-100]` | Setzt den Treibstoff. | `set_airplane_fuel 100` |
| | `set_airplane_health [0-100]` | Setzt die Gesundheit des Flugzeugs. | `set_airplane_health 100` |
| | `set_airplane_integrity [0-100]` | Setzt die strukturelle Integrität des Flugzeugs. | `set_airplane_integrity 100` |
| | `destroy_airplane [airplane_id]` | Entfernt ein Flugzeug. | `destroy_airplane [id]` |
| | `plane_fire` | Setzt ein zufälliges Flugzeug in Brand. | `plane_fire` |
| | `spawn_plane_crash [airplane_id]` | Spielt einen Absturz für dieses Flugzeug ab. | `spawn_plane_crash [id]` |
| | `landing_queue_event [Wobbly/Overshoot/Smoked/Burning/Crash]` | Das nächste ankommende Flugzeug landet mit diesem Ereignis. | `landing_queue_event Wobbly` |
| | `set_max_scramble_damage [amount]` | Begrenzt den Schaden, den ein Alarmstart-Flugzeug nehmen kann. | `set_max_scramble_damage 10` |

### Crew und Moral { #crew-and-morale }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| ★ | `deliver_crew [count] [Male/Female]` | Schickt einen Lastwagen mit neuer Crew (Standard 2). | `deliver_crew 4` |
| | `spawn_character [role] [male/female] [true/false] [x] [y]` | Erzeugt ein Crewmitglied am Mauszeiger oder an einer Position. Die Rolle ist eine Flugzeugbesatzungsrolle oder `none` für Bodenpersonal. | `spawn_character none female` |
| | `set_crew_morale [Confidence/Mood/Energy] [-100..100]` | Setzt einen Moralwert für alle. Nur mit einer Zahl werden alle Werte gesetzt. `random` verteilt sie zufällig. | `set_crew_morale Confidence 100` |
| | `freeze_morale [true/false]` | Verhindert, dass sich die Moral ändert. | `freeze_morale true` |
| | `set_morale_flag [add/sub] [flag] [character_id]` | Fügt einem Crewmitglied ein Moral-Flag (happy, sad, angry ...) hinzu oder entfernt es. | `set_morale_flag add [flag] [id]` |
| | `set_crisis [Confidence/Mood/Energy] [character_id]` | Schickt ein Crewmitglied in eine Krise: Panik, Wut oder Erschöpfung. | `set_crisis Confidence [id]` |
| | `set_character_health [character_id] [health]` | Setzt die Gesundheit eines Crewmitglieds. | `set_character_health [id] 100` |
| | `set_invulnerable_characters [true/false]` | Die Crew nimmt keinen Schaden. | `set_invulnerable_characters true` |
| | `injure_random_character [count]` | Verletzt zufällige Crewmitglieder schwer. | `injure_random_character 1` |
| | `character_fire [count]` | Setzt zufällige Crewmitglieder in Brand. | `character_fire 1` |
| | `poison` | Gibt zufälligen Crewmitgliedern eine Pilzvergiftung. | `poison` |
| | `destroy_character [name]` | Entfernt ein Crewmitglied. | `destroy_character [name]` |
| | `spawn_dogs [count]` | Fügt Hunde an zufälligen Spawnpunkten hinzu. | `spawn_dogs 3` |

### Angriffe, Feuer und Schaden { #attacks-fire-and-damage }

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| | `attack [severity]` | Startet sofort einen Angriff auf die Basis. Übergib eine Stärke oder eine genaue Mischung wie `fighters=6 divers=4 bombers=3`. | `attack 3` |
| | `schedule_attack [day of week / +hours]` | Plant einen Angriff auf die Basis für einen Tag oder in einer Anzahl Stunden. | `schedule_attack +2` |
| | `show_grid` / `show_grid off` | Zeichnet das Angriffsraster (A1 bis P16) auf den Boden. | `show_grid` |
| | `grid_info [square]` | Listet auf, was sich auf den Rasterfeldern oder auf einem Feld befindet. | `grid_info G6` |
| | `attack_square [square] [divers=] [bombers=]` | Greift ein Rasterfeld an. | `attack_square G6 divers=3 bombers=2` |
| | `get_attack_severity` | Gibt die aktuelle Angriffsstärke aus. | `get_attack_severity` |
| | `bomb [x] [y]` | Wirft eine Bombe an einer Position oder am Mauszeiger ab. | `bomb 20 40` |
| | `bomber_mode [true/false]` | Linksklick wirft eine Bombe ab, Rechtsklick eine Sturzkampfbombe. | `bomber_mode true` |
| | `explode [x] [y]` | Explosionseffekte an einer Position. | `explode 10 30` |
| | `explode_prop [build_id]` | Sprengt ein platziertes Objekt oder eine Werkbank, zum Beispiel `Kitchen`. | `explode_prop Kitchen` |
| | `fire [x] [y] [count]` | Legt Feuer an einer Position, an zufälligen Stellen (nur Anzahl) oder am Mauszeiger. | `fire 5` |
| | `disable_fires [true/false]` | Verhindert, dass Feuer entstehen und sich ausbreiten. | `disable_fires true` |
| | `target` | Lässt zielende Flugzeuge das anvisieren, was unter dem Mauszeiger liegt. | `target` |

### Karteneinstellungen { #map-settings }

Diese Befehle ändern die Einstellungen, die du beim Start einer Karte wählst. Die Zahl ist die Stufe der Einstellung.

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| | `attacks_rate_parameter [value]` | Einstellung für die Angriffshäufigkeit. | `attacks_rate_parameter 1` |
| | `change_attack_severity_parameter [value]` | Einstellung für die Verschiebung der Angriffsstärke. | `change_attack_severity_parameter 1` |
| | `change_harvest_rate_parameter [value]` | Einstellung für die Ernterate. | `change_harvest_rate_parameter 1` |
| | `change_resource_degradation_rate_parameter [value]` | Einstellung für den Ressourcenverfall. | `change_resource_degradation_rate_parameter 1` |
| | `explosion_damage_rate_parameter [value]` | Einstellung für den Explosionsschaden. | `explosion_damage_rate_parameter 1` |
| | `hq_strikes_parameter [value]` | Einstellung für die HQ-Anforderungen. | `hq_strikes_parameter 0` |
| | `set_random_event_chance [0-1]` | Grundwahrscheinlichkeit für Zufallsereignisse. | `set_random_event_chance 0.5` |

### Debug-Ansichten und Technisches { #debug-views-and-technical }

Nutze diese nur, wenn du weißt, warum. `enable_system` und `enable_input_action` können einen Spielstand in einem seltsamen Zustand hinterlassen.

| | Befehl | Was er tut | Beispiel |
|---|---|---|---|
| | `show_attack_heatmap` | Zeigt, wohin Angriffe zielen werden. | `show_attack_heatmap` |
| | `show_voxel_owners` / `show_voxel_owners off` | Zeigt, welches Objekt welches Feld belegt. | `show_voxel_owners` |
| | `damage_debug [true/false]` | Macht Explosionsschaden sichtbar. | `damage_debug true` |
| | `set_target_fps [fps]` | Begrenzt die Bildrate. | `set_target_fps 30` |
| | `enable_input_action [map/action] [true/false]` | Schaltet eine Eingabeaktion ein oder aus. | `enable_input_action Game/TimeScalePause false` |
| | `enable_system [name] [true/false]` | Schaltet einen internen Spielprozess ein oder aus. | `enable_system [name] false` |

## Ein typischer Testlauf { #a-typical-test-run }

```text
create_mission coastal_patrol
set_all_airstrips_tier 3
deliver_crew 4
skip_day
```

Erstelle deine Mission, sorg dafür, dass die Basis ihre Voraussetzungen erfüllt, hol dir genug Crew und spring einen Tag weiter, um zu sehen, was als Nächstes passiert.
