---
name: design-taste
description: Use when designing, building, changing, or reviewing any noticed UI — pages, tiles, chips, detail panels, sidebar/nav, empty states, onboarding or connect flows, UI copy — before writing or approving JSX that users will see.
---

# design-taste

## Overview

Filipe's UI judgment for noticed, distilled from his merged PRs. CLAUDE.md's Frontend Rules are the hard rails (Phosphor icons, type tokens, casing, `PageContainer`); this is the taste layer on top — the calls he'd otherwise have to make in review.

## Rules

1. **No false affordances.** If it looks clickable, it must work. A mock/preview must self-declare: dashed panel, lowercase `preview` chip, caption ("What the extension popup looks like"), `pointer-events-none`, no floating shadow, slight opacity (#637). If users still try to click it, **delete it from the flow** — reframing has a one-strike limit (#637 → #639, removed the next day). Diagnose affordance bugs in token terms: the fake button was confusing because it used the real `bg-brand text-brand-foreground` tokens.

2. **Remove or hide what isn't pulling weight.** Nav items with no shipped surface behind them: delete outright (#589 removed Memories/Notifications). A control that only does one thing: collapse it into that thing (#642 — Quick Actions only opened ⌘K, so hide the button and put a `⌘K` chip on the Search row). Hide-don't-delete only when restoration is plausible: gate behind a boolean flag with a restore note (#642's `SHOW_QUICK_ACTIONS = false`). Same instinct at page level: a non-working Sync button and an empty AI Summary get dropped, not kept "for later" (#535).

3. **Reuse existing contracts verbatim.** A new tile mirrors the closest existing tile's full contract, including completion semantics: when the real-world action is unverifiable, **click IS completion**, and done tiles lose their href (#625, "Rate the extension" mirrors Follow on X down to parallel file names). Chip placement follows the existing `new`/`soon`/`lock` affordance-chip convention (#642). One shared component/resolver per concept so surfaces can't disagree — one `ActionRow` for `/home` and the panel, one company resolver for table and panel (#535).

4. **Never a fake number.** A block whose data isn't reliable yet renders a small lowercase `soon` / `coming soon` state (#631). Fabricated data is only acceptable behind an admin gate (see `frontend-prototype`).

5. **Layout stability.** No CLS, no post-hydration reorder: read completion/state server-side so SSR renders the final state and hydration agrees (#625 reads the cookie in `page.tsx` so the grid never reorders on load).

6. **Hierarchy by tone and weight, not size.** Promote emphasis within the two-size type scale: `tone="tertiary"` → `"secondary"`, `semibold tone="primary"` on the action words (#637). Section headings in record views are subtle — small, muted — not bold `SectionHeading` (#535).

7. **Detail/record views read like Lightfield or Attio.** Clean header (avatar + name + inline social icon-links + clamped headline), a single `PropertyRow` field list, muted "Set X" placeholders for empty fields, secondary fields behind "See more", a single hairline divider before the activity sections (#535).

8. **Screenshot-worthy bar for new pages.** A new page should be worth screenshotting and sharing: fixed section order, on-brand accents, no filler (#628).

9. **Scope restraint.** Touch only the surface in question; leave siblings alone and say so ("`ExtensionPopupPreview` itself is untouched — still used on integrations", #639; the design-playground's copy of the sidebar deliberately not changed, #642).

## Red flags — stop and reconsider

- A page or modal stub behind a new nav item ("we'll build it next sprint")
- A button, tile, or link that does nothing yet
- A new tile with novel semantics when a sibling tile already solved it
- A number displayed that no loader actually produced
- A preview/mock styled with live button tokens
- A completion state that only exists client-side (hydration will reorder)
