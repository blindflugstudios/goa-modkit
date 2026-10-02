# Orte

Jede Mission findet irgendwo statt. Eine Mission listet die Orte auf, an denen sie erscheinen kann, und das Spiel wählt bei jeder Erstellung der Mission einen davon aus. Diese Seite erklärt, wie diese Auswahl funktioniert, was die Orts-Flags bedeuten, listet jeden Ort auf, der mit dem Spiel ausgeliefert wird, samt Koordinaten, und zeigt, wie ein Mod eigene Orte hinzufügt.

## Wie ein Ort ausgewählt wird { #how-a-location-is-chosen }

Wenn eine Mission erstellt wird, zieht das Spiel einen Eintrag aus der Ortsliste der Mission (`_potentialLocations` im Missions-JSON). Ist dieser Platz schon von einer anderen Mission auf der Karte belegt, zieht es erneut, bis zu fünf weitere Male. Sind alle Ziehungen belegt, behält es die letzte - zwei Missionen können sich also einen Ort teilen.

Listet eine Mission gar keine Orte, nimmt das Spiel ersatzweise einen zufälligen Ort aus der vollständigen Liste: den [mitgelieferten Orten](#the-locations-that-ship-with-the-game) plus allen, die aktivierte Mods hinzufügen (siehe [Orte mit einem Mod hinzufügen](#adding-locations-with-a-mod)).

Die Entfernung ist keine Deko: Der Treibstoff, den ein Flug kostet, wird aus der Großkreisentfernung (der kürzesten Strecke über den Globus) zwischen dem Ort und den Koordinaten der geladenen Karte berechnet, multipliziert mit `FuelConsumptionPerKilometer` aus der Tabelle `Variables` (siehe [CSV-Tabellen](../data/csv.md)). Eine Mission über Berlin ist also viel teurer als eine über dem Ärmelkanal.

## Einen Ort verwenden { #using-a-location }

**Im Mission Editor** öffnest du den Abschnitt **Locations**, wählst einen Ort aus dem Dropdown und fügst ihn hinzu. Füge so viele hinzu, wie du willst; derselbe Ort kann nicht zweimal hinzugefügt werden.

**In einer Missions-`.json`** sieht jeder Eintrag von `_potentialLocations` so aus:

```json
{
    "_locationId": "dover",
    "_locationName": "dover",
    "_coordinates": { "x": 51.13512, "y": 1.312756 },
    "_flags": 4
}
```

| Feld | Bedeutung |
|---|---|
| `_locationName` | Der Name des Orts. Das ist das Feld, das das Spiel tatsächlich nutzt: um zu erkennen, ob ein Platz schon belegt ist, und um die Flags des Orts nachzuschlagen. |
| `_locationId` | Nur zur Information. Halte ihn identisch mit dem Namen. |
| `_coordinates` | `x` ist der **Breitengrad**, `y` der **Längengrad**, in Grad. Wird für die Markierung auf der Kriegskarte und für die Entfernung (und damit die Treibstoffkosten) genutzt. |
| `_flags` | Eine Zahl, die den Ort beschreibt (siehe unten). Muss eine Zahl sein - `"Sea"` wird nicht akzeptiert. |

Mit einer Liste mehrerer Orte kann dieselbe Mission an verschiedenen Stellen auftauchen:

```json
"_potentialLocations": [
    { "_locationId": "dover_strait", "_locationName": "dover_strait", "_coordinates": { "x": 51.0598, "y": 1.5825 }, "_flags": 2 },
    { "_locationId": "english_channel", "_locationName": "english_channel", "_coordinates": { "x": 50.166, "y": -1.7013 }, "_flags": 2 },
    { "_locationId": "seine_bay", "_locationName": "seine_bay", "_coordinates": { "x": 49.7154, "y": -0.672 }, "_flags": 2 }
]
```

**Aus einem Skript** wird eine reine Skript-Mission (eine ohne `.json`) mit `missions_api.SetMissionLocation(mission_entity_id, location_name)` platziert, meist in `initialize_mission`. Die Funktion akzeptiert nur einen Namen aus der Liste unten oder einen, den ein aktivierter Mod hinzufügt (siehe [Orte mit einem Mod hinzufügen](#adding-locations-with-a-mod)), nie eigene Koordinaten, und gibt bei einem unbekannten Namen `False` zurück. Ohne Ort sitzt eine reine Skript-Mission am Ursprung der Karte. Siehe [Referenz](reference.md).

## Orts-Flags { #location-flags }

| Wert | Name | Bedeutung |
|---|---|---|
| 0 | `None` | keine |
| 1 | `Land` | über Land |
| 2 | `Sea` | über dem Meer |
| 4 | `OwnTerritory` | über eigenem Gebiet |
| 8 | `EnemyTerritory` | über feindlichem Gebiet |

Sie werden addiert: `10` ist also Meer + feindliches Gebiet (2 + 8) - der häufigste Wert für ein Küstenziel auf der anderen Seite des Ärmelkanals.

!!! warning "Die Flags in deiner Missionsdatei werden nicht gelesen"
    Der Wert `_flags` in einer Missionsdatei ist nur der Vollständigkeit halber da, aber **das Spiel liest ihn nicht**. Jede mitgelieferte Mission lässt ihn auf `0`. Quest-Schritte wie "fliege eine Mission über dem Meer" schlagen den **Namen** des Missionsorts in der Ortsliste nach - den Orten unten plus allen, die aktivierte Mods hinzufügen - und nutzen die dort hinterlegten Flags. Der Quest-Schritt schreibt den **Namen** des Flags, nicht die Zahl: `location,sea`, `location,ownterritory`, `location,enemyterritory` (siehe [Quests](../quests/index.md#aircraft-and-missions)).

    Zwei Folgen: Ein Ortsname, der nicht in der Liste steht, erfüllt jede Ortsbedingung automatisch, und weil kein mitgelieferter Ort `Land` trägt, kann eine Bedingung `location,land` nie erfüllt werden.

## Die Orte, die mit dem Spiel ausgeliefert werden { #the-locations-that-ship-with-the-game }

82 Orte sind vordefiniert. Nutze sie, statt Koordinaten zu erfinden: Sie sind passend zur Kriegskarte platziert, und der Spieler erkennt sie wieder. Sie reichen von Breitengrad 44.87 bis 60.38 und Längengrad -9.00 bis 14.55.

In der Tabelle steht **Eigen** für `OwnTerritory` (4), **Feind** für `EnemyTerritory` (8), **Meer** für `Sea` (2); kombinierte Einträge werden addiert (Meer + Feind = 10).

| Name | Breitengrad | Längengrad | Flags |
|---|---|---|---|
| `aarhus` | 56.1509 | 10.1799 | Feind |
| `amiens` | 49.8980 | 2.3286 | Feind |
| `amsterdam` | 52.3713 | 4.8995 | Meer + Feind |
| `arras` | 50.2933 | 2.7758 | Feind |
| `atlantic_ocean` | 56.5000 | -9.0000 | Meer |
| `bergen` | 60.3829 | 5.3042 | Meer + Feind |
| `berlin` | 52.5217 | 13.3958 | Feind |
| `birmingham` | 52.4907 | -1.8466 | Eigen |
| `bordeaux` | 44.8695 | -0.5592 | Meer + Feind |
| `boulogne-sur-mer` | 50.7246 | 1.6019 | Meer + Feind |
| `bremen` | 53.0869 | 8.7973 | Feind |
| `bremerhaven` | 53.5352 | 8.5838 | Meer + Feind |
| `brest` | 48.3912 | -4.4851 | Meer + Feind |
| `bristol_channel` | 51.3681 | -4.2301 | Meer |
| `brussels` | 50.8552 | 4.3559 | Feind |
| `caen` | 49.1857 | -0.3894 | Meer + Feind |
| `calais` | 50.9587 | 1.8552 | Meer + Feind |
| `cambridge` | 52.1925 | 0.1337 | Eigen |
| `canterbury` | 51.2733 | 1.0855 | Eigen |
| `cardigan_bay` | 52.5000 | -4.6000 | Meer |
| `celtic_sea` | 50.8000 | -7.5000 | Meer |
| `chelmsford` | 51.7352 | 0.4673 | Eigen |
| `cologne` | 50.9375 | 6.9517 | Feind |
| `compiegne` | 49.3991 | 2.8277 | Feind |
| `dedham_vale` | 51.9878 | 0.9096 | Eigen |
| `dieppe` | 49.9189 | 1.0747 | Meer + Feind |
| `dogger_bank` | 54.9952 | 3.0143 | Meer |
| `dorchester` | 50.7106 | -2.4410 | Eigen |
| `dover` | 51.1351 | 1.3128 | Eigen |
| `dover_strait` | 51.0598 | 1.5825 | Meer |
| `dunkirk` | 51.0370 | 2.3788 | Meer + Feind |
| `dunkirk_bay` | 51.3082 | 2.1831 | Meer |
| `eastbourne_bay` | 50.6432 | 0.4435 | Meer |
| `eindhoven` | 51.4497 | 5.3770 | Feind |
| `english_channel` | 50.1660 | -1.7013 | Meer |
| `essen` | 51.4535 | 7.0060 | Feind |
| `frankfurt` | 50.1028 | 8.6791 | Feind |
| `great_yarmouth_bay` | 52.5492 | 2.2980 | Meer |
| `guernsey` | 49.4438 | -2.5571 | Meer |
| `hamburg` | 53.5381 | 9.9669 | Meer + Feind |
| `hanover` | 52.3736 | 9.7400 | Feind |
| `hardangervidda` | 60.0327 | 7.4297 | Feind |
| `high_weald` | 51.0563 | 0.4398 | Eigen |
| `ipswich` | 52.0524 | 1.1532 | Eigen |
| `irish_sea` | 53.5000 | -4.8000 | Meer |
| `kassel` | 51.3127 | 9.4948 | Feind |
| `krefeld` | 51.3394 | 6.5521 | Feind |
| `kristiansand` | 58.1581 | 7.9766 | Meer + Feind |
| `la_rochelle` | 46.1597 | -1.1592 | Meer + Feind |
| `lannion` | 48.7372 | -3.4625 | Meer + Feind |
| `le_havre` | 49.5003 | 0.1352 | Meer + Feind |
| `leeuwarden` | 53.2037 | 5.7917 | Meer + Feind |
| `liege` | 50.6413 | 5.5752 | Feind |
| `lille` | 50.6252 | 3.0551 | Feind |
| `london` | 51.5090 | -0.1280 | Eigen |
| `maastricht` | 50.8474 | 5.6870 | Feind |
| `maidstone` | 51.2707 | 0.5203 | Eigen |
| `malvern_hills` | 52.1034 | -2.3512 | Eigen |
| `metz` | 48.9610 | 6.1310 | Feind |
| `munster` | 51.9645 | 7.6099 | Feind |
| `nancy` | 48.6921 | 6.1844 | Feind |
| `nantes` | 47.2216 | -1.5501 | Feind |
| `north_channel` | 55.1000 | -5.6000 | Meer |
| `north_sea` | 56.5000 | 3.5000 | Meer |
| `north_wessex` | 51.4482 | -1.4938 | Eigen |
| `outer_silver_pit` | 54.0262 | 2.0864 | Meer |
| `paris` | 48.8535 | 2.3188 | Feind |
| `raf_duxford` | 52.0933 | 0.1311 | Eigen |
| `raf_filton` | 51.5218 | -2.5746 | Eigen |
| `raf_manston` | 51.3461 | 1.3490 | Eigen |
| `raf_tangmere` | 50.8464 | -0.7095 | Eigen |
| `reims` | 49.2570 | 4.0438 | Feind |
| `rotterdam` | 51.9302 | 4.4752 | Meer + Feind |
| `rotterdam_bay` | 51.9939 | 3.1666 | Meer |
| `rouen` | 49.4381 | 1.0937 | Feind |
| `seine_bay` | 49.7154 | -0.6720 | Meer |
| `south_downs` | 50.9450 | -0.6643 | Eigen |
| `st_georges_channel` | 52.0000 | -5.8000 | Meer |
| `stettin` | 53.4282 | 14.5511 | Meer + Feind |
| `telemark` | 59.3766 | 8.3060 | Feind |
| `the_wash` | 52.9159 | 0.2530 | Meer |
| `tours` | 47.3933 | 0.6825 | Feind |

Zwei weitere Einträge stehen in der Liste des Spiels, sind aber Überbleibsel aus der Entwicklung - **nutze sie nicht**: `test1` und `ireland`. Keiner von beiden trägt ein Flag, und `ireland` liegt nicht in Irland.

## Orte mit einem Mod hinzufügen { #adding-locations-with-a-mod }

Ein Mod kann der Liste eigene Orte hinzufügen, damit seine Missionen - und die von anderen - sie über ihren Namen nutzen können. Leg dazu eine oder mehrere `.json`-Dateien in einen Ordner `Locations` im `Missions/`-Ordner deines Mods:

```text
Mods/
  my_mod/
    Missions/
      Locations/
        mymod_locations.json
```

Gelesen werden nur Dateien, die direkt in `Missions/Locations/` liegen. Eine Datei sieht so aus:

```json
{
    "Locations": [
        {
            "_locationId": "mymod_scapa_flow",
            "_locationName": "mymod_scapa_flow",
            "_coordinates": { "x": 58.9, "y": -3.1 },
            "_flags": 2
        }
    ]
}
```

Die Liste `Locations` fasst so viele Orte, wie du willst. Jeder Eintrag hat dieselben Felder wie ein Eintrag in einer Missionsdatei ([siehe oben](#using-a-location)), und `_flags` muss auch hier eine Zahl sein ([Orts-Flags](#location-flags)).

- **Solange dein Mod aktiviert ist, stehen seine Orte auf der Liste**, und sie verschwinden wieder, wenn der Mod ausgeschaltet oder entfernt wird. Schaltest du einen Mod ein oder aus, wird die Liste ohne Neustart des Spiels aktualisiert.
- **Ein Ort aus einem Mod verhält sich wie ein mitgelieferter.** Er wird im Dropdown des Mission Editors angeboten, funktioniert mit `missions_api.SetMissionLocation`, kann für eine Mission ohne Orte gezogen werden, und seine Flags sind das, was Ortsbedingungen in Quests sehen.
- **Mitgelieferte Namen gewinnen immer.** Nutzt dein Ort einen Namen, den das Spiel schon hat, wird der mitgelieferte verwendet. Fügen zwei Mods denselben Namen hinzu, nimmt das Spiel einen davon und sagt dir nichts. Gib also jedem Ort das Präfix deines Mods, wie bei `mymod_scapa_flow`.
- **Der Spieler sieht `_locationName` genau so, wie es dasteht**, samt Unterstrichen. Mitgelieferte Orte haben Übersetzungen; deiner hat keine, bis du einen Term namens `mission_location/<name>` registrierst - siehe [Ortsnamen](../scripting/localization.md#location-names).
- **Eine Datei, die das Spiel nicht lesen kann, wird übersprungen**, mit einer Warnung in [`Player.log`](../start/troubleshooting.md#find-the-playerlog). Deine anderen Ortsdateien werden trotzdem geladen.
- Halte die Koordinaten innerhalb der Kriegskarte (siehe nächster Abschnitt).

## Eigene Koordinaten verwenden { #using-your-own-coordinates }

Nichts hindert eine Mission daran, einen Ort zu nennen, der nicht in der Liste steht. Die Koordinaten stehen in der Datei der Mission selbst, nicht in einer gemeinsamen Tabelle - du kannst eine Mission also überall hinsetzen. Name und Koordinaten gehören dir; die Flags, die ein Quest-Schritt sieht, nicht - die kommen per Name aus der Ortsliste (den mitgelieferten Orten und allen, die ein Mod hinzufügt). Ein Ort, den es nur in der Datei einer Mission gibt, erfüllt also jede Ortsbedingung. Auch ein Skript kann so einen Ort nicht nutzen: `missions_api.SetMissionLocation` akzeptiert nur Namen aus der Liste. Damit ein Ort Flags hat oder aus einem Skript nutzbar ist, [füg ihn mit einem Mod hinzu](#adding-locations-with-a-mod).

Die Kriegskarte zeigt Breitengrad 40.75 bis 61.25 und Längengrad -11.75 bis 21.64 (eine Mercator-Projektion, die übliche flache Weltkarte). Der Bereich der mitgelieferten Orte oben ist einfach nur da, wo sie zufällig liegen, nicht die Grenze der Karte. Ein Ort außerhalb des Kartenrahmens funktioniert trotzdem - Entfernung und Treibstoff sind nur Mathematik -, aber seine Markierung wird an den nächsten Kartenrand geschoben. Der Spieler sieht ihn also am Rand statt dort, wo er wirklich liegt. Anklickbar bleibt er.

!!! tip
    Gib deinen eigenen Orten einen Namen mit dem Präfix deines Mods (`mymod_scapa_flow`). Ein Name, den das Spiel schon nutzt, würde sich die Prüfung "schon belegt" mit jeder Mission teilen, die diesen Ort nutzt.
