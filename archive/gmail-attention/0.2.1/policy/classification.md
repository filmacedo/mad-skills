# Classification policy

Assign exactly one semantic purpose and one attention level to each message.

## Semantic purposes

| Purpose | Meaning | Default handling candidate |
| --- | --- | --- |
| Human correspondence | A person or team wrote the message as correspondence | Keep in Inbox |
| Events | Event discovery, public invitations, roundups, and announcements to consider | Events label or digest |
| Content | Editorial or educational reading: newsletters, articles, essays, interviews, analysis, and curated links | Content/newsletter label or digest |
| Updates | A sender's own product, company, account, service, onboarding, marketing, or operational change | Updates label or digest |
| Notifications | Automated activity, mentions, exports, invitations from apps, and routine alerts | Notifications label or digest |
| Transactions | Receipts, invoices, successful payments, orders, bookings, and records | Transactions label or digest |
| Cold Outreach | Unsolicited sales, agency, recruiting, or partnership attempts without evident prior conversation | Cold-outreach review |
| Other | No confident purpose after reasonable inspection | Leave untouched and review |

Suspicious phishing is a safety state, not a semantic purpose. Preserve the apparent purpose for analysis but let the suspicious attention level override normal handling.

## Attention levels

| Attention | Meaning | Default behavior |
| --- | --- | --- |
| Act now | Due, blocking, security-sensitive, or consequential if delayed | Keep visible and lead the brief |
| Act later | A genuine required action with a future deadline or clear timing | Keep visible with deadline |
| FYI | Useful awareness with no response or decision required | Keep visible by default; persona may archive |
| Routine cleanup | Predictable, low-urgency mail covered by an approved routing policy | Label/archive and disclose |
| Suspicious | Phishing or impersonation concern | Leave untouched and warn |

Do not put optional reading, reversible inactivity notices, or no-action product information under Act later merely because a future date appears in the message.

## Deterministic patterns

| Pattern | Purpose | Default attention |
| --- | --- | --- |
| Automated calendar acceptance | Notifications | Routine cleanup |
| Calendar decline or cancellation | Notifications | Act now or FYI depending on consequence |
| Delivery failure | Notifications | Act now |
| Unsubscribe confirmation | Notifications | Routine cleanup |
| Product onboarding without verification or purchase | Updates | Routine cleanup |
| Terms or privacy update without a material service deadline | Updates | FYI |
| Successful receipt or invoice record | Transactions | Routine cleanup |
| Failed payment or action-required billing problem | Transactions | Act now |
| Automated app connection/follow/workspace invitation | Notifications | FYI |
| Password reset, verification challenge, access-loss warning | Notifications | Act now |
| Ordinary new-sign-in notice without explicit danger | Notifications | FYI |

Persona policy may change the handling or visibility of FYI patterns. A warning that explicitly identifies suspicious activity, irreversible loss, or required remediation stays actionable unless the user gives an equally explicit, appropriately scoped preference.

## Event discovery versus operations

Event discovery includes invitations, promotions, local-event curation, and recurring roundups whose main purpose is helping the user decide whether to attend. Event operations include registration status, tickets, receipts, cancellations, venue or schedule changes, reminders, deadlines, and logistics.

Discovery may be routed to an Events digest. Operations must be classified by their real consequence and kept visible unless persona policy explicitly says the user no longer participates in that source or organization.

## Content versus Updates

- Use Content when the primary value is an idea, argument, interview, article, analysis, or set of links to read.
- Use Updates when a company is talking about its own product, service, account, campaign, or operational change.
- Mailing-list headers identify distribution infrastructure, not purpose.

## Cold outreach versus phishing

Cold outreach is an unwanted but plausibly genuine attempt to start a relationship. Phishing uses deceptive identity, domains, or destinations to obtain credentials, money, or unsafe action. Cold outreach may be labeled and archived under persona policy; suspicious phishing remains untouched until the user approves reporting or blocking.
