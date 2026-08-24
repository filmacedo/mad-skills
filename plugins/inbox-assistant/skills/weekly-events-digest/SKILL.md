---
name: weekly-events-digest
description: Create a read-only weekly Gmail event-discovery brief with dates, locations, relevance, and source links. Use for the weekly events digest, not daily logistics or content reading.
---

# Weekly Events Digest

Help the user decide which newly discovered events may be worth attending.

Read the shared general, classification, security, memory, and weekly digest policies. Validate the supplied memory root and use only the `weekly_events` pipeline. Never read or advance the daily or content checkpoint.

- Verify every configured Gmail address and keep account results isolated.
- Use the exact previous successful cutoff, or seven days on a genuine first run.
- Search All Mail through one captured cutoff, excluding Sent, Drafts, Spam, and Trash; complete pagination and expand event roundups.
- Deduplicate the same event while retaining each useful source link.
- Separate discovery from tickets, confirmations, cancellations, venue changes, deadlines, and logistics; operational mail belongs in the daily digest.
- Follow the events section of `policy/weekly-digest.md` and the user's stored geography, horizon, timezone, relevance, and presentation preferences.

This workflow is read-only. Advance each mailbox checkpoint only after its full digest is reported. Handle later user corrections through the scoped memory rules; never edit shared policy automatically.
