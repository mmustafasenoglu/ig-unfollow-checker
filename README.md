# IG Unfollow Checker

A small desktop tool that checks who you follow on Instagram but who doesn't follow you back.

It runs **entirely on your own computer**. Your credentials/cookies are never sent anywhere except directly to Instagram's own servers.

## Features

- Login via username + password, **or** via your browser's cookie (no password needed)
- Handles 2FA (two-factor authentication) prompts
- Shows the list of non-mutual follows in a simple GUI, with pagination
- **One-click Unfollow button** next to each account in the results
- Export the result to a `.txt` file

## How it works under the hood

- Resolving your user ID uses [instaloader](https://github.com/instaloader/instaloader), which talks to Instagram's web **GraphQL** endpoint.
- Fetching your followers/following list and unfollowing both go through Instagram's **private API** (`/api/v1/friendships/...`), the same endpoints the official Instagram app uses.
- Both require you to be authenticated, which is why a cookie or password is needed.

## ⚠️ Disclaimer

- This project is **not affiliated with, endorsed by, or connected to Instagram/Meta** in any way.
- Automating access to Instagram is against Instagram's Terms of Service. Using this tool may result in temporary action blocks or, in rare cases, account restrictions. Use at your own risk, on your own account only.
- **Unfollowing is a "write" action**, not just reading data — Instagram's bot detection is more sensitive to write actions. Avoid unfollowing many accounts back-to-back in a short time; doing too many too fast is the most common way to trigger an `Action Blocked` (temporary lock on follow/unfollow for ~24-48h).
- Don't run this more than once a day. Don't share your cookie or password with anyone — they grant full access to your account, just like a password does.

## Requirements

- Python 3.9+
- `pip install -r requirements.txt`

## Usage

```bash
python insta.py
```

A window will open asking for your username, and then **either**:
1. A full cookie string, or a pasted `cURL` command (recommended), **or**
2. Your password

### Option A — Login with cookie (recommended)

This method never requires typing your password into the script. Instead, you copy a logged-in request from a browser where you're already signed into Instagram, and paste it into the **"Full Cookie"** field. The app accepts either:
- A full `curl ...` command copied straight from your browser's Network tab (the app automatically extracts the `Cookie:` header from it), **or**
- Just the raw cookie string itself (e.g. `sessionid=...; csrftoken=...; ds_user_id=...`)

#### How to get it on **Chrome**

1. Open [instagram.com](https://www.instagram.com) and make sure you're logged in.
2. Open DevTools (`Cmd+Option+I` on Mac / `Ctrl+Shift+I` on Windows) and go to the **Network** tab.
3. Reload the page, or click on your own profile, so new requests show up in the list.
4. Find any request to `www.instagram.com` (e.g. one with `graphql` or `friendships` in the name).
5. Right-click it → **Copy** → **Copy as cURL** (bash).
6. Paste the entire thing into the "Full Cookie" field in the app.

#### How to get it on **Safari**

1. Open [instagram.com](https://www.instagram.com) and make sure you're logged in.
2. Enable the Develop menu first (if not already): `Safari → Settings → Advanced → Show features for web developers`.
3. Open `Develop → Show Web Inspector` (`Cmd+Option+I`) and go to the **Network** tab.
4. Reload the page, or click on your own profile, so new requests show up.
5. Find a request with `graphql` in the name, right-click it → **Copy as cURL**.
6. Paste the entire thing into the "Full Cookie" field in the app.

> Note: this cookie/curl snapshot is tied to your login session. If you log out of Instagram in that browser, it becomes invalid and you'll need to copy a fresh one.

### Option B — Login with username + password

Just leave the "Full Cookie" field empty and enter your password instead. If you have 2FA enabled, a popup will ask for the code sent to your phone/email.

## Interface

The app is a simple desktop window (Tkinter) with:

- **Username** field
- **Full Cookie** field (optional — see "Option A" above)
- **Password** field (optional — see "Option B" above)
- **"Find non-followers" button** — starts the check
- **Status label** — shows progress (`Logging in...`, `Fetching followers...`, `Fetching following...`, `Done.`)
- **Results list** — once finished, shows, for each non-mutual account:
  - Their username
  - An **"Unfollow"** button next to them
- **Pagination controls** (`<< Previous` / `Next >>`) since the list can be long
- **"Save all results as .txt" button** — exports the full results list to a text file on your computer

Example header shown above the results list:

```
Following: 412 | Followers: 387
Accounts that don't follow you back: 58
Showing: 1 - 30
```

## Project structure

```
insta.py            # main app (GUI + Instagram logic)
requirements.txt     # Python dependencies
```

## Privacy & Security

- Nothing in this project sends your credentials, cookies, or follower data to any third-party server. All requests go directly from your machine to Instagram's own servers (`instagram.com`).
- The "Full Cookie" value is just as sensitive as your password — anyone who has it can access your account. Never paste it into a README, a GitHub issue, a public chat, or share it with anyone.
- If you choose to save your session (so you don't have to log in every time), it's stored **locally** in a file next to the script. Don't commit this file to a public repository or share it with anyone (it's already excluded via `.gitignore`).

## License

MIT — use it, fork it, modify it. No warranty.
