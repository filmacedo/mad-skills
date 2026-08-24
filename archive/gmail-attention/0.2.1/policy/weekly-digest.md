# Weekly digest contract

The weekly digest is a read-only delivery view over Gmail Attention classification and persona policy. It never replaces the daily cleanup checkpoint and never mutates Gmail.

## Content mode

Help the user decide what is worth reading, not merely which newsletters arrived.

1. Open with a two- or three-sentence executive summary of the week's main themes.
2. Show up to three recommended reads, ranked by likely relevance, novelty, and substance. Explain why each may be worth the user's time.
3. List every remaining qualifying message once under `More from this week`.
4. For every item include the account tag, publisher or author, full subject, a useful topic summary, and an account-routed source link.

Do not turn optional reading into an action item. Respect persona preferences for sources, topics, exclusions, length, and ranking, but do not infer a permanent preference from one skipped issue.

## Events mode

Help the user decide what to attend and what planning may be needed.

1. Open with the one to three most relevant upcoming events and why they stand out.
2. Group the full set by event date, not email receipt date.
3. For every invitation include the account tag, organizer, event title, date and time in the user's timezone, location or `Location not disclosed`, RSVP status or deadline when known, and an account-routed source link.
4. Mark attendance or RSVP as `Optional` unless the message or persona establishes a real commitment.

Event discovery belongs here. Registration confirmations, tickets, cancellations, venue changes, deadlines, and operational logistics belong in the daily attention flow and must not be hidden in a discovery digest.

## Completeness and failures

- Include each qualifying message exactly once; do not collapse separate issues or invitations into an unlabeled count.
- Note duplicates across accounts or multiple invitations to the same event, but retain each source link.
- If nothing qualifies across all successful mailboxes, output only `Nothing new for this weekly digest.`
- Prominently identify incomplete mailboxes and say their pipeline checkpoints were retained.
