# Persona memory and learning policy

Keep shared plugin policy, user persona, and operational run state separate.

## Storage layers

### Shared policy

Versioned files under the installed plugin's `policy/` directory. Read-only during user workflows. Changes require review, regression coverage, and a plugin release.

### Persona

User-owned `persona.json`. Contains explicit preferences, corrections, standing permissions, mailbox-specific behavior, presentation choices, and compact provenance. Never write it into the installed plugin.

### Run state

User-owned `state.json`. Contains independent pipelines such as `daily`, `weekly_content`, and `weekly_events`. Each pipeline owns its own per-mailbox successful cutoffs, bounded deduplication data, pending reconciliation, and recent run summaries. It is operational state, not preference memory.

Never reuse or advance one pipeline's checkpoint for another pipeline. A successful daily cleanup does not imply that either weekly digest was delivered.

### Feedback and policy candidates

- `feedback.jsonl` is an append-only audit trail of user corrections and their interpretation.
- `policy-candidates.jsonl` contains de-identified proposals for improving shared policy. Candidates are never active rules.

## Preference kinds

| Kind | Meaning | May become active automatically? |
| --- | --- | --- |
| Explicit persistent | The user clearly says always, never, by default, or describes an ongoing status | Yes, within the stated scope |
| Exact-message correction | Applies to named messages only | Yes, to those messages |
| Standing permission | Authorizes a side effect for a precise mailbox/matcher/action | Only after explicit approval |
| Inferred preference | Suggested from behavior or ambiguous wording | No; propose it |
| Resolved item | Prevents one handled message from resurfacing | Yes, for that exact item |

## Preference shape

Every active preference needs:

- stable `id`;
- `scope`, including mailbox when relevant;
- optional matcher;
- semantic classification or attention override when applicable;
- action and digest visibility;
- source and compact reason;
- confidence;
- creation and update timestamps;
- optional expiry and example message IDs.

More-specific preferences beat broader ones. When two equally specific active preferences conflict, do not guess: record the conflict and ask.

## Feedback loop

For each correction:

1. Preserve the user's wording in the private feedback log.
2. Interpret it as one of the preference kinds above.
3. Show the scope before applying a destructive or materially broad rule.
4. Upsert an active persona preference only when authority is clear.
5. Reconcile named messages only when requested and within approved permissions.
6. Create a de-identified shared-policy candidate when the lesson appears sender-independent.
7. Never edit shared policy or installed skill files from the digest or feedback workflow.

Do not call this model fine-tuning. It is explicit, auditable policy learning. Model fine-tuning should be considered only after a separate privacy-reviewed dataset and evaluation process exists.
