# Database Migration — 0.10.0-beta

The application performs these additive SQLite migrations during startup:

- `people.charity_opt_in INTEGER NOT NULL DEFAULT 0`
- `registration_intents.charity_opt_in INTEGER NOT NULL DEFAULT 0`
- `attendees.charity_opt_in INTEGER NOT NULL DEFAULT 0`
- `waiver_evidence.charity_opt_in INTEGER NOT NULL DEFAULT 0`

Existing event and sponsor permissions are preserved. Existing records default to no charity-contact permission.

Before deployment:

1. Download a show snapshot and back up `/data/app.db`.
2. Deploy the release.
3. Confirm `/admin/version` reports `0.10.0-beta`.
4. Open the Consented Contact Center and verify expected historical event/sponsor permissions.
5. Test each restricted voting mode on a non-production show.
