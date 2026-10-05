# 01 · The project

Step 1 of 7, about three minutes. Previous: [00 · The map](00-map.md). Next: [02 · The APIs](02-apis.md)

## What it is

A Google Cloud project is a named box in Google's console. Your APIs, your consent screen and your client all live inside one.

## Why Google wants it

Google counts and limits every API call by project, and the consent screen tells people which project is asking. A project also gives you one place to switch it all off: delete the project and its client stops working.

## How

The labels below come from Google's guide [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project) (updated 2026-09-03, read 2026-10-05).

1. Open [console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate), the address behind Google's "Go to Create a Project" button. Sign in with the Google account you want Claude to work in. The console's menu route to the same page is Menu > IAM & Admin > Create a Project.
2. In the **Project Name** field, type a name you'll recognise, such as `claude-google`.
3. Leave the **Project ID** as Google fills it, or click **Edit** to choose your own. Google warns that the ID can't change after the project exists.
4. **Location:** for a Workspace account, click **Browse**, pick your organisation, then click **Select**. You need this if you plan to choose Internal in step 3. For a gmail.com account there's no organisation to pick, so leave the field as it is.
5. Click **Create**.

**You should see** the console's Dashboard. In Google's words, "your project is created within a few minutes". Check that the project picker at the top of the page shows your project's name before you go on: every later step acts on the project selected there.

One command does the same, if you already use Google's `gcloud` tool: `gcloud projects create PROJECT_ID`.

## What it lets you do

Open the doors (APIs) in [02](02-apis.md), set up the consent screen in [03](03-consent.md) and make the client in [04](04-client.md), all inside this one box.

## If it fails

- **No organisation to pick on a Workspace account.** Google's guide says this means "you aren't signed in to a Google Workspace account". Check the account in the top right of the console.
- **The console asks for a billing account or a card.** These APIs need neither: Google's limits pages for Gmail, Drive, Calendar, Docs, Sheets, Slides and Forms each say standard use "is available at no additional cost" (read 2026-10-05). Later, the Google Auth Platform's Overview page runs a "Project Checkup" that recommends a billing account ([Google's page](https://support.google.com/cloud/answer/15548748)). You can leave that warning in place.
- **Your Workspace blocks project creation.** Some organisations limit who may create projects. Ask your admin, or ask them to create the project and add you to it.
