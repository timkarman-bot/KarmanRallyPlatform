# Database Migration 0.9.1-beta

The migration is handled in `init_db()` using safe SQLite `CREATE TABLE IF NOT EXISTS` and `ALTER TABLE ... ADD COLUMN` wrapped in try/except.

## Added Show Columns

- `participant_voting_enabled INTEGER NOT NULL DEFAULT 0`
- `participant_vote_change_allowed INTEGER NOT NULL DEFAULT 1`
- `participant_voting_completion_message TEXT`

## Added Tables

### show_voters

Stores participant and judge voting identities.

### restricted_votes

Stores one active restricted vote per voter/category.

Unique constraint:

`UNIQUE(show_id, voter_id, category_key)`

This is what allows changing a vote instead of creating duplicates.
