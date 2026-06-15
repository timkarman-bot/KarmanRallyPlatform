Release 0.9.0-beta - Show Ownership and Role-Based Administration

Drop-in files:
- app.py
- database.py
- templates/base.html
- templates/admin.html
- templates/admin_shows.html
- templates/admin_show_detail.html
- templates/admin_placeholders.html
- templates/admin_users.html
- docs/ROLE_SECURITY_MODEL.md

What this release adds:
1. Named admin users.
2. Admin user show assignments.
3. Role-based show visibility.
4. Super-admin user management page at /admin/users.
5. Legacy password-only super-admin login remains available.
6. Show list filters to assigned shows for non-super users.
7. Show detail, imports, exports, and updates require show access.
8. Active/global show status controls are super-admin only.
9. Admin tool pages use the current accessible show for scoped users.
10. APP_VERSION is 0.9.0-beta.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Test:
/admin
/admin/version
/admin/users
/admin/shows
/admin/shows/<show_id>
/admin/car-search
/admin/placeholders
/admin/command-center

Suggested commit:
git add app.py database.py templates/base.html templates/admin.html templates/admin_shows.html templates/admin_show_detail.html templates/admin_placeholders.html templates/admin_users.html docs/ROLE_SECURITY_MODEL.md
git commit -m "Release 0.9.0-beta add show ownership and role-based admin access"
git push origin main
