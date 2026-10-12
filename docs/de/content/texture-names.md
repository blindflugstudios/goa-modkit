# Eingebaute Texturnamen

Eine PNG im Ordner `Objects/` deiner Mod, die genauso heißt wie eine der Texturen des Spiels, **ersetzt diese Textur** auf jedem Objekt, das sie verwendet. Dafür brauchst du kein Modell: Das Spiel behält sein eigenes Modell und malt dein Bild darauf. `Objects/BedMetal_Toon-Main_BaseMap_1001.png` zum Beispiel übermalt das Metallbett. Die Regeln stehen unter [Objekte und Modelle](objects.md#re-painting-without-a-model).

Manche Texturen teilen sich mehrere Objekte. So eine Textur steht unter jedem davon, und wenn du sie ersetzt, ändern sich alle auf einmal. Male deinen Ersatz in derselben Größe und Aufteilung wie das Original, denn das Modell bleibt das des Spiels.

Die Spalte **Slot** sagt, was die Textur auf dem Objekt macht:

| Slot | Was er enthält |
|---|---|
| `_BaseMap` | die Grundfarbe; bei Objekten mit mehreren Kacheln die Kachel 1001 (UVs mit U von 0 bis 1) |
| `_BaseMap1002`, `_BaseMap1003` | die Grundfarbe der Kacheln 1002 (U von 1 bis 2) und 1003 (U ab 2) |
| `_SpecularMap` | die Glanzfarbe, also wie stark jede Stelle glänzt; bei Objekten mit mehreren Kacheln die Kachel 1001 |
| `_SpecularMap1002`, `_SpecularMap1003` | die Glanzfarbe der Kacheln 1002 und 1003 |

Der Slot dient nur zur Information: Deine Datei benennst du nach der **Textur**, nie nach dem Slot. Andere Slots, die das Spiel intern verwendet (zum Beispiel für Kampfschäden, Schnee oder das Ausblenden), fehlen in diesen Tabellen absichtlich.

Diese Tabellen stammen aus der vom Spiel erzeugten Texturliste, Stand 2026-10-01.

## Objekte aus dem Baumenü { #objects-from-the-build-menu }

| Objekt | Textur | Slot |
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

## Werkbänke { #workbenches }

| Objekt | Textur | Slot |
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

## Trainingsobjekte { #training-objects }

| Objekt | Textur | Slot |
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

## Kartenobjekte { #map-objects }

Bäume, Felsen, Teiche und die anderen Objekte auf einer Karte. Mehrere davon teilen sich eine Textur, allen voran `T_PP_ResourceMap_O4`: Ersetzt du sie, änderst du jedes Kartenobjekt, das mit ihr aufgeführt ist. Um nur eines davon zu ändern, gib ihm ein Modell (siehe [Kartenobjekte](objects.md#map-objects)).

| Objekt | Textur | Slot |
|---|---|---|
| `berry_bush` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `berry_bush` | `leaf` | `_BaseMap` |
| `bush` | `Bush07-Cowparsley_Toon-Opaque_1001` | `_BaseMap` |
| `bush` | `T_Bush01_d` | `_BaseMap` |
| `bush` | `T_Bush02_d` | `_BaseMap` |
| `bush` | `T_Bush03_d` | `_BaseMap` |
| `bush` | `T_Bush04_d` | `_BaseMap` |
| `bush` | `T_Bush05_d` | `_BaseMap` |
| `bush` | `T_Bush05_s` | `_SpecularMap` |
| `bush_big` | `Bush06-Blackthorn_Toon-Opaque_1001` | `_BaseMap` |
| `clay_pit` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `damaged_car` | `M_TO_Car-Damaged_Base_color` | `_BaseMap` |
| `flowers` | `Flowers-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `flowers` | `Flowers-03_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `herbs_plant` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `herbs_plant` | `leaf` | `_BaseMap` |
| `large_rock` | `Rock-Large-Round-Moss_Toon-Opaque_1001` | `_BaseMap` |
| `large_rock` | `Rock-Large-Round_Toon-Opaque_1001` | `_BaseMap` |
| `large_rock` | `T_PP_Cosmetic_O4` | `_BaseMap` |
| `long_rock` | `Rocks-Moss_Toon-Opaque_1001` | `_BaseMap` |
| `long_rock` | `T_PP_Cosmetic_O4` | `_BaseMap` |
| `mushroom_patch` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `mushroom_patch` | `leaf` | `_BaseMap` |
| `old_fence` | `M_TO_Old-Fence_Base_color` | `_BaseMap` |
| `old_fence_pole` | `M_TO_Old-Fence_Base_color` | `_BaseMap` |
| `old_grave` | `Batch_03_1` | `_BaseMap` |
| `old_grave` | `Props-01_AlbedoTransparency` | `_BaseMap` |
| `old_headstone` | `Batch_03_1` | `_BaseMap` |
| `old_headstone` | `GraveStone-White-RAF_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `sand_pit` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `small_rock` | `Rock-Standard-Round_Toon-UDIM_BaseMap_1001` | `_BaseMap` |
| `small_rock` | `Rock-Standard-Round_Toon-UDIM_BaseMap_1002` | `_BaseMap1002` |
| `small_rock` | `Rocks-Moss_Toon-Opaque_1001` | `_BaseMap` |
| `tree` | `Broadleaf_Mobile_Atlas 1` | `_BaseMap` |
| `tree` | `Broadleaf_Mobile_Atlas Low` | `_BaseMap` |
| `tree` | `Conifer_Desktop_Atlas` | `_BaseMap` |
| `tree_big` | `OakTree-01-Bark_Toon-Opaque_1001` | `_BaseMap` |
| `tree_big` | `OakTree-02-Bark_Toon-Opaque_1001` | `_BaseMap` |
| `tree_big` | `OakTree-Leaf_Toon-Opaque_1001` | `_BaseMap` |
| `tree_big_log` | `TreeLog-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `tree_big_log` | `TreeLog-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `tree_big_stump` | `TreeStump-01_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `tree_big_stump` | `TreeStump-02_Toon-Opaque_BaseMap_1001` | `_BaseMap` |
| `water_pond` | `T_PP_ResourceMap_O4` | `_BaseMap` |
| `wild_beans` | `Batch_03_1` | `_BaseMap` |
| `wild_beans` | `T_Batch_02_2_BC` | `_BaseMap` |
| `wild_beans` | `leaf` | `_BaseMap` |
| `wild_grain` | `T_Batch_02_2_BC` | `_BaseMap` |
| `wild_grain` | `leaf` | `_BaseMap` |
| `wild_potato` | `T_Batch_02_2_BC` | `_BaseMap` |
| `wild_potato` | `leaf` | `_BaseMap` |
| `wild_tomato` | `T_Batch_02_2_BC` | `_BaseMap` |
| `wild_tomato` | `leaf` | `_BaseMap` |
| `young_tree` | `Broadleaf_Mobile_Atlas 1` | `_BaseMap` |
| `young_tree` | `Broadleaf_Mobile_Atlas Low` | `_BaseMap` |
| `young_tree` | `Conifer_Desktop_Atlas` | `_BaseMap` |
| `young_tree_big` | `OakTree-01-Bark_Toon-Opaque_1001` | `_BaseMap` |
| `young_tree_big` | `OakTree-02-Bark_Toon-Opaque_1001` | `_BaseMap` |
| `young_tree_big` | `OakTree-Leaf_Toon-Opaque_1001` | `_BaseMap` |
