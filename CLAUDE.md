# Instructions for Claude Code in this folder

You're setting someone up so Claude Code can work in their Google account. They pointed you at this repo and said something like "set me up". They may never have opened the Google Cloud console or used a terminal before today. You carry them through the whole route below, one step at a time, and they do the clicking in their browser.

## What this folder is

- **Scripts.** `setup` installs two servers, Taylor Wilsdon's workspace-mcp 2.0.1 and Google's analytics-mcp 0.7.0, keeps the person's Google client in a file only they can read, and registers both with Claude Code. `auth` signs the account in to Google. `auth-analytics` adds a read-only Analytics sign-in. `doctor` checks everything. `kit.py` holds what they share. All are Python, standard library only.
- **A guide.** `README.md` has the route by hand. `docs/00-what-claude-already-has.md` says what Anthropic's connectors already do. `docs/00-map.md` explains the words. `docs/01-project.md` to `docs/07-first-call.md` are one page per step. `docs/08-uses.md` is the whole job they can hand you afterwards, `docs/09-several-accounts.md` a second account, `docs/10-trouble.md` every known error.
- **A gateway** in `gateway/`, for several accounts, explained in `gateway/README.md`.

## How you work

1. **Answer in the language the person writes in.** A Russian README exists (`README.ru.md`).
2. **Say what you're about to do before you do it**, in a sentence, and why. Then do it.
3. **Explain each command before you run it**: what it does and what it changes. Claude Code shows them the command; they approve it.
4. **Quote the page.** Read the step's page in `docs/` before you explain it and use its labels. Several pages say which labels nobody has seen live yet; say so when you reach one, and never invent a button.
5. **Ask what they see, and compare it** with the page's "You should see" before you move on.
6. **Show real output.** When a command fails, show the error, say what it means, and point to the page that covers it. Never report a step as done when its check didn't pass.
7. **Use plain words.** Explain a technical word once, the way `docs/00-map.md` does.

## The route

### 1. Three questions first

Ask, and remember the answers:

- Is it a gmail.com account, or an address their company, school or own domain gave them (Workspace)?
- If Workspace: are they the Workspace admin? If not, step 5 needs a message to whoever is.
- Do they want Google Analytics too? It needs an Analytics property their account can read. If not, every command below gets `--no-analytics` where it applies.

Tell them the route takes about 25 minutes, most of it in Google's console, and costs nothing.

### 2. The Google steps, in their browser

Walk them through the pages in order. For each one, give the link and the clicks, wait for them to say it's done, and check what they see.

1. `docs/01-project.md`: the project.
2. `docs/02-apis.md`: the APIs. The one link turns on all thirteen: ten for the Workspace apps, Chat for Workspace accounts, and two for Analytics. A gmail.com account uses twelve of them; without Analytics, ten are enough.
3. `docs/03-consent.md`: the consent screen. Note which they end with, Internal, External In production, or External Testing: it becomes `--audience internal`, `production` or `testing`. Recommend publishing (step 8 there) for External, and say why: Testing ends the sign-in every 7 days.
4. `docs/04-client.md`: the client. Tell them to download the JSON file Google offers when it shows the new client, and to remember where they saved it. That file is how setup gets the client. **Nothing from it goes into this chat.**
5. `docs/05-admin.md`: the Apps Script switch for everyone; the admin's trust for Workspace accounts; the message to send if they aren't the admin.

### 3. Setup

1. Run `./setup --dry-run` (plus `--no-analytics` if they said no). Read the plan back to them in plain words: what gets installed where, which file holds the secret, which entries go into Claude Code. Ask: "Shall I go ahead?"
2. Ask two things: "Where did you save the client file Google gave you?" and their Google address. Neither is a secret, and you need only the file's path, never its contents.
3. On their yes, run `./setup --yes --audience <their answer> --from-json <the path> --email <their address>`. Give it a long timeout: up to 10 minutes, for the installs. The script reads the client file itself. Never open, read, copy or print that file.
   If they have no file (they copied the ID and secret instead), don't take the values in the chat. Tell them to open their own terminal, `cd` into this folder and run `./setup` there: it asks for the values with typing hidden. When it's done, carry on with the sign-ins below.
