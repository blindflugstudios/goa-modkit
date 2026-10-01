# Glossar

Jedes Fachwort aus diesem Handbuch, in einfacher Sprache.

## Computer-Grundlagen { #computer-basics }

**Terminal** - Ein Fenster, in das du Befehle tippst, statt zu klicken. Unter Windows heißt es Terminal oder PowerShell, auf dem Mac Terminal.

**Befehl** - Eine Zeile, die du ins Terminal tippst und mit Enter bestätigst, zum Beispiel `git pull`. Das erste Wort ist das Programm, der Rest sagt ihm, was es tun soll.

**Prompt** - Der Text am Anfang der Terminal-Zeile (endet unter Windows auf `>`, auf dem Mac auf `%`). Er bedeutet, dass das Terminal für den nächsten Befehl bereit ist.

**Ordner / Pfad** - Ein Ordner ist ein Verzeichnis auf deiner Festplatte. Ein Pfad ist seine Adresse, geschrieben als Ordnernamen, verbunden durch `\` (Windows) oder `/` (Mac), zum Beispiel `~/goa-modkit/mods`. Das `~` ist die Abkürzung für deinen persönlichen Benutzerordner.

**`cd`** - "Change directory" (Verzeichnis wechseln). Bringt das Terminal in einen Ordner, damit die nächsten Befehle dort arbeiten. `cd ~/goa-modkit` wechselt ins Modkit.

**PATH** - Die Liste der Orte, an denen das Terminal nach Programmen sucht. Deshalb musst du das Terminal nach einer Installation manchmal neu öffnen.

**Paketmanager** - Ein Programm, das andere Programme mit einem einzigen Befehl installiert. Unter Windows nutzt dieses Handbuch **winget**, auf dem Mac **Homebrew** (`brew`).

**Admin-Rechte** - Die Erlaubnis, auf einem Computer Programme zu installieren. Dein eigener PC oder Mac hat sie meistens. Ein Arbeits- oder Schulcomputer vielleicht nicht.

## Dateitypen { #file-types }

**JSON** - Ein Klartext-Format für Daten, mit `"name": value`-Paaren in geschweiften Klammern. Die Zahlen einer Mission (Werte, Ausgänge, Zeiten) stehen in JSON-Dateien mit der Endung `.json`.

**Python** - Eine Programmiersprache. Mods nutzen sie für Texte und für Logik, die auf das Geschehen im Spiel reagiert. Skriptdateien enden auf `.py`. Das Spiel führt sie mit **IronPython 3.4** aus, einem älteren Python für .NET, deshalb funktioniert ganz neue Python-Syntax nicht.

**CSV** - Eine Tabelle als Klartext, ein Datensatz pro Zeile, Werte durch Kommas getrennt. Mods nutzen CSV-Dateien, um Spieldaten wie Gebäude- oder Flugzeugwerte zu ändern.

**Texteditor** - Ein Programm zum Bearbeiten von Klartext-Dateien wie JSON und Python. Dieses Handbuch empfiehlt Visual Studio Code. Textverarbeitungen wie Word sind keine Texteditoren.

## Git und GitHub { #git-and-github }

**Git** - Ein Programm, das ein Projekt herunterlädt und jede Änderung daran festhält.

**GitHub** - Die Website, auf der das Modkit veröffentlicht ist. Für die GitHub CLI brauchst du ein kostenloses Konto.

**Repository (Repo)** - Ein Projektordner, den Git verfolgt, mit seiner ganzen Geschichte. Das Modkit ist ein Repository.

**Clone** - Ein Repository zum ersten Mal auf deinen Computer herunterladen ("klonen"): `gh repo clone blindflugstudios/goa-modkit`.

**Pull** - Die neuesten Änderungen eines Repositorys holen, das du schon geklont hast: `git pull`. Deine eigenen Mods in `mods/` werden nie angefasst.

**CLI** - "Command-line interface" (Kommandozeilen-Schnittstelle). Ein Programm, das du bedienst, indem du Befehle ins Terminal tippst, statt zu klicken.

**GitHub CLI (`gh`)** - GitHubs eigenes Terminal-Programm. Damit meldest du dich an (`gh auth login`) und klonst das Modkit.

**Release** - Eine veröffentlichte, nummerierte Version eines Projekts auf GitHub, mit fertigen Dateien zum Herunterladen. Der fertige Validator kommt aus den Releases des Modkits.

## KI-Agenten { #ai-agents }

**Agent** - Ein KI-Programm, das auf deinem Computer Dateien lesen, Dateien schreiben und Befehle ausführen kann, um eine Aufgabe zu erledigen, die du beschreibst. Claude Code, Codex und OpenCode sind Agenten.

**Claude Code** - Der Agent von Anthropic, der im Terminal läuft. Braucht ein bezahltes Claude-Abo (Pro oder höher).

**Codex** - Der Agent von OpenAI, der im Terminal läuft. Braucht einen bezahlten ChatGPT-Tarif.

**OpenCode** - Ein quelloffener Agent, der im Terminal läuft. Kostenlos zu installieren; das KI-Modell wählst du selbst, und es kostet meist Geld pro Nutzung. Einige Gratis-Modelle gibt es für begrenzte Zeit.

**Modell** - Die KI, die in einem Agenten die Denkarbeit macht, zum Beispiel Claude oder GPT. Stärkere Modelle machen weniger Fehler; viele kosten Geld pro Nutzung.

**Prompt (für einen Agenten)** - Das, was du dem Agenten schreibst: eine Bitte in ganz normaler Sprache, etwa "Mach mir eine Mission, in der...".

**Skill** - Eine schriftliche Anleitung im Modkit, die dem Agenten eine bestimmte Aufgabe beibringt, zum Beispiel `new-mission`, `validate` oder `install-mod`. Der Agent sucht sich den passenden Skill selbst aus.

**`AGENTS.md`** - Das Regelbuch für Agenten im Modkit: Ordner, Fallstricke und die Routine aus Bauen, Prüfen, Kopieren.

## Modding

**Mod** - Ein Ordner mit Dateien, der dem Spiel etwas hinzufügt oder es verändert: Missionen, Quests, Skripte, Karten, Objekte, Flugzeug-Skins oder Datentabellen.

**`Mods`-Ordner** - Hier sucht das Spiel nach installierten Mods. Du öffnest ihn im Hauptmenü: **Mods → Open folder**.

**`mods/`-Ordner (im Modkit)** - Hier bauen du und dein Agent eure eigenen Mods, bevor sie in den `Mods`-Ordner des Spiels kopiert werden. Git ignoriert ihn, deshalb ändern Updates ihn nie.

**Inhaltsordner** - Ein Ordner in einem Mod, dessen Name dem Spiel sagt, was drin ist: `Missions`, `Quests`, `Maps`, `Objects`, `CSV`, `Biomes`, `Airplanes`. Neue Missionsorte liegen eine Ebene tiefer, in `Missions/Locations`.

**ID** - Der eindeutige Name eines Dings im Spiel, zum Beispiel die Missions-ID `coastal_patrol`. IDs dürfen keine Leerzeichen enthalten und müssen eindeutig sein: Zwei Missionen mit derselben ID ersetzen sich gegenseitig.

**Lokalisierungsschlüssel** - Der Name eines Textes, etwa `missions/coastal_patrol/mission_name`. Das Spiel schlägt den Schlüssel nach, um den Text in der Sprache des Spielers zu finden. Fehlt der Text, siehst du den Schlüssel selbst.

**Validator** - Der Prüfer des Modkits (`goa_validate`). Er liest deinen Mod und meldet, was im Spiel kaputtgehen würde, ohne das Spiel zu starten und ohne deine Skripte auszuführen.

**Ausgang (Outcome)** - Eines der vier möglichen Ergebnisse einer Mission (nach Plan oder schiefgegangen, Fähigkeitsprobe bestanden oder nicht). Jede Mission hat genau vier.

**Handler** - Eine Funktion in einem Missions- oder Ereignis-Skript, die das Spiel zu einem bestimmten Zeitpunkt aufruft, zum Beispiel wenn eine Mission einen Funkspruch sendet.

**Mission Editor** - Das Werkzeug im Spiel, im Hauptmenü, mit dem du Missionen ganz ohne Dateien oder Werkzeuge erstellst.

**Konsole / Cheat-Konsole** - Ein kleines Fenster im Spiel, in das du Befehle wie `create_mission` tippst. Du schaltest sie unter **Einstellungen** (Options) **→ Cheats** ein. Siehe [Cheat-Konsole](../basics/cheats.md).

**Player.log** - Die Textdatei, in die das Spiel seine Fehler schreibt (Entwicklungs-Builds schreiben auch hinein, was es tut). Die erste Anlaufstelle, wenn ein Mod sich danebenbenimmt. Siehe [Wenn nichts passiert](troubleshooting.md#find-the-playerlog).

**Steam Workshop** - Die Seite von Steam zum Teilen von Mods. Spieler abonnieren dort einen Mod, und Steam installiert ihn für sie.

**Abonnieren** - Ein Klick auf **Abonnieren** (Subscribe) bei einem Workshop-Mod. Steam lädt ihn herunter, und das Spiel lädt ihn beim nächsten Mal.
