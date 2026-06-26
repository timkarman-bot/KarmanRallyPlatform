# Release History

## 0.10.0-beta — Consent, Restricted Voting, and Event-Day Safety

Date: 2026-06-25

This release adds independently recorded permissions for future event information, sponsor information, and benefiting-charity information. The admin contact center now combines consented registrations, attendee check-ins, and upcoming-event signups while excluding operational records that do not include marketing consent.

Restricted voting can be configured for registered participants only, staff-issued judges only, or both. Participant access requires an eligible completed registration, self-voting remains blocked, and vote changes can be disabled.

Security and operations improvements include administrative CSRF protection, stronger role checks for sensitive show actions and contact exports, security headers, mobile navigation, stale-date warnings, empty-waiver registration blocking, safer voting controls, and removal of generated waiver captures from source control.

## 0.9.2-beta v3 — Import Hardening
Date: 2026-06-09

### Added
- Import page instructions for judging classes and accepted registrations.
- Accepted registration import can create missing judging classes for the show.
- Common CSV header aliases for outside spreadsheets and Google Forms exports.
- Import workflow documentation.

### Improved
- Registration imports now report how many missing classes were created.
- Import page explains required/preferred fields and accepted aliases.
- Extra custom columns are allowed and ignored for now.

### Deployment Notes
- Drop in app.py, database.py, templates/admin_show_import.html, and docs.
- Run `python -m py_compile app.py database.py utils/print_cards.py`.
- Commit as `Release 0.9.2-beta harden class and registration imports`.

## 0.9.2-beta v2 — Paper Ballot Completion Mode
Date: 2026-06-09

Added voter session/cookie resume behavior and paper ballot completion mode tied to participant car number. Prior electronic votes remain locked and paper entry fills only missing classes.

## 0.9.2-beta — Paper Ballot Entry
Date: 2026-06-09

Added class-based paper ballot entry, printable ballots generated from show classes, and CSV paper ballot import support.

## 0.9.1-beta — Participant-Restricted Voting
Date: 2026-06-09

Added participant voting access, restricted voting pages, judge access planning, and one-vote-per-class logic.

## 0.9.0-beta — Show Ownership / Role-Based Admin
Date: 2026-06-09

Added show ownership and role-based administration foundation.

## 0.8.4-beta — Multi-Show Registration Selector
Date: 2026-06-09

Added public registration show picker, registration full/closed states, and capacity reopening after cancellation.


## 0.9.2-beta v4 — Downloadable Import Templates

Date: 2026-06-09

### Added
- Downloadable Judging Classes CSV template.
- Downloadable Accepted Registrations CSV template.
- Downloadable Combined Show Import CSV template.
- Import-page instructions for preferred fields and custom columns.

### Purpose
Reduce import setup errors by giving clubs and show organizers a ready-to-use spreadsheet format.


## 0.9.2-beta v5 — Import Page Cleanup

Date: 2026-06-09

### Changed
- Kept the green downloadable template/mapping section.
- Removed redundant blue CSV instruction block from the import page.
- Simplified import setup so users rely on the system-generated templates.


## 0.9.2-beta v7 - Contact Email Timeout Control
- Added `EMAIL_ENABLED=false` support so contact messages continue saving without waiting on SMTP.
- Reduced SMTP timeout from 30 seconds to a configurable `MAIL_TIMEOUT` default of 5 seconds.
- Added SMTP mode logging showing host, port, SSL/TLS mode, and timeout without exposing credentials.
- Contact Us remains database-first: platform retention still works even when email is disabled or SMTP fails.

## 0.9.2-beta v6 — Contact Message Center and NWRA Email

Date: 2026-06-15

### Added
- Contact Us submissions now save to the platform database in `contact_messages`.
- Admin Contact Messages page for reading, searching, marking read, and archiving messages.
- Email notification support using Railway environment variables for Northwest Registered Agent / Business Identity SMTP.
- Command Center link and new-message count for Contact Messages.

### Reliability
- Contact messages are saved before email is attempted.
- If SMTP/email fails, the message remains available in the platform admin area and the visitor still receives a successful submission message.

### Deployment Notes
- Add Railway variables: MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, CONTACT_EMAIL.
- Recommended NWRA settings: MAIL_SERVER=mailserver.businessidentity.llc, MAIL_PORT=465, MAIL_USE_SSL=true, MAIL_USE_TLS=false.
- Run `python -m py_compile app.py database.py utils/print_cards.py`.
