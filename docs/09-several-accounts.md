# 09 · A second account

After the setup. Previous: [08 · The uses](08-uses.md). Next: [10 · Trouble](10-trouble.md)

## What it is

A second Google account working alongside the first: a work address next to a personal one, say. Each account gets its own client, its own config folder and its own token, so the two never mix.

## Why it's set up apart

Google ties each token to one account, and the server in its single-user mode uses whichever token it finds in its folder. Two folders keep two accounts from ever answering for each other. A client per account keeps their tokens apart at Google's end too. Google's [OAuth page](https://developers.google.com/identity/protocols/oauth2) limits each account to 100 live tokens per client (read 2026-10-05). One public repo, [evolsb/claude-code-google-workspace](https://github.com/evolsb/claude-code-google-workspace), reports that signing a second account in through the same client made Google drop the first account's token (read 2026-10-05). Google's pages describe no such rule, and this kit wasn't tested either way, so the safe path is one client per account.

## How

1. **Repeat the Google steps for the second account.** For a Workspace account, make the project inside that organisation and choose Internal ([01](01-project.md) to [05](05-admin.md)): its admin rules apply to it. For a second gmail.com account you may reuse your first project: open its **Clients** page and make a second Desktop app client ([04](04-client.md)), then add the second address as a test user or keep the app published ([03](03-consent.md)).
2. **Run setup with a name for it:**

   ```
   ./setup --account work
   ```

   Names are lowercase letters, digits and dashes. Setup writes `~/.config/google-doors/work/config` and adds two more servers to Claude Code, named `google-work` and `analytics-work` (leave the second out with `--no-analytics`).
3. **Sign in, one account at a time.** Setup offers it at the end, or run `./auth --account work`, then `./auth-analytics --account work`. Pick the second account on Google's first screen.
4. **Check it:** `./doctor --account work`.

**You should see** `every service answered for 'work'`, and the new servers in Claude Code when you run `claude mcp list`: `google-work` and `analytics-work` beside `google` and `analytics`.

### Tell Claude which account

Name it in the prompt: "Using my work account, list tomorrow's meetings." Claude Code shows each tool with its server's name, so a call to `google-work` acts on the work account.

### Or use the gateway

With two or more accounts, the [gateway](../gateway/README.md) serves them all as one server with three tools, and Claude passes the account name in each call:

```
./setup --gateway
claude mcp remove google-work -s user
```

The first line replaces the `google` entry with the gateway; the second removes the per-account entry it makes redundant. Repeat that removal for each extra account. The gateway covers the Workspace server only: each account keeps its own `analytics` entry. [gateway/README.md](../gateway/README.md) says when the gateway is worth it.

## What it lets you do

Work across both in one request: "Copy the three meetings on my work calendar this Friday into my personal calendar as busy blocks, with no details." Claude reads through one server and writes through the other, and you approve each call.

## If it fails

- **`./auth` says you signed in as the wrong address.** Google's first screen offered the other account and it got picked. Run `./auth --account work` again and pick the right one.
- **Port 8000 is taken while you sign in.** A server for the other account may hold it during its own sign-in. Finish one sign-in before you start the next; `./auth` falls back to ports 8001 to 8004 when it can.
- **A Workspace account fails with `admin`.** That organisation's admin has to trust your second client as well ([05](05-admin.md)).
