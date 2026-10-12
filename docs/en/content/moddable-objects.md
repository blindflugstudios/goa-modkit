# Moddable objects

These are the objects a mod can give a new model and new textures: the ones you place from the build menu (props, workbenches and training objects), which can also get a new build-menu icon, and the [map objects](#map-objects) such as trees and rocks. To change one, name a file in your mod's `Objects/` folder after its id, for example `Chair.glb` or `Chair.thumbnail.png`. How the file names work is explained on [Objects and models](objects.md#file-names).

- Ids are matched without regard to capital letters: `chair.glb` works as well as `Chair.glb`.
- The built-in textures each object uses are listed on [Built-in texture names](texture-names.md).
This list was taken from the game's generated list of moddable objects on 2026-10-01, and the map objects on 2026-10-12.

## Build menu objects

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

## Map objects

Trees, rocks, ponds and the other objects placed on a map. A file named after the id changes every variant; `<id>.<variant>` changes one variant alone, counted from `0`. Map objects have a few rules of their own, see [Map objects](objects.md#map-objects).

| Id | Variants |
|---|---|
| `berry_bush` | 1 |
| `bush` | 6: `bush.0` to `bush.5` |
| `bush_big` | 1 |
| `clay_pit` | 1 |
| `damaged_car` | 1 |
| `flowers` | 3: `flowers.0` to `flowers.2` |
| `herbs_plant` | 1 |
| `large_rock` | 2: `large_rock.0` to `large_rock.1` |
| `long_rock` | 1 |
| `mushroom_patch` | 1 |
| `ocean` | 1 |
| `old_fence` | 1 |
| `old_fence_pole` | 1 |
| `old_grave` | 2: `old_grave.0` to `old_grave.1` |
| `old_headstone` | 1 |
| `sand_pit` | 1 |
| `small_rock` | 2: `small_rock.0` to `small_rock.1` |
| `tree` | 5: `tree.0` to `tree.4` |
| `tree_big` | 2: `tree_big.0` to `tree_big.1` |
| `tree_big_log` | 2: `tree_big_log.0` to `tree_big_log.1` |
| `tree_big_stump` | 2: `tree_big_stump.0` to `tree_big_stump.1` |
| `water_pond` | 1 |
| `wild_beans` | 1 |
| `wild_grain` | 1 |
| `wild_potato` | 1 |
| `wild_tomato` | 1 |
| `young_tree` | 2: `young_tree.0` to `young_tree.1` |
| `young_tree_big` | 2: `young_tree_big.0` to `young_tree_big.1` |
