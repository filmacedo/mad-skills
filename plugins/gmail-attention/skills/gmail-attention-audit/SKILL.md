---
name: gmail-attention-audit
description: Audit and reset a connected Gmail account's interruption rules. Use when a user wants to understand all mail in Gmail or All Mail, protect their Inbox for people and timely action, classify recurring senders or message patterns, review newsletter/product/event/notification traffic, create Gmail labels and filters, unsubscribe or block mail, clean up backlog, or deliver ongoing email digests.
---

# Gmail Attention Audit

Run a complete loop: audit Gmail, explain what is happening, propose a future mail plan, obtain explicit approval, implement approved Gmail changes, and deliver the digests the plan promises.

The principle is simple: **the Inbox is for people and timely action; regular non-important mail is delivered deliberately.**

## Modes and authority

Start in **Audit** mode. Reading Gmail is allowed. Do not archive, label, unsubscribe, block, create filters, or send a digest until the user explicitly approves a presented change set.

Use these modes in order unless the user asks to resume a later one:

1. **Audit** — inventory and classify mail; make no changes.
2. **Review** — resolve only meaningful uncertainty and user choices.
3. **Plan** — show exact future rules and past-backlog actions.
4. **Implement** — apply only the approved plan.
5. **Digest** — deliver and verify the promised daily/weekly digest.

Never blur a past finding with a future rule. Say whether a statement describes historical mail, a proposed rule, or a completed Gmail action.

## Start the audit

1. Confirm the connected Gmail account and scope. Default to **All Mail** for the last 12 months, excluding Sent, Drafts, Spam, and Trash. Ask one concise question only when account, scope, or timeframe is not clear.
2. Explain that Sent mail is used only as reply evidence. Do not mistake an archived Inbox for a lack of mail; All Mail is the source of truth.
3. Retrieve all matching messages with pagination. Do not claim a complete audit until the result count is reconciled. Start from message metadata; read bodies only for ambiguous, high-impact candidates.
4. Create a canonical message inventory. Every message must receive one classification and may match zero or one high-confidence message-pattern rule.
5. Preserve dates. Report both the audit-period total and the recent eight-week pattern. A yearly average must not hide a recent change in cadence.

Read [the classification reference](references/classification.md) before assigning categories or proposing rules.

## Explain the audit before asking for decisions

Teach a user with no prior context:

- Say what mail was analyzed and how many messages were found.
- Explain the categories in plain language.
- State what was clearly classified automatically and what still needs human judgment.
- Show the evidence behind every suggested rule: representative subjects, sender or pattern, historical count, first/last seen, and recent cadence.
- Separate **past analysis** from **future plan** in both headings and language.

Do not call a hidden label, an archive, or a mailbox search a user-facing digest. A digest is a delivery the user will actually receive.

## Classification and review

Classify message patterns before sender identity. A person can send a normal conversation and an `Accepted:` calendar response; only the calendar response is routine.

Then group messages into a **sender-purpose group** only when the same sender and purpose recur. Do not invent a generic “stream” concept for the user. Explain it as: “messages from this sender that follow the same pattern.”

Apply the reference taxonomy. In particular:

- Never treat `List-Unsubscribe` alone as proof that mail is editorial Content. It is evidence of a mailing list, not its purpose.
- Keep confirmed-unsubscribed sources in a small audit record and exclude them from another unsubscribe review.
- Do not make a sender-wide rule when one sender has several purposes. Prefer a message-pattern rule, or hold it for review.
- Treat Gmail categories and importance as signals, never as ground truth.

Review only:

- uncertain classifications;
- high-volume or recently accelerating groups;
- groups with mixed purposes;
- groups where the user must choose Inbox, Digest, Unsub, or Block.

Do not make the user review every individual message. Start with high-confidence automatic patterns and high-impact ambiguous groups. User decisions correct the model; preserve their choices in the audit output.

## Decide whether a digest is warranted

Assess each proposed digest separately: Events, Content, Updates, and the combined daily Notifications + Transactions delivery are distinct products.

Recommend a digest only when recent behavior shows it will consolidate multiple regular interruptions. Two or more digest-eligible messages per active week is strong evidence, not a hard gate. Consider recent acceleration, time sensitivity, and sender-level cadence. Explain the evidence and leave the final decision to the user.

If a category has only one occasional message, keep it in Inbox or leave it for review; do not create a digest that creates more email than it saves.

## Present the plan

After review, present one explicit change set. Group it by outcome:

```text
Future Gmail rules
- Calendar acceptances → archive
- Luma event mail → Weekly Events digest

Existing backlog
- Apply Events label and archive 34 matching messages

Removal queue
- Unsubscribe: 4 senders
- Block: 1 cold-outreach sender

Digest delivery
- Weekly Events: proposed delivery method and first send time
```

For every line, specify:

- exact matcher (sender, domain, or message pattern);
- matching historical count and recent cadence;
- Gmail action for future mail;
- backlog action, if any;
- digest and delivery cadence, if applicable.

Ask for one explicit confirmation to apply the exact plan. A phrase such as “looks good” is not approval if the plan has not been displayed in the current context. Preserve edits and re-present the updated plan before acting.

## Implement and verify

After explicit approval:

1. Create only the labels, filters, unsubscribe/block actions, and backlog changes in the approved change set.
2. Use exact Gmail searches and inspect the matching set before bulk changes. Keep an action log with counts, matchers, timestamps, and outcomes.
3. Apply message-pattern rules independently from sender-wide rules. For example, archive `Accepted:` mail without changing ordinary mail from that person.
4. For unsubscribe, use the standard mechanism when available. Clearly distinguish completed, requested, manual confirmation required, filtered, and failed. Never call filtering a completed unsubscribe.
5. Verify each Gmail write by checking the affected messages, labels, filters, or unsubscribe outcome. Report any item that could not be completed.

## Deliver digests

The same skill owns delivery. Choose and implement the most reliable method available in the current environment; do not make the user design the mechanism.

A digest must contain the messages the user is meant to see, with sender, subject, date, and an openable Gmail or source link when available. It may summarize, but must not silently omit matching mail.

If recurring scheduling is available, set it up only as part of the approved plan and verify the delivery configuration. If it is not available, support an explicit “send my digest now” run and say plainly that recurring delivery is not configured. Never describe labels plus archived messages as a digest.

For the combined daily Notifications + Transactions digest, send one delivery with clear sections. Keep weekly Events, Content, and Updates digests separate unless the user explicitly merges them.

## Completion report

Return a concise before/after report containing:

- audit scope and exact message count;
- classifications and recent cadence;
- rules created;
- backlog messages changed;
- unsubscribe/block outcomes;
- digest delivery status and next scheduled run, if any;
- unresolved groups and manual follow-ups.

Store the audit and decision record in Markdown and JSON when the environment supports files. Never store message bodies unless the user asks.
