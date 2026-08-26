---
name: no-ai-slop
description: Use when editing or auditing prose that may contain AI-writing patterns, including requests to de-slop, scan for AI tropes, sharpen machine-drafted text, or run a final editorial review before publishing.
---

# no-ai-slop

## Overview

Remove machine-written habits without removing the writer. Preserve intent, voice, and useful specificity; make the minimum effective edit.

## Before editing

1. Establish provenance: **AI-drafted**, **human-drafted**, or **mixed**. Ask if it changes how aggressively the rules should apply and the answer is unclear.
2. Load any writer or brand voice profile supplied by the user or project. Treat it as the authority for deliberate voice, vocabulary, and formatting choices.
3. Read the full draft. Identify its core point and 3-5 voice signals to protect, such as cadence, bluntness, humor, hedges, or digressions.

For mixed drafts, apply AI-drafted thresholds only to model-written passages when their origin is known. Do not flatten the writer's own sentences to make the whole draft consistent.

## Precedence

When rules collide:

1. A supplied voice profile and voice preservation beat generic pattern bans on human-drafted text.
2. HARD beats STRONG beats LIGHT within the same authority level.
3. Anti-overfitting is the final gate. If a fix sounds forced or less human, restore the original and note it.

HARD means the burden of proof is on keeping the line, not that judgment stops.

## Modes

### Edit (default)

Return the full edited draft, followed by a short **What changed** section. Never return only a summary.

### Detect

Name each pattern, quote the relevant line, and give a short suggested fix. Do not rewrite the draft, score it, or claim to know whether AI wrote it. Offer to edit after the report.

If you drafted the piece in the same session, disclose that conflict and recommend a fresh reviewer before publishing.

## Context and frequency

| Context | Treatment |
|---|---|
| Long-form essays and posts | Full sweep |
| Short-form posts | Light scan; catch stacked tropes and obvious tells |
| Newsletters and letters | Allow useful meta-commentary about the issue or letter |
| Batches | Count repeated patterns across the batch, not per item |

- **HARD:** rewrite unless precedence or anti-overfitting applies.
- **STRONG:** rewrite by default, but use context.
- **LIGHT:** flag only when repeated, distracting, or unsupported.

## The contested three

These patterns are common AI tells, but also legitimate human rhetoric. Treat them as HARD on AI-drafted text and as density checks on human-drafted text.

### Negative parallelism and reframes

Examples: “This isn't X, it's Y,” “less X, more Y,” “you don't need X, you need Y,” and “stop thinking X, start thinking Y.”

On human-drafted text, keep a reframe when it corrects a real belief the reader may hold. Flag straw-man contrasts and repeated reframes that manufacture depth.

### Aphoristic endings

On AI-drafted text, remove a generic mic-drop line and end on the clearest concrete sentence already present. On human-drafted text, preserve a deliberate aphorism that adds a thought; cut conclusions that merely restate the piece.

### Fragmentation

On AI-drafted text, rewrite stacked fragments that perform profundity. On human-drafted text, preserve fragments that carry content or improve rhythm. Remove self-congratulating fragments such as “That's it. That's the whole thing.”

## Preserve the writer

- **Minimum effective edit. HARD.** Fix slop, errors, repetition, and genuinely unclear passages. Leave strong sentences alone.
- **Do not invent. HARD.** Add no claims, examples, statistics, quotes, or opinions. Ask when a missing fact matters.
- **Keep the edge. HARD.** Preserve strong opinions, blunt language, profanity, self-interruptions, and honest admissions.
- **Keep the structure. STRONG.** Reorganize only when structure hurts the piece, then explain why.
- **Cut proportionally. STRONG.** Heavy compression can strip character.
- **Fix actual errors. STRONG.** Correct typos and grammar even in sentences that otherwise stay intact.

## Patterns to catch

**Trailing participle clauses that fake analysis — HARD.** Cut empty clauses built around “highlighting,” “underscoring,” “reflecting,” or “showcasing.” If the analysis matters, state a specific claim in its own sentence.

**Padding — HARD.** Remove phrases whose deletion costs no meaning: “serves to,” “goes a long way in helping,” and similar filler.

**Weasel attribution — HARD.** Name the source behind “experts agree,” “studies show,” or “many argue,” or cut the claim. Never invent a source.

**Unexplained name-dropping — STRONG.** A list of publications, companies, customers, or notable people is not evidence by itself. Keep a name only when the supplied material gives it relevant context, and state only what that material establishes the person or organization did, said, or proved. Otherwise cut the name or ask the writer.

**Importance puffery — HARD.** Replace “a pivotal moment,” “stands as a testament,” “plays a vital role,” and similar claims with the underlying fact.

**Copulative avoidance — HARD.** Prefer “is” or “has” to “serves as,” “stands as,” “represents a,” “boasts,” or “features” when the longer form adds nothing.

**Synonym cycling — HARD.** Repeat the clear name instead of rotating through forced labels such as “the assistant,” “the tool,” and “the solution.”

**Throat-clearing and faux insight — HARD.** Cut “here's the thing,” “let me be clear,” “what nobody tells you,” and “the part everyone misses” when they only announce importance. Do not flag ordinary uses of “nobody” or “most people.”

