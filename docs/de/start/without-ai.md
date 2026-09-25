# Ohne KI-Agent

Alles, was ein Agent macht, kannst du auch von Hand machen. Dafür gibt es zwei Wege.

## Der einfachste Weg: der Mission Editor im Spiel { #the-easiest-route-the-in-game-mission-editor }

Keine Werkzeuge, kein Terminal. Öffne im Hauptmenü den **Mission Editor**, leg eine Mission an, füll die Felder aus und speichere. Der Editor prüft deine Mission beim Speichern und weigert sich, eine zu speichern, die etwas kaputt machen würde. Missionen, die du dort speicherst, landen im Ordner `Missions` neben dem `Mods`-Ordner des Spiels und werden beim nächsten Spiel geladen.

Eine geführte Tour findest du unter [Deine erste Mission schreiben](../missions/first-mission.md).

## Der handgemachte Weg: Beispiel kopieren und bearbeiten { #the-hand-made-route-copy-an-example-and-edit-it }

So bekommst du einen echten Mod-Ordner, den du später im Steam Workshop teilen kannst. Du brauchst einen Texteditor und, für die Prüfung in Schritt 4, Python (siehe die Installationsseiten für [Windows](install-windows.md#6-optional-install-python-recommended) oder [Mac](install-mac.md#5-optional-install-python-recommended)). Außerdem brauchst du das Modkit auf deinem Computer, entweder mit `gh repo clone blindflugstudios/goa-modkit` oder als Download von [der GitHub-Seite](https://github.com/blindflugstudios/goa-modkit) (grüner **Code**-Knopf → **Download ZIP**, dann entpacken).

### 1. Hol dir einen richtigen Texteditor { #1-get-a-proper-text-editor }

Nimm **[Visual Studio Code](https://code.visualstudio.com/)** (kostenlos, für Windows und Mac). Er färbt JSON und Python ein, zeigt Fehler wie ein fehlendes Komma an und lässt dich mit **File → Open Folder** (bzw. **Datei → Ordner öffnen**) den ganzen Modkit-Ordner öffnen. Editor (Notepad) und TextEdit gehen zur Not auch, aber TextEdit muss im reinen Textmodus sein (**Format → In reinen Text umwandeln**).

### 2. Kopiere das Beispiel { #2-copy-the-example }

Leg im Modkit diese Ordnerstruktur an und kopiere die beiden Dateien aus `examples/coastal_patrol/` hinein:

```text
goa-modkit/
  mods/
    my_first_mod/
      Missions/
        coastal_patrol.json
        coastal_patrol.py
```

Der Ordnername `Missions` ist wichtig: Das Spiel sucht Inhalte anhand der Ordnernamen. Den Namen des Mod-Ordners (`my_first_mod`) kannst du frei wählen.

### 3. Bearbeite es { #3-edit-it }

Öffne `coastal_patrol.json`. Probier erst kleine Änderungen, speichere und prüf jede einzeln:

```json
"_maxPlaneSlots": 2,
"_asPlannedChance": 80,
```

Setz `_maxPlaneSlots` auf `3`, um drei Flugzeuge zu erlauben, oder senke `_asPlannedChance`, damit öfter etwas schiefgeht.

Öffne `coastal_patrol.py` und ändere die Texte zwischen den Anführungszeichen, zum Beispiel den Missionsnamen:

```python
_term("mission_name", "Coastal Patrol")
```

!!! warning "Drei Dinge, die du nicht kaputt machen darfst"
    - `_missionOutcomes` muss **genau 4** Einträge haben, in ihrer festen Reihenfolge.
    - `_missionStats` muss **mindestens 2** Einträge haben.
    - Die Dateinamen und die ID, die `get_mission_id` in der `.py` zurückgibt, müssen übereinstimmen. Wenn du die Mission umbenennst, benenne beide Dateien und die Zeile `MISSION_ID` gemeinsam um.

    Die [Missions-Referenz](../missions/reference.md) erklärt jedes Feld.

### 4. Prüf es mit dem Validator {#4-check-it-with-the-validator}

Der **Validator** liest deinen Mod und sagt dir, was im Spiel schiefgehen würde, ohne dass du das Spiel starten musst. Öffne das Terminal im Modkit-Ordner und führ aus:

=== "Windows"

    ```powershell
    cd ~\goa-modkit
    python tools\validator\goa_validate.py mods\my_first_mod
    ```

=== "Mac"

    ```bash
    cd ~/goa-modkit
    python3 tools/validator/goa_validate.py mods/my_first_mod
    ```

**Das solltest du sehen:** eine Zusammenfassung wie `2 file(s) checked - 0 error(s), 0 warning(s), 0 note(s)`.

Jedes Problem wird als `file:line: error: ...` ausgegeben, mit einem Hinweis darunter. Korrigiere die genannte Zeile, speichere und prüf erneut. Fehler (errors) müssen weg. Warnungen (warnings) solltest du lesen.

### 5. Kopiere es ins Spiel { #5-copy-it-into-the-game }

Kopiere den ganzen Ordner `my_first_mod` in den `Mods`-Ordner des Spiels. Am schnellsten öffnest du diesen Ordner im Hauptmenü des Spiels über **Mods → Open folder**. Oder du fügst den Pfad im Explorer bzw. Finder ein:

=== "Windows"

    In die Adressleiste des Explorers einfügen:

    ```text
    %USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Mods\
    ```

=== "Mac"

    Im Finder **Cmd+Shift+G** drücken und einfügen:

    ```text
    ~/Library/Application Support/Blindflug Studios/Ground Of Aces/Mods/
    ```

Kopiere den Ordner, leg keine Verknüpfung und keinen Alias an: Das Spiel überspringt verlinkte Ordner.

### 6. Laden und losfliegen { #6-load-it-and-fly }

1. Ist ein Spielstand offen: **Einstellungen** (Options) **→ Verlassen zum Hauptmenü** (Quit to main menu).
2. Öffne **Mods**. Dein Mod steht in der Liste. Weil er eine `.py`-Datei hat, zeigt er auch einen **Scripting**-Schalter: Schalte ihn ein und bestätige (das aktuelle Spiel führt die Skripte ohnehin aus).
3. Lade deinen Spielstand.
4. Schalte **Einstellungen → Cheats** ein, öffne die Konsole mit dem Cheat-Knopf und tippe `create_mission coastal_patrol`. Die Mission erscheint auf der Kriegskarte.

Nach jeder späteren Änderung: prüfen, erneut kopieren (alte Dateien ersetzen), **Verlassen zum Hauptmenü**, Spielstand laden (öffne vorher **Mods**, wenn du einen neuen Ordner wie `Quests/` angelegt hast).

Es passiert nichts? Siehe [Wenn nichts passiert](troubleshooting.md).
