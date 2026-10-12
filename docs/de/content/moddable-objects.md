# Veränderbare Objekte

Das sind die Objekte, denen eine Mod ein neues Modell und neue Texturen geben kann: die, die du aus dem Baumenü platzierst (Requisiten, Werkbänke und Trainingsobjekte), die außerdem ein neues Symbol im Baumenü bekommen können, und die [Kartenobjekte](#map-objects) wie Bäume und Felsen. Um eins zu ändern, benennst du eine Datei im Ordner `Objects/` deiner Mod nach seiner Id, zum Beispiel `Chair.glb` oder `Chair.thumbnail.png`. Wie die Dateinamen funktionieren, steht unter [Objekte und Modelle](objects.md#file-names).

- Bei den Ids spielt Groß- und Kleinschreibung keine Rolle: `chair.glb` funktioniert genauso wie `Chair.glb`.
- Welche eingebauten Texturen jedes Objekt verwendet, steht unter [Eingebaute Texturnamen](texture-names.md).
Diese Liste stammt aus der vom Spiel erzeugten Liste der veränderbaren Objekte, Stand 2026-10-01, die Kartenobjekte Stand 2026-10-12.

## Objekte aus dem Baumenü { #build-menu-objects }

| | | | |
|---|---|---|---|
| `AntitankPimple` | `FieldKitchen` | `Poster03` | `Sickbed` |
| `BarbedWire` | `Flagpole10` | `Poster04` | `SirenOnPole` |
| `BarCounter` | `Flagpole5` | `Poster05` | `SmallFuelTank` |
| `Barrel` | `FlagpoleFloor` | `Poster06` | `SmallLoungeTable` |
| `BarStool` | `FlagpoleWall` | `Poster07` | `Stepladder` |
| `Bed` | `Flowerbed01` | `Poster08` | `StoveSmall` |
| `BedMetal` | `Flowerbed02` | `Poster09` | `TableMetal` |
| `BedWood` | `FlyingAdvancedLinkTrainer` | `Poster10` | `TableOutdoor` |
| `BilliardTable` | `FlyingSimpleWoodenConstruction` | `Poster11` | `TableTypewriter` |
| `BloodPackRack` | `FuelTank` | `Poster12` | `TailorStation` |
| `Bofors40mm` | `Gramophone` | `Poster13` | `Toilet` |
| `BombingAdvancedSimulator` | `Gravestone` | `Poster14` | `Toolbox` |
| `BombingSimpleBench` | `GravestoneWhite` | `Poster15` | `VickersGunAA` |
| `Brickstation` | `Guitar` | `Poster16` | `WallPhone` |
| `CanningStation` | `HandwashBowls` | `Poster17` | `WallSign1` |
| `CementMixer` | `Hangers` | `Poster18` | `WallSign2` |
| `Chair` | `HerbDryer` | `Poster19` | `WallSign3` |
| `Chalkboard` | `IndoorKitchen` | `Poster20` | `WallSign4` |
| `Clock` | `Jukebox` | `Poster21` | `WallSign5` |
| `Clothesline` | `KickstarterBackerMonument` | `Radio` | `WarningSign1` |
| `ClothingRack` | `KickstarterCustomMonument` | `RadioTower` | `WarningSign2` |
| `ClothingStand` | `LiquorShelf` | `Roadblock` | `WarningSign3` |
| `ComfyChair` | `Lookout` | `RollableScaffolding` | `WarningSign4` |
| `ComfyChairLarge` | `MedicineCabinet` | `RollableToolTable` | `WarningSign5` |
| `ControlTowerBrick` | `MetalBoxSmall` | `RugBedrug` | `WaterCooker` |
| `ControlTowerConcrete` | `MetalFenceEdge` | `RugBedrugSmall` | `WaterPump` |
| `ControlTowerMetal` | `MetalShelf` | `RugCubismrug` | `WaterTower` |
| `CookingFire` | `MetalShelfClosedClothes` | `RugDoormat` | `WaySign1` |
| `CrateEmpty` | `MetalShelfClosedFiles` | `RugJuterug` | `WaySign2` |
| `Cross` | `MetalworksWorkbench` | `RugKitchenrug` | `WaySign3` |
| `CurtainsClosedSmall` | `NavigationAdvancedNaviTrainer` | `RugPersian` | `WaySign4` |
| `CurtainsOpenSmall` | `NavigationSimpleBoard` | `SandbagFence1mCorner` | `WaySign5` |
| `Dartboard` | `NightTable` | `SandbagFence1mStraight` | `WickerChair` |
| `Distillery` | `OerlikonGun` | `SawStation` | `Windhose` |
| `DividerCurtains` | `OxygenBottle` | `ScrambleBell` | `WoodenChair` |
| `Drawer` | `Piano` | `Searchlight` | `WoodenFenceSimple` |
| `ElectronicsWorkbench` | `PilotBoard` | `Shelf` | `WoodenFenceSimplePole` |
| `EnduranceAdvancedBikeExerciser` | `PlanningBoard` | `ShelfBooks` | `WoodenFenceSturdyEdge` |
| `EnduranceSimpleRack` | `PolishPilotsFlag` | `ShelfFolders` | `WoodenTableLarge` |
| `EngineeringAdvancedEngine` | `Poster` | `ShelfPersonalStuff` | `WoodenTableMedium` |
| `EngineeringSimpleMechanicWorkstation` | `Poster01` | `ShootingAdvancedTurret` | `WoodenTableSmall` |
| `EspionageRadio` | `Poster02` | `ShootingSimpleTargetRange` |  |

## Kartenobjekte { #map-objects }

Bäume, Felsen, Teiche und die anderen Objekte, die auf einer Karte platziert sind. Eine Datei, die nach der Id benannt ist, ändert jede Variante; `<id>.<variant>` ändert nur eine Variante, gezählt ab `0`. Für Kartenobjekte gelten ein paar eigene Regeln, siehe [Kartenobjekte](objects.md#map-objects).

| Id | Varianten |
|---|---|
| `berry_bush` | 1 |
| `bush` | 6: `bush.0` bis `bush.5` |
| `bush_big` | 1 |
| `clay_pit` | 1 |
| `damaged_car` | 1 |
| `flowers` | 3: `flowers.0` bis `flowers.2` |
| `herbs_plant` | 1 |
| `large_rock` | 2: `large_rock.0` bis `large_rock.1` |
| `long_rock` | 1 |
| `mushroom_patch` | 1 |
| `ocean` | 1 |
| `old_fence` | 1 |
| `old_fence_pole` | 1 |
| `old_grave` | 2: `old_grave.0` bis `old_grave.1` |
| `old_headstone` | 1 |
| `sand_pit` | 1 |
| `small_rock` | 2: `small_rock.0` bis `small_rock.1` |
| `tree` | 5: `tree.0` bis `tree.4` |
| `tree_big` | 2: `tree_big.0` bis `tree_big.1` |
| `tree_big_log` | 2: `tree_big_log.0` bis `tree_big_log.1` |
| `tree_big_stump` | 2: `tree_big_stump.0` bis `tree_big_stump.1` |
| `water_pond` | 1 |
| `wild_beans` | 1 |
| `wild_grain` | 1 |
| `wild_potato` | 1 |
| `wild_tomato` | 1 |
| `young_tree` | 2: `young_tree.0` bis `young_tree.1` |
| `young_tree_big` | 2: `young_tree_big.0` bis `young_tree_big.1` |
