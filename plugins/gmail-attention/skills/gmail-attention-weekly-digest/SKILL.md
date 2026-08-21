---
name: gmail-attention-weekly-digest
description: Produce a read-only weekly Gmail digest in content or events mode using private persona preferences and an independent per-mode checkpoint. Use for newsletter/article reading briefs or event-discovery briefs; do not use for daily inbox cleanup or the initial Gmail audit.
---

# Gmail Attention Weekly Digest

Create one useful weekly briefing from newly received content or event-discovery mail. This skill has exactly two modes:

- `content` for newsletters, articles, interviews, analysis, and curated reading;
- `events` for public or professional event invitations, promotions, and local-event roundups.

A scheduled task should explicitly invoke `$gmail-attention-weekly-digest`, specify one mode, and provide the memory location and delivery context. Use separate scheduled tasks for the two modes.

## Load policy and memory

Before accessing Gmail, read:

- [general policy](../../policy/general-policy.md);
- [classification policy](../../policy/classification.md);
- [security policy](../../policy/security.md);
- [persona memory policy](../../policy/memory.md);
- [weekly digest contract](../../policy/weekly-digest.md).

Resolve and validate the durable memory root. If mode is `content`, use pipeline `weekly_content`; if mode is `events`, use pipeline `weekly_events`. Reject any other mode. Never read or advance the `daily` pipeline or the other weekly mode's state.

## Verify account scope

For every configured mailbox:

1. Use only its configured connection or selector.
2. Fetch the authenticated Gmail profile and require an exact normalized address match.
3. Keep searches, message IDs, links, results, and state isolated by mailbox.

Fail only the affected mailbox when possible. Never substitute a different account.

## Capture the weekly window

- Capture one current cutoff before searching.
- Use the selected pipeline's exact per-mailbox successful cutoff as the exclusive lower bound.
- On a genuine first run, use cutoff minus seven days unless persona configuration specifies another weekly lookback.
- Include exact received timestamps `> lower_bound` and `<= cutoff`.
- Search All Mail, excluding Sent, Drafts, Spam, and Trash, and complete every page.
- Deduplicate by `(mailbox, Gmail message ID, exact received timestamp)`.

Use the mailbox's `label_map` entry for `content` or `events` as evidence and as an efficient primary query. Also perform enough All Mail coverage to recover qualifying messages that the daily cleanup or a Gmail rule failed to label. Do not assume a daily run completed.

## Select and summarize

Classify messages by purpose using shared policy plus active persona preferences. Include only the requested semantic purpose. Read enough content to produce a useful summary; do not store message bodies.

In content mode, distinguish editorial reading from a company's own product marketing. In events mode, distinguish discovery from tickets, confirmations, cancellations, deadlines, venue changes, and other operational mail.

If a qualifying message lacks the configured label, include it in the digest and mention the labeling gap in one compact maintenance note. Do not repair labels in this read-only workflow; route corrections through `$gmail-attention-feedback` or the daily cleanup.

## Produce the digest

Follow [the weekly digest contract](../../policy/weekly-digest.md) for the selected mode. Apply persona preferences for account tags, timezone, source/topic relevance, event geography, event horizon, verbosity, and ranking.

Use account-routed Gmail links. Keep the digest conversational and easy to skim. Prioritization may highlight a few items, but every qualifying message must still appear once.

## Commit state

After the digest is completely reported for a mailbox, record the run through the memory helper:

```bash
python3 ../../scripts/memory_store.py record-run \
  --root <memory-root> \
  --json '<run-record>'
```

Set `pipeline` to `weekly_content` or `weekly_events`, matching the selected mode. Advance only fully searched, read, classified, and reported mailboxes. Retain the checkpoint for any mailbox with incomplete access, search, pagination, reads, or output.

## Mutation boundary

This skill is read-only. Never label, archive, unsubscribe, report spam, block, create a filter, or change Gmail state. When the user corrects a source, topic, event preference, classification, or presentation choice, use `$gmail-attention-feedback` to persist the scoped learning.
