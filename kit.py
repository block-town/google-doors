"""Shared by setup, auth, auth-analytics and doctor. Python standard library only; nothing here touches the network."""
import datetime, json, os, queue, re, shutil, subprocess, sys, threading, time
from pathlib import Path
from urllib.parse import quote, unquote

sys.stdout.reconfigure(line_buffering=True)   # prompts and prints stay in order when piped

PACKAGE, VERSION = "workspace-mcp", "2.0.1"   # the server, pinned: pypi.org/project/workspace-mcp/2.0.1 (2026-10-04)
ANALYTICS = ("analytics-mcp", "0.7.0")         # Google's Analytics server: pypi.org/project/analytics-mcp/0.7.0 (2026-07-29)
PINS = {PACKAGE: (VERSION, "server-constraints.txt"), ANALYTICS[0]: (ANALYTICS[1], "analytics-constraints.txt")}
KIT = Path(__file__).resolve().parent
HOME = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "google-doors"
DEFAULT = ["gmail", "drive", "calendar", "docs", "sheets", "slides", "forms", "tasks", "contacts", "appscript"]
ENABLE = "https://console.cloud.google.com/flows/enableapi?apiid="
# service: (Google's API id, the read-only call doctor makes). The three ids are Google's public quickstart samples.
SERVICES = {
    "gmail": ("gmail.googleapis.com", "search_gmail_messages", {"query": "in:inbox", "page_size": 1}),
    "drive": ("drive.googleapis.com", "list_drive_items", {"folder_id": "root", "page_size": 1}),
    "calendar": ("calendar-json.googleapis.com", "list_calendars", {"max_results": 1}),
    "docs": ("docs.googleapis.com", "get_doc_content", {"document_id": "195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE"}),
    "sheets": ("sheets.googleapis.com", "read_sheet_values",
               {"spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", "range_name": "Class Data!A1:B2"}),
    "slides": ("slides.googleapis.com", "get_presentation", {"presentation_id": "1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc"}),
    "forms": ("forms.googleapis.com", "list_form_responses", {"form_id": "google-doors-probe", "page_size": 1}),
    "tasks": ("tasks.googleapis.com", "list_task_lists", {"max_results": 1}),
    "contacts": ("people.googleapis.com", "list_contact_groups", {"page_size": 1}),
    "appscript": ("script.googleapis.com", "get_script_activity", {"action": "processes", "page_size": 1}),
    "chat": ("chat.googleapis.com", "list_spaces", {"page_size": 1}),
}


def valid_account(name):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,29}", name):
        sys.exit(f"'{name}' can't be an account name: use lowercase letters, digits and dashes, 30 at most.")
    return name


def folder(account): return HOME / account
def config_path(account): return folder(account) / "config"
def tokens(account): return folder(account) / "tokens"
def accounts(): return sorted(p.parent.name for p in HOME.glob("*/config"))
def entry_name(account, kind="google"): return kind if account == "main" else f"{kind}-{account}"
def analytics_file(account): return folder(account) / "analytics.json"
def now(): return datetime.datetime.now().astimezone()


def check(data):
    """The config's shape, checked before anything acts on it. Returns the problem, or None."""
    try:
        client, mine = data["installed"], data["kit"]
        if not client["client_id"].endswith(".apps.googleusercontent.com"): return "the client id has the wrong shape"
        if not client["client_secret"]: return "the client secret is empty"
        if "@" not in mine["email"]: return "the address has no @"
        if not mine["services"] or not set(mine["services"]) <= set(SERVICES): return "the service list is wrong"
        if mine["audience"] not in ("internal", "production", "testing"): return "the audience is unknown"
        if not mine["server"]: return "the server path is missing"
        if not set(mine.get("options", [])) <= {"--read-only", "--disabled-tools", "send_gmail_message"}: return "unknown options"
        if not isinstance(mine.get("analytics", ""), str): return "the analytics entry is wrong"
    except (KeyError, TypeError, AttributeError):
        return "a field is missing"
    return None


def load(account):
    path = config_path(valid_account(account))
    if not path.exists():
        sys.exit(f"No account '{account}' yet. Run: ./setup --account {account}")
    try:
        data = json.loads(path.read_text())
    except ValueError:
        data = None
    problem = check(data) if isinstance(data, dict) else "it isn't JSON"
    if problem:
        sys.exit(f"{path} can't be used: {problem}. Run ./setup --account {account} to write it again.")
    return data


def private_dir(path):
    """Make path, and each folder between it and HOME, readable by you alone."""
    for p in reversed([path, *(p for p in path.parents if str(p).startswith(str(HOME)))]):
        p.mkdir(mode=0o700, parents=True, exist_ok=True)
        p.chmod(0o700)


def private_write(path, text):
    """Write a file only your user can read, in one step, so no half-written copy is left behind."""
    if str(path).startswith(str(HOME)):
        private_dir(path.parent)
    tmp = path.with_name(path.name + ".tmp")
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as handle:
        handle.write(text)
    os.replace(tmp, path)


def save(account, data):
    if check(data):
        sys.exit(f"Refusing to write a broken config: {check(data)}.")
    private_write(config_path(account), json.dumps(data, indent=1) + "\n")


