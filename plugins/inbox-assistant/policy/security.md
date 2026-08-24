# Security and mutation policy

Read this before any Gmail write, unsubscribe, spam, block, or recommendation to follow an email link.

## Mailbox identity

- Fetch the authenticated Gmail profile before searching each connection.
- Require an exact normalized match to the configured mailbox.
- Fail closed on missing, ambiguous, or mismatched identity.
- Never move message IDs, thread IDs, labels, links, checkpoints, or results between mailboxes.

## Phishing screening

For branded security, access, payment, or account-action mail:

- compare the visible brand with the actual From and authenticated/return-path domain;
- inspect authentication results when available;
- inspect the real hostname of action links without opening them;
- treat a material brand/domain mismatch, misleading display name, unencrypted HTTP action link, or destination outside expected official domains as suspicious;
- never recommend clicking a suspicious message link; direct the user to navigate independently to the official service.

If authenticity cannot be established confidently, leave the message untouched and explain the uncertainty.

## Write safety

- Complete search, pagination, required reads, deduplication, and classification for a mailbox before mutating that mailbox.
- Archive only by removing `INBOX` from exact inspected message IDs.
- Preserve read/unread, starred, importance, and unrelated labels.
- Use an explicit allowed-label set from persona policy. Do not invent fallback labels after a failure.
- Make writes idempotent. On an uncertain result, reread state before retrying.
- Verify every write before marking a mailbox or run complete.

## Approval boundaries

- An approved audit plan authorizes only the displayed matchers and actions.
- Spam reporting and blocking require explicit authorization scoped to the sender or matcher, unless persona memory contains an equally explicit standing permission.
- Unsubscribe authority is separate from label/archive authority. Scope it by mailbox and message type.
- Prefer standards-based `List-Unsubscribe` mailto or one-click mechanisms. Do not follow arbitrary body links automatically.
- Browser actions with external side effects require confirmation at action time unless a standing permission covers the exact action and scope.

## Sensitive storage

Do not store message bodies, credentials, tokens, raw MIME, or arbitrary link query strings in persona memory, run state, feedback logs, fixtures, or policy candidates. Retain message IDs and compact non-sensitive evidence only when needed for auditability.