4. When setup ends, show them its last line, and tell them they may delete the client file from where they saved it: setup keeps its own copy.

### 4. The sign-ins

1. Tell them what Google will show (the four screens `./auth --dry-run` prints), then run `./auth --yes`, with a 10-minute timeout. It opens Google's page in their browser and waits. When it ends, tell them which address signed in.
2. With Analytics: the same with `./auth-analytics --yes`. One permission this time, read-only.

### 5. The doctor

Run `./doctor` and read it to them line by line, using the table below. Fix problems from the top, then run it again. Done means its last line says every service answered.

### 6. Hand over

Tell them to quit this session, start `claude` again in any folder, and type `/mcp`: it should list `google` and `analytics`. Suggest the read-only first prompt near the top of `docs/08-uses.md`, then the whole job on that page.

## Secrets: never touch them

- Never ask for the client ID, the client secret, a token or a password in this chat. Ask for the path of the client file; their own terminal takes typed values.
- If they paste a secret here anyway, tell them to make a new one (`docs/04-client.md`, "If it fails") and run `./setup` again with it.
- Never read, open, print, copy, move or summarise anything under `~/.config/google-doors/` except the `attachments/` folder: `config` holds the client secret, `tokens/` and `analytics.json` hold their sign-ins.
- Never open a client JSON file they downloaded. Pass its path to `./setup --from-json` and nothing else.
- Never put a secret, a token or a client ID into a file in this folder, a commit or a command line.

## Reading `./doctor`

Each line starts with a word. The line under it, when there is one, is the fix.

| Word | Meaning | Page |
|---|---|---|
| `ok` | that part works | |
| `note` | worth knowing, nothing broken. One note always says Anthropic's own Google connectors are separate and don't clash | |
| `warn` | works now, needs action soon: a Testing sign-in near its 7 days, a config others can read, a Google setting left in the shell | [docs/03](docs/03-consent.md), [docs/10](docs/10-trouble.md) |
| `api` | that service's API is off in their project; the next line is the link that turns it on | [docs/02](docs/02-apis.md) |
| `switch` | their own Apps Script API switch is off | [docs/05](docs/05-admin.md) |
| `admin` | a Workspace admin hasn't trusted the client (`admin_policy_enforced`) | [docs/05](docs/05-admin.md) |
| `expired` | Google ended the sign-in; in Testing that happens every 7 days | [docs/03](docs/03-consent.md), then `./auth --yes` or `./auth-analytics --yes` |
| `token` | the sign-in doesn't cover that service, or has lapsed | the sign-in the line names, ticking every box |
| `fail` | anything else; the line under it is the first line of the error | [docs/10](docs/10-trouble.md) |

An `api` line can cause the lines after it, so fix from the top. `./doctor` exits 0 only when every service answers.

## Known errors and their pages

- "Google hasn't verified this app", "Access blocked", `org_internal`, the 7-day expiry: `docs/03-consent.md`.
- A lost client secret, a wrong client ID, a leaked secret: `docs/04-client.md`.
- `admin_policy_enforced`, Apps Script 403 or 503, Chat: `docs/05-admin.md`.
- uv, the installs, the client file, `uvx workspace-cli`, Claude Code refusing an entry: `docs/06-install.md`.
- Ports 8000 to 8004 busy, the wrong account signed in, the Analytics sign-in: `docs/07-first-call.md`.
- Everything else, including Claude Code not seeing the servers (`.mcp.json` versus user scope): `docs/10-trouble.md`.

## After setup: working in their account

Before any tool call that sends mail, shares a file, deletes something, books an event or uploads, say what it will do and wait for their yes. Files the Google server reads or uploads from this computer live in `~/.config/google-doors/<account>/attachments/`: put a file there before you ask the server to upload it.

## What stays off limits

- No `sudo`.
- No changes outside this folder beyond what `./setup` lists in its dry run and the person agreed to.
- No edits to shell profiles, no background services, no scheduled jobs.
- No paid Google service. Everything here runs without a billing account; if a page asks for a card, stop and check `docs/01-project.md`.
