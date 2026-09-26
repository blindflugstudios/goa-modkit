# Install on Windows

This page sets up everything once. Take it one step at a time: type (or paste) the command, press **Enter**, and compare what you see with "You should see". It takes about 20-30 minutes, mostly waiting for downloads.

You need Windows 10 or 11 and permission to install programs on this PC.

## 1. Open the terminal

The **terminal** is a window where you type commands instead of clicking. It looks old-fashioned, but you only need a handful of commands.

1. Press the **Windows key**.
2. Type `terminal`.
3. Click **Terminal** (on Windows 10 it may be called **Windows PowerShell**).

<!-- screenshot: Windows start menu with "terminal" typed and Terminal highlighted -->

**You should see** a dark window with a line like:

```powershell
PS C:\Users\YourName>
```

That line is the **prompt**. It means "ready, type a command". The `PS` tells you it is PowerShell, which is what this guide uses.

!!! tip "Pasting"
    Copy a command from this page with the copy button in the corner of each box. In the terminal, paste with **right-click** or **Ctrl+V**, then press **Enter**.

## 2. Check winget

**winget** is Windows' own app installer. It is built into Windows 10 and 11. Type:

```powershell
winget --version
```

**You should see** a version number, for example `v1.9.25200`.

**If it fails** with "winget is not recognized": open the **Microsoft Store**, search for **App Installer**, click **Update** (or **Get**), then close and reopen the terminal and try again.

The first time you use winget it may ask you to accept the store terms. Type `Y` and press **Enter**.

## 3. Install Git

**Git** downloads the modkit and keeps it up to date. Claude Code also uses it on Windows.

```powershell
winget install --id Git.Git -e
```

Windows may ask "Do you want to allow this app to make changes to your device?". Click **Yes**.

**You should see** a download bar and then `Successfully installed`.

!!! warning "Close and reopen the terminal now"
    Windows only learns about new programs in a fresh terminal window. Close the terminal and open it again (step 1). Do this after **every** install on this page.

Check it:

```powershell
git --version
```

**You should see** something like `git version 2.47.1.windows.1`.

**If it fails** with "git is not recognized": you probably did not reopen the terminal. Close it, open it again, try once more.

## 4. Install the GitHub CLI

The **GitHub CLI** (`gh`) connects your terminal to GitHub, the website where the modkit lives.

```powershell
winget install --id GitHub.cli -e
```

Close and reopen the terminal, then check:

```powershell
gh --version
```

**You should see** something like `gh version 2.63.0`.

## 5. Install Claude Code

**Claude Code** is the AI agent that writes and checks your mods. Remember: it needs a paid Claude subscription (Pro or higher). No subscription? Skip to step 7 and use [Without an AI agent](without-ai.md) later.

!!! tip "Prefer open source? OpenCode instead of Claude Code"
    [OpenCode](../ai/opencode.md) is an open-source agent that uses the same rules. The program
    is free; the AI model behind it is paid per use or one of a few free, weaker models offered
    for a limited time. Install it with `winget install --id SST.opencode -e` instead of this step, then read the
    [OpenCode](../ai/opencode.md) page.

```powershell
winget install Anthropic.ClaudeCode
```

Close and reopen the terminal, then check:

```powershell
claude --version
```

**You should see** a version number followed by `(Claude Code)`.

**If it fails**: reopen the terminal once more. If it still fails, run `claude doctor` and paste its output into the Discord modding channel.

## 6. Optional: install Python (recommended)

**Python** lets the agent run the mod checker (the **validator**) directly. Without it the agent downloads a ready-made version of the checker instead, so this step is optional, but recommended.

```powershell
winget install --id Python.Python.3.12 -e
```

Close and reopen the terminal, then check:

```powershell
python --version
```

**You should see** `Python 3.12.x`.

!!! warning "\"Python was not found\" or the Microsoft Store opens"
    Windows ships a fake `python` that only points to the Microsoft Store, and it can hide the
    real one. You see *"Python was not found; run without arguments to install from the
    Microsoft Store..."* (German Windows: *"Python wurde nicht gefunden..."*), even though winget
    says Python is already installed. Fix it like this:

    1. Try the Python launcher, which comes with the same install:

        ```powershell
        py --version
        ```

        If this shows `Python 3.12.x`, Python works. You can type `py` wherever this site says
        `python`. The AI agent knows this too.

    2. To make `python` work as well, open **Settings → Apps → Advanced app settings → App
       execution aliases** and switch off **App Installer python.exe** and **python3.exe**.
       Close the terminal and open a new one.

    3. Still not working? Type `where.exe python`. If it only lists a path containing
       `WindowsApps`, that is still the fake one. Reinstall with
       `winget install --id Python.Python.3.12 -e --force` and open a new terminal.

