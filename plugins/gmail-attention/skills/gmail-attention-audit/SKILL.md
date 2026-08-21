---
name: gmail-attention-audit
description: Run a one-time Gmail attention audit, propose an evidence-backed cleanup plan, and implement only approved labels, filters, backlog changes, unsubscribes, or blocks. Use for initial inbox cleanup or a deliberate re-audit; do not use for recurring daily processing.
---

# Gmail Attention Audit

Audit Gmail once, explain what is interrupting the user, agree on a future mail plan, and implement the approved Gmail-native changes. The outcome is a quieter Inbox plus a portable persona policy that a separate recurring workflow may consume.

The principle is: **the Inbox is for people and timely action; predictable lower-value mail is delivered deliberately.**

Before classifying mail, read the plugin's shared [general policy](../../policy/general-policy.md) and [classification policy](../../policy/classification.md). Read [the audit reference](references/classification.md) before grouping history or proposing Gmail rules. Read [security policy](../../policy/security.md) before recommending unsubscribe, spam, block, or any action involving email links.

## Boundary

This skill owns a one-time audit and implementation plan. It does not:

- process incremental daily windows;
- maintain successful-run checkpoints;
- generate a recurring executive brief;
- silently install a scheduled task;
- rewrite shared plugin policy from one user's preferences.

If the user wants recurring processing, finish the audit first and hand the approved persona to `$gmail-attention-daily` or `$gmail-attention-weekly-digest`. Create or update a schedule only when the user explicitly asks.

## Modes and authority

Use these modes in order unless the user explicitly resumes a later one:

1. **Audit** — read, inventory, and classify; make no changes.
2. **Review** — resolve only meaningful uncertainty and user choices.
3. **Plan** — present exact future rules and backlog actions.
4. **Implement** — apply only the approved plan.
5. **Handoff** — report results and persist the approved persona policy.

Reading is allowed in Audit mode. Do not archive, label, unsubscribe, block, create filters, or send mail until the exact change set has been presented and explicitly approved. Never blur historical findings, proposed rules, and completed actions.

## Establish account scope

1. Resolve each requested Gmail connection to its authenticated profile email before searching.
2. Fail closed for a connection whose identity cannot be confirmed. Never inspect a different mailbox as a substitute.
3. Keep message IDs, thread IDs, searches, labels, writes, links, and counts associated with their originating mailbox.
4. Default to All Mail for the previous 12 months, excluding Sent, Drafts, Spam, and Trash. Use Sent only as reply evidence.
5. Complete pagination and reconcile the result count before calling the audit complete.

For multiple accounts, audit each independently and present both per-mailbox and combined findings. A failure in one mailbox must not contaminate another mailbox's results.

## Build the inventory

- Start from metadata and headers. Read bodies or surrounding threads only for ambiguous, mixed-purpose, security-sensitive, or high-impact candidates.
- Give every message one semantic purpose and one attention level from the shared classification policy.
- Preserve exact received timestamps and deduplicate by `(mailbox, Gmail message ID, exact received timestamp)`.
- Group only recurring messages with the same sender and purpose. Do not assume a sender has one purpose.
- Report both the full audit-period total and the recent eight-week pattern so an annual average cannot hide a recent change.

## Explain findings

Before requesting decisions:

- state the mailboxes, period, exclusions, and exact message count;
- explain the categories in plain language;
- separate confident classifications from groups needing judgment;
- show representative subjects, historical count, first and last seen, recent cadence, reply evidence, and unsubscribe availability for every proposed rule;
- distinguish native Gmail signals from conclusions; Gmail categories and importance are evidence, not ground truth.

Do not call labels or archived search results a digest. A digest is a delivery the user actually receives.

## Present one explicit plan

Group the plan by outcome:

```text
Future Gmail rules
- Exact matcher → label, archive/keep, and rationale

Existing backlog
- Exact matcher → count and proposed change

Removal queue
- Unsubscribe, spam, or block candidates with evidence

Persona preferences
- The durable user-specific decisions this audit will save

Optional recurring handoff
- Whether a daily or weekly skill is warranted and why
```

For every line, include the exact matcher, historical count, recent cadence, future action, backlog action, and any delivery cadence. Prefer deterministic message-pattern rules. Propose a sender-wide or organization-wide rule only when history shows a stable purpose or the user explicitly chooses that broader scope.

Re-present the final edited plan and ask for one explicit confirmation before implementing it.

## Implement and verify

After approval:

1. Resolve each exact Gmail search again immediately before mutation.
2. Create only approved labels and filters.
3. Archive only by removing `INBOX`; preserve read state, starred state, importance, and unrelated labels.
4. Treat writes as idempotent. If a result is uncertain, inspect current state before retrying.
5. For unsubscribe, distinguish completed, requested, confirmation pending, manual action required, filtered, and failed. Never describe filtering as an unsubscribe.
6. Require explicit authorization for spam reporting and blocking, scoped to the named sender or rule.
7. Verify every label, filter, archive, unsubscribe, spam, and block outcome.

## Persist the persona handoff

Read [memory policy](../../policy/memory.md). When local project storage is available, initialize or validate the user-owned memory directory with:

```bash
python3 ../../scripts/memory_store.py init --root <memory-root>
python3 ../../scripts/memory_store.py validate --root <memory-root>
```

Default `<memory-root>` to an explicit user-provided location or the current project's `.gmail-attention/` directory. Never write persona data into the installed plugin. If durable storage is unavailable, return the proposed persona as a JSON artifact and say plainly that it has not been persisted.

Configure each verified account with `upsert-mailbox`, including the approved semantic `label_map`; save presentation choices with `set-output-preferences`; and save each approved behavior with `upsert-preference`. All three commands accept `--root` and `--json` using either inline JSON or `@path/to/file.json`.

Store only approved preferences and compact evidence. Do not store message bodies. Record inferred preferences as proposals, not active rules. Run `validate` again after the handoff is written.

## Completion report

Return a concise before/after report containing:

- scope and exact counts;
- classifications and recent cadence;
- Gmail rules and backlog changes completed;
- unsubscribe, spam, and block outcomes;
- persona preferences persisted;
- unresolved groups or manual follow-ups;
- whether a recurring handoff was configured.

If any operation could not be verified, say so and do not claim the audit is complete.
