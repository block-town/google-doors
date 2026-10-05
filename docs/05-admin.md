# 05 · Workspace accounts, the Apps Script switch, and Chat

Step 5 of 7. Previous: [04 · The client](04-client.md). Next: [06 · The kit](06-install.md)

This page has three parts. The Apps Script switch is for everyone. The admin part is for Workspace accounts: an address your company, school or own domain gave you, as opposed to a gmail.com one. Chat is optional and needs a Workspace account.

## The Apps Script switch, for everyone

### What it is

A per-person setting in your Google account that lets programs you've authorised manage your Apps Script projects. Google keeps it off by default.

### Why Google wants it

Google's page [Enable script authorization and access](https://developers.google.com/apps-script/api/how-tos/enable) (updated 2026-09-03, read 2026-10-05) explains it: a program that can edit your scripts could plant a harmful one, so "the Apps Script API cannot access your script projects by default". Turning on the API in your project (step 2) isn't enough; you also flip this switch for your own account.

### How

1. Open [script.google.com/home/usersettings](https://script.google.com/home/usersettings) while signed in with the account Claude will use.
2. Click **Google Apps Script API**. Google's [dashboard guide](https://developers.google.com/apps-script/guides/dashboard) says this "opens a new panel with warning text and a toggle switch".
3. Turn the toggle on.

**You should see** the toggle in the on position. The address comes from Google's own error message for this case, as an [open pull request on the server](https://github.com/taylorwilsdon/google_workspace_mcp/pull/1197) quotes it (read 2026-10-05).

### If it fails

`./doctor` prints `switch` on the Apps Script line. With the switch off, Google answers 403 "User has not enabled the Apps Script API". The same pull request reports that Google can also answer 503 "Service error -27", which reads like an outage. Both mean the switch.

## Your Workspace admin trusts the client

### What it is

A Workspace admin decides which outside apps may reach the organisation's data. Your client counts as an outside app until the admin trusts it, even though you made it.

### Why Google wants it

Admins can restrict Gmail and Drive, among others, to trusted apps. Google's page [Control which third-party & internal apps access Google Workspace data](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data) (updated 2026-10-01, read 2026-10-05) says that when a service is restricted, "if an app requests access to a restricted service and you haven't specifically trusted the app, users can't add it". Gmail's and Drive's sensitive scopes, the ones this server uses, sit on that page's high-risk list.

### How, if you're the admin

The clicks below are that page's, for an admin with the Service Settings administrator privilege.

1. Open [admin.google.com](https://admin.google.com). Go to Menu > **Security** > **Access and data control** > **API controls**.
2. Under **App access control**, click **Manage Third-Party App Access**.
3. For **Configured apps**, click **Add app**.
4. Choose **OAuth App Name or Client ID**.
5. Enter your client ID (from [04](04-client.md)) and click **Search**.
6. Point to the app and click **Select**. Check the box for your client ID and click **Select**.
7. Select **Trusted** and click **Configure**.

**You should see** your app in the Configured apps list with access set to Trusted. The page notes that "Trusting an app overrides a service restriction."

If your project lives in your organisation and you chose Internal ([03](03-consent.md)), Google offers a wider switch: on **API controls**, click the **Settings** card, click **Internal apps**, and check **Trust internal apps**. That trusts every app your organisation's own projects own.

### If you're not the admin

Send your admin this, with your client ID filled in:

> I've made an app for my own Google account so Claude Code can work in my mail, files and calendar. It's a Desktop app client in our Google Cloud project, used by me alone. Please trust it: Admin console > Security > Access and data control > API controls > Manage Third-Party App Access > Add app > OAuth App Name or Client ID > `<your client ID>` > Select > Trusted > Configure. Google's page for this: https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data

### If it fails

`./doctor` prints `admin` when Google answers `admin_policy_enforced`. Google's [OAuth page](https://developers.google.com/identity/protocols/oauth2) names that error for the case where an admin set a service your app uses to Restricted. Your admin trusts the client, then you run `./auth`.

Admins see the app as well. The same page says an admin can list every app that reached the organisation's data, with its client ID, its number of users and the scopes it asked for. [SECURITY.md](../SECURITY.md) has more.

## Google Chat, optional

Chat works on Workspace accounts alone. Google's page [Configure the Google Chat API](https://developers.google.com/workspace/chat/configure-chat-api) (updated 2026-09-03, read 2026-10-05) sets two levels:

- **Reading** spaces and messages with your own sign-in needs the Chat API turned on ([02](02-apis.md)) and the client, nothing more.
- **Creating, changing or deleting** needs a Chat app configured in your project. Open the Chat API's **Configuration** page, fill in **App name**, **Avatar URL** and **Description** under **Application info**, turn **Enable interactive features** off, and click **Save**. Google lists "A Business or Enterprise Google Workspace account with access to Google Chat" as the prerequisite.

Then add Chat to the kit: `./setup --chat`, and sign in again when it asks.
