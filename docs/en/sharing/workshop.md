# Steam Workshop

The Steam Workshop is how a finished mod reaches other players. You upload from inside the game, players subscribe on the Workshop page, and Steam delivers the mod to them. Players who do not use the Workshop can still install a mod by copying its folder by hand.

Workshop page for Ground of Aces: <https://steamcommunity.com/app/2308690/workshop/>

!!! note "Steam version only"
    The Workshop needs the Steam version of the game, started through Steam. DRM-free builds (for example from a store without a Workshop) have no Workshop at all: they list no Workshop mods, and the **Upload** button only reports that Steam is not available. Mods in your own `Mods` folder work the same in every version, so players of a DRM-free build [install by hand](#installing-a-mod-by-hand).

## Uploading your mod

1. **Make the folder exactly what you want to ship.** The *whole* mod folder is uploaded as it is - `config.json`, `preview.png` and every content subfolder. Remove test files, backups and notes you do not want to publish first.
2. **Give it a name and a picture.** The `Name` in `config.json` becomes the Workshop title on a first upload (without a `config.json` the folder name is used). `preview.png` at the root of the mod folder becomes the Workshop picture on a first upload. It must be a PNG of **at most 1 MB**; a larger file makes the upload fail with an error.
3. **Open Main menu → Mods** and press **Upload** on the mod. Only your own mods (from your `Mods` folder) have this button; Workshop items you are subscribed to do not.
4. **Pick the target.** A window lists **New Workshop item** followed by every Workshop item you have published before. Pick **New Workshop item** for a first upload, or one of your existing items to replace its contents with this version.
5. **Confirm.** The game asks once more - "Do you want to create a new Workshop item for ...?" or, for an update, whether to use the existing item - and you answer **Yes**.
6. **Wait for the upload.** The window shows a progress bar. When the upload is done, the window shows the item's Workshop link.

What the game sends with the upload:

| Part | New item | Update of an existing item |
|---|---|---|
| Files | the whole mod folder | the whole mod folder, replacing the old files |
| Title | the mod's `Name` | left as it is |
| Description | none | left as it is |
| Picture | `preview.png`, if there is one | left as it is |
| Visibility | public | public |
| Workshop tag | `Mod` | `Mod` |

The description is always written on the item's Steam page; the game never sends one. An update replaces the files only: to change the title or the picture of an item you already published, edit them on the Steam page too.

!!! tip
    Steam may ask you to accept the Workshop legal agreement the first time you publish. Until you do, the item stays hidden. Open the item's Steam page and accept the agreement there, and the item becomes visible.

### Keep working after you publish

Your own copy in `Mods` always wins over the Workshop copy of the same mod (see [Which mod wins](../basics/mods.md#which-mod-wins)). So you can stay subscribed to your published mod, keep editing the local folder, test, and upload again when you are happy. Pick your existing item in step 4 so players get the update instead of a second item.

Before you upload an update, think about players who are in the middle of a playthrough with your mod. Removing a quest, renaming a mission id or changing the order of quest steps can strand them. The [Quests](../quests/index.md#saves-and-removing-a-mod) page explains what happens to quests in a running save.

### When the upload fails

| What you see | What to do |
|---|---|
| Steam not available | Start the game through Steam. In a DRM-free build there is no Workshop. |
| An error while fetching your items | Check that Steam is online, then press **Upload** again. |
| An upload error naming the preview image | Make `preview.png` smaller than 1 MB (a smaller resolution, or fewer colours). |
| Any other upload error | The message includes Steam's error code. Try again later; if it keeps happening, ask in the [Discord modding channel](https://discord.com/channels/1006159027157356587/1551969822911242240). |

## Installing a mod from the Workshop

Subscribe to the item on the Steam Workshop. Steam downloads it into its own Workshop folder - nothing lands in your `Mods` folder - and the game lists it in the Mods window the next time it starts, or after you press **Refresh**. It is switched on by default and marked as a Workshop item. An item that Steam is still downloading does not appear until the download has finished.

The **Workshop** button in the Mods window opens the game's Workshop page in the Steam overlay, so you can browse and subscribe without leaving the game. Press **Refresh** afterwards.

Unsubscribing removes the mod again. Saves that used the mod keep loading. What happens to the content the mod added depends on the kind of content; for quests, see [Quests](../quests/index.md#saves-and-removing-a-mod).

## Installing a mod by hand

Copy the mod's folder into your `Mods` folder so that its `config.json` or its content subfolders sit directly inside it:

```text
Mods/some_mod/CSV/...            correct
Mods/some_mod/some_mod/CSV/...   wrong - one folder too deep
```

A mod you downloaded as a `.zip` usually needs to be unpacked first; check that unpacking did not add that extra folder level. Then press **Refresh** in the Mods window or restart the game.

Where the `Mods` folder is on each platform is listed on [How mods work](../basics/mods.md#where-mods-live). The quickest way there is **Main menu → Mods → Open folder**.

!!! warning
    A mod can contain Python scripts, and scripts run whenever the mod is enabled. Only install mods from people you trust, and read [Python mods and safety](../basics/security.md) first.
