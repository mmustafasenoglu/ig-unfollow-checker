# IG Unfollow Checker

A small desktop tool that checks who you follow on Instagram but who doesn't follow you back.

It runs **entirely on your own computer**. Your credentials/cookies are never sent anywhere except directly to Instagram's own servers.

## Features

- Login via username + password, **or** via your browser's session cookie (no password needed)
- Handles 2FA (two-factor authentication) prompts
- Shows the list of non-mutual follows in a simple GUI
- Export the result to a `.txt` file

## ⚠️ Disclaimer

- This project is **not affiliated with, endorsed by, or connected to Instagram/Meta** in any way.
- Automating access to Instagram is against Instagram's Terms of Service. Using this tool may result in temporary action blocks or, in rare cases, account restrictions. Use at your own risk, on your own account only.
- Don't run this more than once a day. Don't share your `sessionid` or password with anyone — they grant full access to your account, just like a password does.

## Requirements

- Python 3.9+
- `pip install -r requirements.txt`

## Usage

```bash
python insta.py
```

A window will open asking for your username, and then **either**:
1. A session ID (recommended — see below), **or**
2. Your password

### Option A — Login with Session ID (recommended)

This method never requires typing your password into the script. Instead, you copy the `sessionid` cookie from a browser where you're already logged into Instagram.

#### How to get your `sessionid` cookie on **Chrome**

1. Open [instagram.com](https://www.instagram.com) and make sure you're logged in.
2. Open DevTools: `View → Developer → Developer Tools` (or `Cmd+Option+I` on Mac / `Ctrl+Shift+I` on Windows).
3. Go to the **Application** tab (may be hidden under `»` if the window is narrow).
4. In the left sidebar, expand **Cookies** → click `https://www.instagram.com`.
5. Find the row named `sessionid`, and copy its **Value**.
6. Paste that value into the "Session ID" field in the app.

#### How to get your `sessionid` cookie on **Safari**

1. Open [instagram.com](https://www.instagram.com) and make sure you're logged in.
2. Enable the Develop menu first (if not already): `Safari → Settings → Advanced → Show features for web developers`.
3. Open `Develop → Show Web Inspector` (or `Cmd+Option+I`).
4. Go to the **Storage** tab → **Cookies** → `instagram.com`.
5. Find the row named `sessionid`, and copy its **Value**.
6. Paste that value into the "Session ID" field in the app.

> Note: a `sessionid` cookie is tied to your login session. If you log out of Instagram in that browser, the cookie becomes invalid and you'll need to copy a new one.

### Option B — Login with username + password

Just leave the Session ID field empty and enter your password instead. If you have 2FA enabled, a popup will ask for the code sent to your phone/email.

## Interface

The app is a simple desktop window (Tkinter) with:

- **Username** field
- **Session ID** field (optional — see "Option A" below)
- **Password** field (optional — see "Option B" below)
- **"Find non-followers" button** — starts the check
- **Status label** — shows progress (`Logging in...`, `Fetching followers...`, `Fetching following...`, `Done.`)
- **Results box** — once finished, it lists:
  - Total accounts you follow
  - Total followers you have
  - The full list of accounts you follow that **don't follow you back**
- **"Save as .txt" button** — exports the results list to a text file on your computer

Example of what the results box shows after a run:

```
Following: 412
Followers: 387
Accounts that don't follow you back (58):

- some_user1
- some_user2
- some_user3
...
```

## Project structure

```
insta.py            # main app (GUI + Instagram logic)
requirements.txt     # Python dependencies
```

## Privacy & Security

- Nothing in this project sends your credentials, cookies, or follower data to any third-party server. All requests go directly from your machine to Instagram's own servers (`instagram.com`).
- If you choose to save your session (so you don't have to log in every time), it's stored **locally** in a file next to the script. Don't commit this file to a public repository or share it with anyone.

## License

MIT — use it, fork it, modify it. No warranty.
