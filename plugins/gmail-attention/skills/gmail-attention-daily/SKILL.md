---
name: gmail-attention-daily
description: Run an incremental Gmail attention brief using an approved persona policy and durable per-mailbox state. Use for a scheduled or manually requested daily inbox cleanup; do not use for the initial historical audit or Gmail-filter design.
---

# Gmail Attention Daily

Process only newly received mail, protect the Inbox for people and timely action, apply the user's approved routing preferences, and return an action-first executive brief.

This skill is the reusable operating system for recurring runs. A scheduled task should explicitly invoke `$gmail-attention-daily` and provide only the memory location, mailbox bindings, and delivery context—not copy these instructions into its prompt.

## Load policy and memory

Before accessing Gmail, read:

- [general policy](../../policy/general-policy.md);
- [classification policy](../../policy/classification.md);
- [security policy](../../policy/security.md);
- [persona memory policy](../../policy/memory.md);
- [digest contract](../../policy/digest.md).

Resolve the memory root from the task prompt or user configuration. In a local project, default to `.gmail-attention/`. Validate it with:

```bash
python3 ../../scripts/memory_store.py validate --root <memory-root>
```

If persona or state cannot be loaded, do not mutate Gmail and do not invent a checkpoint. Report the run as incomplete. If the environment cannot provide durable storage, explain that recurring processing is not safely configured.

Require every configured mailbox to include a connection, timezone, allowed labels, allowed actions, and a semantic label map for enabled routing categories. The audit skill normally creates these bindings with the memory helper's `upsert-mailbox` command.

## Verify mailbox identity

For every mailbox in persona configuration:

1. Use only its configured connection or selector.
2. Fetch the authenticated Gmail profile before any search.
3. Require an exact normalized match to the configured address.
4. Keep the mailbox's searches, IDs, labels, links, writes, and state isolated.

Fail only the affected mailbox when identity or access fails. Never substitute another connection. Other verified mailboxes may complete independently.

## Capture the run window

- Capture one current cutoff before searching.
- Use each mailbox's exact most recent successful cutoff in the `daily` pipeline as its exclusive lower bound. Never read or advance a weekly pipeline checkpoint.
- On a genuine first run with no checkpoint, use cutoff minus 24 hours.
- Include exact Gmail received timestamps `> lower_bound` and `<= cutoff`.
- Search All Mail. A query may look back 48 hours to tolerate coarse or delayed search results, but filter locally to the exact window.
- Exclude Sent, Drafts, Spam, and Trash.
- Complete every page and deduplicate by `(mailbox, Gmail message ID, exact received timestamp)`.

Do not advance a checkpoint until that mailbox has completed search, reads, classification, authorized writes, verification, and reporting.

## Classify before acting

For every candidate:

1. Determine semantic purpose and attention level independently.
2. Read the full message or surrounding thread when human authorship, reply need, security, payment, opportunity, deadline, or ambiguity depends on it.
3. Screen potential action items for phishing before recommending an action or link.
4. Apply the most specific active persona preference after shared safety policy.
5. Record which general rule and persona preference produced the decision.

Human-written acknowledgements remain human correspondence even when they need no reply. Mixed-purpose senders must be handled message by message.

## Resolve allowed actions

Persona policy must explicitly define the labels, routing actions, unsubscribe authority, spam/block authority, and digest visibility available for each mailbox.

- Leave Act now, Act later, Suspicious, and unapproved ambiguous messages untouched.
- Leave human correspondence untouched unless a matching explicit persona preference authorizes a different treatment.
- For Routine cleanup, apply only an allowed matching label and archive only if persona policy authorizes it.
- Preserve read state, starred state, importance, and unrelated labels.
- Treat all mutations as idempotent and verify final state.
- For unsubscribe, spam, block, or browser actions, obey the separate approval boundaries in security policy.

Only begin writes after every candidate in that mailbox has been read enough and classified. If a write fails or cannot be verified, mark that mailbox incomplete and retain its checkpoint. Successfully applied idempotent changes may remain for reconciliation.

## Produce the brief

Follow [the digest contract](../../policy/digest.md). Lead with whether the user needs to act now, not with processing statistics.

For attention items, state:

- mailbox/account tag;
- sender and full subject;
- exact received time in the user's timezone;
- why it matters;
- reply needed: Yes or No, with evidence;
- explicit deadline or `No stated deadline`;
- one concrete next action;
- an account-routed Gmail link.

Disclose every routine message exactly once under cleanup. Never silently archive mail. Clearly distinguish newly removed Inbox messages from messages already outside Inbox that were labeled or confirmed.

## Commit state

After producing a complete mailbox result, record the run through the memory helper. A run may advance successful mailboxes while retaining failed mailboxes:

```bash
python3 ../../scripts/memory_store.py record-run \
  --root <memory-root> \
  --json '<run-record>'
```

The run record must set `pipeline` to `daily` and identify the captured cutoff and status for every mailbox. Never submit `complete` for a mailbox whose reporting, unsubscribe, or write verification is incomplete.

Append compact decision evidence and message IDs when useful for future corrections, but never store message bodies.

## Learning boundary

Do not reinterpret casual silence as a preference and do not update shared policy. When the user corrects the digest or requests an ongoing behavior, use `$gmail-attention-feedback` to record the correction, update persona memory when authorized, and create a de-identified shared-policy candidate when appropriate.
