# Implementation Notes 0.9.1-beta

## Scope

This release should add:
- Show support roles
- Participant-restricted voting foundation
- Data retention/contact policy
- Documentation updates

## Support Roles

Use:
- owner
- manager
- staff
- judge

Do not add too many roles yet.

## Route Protection

Add helper functions:

- current_admin_user()
- current_admin_role()
- user_can_access_show(show_id)
- user_can_manage_show(show_id)
- user_can_staff_show(show_id)
- user_can_judge_show(show_id)

## Restricted Voting

Add a new voting mode:
participant_restricted

Use voter activation QR from the back of the windshield card.

## Voting Completion

System should show:
- Number of categories completed
- Number remaining
- Voting complete message

## Data Retention

Keep registration records.
Limit future marketing to opted-in contacts.
Limit organizer access to assigned show data.

## Do Not Break

- Existing public fundraising voting
- Existing registration
- Existing placeholder claims
- Existing admin password fallback
- Existing Railway deployment

## Recommended Release Commit

git commit -m "Release 0.9.1-beta add support roles, participant-restricted voting plan, and contact retention policy"
