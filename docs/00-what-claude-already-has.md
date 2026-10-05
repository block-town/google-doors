# What Claude already has

Read this first. Next: [00 · The map](00-map.md)

Claude can reach your Google account today without this kit. Anthropic runs its own Google connectors, and Google runs MCP servers in preview. This page says what each one does, from their own pages as read on 2026-10-05, and what this kit adds. If the connectors cover your work, use them: they take a minute to switch on.

## Anthropic's Google connectors

Anthropic's help page [Use Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors) (marked "Updated this week" on 2026-10-05) describes three connectors, Gmail, Google Calendar and Google Drive, "available for all users on Claude and Claude Desktop". On Team and Enterprise plans an owner turns them on first. In its words, they let Claude:

- **Gmail:** search and read mail, draft, and "send, reply to, and forward emails", asking your approval before each by default; read "email metadata, including attachment metadata (not attachment content)"; manage labels and threads; list drafts.
- **Google Calendar:** view events and calendars, shared ones included; "create, update, and delete events"; "find mutual availability across attendees"; manage attendees and answer invitations; set up recurring meetings.
- **Google Drive:** search and read Docs, Sheets, Slides, PDFs, images and Office files; "share, move, and trash files", with approval by default; upload "any file type, with optional auto-convert to Google formats"; create folders; "view file permissions and list recent changes"; "save Claude-generated files directly to your Drive".

The same page now describes three more, in beta: **Google Docs, Sheets and Slides** connectors that "edit files live in a pane beside the chat", create new files, and "read and work with comments and suggestions in Google Docs". The page lists their limits: Claude "can't add charts to Google Slides", and the live pane works "on Claude on the web in Chrome and on Claude Desktop with the built-in browser turned on".

Two more lines from that page matter here. "Claude can only access the Gmail, Calendar, and Drive data for the Google account you've connected." And the data Claude retrieves "is stored on Anthropic servers" with its chat.

**In Claude Code.** Claude Code's [MCP page](https://code.claude.com/docs/en/mcp) says connectors you add on claude.ai "are automatically available in Claude Code" when you log in with a claude.ai subscription, and aren't loaded when an API key or a cloud provider supplies the login. It adds that the Gmail and Google Calendar connectors "don't support local OAuth from Claude Code": you connect them at claude.ai. Whether the Docs, Sheets and Slides beta connectors show up in Claude Code wasn't checked.

## Google's own MCP servers

Google runs remote MCP servers for Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat and People ([Google's page](https://developers.google.com/workspace/guides/configure-mcp-servers), updated 2026-09-18). They're a Developer Preview: you join Google's Workspace Developer Preview Program first, make a project and an OAuth client, and add each server as its own connector. Google's list has no Apps Script, Forms, Tasks or Analytics server. [docs/alternatives.md](alternatives.md) covers this route and the open-source ones.

## What this kit adds

The connectors cover a lot, editing included. What they don't list, on that page on 2026-10-05: opening a mail's attachment; writing, running and deploying Apps Script; Forms, Tasks, Contacts and Chat; Analytics; several accounts kept apart. Their editing happens in a pane beside the chat, in Chrome or the desktop app, with you watching. This kit gives Claude Code all of it as tools it calls one after another in a single run, with your own files and the programs on your computer in the loop: it can save a client's attachment, rebuild the deck with your own deck tool, upload it back and mail the result, in one job ([08](08-uses.md)).

| You want to | Anthropic's connectors, 2026-10-05 | This kit |
|---|---|---|
| Read, search, draft and send mail | yes | yes |
| Open a mail's attachment | metadata only, per the help page | yes: `get_gmail_attachment_content` saves the file |
| Book a meeting in a free slot, with a Meet link | yes | yes: `query_freebusy`, `manage_event` with `add_google_meet` |
| Upload and share Drive files | yes | yes |
| Edit a Doc, a Sheet or a Slides deck in place | yes, in the Docs, Sheets and Slides beta, with a live pane on the web and Desktop | yes, from Claude Code: `modify_doc_text`, `find_and_replace_doc`, `modify_sheet_values`, `format_sheet_range`, `batch_update_presentation` |
| Read, answer and resolve comments | Docs comments and suggestions, in the beta | Docs, Sheets and Slides: `manage_document_comment`, `manage_spreadsheet_comment`, `manage_presentation_comment` |
| Export a deck or a doc as PDF, PPTX or DOCX | not listed on the help page | yes: `get_drive_file_download_url`, `export_doc_to_pdf` |
| Forms, Tasks, Contacts, Chat | not listed | yes |
| Write, deploy and run Apps Script | not listed | yes, with the switch in [05](05-admin.md) |
| Read Google Analytics | not listed | yes, through Google's own `analytics-mcp`, read-only |
| Work in several Google accounts | the one account you connected | yes, one folder per account, and a [gateway](../gateway/README.md) |
| Use Claude Code logged in with an API key | not loaded, per Claude Code's page | yes |
| Keep the sign-in on your computer | stored by Anthropic for the connector | yes, in a file only you can read |
| Set it up | switch it on in claude.ai | about 25 minutes in Google's console |

The two routes don't clash. They're separate servers with separate sign-ins, and you can run both: the connectors for a quick question in the Claude app, this kit for the long jobs in Claude Code. `./doctor` says the same in one line.

## What the kit's tools were checked against

The tool names above are the server's own, workspace-mcp 2.0.1 and analytics-mcp 0.7.0, listed by asking each server for its tools on 2026-10-05. The Anthropic column quotes the help page; where the page says nothing, the table says "not listed", which isn't proof the connectors can't do it.
