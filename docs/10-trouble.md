# 10 · Trouble

Previous: [09 · A second account](09-several-accounts.md). Back to the [README](../README.md)

Every error this kit knows, with its cause and its fix, in the order you'd meet them. Start with `./doctor`: it names most of these itself. The Google texts quoted here were read on Google's pages on 2026-10-05.

## During setup

**`this needs Python 3.10 or newer`.** Your `python3` is older. Install a current one from [python.org/downloads](https://www.python.org/downloads/) and open a new terminal.

**The uv installer fails, or you'd rather not run it.** [Astral's install page](https://docs.astral.sh/uv/getting-started/installation/) lists other routes, such as Homebrew (`brew install uv`). Install uv one of those ways, then run `./setup` again; it finds uv in `~/.local/bin` or on your PATH. On 2026-10-05 on macOS, Astral's installer printed "skipping sha256 checksum verification (it requires the 'sha256sum' command)". That's the installer's own check, which macOS can't run without that command.

**`uv could not install workspace-mcp`** (or `analytics-mcp`). uv's lines above it say why; a dropped connection is the usual cause. Run `./setup` again.

**`give setup the client file Google gave you`.** Setup had no terminal to ask in, as when Claude runs it, and no `--from-json`. Tell Claude where you saved the file, or run `./setup` in your own terminal and type the values there.

**`stopped at a prompt`.** A script asked a question with nobody to answer it, as when Claude runs it without `--yes`. Claude reads you the `--dry-run` plan, then runs the command with `--yes` once you agree.

**`say which with --audience`.** Setup needs your publishing status ([03](03-consent.md)) and had no terminal to ask in. Pass `--audience internal`, `production` or `testing`.

**`uvx workspace-cli` runs something else.** The server's README warns that "an abandoned PyPI package squats that name". Don't use `uvx workspace-cli`. This kit never calls it; the `workspace-cli` that `uv tool install` puts in `~/.local/bin` is the server's own.

**`that client ID doesn't end in .apps.googleusercontent.com`.** You pasted something else, such as the project ID. Copy the Client ID from the Clients page ([04](04-client.md)).

**`Claude Code refused the entry`.** Claude Code's reason is on the line above. Two common ones: a server named `google` exists in another scope (setup gives you the `claude mcp remove` line), or you named a server `workspace`, which Claude Code reserves for a built-in ([its MCP page](https://code.claude.com/docs/en/mcp)). This kit uses `google`.

## During the sign-in

**"Google hasn't verified this app".** Expected: you made the app and nobody at Google reviewed it. Continue, or click Advanced then "Go to <your app name> (unsafe)" ([03](03-consent.md)).

**"Access blocked".** Your app is External and in Testing, and you aren't a test user. Add your address under Audience > Test users, or publish ([03](03-consent.md)).

**`org_internal`.** The app is Internal and you signed in with an account outside its organisation ([03](03-consent.md)).

**`admin_policy_enforced`, or a message that your admin blocked the app.** Your Workspace admin restricts Gmail, Drive or another service to trusted apps, and hasn't trusted yours ([05](05-admin.md)).

**Google refuses because the app asks for too much, or answers `restricted_client`.** Not seen with this kit. Google's own gws CLI guide says unverified apps are "limited to ~25 OAuth scopes" (read 2026-10-05), and with ten services this server asks for 36. Nobody had reported this against workspace-mcp in its issue tracker by 2026-10-05. If it happens to you, ask for fewer services: `./setup --services gmail drive calendar docs sheets slides tasks` asks for 23 scopes. Then `./auth`.

**`ports 8000 to 8004 are all in use`.** Google sends your browser back to `localhost` on one of those ports, and other programs hold all five. `lsof -i :8000` names the program on each. Close it and run `./auth` again.

**"Authentication Error" in the browser.** The page prints Google's reason. `access_denied` means you clicked Cancel. `invalid_client` means the client ID or secret is wrong: run `./setup`, answer no to keeping the client, and paste them again.

**`./auth` or `./auth-analytics` waits and nothing happens.** The browser didn't open. Copy the address the script printed into your browser. It waits ten minutes.

**`./auth-analytics`: `the exchange with Google failed`.** The reason is in brackets. `invalid_client` means the client secret in your config is wrong or was disabled: run `./setup`, answer no to keeping the client, paste the right one. `invalid_grant` usually means the code was used or the page sat too long: run it again. `couldn't reach Google` means no network.

**`./auth-analytics`: `the Analytics permission was left unticked`.** Run it again and tick the box.

**`Signed in as ... That isn't the address in the config`.** You picked another account on Google's first screen. Run `./auth` again and pick the right one.

## After the sign-in

**Claude stops working every 7 days.** Your app is External and in Testing, and Google ends Testing sign-ins after 7 days ([Google's OAuth page](https://developers.google.com/identity/protocols/oauth2), "Refresh token expiration"). Publish the app ([03](03-consent.md), step 8), record it with `./setup --audience production`, then `./auth`. `./doctor` warns a day before the end.

**`expired` in `./doctor`, or `invalid_grant`.** Google ended the sign-in. Besides the 7-day rule, Google's OAuth page lists these causes: you removed the app's access, the token went unused for six months, you changed your password while the token held Gmail scopes, or an admin restricted a service. Run `./auth`.

**Sign-ins vanish after you sign in on many computers.** Google allows "100 refresh tokens per Google Account per OAuth 2.0 client ID" and drops the oldest "without warning" past that (same page). Each `./auth` makes a new one. Use a client per computer if you sign in on many.

**`token` in `./doctor`.** The sign-in doesn't cover that service: a box left unticked on the consent screen, or a service you added later. Run `./auth` and tick every box.

**`api` in `./doctor`.** That API is off in your project. The line under it is the link that turns it on ([02](02-apis.md)).

**`switch` in `./doctor`, or Apps Script answering 403 "User has not enabled the Apps Script API" or 503 "Service error -27".** Turn on your own switch at [script.google.com/home/usersettings](https://script.google.com/home/usersettings) ([05](05-admin.md)).

**`admin` in `./doctor`.** Google answered `admin_policy_enforced`; see the sign-in section above.

**The Analytics line says `api`.** One of the two Analytics APIs is off in your project; the link turns both on ([02](02-apis.md)).

**The Analytics line says no Analytics account is visible.** The sign-in works, but your Google account can't read any Analytics property. Ask the property's owner to add your address in Analytics, or sign in with the account that owns it.

**The Analytics line fails with a quota project or `PERMISSION_DENIED` message.** Not seen with this kit. Google's README for analytics-mcp suggests a `GOOGLE_PROJECT_ID` setting for people who sign in through gcloud; version 0.7.0's code reads no such setting (checked 2026-10-05). If Google asks for a quota project, add `"quota_project_id": "<your project ID>"` to `analytics.json`, a field Google's library reads, and run `./doctor` again.

**Chat fails on a gmail.com account.** Google's Chat API needs "A Business or Enterprise Google Workspace account". Leave Chat out: `./setup --services gmail drive calendar docs sheets slides forms tasks contacts appscript`.

**`./doctor` warns that `GOOGLE_OAUTH_CLIENT_ID` or another such name is set in your shell.** The server reads those names first, and Claude Code passes your shell's settings on to it, so they'd override this kit's config. Remove the `export` line from your shell profile (`~/.zshrc` or `~/.bashrc`) and open a new terminal.

**`the server stopped during the checks`.** Run the server by hand to read its error: the path is in the `server` line of your config, and `--help` is a safe first argument.

**Running an Apps Script from Claude fails.** Google runs a script through its API only when the script is deployed as an API executable and shares one standard Cloud project with your client ([08](08-uses.md), use 7).

**A tool says a local file is outside the allowed folder.** The server reads local files only from its attachments folder, which this kit sets to `~/.config/google-doors/<account>/attachments`. Copy the file there first.

**The client disappeared from the console.** Google deletes an OAuth client unused for six months, after an email 30 days before ([Google's page](https://support.google.com/cloud/answer/15549257)). Make a new client ([04](04-client.md)), then `./setup` and `./auth`.

## Claude Code doesn't see the servers

- **Start a new session** after `./setup`, then look for `google` in `/mcp`.
- **Check the entry.** `claude mcp get google` shows it and whether Claude Code can connect. On 2026-10-05 a working entry showed `Status: ✔ Connected`.
- **`.mcp.json` versus user scope.** This kit adds the server at user scope, kept in `~/.claude.json`, so it loads in every project. A project's `.mcp.json` holds project-scope servers and needs your approval the first time Claude Code opens that project. A server added at local scope loads in one project only. When the same name sits in two scopes, Claude Code uses local first, then project, then user ([Claude Code's MCP page](https://code.claude.com/docs/en/mcp), "Scope hierarchy and precedence"). An old `google` entry in a project can hide this kit's.
- **Put MCP servers where Claude Code reads them.** Claude Code's MCP page names `~/.claude.json` (local and user scope) and a project's `.mcp.json` (project scope) as the places it keeps servers. One public repo reports that an `mcpServers` block in `.claude/settings.local.json` was ignored without an error ([evolsb/claude-code-google-workspace](https://github.com/evolsb/claude-code-google-workspace), read 2026-10-05). `claude mcp add` writes to the right place for you.
