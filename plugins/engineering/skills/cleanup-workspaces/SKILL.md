---
name: cleanup-workspaces
description: Reclaim disk and remove local development resources left by completed work. Use explicitly after merge or abandonment to audit and clean worktrees, reproducible web build artifacts, and stale iOS development resources; do not use for source-code simplification.
---

# Cleanup Workspaces

Reclaim local development space without losing active or unique work. Treat discovery and safety gates as the review for every deletion.

## Audit from authoritative state

Measure relevant disk use, then discover candidates from the tools that own them: Git for worktrees, project commands for build outputs, and platform tools for simulators or runtimes. Do not construct paths from memory or broad globs.

For each candidate establish its path or identifier, size when practical, age, merge or abandonment evidence, active process or task usage, uncommitted tracked changes, untracked files, and whether it can be reproduced. Classify it as protected, uncertain, or eligible; heuristics are advice, not permission.

## Protect unique work

Never remove the current workspace, an active task's resources, uncommitted tracked work, or anything whose recoverability is unclear. Name untracked files rather than assuming they are disposable. Preserve branch references unless deleting them is separately requested.

Before irreversible deletion, show the exact eligible targets, why each is safe, and what will be retained. Obtain confirmation when those targets were not already explicitly authorized. Pause on any uncertain, active, or unique state.

## Clean proportionately

Remove only the confirmed targets with the owning tool where possible, then prune its stale metadata.

- **All repositories:** clean merged or explicitly abandoned worktrees and reproducible ignored build artifacts.
- **Web projects:** prefer the project's clean command for framework outputs and tool caches; preserve dependencies or caches the user asked to keep.
- **iOS projects:** distinguish unavailable devices, test clones, obsolete runtimes, DerivedData, and device support. Remove only the categories needed to meet the cleanup goal, and preserve active simulators and required runtimes.

Do not use recursive deletion against a home directory, repository root, unresolved variable, or guessed wildcard. Stop if the safe target set cannot be resolved exactly.

## Verify the result

Re-list the owning tools and measure disk use again. Report space reclaimed, every resource removed, and every candidate held back with its reason. A successful cleanup leaves active work intact and its decisions auditable.
