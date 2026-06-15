Release 0.9.1-beta v3 - Registration Session Cleanup Fix

Files:
- database.py
- templates/admin_show_detail.html

What this fixes:
1. Admin show detail displays one registration day/session row by default.
2. Extra day/session rows are hidden until Add another day/session is clicked.
3. Hidden rows are disabled so they do not submit blank/default slot data.
4. Extra rows can be removed/cleared from the page.
5. Blank existing slot rows are made inactive on save instead of remaining visible forever.
6. Slots removed from the form are made inactive, not deleted, preserving history and old registrations.
7. Participant judge access remains simple: registered participants activate voting from the windshield-card QR; manual judge codes are only for outside judges/staff judges/special groups.

Important verification:
After replacing files, run:
findstr /N /C:"addSlotBtn" templates\admin_show_detail.html
findstr /N /C:"slot-row" templates\admin_show_detail.html
findstr /N /C:"def save_registration_slots_for_show" database.py

Then:
python -m py_compile app.py database.py utils/print_cards.py
python app.py

Local test:
1. Open /admin/shows/<show_id>
2. Confirm only one registration day/session row is visible.
3. Click Add another day/session.
4. Confirm a second row appears.
5. Save Show.
6. Reload the page and confirm only rows with real content remain visible.

Commit:
git add database.py templates/admin_show_detail.html README_DROPIN_0.9.1-beta_v3.txt
git commit -m "Release 0.9.1-beta fix registration session defaults and cleanup"
git push origin main
