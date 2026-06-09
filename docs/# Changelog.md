# Changelog

All notable changes to the Karman Kar Shows Platform will be documented in this file.

Format:
- Added
- Changed
- Fixed
- Removed

---

### Release 0.8.4-beta

Public Registration
- Added multi-show registration selector page.
- Register button no longer assumes a single active show.
- Users can select from active and upcoming shows.

Registration Capacity
- Registration automatically closes when max cars are reached.
- Registration displays Full when capacity is reached.
- Registration displays Closed when administratively closed.
- Canceled, refunded, and removed registrations release capacity automatically.
- Admin hard close overrides available capacity.

Multi-Day Registration
- Added support for single-select and multi-select registration sessions.
- Session capacities tracked independently.

Admin Improvements
- Added Edit button to Placeholder Cars page.
- Fixed Car Search judging class joins.
- Fixed registration slot display issues.
- Improved placeholder card workflow.
- Improved owner claim and registration workflow.

Documentation
- Updated architecture baseline.
- Updated release tracking.
- Updated project status documentation.## 0.8.3-beta

### Fixed
- Fixed admin car search 500 error caused by judging class join.
- Corrected search_show_cars_admin query structure.
- Fixed placeholder page edit link integration.
- Corrected judging class migration compatibility issues.

### Added
- Registration Edit workflow.
- Registration Edit page.
- Placeholder record editing capability.
- Improved admin registration management.

---

## 0.8.2-beta

### Added
- Placeholder edit link support.
- Additional judging class migration support.

### Fixed
- Railway database compatibility issues.

---

## 0.8.1-beta

### Added
- Admin version endpoint.
- Platform version reporting.

### Fixed
- Judging class migration initialization.

---

## Earlier Releases

Multiple alpha and beta releases implemented:

- Show Management
- Registration Processing
- Voting System
- Stripe Integration
- Sponsorship System
- Waiver System
- Placeholder Registration Cards
- Windshield Card Printing
- Admin Dashboard
- Multi-Day Event Support
- Registration Slots
- Judging Classes
- Charity Payment Routing

Historical details reconstructed from commit history and project records.