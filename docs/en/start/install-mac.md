# Install on Mac

This page sets up everything once. Take it one step at a time: type (or paste) the command, press **Return**, and compare what you see with "You should see". It takes about 20-30 minutes, mostly waiting for downloads.

You need macOS 13 (Ventura) or newer and your Mac's login password (an administrator account).

## 1. Open the terminal

The **terminal** is a window where you type commands instead of clicking. It looks old-fashioned, but you only need a handful of commands.

1. Press **Cmd+Space** to open Spotlight.
2. Type `terminal`.
3. Press **Return**.

<!-- screenshot: Spotlight search with "terminal" typed -->

**You should see** a window with a line ending in `%`, for example:

```bash
yourname@MacBook ~ %
```

That line is the **prompt**. It means "ready, type a command".

!!! tip "Pasting"
    Copy a command from this page with the copy button in the corner of each box. In the terminal, paste with **Cmd+V**, then press **Return**.

## 2. Install Homebrew

**Homebrew** is an app installer for the terminal. Everything else on this page is installed with it.

Go to [brew.sh](https://brew.sh), copy the install command shown at the top of the page (it starts with `/bin/bash -c`) and paste it into the terminal. At the time of writing it is:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

What happens next:

1. It asks for your **Mac password**. Type it and press **Return**. You will not see any characters while typing. That is normal.
2. It tells you what it will install and asks you to press **Return**.
3. It installs Apple's **Xcode Command Line Tools** if they are missing. This can take 5-15 minutes. A window may pop up asking to install them: click **Install**.

**You should see** `Installation successful!` near the end.

### The "Next steps" lines (Apple Silicon Macs)

On Macs with an Apple chip (M1, M2, M3, M4 ...) Homebrew ends with a section called **==> Next steps** that shows two or three commands. They look like this:

```bash
echo >> /Users/yourname/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/yourname/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Copy the lines from your own terminal** (they contain your user name), paste them, and press **Return**. They tell the terminal where Homebrew lives. On older Intel Macs there are no such lines and you can skip this.

<!-- screenshot: Homebrew "Next steps" section in the terminal -->

Check it:

```bash
brew --version
```

**You should see** something like `Homebrew 4.4.10`.

**If it fails** with "command not found: brew": you skipped the Next steps lines. Scroll up in the terminal, find them, run them. Or close the terminal, open it again and retry.

## 3. Install Git and the GitHub CLI

**Git** downloads the modkit and keeps it up to date. The **GitHub CLI** (`gh`) connects your terminal to GitHub, the website where the modkit lives.

```bash
brew install git gh
```

Check both:

```bash
git --version
gh --version
```

**You should see** something like `git version 2.47.1` and `gh version 2.63.0`.

## 4. Install Claude Code

**Claude Code** is the AI agent that writes and checks your mods. Remember: it needs a paid Claude subscription (Pro or higher). No subscription? Skip to step 6 and use [Without an AI agent](without-ai.md) later.

```bash
brew install --cask claude-code
```

Check it:

```bash
claude --version
```

**You should see** a version number followed by `(Claude Code)`.

**If it fails**: close and reopen the terminal and try again. If it still fails, run `claude doctor` and paste its output into the Discord modding channel.

## 5. Optional: install Python (recommended)

**Python** lets the agent run the mod checker (the **validator**) directly. Without it the agent downloads a ready-made version of the checker instead, so this step is optional, but recommended.

```bash
brew install python
```

Check it:

```bash
python3 --version
```

**You should see** `Python 3.x.x` (3.9 or newer). On a Mac the command is `python3`, not `python`.

## 6. Create a GitHub account and log in

1. Go to [github.com/signup](https://github.com/signup) and create a free account. Confirm your email.
2. In the terminal, type:

```bash
gh auth login
```

It asks a few questions. Use the arrow keys and **Return**:

| Question | Choose |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

Then comes the part in the browser. Take it slowly - the terminal waits for you:

1. The terminal shows a **one-time code**, for example `ABCD-1234`, and says *"Press Return to open github.com in your browser"*. **Write the code down** (or leave the terminal visible), then press **Return**.
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

## 7. Get the modkit

!!! warning "Invitation needed"
    During the developer preview the modkit is private. This step only works once you have
    accepted the GitHub invitation - see [Get access first](index.md#get-access-first).

This downloads the modkit into a folder called `goa-modkit` in your home folder. You do this once.

```bash
cd ~
gh repo clone blindflugstudios/goa-modkit
cd goa-modkit
```

**You should see** a few lines ending in `done`, and your prompt now shows `goa-modkit`.

Later, to get updates (new docs, examples, checker fixes), open the terminal and type:

```bash
cd ~/goa-modkit
git pull
```

Your own mods live in `goa-modkit/mods/`. Updates never touch that folder.

## 8. Start Claude Code and log in

Still inside the `goa-modkit` folder, type:

```bash
claude
```

The first time:

1. Pick a color theme with the arrow keys and **Return**.
2. Choose to log in with your **Claude account** (your subscription). Your browser opens. Log in and click **Authorize**.
3. Claude Code asks whether you trust the files in this folder. Choose **Yes**.

<!-- screenshot: Claude Code welcome screen after login -->

**You should see** a box with a cursor where you can type. That is where you talk to the agent. Type `/exit` (or press **Ctrl+C** twice) to leave.

## Done

You are ready for [Your first mod in 10 minutes](first-mod.md).

## Keeping tools up to date

Homebrew does not update Claude Code on its own. Every few weeks, run:

```bash
brew update
brew upgrade claude-code git gh
```

Close Claude Code before upgrading it.
