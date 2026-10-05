#!/usr/bin/env python3
"""google-doors gateway: three MCP tools in front of one workspace-mcp server per account.

    gw(account, tool, params)    one call on one account
    gw_discover(service)         the tools a service offers, with their parameters
    gw_batch(account, calls)     several calls on one account at once

Accounts are the folders ./setup made under ~/.config/google-doors. Each account's server starts on its first
call, with that account's settings alone, and stays up until Claude Code closes. Written against the server's
public MCP interface; README.md beside this file says when you'd want it.
"""
import asyncio, json, sys
from pathlib import Path

from fastmcp import Client, FastMCP
from fastmcp.client.transports import StdioTransport

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kit  # noqa: E402  the kit's own module: paths, the config check, the server's settings

TIMEOUT = 120
ACCOUNTS = kit.accounts()
NAMES = ", ".join(ACCOUNTS) or "none yet: run ./setup"
_clients: dict = {}
_lock = asyncio.Lock()
_listed: dict = {}


def _transport(account, services=None):
    try:
        data = kit.load(account)
    except SystemExit as stop:   # kit.load exits on a broken config; a gateway must keep running
        raise ValueError(str(stop)) from None
    logs = kit.folder(account) / "logs"
    kit.private_dir(logs)
    return StdioTransport(command=data["kit"]["server"], args=kit.server_args(data, services),
                          env=kit.server_env(account, data), log_file=logs / "gateway-server.log")


async def _client(account):
    if account not in ACCOUNTS:
        raise ValueError(f"no account named '{account}'. Accounts: {NAMES}")
    async with _lock:
        if account not in _clients:
            client = Client(_transport(account), timeout=TIMEOUT)
            await client.__aenter__()
            _clients[account] = client
    return _clients[account]


async def _call(account, tool, params):
    try:
        client = await _client(account)
        result = await asyncio.wait_for(client.call_tool(tool, params or {}, raise_on_error=False), TIMEOUT)
    except asyncio.TimeoutError:
        return f"Error: {tool} gave no answer in {TIMEOUT} s."
    except Exception as error:   # returned as text, so Claude can read it and say what went wrong
        return f"Error: {type(error).__name__}: {error}"
    text = "\n".join(getattr(part, "text", "") for part in result.content).strip()
    return f"Error: {text}" if result.is_error else text


server = FastMCP("google", instructions=f"Google Workspace through google-doors. Accounts: {NAMES}. "
                 "Call gw_discover(service) to see tool names and parameters, then gw(account, tool, params).")


@server.tool(description=f"Call one Google Workspace tool on one account. Accounts: {NAMES}. params holds the tool's "
             "arguments as an object; user_google_email is filled in for you. Common tools: search_gmail_messages(query), "
             "get_gmail_message_content(message_id), draft_gmail_message(subject, body, to), list_calendars(), "
             "get_events(time_min, time_max), query_freebusy(time_min, time_max), search_drive_files(query), "
             "get_doc_as_markdown(document_id), create_doc(title, content), read_sheet_values(spreadsheet_id, "
             "range_name), create_spreadsheet(title), get_presentation(presentation_id). gw_discover lists the rest.")
async def gw(account: str, tool: str, params: dict | None = None) -> str:
    return await _call(account, tool, params)


@server.tool(description="List the tools one service offers, with their parameters (* required, ? optional). "
             f"Services: {', '.join(kit.SERVICES)}, search. Leave service empty for all of them.")
async def gw_discover(service: str | None = None) -> str:
    key = service or "all"
    if key not in _listed:
        if not ACCOUNTS:
            return "Error: no account yet. Run ./setup in the google-doors folder."
        try:
            async with Client(_transport(ACCOUNTS[0], [service] if service else list(kit.SERVICES)), timeout=60) as c:
                tools = await c.list_tools()
        except Exception as error:
            return f"Error: {type(error).__name__}: {error}"
        lines = []
        for tool in sorted(tools, key=lambda t: t.name):
            schema = getattr(tool, "input_schema", None) or {}
            needed = set(schema.get("required", []))
            params = [f"{name}{'*' if name in needed else '?'}" for name in schema.get("properties", {})
                      if name != "user_google_email"]
            lines.append(f"{tool.name}({', '.join(params)})\n    {(tool.description or '').strip().splitlines()[0][:110]}")
        _listed[key] = f"{key}: {len(tools)} tools\n" + "\n".join(lines)
    return _listed[key]


@server.tool(description=f"Run several tools on one account at once. Accounts: {NAMES}. "
             'calls is a list of {"tool": name, "params": {...}}; the answer lists each result in order.')
async def gw_batch(account: str, calls: list[dict]) -> str:
    async def one(index, call):
        if not call.get("tool"):
            return {"index": index, "error": "this call names no tool"}
        return {"index": index, "tool": call["tool"], "result": await _call(account, call["tool"], call.get("params"))}
    return json.dumps(await asyncio.gather(*(one(i, c) for i, c in enumerate(calls))), indent=1)


if __name__ == "__main__":
    server.run(show_banner=False)
