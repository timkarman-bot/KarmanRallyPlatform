SHOW ADMIN + IMPORT + ARCHIVE DROP-IN

Purpose
- Replaces the crowded Manage Shows page with a clean show list.
- Adds a per-show Manage page.
- Adds an Import Center for outside registrations and judging classes.
- Adds Archived Shows as a collapsed section.
- Adds an Archive action that preserves data and closes the show.

Files included
- app.py
- database.py
- templates/admin_shows.html
- templates/admin_show_detail.html
- templates/admin_show_import.html
- templates/admin_placeholders.html
- utils/print_cards.py

Important
- Do not install the earlier 8-category ZIP.
- This package builds on the claimable placeholder / auto class design.
- The import center accepts CSV files, including Google Forms / Google Sheets CSV exports.

Import classes CSV accepted columns
- class_code
- class_name
- description
- year_min
- year_max
- make_contains
- model_contains
- keyword_contains
- award_places
- sort_order
- is_active

Import registrations CSV accepted columns
- car_number
- owner_name or name
- phone
- email
- year
- make
- model
- class_code or class_name or judging_class
- payment_status
- waiver_received

Behavior
- Imported outside registrations are assumed already accepted by the outside system.
- If car_number is blank, the next available open placeholder card is claimed.
- If car_number matches an open placeholder, that placeholder is claimed.
- If class is not supplied, the system attempts auto class assignment from year/make/model.
- If zero or multiple classes match, the car is flagged for staff review.
- Archived shows remain in the database and are hidden in a collapsed Archived Shows area.

Local test before deploy
1. Stop Flask with CTRL+C.
2. Replace the files.
3. Run:
   python -m py_compile app.py database.py utils/print_cards.py
4. Run:
   python app.py
5. Open:
   http://127.0.0.1:8080/admin/shows
6. Test:
   - Shows list loads cleanly.
   - Click Manage on a show.
   - Save a show.
   - Open Import.
   - Upload a small classes CSV.
   - Upload a small registrations CSV.
   - Check Placeholder Cars and Show Mode.

Do not commit
- instance/
- local app.db
- .env
