# Role Security Model

Version: 0.9.1-beta

## Purpose

This document defines administrative and show-support roles for the Karman Rally Platform.

## Platform-Level Roles

### Super Admin
Usually Karman / platform owner.

Can:
- View all shows
- Manage all shows
- Manage all admin users
- Assign users to shows
- Export data
- Access global contact history
- Manage platform settings

### Platform Admin
Future optional role.

Can:
- Support platform operations
- Assist show owners
- View assigned operational areas

## Show-Level Roles

### Owner
The show owner or organizer.

Can:
- Manage assigned show
- Edit show details
- Manage registration settings
- Manage judging classes
- Import/export assigned show data
- View assigned show registrations
- Manage assigned show staff

Cannot:
- View unrelated shows
- View unrelated organizer data
- Manage platform-wide settings unless also Super Admin

### Manager
Trusted show operator.

Can:
- Run most show operations
- Manage check-in
- Manage placeholders
- Edit registrations
- Print cards
- View assigned show reports

Cannot:
- Delete/archive shows
- Manage platform settings
- View unrelated shows

### Staff
Registration table / show-day staff.

Can:
- Search registrations for assigned show
- Check in cars
- Mark cash paid
- Manage placeholders
- Print cards

Cannot:
- Edit show setup
- Manage users
- Export full data unless explicitly allowed

### Judge
Voting or judging access.

Can:
- Access judging/voting tools for assigned show
- Submit or manage judging results if enabled

Cannot:
- View full registration details
- Edit registrations
- Manage show setup

## Rule

Every admin route must verify:

1. User is authenticated.
2. User has access to the show.
3. User role allows the requested action.

## Recommended Role Order

super_admin > owner > manager > staff > judge
