---
name: ship-feature
description: Use when Filipe says "ship this", "ship it", "build this", "/ship-feature", or hands over a PRD, spec, bug, or chore to implement end-to-end in noticedso/noticed. Covers taking any scoped piece of work from description to a reviewable pull request.
---

# ship-feature

## Overview

Come back to Filipe **exactly once per PR** — with a PR he can merge without a single comment. The bar: 95% of PRs merge with zero feedback. Everything in this loop exists to make that true before he ever sees the work. (Multi-PR flows — `frontend-prototype` iterations, a score-change calibration cutover — are one hand-over per PR, not zero contact across the whole feature.)

Supersedes the repo's `build-feature` skill (Notion-status-driven, outdated — Filipe doesn't use it). If both match, use this one. `new-feature` (PRD intake into Notion) still runs before this skill; ship-feature starts once a PRD/spec/description exists.

## The loop

1. **Isolate.** New git worktree + feature branch off `main` (`feature/<kebab>` or `fix/<kebab>`). Never build on `main`, never in the shared checkout. Run `npm run setup-worktree` first (fresh worktrees have no `node_modules`/`.env` — see CLAUDE.md).
2. **Lock the contract.** Read the PRD/spec; its Done-when items are the acceptance checklist. If anything is genuinely ambiguous on a **product/UX** call (including whether an action is verifiable enough to gate a completion state on), ask Filipe ONCE, up front, all questions batched. Engineering calls you make yourself. Write the plan file per CLAUDE.md's Plan Mode Rule (`plans/<date>-<kebab>.plan.md`) and keep its todo statuses current. After this point, no mid-build check-ins — the next time Filipe hears from you is step 6.
3. **Build with TDD.** REQUIRED SUB-SKILL: `test-driven-development`. Iterate until EVERY goal is met and ALL tests pass — not "most", not "the ones that run locally by default". CLAUDE.md rails are hard constraints (bench tags, PageContainer, type tokens, Phosphor icons, ClickHouse rules). For a new user-facing page from a PRD, consider the `frontend-prototype` skill's iteration split. For any UI, apply `design-taste`. For anything touching the relationship score, `score-change` is mandatory.
4. **Independent review.** Spawn FRESH subagents that did not write the code: one code review, one security review (security is non-optional when the diff touches auth, API routes, uploads, or user input — run it anyway when unsure). Fix every Critical/Important finding, re-run the tests. Don't skip because "the diff is small" — PR #627 came from review catching a pagination bug in a 5-file diff.
5. **CI green.** Push, open the PR as a **draft** (feature-branch CI runs via the PR trigger). Wait for ALL jobs green — lint-types, unit-tests, postgres-tests, build, clickhouse-integration. Fix and re-push until green. A locally-skipped DB test (ECONNREFUSED) is not a passing test.
6. **Hand over once.** Mark the PR ready, then report: PR link + one-line status. This is the first time you come back since step 2.

## The PR body (Filipe's shape — from merged PRs #640, #628, #631, #586)

- `## What` / `## Why` / `## How` (or `What & why`) H2 sections; lead with the user-visible change.
- PRD anchor: NT-xx id in the title or first line, Notion PRD link when one exists.
- `## Verification` with **numeric tallies**: "20/20 green", "tsc 0 errors", "lint 0 warnings", "bench-drift 0 errors". Never a bare "tests pass".
- Visual changes: Before/After description or table; embed a screenshot when one can be captured; when auth-gating makes that infeasible, say so honestly and name the substitute (render tests, Vercel preview).
- `## Not in scope` for deliberate exclusions; name what was deliberately left untouched.
- Fix PRs: name the root cause mechanistically (the causal chain, not the symptom) — see #641, #586, #590.
- Honest gaps: leave boxes **unchecked** for what genuinely couldn't be verified, with the reason ("needs Blob creds", "manual click-through once deployed").

## Hold-for-review flags

Green CI does NOT mean mergeable for: score-model changes, new user-facing routes or major redesigns, DB migrations, or anything unvalidatable locally (real-data aggregates). Write "**do not auto-merge** — needs real-data validation / your review" in the PR body, like #631 and #643. Borderline (a small utility page)? Flag it in the body and let Filipe decide. Everything else: done when green.

## Common mistakes

| Mistake | Fix |
|---|---|
| Building on `main` or a plain branch in the shared checkout | Worktree + feature branch, always |
| Coming back mid-build with questions the code can answer | Batch product questions at step 2; decide engineering yourself |
| "Tests pass" with DB suites skipped locally | Skipped ≠ passing; CI's PG/CH jobs are the proof |
| Skipping review subagents on a small diff | #627: review caught a pagination dup/skip bug in a tiny diff |
| Handing over before CI is green | Draft PR until every job passes |
| Silently dropping a Done-when item | Every item ships, or the PR says why it didn't |
