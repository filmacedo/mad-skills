# Executive digest contract

The digest reduces cognitive load. It is not a database export, action log, or dense email list.

## Required order

1. `## TL;DR`
2. `## What you need to do`
   - `### Now`
   - `### Later`
3. `## FYI — no action needed`
4. `## What I cleaned up`

Open with exactly one of:

- `**Action required now: Yes.**`
- `**Action required now: No.**`

Show only genuine actions under Now and Later. For each action include why it matters, whether an email reply is required, the deadline or timing, and one concrete next step. Rank by urgency and consequence; keep the top one to three critical items prominent.

Use FYI only for useful awareness that requires no decision. Do not repeat routine cleanup there.

## Cleanup disclosure

Every newly processed routine message must appear exactly once with:

- account tag when more than one mailbox is in scope;
- sender and useful one-sentence summary;
- label or other action applied;
- whether it was newly removed from Inbox or already outside Inbox;
- an account-routed Gmail/source link when available.

Use conversational sentences. Avoid tables, metadata chains, repeated bold sender names, or timestamps that dominate the message. Provide category counts and one totals line distinguishing newly archived mail from mail merely labeled or confirmed.

## Links and formatting

For Gmail, prefer an account-routed link:

```text
https://mail.google.com/mail/u/?authuser=<URL-encoded-mailbox>#all/<message-id>
```

Never use `/u/0` when more than one account may be signed in.

Use real Markdown newline characters. Do not wrap the digest in CDATA, HTML, a code fence, literal escaped `\n`, or transport syntax that could appear in the rendered output.

## Empty and incomplete runs

- If all successful mailboxes have no qualifying mail and no action or FYI, use the environment's conditional-notification capability. If unavailable, output only: `No qualifying messages since the previous successful run.`
- Prominently identify each incomplete mailbox and state that its checkpoint was retained.
- Never present a partial result as a complete digest.
