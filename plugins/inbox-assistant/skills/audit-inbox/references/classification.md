# Audit evidence and Gmail-rule design

Use this reference only during a one-time audit. The plugin-wide semantic categories and attention levels live in `../../../policy/classification.md`.

## Evidence retained for every candidate group

- mailbox and authenticated profile;
- exact sender, authenticated domain, and stable message pattern;
- message count, first seen, last seen, and representative subjects;
- messages and active weeks in the previous eight weeks;
- messages per active week;
- reply evidence and relevant Gmail Personal, Promotions, and Important signals;
- unsubscribe mechanism and known unsubscribe status;
- mixed-purpose counterexamples from the same sender or domain.

## Rule-safety ladder

Prefer the narrowest matcher that produces the desired result:

1. exact deterministic subject or header pattern;
2. sender plus purpose-specific subject/header pattern;
3. stable sender address;
4. authenticated organization domain;
5. broad category only when the user explicitly accepts its trade-offs.

Never create a sender-wide rule from a sample that contains materially different purposes. A user may explicitly approve an organization-wide preference after seeing its scope; persist that choice as persona policy rather than pretending it is a universal classification rule.

## Digest recommendation evidence

Assess Events, Content, Updates, and Notifications/Transactions separately. Two or more digest-eligible messages per active week is strong evidence that consolidation may help, not a mandatory threshold. Consider recent acceleration, time sensitivity, and whether a digest would save more interruptions than it creates.

## Removal review

- `List-Unsubscribe` proves list infrastructure, not message purpose.
- Keep confirmed-unsubscribed sources in the audit record and exclude them from duplicate review.
- Treat unsubscribe, spam, and block as distinct outcomes and permissions.
- Flag suspicious impersonation separately from ordinary cold outreach.
