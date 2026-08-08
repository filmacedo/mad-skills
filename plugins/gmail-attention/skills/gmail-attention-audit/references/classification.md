# Classification reference

Use one primary classification per message. Classify a deterministic message pattern before grouping by sender. Use Gmail labels, importance, headers, sender identity, subject, snippets, recurrence, and reply history as evidence; do not treat any single weak signal as proof.

## Primary categories

| Classification | Meaning | Default future treatment |
| --- | --- | --- |
| Inbox | Real conversations, replies, and any mail the user explicitly wants immediately | Keep in Inbox |
| Events | Event discovery: newsletters, roundups, and announcements of events to consider | Consider a separate weekly Events digest |
| Content | Editorial newsletters, creator writing, research, and reading | Consider a separate weekly Content digest |
| Updates | Product, company, competitor, onboarding, and business updates | Consider a separate weekly Updates digest |
| Notifications | App activity, mentions, exports, and automated alerts | Daily Notifications + Transactions digest, unless timely |
| Transactions | Receipts, invoices, confirmations, bookings, terms, and records | Daily Notifications + Transactions digest, unless timely |
| Cold Outreach | Unsolicited attempts to start a sales, recruiting, or partnership conversation | Review for Unsub or Block |
| Other | Mail without a confident classification | Manual review |

## Deterministic message patterns

| Pattern | Detection | Classification | Default future rule |
| --- | --- | --- |
| Calendar acceptance | Subject begins `Accepted:` | Notifications | Archive |
| Calendar decline/cancellation | Subject begins `Declined:`, `Cancelled:`, or `Canceled:` | Inbox | Keep visible |
| Shared-calendar access | Shared-calendar or calendar-access request | Inbox | Keep visible |
| Delivery failure | Mailer daemon or delivery-failure language | Inbox | Keep visible |
| Out-of-office | Out-of-office automatic reply | Inbox | Keep visible |
| Unsubscribe confirmation | Explicit “you are unsubscribed”, “successfully unsubscribed”, or preferences-updated message | Notifications | Archive; record source as unsubscribed |
| Product onboarding | Welcome/getting-started product sequence without security, verification, purchase, or booking language | Updates | Candidate for weekly Updates digest |
| Terms or privacy update | Terms of service, legal terms, privacy notice/update | Transactions | Candidate for combined daily digest |
Message patterns override sender rules. A sender-wide rule is safe only when sampled history shows one stable purpose.

## Event discovery versus operations

Do not treat all event-related mail as digest-eligible. Make this split before creating any event rule:

| Type | Examples | Default treatment |
| --- | --- | --- |
| Event discovery | Event newsletters, recurring roundups, invitations, and announcements to consider | Candidate for Events digest after audit evidence and approval |
| Event operations | Registration/waitlist status, tickets, receipts, cancellations, schedule or venue changes, reminders, logistics, and personal calendar invitations | Keep visible or classify by purpose; do not route automatically into the digest |

Do not use an entire event-platform domain as a rule. A platform can send both discovery and operational mail. Derive a sender or subject rule only when the audit demonstrates one stable, discovery-only purpose without false positives.

## Evidence and cadence

For every candidate group, retain:

- message count, first seen, last seen, and representative subjects;
- messages and active weeks in the last eight weeks;
- messages per active week;
- reply evidence and relevant Gmail Important/Personal/Promotions signals;
- unsubscribe availability and current unsubscribe status.

Avoid annual-only recommendations. Recent acceleration may justify a digest even if a full-year average is low. Conversely, a single regular weekly sender may not benefit from a category digest if it would not consolidate multiple messages.

## Guardrails

- `List-Unsubscribe`, `List-ID`, bulk-mail headers, and known platforms identify mailing-list infrastructure, not Content by themselves.
- Do not classify receipts, account/security alerts, application status, legal notices, or onboarding as Content merely because they have unsubscribe links.
- Do not assume a sender represents one purpose. Use pattern rules for mixed senders; send the rest to review.
- Confirmed-unsubscribed mail is an audit record, not an active review candidate.
