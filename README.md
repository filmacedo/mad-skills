# mad-skills

This is where I keep the reusable skills I use with AI agents.

A skill is a small Markdown guide for a recurring job. It tells an agent what outcome matters, what judgment to apply, and which boundaries to respect. A plugin groups several related skills so they can be installed together.

The system is deliberately lightweight. Skills start small, improve through real use, and focus on principles rather than instructions tied to one model or app version.

## What is here

### Plugins

- [Chief of Staff](plugins/chief-of-staff) reviews the week, manages personal commitments, and drafts founder updates.
- [Inbox Assistant](plugins/inbox-assistant) audits Gmail and produces daily, reading, and events digests without making unapproved inbox changes.
- [Mad Engineering](plugins/mad-engineering) covers the software lifecycle: prototyping, debugging, test-driven development, code review, simplification, shipping, and post-merge workspace cleanup.

### Standalone skills

- [Brainstorm](skills/brainstorm) challenges an early idea and finds the smallest useful test.
- [Challenge Me](skills/challenge-me) questions an existing proposal until its assumptions and decisions are clear.
- [No AI Slop](skills/no-ai-slop) removes common machine-writing habits while preserving the writer's voice.
- [Write Substack Post](skills/write-substack-post) helps develop and draft a personal essay without turning the agent into a ghostwriter.
- [Mad Mac: Classify New Tracks](skills/madmac-classify-new-tracks) supports a personal Rekordbox tagging workflow. It is currently marked for repair in the catalog.

## How invocation works

Most skills are available when an agent decides they fit the task. Some workflows should start only when I ask for them directly.

The current explicit-only skills are:

- `challenge-me`
- `simplify-code`
- `ship`
- `cleanup-workspaces`

Codex can use ordinary skills when they fit, while broad or destructive workflows wait for a direct request.

## What belongs here

This repository contains portable personal skills: work I want to reuse across projects and keep under my ownership.

Project-specific workflows stay with the project they operate. For example, noticed engineering and publishing workflows live in the noticed repositories. They are recorded in the [skill catalog](skill-system/catalog.json), but they are not copied into this repository as personal skills.

## Design principles

- Start with the smallest useful skill.
- Describe the outcome, judgment, and safety boundaries.
- Prefer durable principles over exact commands or model-specific tricks.
- Improve a skill only when real usage provides evidence.
- Keep personal preferences personal and project rules with their project.
- Use review and fresh verification in proportion to the risk.

The aim is a system that is easy to understand, easy to maintain, and still useful after models and agent tools change.

## Install a plugin in Codex

Add this repository as a marketplace once:

```bash
codex plugin marketplace add filmacedo/mad-skills --ref main
```

Then install the plugin you want:

```bash
codex plugin add chief-of-staff@filipe-skills
codex plugin add inbox-assistant@filipe-skills
codex plugin add mad-engineering@filipe-skills
```

Refresh the marketplace after new versions are merged:

```bash
codex plugin marketplace upgrade filipe-skills
```

Standalone skills are installed individually from their folder under [`skills/`](skills).

## Repository structure

```text
plugins/         related skills that install together
skills/          independent personal skills
skill-system/    ownership, locations, and maintenance rules
archive/         old material kept for reference
```

Codex reads `.agents/plugins/marketplace.json`. A Claude-compatible marketplace manifest is also included under `.claude-plugin/`.

## How skills improve

1. Use the skill on real work.
2. Record specific friction or a repeated useful behavior.
3. Propose the smallest change that addresses the evidence.
4. Review and merge the change through a pull request.
5. Reinstall or update the skill and test it in a new task.

Skills may suggest improvements, but they do not rewrite themselves. The detailed process lives in [skill-system/README.md](skill-system/README.md).
