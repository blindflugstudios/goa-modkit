# Built-in texture names

A PNG in your mod's `Objects/` folder that is named exactly like one of the game's own textures **replaces that texture** on every object that uses it. You do not need a model for this: the game keeps its own model and paints your picture onto it. `Objects/BedMetal_Toon-Main_BaseMap_1001.png`, for example, re-paints the metal bed. The rules are on [Objects and models](objects.md#re-painting-without-a-model).

Some textures are shared by several objects. Such a texture is listed under each of them, and replacing it changes all of them at once. Paint your replacement at the same size and layout as the original, because the model stays the game's own.

The **Slot** column says what the texture does on the object:

| Slot | What it holds |
|---|---|
| `_BaseMap` | the base colour; for objects with several tiles, tile 1001 (UVs with U from 0 to 1) |
| `_BaseMap1002`, `_BaseMap1003` | the base colour of tiles 1002 (U from 1 to 2) and 1003 (U from 2) |
| `_SpecularMap` | the specular colour, how shiny each spot is; for objects with several tiles, tile 1001 |
| `_SpecularMap1002`, `_SpecularMap1003` | the specular colour of tiles 1002 and 1003 |

The slot is only information: your file is named after the **texture**, never after the slot. Other slots the game uses internally (for example for battle damage, snow or fading out) are left out of these tables.

These tables were taken from the game's generated texture list on 2026-10-01.

## Objects from the build menu

| Object | Texture | Slot |
|---|---|---|
| `AntitankPimple` | `AntitankPimple_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `BarbedWire` | `M_TO_Old-Fence_Base_color` | `_BaseMap` |
| `BarbedWire` | `T_Batch_02_2_BC` | `_BaseMap` |
| `BarCounter` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `Barrel` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `BarStool` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `BarStool` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Bed` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `BedMetal` | `BedMetal_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `BedMetal` | `BedMetal_Toon-Main_BaseMap_1002` | `_BaseMap1002` |
| `BedMetal` | `BedMetal_Toon-Main_Specular_1001` | `_SpecularMap` |
| `BedMetal` | `BedMetal_Toon-Main_Specular_1002` | `_SpecularMap1002` |
| `BedWood` | `BedWood_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `BilliardTable` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `BilliardTable` | `T_PP_Entertainment_O4` | `_BaseMap` |
| `BilliardTable` | `T_PV_CrewItems_04` | `_BaseMap` |
| `BloodPackRack` | `Batch_03_2` | `_BaseMap` |
| `Bofors40mm` | `Batch_03_1` | `_BaseMap` |
| `Chair` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Chalkboard` | `Chalkboard_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Chalkboard` | `Chalkboard_Toon-Main_Specular_1001` | `_SpecularMap` |
| `Clock` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `Clock` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Clothesline` | `Batch_03_2` | `_BaseMap` |
| `ClothingRack` | `ClothingRack_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ClothingRack` | `TIG_Colors_01` | `_BaseMap` |
| `ClothingStand` | `ClothingStand_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ClothingStand` | `TIG_Colors_01` | `_BaseMap` |
| `ComfyChair` | `Batch_03_1` | `_BaseMap` |
| `ComfyChair` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ComfyChairLarge` | `Batch_03_1` | `_BaseMap` |
| `ComfyChairLarge` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ControlTowerBrick` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `ControlTowerBrick` | `Batch_03_2` | `_BaseMap` |
| `ControlTowerBrick` | `MetalShelf-Closed-Clothes_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ControlTowerBrick` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ControlTowerBrick` | `T_Batch_01_BC` | `_BaseMap` |
| `ControlTowerBrick` | `T_Batch_02_1_BC` | `_BaseMap` |
| `ControlTowerBrick` | `T_Batch_02_2_BC` | `_BaseMap` |
| `ControlTowerBrick` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `ControlTowerBrick` | `T_PV_CrewItems_04` | `_BaseMap` |
| `ControlTowerBrick` | `T_SR_Resource_05_1` | `_BaseMap` |
| `ControlTowerBrick` | `Typewriter-Table_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `ControlTowerBrick` | `Typewriter-Table_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `ControlTowerConcrete` | `BB0855_Ground_Bunker_M_BB_Bunker_BaseMap` | `_BaseMap` |
| `ControlTowerConcrete` | `Batch_03_2` | `_BaseMap` |
| `ControlTowerConcrete` | `Control-Tower-Concrete_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ControlTowerConcrete` | `Control-Tower-Concrete_Toon-Main_Specular_1001` | `_SpecularMap` |
| `ControlTowerConcrete` | `Control-Tower-Metal_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ControlTowerConcrete` | `Control-Tower-Metal_Toon-Main_Specular_1001` | `_SpecularMap` |
| `ControlTowerConcrete` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ControlTowerConcrete` | `T_Batch_01_BC` | `_BaseMap` |
| `ControlTowerConcrete` | `T_Batch_02_2_BC` | `_BaseMap` |
| `ControlTowerConcrete` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `ControlTowerConcrete` | `T_SR_Resource_05_1` | `_BaseMap` |
| `ControlTowerMetal` | `Control-Tower-Metal_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ControlTowerMetal` | `Control-Tower-Metal_Toon-Main_Specular_1001` | `_SpecularMap` |
| `ControlTowerMetal` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ControlTowerMetal` | `T_Batch_02_2_BC` | `_BaseMap` |
| `ControlTowerMetal` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `ControlTowerMetal` | `T_SR_Resource_05_1` | `_BaseMap` |
| `ControlTowerMetal` | `TableMetal_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ControlTowerMetal` | `TableMetal_Toon-Main_Specular_1001` | `_SpecularMap` |
| `ControlTowerMetal` | `Water-Reservoir_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `ControlTowerMetal` | `Water-Reservoir_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `CookingFire` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `CookingFire` | `T_Batch_02_1_BC` | `_BaseMap` |
| `CrateEmpty` | `T_SR_Resource_05_1` | `_BaseMap` |
| `Cross` | `Batch_03_1` | `_BaseMap` |
| `Cross` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Cross` | `T_PV_CrewItems_04` | `_BaseMap` |
| `CurtainsClosedSmall` | `Batch_03_2` | `_BaseMap` |
| `CurtainsClosedSmall` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `CurtainsOpenSmall` | `Batch_03_2` | `_BaseMap` |
| `CurtainsOpenSmall` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Dartboard` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Dartboard` | `T_PP_Entertainment_O4` | `_BaseMap` |
| `DividerCurtains` | `Batch_03_2` | `_BaseMap` |
| `Drawer` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Flagpole10` | `T_Batch_02_1_BC` | `_BaseMap` |
| `Flagpole10` | `Union_Jack` | `_BaseMap` |
| `Flagpole5` | `T_Batch_02_1_BC` | `_BaseMap` |
| `Flagpole5` | `Union_Jack` | `_BaseMap` |
| `FlagpoleFloor` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `FlagpoleFloor` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `FlagpoleWall` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `FlagpoleWall` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Flowerbed01` | `Batch_03_1` | `_BaseMap` |
| `Flowerbed02` | `Batch_03_1` | `_BaseMap` |
| `FuelTank` | `T_Batch_02_3_BC` | `_BaseMap` |
| `Gramophone` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `Gravestone` | `Batch_03_1` | `_BaseMap` |
| `Gravestone` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Gravestone` | `T_PV_CrewItems_04` | `_BaseMap` |
| `GravestoneWhite` | `Batch_03_1` | `_BaseMap` |
| `GravestoneWhite` | `GraveStone-White-RAF_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `GravestoneWhite` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `GravestoneWhite` | `T_PV_CrewItems_04` | `_BaseMap` |
| `Guitar` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `Guitar` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `HandwashBowls` | `Batch_03_2` | `_BaseMap` |
| `Hangers` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `Hangers` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Jukebox` | `T_PP_Entertainment_O4` | `_BaseMap` |
| `KickstarterBackerMonument` | `Kickstarter-BackerMonument_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `KickstarterBackerMonument` | `Kickstarter-BackerMonument_Toon-Main_Specular_1001` | `_SpecularMap` |
| `KickstarterCustomMonument` | `Kickstarter-BackerMonument_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `KickstarterCustomMonument` | `Kickstarter-BackerMonument_Toon-Main_Specular_1001` | `_SpecularMap` |
| `LiquorShelf` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `Lookout` | `Lookout_Toon-Opaque_1001` | `_BaseMap` |
| `Lookout` | `Lookout_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `Lookout` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `Lookout` | `T_PV_CrewItems_04` | `_BaseMap` |
| `Lookout` | `T_SR_Resource_05_1` | `_BaseMap` |
| `MedicineCabinet` | `Batch_03_2` | `_BaseMap` |
| `MetalBoxSmall` | `T_Batch_02_1_BC` | `_BaseMap` |
| `MetalFenceEdge` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `MetalFenceEdge` | `T_Batch_02_2_BC` | `_BaseMap` |
| `MetalShelf` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `MetalShelf` | `T_Batch_02_2_BC` | `_BaseMap` |
| `MetalShelfClosedClothes` | `MetalShelf-Closed-Clothes_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `MetalShelfClosedFiles` | `MetalShelf-Closed-Files_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `NightTable` | `Batch_03_2` | `_BaseMap` |
| `OerlikonGun` | `Batch_03_1` | `_BaseMap` |
| `OerlikonGun` | `Oerlikon20mmAAgun_Toon-Opaque_1001` | `_BaseMap` |
| `OerlikonGun` | `projectiles` | `_BaseMap` |
| `OxygenBottle` | `Batch_03_2` | `_BaseMap` |
| `Piano` | `T_PP_Entertainment_O4` | `_BaseMap` |
| `PilotBoard` | `PilotBoard_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `PilotBoard` | `PilotBoard_Toon-Main_Specular_1001` | `_SpecularMap` |
| `PlanningBoard` | `M_Navigation Simple_AlbedoTransparency` | `_BaseMap` |
| `PlanningBoard` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `PolishPilotsFlag` | `PolishPilotsFlag_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster01` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster01` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster02` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster02` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster03` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster03` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster04` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster04` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster05` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster05` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster06` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster06` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster07` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster07` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster08` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster08` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster09` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster09` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster10` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster10` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster11` | `Poster_Substance_M_Poster_BaseMap` | `_BaseMap` |
| `Poster11` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster12` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster12` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster13` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster13` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster14` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster14` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster15` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster15` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster16` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster16` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster17` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster17` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster18` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster18` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster19` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster19` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster20` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster20` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Poster21` | `Posters-WoV_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Poster21` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Radio` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RadioTower` | `Radiotower+Siren_M_Radiotower_Siren_BaseMap` | `_BaseMap` |
| `Roadblock` | `PolygonWar_Texture_01_A` | `_BaseMap` |
| `Roadblock` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RollableScaffolding` | `Batch_03_2` | `_BaseMap` |
| `RollableToolTable` | `Batch_03_2` | `_BaseMap` |
| `RugBedrug` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugBedrug` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugBedrugSmall` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugBedrugSmall` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugCubismrug` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugCubismrug` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugDoormat` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugDoormat` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugJuterug` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugJuterug` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugKitchenrug` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugKitchenrug` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `RugPersian` | `Initial_Decoration_Substance_M_Decoration_BaseMap` | `_BaseMap` |
| `RugPersian` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `SandbagFence1mCorner` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `SandbagFence1mCorner` | `T_Batch_01_BC` | `_BaseMap` |
| `SandbagFence1mStraight` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `SandbagFence1mStraight` | `T_Batch_01_BC` | `_BaseMap` |
| `ScrambleBell` | `Scramble-Bell_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `ScrambleBell` | `Scramble-Bell_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `Searchlight` | `T_PP_Defense_O4` | `_BaseMap` |
| `Searchlight` | `small_opacity_gradient_up` | `_BaseMap` |
| `Shelf` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ShelfBooks` | `Books-Personal_Toon-Main_1001` | `_BaseMap` |
| `ShelfBooks` | `Books-Personal_Toon-Main_1002` | `_BaseMap1002` |
| `ShelfBooks` | `Books-Personal_Toon-Main_1003` | `_BaseMap1003` |
| `ShelfBooks` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ShelfFolders` | `Folder-GB_Toon-Main_1001` | `_BaseMap` |
| `ShelfFolders` | `Folder-GB_Toon-Main_1002` | `_BaseMap1002` |
| `ShelfFolders` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ShelfFolders` | `Typewriter-Table_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `ShelfFolders` | `Typewriter-Table_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `ShelfPersonalStuff` | `Books-Personal_Toon-Main_1001` | `_BaseMap` |
| `ShelfPersonalStuff` | `Books-Personal_Toon-Main_1002` | `_BaseMap1002` |
| `ShelfPersonalStuff` | `Books-Personal_Toon-Main_1003` | `_BaseMap1003` |
| `ShelfPersonalStuff` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `ShelfPersonalStuff` | `Shelf-Personal-Stuff_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `ShelfPersonalStuff` | `Shelf-Personal-Stuff_Toon-Main_Specular_1001` | `_SpecularMap` |
| `ShelfPersonalStuff` | `TIG_Colors_01` | `_BaseMap` |
| `Sickbed` | `T_PP_Lazarett_O4` | `_BaseMap` |
| `SirenOnPole` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `SirenOnPole` | `Radiotower+Siren_M_Radiotower_Siren_BaseMap` | `_BaseMap` |
| `SmallFuelTank` | `Fuel-Tank-Small_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `SmallFuelTank` | `Fuel-Tank-Small_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `SmallFuelTank` | `T_Batch_02_1_BC` | `_BaseMap` |
| `SmallLoungeTable` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `SmallLoungeTable` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Stepladder` | `Batch_03_2` | `_BaseMap` |
| `StoveSmall` | `Stove-Small_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `StoveSmall` | `Stove-Small_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `TableMetal` | `TableMetal_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `TableMetal` | `TableMetal_Toon-Main_Specular_1001` | `_SpecularMap` |
| `TableOutdoor` | `TableOutdoor_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `TableTypewriter` | `Typewriter-Table_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `TableTypewriter` | `Typewriter-Table_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `Toilet` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `Toolbox` | `Batch_03_2` | `_BaseMap` |
| `VickersGunAA` | `Batch_03_1` | `_BaseMap` |
| `VickersGunAA` | `projectiles` | `_BaseMap` |
| `WallPhone` | `Wall-Phone_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallPhone` | `Wall-Phone_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WallSign1` | `Signs-RAF-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallSign1` | `Signs-RAF-02_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WallSign2` | `Signs-RAF-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallSign2` | `Signs-RAF-02_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WallSign3` | `Signs-RAF-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallSign3` | `Signs-RAF-02_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WallSign4` | `Signs-RAF-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallSign4` | `Signs-RAF-02_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WallSign5` | `Signs-RAF-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WallSign5` | `Signs-RAF-02_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WarningSign1` | `WarningSigns_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `WarningSign1` | `WarningSigns_Toon-Main_Specular_1001` | `_SpecularMap` |
| `WarningSign2` | `WarningSigns_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `WarningSign2` | `WarningSigns_Toon-Main_Specular_1001` | `_SpecularMap` |
| `WarningSign3` | `WarningSigns_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `WarningSign3` | `WarningSigns_Toon-Main_Specular_1001` | `_SpecularMap` |
| `WarningSign4` | `WarningSigns_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `WarningSign4` | `WarningSigns_Toon-Main_Specular_1001` | `_SpecularMap` |
| `WarningSign5` | `WarningSigns_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `WarningSign5` | `WarningSigns_Toon-Main_Specular_1001` | `_SpecularMap` |
| `WaterPump` | `T_PP_WaterPump` | `_BaseMap` |
| `WaterTower` | `T_PP_WaterPump` | `_BaseMap` |
| `WaterTower` | `Water-Reservoir_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WaterTower` | `Water-Reservoir_Toon-Opaque_Specular_1001` | `_SpecularMap` |
| `WaySign1` | `Signs-RAF-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WaySign2` | `Signs-RAF-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WaySign3` | `Signs-RAF-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WaySign4` | `Signs-RAF-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WaySign5` | `Signs-RAF-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `WickerChair` | `WickerChair_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `Windhose` | `Batch_03_1` | `_BaseMap` |
| `WoodenChair` | `Bar_Items_Spread_Bar_Items_BaseMap` | `_BaseMap` |
| `WoodenFenceSimple` | `M_TO_Old-Fence_Base_color` | `_BaseMap` |
| `WoodenFenceSimplePole` | `M_TO_Old-Fence_Base_color` | `_BaseMap` |
| `WoodenFenceSturdyEdge` | `T_Batch_01_BC` | `_BaseMap` |
| `WoodenTableLarge` | `T_Batch_02_2_BC` | `_BaseMap` |
| `WoodenTableMedium` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `WoodenTableMedium` | `T_Batch_02_2_BC` | `_BaseMap` |
| `WoodenTableSmall` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `WoodenTableSmall` | `T_Batch_02_2_BC` | `_BaseMap` |

## Workbenches

| Object | Texture | Slot |
|---|---|---|
| `Brickstation` | `T_PP_Workbenches_05_1` | `_BaseMap` |
| `CanningStation` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `CementMixer` | `T_PP_Workbenches_05_1` | `_BaseMap` |
| `CementMixer` | `T_SR_Ressource_O4` | `_BaseMap` |
| `Distillery` | `T_PP_Workbenches_06_1` | `_BaseMap` |
| `ElectronicsWorkbench` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `ElectronicsWorkbench` | `T_SR_Resource_05_1` | `_BaseMap` |
| `EspionageRadio` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `EspionageRadio` | `T_PV_CrewItems_04` | `_BaseMap` |
| `FieldKitchen` | `Batch_03_1` | `_BaseMap` |
| `HerbDryer` | `T_PP_Workbenches_06_1` | `_BaseMap` |
| `HerbDryer` | `T_SR_Ressource_O4` | `_BaseMap` |
| `IndoorKitchen` | `T_PP_Workbenches_05_1` | `_BaseMap` |
| `MetalworksWorkbench` | `T_PP_Workbenches_05_1` | `_BaseMap` |
| `MetalworksWorkbench` | `T_PV_CrewItems_04` | `_BaseMap` |
| `MetalworksWorkbench` | `T_SR_Resource_05_2` | `_BaseMap` |
| `SawStation` | `T_PP_Workbenches_05_1` | `_BaseMap` |
| `SawStation` | `T_PV_CrewItems_04` | `_BaseMap` |
| `SawStation` | `leaf` | `_BaseMap` |
| `TailorStation` | `T_PP_Workbenches_05_2` | `_BaseMap` |
| `WaterCooker` | `T_PP_Workbenches_06_1` | `_BaseMap` |
| `WaterCooker` | `T_SR_Resource_05_1` | `_BaseMap` |

## Training objects

| Object | Texture | Slot |
|---|---|---|
| `BombingAdvancedSimulator` | `M_Bombing Advanced Simulator_AlbedoTransparency` | `_BaseMap` |
| `BombingAdvancedSimulator` | `M_Bombing Advanced Simulator_AlbedoTransparency_1` | `_BaseMap` |
| `BombingAdvancedSimulator` | `M_Bombing Advanced Simulator_AlbedoTransparency_2` | `_BaseMap` |
| `BombingSimpleBench` | `M Bombing Simple Bench_AlbedoTransparency` | `_BaseMap` |
| `BombingSimpleBench` | `T_Batch_02_1_BC` | `_BaseMap` |
| `EnduranceAdvancedBikeExerciser` | `T_Batch_02_2_BC` | `_BaseMap` |
| `EnduranceSimpleRack` | `M Endurance Simple Rack_AlbedoTransparency` | `_BaseMap` |
| `EngineeringAdvancedEngine` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-Main_BaseMap_1001` | `_BaseMap` |
| `EngineeringAdvancedEngine` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-Main_BaseMap_1002` | `_BaseMap1002` |
| `EngineeringAdvancedEngine` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-Main_Specular_1001` | `_SpecularMap` |
| `EngineeringAdvancedEngine` | `Gloster-Gladiator_MK01_Temperate-Land_Toon-Main_Specular_1002` | `_SpecularMap1002` |
| `EngineeringAdvancedEngine` | `M_Engineering Advanced Engine_AlbedoTransparency` | `_BaseMap` |
| `EngineeringSimpleMechanicWorkstation` | `M_Engineering Simple Workstation_AlbedoTransparency` | `_BaseMap` |
| `EngineeringSimpleMechanicWorkstation` | `T_Batch_02_2_BC` | `_BaseMap` |
| `EngineeringSimpleMechanicWorkstation` | `T_PV_CrewItems_04` | `_BaseMap` |
| `FlyingAdvancedLinkTrainer` | `M_Flying Advanced Link Trainer_AlbedoTransparency` | `_BaseMap` |
| `FlyingSimpleWoodenConstruction` | `M_Flying Simple Wooden Construction_AlbedoTransparency` | `_BaseMap` |
| `FlyingSimpleWoodenConstruction` | `M_Flying Simple Wooden Construction_AlbedoTransparency_1` | `_BaseMap` |
| `NavigationAdvancedNaviTrainer` | `M Navigation Advanced Trainer Navi_Trainer_AlbedoTransparency` | `_BaseMap` |
| `NavigationSimpleBoard` | `M_Navigation Simple_AlbedoTransparency` | `_BaseMap` |
| `ShootingAdvancedTurret` | `BB0855_Ground_Bunker_M_BB_Bunker_BaseMap` | `_BaseMap` |
| `ShootingAdvancedTurret` | `Batch_03_1` | `_BaseMap` |
| `ShootingAdvancedTurret` | `M_Shooting Advvanced Turret_AlbedoTransparency` | `_BaseMap` |
| `ShootingSimpleTargetRange` | `Batch_03_1` | `_BaseMap` |
| `ShootingSimpleTargetRange` | `M_Rifle_LeeEnfield_AlbedoTransparency` | `_BaseMap` |
