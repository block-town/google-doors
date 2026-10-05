# 07 · The first call

Step 7 of 7, about three minutes. Previous: [06 · The kit](06-install.md). Next: [08 · The uses](08-uses.md)

## What it is

The one time you sign in. The server asks Google for a token, your browser opens Google's page, Google lists what the app wants, you say yes, and the token lands in a file on your computer. After that, Claude asks and the server answers, with no browser.

## Why Google wants it

Your client proves which program is asking ([04](04-client.md)); this step proves that you, the account owner, agreed. Google gives the token only to the program on your computer that started the sign-in, at the `localhost` address it named.

## How

`./setup` offers this at the end, and on the Claude route Claude runs it as `./auth --yes`, which skips the Enter. To run it on its own, or again later:

```
./auth
```

It prints what you'll see, then waits for Enter:

```
Your browser opens Google's sign-in. What you'll see, in order:
  1. Choose an account. Pick you@example.com.
  2. "Google hasn't verified this app". You made this app, so that's expected. Click Continue. If the page
     has no Continue, click Advanced, then "Go to <your app name> (unsafe)".
  3. The list of what the app may do. Tick every box, or "Select all", then click Continue.
  4. A page titled "Authentication Successful". Close it and come back here.
```

Press Enter. The script starts the server, which opens Google's page in your browser, and prints the same address in case no window opens. The address goes to `accounts.google.com` and carries your client ID, the scopes, and a `redirect_uri` of `http://localhost:8000/oauth2callback`: the server listens there for Google's answer. If port 8000 is busy, the server takes the next free one up to 8004, and `./auth` tells you which.

Follow the four screens. Screens 2 and 3 are worded as Google's own [gws CLI guide](https://github.com/googleworkspace/cli) has them (read 2026-10-05); yours may differ slightly. The last page's title, "Authentication Successful", is the server's own page.

**You should see** in the terminal:

```
Signed in as you@example.com. The token is ~/.config/google-doors/main/tokens/you@example.com.json, readable by you alone.

google-doors 2026-10-05 10:14: signed in 'main'. Next: ./doctor --account main
```

If your app is in Testing, `./auth` adds that Google ends this sign-in in 7 days ([03](03-consent.md)).

### The Analytics sign-in

Google's Analytics server reads its sign-in from a credentials file of the kind Google calls Application Default Credentials. Google's README makes that file with its `gcloud` tool. This kit makes the same file without gcloud:

```
./auth-analytics
```

It asks Google for one permission, `analytics.readonly`, through the same client, using Google's sign-in for desktop apps: your browser comes back to `http://127.0.0.1:<a free port>/`, a page the script serves on your own computer, and the script trades Google's one-time code for a refresh token with a PKCE check, the method Google's [desktop-app guide](https://developers.google.com/identity/protocols/oauth2/native-app) describes (read 2026-10-05). It then writes `~/.config/google-doors/main/analytics.json`, readable by you alone, in the shape Google's own library reads: `type` set to `authorized_user`, with the client ID, the secret and the refresh token. google-auth 2.59.1, the library the Analytics server uses, loads a file of that shape as user credentials.

**You should see**, after the browser says "Google Analytics sign-in received":

```
Saved ~/.config/google-doors/main/analytics.json, readable by you alone: the client and this read-only sign-in, nothing else.

google-doors 2026-10-05 10:49: Analytics signed in for 'main'. Next: ./doctor --account main
```

### Check it

```
./doctor
```

One read-only call per service, plus `get_account_summaries` on Analytics, about a minute. **You should see** `ok` on each line. Each other word names a fault, with its fix on the next line: `api` (turn on an API), `switch` (the Apps Script switch), `admin` (your admin's trust), `expired` or `token` (run `./auth` or `./auth-analytics` again). An Analytics line that says no account is visible means your Google account can't read any Analytics property yet.

### Ask Claude

Start a new Claude Code session in any folder:

```
claude
```

Type:

```
List the subjects and senders of my five newest unread emails. Change nothing.
```

**You should see** Claude ask to run `search_gmail_messages` from the `google` server. Approve it, then the follow-up call that reads the messages, and Claude answers with your mail.

## What it lets you do

Everything in [08](08-uses.md). The token renews itself in the background; you sign in again only when Google ends it.

## If it fails

- **`./auth` says ports 8000 to 8004 are all in use.** Another program holds them. `lsof -i :8000` names the program on macOS and Linux. Close it and run `./auth` again.
- **The browser shows "Access blocked".** You're in Testing and not a test user ([03](03-consent.md), step 7).
- **The browser names `admin_policy_enforced`, or says your admin blocked the app.** Your admin hasn't trusted the client ([05](05-admin.md)).
- **You clicked Cancel, or left boxes unticked.** Run `./auth` again and tick every box. `./doctor` names any service the token doesn't cover.
- **"Authentication Error" in the browser.** The server's page prints Google's reason. A common one is a client ID or secret pasted wrong: run `./setup`, answer no to keeping the client, and paste them again.
- **Signed in as the wrong address.** `./auth` warns when the address Google returns differs from the one in your config. Run it again and pick the right account on the first screen.
- **You already have a token.** `./auth` offers to move it aside with a dated suffix (`.bak-20261005-101643`) so the new one can land. The old file stays until you delete it. `./auth-analytics` does the same with `analytics.json`.
- **`./auth-analytics` says the Analytics permission was left unticked.** Run it again and tick the one box.
- **`./auth-analytics` says the exchange with Google failed.** The reason is in brackets. `invalid_client` means the secret in your config is wrong; `couldn't reach Google` means no network.
