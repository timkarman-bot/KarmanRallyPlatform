# Role Security Model

Version: 0.9.0-beta

## Purpose

This release introduces show ownership and role-based administration so the platform can support multiple organizers without exposing every show or back-office function to every user.

## Roles

### Super Admin
Can see all shows, create shows, archive shows, set active/upcoming/past status, manage users, assign roles, and access all admin tools.

### Show Owner
Can see and manage only assigned shows.

### Registrar
Intended for show-day registration, check-in, placeholder, and registration correction workflows for assigned shows.

### Judge
Reserved for judging and voting workflows for assigned shows.

### Volunteer
Reserved for limited show-day workflows.

## Backward Compatibility

The existing Railway `ADMIN_PASSWORD` or `ADMIN_PASSWORD_HASH` login remains available as a legacy super-admin fallback.

The new login form supports:
- email + password for named admin users
- password only for the legacy super-admin login

## New Database Tables

- `admin_users`
- `admin_user_show_roles`

## Required Production Validation

1. Legacy password-only admin login still works.
2. Super admin can open `/admin/users`.
3. Super admin can create a show owner.
4. Show owner can log in with email/password.
5. Show owner sees only assigned shows.
6. Show owner cannot create shows.
7. Show owner cannot set global active/upcoming/past status.
8. Show owner can manage assigned show details.
9. Unassigned show access returns 403.
10. `/admin/version` reports 0.9.0-beta.

## Important Notes

This is the first multi-tenant administration foundation. It does not yet fully isolate every future module such as sponsor management by role. Those should be tightened in follow-up patches as each module is made tenant-aware.
