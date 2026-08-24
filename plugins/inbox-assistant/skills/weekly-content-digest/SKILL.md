---
name: weekly-content-digest
description: Create a read-only weekly Gmail reading brief from newsletters, articles, interviews, analysis, and curated links. Use for the weekly content digest, not daily cleanup or event discovery.
---

# Weekly Content Digest

Help the user decide what is worth reading from newly received editorial mail.

Read the shared general, classification, security, memory, and weekly digest policies. Validate the supplied memory root and use only the `weekly_content` pipeline. Never read or advance the daily or events checkpoint.

- Verify every configured Gmail address and keep account results isolated.
- Use the exact previous successful cutoff, or seven days on a genuine first run.
- Search All Mail through one captured cutoff, excluding Sent, Drafts, Spam, and Trash; complete pagination and recover qualifying mail that may lack its expected label.
- Separate editorial value from a sender's own product marketing.
- Summarize enough substance to judge relevance, preserve source links, and include every qualifying message once.
- Follow the content section of `policy/weekly-digest.md` and the user's stored source, topic, account-tag, timezone, and verbosity preferences.

This workflow is read-only. Advance each mailbox checkpoint only after its full digest is reported. Handle later user corrections through the scoped memory rules; never edit shared policy automatically.
