---
name: frontend-prototype
description: Use when Filipe says "frontend prototype", "prototype this", "mock it first", "iteration 1", or when a PRD describes a new page/surface whose design should be locked before real data is wired. Also use when asked for "iteration 2" of a previously prototyped page.
---

# frontend-prototype

## Overview

Filipe ships new surfaces in two iterations: **iteration 1 locks layout and design on a typed mock; iteration 2 swaps in real data behind unchanged component props.** The mock fixture IS the contract between them. Grounded in the `/network` audit chain: #628 (iter 1) → #630 (gate) → #631 (iter 2).

## Iteration 1 — the prototype

- Build the **complete page** (every section, both charts, all states) on a typed mock fixture (`*-mock.ts`) with realistic-looking names and numbers. The bar is **screenshot-worthy**: on brand, worth sharing (#628).
- The mock flows through the same pure shaping function (`*-aggregate.ts` / `assemble*.ts`) the real loader will feed later — "the exact contract iteration 2 fills" (#628). Build that core **test-first**.
- Components consume shaped data only; they never know whether it's mock or real.
- Reuse shell primitives (`PageContainer`, `PageHeader`, `Box`, `Text`, `Icon`) and brand tokens; add only genuinely-new pieces (#628).
- **Gate it from real users** — fabricated names/numbers must never be live (#630): add the page to `ADMIN_ONLY_LABELS` in `Sidebar.tsx` (locked + visible, not hidden) AND a route `layout.tsx` calling `requireBackofficeAdmin()`. Put a "drop this gate in iteration 2" comment in the gate file, and a `## Follow-up` note in the PR. (This admin gate is for mock pages merged to `main`; CLAUDE.md's `VERCEL_ENV !== "production"` rule is a different thing — draft *content* visibility on previews.)
- Title the PR with `(iter 1)` and state the iteration-2 plan in the body.

## Iteration 2 — real data

- Add a `wire-*.ts` server loader producing the **same shape** (cached per owner, e.g. `unstable_cache` 60s). `page.tsx` swaps one function call; components stay untouched except: fields become **nullable** + per-block "coming soon" branches (#631).
- **Reuse proven loaders** other pages already use (cached, RLS-scoped) so the same number never disagrees across pages — #631 reused `/home`'s portrait loaders and mirrored `load-owner-portrait-counts.ts` exactly for the one new aggregate.
- No reliable data for a block → a lowercase `soon` / `coming soon` state, **never a fake number**. Don't wire loaders you can't validate — "I left them 'coming soon' to avoid wiring loaders I couldn't validate blind" (#631).
- Remove the iteration-1 gate in this same PR.
- A new aggregate that can't be exercised locally (no seeded DB, CI mocks it) → flag it: "⚠️ needs real-network validation — **do not auto-merge**" (#631).
- Keep the mock file: it powers tests and documents the contract.

## Quick reference

| | Iteration 1 | Iteration 2 |
|---|---|---|
| Data | Typed mock fixture | `wire-*.ts` real loader, same shape |
| Goal | Lock layout + design | Real numbers, no design change |
| Components | Built final | Untouched (nullable fields + `soon` branches only) |
| Access | Admin-gated | Gate removed |
| Missing data | Realistic fake (it's gated) | `coming soon` block, never a fake number |

## Common mistakes

| Mistake | Fix |
|---|---|
| Shipping the mock ungated "just for a day" | Gate in the same PR or an immediate follow-up (#630 merged 5 min after opening) |
| Reshaping component props in iteration 2 | Props were the contract; only nullability + soon-branches may change |
| Writing a new aggregate when a proven loader exists | Reuse first; numbers must agree across pages |
| Filling a data gap with a plausible number | `soon` chip. Real users never see invented data |
| Merging iteration 2 without real-data sanity check | Flag "do not auto-merge", ask for validation on a real network |
