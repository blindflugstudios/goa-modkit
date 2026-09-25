# Installation auf dem Mac

Auf dieser Seite richtest du alles einmalig ein. Geh Schritt für Schritt vor: Befehl tippen (oder einfügen), **Return** drücken und mit "Das solltest du sehen" vergleichen. Das dauert etwa 20-30 Minuten, die meiste Zeit wartest du auf Downloads.

Du brauchst macOS 13 (Ventura) oder neuer und das Anmeldepasswort deines Macs (ein Administrator-Konto).

## 1. Öffne das Terminal { #1-open-the-terminal }

Das **Terminal** ist ein Fenster, in das du Befehle tippst, statt zu klicken. Es sieht altmodisch aus, aber du brauchst nur eine Handvoll Befehle.

1. Drück **Cmd+Leertaste**, um Spotlight zu öffnen.
2. Tippe `terminal`.
3. Drück **Return**.

<!-- screenshot: Spotlight search with "terminal" typed -->

**Das solltest du sehen:** ein Fenster mit einer Zeile, die auf `%` endet, zum Beispiel:

```bash
yourname@MacBook ~ %
```

Diese Zeile ist der **Prompt**. Er bedeutet "bereit, tippe einen Befehl".

!!! tip "Einfügen"
    Kopiere einen Befehl von dieser Seite mit dem Kopier-Knopf in der Ecke jedes Kastens. Im Terminal fügst du ihn mit **Cmd+V** ein und drückst dann **Return**.

## 2. Installiere Homebrew { #2-install-homebrew }

**Homebrew** ist ein App-Installer fürs Terminal. Alles andere auf dieser Seite wird damit installiert.

