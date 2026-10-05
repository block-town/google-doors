# The gateway

Optional. One MCP server with three tools that stands in front of a workspace-mcp server for each of your Google accounts. You don't need it for one account. It covers the Workspace server only; Google Analytics keeps its own `analytics` entry per account.

## What it does

| Tool | It does |
|---|---|
| `gw(account, tool, params)` | runs one of the server's tools on one account, such as `gw("work", "search_gmail_messages", {"query": "is:unread"})` |
| `gw_discover(service)` | lists one service's tools with their parameters, `*` for required and `?` for optional, so Claude learns the names it needs |
| `gw_batch(account, calls)` | runs several tools on one account at once and returns each result in order |

Your accounts are the folders `./setup` made under `~/.config/google-doors`. On an account's first call, the gateway starts that account's workspace-mcp with that account's settings and no other's. The server stays up until Claude Code closes, so later calls skip the start-up. Each call has 120 seconds; a failure comes back as text that starts with `Error:`, so Claude can read it and tell you.

The code is [server.py](server.py), about 110 lines. It speaks to each server through MCP, the same public interface Claude Code uses, and reads your settings through the kit's own `kit.py`.

## When you want it

- **Several accounts.** Without it, each account is its own server in Claude Code (`google`, `google-work`, and so on), each with the same 112 tool names. With it, one server serves all of them and the account is a parameter, which keeps "which account?" in plain sight in every call.
- **A short tool list.** Three tools instead of 112 for each account. Claude Code's tool search, on by default, already defers tool details until Claude needs them ([Claude Code's MCP page](https://code.claude.com/docs/en/mcp), read 2026-10-05), so this matters less than it used to. It still helps where tool search is off, such as behind a proxy that sets `ANTHROPIC_BASE_URL`.

Stay with the plain server if you have one account. There, Claude sees each tool's description and parameters from the start; through the gateway it has to ask `gw_discover` first.

## How setup wires it

```
./setup --gateway
```

It installs the gateway's Python packages into `gateway/.venv` inside this folder, pinned by `gateway/uv.lock` (FastMCP 4.0.11 and its dependencies), then replaces Claude Code's `google` entry with this one:

```
claude mcp add --scope user --transport stdio google -- ~/.local/bin/uv run --frozen --directory <this folder>/gateway server.py
```

The entry holds no secret and no address: the gateway reads them from each account's config when it starts that account's server. Remove the per-account entries you no longer need with `claude mcp remove google-<name> -s user` ([09](../docs/09-several-accounts.md)).

Sign each account in with `./auth --account <name>` before you use it. The gateway can sign an account in on its first call, through the server's own sign-in, but two accounts signing in at once would compete for port 8000.

## What was tested

On macOS: `gw_discover("gmail")` listed 15 tools in about a second; `gw("main", "list_calendars")` started that account's server and returned its answer in about a second; a second call reused the running server in 0.1 seconds; an unknown account and an unknown tool each came back as an `Error:` line; `gw_batch` returned each result in order.

## If it fails

- **`Error: no account named 'x'`.** The names come from the folders under `~/.config/google-doors`. Make one with `./setup --account x`, then start a new Claude Code session: the gateway reads the folders when it starts.
- **`Error: ... ACTION REQUIRED`.** That account has no working token. Run `./auth --account <name>`.
- **The gateway doesn't start.** Run `uv sync --frozen --directory gateway` in this folder and read its output. Its server logs go to `~/.config/google-doors/<account>/logs/`.
