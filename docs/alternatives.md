# Other ways to connect Claude to Google

This kit is one route among several. Each route below does something well, and for some people one of them beats this kit. Every fact here comes from the project's own page, read on 2026-10-05; star counts and versions move.

## Anthropic's own Google connectors

**What it is.** Claude's built-in connectors for Gmail, Google Calendar and Google Drive, and, in beta, for Google Docs, Sheets and Slides. Anthropic's [help page](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors) says they're "available for all users on Claude and Claude Desktop"; on Team and Enterprise plans an owner turns them on first. Claude Code's [MCP page](https://code.claude.com/docs/en/mcp) says connectors you've added in claude.ai appear in Claude Code when you're logged in with a claude.ai subscription. [docs/00-what-claude-already-has.md](00-what-claude-already-has.md) lists what each one does.

**What it does well.** No Cloud project, no client, no token file to look after: you sign in to Google from claude.ai. It searches, reads and sends mail, books and changes events, finds a time that suits everyone, reads and uploads Drive files, and, in the beta, edits Docs, Sheets and Slides live in a pane beside the chat and works with comments in Docs. Claude asks for your approval before it sends mail or shares and moves files.

**Pick it when** you use the Claude app or Claude Code with a claude.ai subscription and those apps cover your work. It's the quickest route there is.

**Pick this kit instead when** you need what the help page doesn't list: a mail's attachment, Apps Script, Forms, Tasks, Contacts, Chat or Analytics; several Google accounts kept apart; Claude Code logged in with an API key, since Claude Code's MCP page says connectors load only with a claude.ai subscription login; or one long job run from Claude Code with your own files and programs in the loop.

## Google's remote MCP servers

**What it is.** Google runs MCP servers for Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat and People at addresses such as `https://gmailmcp.googleapis.com/mcp/v1` ([Google's page](https://developers.google.com/workspace/guides/configure-mcp-servers), updated 2026-09-18). They're in Developer Preview: you join Google's Workspace Developer Preview Program first.

**What it does well.** Google hosts and maintains the servers, so nothing runs on your computer, and each one follows Google's own permissions and data rules.

**Watch for.** A public repo that scripts this route, [xbill9/workspace-mcp-claude](https://github.com/xbill9/workspace-mcp-claude), measured on 2026-10-04 that sign-ins through Claude Code "last about an hour", with no refresh token. The list has no Apps Script, Forms or Tasks.

**Pick it when** you're in the preview and want Google-run servers.

## Google's `gws` command-line tool

**What it is.** [googleworkspace/cli](https://github.com/googleworkspace/cli), "one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more", built from Google's API descriptions, Apache 2.0, about 31,000 stars on 2026-10-05. It includes skills for AI agents.

**What it does well.** Breadth: it reaches most Workspace APIs, Admin among them, from one tool. Its guide also documents the unverified-app screens and the Testing limits.

**Pick it when** you want a command-line tool you also use by hand, or an API this server doesn't cover.

## Other open-source setups and servers

| Project | What it does well | Pick it when |
|---|---|---|
| [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | The server this kit installs: 12 services, tool tiers, read-only and per-service permission modes, OAuth 2.1 for many users, a hosted option | You want the server's full range of modes, or to run it for a team over HTTP. This kit adds a beginner's path, the admin page, `doctor` and the gateway around it |
| [evolsb/claude-code-google-workspace](https://github.com/evolsb/claude-code-google-workspace) | Several accounts through `gws`, a CLAUDE.md for guided setup, a frank table of nine gotchas, Slack alongside | You want Gmail, Drive, Calendar, Sheets and Docs plus Slack. Its own notes say access tokens last about an hour and it was tested on macOS |
| [xbill9/workspace-mcp-claude](https://github.com/xbill9/workspace-mcp-claude) | Scripts and a Claude Code plugin for Google's remote MCP servers, with measured sign-in behaviour | You're in Google's preview (above) |
| [aaronsb/google-workspace-mcp](https://github.com/aaronsb/google-workspace-mcp) | Gmail, Calendar, Drive, Docs, Sheets, Tasks, Meet and Contacts across many accounts, per-account read-only, a one-click Claude Desktop bundle | You want many accounts with read-only per account, and don't need Slides, Forms or Apps Script (its README says it doesn't touch Chat, Slides or Forms yet) |
| [bobmatnyc/gworkspace-mcp](https://github.com/bobmatnyc/gworkspace-mcp) | 116 tools over Gmail, Calendar, Drive, Docs, Sheets, Slides and Tasks, named account profiles, its own `doctor` | You want deep Gmail and Slides tools with account profiles in one Python package |
| [sputnicyoji/google-workspace-mcp-with-script](https://github.com/sputnicyoji/google-workspace-mcp-with-script) | 72 tools over Docs, Sheets, Drive, Gmail, Calendar and Apps Script, an interactive setup, README in three languages | You work in Node and want Apps Script with the core apps |
| [dguido/google-workspace-mcp](https://github.com/dguido/google-workspace-mcp) | Drive, Docs, Sheets, Slides, Calendar, Gmail and Contacts from one `npx` command | You want a Node server with a short Claude Desktop setup |
| [danielrosehill/google-workspace-mcp](https://github.com/danielrosehill/google-workspace-mcp) | A fork of dguido's that serves several accounts from one process by URL path, with mail attachments and signatures | You want dguido's server with several accounts |
| [cudijo/workspace-mcp](https://github.com/cudijo/workspace-mcp) | Gmail, Calendar, Chat, Drive, Meet and the Workspace directory, no dependencies beyond Node, several accounts at once | You want a small Node server that needs no npm install |

## Where this kit sits

It installs the broadest of these servers and adds what a first-timer needs around it: each console page with Google's own labels and the date they were checked, the Workspace admin page and the message to send your admin, the Apps Script switch, the 7-day trap and how to leave it, a `setup` that keeps the secret out of Claude Code's config, a `doctor` that names the missing piece, and a gateway for several accounts.