Geh auf [brew.sh](https://brew.sh), kopiere den Installationsbefehl oben auf der Seite (er beginnt mit `/bin/bash -c`) und füg ihn ins Terminal ein. Zum Zeitpunkt, als diese Seite geschrieben wurde, lautet er:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Was dann passiert:

1. Es fragt nach deinem **Mac-Passwort**. Tippe es ein und drück **Return**. Beim Tippen siehst du keine Zeichen. Das ist normal.
2. Es sagt dir, was es installieren wird, und bittet dich, **Return** zu drücken.
3. Es installiert Apples **Xcode Command Line Tools**, falls sie fehlen. Das kann 5-15 Minuten dauern. Vielleicht erscheint ein Fenster, das fragt, ob du sie installieren willst: Klick auf **Installieren**.

**Das solltest du sehen:** `Installation successful!` gegen Ende.

### Die "Next steps"-Zeilen (Macs mit Apple-Chip) { #the-next-steps-lines-apple-silicon-macs }

Auf Macs mit Apple-Chip (M1, M2, M3, M4 ...) endet Homebrew mit einem Abschnitt namens **==> Next steps**, der zwei oder drei Befehle zeigt. Die sehen so aus:

```bash
echo >> /Users/yourname/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/yourname/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Kopiere die Zeilen aus deinem eigenen Terminal** (sie enthalten deinen Benutzernamen), füg sie ein und drück **Return**. Sie sagen dem Terminal, wo Homebrew wohnt. Auf älteren Intel-Macs gibt es diese Zeilen nicht, dann kannst du das überspringen.

<!-- screenshot: Homebrew "Next steps" section in the terminal -->

Prüf es:

```bash
brew --version
```

**Das solltest du sehen:** etwas wie `Homebrew 4.4.10`.

**Falls es fehlschlägt** mit "command not found: brew": Du hast die Next-steps-Zeilen übersprungen. Scroll im Terminal nach oben, such sie und führ sie aus. Oder schließ das Terminal, öffne es neu und versuch es noch einmal.

## 3. Installiere Git und die GitHub CLI { #3-install-git-and-the-github-cli }

**Git** lädt das Modkit herunter und hält es aktuell. Die **GitHub CLI** (`gh`) verbindet dein Terminal mit GitHub, der Website, auf der das Modkit liegt.

```bash
brew install git gh
```

Prüf beide:

```bash
git --version
gh --version
```

**Das solltest du sehen:** etwas wie `git version 2.47.1` und `gh version 2.63.0`.

## 4. Installiere Claude Code { #4-install-claude-code }

**Claude Code** ist der KI-Agent, der deine Mods schreibt und prüft. Denk dran: Er braucht ein bezahltes Claude-Abo (Pro oder höher). Kein Abo? Spring zu Schritt 6 und nutze später [Ohne KI-Agent](without-ai.md).

```bash
brew install --cask claude-code
```

Prüf es:

```bash
claude --version
```

**Das solltest du sehen:** eine Versionsnummer, gefolgt von `(Claude Code)`.

**Falls es fehlschlägt:** Schließ das Terminal, öffne es neu und versuch es noch einmal. Klappt es immer noch nicht, führ `claude doctor` aus und füg die Ausgabe in den Modding-Kanal auf Discord ein.

## 5. Optional: Installiere Python (empfohlen) {#5-optional-install-python-recommended}

Mit **Python** kann der Agent den Mod-Prüfer (den **Validator**) direkt ausführen. Ohne Python lädt der Agent stattdessen eine fertige Version des Prüfers herunter. Dieser Schritt ist also optional, aber empfohlen.

```bash
brew install python
```

Prüf es:

```bash
python3 --version
```

**Das solltest du sehen:** `Python 3.x.x` (3.9 oder neuer). Auf dem Mac heißt der Befehl `python3`, nicht `python`.

## 6. Leg ein GitHub-Konto an und melde dich an { #6-create-a-github-account-and-log-in }

1. Geh auf [github.com/signup](https://github.com/signup) und leg ein kostenloses Konto an. Bestätige deine E-Mail-Adresse.
2. Tippe im Terminal:

```bash
gh auth login
```

Es stellt dir ein paar Fragen (auf Englisch). Nutze die Pfeiltasten und **Return**:

| Frage | Wähle |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

Danach zeigt es einen **Einmal-Code** wie `ABCD-1234`. Drück **Return**, dein Browser öffnet sich, füg den Code ein und klick auf **Authorize**.

<!-- screenshot: gh auth login in the terminal showing the one-time code -->

**Das solltest du sehen:** `✓ Logged in as YourName` im Terminal.

## 7. Hol dir das Modkit { #7-get-the-modkit }

!!! warning "Einladung nötig"
    Während der Developer Preview ist das Modkit privat. Dieser Schritt klappt erst, wenn du die
    Einladung von GitHub angenommen hast - siehe [Zuerst Zugang holen](index.md#get-access-first).

Damit lädst du das Modkit in einen Ordner namens `goa-modkit` in deinem Benutzerordner. Das machst du einmal.

```bash
cd ~
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
```

**Das solltest du sehen:** ein paar Zeilen, die mit `done` enden, und dein Prompt zeigt jetzt `goa-modkit`.

Wenn du später Updates holen willst (neue Doku, Beispiele, Korrekturen am Prüfer), öffne das Terminal und tippe:

```bash
cd ~/goa-modkit
git pull
```

Deine eigenen Mods liegen in `goa-modkit/mods/`. Updates fassen diesen Ordner nie an.

## 8. Starte Claude Code und melde dich an { #8-start-claude-code-and-log-in }

Tippe, immer noch im Ordner `goa-modkit`:

```bash
claude
```

Beim ersten Mal:

1. Wähl mit den Pfeiltasten und **Return** ein Farbschema.
2. Entscheide dich für die Anmeldung mit deinem **Claude-Konto** (deinem Abo). Dein Browser öffnet sich. Melde dich an und klick auf **Authorize**.
3. Claude Code fragt, ob du den Dateien in diesem Ordner vertraust. Wähle **Yes**.

<!-- screenshot: Claude Code welcome screen after login -->

**Das solltest du sehen:** einen Kasten mit einem Cursor, in den du tippen kannst. Dort sprichst du mit dem Agenten. Tippe `/exit` (oder drück zweimal **Ctrl+C**), um ihn zu verlassen.

## Fertig { #done }

Du bist bereit für [Dein erster Mod in 10 Minuten](first-mod.md).

## Werkzeuge aktuell halten { #keeping-tools-up-to-date }

Homebrew aktualisiert Claude Code nicht von selbst. Führ alle paar Wochen aus:

```bash
brew update
brew upgrade claude-code git gh
```

Schließ Claude Code, bevor du es aktualisierst.
