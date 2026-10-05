# 02 · The APIs

Step 2 of 7, about two minutes. Previous: [01 · The project](01-project.md). Next: [03 · The consent screen](03-consent.md)

## What it is

An API is a door a program uses to reach one Google app. Gmail has a door, Drive has another, Calendar a third. A new project has every door shut.

## Why Google wants it

You open only the doors your program needs. If your client ever leaked, it could reach those apps and no others. Google also counts calls per API, so each door has its own limits.

## How

The API names and IDs below come from Google's page [Enable Google Workspace APIs](https://developers.google.com/workspace/guides/enable-apis) (updated 2026-09-03, read 2026-10-05).

### The one link

Open this link with your project selected. It asks Google to turn on all thirteen APIs the kit can use: the ten Workspace ones it uses by default, Chat for Workspace accounts, and the two Analytics ones. A gmail.com account uses twelve of them, since Chat needs Workspace:

[console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com,drive.googleapis.com,calendar-json.googleapis.com,docs.googleapis.com,sheets.googleapis.com,slides.googleapis.com,forms.googleapis.com,tasks.googleapis.com,people.googleapis.com,script.googleapis.com,chat.googleapis.com,analyticsadmin.googleapis.com,analyticsdata.googleapis.com](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com,drive.googleapis.com,calendar-json.googleapis.com,docs.googleapis.com,sheets.googleapis.com,slides.googleapis.com,forms.googleapis.com,tasks.googleapis.com,people.googleapis.com,script.googleapis.com,chat.googleapis.com,analyticsadmin.googleapis.com,analyticsdata.googleapis.com)

Google uses this form of link, with several API IDs separated by commas, in its own [Chat app quickstart](https://developers.google.com/workspace/chat/quickstart/gcf-app) (read 2026-10-05). Check the project name the page shows and confirm what it asks. Turning on the Chat API costs nothing on a gmail.com account; the kit leaves Chat's tools off unless you ask for them.

### One at a time

Google's route in the console: Menu > **APIs & Services** > **Library** > **Google Workspace**. Click an API, then click **Enable**. Repeat for each row:

| Service | Google's name for the API | Its ID |
|---|---|---|
| Gmail | Gmail API | `gmail.googleapis.com` |
| Drive | Drive API | `drive.googleapis.com` |
| Calendar | Calendar API | `calendar-json.googleapis.com` |
| Docs | Docs API | `docs.googleapis.com` |
| Sheets | Sheets API | `sheets.googleapis.com` |
| Slides | Slides API | `slides.googleapis.com` |
| Forms | Forms API | `forms.googleapis.com` |
| Tasks | Tasks API | `tasks.googleapis.com` |
| Contacts | People API | `people.googleapis.com` |
| Apps Script | Apps Script API | `script.googleapis.com` |
| Chat, Workspace accounts only | Chat API | `chat.googleapis.com` |
| Analytics, accounts and properties | Google Analytics Admin API | `analyticsadmin.googleapis.com` |
| Analytics, reports | Google Analytics Data API | `analyticsdata.googleapis.com` |

The Calendar API's ID is `calendar-json.googleapis.com`. People often type `calendar.googleapis.com`, which isn't it.

Chat is optional. It works on Workspace accounts alone, and [05](05-admin.md) covers the extra setup it needs. The two Analytics APIs are the ones Google's [analytics-mcp README](https://github.com/googleanalytics/google-analytics-mcp) names (read 2026-10-05); the first eleven IDs come from Google's Workspace page above.

### One command

If you use Google's `gcloud` tool and are signed in to it:

```
gcloud services enable gmail.googleapis.com drive.googleapis.com calendar-json.googleapis.com docs.googleapis.com sheets.googleapis.com slides.googleapis.com forms.googleapis.com tasks.googleapis.com people.googleapis.com script.googleapis.com chat.googleapis.com analyticsadmin.googleapis.com analyticsdata.googleapis.com --project=PROJECT_ID
```

**You should see** each API's page in the console report it as enabled. `./doctor` checks each one later and prints the link for any that's still off.

## What it lets you do

Each open door lets the server's tools for that app work: the Gmail API for `search_gmail_messages` and `draft_gmail_message`, the Sheets API for `read_sheet_values` and `modify_sheet_values`, the two Analytics APIs for `get_account_summaries` and `run_report`, and so on.

## If it fails

- **`./doctor` prints `api` on a line.** That API is still shut. The line under it gives the link that opens it. The server's own message says to allow a minute or two after enabling before you try again.
- **The link opens the wrong project.** Pick your project in the selector at the top of the console, then open the link again.
- **Calendar fails while the rest work.** Check that you enabled `calendar-json.googleapis.com`.
