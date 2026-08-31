---
name: simplify-code
description: Reduce accidental complexity in working code without changing its behavior. Use explicitly before merging when the implementation is correct but harder to understand or maintain than necessary; do not use for feature work or broad redesign.
---

# Simplify Code

Make a correct change easier to understand before it is merged. Preserve behavior and keep the simplification proportional to the work under review.

## Find real complexity

Read the intended behavior, current verification, complete diff, and the nearby code needed to understand it. Look for duplication, needless indirection, speculative abstractions, dead branches, confusing names, excessive state, or wrappers that obscure rather than clarify.

Do not equate fewer lines with simpler code. Prefer the representation that makes invariants, data flow, and failure behavior easiest to see. Respect active project conventions and avoid rewriting unrelated areas merely for consistency.

## Simplify safely

Change one coherent source of complexity at a time. Preserve public behavior, compatibility, error semantics, observability, and intentional performance characteristics. Remove an abstraction only after checking its callers and extension points.

Avoid mixing simplification with new behavior. If a cleanup reveals a product or architectural decision, stop and surface it rather than choosing silently.

## Prove preservation

Run the closest existing checks before and after when practical. Add a characterization test only when behavior is important and otherwise unprotected; do not create brittle tests for internal structure.

Report what became simpler, what evidence shows behavior was preserved, and any complexity deliberately retained. If the proposed rewrite would not materially improve comprehension or maintenance, leave the code alone.
