Release 0.8.4-beta v3 - Public Registration Show Picker + Capacity Reopen Rule

Drop-in files:
- app.py
- database.py
- templates/base.html
- templates/register_picker.html

What this version does:
1. Top navigation Register button opens /register, a show picker.
2. /register lists active/upcoming public shows without forcing users through every show detail page.
3. Each show card displays whether pre-registration is open, full, or closed.
4. Full shows display "Registration Full" and do not show the Register button.
5. Admin-closed/day-of shows display "Registration Closed" and do not show the Register button.
6. Direct /register/<show_slug> links are protected too. If full/closed, they show registration_closed.html.
7. APP_VERSION remains 0.8.4-beta.
8. Canceled, refunded, or removed registrations now release their slot assignment so registration can reopen automatically when capacity becomes available.
9. A hard admin close still blocks registration even if spots are available.

Important business rule:
- Canceling a registration frees the spot.
- Admin hard close overrides capacity and keeps registration closed.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Test:
/register
/register/<open-show-slug>
/register/<full-show-slug>
/register/<closed-show-slug>
/admin/car-search
/admin/placeholders
/admin/version

Suggested commit:
git add app.py database.py templates/base.html templates/register_picker.html
git commit -m "Release 0.8.4-beta reopen capacity after cancellation"
git push origin main
