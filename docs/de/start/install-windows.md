# Installation unter Windows

Auf dieser Seite richtest du alles einmalig ein. Geh Schritt für Schritt vor: Befehl tippen (oder einfügen), **Enter** drücken und mit "Das solltest du sehen" vergleichen. Das dauert etwa 20-30 Minuten, die meiste Zeit wartest du auf Downloads.

Du brauchst Windows 10 oder 11 und die Erlaubnis, auf diesem PC Programme zu installieren.

## 1. Öffne das Terminal { #1-open-the-terminal }

Das **Terminal** ist ein Fenster, in das du Befehle tippst, statt zu klicken. Es sieht altmodisch aus, aber du brauchst nur eine Handvoll Befehle.

1. Drück die **Windows-Taste**.
2. Tippe `terminal`.
3. Klick auf **Terminal** (unter Windows 10 heißt es vielleicht **Windows PowerShell**).

<!-- screenshot: Windows start menu with "terminal" typed and Terminal highlighted -->

**Das solltest du sehen:** ein dunkles Fenster mit einer Zeile wie:

```powershell
PS C:\Users\YourName>
```

Diese Zeile ist der **Prompt**. Er bedeutet "bereit, tippe einen Befehl". Das `PS` zeigt dir, dass es PowerShell ist - genau das verwendet diese Anleitung.

!!! tip "Einfügen"
    Kopiere einen Befehl von dieser Seite mit dem Kopier-Knopf in der Ecke jedes Kastens. Im Terminal fügst du ihn mit **Rechtsklick** oder **Strg+V** ein und drückst dann **Enter**.

## 2. Prüfe winget { #2-check-winget }

**winget** ist der eigene App-Installer von Windows. Er ist in Windows 10 und 11 eingebaut. Tippe:

```powershell
winget --version
```

**Das solltest du sehen:** eine Versionsnummer, zum Beispiel `v1.9.25200`.

**Falls es fehlschlägt** mit "winget is not recognized" (bzw. "wird nicht erkannt"): Öffne den **Microsoft Store**, such nach **App-Installer** (App Installer), klick auf **Aktualisieren** (oder **Herunterladen**), schließ dann das Terminal, öffne es neu und versuch es noch einmal.

Beim ersten Mal fragt winget eventuell, ob du die Store-Bedingungen akzeptierst. Tippe `Y` und drück **Enter**.

## 3. Installiere Git { #3-install-git }

**Git** lädt das Modkit herunter und hält es aktuell. Claude Code nutzt es unter Windows ebenfalls.

```powershell
winget install --id Git.Git -e
```

Windows fragt vielleicht "Möchten Sie zulassen, dass durch diese App Änderungen an Ihrem Gerät vorgenommen werden?". Klick auf **Ja**.

**Das solltest du sehen:** einen Download-Balken und danach `Successfully installed`.

!!! warning "Schließ das Terminal jetzt und öffne es neu"
    Windows bekommt neue Programme erst in einem frischen Terminal-Fenster mit. Schließ das Terminal und öffne es wieder (Schritt 1). Mach das nach **jeder** Installation auf dieser Seite.

Prüf es:

```powershell
git --version
```

**Das solltest du sehen:** etwas wie `git version 2.47.1.windows.1`.

**Falls es fehlschlägt** mit "git is not recognized": Wahrscheinlich hast du das Terminal nicht neu geöffnet. Schließ es, öffne es wieder und versuch es noch einmal.

## 4. Installiere die GitHub CLI { #4-install-the-github-cli }

Die **GitHub CLI** (`gh`) verbindet dein Terminal mit GitHub, der Website, auf der das Modkit liegt.

```powershell
winget install --id GitHub.cli -e
```

Schließ das Terminal, öffne es neu und prüf dann:

```powershell
gh --version
```

**Das solltest du sehen:** etwas wie `gh version 2.63.0`.

## 5. Installiere Claude Code { #5-install-claude-code }

**Claude Code** ist der KI-Agent, der deine Mods schreibt und prüft. Denk dran: Er braucht ein bezahltes Claude-Abo (Pro oder höher). Kein Abo? Spring zu Schritt 7 und nutze später [Ohne KI-Agent](without-ai.md).

```powershell
winget install Anthropic.ClaudeCode
```

Schließ das Terminal, öffne es neu und prüf dann:

```powershell
claude --version
```

**Das solltest du sehen:** eine Versionsnummer, gefolgt von `(Claude Code)`.

**Falls es fehlschlägt:** Öffne das Terminal noch einmal neu. Klappt es immer noch nicht, führ `claude doctor` aus und füg die Ausgabe in den Modding-Kanal auf Discord ein.

## 6. Optional: Installiere Python (empfohlen) {#6-optional-install-python-recommended}

Mit **Python** kann der Agent den Mod-Prüfer (den **Validator**) direkt ausführen. Ohne Python lädt der Agent stattdessen eine fertige Version des Prüfers herunter. Dieser Schritt ist also optional, aber empfohlen.

```powershell
winget install --id Python.Python.3.12 -e
```

Schließ das Terminal, öffne es neu und prüf dann:

```powershell
python --version
```

**Das solltest du sehen:** `Python 3.12.x`.

