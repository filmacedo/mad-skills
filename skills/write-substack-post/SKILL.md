---
name: write-substack-post
description: Develop and draft a personal Substack post through brief, sparring, drafting, editorial review, and Notion handoff. Use for a personal essay or post, not a company blog post or social copy.
---

# Write Substack Post

Be a writing sparring partner, not a ghostwriter. Help the writer find the strongest personal angle, challenge it, and produce a draft that still sounds like them.

## Context and source

Load the writer's personal context and voice from the supplied context root. Use the configured Notion content database; for Filipe, the data source is `collection://5bdefbd6-e46b-8323-a023-07f364e873c3`. Keep one page for the idea, brief, and draft.

If a topic is already supplied, use it. Otherwise offer a short selection of personal essay ideas currently marked `Idea` and let the writer choose.

## Brief and sparring

Read the existing raw capture and brief. Sharpen, rather than replace, the central argument, opening, supporting scenes or evidence, and closing. Challenge the weakest assumption and ask for any missing personal fact or feeling; never manufacture emotional texture.

Get agreement on the angle before drafting.

## Draft and handoff

Write a concise first draft in the supplied voice. Favor concrete scenes and simple language. Do not force a fixed length or structure when the idea needs something else.

Run `$no-ai-slop` with the writer's voice context. On human-drafted passages, voice preservation beats generic bans.

After the writer approves the draft for Notion, update the existing content page, add or replace its `## Draft` section, and set `Status` to `Draft`. Share the page URL. Do not publish, schedule, or create social posts unless separately requested.

When repeated feedback reveals a durable writing lesson, propose a small change to the voice context or this skill after the draft is complete; never self-edit during the run.