def entry_env(account, data):
    """What the server needs to find this account. The secret stays in the config file; only its path is here."""
    base = folder(account)
    return {"GOOGLE_CLIENT_SECRET_PATH": str(config_path(account)), "USER_GOOGLE_EMAIL": data["kit"]["email"],
            "WORKSPACE_MCP_CREDENTIALS_DIR": str(tokens(account)), "WORKSPACE_MCP_LOG_DIR": str(base / "logs"),
            "WORKSPACE_ATTACHMENT_DIR": str(base / "attachments")}


def server_args(data, services=None):
    return ["--single-user", "--tools", *(services or data["kit"]["services"]), *data["kit"].get("options", [])]


def clean_env():
    # Google settings left in your shell would override this account's, so they are dropped here. PORT too: the
    # server reads it for its sign-in listener, and a web developer's shell often exports one.
    return {k: v for k, v in os.environ.items()
            if not k.startswith(("GOOGLE_", "WORKSPACE_", "USER_GOOGLE", "MCP_")) and k != "PORT"}


def server_env(account, data): return {**clean_env(), **entry_env(account, data)}
def analytics_env(account): return {"GOOGLE_APPLICATION_CREDENTIALS": str(analytics_file(account))}


def shell_overrides():
    return sorted(k for k in os.environ if k.startswith(("GOOGLE_OAUTH_", "GOOGLE_CLIENT_SECRET", "WORKSPACE_MCP_")))


def token_files(account):
    """Tokens the server wrote: <address>.json. Files moved aside end in a date, so they don't count."""
    return sorted(p for p in tokens(account).glob("*.json") if "@" in unquote(p.stem))


def token_path(account, email): return tokens(account) / (quote(email, safe="@._-") + ".json")


def uv():
    found = shutil.which("uv")
    if found: return found
    for place in (os.environ.get("XDG_BIN_HOME"), Path.home() / ".local" / "bin"):
        if place and (Path(place) / "uv").exists(): return str(Path(place) / "uv")
    return None


def installed(uv_path, package=PACKAGE):
    """The version of a package uv has installed as a tool, or None."""
    out = subprocess.run([uv_path, "tool", "list"], capture_output=True, text=True).stdout
    found = re.search(rf"^{package} v(\S+)", out, re.M)
    return found.group(1) if found else None


YES = "--yes" in sys.argv   # the person said yes to the --dry-run plan, in the terminal or to Claude in the chat


def ask(question, default=False):
    if YES:
        print(f"{question} yes (--yes)")
        return True
    answer = input(f"{question} [{'Y/n' if default else 'y/N'}] ").strip().lower()
    return default if not answer else answer in ("y", "yes")


def done(text, code=0):
    print(f"\ngoogle-doors {now():%Y-%m-%d %H:%M}: {text}")
    sys.exit(code)


def guarded(main):
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        done("stopped at a prompt. Nothing past that point was changed.", 130)


def workspace(account, data, extra=None):
    return Server([data["kit"]["server"], *server_args(data)], {**server_env(account, data), **(extra or {})})


def analytics(account, data):
    return Server([data["kit"]["analytics"]], {**clean_env(), **analytics_env(account)})


class Server:
    """One MCP server process, spoken to over stdio in MCP's own JSON messages, as Claude Code runs it."""

    def __init__(self, command, env):
        self.proc = subprocess.Popen(command, text=True, env=env,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.inbox, self.log, self.last = queue.Queue(), [], 0
        threading.Thread(target=self._pump, args=(self.proc.stdout, self.inbox.put), daemon=True).start()
        threading.Thread(target=self._pump, args=(self.proc.stderr, self.log.append), daemon=True).start()
        self.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                    "clientInfo": {"name": "google-doors", "version": "1"}}, 90)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    @staticmethod
    def _pump(stream, put):
        for line in stream:
            put(line.rstrip("\n"))
        put(None)

    def _send(self, message):
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()

    def request(self, method, params, timeout):
        self.last += 1
        self._send({"jsonrpc": "2.0", "id": self.last, "method": method, "params": params})
        deadline = time.time() + timeout
        while True:
            try:
                line = self.inbox.get(timeout=max(0.1, deadline - time.time()))
            except queue.Empty:
                raise TimeoutError(f"no answer to {method} in {timeout} s") from None
            if line is None:
                raise ConnectionError("the server stopped")
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if "method" in message and "id" in message:   # the server asking us something: decline
                self._send({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": "not supported"}})
            elif message.get("id") == self.last:
                if "error" in message:
                    raise RuntimeError(message["error"].get("message", "error"))
                return message["result"]

    def tools(self):
        return [tool["name"] for tool in self.request("tools/list", {}, 60)["tools"]]

    def call(self, tool, arguments, timeout=90):
        """One tool call. Returns (ok, text)."""
        result = self.request("tools/call", {"name": tool, "arguments": arguments}, timeout)
        text = "\n".join(part.get("text", "") for part in result.get("content", []) if part.get("type") == "text")
        return not result.get("isError"), text

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self.proc.kill()
