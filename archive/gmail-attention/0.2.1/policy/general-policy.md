# General policy

This is shared, versioned product knowledge. It applies to every user unless an explicit persona preference overrides it. Do not write personal senders, organizations, documents, projects, accounts, or formatting tastes into this file.

## Decision model

Decide each message on two independent axes:

1. **Semantic purpose** — what kind of message it is.
2. **Attention level** — what the user should do about it.

Then resolve the allowed mailbox action from shared safety rules plus the user's persona. A message may be a Notification and still require action; a human message may be FYI with no reply required. Do not use category as a proxy for urgency.

## Precedence

Apply rules in this order:

1. authenticated mailbox identity, phishing, and mutation safety;
2. explicit user preference or standing permission with matching scope;
3. deterministic message-purpose pattern;
4. shared general policy;
5. sender-purpose history;
6. model inference;
7. leave untouched and ask when material ambiguity remains.

Specific rules beat broad rules at the same level. An explicit persona preference may change classification, action, or digest visibility, but it cannot disable mailbox identity verification or silently authorize a destructive action outside its recorded scope.

## Human correspondence

- Human-written mail remains human correspondence even when it is a one-word acknowledgement or requires no reply.
- Sender display names are insufficient. Inspect headers, message content, and thread context when automation versus human authorship matters.
- Do not label or archive human correspondence by default. A user may explicitly create a narrow sender, organization, thread, or document override.
- Cold outreach is the exception: clearly unsolicited outreach may be labeled and archived under an approved policy, but spam reporting and blocking require their own authority.

## Mixed-purpose senders

Classify the message, not the brand or sender. Payment providers, event platforms, GitHub, Google, colleagues, and vendors can each send multiple purposes. Prefer narrow message-pattern matchers over sender-wide rules.

## Shared versus personal learning

Feedback changes persona memory immediately only when it expresses an explicit preference or correction. It may also create a pending shared-policy candidate. Never modify this shared policy automatically during a digest or feedback run.

A shared-policy candidate is suitable for promotion only when it:

- describes sender-independent behavior;
- is not merely a personal tolerance or preference;
- contains no private message text or personal identifiers;
- has a regression fixture;
- does not conflict with an existing safety invariant;
- is reviewed before a plugin version is released.
