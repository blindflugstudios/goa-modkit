# Locations

Every mission happens somewhere. A mission lists the places it can appear, and the game picks one of them each time the mission is created. This page explains how that choice works, what the location flags mean, lists every place that ships with the game, with its coordinates, and shows how a mod adds places of its own.

## How a location is chosen

When a mission is created, the game draws one entry from the mission's list of locations (`_potentialLocations` in the mission JSON). If that spot is already used by another mission on the map, it draws again, up to five more times. If every draw comes up taken, it keeps the last one, so two missions can end up sharing a location.

If a mission lists no locations at all, the game falls back to a random place from the full list: the [places that ship with the game](#the-locations-that-ship-with-the-game) plus any that enabled mods add (see [Adding locations with a mod](#adding-locations-with-a-mod)).

Distance is not decoration: the fuel a flight costs is worked out from the great-circle distance (the shortest distance over the globe) between the location and the loaded map's own coordinates, multiplied by `FuelConsumptionPerKilometer` from the `Variables` table (see [CSV tables](../data/csv.md)). A mission over Berlin is far more expensive to fly than one over the Channel.

## Using a location

**In the Mission Editor**, open the **Locations** section, pick a place from the dropdown and add it. Add as many as you like; the same place cannot be added twice.

**In a mission `.json`**, each entry of `_potentialLocations` names a place by its ID:

```json
{
    "_locationId": "dover"
}
```

| Field | Meaning |
|---|---|
| `_locationId` | **Required**, and the only field the game reads from the entry. It must be the ID of a place from the [list below](#the-locations-that-ship-with-the-game) or of one that an enabled mod adds (see [Adding locations with a mod](#adding-locations-with-a-mod)). |

The place's coordinates, flags and display name come from that list, not from the mission file. A `_locationName`, `_coordinates` or `_flags` left on the entry is ignored.

An entry whose ID is missing, empty or unknown is never found. When the drawn entry cannot be found, the game falls back to a random location.

The ID is also what the game uses to tell whether a spot is already taken, so it avoids placing two live missions on the same ID where it can (see [How a location is chosen](#how-a-location-is-chosen)).

A list with several places lets the same mission turn up in different spots:

```json
"_potentialLocations": [
    { "_locationId": "dover_strait" },
    { "_locationId": "english_channel" },
    { "_locationId": "seine_bay" }
]
```

**From a script**, a script-only mission (one without a `.json`) is placed with `missions_api.SetMissionLocation(mission_entity_id, location_id)`, usually from `initialize_mission`. It accepts only the ID of a place from the list below or of one that an enabled mod adds (see [Adding locations with a mod](#adding-locations-with-a-mod)), never coordinates of your own, and returns `False` for an unknown ID. Without a location, a script-only mission sits at the map origin. See [Reference](reference.md).

## Location flags

| Value | Name | Meaning |
|---|---|---|
| 0 | `None` | none |
| 1 | `Land` | over land |
| 2 | `Sea` | over the sea |
| 4 | `OwnTerritory` | over friendly territory |
| 8 | `EnemyTerritory` | over enemy territory |

They add up, so `10` is Sea + Enemy territory (2 + 8) - the most common value for a coastal target on the far side of the Channel. Some combinations:

| Value | Flags |
|---|---|
| 3 | Land + Sea |
| 5 | Land + OwnTerritory |
| 6 | Sea + OwnTerritory |
| 9 | Land + EnemyTerritory |
| 10 | Sea + EnemyTerritory |
| 12 | OwnTerritory + EnemyTerritory |

A place with several flags passes a quest condition for each of them: a `10` place counts for both `location,sea` and `location,enemyterritory`.

In the shipped game, location flags are used only to **unlock the built-in airplane skins**: hidden skin quests such as "fly 20 missions over the sea with a Beaufighter" use `location,sea`, `location,ownterritory` and `location,enemyterritory`. No other shipped quest checks them.

!!! warning "Flags come from the location list, not from your mission file"
    A mission's location entry carries only the ID; a `_flags` value left on it is ignored. Quest steps such as "fly a mission over the sea" look the mission's location **ID** up in the location list - the places below plus any that enabled mods add - and use the flags recorded there. The quest step writes the flag **name**, not the number: `location,sea`, `location,ownterritory`, `location,enemyterritory` (see [Quests](../quests/index.md#aircraft-and-missions)).

    Because no shipped location carries `Land`, a `location,land` condition can never be met unless a mod adds a place with that flag.

## The locations that ship with the game

82 places are predefined. Reuse them rather than inventing coordinates: they are positioned to line up with the war map, and the player will recognise them. They run from latitude 44.87 to 60.38 and longitude -9.00 to 14.55.

In the table, **Own** is `OwnTerritory` (4), **Enemy** is `EnemyTerritory` (8), **Sea** is `Sea` (2); combined entries add up (Sea + Enemy = 10).

| ID | Latitude | Longitude | Flags |
|---|---|---|---|
| `aarhus` | 56.1509 | 10.1799 | Enemy |
| `amiens` | 49.8980 | 2.3286 | Enemy |
| `amsterdam` | 52.3713 | 4.8995 | Sea + Enemy |
| `arras` | 50.2933 | 2.7758 | Enemy |
| `atlantic_ocean` | 56.5000 | -9.0000 | Sea |
| `bergen` | 60.3829 | 5.3042 | Sea + Enemy |
| `berlin` | 52.5217 | 13.3958 | Enemy |
| `birmingham` | 52.4907 | -1.8466 | Own |
| `bordeaux` | 44.8695 | -0.5592 | Sea + Enemy |
| `boulogne-sur-mer` | 50.7246 | 1.6019 | Sea + Enemy |
| `bremen` | 53.0869 | 8.7973 | Enemy |
| `bremerhaven` | 53.5352 | 8.5838 | Sea + Enemy |
| `brest` | 48.3912 | -4.4851 | Sea + Enemy |
| `bristol_channel` | 51.3681 | -4.2301 | Sea |
| `brussels` | 50.8552 | 4.3559 | Enemy |
| `caen` | 49.1857 | -0.3894 | Sea + Enemy |
| `calais` | 50.9587 | 1.8552 | Sea + Enemy |
| `cambridge` | 52.1925 | 0.1337 | Own |
| `canterbury` | 51.2733 | 1.0855 | Own |
| `cardigan_bay` | 52.5000 | -4.6000 | Sea |
| `celtic_sea` | 50.8000 | -7.5000 | Sea |
| `chelmsford` | 51.7352 | 0.4673 | Own |
| `cologne` | 50.9375 | 6.9517 | Enemy |
| `compiegne` | 49.3991 | 2.8277 | Enemy |
| `dedham_vale` | 51.9878 | 0.9096 | Own |
| `dieppe` | 49.9189 | 1.0747 | Sea + Enemy |
| `dogger_bank` | 54.9952 | 3.0143 | Sea |
| `dorchester` | 50.7106 | -2.4410 | Own |
| `dover` | 51.1351 | 1.3128 | Own |
| `dover_strait` | 51.0598 | 1.5825 | Sea |
| `dunkirk` | 51.0370 | 2.3788 | Sea + Enemy |
| `dunkirk_bay` | 51.3082 | 2.1831 | Sea |
| `eastbourne_bay` | 50.6432 | 0.4435 | Sea |
| `eindhoven` | 51.4497 | 5.3770 | Enemy |
| `english_channel` | 50.1660 | -1.7013 | Sea |
| `essen` | 51.4535 | 7.0060 | Enemy |
| `frankfurt` | 50.1028 | 8.6791 | Enemy |
| `great_yarmouth_bay` | 52.5492 | 2.2980 | Sea |
| `guernsey` | 49.4438 | -2.5571 | Sea |
| `hamburg` | 53.5381 | 9.9669 | Sea + Enemy |
| `hanover` | 52.3736 | 9.7400 | Enemy |
| `hardangervidda` | 60.0327 | 7.4297 | Enemy |
| `high_weald` | 51.0563 | 0.4398 | Own |
| `ipswich` | 52.0524 | 1.1532 | Own |
| `irish_sea` | 53.5000 | -4.8000 | Sea |
| `kassel` | 51.3127 | 9.4948 | Enemy |
| `krefeld` | 51.3394 | 6.5521 | Enemy |
| `kristiansand` | 58.1581 | 7.9766 | Sea + Enemy |
| `la_rochelle` | 46.1597 | -1.1592 | Sea + Enemy |
| `lannion` | 48.7372 | -3.4625 | Sea + Enemy |
| `le_havre` | 49.5003 | 0.1352 | Sea + Enemy |
| `leeuwarden` | 53.2037 | 5.7917 | Sea + Enemy |
| `liege` | 50.6413 | 5.5752 | Enemy |
| `lille` | 50.6252 | 3.0551 | Enemy |
| `london` | 51.5090 | -0.1280 | Own |
| `maastricht` | 50.8474 | 5.6870 | Enemy |
| `maidstone` | 51.2707 | 0.5203 | Own |
| `malvern_hills` | 52.1034 | -2.3512 | Own |
| `metz` | 48.9610 | 6.1310 | Enemy |
| `munster` | 51.9645 | 7.6099 | Enemy |
| `nancy` | 48.6921 | 6.1844 | Enemy |
| `nantes` | 47.2216 | -1.5501 | Enemy |
| `north_channel` | 55.1000 | -5.6000 | Sea |
| `north_sea` | 56.5000 | 3.5000 | Sea |
| `north_wessex` | 51.4482 | -1.4938 | Own |
| `outer_silver_pit` | 54.0262 | 2.0864 | Sea |
| `paris` | 48.8535 | 2.3188 | Enemy |
| `raf_duxford` | 52.0933 | 0.1311 | Own |
| `raf_filton` | 51.5218 | -2.5746 | Own |
| `raf_manston` | 51.3461 | 1.3490 | Own |
| `raf_tangmere` | 50.8464 | -0.7095 | Own |
| `reims` | 49.2570 | 4.0438 | Enemy |
| `rotterdam` | 51.9302 | 4.4752 | Sea + Enemy |
| `rotterdam_bay` | 51.9939 | 3.1666 | Sea |
| `rouen` | 49.4381 | 1.0937 | Enemy |
| `seine_bay` | 49.7154 | -0.6720 | Sea |
| `south_downs` | 50.9450 | -0.6643 | Own |
| `st_georges_channel` | 52.0000 | -5.8000 | Sea |
| `stettin` | 53.4282 | 14.5511 | Sea + Enemy |
| `telemark` | 59.3766 | 8.3060 | Enemy |
| `the_wash` | 52.9159 | 0.2530 | Sea |
| `tours` | 47.3933 | 0.6825 | Enemy |

Two further entries exist in the game's list but are development leftovers - **do not use them**: `test1` and `ireland`. Neither carries any flag, and `ireland` is not in Ireland.

## Adding locations with a mod

A mod can add its own places to the list, so its missions - and anyone else's - can use them by ID. Put one or more `.json` files into a `Locations` folder inside your mod's `Missions/` folder:

```text
Mods/
  my_mod/
    Missions/
      Locations/
        mymod_locations.json
```

Only files directly inside `Missions/Locations/` are read. A file looks like this:

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

The `Locations` list holds as many places as you like. Each entry has four fields:

| Field | Meaning |
|---|---|
| `_locationId` | **Required.** The ID missions and scripts use to refer to the place. |
| `_locationName` | The name the player sees (see below). |
| `_coordinates` | `x` is **latitude**, `y` is **longitude**, in degrees. Used for the marker on the war map and for the distance (and so the fuel cost). |
| `_flags` | A number describing the place ([Location flags](#location-flags)). Must be a number - `"Sea"` is not accepted. |

- **While your mod is enabled, its places are on the list**, and they leave it when the mod is switched off or removed. Switching a mod on or off updates the list without restarting the game.
- **A place from a mod behaves like a shipped one.** It is offered in the Mission Editor's dropdown, works with `missions_api.SetMissionLocation`, can be drawn for a mission that lists no locations, and its flags are what quest location conditions see.
- **`_locationId` is the lookup key, so it has to be unique. Shipped IDs always win.** If your place uses an ID the game already has, the shipped one is used. If two mods add the same ID, the game uses one of them and does not tell you. So give every place your mod's prefix, as in `mymod_scapa_flow`.
- **An entry without an ID can never be found**, neither by a mission nor by `missions_api.SetMissionLocation`.
- **The player sees `_locationName` exactly as written**, underscores and all. Shipped places come with translations; yours has none until you register a term called `mission_location/<name>` - see [Location names](../scripting/localization.md#location-names).
- **A file the game cannot read is skipped**, with a warning in [`Player.log`](../start/troubleshooting.md#find-the-playerlog). Your other location files still load.
- Keep the coordinates inside the war map (see the next section).

## Using your own coordinates

A mission file cannot carry coordinates of its own: it only names a place by ID, and the coordinates and flags come from the location list (the shipped places and any added by a mod). An ID that is not on the list is never found, and the mission goes to a random location instead. To put a mission somewhere new, [add the place with a mod](#adding-locations-with-a-mod) and refer to it by its ID - from a mission file and from `missions_api.SetMissionLocation` alike.

The war map shows latitude 40.75 to 61.25 and longitude -11.75 to 21.64 (a Mercator projection, the usual flat world map). The range of the shipped places above is simply where they happen to be, not the map's limit. A location outside the map's box still works - distance and fuel are just maths - but its marker is pushed to the nearest edge of the map, so the player sees it at the border rather than where it really is. It stays clickable.

!!! tip
    Give your own places an ID with your mod's prefix (`mymod_scapa_flow`). An ID the game already has is not yours to define: the shipped place wins.
