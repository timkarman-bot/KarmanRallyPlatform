# Participant-Restricted Voting

Version: 0.10.0-beta

## Purpose

Participant-restricted voting allows a show to limit voting to registered participants and staff-issued judges while still using QR codes on the vehicle cards.

## Supported Uses

- Participant-only judging
- Staff-issued judge codes
- Judges-only voting
- Participant-and-judge voting
- School/team voting later
- One vote per category
- Vote changes before voting closes

## Workflow

1. Admin selects `participant_only`, `judge_only`, or `participant_restricted` for both groups.
2. Voting is opened for the show.
3. Registered participant cards are printed with backs enabled.
4. The back of each registered card shows a Voting Access QR.
5. The participant scans the access QR once to activate their voting access.
6. The participant scans vehicle category QR codes to vote.
7. The system allows one active vote per category.
8. If the participant votes again in the same category, the vote is changed.
9. The system shows voting progress and a completion message.

## Judge Codes

Admin can create a judge code from the show detail page. The judge receives a link that activates voting access without being tied to a registered vehicle.

## Rules

- One voter has one active vote per category.
- Participant voters cannot vote for their own vehicle.
- Participant access requires a paid, paid-cash, manually paid, or comped registration.
- Judges are not tied to a vehicle.
- Vote changes are allowed only when the show setting permits changes.
- Public fundraiser voting remains separate.

## New Routes

- `/vote-access/<show_slug>/<car_token>`
- `/judge-access/<show_slug>/<voter_token>`
- `/restricted-vote`
- `/restricted-vote/<show_slug>/complete`

## New Templates

- `voter_activate.html`
- `restricted_vote.html`
- `restricted_vote_success.html`
- `restricted_vote_complete.html`
- `restricted_vote_not_authorized.html`
