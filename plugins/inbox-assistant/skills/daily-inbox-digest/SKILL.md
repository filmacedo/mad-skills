---
name: daily-inbox-digest
description: Process new Gmail since the previous successful run, apply authorized routing, and produce an action-first daily brief. Use for scheduled or manually requested daily inbox processing, not the initial audit.
---

# Daily Inbox Digest

Protect the Inbox for people and timely action, apply only approved routing preferences, and return a useful daily brief.

Read the shared general, classification, security, memory, and daily digest policies. Resolve and validate the supplied memory root before Gmail access. If persona or state cannot be loaded, do not mutate Gmail or invent a checkpoint.

## Run safely

- Verify each authenticated Gmail address against its configured mailbox.
- Use that mailbox's last successful `daily` cutoff as the exclusive lower bound; use 24 hours only on a genuine first run.
- Search All Mail through one captured cutoff, exclude Sent, Drafts, Spam, and Trash, complete pagination, and deduplicate exact messages.
- Classify every candidate by purpose and attention before writing.
- Leave human, actionable, suspicious, and unapproved ambiguous mail untouched.
- Apply only explicitly allowed labels and archive actions, preserving unrelated message state.
- Verify every write. A failed mailbox retains its checkpoint; other mailboxes may complete.

## Brief

Follow `policy/digest.md`. Lead with whether action is required. For each action, include why it matters, reply need, deadline, next action, and an account-routed Gmail link. Disclose every routine message handled exactly once.

Advance a mailbox checkpoint only after complete search, classification, authorized writes, verification, and reporting.

## Corrections

When the user corrects a classification, action, sender rule, or digest preference, distinguish an exact-message correction from an ongoing preference or standing permission. Persist only clearly authorized scope with `scripts/memory_store.py`; reconcile existing Gmail state only when requested. Never turn casual feedback into unsubscribe, spam, block, or filter authority.
