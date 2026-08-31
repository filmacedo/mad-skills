---
name: ship
description: Take an approved software change from its current state to the requested delivery boundary, usually a ready pull request or an explicitly authorized merge. Use explicitly when the user asks to finish, ship, babysit, or prepare a change for handoff.
---

# Ship

Own the delivery loop until the requested stopping point is genuinely reached. Keep scope fixed and make readiness visible.

## Establish the destination

Determine the intended behavior, repository rules, base branch, current branch state, and the user's requested boundary: ready pull request, passing review, merge, release, or another explicit handoff. Do not infer permission to merge, deploy, delete resources, or contact people from a general request to finish the implementation.

Inspect the complete diff and existing evidence. Resolve unrelated working-tree changes without overwriting them, and preserve the user's branch and commit conventions.

## Make the change ready

Complete only the approved scope. Run the closest checks that prove the changed behavior and important failure modes. Review the final diff for accidental files, debugging residue, security or compatibility risk, and missing proof.

For material or high-risk work, obtain an independent review from a fresh context when available. Give the reviewer the contract, full diff, project rules, and verification results. Triage findings, apply only confirmed fixes that are in scope, and rerun affected checks.

## Present and babysit the pull request

When authorized, create coherent commits, push the branch, and open or update the pull request with the problem, solution, verification, risks, and any follow-up work. Never claim checks or review passed without reading current evidence.

If the user asks to babysit, monitor the actual CI and review state, diagnose failures, fix in-scope causes, push updates, and continue until the requested gate is satisfied or a genuine external blocker requires the user.

Merge or release only when explicitly requested and repository policy permits it. Finish with the delivered boundary, pull request or revision, checks and review completed, residual risks, and next action. After a successful merge, suggest `$cleanup-workspaces`; do not run destructive cleanup implicitly.
