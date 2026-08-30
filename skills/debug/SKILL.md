---
name: debug
description: Find and prove the cause of a software failure before changing behavior. Use for bugs, failing tests, regressions, or unexpected runtime behavior when the cause is unclear; do not use when the requested fix and causal chain are already established.
---

# Debug

Turn an observed symptom into an evidence-backed causal explanation. Fix it only when the user has asked for implementation as well as diagnosis.

## Establish the symptom

State what was observed, what should have happened, where it occurs, and what evidence would distinguish success from failure. Reproduce it on the closest practical real surface before proposing a cause.

Preserve useful evidence: errors, inputs, state, timing, environment, recent changes, and the first point where actual behavior diverges from expected behavior. If reproduction is blocked, identify the missing access or observability instead of guessing.

## Test explanations

Trace data and control flow backward from the symptom. Form a small set of competing, falsifiable hypotheses and rank them by existing evidence.

Run the cheapest discriminating check first. Change one variable at a time and record what each result rules in or out. Prefer inspection, focused probes, logs, or tests over speculative production edits.

Do not stack fixes until something works. If evidence contradicts the leading theory or repeated attempts fail, revisit the assumptions, reproduction, boundary, and architecture before continuing.

## Prove the causal chain

A correlation or suspicious line is not yet a cause. Connect:

1. the triggering condition;
2. the mechanism that produces the wrong state or output;
3. the observed symptom;
4. evidence that changing or isolating the condition changes the outcome.

When several defects contribute, separate the root cause from amplifiers and downstream damage.

## Fix and verify when authorized

For diagnosis-only requests, report the cause, evidence, confidence, and unresolved gaps without editing code.

When a fix is in scope, prefer the smallest change that removes the proven cause. Add a regression test when it provides durable proof, then verify both the original symptom and the relevant surrounding behavior. Do not bundle unrelated cleanup.

Return the symptom, proven cause, decisive evidence, change made if any, verification performed, and remaining uncertainty.