**Dramatic reveals — STRONG.** Rewrite noun-phrase reveals such as “The best part: it learns.” Keep colons used as real labels or organization.

**Redundant inline headers — STRONG.** Convert a bold label that merely repeats the sentence after it into prose: “**Performance:** Performance improved” says the same thing twice. Preserve a real label followed by new information: “**Schema in TypeScript.** Tables live in one file.”

**Rhetorical setups — HARD.** Cut “what if I told you,” “think about it,” “plot twist,” and self-answered question-and-answer pairs used as theater.

**False ranges — HARD.** Remove “from ancient traditions to modern innovations” when the endpoints do not describe a meaningful range.

**Meta-commentary — HARD in essays and posts.** Cut “in this section,” “let me walk you through,” and “here's a comprehensive overview.” Allow it when the format genuinely requires navigation.

**Chat leakage — HARD.** Remove “great question,” “certainly,” “I hope this helps,” knowledge-cutoff disclaimers, and references to being an assistant.

**Metronome rhythm — STRONG.** Vary sentence and paragraph shapes when the whole draft has settled into a mechanical cadence.

## Words and phrases

Treat these as evidence, not a substitute for reading. Quoted examples, titles, technical terms, and deliberate voice choices are exempt.

**Usually HARD:** delve, realm, harness, tapestry, paradigm shift, cutting-edge, revolutionize, abstract “landscape,” intricate, intricacies, showcasing, crucial, pivotal, meticulously, vibrant, unparalleled, underscore as a verb, leverage, synergy, game-changer, testament, commendable, groundbreaking, foster, enhance, holistic, pioneering, transformative, seamless, robust, empower, frictionless, elevate, mission-critical, visionary, disruptive, reimagine, unprecedented, democratize, state-of-the-art, turnkey, future-proof, supercharge, multifaceted, paramount, ever-evolving.

**Dead phrases — HARD:** “in today's world,” “it's important to note,” “in order to,” “at the end of the day,” “moving forward,” “at its core,” “let's dive in,” “let's unpack,” “to put this in perspective,” “the implications here are,” and “it goes without saying.”

**Dead transitions — HARD:** furthermore, additionally, moreover, that being said, with that in mind, and it is also worth mentioning.

**Engagement bait — HARD:** “let that sink in,” “read that again,” “full stop,” “this changes everything,” and “are you paying attention?”

**Hype — HARD only when vague or promotional:** “unlock your potential,” “unlock growth,” “10x your results,” promises of overnight transformation, and empty claims of superpowers. Literal or precise uses of **unlock** are not automatically banned.

### Contextual jargon

**Decorative technical metaphors — STRONG.** Words such as “substrate,” “wedge,” “vector,” “locus,” “nexus,” “primitive” as a noun, “surface,” “bedrock,” “scaffolding,” “modality,” “gold-plating,” “ratchet,” “endgame,” “north star,” and “flywheel” often make an ordinary mechanism sound more sophisticated. Prefer the concrete mechanism or plain word when the metaphor adds no precision. Preserve established domain terms and literal uses; a phrase such as “API surface” may be the clearest technical name in context.

## Whole-draft checks

- Does sentence length vary naturally?
- Are lists of three real categories or near-synonyms padding for completeness?
- Can abstract claims become concrete using facts already in the draft?
- In product, project, and technical writing, could a sentence appear unchanged in another project's copy? If so, replace it using only a mechanism, instruction, fact, or number already present in the supplied material. Otherwise cut it or ask the writer.
- Do direct verbs replace noun phrases such as “made a decision” and “has the ability to”?
- Does the piece use active voice and human subjects where natural?
- Did any rule fire so mechanically that the result sounds like an AI imitating a human?

## Quick reference

| If you see | Do this |
|---|---|
| Unsupported attribution | Source it, cut it, or ask |
| Generic importance claim | State the underlying fact |
| Repeated reframe | Keep real reader priors; cut straw men |
| Generic final kicker | End on the last concrete sentence |
| Strong human sentence | Leave it alone |
| Detect request | Report patterns; do not rewrite |

## Common mistakes

- Applying every rule at full strength and producing sterile prose.
- Treating one banned word as proof that AI wrote the draft.
- Rewriting the writer's deliberate cadence for consistency.
- Inventing a concrete example to replace an abstract claim.
- Returning an edit summary without the complete edited draft.
- Applying generation advice during Detect mode.

## Workflow

1. Establish provenance and load any available voice profile.
2. Read the full draft and identify the point and voice signals.
3. For Detect mode, return named findings and stop.
4. For Edit mode, make the minimum effective changes.
5. Run every applicable check in `eval.md`; fix failures and re-run.
6. Return the full draft and **What changed**.

If repeated real feedback exposes a durable failure in this skill, propose the
smallest correction after the edit is complete. Check existing
`skill-improvement` issues in `filmacedo/mad-skills`, then offer to create or
update one using compact, non-sensitive evidence. Create or update the issue
only after the user's explicit approval. Never rewrite the skill without
approval, and do not invent an improvement after every use.
