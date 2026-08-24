---
name: new-feature
description: >-
  Draft a PRD for a noticed feature, bug, chore, refactor, or removal and
  create the row in the `noticed_ PRDs` Notion database. Use whenever Filipe
  or Simão says "new feature", "spec a feature", "write a PRD", "draft a
  PRD", "/new-feature", pastes a voice-note transcript that describes
  something to build, or says "let's build X", "we should add Y", "there's a
  bug in Z", "rewrite of X", "kill Y", "redo Z". Picks up at idea/voice-note
  intake and ends with a Notion page link the human can review.
---

# new-feature

End-to-end: idea or voice dump → Notion PRD row in `Status = Spec`. Companion to `build-feature` (in development — humans currently run the build manually after the PRD is filed).

A PRD should fit on one screen. It's the shortest of the artifacts and the most consequential — it sets direction, and everything downstream (Approach, the build) is a consequence of what's written here. If it won't fit on a screen, it's probably two features: split it into separate rows rather than padding one.

## Inputs

One of:
- A raw idea ("we should add LinkedIn import to onboarding")
- A voice-note transcript (paragraph or three)
- A bug report ("webhook fires twice when X")
- A chore / refactor / removal ("upgrade Next.js", "rewrite the search ranker", "kill the legacy embedding job")

Whatever the human typed/dumped, treat as the seed. If sparse, interview to fill gaps. If rich, lift quotes directly into the right sections and skip ahead.

## Reference

- Methodology: `how we ship at noticed` Notion page (id `365efbd6e46b80bda569f2275b35ee03`).
- PRDs database (write target): `efbb5a57455948e8adeff4c1cb0dd58d`.
- PRD page template: id `371efbd6e46b809e90b2d224ad16fe1e` — the canonical 5-section shape.
- Notion API: use the `notion-cli` skill (`ntn`). Look up exact flags with `ntn pages create --help` and `ntn api v1/pages --docs` — do not hallucinate syntax.

### Database schema (verified — keep in sync if it drifts)

- `Name` — title
- `Status` — **status** type (not a plain select), one of `Idea` / `Spec` / `Building` / `Shipped` / `Parked`
- `When` — select of weekly date-ranges (e.g. `jun 08 - jun 14`); leave blank
- `Owner` — **person** (JSON array of Notion user IDs, not strings; `limit: 1`)
- `PR` — relation to the PRs DB (leave blank; `build-feature` populates it)
- `ID` — auto-increment, system-managed

## Pre-flight (run once per session, cache results)

1. `ntn` on PATH? If not, install: `curl -fsSL https://ntn.dev | bash`.
2. `ntn` authenticated? Check `NOTION_API_TOKEN`; otherwise `ntn login`.
3. Resolve owner user IDs once: `ntn api v1/users` and grep for Filipe + Simão. Cache them in memory for the rest of the run. If neither is found, surface the error — don't write the row.

## Core loop

### 1. Classify

Read the input. Pick one:
- **Feature** — net-new behavior, user-visible. Default.
- **Bug** — something existing is broken.
- **Chore / refactor / removal** — internal-only or invisible work.

If genuinely ambiguous, `AskUserQuestion`. Otherwise decide.

### 2. Interview

Style: mostly `AskUserQuestion` with 2-3 options each (plus the implicit Other / free text). Allow the human to paste a voice dump at any point — if they do, lift it verbatim into the relevant section and skip ahead.

**The tables below are a default scaffold, not a script.** Rephrase the questions to fit the seed, generate the options from the seed (not a fixed list), reorder when it makes the flow more natural, and drop any question whose answer is already in the seed. The only fixed pieces are which PRD sections each PRD type needs to fill (Problem / Goal-Non-goals / Approach / Locked decisions / Done when for features; Goal / Approach / Locked decisions / Done when for bugs and chores — Locked decisions omitted when there are genuinely none). Everything else is shapeable.

Default scaffold, mapped to the PRD section each question feeds:

**Feature** (all 5 sections):

| Question | Feeds section |
|---|---|
| "What's broken or missing today?" — 2-3 framings of the seed + Other. Frame it from the user's POV (the pain they experience), not as a pre-baked solution. | `Problem` |
| "What's true after we ship?" — 2-3 target-state phrasings + Other. Push for an observable change in behavior (what users do differently), not a feature/UI element. | `Goal / Non-goals` (Goal) |
| "What's explicitly out of scope?" — 2-4 likely-adjacent things + Other, each with a one-line why. Skip if nothing comes to mind. | `Goal / Non-goals` (Non-goals) |
| "What gets built?" — 2-3 surface-area sketches + Other | feeds `Approach` (combined with step 3) |

**Bug** (skip Problem and Non-goals):

| Question | Feeds section |
|---|---|
| "Desired end state?" — short free text or AskUserQuestion if obvious options exist | `Goal / Non-goals` (Goal only) |
| "Suspected cause / where does it live?" — 2-3 guesses + Other | feeds `Approach` |

**Chore / refactor / removal** (skip Problem and Non-goals):

| Question | Feeds section |
|---|---|
| "Desired end state?" — one line | `Goal / Non-goals` (Goal only) |
| "Where does the change live?" — file/package guesses + Other | feeds `Approach` |

Rule of thumb: if the seed already answers a question, lift it verbatim and skip the question entirely. The goal is the fewest prompts that fill the required sections — not running the table top-to-bottom. Don't interview for Locked decisions: harvest them from the seed/interview (any choice the human has already made — tech, UX, library) and draft the rest in step 4.

### 3. Ground Approach in the codebase

Before drafting Approach, search the noticed repo so Approach names real files. This is a Turborepo — paths to know:

