# Database Migration Plan 0.9.1-beta

## Purpose

Plan database changes for participant-restricted voting, show support roles, and platform contact retention.

## Admin / Role Tables

### admin_users
Already planned in 0.9.0-beta.

Recommended fields:
- id
- name
- email
- password_hash
- global_role
- is_active
- created_at
- updated_at

### admin_user_show_roles
Already planned in 0.9.0-beta.

Recommended fields:
- id
- admin_user_id
- show_id
- role
- is_active
- created_at
- updated_at

Allowed show roles:
- owner
- manager
- staff
- judge

## Participant Voting Tables

### show_voters

CREATE TABLE IF NOT EXISTS show_voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL,
    show_car_id INTEGER,
    voter_token TEXT NOT NULL UNIQUE,
    voter_type TEXT NOT NULL DEFAULT 'participant',
    display_name TEXT,
    email TEXT,
    phone TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    activated_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT,
    FOREIGN KEY(show_id) REFERENCES shows(id),
    FOREIGN KEY(show_car_id) REFERENCES show_cars(id)
);

### restricted_votes

CREATE TABLE IF NOT EXISTS restricted_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL,
    voter_id INTEGER NOT NULL,
    category_key TEXT NOT NULL,
    judging_class_id INTEGER,
    selected_show_car_id INTEGER NOT NULL,
    vote_weight INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT,
    UNIQUE(show_id, voter_id, category_key),
    FOREIGN KEY(show_id) REFERENCES shows(id),
    FOREIGN KEY(voter_id) REFERENCES show_voters(id),
    FOREIGN KEY(judging_class_id) REFERENCES show_judging_classes(id),
    FOREIGN KEY(selected_show_car_id) REFERENCES show_cars(id)
);

## Show Settings

Add if missing:

ALTER TABLE shows ADD COLUMN participant_voting_enabled INTEGER NOT NULL DEFAULT 0;
ALTER TABLE shows ADD COLUMN participant_vote_change_allowed INTEGER NOT NULL DEFAULT 1;
ALTER TABLE shows ADD COLUMN participant_voting_completion_message TEXT;

## Contact Retention Fields

Existing fields:
- people.opt_in_future
- people.sponsor_opt_in
- consent_text
- consent_version

Recommended future additions:
ALTER TABLE people ADD COLUMN future_contact_status TEXT NOT NULL DEFAULT 'unknown';
ALTER TABLE people ADD COLUMN unsubscribed_at TEXT;
ALTER TABLE people ADD COLUMN last_contacted_at TEXT;

## Migration Rule

All SQLite migrations must be wrapped:

try:
    cur.execute(sql)
except sqlite3.OperationalError:
    pass