!!! warning "\"Python wurde nicht gefunden\" oder der Microsoft Store öffnet sich"
    Windows bringt ein falsches `python` mit, das nur auf den Microsoft Store verweist und das
    echte verdecken kann. Du siehst dann *"Python wurde nicht gefunden; ohne Argumente ausführen,
    um aus dem Microsoft Store zu installieren..."*, obwohl winget sagt, dass Python schon
    installiert ist. So behebst du das:

    1. Probier den Python-Launcher, der bei derselben Installation dabei ist:

        ```powershell
        py --version
        ```

        Zeigt er `Python 3.12.x`, funktioniert Python. Du kannst überall `py` tippen, wo auf
        dieser Seite `python` steht. Der KI-Agent weiß das auch.

    2. Damit auch `python` funktioniert, öffne **Einstellungen → Apps → Erweiterte
       App-Einstellungen → App-Ausführungsaliase** und schalte **App-Installer python.exe** und
       **python3.exe** aus. Schließ das Terminal und öffne ein neues.

    3. Klappt es immer noch nicht? Tipp `where.exe python`. Steht dort nur ein Pfad mit
       `WindowsApps`, ist das noch das falsche. Installier dann neu mit
       `winget install --id Python.Python.3.12 -e --force` und öffne ein neues Terminal.

## 7. Leg ein GitHub-Konto an und melde dich an { #7-create-a-github-account-and-log-in }

1. Geh auf [github.com/signup](https://github.com/signup) und leg ein kostenloses Konto an. Bestätige deine E-Mail-Adresse.
2. Tippe im Terminal:

```powershell
gh auth login
```

Es stellt dir ein paar Fragen (auf Englisch). Nutze die Pfeiltasten und **Enter**:

| Frage | Wähle |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

Dann kommt der Teil im Browser. Lass dir Zeit - das Terminal wartet auf dich:

1. Das Terminal zeigt einen **Einmal-Code**, zum Beispiel `ABCD-1234`, und schreibt *"Press Enter to open github.com in your browser"*. **Schreib dir den Code auf** (oder lass das Terminal sichtbar) und drück dann **Enter**.
2. Dein Browser öffnet eine GitHub-Seite mit dem Titel **Device Activation**. Falls GitHub dich zuerst anmelden will, tu das.
3. Tipp den Code aus dem Terminal in die Kästchen und klick auf **Continue**.
4. GitHub zeigt jetzt **Authorize GitHub CLI**. Damit darf das Werkzeug `gh` auf deinem Rechner für dein GitHub-Konto handeln, um das Modkit herunterzuladen. Klick auf **Authorize github** (eventuell fragt GitHub noch einmal nach deinem Passwort).
5. Der Browser meldet *"Congratulations, you're all set!"*. Jetzt **zurück ins Terminal und warten**, bis dort `✓ Logged in as YourName` steht. Erst dann weitermachen - wenn du vorher das Terminal schließt oder etwas anderes tippst, ist die Anmeldung nicht fertig.

<!-- screenshot: gh auth login in the terminal showing the one-time code -->

**Kontrollieren** kannst du das jederzeit:

```
gh auth status
```

**Das solltest du sehen:** `✓ Logged in to github.com account YourName`. Steht dort *"You are not logged into any GitHub hosts"*, führ `gh auth login` noch einmal aus.

**Nimm deine Einladung an.** Während der Developer Preview ist das Modkit privat, du brauchst also auch die Einladung von Blindflug Studios (siehe [Zuerst Zugang holen](index.md#get-access-first)). GitHub schickt sie per Mail; du kannst auch angemeldet [github.com/blindflugstudios/goa-modkit/invitations](https://github.com/blindflugstudios/goa-modkit/invitations) öffnen und auf **Accept invitation** klicken. Mach das einmal, vor dem nächsten Schritt.

## 8. Hol dir das Modkit { #8-get-the-modkit }

!!! warning "Einladung nötig"
    Während der Developer Preview ist das Modkit privat. Dieser Schritt klappt erst, wenn du die
    Einladung von GitHub angenommen hast - siehe [Zuerst Zugang holen](index.md#get-access-first).

Damit lädst du das Modkit in einen Ordner namens `goa-modkit` in deinem Benutzerordner. Das machst du einmal.

```powershell
cd ~
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
```

**Das solltest du sehen:** ein paar Zeilen, die mit `done` enden, und dein Prompt endet jetzt auf `goa-modkit>`.

Wenn du später Updates holen willst (neue Doku, Beispiele, Korrekturen am Prüfer), öffne das Terminal und tippe:

```powershell
cd ~\goa-modkit
git pull
```

Deine eigenen Mods liegen in `goa-modkit\mods\`. Updates fassen diesen Ordner nie an.

## 9. Starte Claude Code und melde dich an { #9-start-claude-code-and-log-in }

Tippe, immer noch im Ordner `goa-modkit`:

```powershell
claude
```

Beim ersten Mal:

1. Wähl mit den Pfeiltasten und **Enter** ein Farbschema.
2. Entscheide dich für die Anmeldung mit deinem **Claude-Konto** (deinem Abo). Dein Browser öffnet sich. Melde dich an und klick auf **Authorize**.
3. Claude Code fragt, ob du den Dateien in diesem Ordner vertraust. Wähle **Yes**.

<!-- screenshot: Claude Code welcome screen after login -->

**Das solltest du sehen:** einen Kasten mit einem Cursor, in den du tippen kannst. Dort sprichst du mit dem Agenten. Tippe `/exit` (oder drück zweimal **Strg+C**), um ihn zu verlassen.

## Fertig { #done }

Du bist bereit für [Dein erster Mod in 10 Minuten](first-mod.md).

## Werkzeuge aktuell halten { #keeping-tools-up-to-date }

winget aktualisiert diese Werkzeuge nicht von selbst. Führ alle paar Wochen aus:

```powershell
winget upgrade Anthropic.ClaudeCode
winget upgrade --id Git.Git -e
winget upgrade --id GitHub.cli -e
```

Schließ Claude Code, bevor du es aktualisierst.
