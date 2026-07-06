---
name: score-change
description: Use when changing anything about the relationship strength score in noticedso/noticed — strength.ts, channel/type weights, half-lives, saturation, presence floors, tier cutoffs, score inputs or output shape, SCORE_DERIVATION_VERSION, FORMULA_FINGERPRINTS — or when investigating why scores or tiers (Frequent/Regular/Occasional/Rare) shifted.
---

# score-change

## Overview

CLAUDE.md's hard rule (version bump + fingerprint entry, CI-enforced by the golden test and drift check) is the **floor**. This skill is the workflow Filipe requires on top: a score change without real-data evidence and a calibration gate is not shippable, even with green CI. Score changes are **always held for Filipe's review — never auto-merge.**

## Version decision table

| Change | Action | Precedent |
|---|---|---|
| Math or constants change | New version + genuinely new fingerprint | #609 (v10 recency decay), #626 (v11 LinkedIn presence-only), #643 (v13 type-based) |
| Output shape changes, numbers identical | Bump anyway; ledger comment states "numbers UNCHANGED — fingerprint moves because \<field\> left the hashed output" | #629 (v12, `active` flag removed) |
| Input-layer only (mapping/resolver), formula untouched | Bump; fingerprint may be identical to the previous version — say so, citing the v7/v8 precedent | #643 (v14) |
| No formula change (sorts, UI, read paths) | No bump — and the PR explicitly states "No score-formula change (still vN)" | #627 |

Ledger entries are append-only; each carries a rationale comment. If the PRD's version number conflicts with live code, live code wins — correct it and note the correction (#609 caught "bump to 7" when code was at v8).

## Evidence requirements (in the PR body)

- **Arithmetic to the digit** for the affected case: `0.3·(0.4+0.6·1) = 0.30 → score 15` vs `0.3·0.4 = 0.12 → score 6` (#626).
- **Read-only prod before/after**: a table of real named people (interaction counts, last interaction, tier before → after) plus the population-level tier shift, e.g. `Frequent 49→23, Regular 20→35…` (#609). Use the read-only prod connection (`POSTGRES_PROD_URL`, as in #640's spot-check); if no prod access is available in the session, say so and leave that evidence box **unchecked** — don't fabricate or substitute local data silently. The table must *read correctly* — the still-active stay put, the historically-active-but-quiet fall.
- **Tier pyramid check**: Rare biggest → Frequent smallest; a bulge (78% in Occasional) is a calibration bug (#626).
- **Extend `GOLDEN_INPUTS`** to exercise every new mechanism (weighted counts in v10; size weight, per-type half-lives, presence-only in v13), and keep every constant human-explained in `STRENGTH_PARAMETERS`.

## Calibration gate

- Constants ship as **sim-validated starting points**; the finals come from a human pass on `/relationships/eval` against a real network.
- **Hold the fleet recompute** for a single cutover after calibration — never recompute prod in the formula PR (#643: "held for the eval-calibrated constants"). The recompute is a separate follow-up task that Filipe triggers after his eval pass; the formula PR just states that.
- Stale caches self-heal (version-aware reads in `score_cache` + `person_facts` treat old versions as misses) — no manual flush, but verify both read paths compare against the new constant.

## Model philosophy — don't violate silently

- **Decay lives inside the definition of frequency** (`Σ 0.5^(ageDays/halfLife)`), never a `base × recency` multiplier (#609).
- **Presence is durable state, not a dated interaction**: bare LinkedIn / phone / X-follow gets `frequency 0`, an absolute Rare-capped floor combined by `max` — it never clears Rare, never dilutes or outranks real contact (#626, #643).
- **Provenance must not affect the score**: a manually logged "met" and a synced meeting of the same type score identically (#643).
- **One shared input builder** so list and detail score identically by construction (#643's `assemble-inputs.ts`).
- **SQL mirrors TS via query parameters** — pass the half-life as a param so the SQL constant can't drift from `decayWeight()` (#609).
- Sorts over equal scores need a **total order**: recency, then `created_at`, then unique `pers.id` — or pagination duplicates/skips rows (#627).

## Common mistakes

| Mistake | Fix |
|---|---|
| Green CI ⇒ merge | Score changes always wait for Filipe |
| Formula PR also recomputes prod | Hold recompute for the post-calibration cutover |
| "Numbers unchanged, so no bump" on a shape change | #629: the hashed output changed — bump with rationale |
| Skipping prod inspection because tests pass | Unit tests can't show tier redistribution on a real network |
| Fixing an odd tier by tweaking cutoffs | Check the pyramid + per-channel behavior first; the bug is usually a floor/weight (#626) |