- App routes / pages: `apps/noticed-agent/app/`
- App-local components: `apps/noticed-agent/components/`
- Shared UI primitives (shadcn): `packages/ui/src/`
- Postgres schema (Drizzle): `packages/postgres/src/`
- ClickHouse migrations: `packages/clickhouse/src/migrations/`
- Agent capabilities / personas: `packages/agent-core/`
- Pipeline processors: `apps/noticed-agent/app/lib/pipeline/`

`CLAUDE.md` is the source of truth for monorepo structure, database conventions, and architecture rules — skim the relevant section (Monorepo Structure, Databases, Architecture Rules, ClickHouse Best Practices) before grounding Approach in any area it covers.

The goal isn't a full design review — it's enough context that Approach names actual files, components, and tables, not generic placeholders.

If the search surfaces a meaningful conflict (e.g., the human asked for a new modal but a similar one already exists), surface it via one `AskUserQuestion` before drafting. Otherwise proceed.

### 4. Draft Approach + Locked decisions + Done when (autonomous)

Write these without asking the human — they edit in Notion if wrong.

- **Approach** — concrete surfaces (specific tables, routes, pages, components). Reference real file paths and component names from step 3. Short bulleted list, one bullet per surface.
- **Locked decisions** — choices already settled that `build-feature` must NOT reopen without asking (e.g. "WebSocket push, not polling"; "reuse the existing `<Dialog>`, don't build a new modal"; "email notifications stay out — that's the Non-goal"). Lift verbatim any decision the human stated in the seed/interview; add the load-bearing ones implied by Approach. One bullet each. Omit the section entirely when there are genuinely none — don't pad it.
- **Done when** — observable checklist. Each item concrete enough that someone watching a screen recording could confirm it: "a badge appears on the inbox icon within 5s of a new comment" (testable), not "the user receives a notification" (vague). Markdown task list (`- [ ] ...`). 3-7 items.

### 5. Preview (skip if seed was rich)

If every section was lifted verbatim from a rich seed and no questions were asked, skip preview — go straight to step 6.

Otherwise, show the full PRD body in chat using the template shape below, then ask one confirmation: "Looks right? (yes / edit X)". Empty reply = ship it. If `edit X`, loop back to the relevant section. Stop after 3 edit cycles and surface state.

**Feature preview:**

```
## <Title>

### Problem
<lifted or interview content>

### Goal / Non-goals
**Goal:** <one line — observable behavior change>
**Non-goals:**
- ... (+ why)

### Approach
- ...

### Locked decisions
- ...

### Done when
- [ ] ...
```

**Bug / chore / refactor / removal preview** (no Problem, no Non-goals; Locked decisions only if present):

```
## <Title>

### Goal / Non-goals
**Goal:** <one line>

### Approach
- ...

### Locked decisions
- ...

### Done when
- [ ] ...
```

If the seed was a voice transcript, append it at the bottom as a collapsed quote for future reference:

```
> **Original transcript**
> <full transcript verbatim>
```

### 6. Write to Notion

Create the row in the `noticed_ PRDs` database via `notion-cli`. The PRD template (id `371efbd6e46b809e90b2d224ad16fe1e`) defines section headings as `##` (h2) — write the body with the same headings so it merges visually with existing PRDs.

Required properties:
- **parent**: database `efbb5a57455948e8adeff4c1cb0dd58d`
- **Name** (title): action verb + object, lowercased to match nearby PRDs in the DB (e.g., "add linkedin import to onboarding", "fix duplicate webhook on agent reply"). Glance at the DB before writing to confirm the convention hasn't drifted.
- **Status**: `Spec`
- **Owner**: array containing the resolved Notion user ID for the human who triggered the skill. Detection order:
  1. Session `userEmail` if available → match to Filipe / Simão.
  2. `git config user.email` → match.
  3. If still unclear, `AskUserQuestion` between Filipe / Simão / Other.
  4. Default to Filipe only as a last resort.
- **When**: leave blank.
- **PR**: leave blank (relation, populated by `build-feature` later).
- **page body**: the sections from step 5 in Notion-flavored Markdown, h2 headings, matching the template shape. Bug / chore PRDs omit `Problem` and `Non-goals` entirely (no empty headings), and omit `Locked decisions` when there are none.

Look up exact `ntn pages create` flags at runtime — don't hardcode.

Verify the page was created (e.g., fetch it back). Return the page URL.

### 7. Output

One line in chat:

```
PRD created: <Notion URL>
```

Stop. Human reviews + edits in Notion. When ready, they run `/build-feature <URL>` (or, while `build-feature` is in development, build it manually).

## Interaction with plan mode

This skill writes a PRD in Notion, not a plan file. If invoked while Claude is in plan mode, **do not** also create a `plans/<date>-<slug>.plan.md` file — the PRD is the single source of truth at this stage. `build-feature` writes the plan file later, after it reads the PRD.

## What this skill does NOT do

- Build anything. That's `build-feature`.
- Set `When`, `Status = Building`, or `GitHub Pull Requests`. Those belong to the human / `build-feature`.
- Loop with a CTO / require approval. The human edits the PRD directly in Notion.
- Full design review. The codebase search grounds Approach; it isn't exhaustive analysis.
- Check for duplicate PRDs. Humans sweep the DB during the weekly ritual.

## Failure modes

- **`ntn` not installed** → `curl -fsSL https://ntn.dev | bash`, then retry. Don't proceed otherwise.
- **`ntn` not authenticated** → set `NOTION_API_TOKEN` or run `ntn login`. Don't proceed.
- **Owner user IDs not resolvable** → surface the error verbatim, don't write the row.
- **DB write fails** → surface the error verbatim, leave the PRD content in chat for manual paste.
- **Human declines preview repeatedly** → stop after 3 edit cycles, surface state, ask what's wrong.
