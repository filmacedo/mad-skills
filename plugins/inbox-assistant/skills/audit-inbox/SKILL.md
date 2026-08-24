---
name: audit-inbox
description: Audit Gmail interruption patterns, propose an evidence-backed cleanup plan, and apply only explicitly approved labels, filters, backlog changes, unsubscribes, or blocks. Use for initial inbox cleanup or a deliberate re-audit, not recurring digests.
---

# Audit Inbox

Explain what is interrupting the user, agree on a future mail plan, and implement only the approved Gmail-native changes. The Inbox is for people and timely action; predictable lower-value mail should arrive deliberately.

Read the shared general, classification, security, and memory policies before acting. Read the [audit classification reference](references/classification.md) when grouping history or proposing rules.

## Audit first

- Verify the authenticated address of every requested Gmail connection.
- Keep accounts, message IDs, searches, links, and writes isolated.
- Default to the previous 12 months of All Mail, excluding Sent, Drafts, Spam, and Trash. Use Sent only as reply evidence.
- Complete pagination and report both the full period and recent pattern.
- Classify messages by purpose and attention, not merely sender or Gmail category.
- Read bodies or threads only where ambiguity, safety, or consequence requires it.

The audit is read-only. Separate observed history from proposed rules and completed actions.

## Agree on one plan

Show exact matchers, counts, recent cadence, future handling, backlog handling, and any unsubscribe, spam, or block candidates. Prefer narrow message-pattern rules over sender-wide rules.

Ask for one explicit approval of the final edited plan. Silence is not approval.

## Implement safely

Resolve each search again immediately before mutation. Apply only approved labels, filters, archive actions, unsubscribes, spam reports, or blocks. Preserve unrelated labels and read, starred, and importance state. Verify every change and describe uncertain outcomes honestly.

Persist approved mailbox bindings, output preferences, and scoped behavior in the supplied memory root with `scripts/memory_store.py`. Store compact evidence and message IDs, never bodies or credentials.

Return a concise before/after report and identify anything incomplete. Do not create an automation unless the user explicitly asks.
