# 04 · The client

Step 4 of 7, about two minutes. Previous: [03 · The consent screen](03-consent.md). Next: [05 · Workspace accounts](05-admin.md)

## What it is

The client is your program's badge. It has two parts: a **client ID**, which tells Google which program is asking, and a **client secret**, which proves it. Google's [help page on clients](https://support.google.com/cloud/answer/15549257) compares them to a username and a password (read 2026-10-05).

## Why Google wants it

Every request for a token names a client, so Google knows which project's consent screen to show and whose limits to count. A Desktop app client also tells Google the answer comes back to your own computer, at a `localhost` address, so you set up no web address of your own.

## How

The clicks below come from Google's guide [Create access credentials](https://developers.google.com/workspace/guides/create-credentials), section "Desktop app" (updated 2026-09-03, read 2026-10-05).

1. Open **Clients**: [console.developers.google.com/auth/clients](https://console.developers.google.com/auth/clients), the address behind Google's "Go to Clients" button. The menu route is Menu > Google Auth platform > Clients.
2. Click **Create Client**.
3. Click **Application type** > **Desktop app**.
4. In the **Name** field, type a name such as `google-doors`. Google shows this name only in the console.
5. Click **Create**.
6. **Copy both values now.** Google's help page warns that the client secret "will only be shown after you create the client" and "will not be visible or accessible again". Download the JSON file the window offers and note where it lands: setup reads the client from it. You can also copy the **Client ID** and the **Client secret** into a place only you can see. Google's [Gmail quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python) tells you to save "the downloaded JSON file" at this point.

**You should see** your client under "OAuth 2.0 Client IDs" on the Clients page, as Google's guide puts it.

The client ID looks like `000000000000-example.apps.googleusercontent.com`, with your own digits and letters before that ending.

### Where they go

Into `./setup`, and nowhere else ([06](06-install.md)). The main way is the JSON file: `./setup --from-json ~/Downloads/<the file>.json`, or give its path when setup asks, and on the Claude route tell Claude the path. The script reads the file; Claude never opens it. Without the file, you paste the ID and the secret into setup in your own terminal, typing hidden. Setup writes them to `~/.config/google-doors/main/config`, a file only your user can read, and then offers to delete the download, or reminds you to.

The secret is a password. Keep it out of chats, screenshots, commits and shared folders, including this one. Claude doesn't need to see it, and the kit never prints it. The same client serves the Analytics sign-in ([07](07-first-call.md)), so you make one client, not two.

## What it lets you do

Sign in as yourself through your own client: Google sends your data to your program alone, and your project's limits apply to nobody else.

## If it fails

- **You closed the window before copying the secret.** Google's help page describes how to add a second secret to a client: open the client from the Clients page and click **Add Secret**. Then disable the old one.
- **`./setup` says the client ID has the wrong shape.** You copied something else, such as the project ID or the secret. The client ID looks like `000000000000-example.apps.googleusercontent.com`, with your own digits and letters before that ending.
- **The secret leaked.** Add a new secret, run `./setup` again with it, then disable and delete the old one ([Google's steps](https://support.google.com/cloud/answer/15549257), "Rotating your clients secrets").
- **Months later the client is gone.** Google deletes an OAuth client that has been unused for six months and emails you 30 days before (same page, "Unused Client Deletion"). Each time the server renews your token it asks Google for one, and Google counts that as use.
