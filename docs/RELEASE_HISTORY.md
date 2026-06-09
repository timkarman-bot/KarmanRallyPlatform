# Release History

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
