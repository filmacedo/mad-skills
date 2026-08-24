---
name: weekly-review
description: Review a founder's work week from available evidence, communicate progress when authorized, and propose a focused next week. Use for weekly reviews, founder status updates, or deciding the next focus.
---

# Weekly Review

Turn evidence from the week into an honest account of progress and a small set of next outcomes.

## Context

Use the context root supplied by the user or automation. Read its agent instructions and only the personal, company, task-system, and communication context relevant to this review. Project systems remain authoritative for live delivery state.

Use the previous successful review as the start of the window. If none is available, use the current calendar week in the configured timezone.

## Evidence

Check available sources that can materially change the review, such as sent mail, calendar, company messages, pull requests, documents, tasks, PRDs, and recent agent work. Name meaningful gaps. Deduplicate one outcome found in several places.

When GitHub is available, review open issues labeled `skill-improvement` in the configured repositories that own active skills. Treat issues as candidates, not active instructions, and distinguish skill-text friction from product or tooling gaps.

Distinguish shipped work from meetings, research, drafts, active work, and abandoned experiments. A task title or plan is not proof of completion.

## Outcome

Produce:

1. a concise first-person progress update;
2. a private note on evidence coverage and uncertainty;
3. one focus and no more than three measurable outcomes for the next week.

For a scheduled run, follow the delivery target and permissions in its prompt, verify any external post, and return its link. In an interactive run, do not publish or message anyone unless the user asks.

Proposed outcomes are not commitments. Persist them only after confirmation, using the configured task system.

Keep skill-maintenance candidates in the private review material. Surface the open issues that need a decision, more evidence, or action without imposing a fixed count.

## Learning loop

After the review, name repeated friction or missing evidence and propose the smallest improvement. Check for an existing `skill-improvement` issue and offer to create or update it with compact, non-sensitive evidence. Never mutate GitHub, rewrite this skill, or change its automation without approval.
