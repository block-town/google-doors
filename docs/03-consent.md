# 03 · The consent screen

Step 3 of 7, about five minutes. Previous: [02 · The APIs](02-apis.md). Next: [04 · The client](04-client.md)

## What it is

The consent screen is the page Google shows when a program asks for your data: the app's name, who made it, and what it wants to touch. In the Google Cloud console its settings live under **Google Auth platform**, in pages named Overview, Branding, Audience, Clients, Data Access and Verification Center ([Google's help page](https://support.google.com/cloud/answer/15544987), read 2026-10-05).

## Why Google wants it

Google shows each person who is asking before they say yes, and it limits apps nobody at Google has reviewed. Two settings decide those limits: who may use the app (the audience), and whether it's published.

## How

The clicks below come from Google's guide [Configure the OAuth consent screen](https://developers.google.com/workspace/guides/configure-oauth-consent) (updated 2026-09-03, read 2026-10-05).

1. Open **Branding**: [console.developers.google.com/auth/branding](https://console.developers.google.com/auth/branding), the address behind Google's "Go to Branding" button. The menu route is Menu > Google Auth platform > Branding. Check the project picker shows your project.
2. If the page says **Google Auth platform not configured yet**, click **Get Started**.
3. Under **App Information**: in **App name**, type a name you'll recognise, such as `Desk Assistant`. Google's rules forbid names that could pass for Google's own products, so leave out words like Google and Gmail ([Google's naming rules](https://support.google.com/cloud/answer/15544987)). In **User support email**, choose your address. Click **Next**.
4. Under **Audience**, choose the user type, then click **Next**:
   - **Internal** if this is a Workspace account and your project sits in that organisation ([01](01-project.md), step 4). Only people in your organisation can sign in.
   - **External** for a gmail.com account, or a Workspace account whose project has no organisation.
5. Under **Contact Information**, type an **Email address** where Google can reach you about the project. Click **Next**.
6. Under **Finish**, read the Google API Services User Data Policy and, if you agree, select **I agree to the Google API Services: User Data Policy**. Click **Continue**, then **Create**.
7. **External only, add yourself as a test user.** Click **Audience**. Under **Test users**, click **Add users**, enter your address, and click **Save**.
8. **External only, publish.** On the same **Audience** page, find the publishing status and click **Publish app**. Google's [Manage App Audience](https://support.google.com/cloud/answer/15549945) page says a project counts as In production "after selecting the Publish app button". Google may ask you to confirm.

Skip **Data Access**. Google's guide says you list scopes there for apps "used by people outside your Google Workspace organization", ahead of Google's review. Your app asks for its scopes when you sign in, and an unlisted scope brings the same unverified-app warning you'll see anyway ([Google's page](https://support.google.com/cloud/answer/15549135)).

**You should see** the **Audience** page show your user type and a publishing status: **In production** after step 8, **Testing** without it. `./setup` asks which one you have.

## The 7-day trap

This choice decides how long your sign-in lasts. Google's words, read 2026-10-05:

- **Testing.** "A Google Cloud Platform project with an OAuth consent screen configured for an external user type and a publishing status of 'Testing' is issued a refresh token expiring in 7 days" ([Google's OAuth page](https://developers.google.com/identity/protocols/oauth2), section "Refresh token expiration"). The [Manage App Audience](https://support.google.com/cloud/answer/15549945) page adds that a Testing app takes at most 100 test users. So in Testing, Claude loses access every week and you run `./auth` again.
- **In production, not verified by Google.** Your sign-in doesn't expire after 7 days. Google shows an "unverified app" warning before the consent screen, because the app asks for sensitive scopes Google hasn't reviewed, and it caps the app at "100 new users in total" over the project's life. You're one user.
- **Internal.** No test users, no 7-day limit, and Google's [unverified apps page](https://support.google.com/cloud/answer/7454865) says internal apps don't need verification. Your Workspace admin may still need to trust the app for Gmail and Drive ([05](05-admin.md)).

| You have | Sign-in lasts | Warning screen | Who can sign in |
|---|---|---|---|
| Internal | until revoked or unused for six months | no | your organisation |
| External, In production | until revoked or unused for six months | yes, "Google hasn't verified this app" | any Google account, 100 in the project's lifetime |
| External, Testing | 7 days | yes | your test users, 100 at most |

The Analytics sign-in ([07](07-first-call.md)) comes from the same app, so the same row applies to it.

The six months come from the same OAuth page, which lists the other ways a token stops working: you revoke it, you change your password while it holds Gmail scopes, or your admin restricts a service it uses.

### The warning screen is yours to pass

When you sign in ([07](07-first-call.md)), Google shows "Google hasn't verified this app". You built the app and you're the only one using it, so continuing is safe. Google's own [gws CLI guide](https://github.com/googleworkspace/cli) (read 2026-10-05) gives the two forms the screen takes: a **Continue** button for a test user, or **Advanced** then **Go to <your app name> (unsafe)**.

## What it lets you do

Sign in once and keep working: published or Internal, the sign-in lasts until you end it. Google shows your app's name on the consent screen, so you always know which program you're letting in.

## If it fails

- **"Access blocked" when you sign in.** Your app is External and in Testing, and your address isn't a test user. Add it (step 7) or publish (step 8). Google's gws CLI guide gives this cause for "Access blocked" (read 2026-10-05).
- **Error `org_internal`.** You chose Internal, then signed in with an account outside the organisation. Google's Manage App Audience page names this error. Sign in with an organisation account, or change the user type to External on the Audience page.
- **Claude stops working every week.** The app is still in Testing. Publish it (step 8), record it with `./setup --audience production`, then run `./auth`.
