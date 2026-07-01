# Changelog

## 0.10.1-beta

Date: 2026-07-01

### Changed
- Redesigned the public home page when no show is active with a centered Karman Kar logo.
- Enlarged the "No Active Show" message and added a direct link for upcoming-show information.

## 0.10.0-beta

Date: 2026-06-25

### Added
- Separate event-update, sponsor, and benefiting-charity contact permissions.
- Unified consented contact center across participants, attendees, and event-interest signups.
- Participants-only and judges-only restricted voting modes.
- CSRF protection for administrative changes and standard browser security headers.
- Mobile navigation menu, stale-event warnings, weekday/date warnings, and waiver configuration safeguards.
- Automated regression tests for consent retention, restricted voting modes, registration, and admin CSRF.

### Changed
- Contact exports contain only people with at least one recorded future-contact permission.
- Restricted participant access requires a completed eligible registration.
- Vote changes honor the show's `participant_vote_change_allowed` setting.
- Event-day voting controls show only the valid next action.
- Sponsor submission is hidden until public sponsorship packages exist.

### Privacy and Operations
- Generated waiver captures and exports are ignored by Git.
- Previously bundled generated waiver files were removed from the release package.
- Show-scoped exports require owner access; platform-wide contact export requires super admin.

## 0.9.2-beta v3

### Added
- Import Center instructions for class and registration CSV files.
- Missing class creation from accepted registration imports.
- Flexible aliases for outside registration/class spreadsheets.
- Import workflow documentation.

### Fixed
- Imported accepted registrations no longer leave cars unclassified when the imported row includes a new class.

### Notes
- Extra custom columns are currently allowed but ignored.
- This release keeps the strict preferred CSV schema while reducing cleanup work for outside spreadsheets.


## 0.9.2-beta v4

### Added
- CSV template download endpoints for classes, registrations, and combined show setup.
- Import-page template buttons.
- Documentation for import template columns.


## 0.9.2-beta v5

### Changed
- Cleaned up import page instructions.
- Removed duplicate blue CSV guidance because downloadable templates now show the required mapping.
