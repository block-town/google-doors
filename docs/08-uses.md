# 08 · The uses

After the setup. Previous: [07 · The first call](07-first-call.md). Next: [09 · A second account](09-several-accounts.md)

One request can do a whole job. This page takes one such job apart, beat by beat: the prompt for each beat, the tools Claude needs, and what changes in your account. Claude picks its own tools, so treat the tool lists as the expected route. Tool names are the servers' own (workspace-mcp 2.0.1, analytics-mcp 0.7.0), checked on 2026-10-05. Swap in your own client, files and addresses.

Claude Code asks before each tool call. Read the call before you approve it, above all the ones marked **sends**, **shares** or **books**.

## The whole job

```
Check my mail for anything from the client. If they sent the deck, read it and their comments, rebuild it in our style with a financial model, put the model in a sheet they can use, send it all back, book a time to go over it, then get me my analytics for the week.
```

Claude splits it into the beats below and asks before each step that changes something. On a first run, take the beats one at a time.

| # | Beat | Changes in your account |
|---|---|---|
| 1–2 | [Mail from the client, with the deck attached](#12-mail-from-the-client) | nothing in Google; saves the attachment on this computer |
| 3 | [The comments on their Slides deck](#3-the-comments-on-their-slides) | nothing: read-only |
| 4–7 | [The deck rebuilt and uploaded back as Slides](#47-the-deck-rebuilt-and-uploaded-back) | creates one Slides file |
| 7 | [A PDF of the deck](#7-a-pdf-of-the-deck) | nothing in Google; saves a PDF on this computer |
| 8 | [The model in a Sheet, formatted and shared](#8-the-model-in-a-sheet) | creates one spreadsheet; **shares** it, and Google emails the client |
| 9 | [Their doc edited in place, comments answered and resolved](#9-their-doc-edited-and-the-comments-resolved) | edits a doc; posts comment replies; resolves comments |
| 10 | [The reply in the thread, with the PDF and the links](#10-the-reply-in-the-thread) | **sends** one email |
| 11 | [An hour that suits both, with a Meet link](#11-an-hour-that-suits-both) | **books** an event; Google emails the invite |
| 12 | [The week's Analytics in a Doc](#12-the-weeks-analytics-in-a-doc) | creates one doc; reads Analytics |

A safe first prompt, read-only:

```
Tell me what's on my calendar this week and which emails from the last three days are still waiting for a reply from me. Change nothing.
```

## 1–2. Mail from the client

```
Check my mail from the last three days for anything from client.example. If one has a presentation attached, save the attachment and tell me in a few lines what each slide says.
```

Tools: `search_gmail_messages`, `get_gmail_message_content`, `get_gmail_attachment_content`. The last one saves the file on this computer, in `~/.config/google-doors/main/attachments/`, and returns its path. Claude then reads the slides with whatever this computer has: Claude Code may ask to install a package such as `python-pptx` to open a `.pptx`, and it asks before it installs.

## 3. The comments on their Slides

```
Open the client's Google Slides deck at <link> and list every comment: who wrote it, on which slide, and what it asks for. Change nothing.
```

Tools: `get_presentation`, `list_presentation_comments`. Read-only. Since 2.0.1 the server prints each comment's anchor, so Claude can say which element a comment sits on (the server's release notes for v2.0.1, read 2026-10-05).

## 4–7. The deck rebuilt and uploaded back

```
Rebuild the deck I saved from the client's mail in our house style: our logo, our colours, one idea per slide, and a slide with the financial model as a table and a chart. Answer each of their comments in the slides themselves. Save it as a .pptx in ~/.config/google-doors/main/attachments, then upload it to my Drive as Google Slides.
```

Tools: Claude Code itself for the rebuild, on this computer, with whatever deck tool you use; the model starts as a CSV it writes. Then `import_to_google_slides`, which the server describes as importing a PPTX "into Google Slides format with automatic conversion". Creates one Slides file in your Drive.

The conversion happens on upload: the tool's code (`gdrive/drive_tools.py`, 2.0.1) sets the Google Slides type as the target. If a file ever lands as a plain `.pptx`, open it from Drive in Google Slides and save it as Slides there.

The server reads local files only from its attachments folder, so the `.pptx` goes there first ([SECURITY.md](../SECURITY.md)).

## 7. A PDF of the deck

```
Export the Google Slides deck we just uploaded as a PDF and keep it on this computer.
```

Tools: `get_drive_file_download_url` with `export_format` set to `pdf`. Its description lists Slides to PDF (the default) or PPTX, Sheets to XLSX, PDF or CSV, and Docs to PDF or DOCX. It saves the file in the attachments folder and returns its path (the server's `core/attachment_storage.py`). For a Doc, `export_doc_to_pdf` saves the PDF into Drive instead.

## 8. The model in a Sheet

```
Make a Google Sheet called "Client model" with one row per month for twelve months and the columns Month, Units, Price, Cost and Margin. Put formulas in the Margin column, format the money as currency, make the header bold, turn margins above 30 percent green, then share the sheet with client@example.com as a commenter.
```

Tools: `create_spreadsheet`; `modify_sheet_values` with `value_input_option` set to `USER_ENTERED`, so a cell like `=(C2-D2)*B2` stays a formula; `format_sheet_range` for the currency format and the bold header; `manage_conditional_formatting` with the action `add` for the green cells; `manage_drive_access` with the action `grant` and the role `commenter`. Creates one spreadsheet and **shares** it: `manage_drive_access` sends Google's share email unless `send_notification` is false (its default is true, per its description).

## 9. Their doc edited and the comments resolved

```
In the client's brief at <link>, replace the numbers section with the figures from our model. Then go through the comments on their Slides deck: reply to each one with what we changed, and resolve the ones we've dealt with. Show me each reply before you post it.
```

Tools: `get_doc_content`, `find_and_replace_doc` or `modify_doc_text`; `list_presentation_comments`, then `manage_presentation_comment` with the actions `reply` and `resolve`. On a Doc, `manage_document_comment` does the same; on a Sheet, `manage_spreadsheet_comment`. Edits one doc, posts replies and resolves comments, all visible to the client.

## 10. The reply in the thread

```
Reply in the client's thread with the PDF attached and links to the Slides deck and the Sheet. Write it as a draft first and show it to me; send it only when I say so.
```

Tools: `get_drive_shareable_link`; `draft_gmail_message` with the thread's `thread_id` and the PDF in `attachments`, then, after your yes, `send_gmail_message`. The server's `send_gmail_message` "sends immediately and cannot schedule", in its own words. **Sends** one email. Attachments come from the attachments folder or from a download link the server made.

## 11. An hour that suits both

```
Find a free hour this week that suits me and client@example.com. Show me the slot first. When I say yes, send an invite called "Deck review" with a Google Meet link.
```

Tools: `query_freebusy`, then `manage_event` with the action `create`, the attendee, and `add_google_meet`. **Books** one event: the server sends Google's invitation to every guest by default (`send_updates` is `all` in version 2.0.1). You see another person's busy times only when their calendar is shared with you.

## 12. The week's Analytics in a Doc

```
Get last week's Google Analytics for my property: users, sessions, the top five pages and the top five traffic sources. Write it up as a short Google Doc called "Analytics, last week".
```

Tools: from the Analytics server, `get_account_summaries` to find the property and `run_report` for the numbers; from the Workspace server, `create_doc`. Reads Analytics, creates one doc. Analytics is read-only through this kit: the sign-in asks for `analytics.readonly` alone.

## Two more the kit does

```
Read the responses to my Google Form named "Workshop sign-up" and put them in a new Google Sheet: one row per response, one column per question, and a first column with the time each response came in.
```

Tools: `search_drive_files`, `get_form`, `list_form_responses`, `create_spreadsheet`, `modify_sheet_values`. Creates one spreadsheet.

```
Write an Apps Script for the spreadsheet named "Client model" that makes the first row bold and freezes it on every tab. Show me the code first. When I say yes, save it as a script bound to that spreadsheet.
```

Tools: `search_drive_files`, `manage_script_project` (create, with the spreadsheet as its parent), `manage_script_content`. Creates one script project. Needs the Apps Script switch ([05](05-admin.md)). To run it, open it at [script.google.com](https://script.google.com) and run it there; Google asks you to authorise it the first time. Claude can run a script itself with `run_script_function` only under Google's conditions for `scripts.run` ([Google's page](https://developers.google.com/apps-script/api/how-tos/execute), read 2026-10-05): the script is deployed as an API executable and shares one standard Cloud project with your client. For the second, open the script, click **Project Settings**, and under **Google Cloud Project** click **Change project**, enter your project's number and click **Set project** ([Google's steps](https://developers.google.com/apps-script/guides/cloud-platform-projects)).

## Safety switches

- **Make sending impossible.** Run `./setup --no-send`. It adds the server's `--disabled-tools send_gmail_message` option, which removes the one tool that sends mail: on 2026-10-05 the server then listed 111 tools instead of 112. Drafts still work, so you send them yourself.
- **Read only.** Run `./setup --read-only`. The server's option of that name "requests only read-only scopes and disables tools requiring write permissions" (its own help text); on 2026-10-05 it left 49 tools, with none for Forms. Then run `./auth`, so Google issues a token with the narrower scopes.
- **Refuse a tool in Claude Code.** A deny rule in Claude Code's settings, such as `"permissions": {"deny": ["mcp__google__send_gmail_message"]}`, stops Claude Code from calling it. Claude Code's [permissions page](https://code.claude.com/docs/en/permissions) gives the `mcp__<server>__<tool>` form (read 2026-10-05).

`./setup` with `--services`, `--chat`, `--read-only` or `--no-send` writes the new choice to your config and to Claude Code's entry, and `./auth` and `./doctor` follow it. Pass every option you want each time: a run with `--services` alone clears `--read-only` and `--no-send`.
