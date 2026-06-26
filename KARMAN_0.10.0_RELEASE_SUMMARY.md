# Karman Kar Shows 0.10.0-beta

Release date: June 25, 2026

## Main changes

- Independent consent for future event updates, sponsor information, and benefiting-charity information.
- Unified consented contact center for participants, attendees, and event-interest signups.
- Restricted voting modes for participants only, judges only, or both.
- Eligible-registration checks, self-vote prevention, and optional vote locking.
- Administrative CSRF protection, security headers, and stronger role checks.
- Mobile navigation, stale-event/date warnings, map and calendar links.
- Registration blocking when no valid waiver text/version is configured.
- Safer event-day voting controls and hidden sponsor submission until packages are published.
- Generated waivers, exports, and uploaded sponsor assets excluded from Git.
- Version incremented to `0.10.0-beta`.

## Deployment

1. Back up the Railway persistent volume and download a show snapshot.
2. Deploy the contents of the release ZIP.
3. Restart the application so additive SQLite migrations run.
4. Verify `/admin/version` reports `0.10.0-beta`.
5. Configure and test the active show's waiver before opening registration.
6. Review the active event date warning and correct the weekday/date if necessary.
7. Test the selected restricted voting mode before opening voting.

## Verification

- Python compilation completed successfully.
- Five automated regression tests passed.
- Public routes, mobile menu, consent controls, sponsorship state, contact center, and admin pages were browser-verified.
