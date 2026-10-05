# 06 · The kit

Step 6 of 7, about five minutes. Previous: [05 · Workspace accounts](05-admin.md). Next: [07 · The first call](07-first-call.md)

## What it is

`./setup`, a Python script in this folder. It installs two servers, stores your client where only you can read it, and tells Claude Code the servers exist.

- **The Workspace server** is [workspace-mcp](https://github.com/taylorwilsdon/google_workspace_mcp) by Taylor Wilsdon, MIT licence, version 2.0.1 from [PyPI](https://pypi.org/project/workspace-mcp/2.0.1/) (released 2026-10-04).
- **The Analytics server** is Google's own [analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp), Apache 2.0, version 0.7.0 from [PyPI](https://pypi.org/project/analytics-mcp/0.7.0/) (released 2026-07-29). Google's README calls it "Experimental". It reads Analytics and changes nothing.

Both speak MCP, the plug Claude uses to reach other programs: Claude Code starts them in the background and calls their tools.

## Why it's needed

Claude Code knows nothing about Google until a server gives it tools, and a server knows nothing about you until it has your client and your address. `./setup` hands each one what it needs and keeps the secret out of everything else.

## How

Claude runs this for you on the Claude route ([README](../README.md)). By hand, in the terminal, inside this folder:

```
./setup
```

Or first see the plan without changing anything:

```
./setup --dry-run
```

`./setup` works through four steps and prints each change outside this folder before it asks for your yes:

1. **uv.** If you don't have [uv](https://docs.astral.sh/uv/), Astral's tool for installing Python programs, setup offers to download Astral's documented installer to a file you can read first, then runs it with `UV_NO_MODIFY_PATH=1`, the setting [Astral's reference](https://docs.astral.sh/uv/reference/installer/) gives for leaving your shell profiles alone. uv lands in `~/.local/bin`. No sudo.
2. **The servers.** It runs `uv tool install --constraints server-constraints.txt workspace-mcp==2.0.1`, then the same for `analytics-mcp==0.7.0` with `analytics-constraints.txt`. Each lands in uv's own folder, with its commands in `~/.local/bin`: `workspace-mcp` and `workspace-cli`, `analytics-mcp` and `google-analytics-mcp`. The constraints files hold the exact version of each package the servers need, as tested on 2026-10-05 with Python 3.10, 3.12 and 3.14, so a newer release can't slip in. Leave Analytics out with `--no-analytics`.
3. **Your client.** It reads the client from the JSON file Google offers when you create the client ([04](04-client.md)): give the path with `--from-json <the file>`, or at the question setup asks. That's the main way, and the one Claude uses: the script opens the file, so the secret never passes through a chat. Without the file, press Enter at that question and paste the client ID and the secret by hand in your own terminal, with typing hidden. Then it asks for your Google address (or takes `--email`).

   Setup shows the end of the ID and the address back so you can check them, then asks which publishing status you chose in [03](03-consent.md) (or takes `--audience`). It writes all of it to `~/.config/google-doors/main/config`, a file only your user can read, in a folder only your user can open, and reminds you to delete Google's file from where you saved it.
4. **Claude Code.** It shows you two commands, with your paths filled in, and runs each after your yes:

   ```
   claude mcp add --env GOOGLE_CLIENT_SECRET_PATH=... --env USER_GOOGLE_EMAIL=... \
     --env WORKSPACE_MCP_CREDENTIALS_DIR=... --env WORKSPACE_MCP_LOG_DIR=... --env WORKSPACE_ATTACHMENT_DIR=... \
     --scope user --transport stdio google -- ~/.local/bin/workspace-mcp --single-user --tools gmail drive calendar docs sheets slides forms tasks contacts appscript
   claude mcp add --env GOOGLE_APPLICATION_CREDENTIALS=... --scope user --transport stdio analytics -- ~/.local/bin/analytics-mcp
   ```

   That adds two servers, `google` and `analytics`, for all your projects ("user scope", which Claude Code keeps in `~/.claude.json`, per its [MCP page](https://code.claude.com/docs/en/mcp), read 2026-10-05). The entries hold the paths to your files, never the secret itself. Without the `claude` command on your PATH, setup prints the entries as JSON and offers to add them to `~/.claude.json`, keeping a dated copy of the old file.

Then it offers to sign you in, which is [07](07-first-call.md). With `--yes` it skips that offer and names the two sign-in commands to run next, so each one runs on its own.

### --yes

`./setup --yes` answers yes at each step. It's for after you've read the `--dry-run` plan: Claude runs `./setup --dry-run`, shows you the plan, and runs `./setup --yes --audience <yours> --from-json <your client file> --email <your address>` once you agree in the chat. It still prints each step as it goes.

**You should see**, on a run where everything is new:

```
Next: install the Google Workspace server (Taylor Wilsdon's, MIT licence), workspace-mcp 2.0.1, as a uv tool, with every package it needs pinned by server-constraints.txt. ...
Install it? [Y/n]
...
Installed 2 executables: workspace-cli, workspace-mcp
...
Installed 2 executables: analytics-mcp, google-analytics-mcp
...
ok    wrote ~/.config/google-doors/main/config
...
Added stdio MCP server google with command: ~/.local/bin/workspace-mcp --single-user --tools gmail drive calendar docs sheets slides forms tasks contacts appscript to user config
...
Added stdio MCP server analytics with command: ~/.local/bin/analytics-mcp  to user config
```

That's from a run on macOS with a test client, with the home folder's path shortened to `~` here. Run `claude mcp get google` or `claude mcp get analytics` afterwards and Claude Code reports `Status: ✔ Connected`: it started the server and spoke to it.

### The services

By default the Workspace server loads ten services: Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Contacts and Apps Script, 112 tools in all. Choose your own with `--services`, for example `./setup --services gmail calendar drive`; add Chat with `--chat` ([05](05-admin.md)). Each service brings its scopes, so a shorter list asks Google for less. The Analytics server offers 9 tools, read-only.

## What it lets you do

Open any Claude Code session and the tools are there. Claude Code loads tool names at the start and fetches a tool's full description when it needs it ("tool search", on by default per Claude Code's MCP page, read 2026-10-05), so 121 tools cost little room in the conversation.

## If it fails

- **`uv could not install workspace-mcp`** (or `analytics-mcp`). The lines above it are uv's own. A network problem is the usual cause: run `./setup` again.
- **`give setup the client file Google gave you`.** Setup had no terminal to ask in (Claude ran it) and no `--from-json`. Tell Claude where you saved the client file, or run `./setup` in your own terminal.
- **`say your Google address with --email`.** The same, for your address.
- **`say which with --audience`.** Claude ran setup without saying which publishing status you have. Tell Claude which one ([03](03-consent.md)).
- **`Claude Code refused the entry`.** Claude Code prints why on the line above. A server named `google` or `analytics` in another scope is one cause: setup tells you the `claude mcp remove` line to run.
- **`uvx workspace-cli` installs something odd.** The server's README warns that "an abandoned PyPI package squats that name". This kit never uses it; `workspace-cli` from the server's own install is the right one.
- **Claude Code doesn't list the servers.** Start a new Claude Code session so it reads the new entries. Inside a session, `/mcp` lists your servers with their status, and `claude mcp get google` in a terminal shows the entry and whether Claude Code can connect.
