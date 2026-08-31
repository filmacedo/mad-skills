---
name: tdd
description: Implement or change testable behavior through short red-green cycles. Use when the user requests test-first development or a project workflow calls for it; do not force it onto work without stable observable behavior.
---

# Test-Driven Development

Build one observable behavior at a time. Use the failing test to clarify the contract, then write only enough implementation to satisfy it.

## Check that TDD fits

Use TDD when the change has a stable behavior, an observable boundary, an independent expected result, and a reasonably fast feedback loop.

Do not invent a tautological test merely to satisfy the process. Documentation, generated code, mechanical configuration, visual-only changes, and exploratory spikes may need different proof. If exploration is necessary, keep it disposable, then begin the durable implementation from what was learned.

For an existing untested bug, first create a regression or characterization test that can demonstrate the failure. Do not automatically delete useful existing work; prove that the test is capable of detecting the defect.

## Choose the test seam

Test through the public boundary closest to the behavior a caller or user depends on. Prefer a stable integration seam over private methods and internal call choreography.

Identify the seam and the source of truth for the expected result before writing the test. Ask the user only when competing seams would materially change coverage, cost, or product behavior and the project does not already decide the tradeoff.

## Run short vertical cycles

For each behavior:

1. **Red:** write one focused test and run it. Confirm it fails because the behavior is absent or wrong, not because the test is broken.
2. **Green:** implement the smallest coherent change that makes the test pass. Do not anticipate unrelated behavior.
3. **Verify:** rerun the focused test and the affected suite. Read the output rather than inferring success.
4. **Refactor:** improve structure while green when it reduces real complexity; add no new behavior.

Then choose the next behavior from what the completed slice taught you. Avoid writing a horizontal batch of imagined tests before any implementation.

## Keep tests worth maintaining

- Name the capability or failure mode the test protects.
- Exercise real code through public interfaces so internal refactors do not break the test.
- Derive expected values independently from a specification, worked example, or hand-checked literal—not the implementation's own logic.
- Mock only a slow, external, or nondeterministic boundary when necessary. Understand and preserve any side effects or data shape the test depends on.
- Cover consequential errors and boundaries, not every function or line by default.

Finish with fresh evidence: the new test was observed failing for the intended reason, now passes, and the relevant surrounding suite remains green. Report any verification that could not be run.
