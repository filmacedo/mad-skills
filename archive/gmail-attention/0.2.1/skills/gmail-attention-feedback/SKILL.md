---
name: gmail-attention-feedback
description: Learn from a user's correction or preference about a Gmail audit or digest, update private persona memory when authorized, reconcile named messages when requested, and propose de-identified shared-policy improvements without editing the shared skill automatically.
---

# Gmail Attention Feedback

Turn feedback about Gmail classification, cleanup, security, formatting, or sender handling into an explicit and auditable persona change. Preserve the boundary between personal preference and shared product knowledge.

Before interpreting feedback, read [general policy](../../policy/general-policy.md), [memory policy](../../policy/memory.md), and [security policy](../../policy/security.md).

## Resolve context

Identify:

- the digest or audit item being corrected;
- mailbox and message IDs when available;
- the prior classification, attention level, action, and rule provenance;
- the durable memory root;
- whether the user is asking to change past mail, future behavior, or both.

Do not search a different mailbox to compensate for missing context. If the named email cannot be resolved safely, update only the clearly stated future preference and report that the past message was not reconciled.

## Interpret the feedback

Classify it as exactly one primary kind:

1. **Exact-message correction** — only the named email was wrong.
2. **Explicit persistent preference** — the user clearly states an ongoing behavior such as always, never, by default, no longer active, or only in this mailbox.
3. **Standing permission** — authorization for a side effect such as unsubscribe, spam, or block within a precise scope.
4. **Inferred preference** — the wording suggests a pattern but does not authorize one confidently.
5. **Resolved item** — an exact action or security question has already been handled and should not resurface.
6. **Shared-policy candidate** — the correction appears sender-independent and generally useful.

A single feedback item may create a persona record and a separate shared-policy candidate, but only one primary feedback kind.

## Decide whether to ask

Apply an explicit, narrow, non-destructive preference without asking again when the scope is clear. Ask before:

- a materially broader sender/domain/organization rule than the user stated;
- spam reporting, blocking, or unsubscribe without an existing matching standing permission;
- changing Gmail filters or rules;
- treating ambiguous wording as a persistent policy;
- resolving a conflict between equally specific active preferences.

When asking, show the proposed matcher, mailbox scope, classification or attention override, Gmail action, and digest visibility.

## Persist private learning

Validate or initialize the memory root, then append the feedback event:

```bash
python3 ../../scripts/memory_store.py append-feedback \
  --root <memory-root> \
  --json '<feedback-record>'
```

For an authorized persistent preference or standing permission, upsert it:

```bash
python3 ../../scripts/memory_store.py upsert-preference \
  --root <memory-root> \
  --json '<preference-record>'
```

Use stable IDs derived from scope and behavior so later feedback updates the same preference rather than creating duplicates. Preserve `created_at`; update provenance, reason, confidence, and `updated_at`.

Store compact evidence and message IDs only. Never store message bodies, credentials, raw MIME, or sensitive link parameters.

## Reconcile Gmail when requested

If the user asks to correct the named message and the action is authorized:

1. verify the originating mailbox profile;
2. inspect current message state;
3. apply the smallest safe change;
4. verify it;
5. record the outcome in feedback memory.

Never infer authorization to report spam, block, unsubscribe, delete, or create a filter from a mere classification correction.

## Propose shared learning

When a correction is plausibly universal, append a de-identified candidate:

```bash
python3 ../../scripts/memory_store.py append-policy-candidate \
  --root <memory-root> \
  --json '<candidate-record>'
```

Describe the general behavior, rationale, counterexamples, and regression case without personal senders or message text. Candidate status begins as `pending`. Do not edit plugin policy or skill files during this workflow.

## Report back

State concisely:

- what was corrected now;
- what future preference was saved and its scope;
- whether any Gmail message was changed;
- whether a shared-policy candidate was recorded;
- anything still awaiting confirmation.
