# Google Doors

Claude Code in your Google Workspace: Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Contacts, Apps Script and Google Analytics, through MCP servers that run on your own computer with your own Google client.

From the Claude app, Anthropic's connectors already open three doors: Gmail, Calendar and Drive, with Docs, Sheets and Slides now in beta. This repo opens every door for Claude Code. [docs/00-what-claude-already-has.md](docs/00-what-claude-already-has.md) says exactly what the connectors do and what this adds, so read it first: if the open doors are enough, you need nothing here.

Published by Sam Town, [samuel.town](https://samuel.town). Free to use, copy and change under the MIT licence: see [LICENSE](LICENSE).

По-русски: [README.ru.md](README.ru.md). The Russian page was translated with AI; corrections are welcome as an issue or a pull request.

## What this is

Two servers and a kit, working together:

- **The Workspace server**, [workspace-mcp](https://github.com/taylorwilsdon/google_workspace_mcp) by Taylor Wilsdon (MIT licence), pinned at version 2.0.1, the newest release on PyPI on 2026-10-05. It runs on your computer and gives Claude Code a set of tools: search mail, edit a doc, fill a sheet, answer a comment, book an event. With this kit's ten default services it offers 112 tools (counted on 2026-10-05).
- **The Analytics server**, Google's own [analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp) (Apache 2.0, which Google marks "Experimental"), pinned at version 0.7.0. It reads your Google Analytics reports; it changes nothing. It offered 9 tools on 2026-10-05.
- **The kit**: Python scripts and a guide. `./setup` installs both servers, keeps your client in a file only you can read and adds both to Claude Code. `./auth` signs you in to Google; `./auth-analytics` adds a read-only sign-in for Analytics. `./doctor` makes one read-only call per Google service and names whatever is missing. An optional [gateway](gateway/README.md) serves several Google accounts through three tools.

Both servers talk to Google with a client you create in your own Google Cloud project, so no third party sits between you and Google.

## What it lets you do

Hand Claude a whole job that spans your Google apps, in plain words:

```
Check my mail for anything from the client. If they sent the deck, read it and their comments, rebuild it in our style with a financial model, put the model in a sheet they can use, send it all back, book a time to go over it, then get me my analytics for the week.
```

Claude finds the mail and saves the attached deck, reads the comments on their Slides, rebuilds the deck on your computer, uploads it back as Slides with a PDF beside it, builds the model in a Sheet with live formulas and shares it, edits their brief in place and resolves the comments, replies in the thread with the PDF and the links, books an hour with a Meet link, and writes the week's Analytics into a Doc. [docs/08-uses.md](docs/08-uses.md) takes that job beat by beat, with the tool behind each beat and what it changes.

## What it costs

No money. Google's limits pages for the Gmail, Drive, Calendar, Docs, Sheets, Slides and Forms APIs each say that standard use "is available at no additional cost" (read 2026-10-05). The Analytics Data API counts work in "tokens" per property, 200,000 a day for a standard property, and its quota page names no price. Your project needs no billing account and you add no card.

You pay in other ways, and you should know them before you start:

- **About 25 minutes**, once, most of it in Google's console.
- **Google's limits on a personal app.** If you leave your app in Testing, Google ends your sign-in every 7 days. If you publish it without Google's review, you see a warning screen when you sign in, and at most 100 people can ever use the app. You are one person, so publishing is the better trade. [docs/03-consent.md](docs/03-consent.md) explains both.
- **What Claude reads.** The servers send your data to Google's APIs and nowhere else. Whatever Claude reads through them, such as an email body, becomes part of your Claude Code conversation like any file it opens. [SECURITY.md](SECURITY.md) says what that means.

## Your first 25 minutes

You need git, Python 3.10 or newer, and [Claude Code](https://code.claude.com/docs/en/overview). Then, in a terminal:

```
git clone https://github.com/block-town/google-doors
cd google-doors
claude
```

When Claude Code opens, type:

```
Set me up.
```

Claude says what it's about to do, then sends you to Google's console with the first link. [CLAUDE.md](CLAUDE.md) tells it the whole route:

- It walks you through the Google steps one page at a time: you click, it checks what you see against the page.
- It runs `./setup --dry-run` and shows you every change the setup will make on your computer, then waits for your yes.
- It asks where you saved the client file Google gave you ([docs/04-client.md](docs/04-client.md)) and your Google address, and runs `./setup` with that path. The script reads the file itself: the secret never passes through the chat, and Claude never opens the file or the config it writes. No file? You run `./setup` in your own terminal and type the values there, hidden.
- It runs the two sign-ins. Your browser opens Google's page each time and you say yes.
- It runs `./doctor`, reads you the result, and tells you what to fix, if anything.

Claude Code asks before each command it runs. Read the command, then approve it. **If it fails,** Claude shows you the error and the page that covers it; [docs/10-trouble.md](docs/10-trouble.md) lists every error the kit knows.

Tested on macOS: `./setup`, `./auth`, `./auth-analytics` and `./doctor`, both typed by hand and run the way Claude runs them. Each page about Google's console quotes Google's own guide for its labels and names the date it was read. Linux should behave the same; on Windows, use WSL.

## By hand

The same route without Claude driving, one page per step. You click through Google's console yourself either way: no program can make your Google Cloud project without your sign-in.

1. [Make a Google Cloud project](docs/01-project.md), about three minutes: the box Google counts your program's calls in.
2. [Turn on the Google APIs](docs/02-apis.md): one link turns on all thirteen, the two Analytics ones among them.
3. [Set up the consent screen](docs/03-consent.md), about five minutes, and publish the app: in Testing, Google ends your sign-in every 7 days.
4. [Make the client](docs/04-client.md) and download the JSON file Google offers: setup reads the client from it.
5. Turn on your own Apps Script API switch at [script.google.com/home/usersettings](https://script.google.com/home/usersettings). On a Workspace account, your admin may also need to trust the client: [docs/05-admin.md](docs/05-admin.md) has the clicks and the message to send.
6. Run `./setup` ([docs/06-install.md](docs/06-install.md)). It installs uv if you have none, then both servers, asks for the client file and your Google address, writes them to a file only you can read, and adds both servers to Claude Code. Then it signs you in, twice: once for the Workspace apps, once for Analytics ([docs/07-first-call.md](docs/07-first-call.md)). See the plan first with `./setup --dry-run`; leave Analytics out with `./setup --no-analytics`.
7. Run `./doctor`. One read-only call per service; every line should say `ok`, and any other word names the fix.
8. Open a new Claude Code session in any folder and ask: `List the subjects and senders of my five newest unread emails. Change nothing.` Claude calls `search_gmail_messages` and answers with your mail. Then try the whole job in [docs/08-uses.md](docs/08-uses.md).

## Every day after

| You type | It does |
|---|---|
| `./doctor` | checks the install, the sign-in and every service, and names what's wrong |
| `./auth` | signs you in again, after Google ends a sign-in or you change the services |
| `./auth-analytics` | the same for the Analytics sign-in |
| `./setup --account work` | adds a second Google account ([docs/09-several-accounts.md](docs/09-several-accounts.md)) |
| `./setup --gateway` | serves all your accounts through three tools ([gateway/README.md](gateway/README.md)) |

## The guide

- [docs/00-what-claude-already-has.md](docs/00-what-claude-already-has.md): Anthropic's Google connectors, Google's preview servers, and what this kit adds.
- [docs/00-map.md](docs/00-map.md): the words (API, OAuth, scope, token, MCP) and one picture of the path from you to Google and back.
- `docs/01` to `docs/07`: one page per setup step, in order.
- [docs/08-uses.md](docs/08-uses.md): the whole job, beat by beat, and what each request reads or changes.
- [docs/09-several-accounts.md](docs/09-several-accounts.md): a second account.
- [docs/10-trouble.md](docs/10-trouble.md): every error the kit knows, with its cause and fix.
- [docs/alternatives.md](docs/alternatives.md): the other ways to connect Claude to Google, and when to pick each.
- [SECURITY.md](SECURITY.md): what the scripts touch, where the secret lives, and how to leave.

## Leaving

1. Remove the servers from Claude Code: `claude mcp remove google -s user` and `claude mcp remove analytics -s user` (plus `google-<name>` and `analytics-<name>` for each extra account).
2. Remove the server programs: `uv tool uninstall workspace-mcp analytics-mcp`.
3. Delete your client and tokens: `rm -r ~/.config/google-doors`.
4. Withdraw the app's access in your Google Account: [myaccount.google.com/linkedapps](https://myaccount.google.com/linkedapps), pick the app, then Remove access.
5. Delete this folder.

[SECURITY.md](SECURITY.md) explains each step.
