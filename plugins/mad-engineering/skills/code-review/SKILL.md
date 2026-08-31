---
name: code-review
description: Review a diff, branch, or pull request against its intended behavior and active project rules, then report evidence-backed findings. Use for direct review requests or as an independent gate in a delivery workflow; do not use to implement the change.
---

# Code Review

Decide whether a change is ready to hand off. Find consequential defects and proof gaps without turning review into a style audit.

## Establish the contract

Read the request, specification, accepted decisions, active project instructions, and verification evidence. Determine the correct base and inspect the complete diff, including uncommitted changes when relevant.

Review the work product rather than the author's reasoning. Follow changed behavior through its callers, data shapes, state transitions, and external boundaries; isolated hunks rarely show the full risk.

## Review proportionately

Apply the lenses the change earns:

- **Contract and correctness:** required behavior, edge cases, errors, retries, concurrency, and state transitions.
- **Safety and blast radius:** authorization, secrets, public inputs, data loss, compatibility, migrations, and downstream consumers.
- **Design and operations:** project conventions, maintainability, performance, observability, recovery, and deployment order.
- **Evidence:** tests and checks prove the changed behavior and its important failure modes.

One general review pass is the default. Add a specialized security, data, or platform review only when the affected surface warrants it. Do not manufacture findings to fill every lens.

## Report only actionable findings

For each finding include:

- severity and exact location;
- a reachable scenario that demonstrates the problem;
- user or system impact;
- the evidence supporting the conclusion;
- the smallest useful fix and any missing regression proof.

Prioritize correctness and risk over formatting preferences. Omit speculative concerns, pre-existing issues the change does not activate, and suggestions whose benefit is merely aesthetic. Verify apparent problems against nearby code or executable evidence before reporting them.

If no actionable findings remain, say so and name any residual verification gap. A clean review is not proof that unrun checks pass.

## Preserve reviewer independence

Review is report-only unless the user separately asks for fixes. Do not edit, commit, push, resolve threads, approve, or merge while acting only as reviewer.

For material changes, prefer a fresh reviewer context containing the contract, full diff, project rules, and verification results—not the implementation transcript. Do not recursively invoke this skill or spawn additional reviewers unless a concrete risk requires specialist review.

The calling delivery workflow owns triage, fixes, reverification, and the final ready/not-ready decision.