## 7. Create a GitHub account and log in

1. Go to [github.com/signup](https://github.com/signup) and create a free account. Confirm your email.
2. In the terminal, type:

```powershell
gh auth login
```

It asks a few questions. Use the arrow keys and **Enter**:

| Question | Choose |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

Then comes the part in the browser. Take it slowly - the terminal waits for you:

1. The terminal shows a **one-time code**, for example `ABCD-1234`, and says *"Press Enter to open github.com in your browser"*. **Write the code down** (or leave the terminal visible), then press **Enter**.
2. Your browser opens a GitHub page titled **Device Activation**. If GitHub asks you to sign in first, do that.
3. Type the code from the terminal into the boxes and click **Continue**.
4. GitHub now shows **Authorize GitHub CLI**. This lets the `gh` tool on your computer act for your GitHub account, so it can download the modkit. Click **Authorize github** (GitHub may ask for your password once more).
5. The browser says *"Congratulations, you're all set!"*. Now **go back to the terminal and wait** until it shows `✓ Logged in as YourName`. Only then go on - if you close the terminal or type something else before that, the login is not finished.

<!-- screenshot: gh auth login in the terminal showing the one-time code -->

**Check it** at any time:

```
gh auth status
```

**You should see** `✓ Logged in to github.com account YourName`. If it says *"You are not logged into any GitHub hosts"*, run `gh auth login` again.

**Accept your invitation.** During the developer preview the modkit is private, so you also need the invitation from Blindflug Studios (see [Get access first](index.md#get-access-first)). GitHub sends it by email; you can also open [github.com/blindflugstudios/goa-modkit/invitations](https://github.com/blindflugstudios/goa-modkit/invitations) while logged in and click **Accept invitation**. Do this once, before the next step.

!!! note "Two-factor authentication is required"
    Blindflug Studios requires **two-factor authentication (2FA)** on GitHub for everyone with
    access. When you open the invitation, GitHub asks you to set it up first - that is expected and
    takes about five minutes. The easiest way is an authenticator app on your phone (GitHub Mobile,
    Microsoft Authenticator or Google Authenticator): scan the QR code GitHub shows, type the
    6-digit code from the app, and **save the recovery codes** somewhere safe. Then accept the
    invitation. GitHub's own guide:
    [Configuring two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).

## 8. Get the modkit

!!! warning "Invitation needed"
    During the developer preview the modkit is private. This step only works once you have
    accepted the GitHub invitation - see [Get access first](index.md#get-access-first).

This downloads the modkit into a folder called `goa-modkit` inside your user folder. You do this once.

```powershell
cd ~
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
```

**You should see** a few lines ending in `done`, and your prompt now ends in `goa-modkit>`.

Later, to get updates (new docs, examples, checker fixes), open the terminal and type:

```powershell
cd ~\goa-modkit
git pull
```

Your own mods live in `goa-modkit\mods\`. Updates never touch that folder.

## 9. Start Claude Code and log in

Still inside the `goa-modkit` folder, type:

```powershell
claude
```

The first time:

1. Pick a color theme with the arrow keys and **Enter**.
2. Choose to log in with your **Claude account** (your subscription). Your browser opens. Log in and click **Authorize**.
3. Claude Code asks whether you trust the files in this folder. Choose **Yes**.

<!-- screenshot: Claude Code welcome screen after login -->

**You should see** a box with a cursor where you can type. That is where you talk to the agent. Type `/exit` (or press **Ctrl+C** twice) to leave.

## Done

You are ready for [Your first mod in 10 minutes](first-mod.md).

## Keeping tools up to date

winget does not update these tools on its own. Every few weeks, run:

```powershell
winget upgrade Anthropic.ClaudeCode
winget upgrade --id Git.Git -e
winget upgrade --id GitHub.cli -e
```

Close Claude Code before upgrading it.
