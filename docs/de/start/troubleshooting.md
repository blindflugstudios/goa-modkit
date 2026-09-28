# Wenn nichts passiert

Die meisten Mod-Probleme haben eine Handvoll Ursachen. Such dein Symptom und probier die Lösung aus. Wenn du einen Agenten nutzt, reicht oft ein einziger Satz: `read my Player.log and tell me what went wrong`.

## Immer zuerst { #first-always }

1. **Lass den Validator** über deinen Mod laufen. Er findet die meisten der Probleme unten, bevor das Spiel sie überhaupt zu sehen bekommt. Bitte den Agenten `validate my mod` oder siehe [Ohne KI-Agent](without-ai.md#4-check-it-with-the-validator).
2. **Richtig neu laden**: **Einstellungen** (Options) **→ Verlassen zum Hauptmenü** (Quit to main menu), dann den Spielstand laden. Hast du einen neuen Mod-Ordner (oder einen neuen Inhaltsordner wie `Quests/`) angelegt, öffne vorher **Mods** und drück auf **Refresh**. Im Zweifel das Spiel neu starten.

## Symptom, Ursache, Lösung { #symptom-cause-fix }

| Symptom | Wahrscheinliche Ursache | Lösung |
|---|---|---|
| **`gh repo clone` meldet "To get started with GitHub CLI, please run: gh auth login"** | Die GitHub-Anmeldung wurde nicht abgeschlossen - meist wurde das Terminal geschlossen oder benutzt, bevor `✓ Logged in` erschien. Es wurde kein Ordner `goa-modkit` angelegt, deshalb schlägt auch `cd goa-modkit` fehl. | Führ `gh auth login` noch einmal aus und geh die Browser-Schritte auf der Installationsseite bis zum Ende durch. `gh auth status` zeigt, ob du angemeldet bist. |
| **`gh repo clone` meldet "Could not resolve to a Repository"** | Du bist angemeldet, hast aber noch keinen Zugang zum privaten Modkit oder die Einladung noch nicht angenommen. | Nimm sie unter [github.com/blindflugstudios/goa-modkit/invitations](https://github.com/blindflugstudios/goa-modkit/invitations) an. Keine Einladung? Siehe [Zuerst Zugang holen](index.md#get-access-first). |
| **"Python wurde nicht gefunden", obwohl Python installiert ist (Windows)** | Ein falsches `python` aus dem Microsoft Store verdeckt das echte. | Nimm `py` statt `python` oder schalte die App-Ausführungsaliase aus - siehe [Installation unter Windows](install-windows.md). |
| **Mein Mod steht nicht im Mods-Fenster** | Der Mod liegt nicht dort, wo das Spiel sucht, oder sein Inhalt steckt nicht in einem Inhaltsordner. Das Spiel sieht nur `Mods/<your mod>/Missions/...` (oder `Quests/`, `Maps/`, `CSV/` ...). Ein `Missions`-Ordner ohne Inhalt zählt als leer. | Öffne **Mods → Open folder** und prüf die Struktur. Der Mod-Ordner muss direkt in `Mods` liegen und die Dateien in einem Ordner, der genau `Missions` heißt. |
| **Mein Mod steht in der Liste, ist aber ausgeschaltet** | Er wurde im Mods-Fenster ausgeschaltet. | Schalte ihn ein und lade deinen Spielstand erneut. |
| **Mein Mod-Ordner ist da, wird aber ignoriert** | Es ist eine Verknüpfung, ein Alias oder ein verlinkter Ordner. Die überspringt das Spiel absichtlich. | Kopiere den echten Ordner nach `Mods`. Der Skill `install-mod` des Agenten kopiert immer. |
| **Die Mission erscheint nie** | Ihre Erscheinungsregeln sind noch nicht erfüllt: `_missionRequirements` wie ein Mindesttag (`EarliestAppearanceDay`) oder eine Startbahn-Stufe (`RunwayTier`), oder die `_tags` der Mission passen nicht zur Karte, die du spielst. Oder das Spiel hat sie einfach noch nicht gezogen. | Teste mit der Konsole: `create_mission <your_mission_id>` erzeugt sie sofort. Kommt dabei `Unknown mission ID`, wurde die Mission nicht geladen: Schau ins Player.log. |
| **Das Spiel gerät ins Stolpern, wenn meine Mission endet** (Fehler im Log, kein Ergebnis) | `_missionOutcomes` hat nicht **genau 4** Einträge. Das merkt das Spiel erst, wenn es das Ergebnis auswählt. | Gib ihr genau 4 Ausgänge in der festen Reihenfolge. Der Validator meldet das als Fehler. |
| **Die Mission bricht ab, wenn die Fähigkeit der Crew ausgewürfelt wird** | `_missionStats` hat weniger als **2** Einträge. | Füg einen zweiten Wert hinzu. Der erste wird gewürfelt, wenn die Mission nach Plan läuft, der zweite, wenn sie schiefgeht. |
| **Meine Änderungen an der Mission werden ignoriert** | Im Ordner `Missions` (neben `Mods`) ist eine Mission mit derselben ID gespeichert, zum Beispiel aus dem Mission Editor im Spiel. Dieser Ordner wird zuletzt geladen und gewinnt gegen jeden Mod. | Lösch oder benenne diese Kopie im Ordner `Missions` um, oder gib deiner Mod-Mission eine andere ID. |
| **Eine von zwei Missionen fehlt, oder die falsche wird angezeigt** | Zwei Missionen haben dieselbe ID. Eine ersetzt stillschweigend die andere, und welche gewinnt, kann sich von Computer zu Computer unterscheiden. | Gib jeder Mission eine eindeutige ID. Der Validator meldet doppelte IDs. |
| **Ich habe eine Funktion in meinem Skript geändert, nichts hat sich geändert** | Wenn eine Mission eine JSON-Datei hat, liefert das JSON die Zahlen, und manche Skript-Funktionen (zum Beispiel die für das Icon) werden nie aufgerufen. | Ändere stattdessen den Wert im JSON. Der Validator warnt vor Funktionen, die das Spiel nie aufruft. |
| **Texte zeigen Dinge wie `missions/my_mission/mission_name` oder `null`** | Der Text für diesen Schlüssel wurde nie gesetzt: ein Tippfehler im Schlüssel, eine fehlende `localization.SetTerm`-Zeile, oder das Skript wurde gar nicht geladen. | Vergleiche den Schlüssel im Text mit dem Schlüssel in `SetTerm`. Fehlen alle Texte, konnte das Skript nicht geladen werden: Schau ins Player.log. |
| **Das ganze Skript scheint übersprungen zu werden** | Es nutzt Python-Syntax, die neuer ist, als das Python des Spiels (IronPython 3.4) versteht: den Walross-Operator `:=`, eine `match`-Anweisung oder reine Positionsparameter mit `/`. Das Spiel überspringt dann die ganze Datei. | Schreib diese Zeilen in älterer Syntax um. f-Strings sind in Ordnung. Der Validator meldet so etwas als Fehler. |
| **Meine neue oder geänderte Quest taucht nicht auf** | Quests werden bei jedem Laden eines Spielstands eingelesen, ein ganz neuer `Quests/`-Ordner wird aber erst bemerkt, wenn du im Mods-Fenster auf **Refresh** drückst (oder das Spiel neu startest). | **Einstellungen → Verlassen zum Hauptmenü**, **Mods** öffnen und **Refresh** drücken, dann den Spielstand laden. |
| **Meine CSV-Änderungen greifen nicht** | Tabellenänderungen werden eingemischt, wenn ein Spiel geladen wird. | Zurück ins Hauptmenü und den Spielstand erneut laden. |
| **Die Konsole sagt `Unknown cheat`** | Ein Tippfehler oder ein Befehl, den es in deiner Version nicht gibt. | Tippe `help`, um alle Befehle aufzulisten. Drück **Tab**, um einen Befehlsnamen zu vervollständigen. |

## Das Player.log finden {#find-the-playerlog}

Das Spiel schreibt seine Fehler in eine Textdatei namens `Player.log`. (Die ausführlichen `[Mod ...]`-Zeilen zu allem, was es lädt, erscheinen nur in Entwicklungs-Builds; das veröffentlichte Spiel schreibt nur Fehler ins Log.) Sie wird bei jedem Spielstart neu geschrieben, der vorherige Durchlauf bleibt als `Player-prev.log` erhalten. Schau direkt nach dem Problem hinein, bevor du das Spiel neu startest.

| System | Wo |
|---|---|
| Windows | `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces\Player.log` |
| Mac | `~/Library/Logs/Blindflug Studios/Ground Of Aces/Player.log` |
| Linux | `~/.config/unity3d/Blindflug Studios/Ground Of Aces/Player.log` |

=== "Windows"

    Drück **Windows+R**, füg `%USERPROFILE%\AppData\LocalLow\Blindflug Studios\Ground Of Aces` ein, drück **Enter** und öffne `Player.log` mit dem Editor (Notepad) oder VS Code.

=== "Mac"

    Drück im Finder **Cmd+Shift+G**, füg `~/Library/Logs/Blindflug Studios/Ground Of Aces/` ein, drück **Return** und öffne `Player.log` mit TextEdit oder VS Code.

Durchsuche es (**Strg+F** / **Cmd+F**) nach dem Namen deines Mods, deiner Missions-ID, `Error` oder `Exception`.

## Gib es dem Agenten { #hand-it-to-the-agent }

Du musst das Log nicht selbst lesen. Tippe in Claude Code (oder Codex), im Ordner `goa-modkit`:

```text
read my Player.log and tell me what went wrong with my mod
```

Der Agent weiß, wo das Log auf deinem System liegt, findet die Zeilen zu deinem Mod und schlägt eine Lösung vor.

## Immer noch festgefahren? { #still-stuck }

Frag im [Modding-Kanal auf Discord](https://discord.com/channels/1006159027157356587/1551969822911242240). Häng dein `Player.log`, die Ausgabe des Validators und deinen Mod-Ordner als Zip an.
