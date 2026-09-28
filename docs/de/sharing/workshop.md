# Steam Workshop

Über den Steam Workshop kommt eine fertige Mod zu anderen Spielern. Du lädst sie direkt aus dem Spiel hoch, Spieler abonnieren sie auf der Workshop-Seite, und Steam liefert die Mod zu ihnen aus. Wer den Workshop nicht nutzt, kann eine Mod trotzdem installieren, indem er ihren Ordner von Hand kopiert.

Workshop-Seite von Ground of Aces: <https://steamcommunity.com/app/2308690/workshop/>

!!! note "Nur Steam-Version"
    Der Workshop braucht die Steam-Version des Spiels, gestartet über Steam. DRM-freie Versionen (zum Beispiel aus einem Store ohne Workshop) haben überhaupt keinen Workshop: Sie listen keine Workshop-Mods auf, und der Button **Upload** meldet nur, dass Steam nicht verfügbar ist. Mods in deinem eigenen `Mods`-Ordner funktionieren in jeder Version gleich, Spieler einer DRM-freien Version [installieren also von Hand](#installing-a-mod-by-hand).

## Deine Mod hochladen { #uploading-your-mod }

1. **Bring den Ordner genau in den Zustand, den du ausliefern willst.** Der *ganze* Mod-Ordner wird so hochgeladen, wie er ist - `config.json`, `preview.png` und jeder Inhaltsunterordner. Entferne vorher Testdateien, Backups und Notizen, die du nicht veröffentlichen willst.
2. **Gib ihr einen Namen und ein Bild.** Der `Name` in der `config.json` wird beim ersten Upload zum Workshop-Titel (ohne `config.json` wird der Ordnername verwendet). Die `preview.png` im Hauptverzeichnis des Mod-Ordners wird beim ersten Upload zum Workshop-Bild. Sie muss ein PNG mit **höchstens 1 MB** sein; eine größere Datei lässt den Upload mit einem Fehler scheitern.
3. **Öffne Hauptmenü (Main menu) → Mods** und drück bei der Mod auf **Upload**. Nur deine eigenen Mods (aus deinem `Mods`-Ordner) haben diesen Button; abonnierte Workshop-Items nicht.
4. **Wähl das Ziel.** Ein Fenster listet **New Workshop item** und darunter jedes Workshop-Item, das du bisher veröffentlicht hast. Wähl **New Workshop item** für einen ersten Upload oder eines deiner bestehenden Items, um dessen Inhalt durch diese Version zu ersetzen.
5. **Bestätige.** Das Spiel fragt noch einmal nach - "Do you want to create a new Workshop item for ...?" oder, bei einem Update, ob das bestehende Item verwendet werden soll - und du antwortest mit **Ja (Yes)**.
6. **Warte auf den Upload.** Das Fenster zeigt einen Fortschrittsbalken. Wenn der Upload fertig ist, zeigt das Fenster den Workshop-Link des Items.

Was das Spiel beim Upload mitschickt:

| Teil | Neues Item | Update eines bestehenden Items |
|---|---|---|
| Dateien | der ganze Mod-Ordner | der ganze Mod-Ordner, ersetzt die alten Dateien |
| Titel | der `Name` der Mod | bleibt unverändert |
| Beschreibung | keine | bleibt unverändert |
| Bild | `preview.png`, falls vorhanden | bleibt unverändert |
| Sichtbarkeit | öffentlich | öffentlich |
| Workshop-Tag | `Mod` | `Mod` |

Die Beschreibung schreibst du immer auf der Steam-Seite des Items; das Spiel schickt nie eine mit. Ein Update ersetzt nur die Dateien: Titel und Bild eines bereits veröffentlichten Items änderst du ebenfalls auf der Steam-Seite.

!!! tip
    Beim ersten Veröffentlichen bittet dich Steam eventuell, der rechtlichen Vereinbarung für den Workshop zuzustimmen. Bis du das tust, bleibt das Item versteckt. Öffne die Steam-Seite des Items und stimm dort zu, dann wird das Item sichtbar.

### Nach dem Veröffentlichen weiterarbeiten { #keep-working-after-you-publish }

Deine eigene Kopie in `Mods` gewinnt immer gegen die Workshop-Kopie derselben Mod (siehe [Welche Mod gewinnt](../basics/mods.md#which-mod-wins)). Du kannst also deine veröffentlichte Mod weiter abonniert lassen, den lokalen Ordner weiterbearbeiten, testen und erneut hochladen, wenn du zufrieden bist. Wähl in Schritt 4 dein bestehendes Item, damit die Spieler das Update bekommen statt eines zweiten Items.

Bevor du ein Update hochlädst, denk an die Spieler, die gerade mitten in einem Durchlauf mit deiner Mod stecken. Eine Quest zu entfernen, eine Missions-Id umzubenennen oder die Reihenfolge von Quest-Schritten zu ändern, kann sie festsitzen lassen. Die Seite [Quests](../quests/index.md#saves-and-removing-a-mod) erklärt, was mit Quests in einem laufenden Spielstand passiert.

### Wenn der Upload scheitert { #when-the-upload-fails }

| Was du siehst | Was du tun kannst |
|---|---|
| Steam nicht verfügbar | Starte das Spiel über Steam. In einer DRM-freien Version gibt es keinen Workshop. |
| Ein Fehler beim Abrufen deiner Items | Prüf, ob Steam online ist, und drück dann erneut auf **Upload**. |
| Ein Upload-Fehler, der das Vorschaubild nennt | Mach die `preview.png` kleiner als 1 MB (geringere Auflösung oder weniger Farben). |
| Jeder andere Upload-Fehler | Die Meldung enthält Steams Fehlercode. Versuch es später noch einmal; wenn es immer wieder passiert, frag im [Modding-Channel auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240). |

## Eine Mod aus dem Workshop installieren { #installing-a-mod-from-the-workshop }

Abonniere das Item im Steam Workshop. Steam lädt es in seinen eigenen Workshop-Ordner herunter - in deinem `Mods`-Ordner landet nichts - und das Spiel listet es beim nächsten Start im Mods-Fenster auf, oder nachdem du auf **Refresh** gedrückt hast. Es ist standardmäßig eingeschaltet und als Workshop-Item markiert. Ein Item, das Steam noch herunterlädt, erscheint erst, wenn der Download fertig ist.

Der Button **Workshop** im Mods-Fenster öffnet die Workshop-Seite des Spiels im Steam-Overlay, so kannst du stöbern und abonnieren, ohne das Spiel zu verlassen. Drück danach auf **Refresh**.

Wenn du das Abo kündigst, wird die Mod wieder entfernt. Spielstände, die die Mod verwendet haben, lassen sich weiterhin laden. Was mit den Inhalten passiert, die die Mod hinzugefügt hat, hängt von der Art des Inhalts ab; zu Quests siehe [Quests](../quests/index.md#saves-and-removing-a-mod).

## Eine Mod von Hand installieren { #installing-a-mod-by-hand }

Kopiere den Ordner der Mod so in deinen `Mods`-Ordner, dass ihre `config.json` oder ihre Inhaltsunterordner direkt darin liegen:

```text
Mods/some_mod/CSV/...            correct
Mods/some_mod/some_mod/CSV/...   wrong - one folder too deep
```

Eine als `.zip` heruntergeladene Mod musst du meist erst entpacken; prüf, dass beim Entpacken keine zusätzliche Ordnerebene entstanden ist. Drück dann im Mods-Fenster auf **Refresh** oder starte das Spiel neu.

Wo der `Mods`-Ordner auf jeder Plattform liegt, steht unter [So funktionieren Mods](../basics/mods.md#where-mods-live). Am schnellsten kommst du über **Hauptmenü → Mods → Open folder** dorthin.

!!! warning
    Eine Mod kann Python-Skripte enthalten, und Skripte laufen immer, wenn die Mod eingeschaltet ist. Installiere Mods nur von Leuten, denen du vertraust, und lies vorher [Python-Mods und Sicherheit](../basics/security.md).
