# Data Retention and Contact Policy

Version: 0.10.0-beta

## Purpose

The platform should retain registration and participation history in a responsible way that supports future event communication without exposing one organizer's data to another organizer.

## Recommended Position

Karman Rally Platform should retain historical registration/contact data as the platform record.

Karman Kar Shows & Events / Karman should be able to use participant contact information for future notifications only when the participant opted in.

## Why Retain Data

Retaining data helps:
- Notify participants about future shows
- Reduce repeat registration friction
- Build long-term event community
- Support sponsor reporting where allowed
- Maintain waiver and payment audit records
- Support event history and reporting

## Privacy Rule

Organizer access is limited to their assigned show data.

Super Admin access is platform-wide.

Future event notifications may only use:
- Participants who opted in
- Contacts collected directly by Karman events
- Contacts where legal consent exists

## Organizer Isolation

A third-party show owner should not automatically receive access to:
- Other shows' registrations
- Karman back-office data
- Platform-wide contact lists
- Other organizer's participants

## Suggested Data Categories

### Operational Records
Kept for audit:
- Registration record
- Payment status
- Waiver evidence
- Check-in history
- Voting records

### Marketing Contact Records
Used only with consent:
- Name
- Email
- Phone
- Future event opt-in
- Sponsor opt-in
- Benefiting-charity opt-in

Each permission is independent. Event-update permission does not grant sponsor or charity contact permission.

### Organizer View
Limited to:
- Their assigned show
- Their assigned participants
- Their own exports

### Platform View
Super Admin can view:
- All shows
- All historical records
- All opt-in contacts
- Platform-wide reporting

## Opt-In Language

Recommended registration language:

By submitting this form, you agree Karman Rally Platform and the event organizer may contact you about this event. If selected, you also agree to receive future event notifications from Karman Kar Shows & Events / Karman Rally. You may opt out at any time.

## Implementation Recommendation

Do not delete existing contacts by default.

Instead:
- Keep operational records for audit.
- Respect opt-in fields for future marketing.
- Restrict organizer visibility by assigned show.
- Add export filters for opted-in contacts only.

## Future Feature

Contact Center now includes:
- All opted-in participants and attendees
- Search by event history
- Export future event mailing list
- Communication tags

Still recommended:
- Unsubscribe/suppression tracking
- Contact preference history instead of overwriting consent
- Campaign delivery logs
