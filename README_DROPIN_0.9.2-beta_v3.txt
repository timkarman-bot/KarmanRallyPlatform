Release 0.9.2-beta v3 - Import Hardening

Drop-in files:
- app.py
- database.py
- templates/admin_show_import.html
- docs/IMPORT_WORKFLOW.md
- docs/RELEASE_HISTORY.md
- docs/CHANGELOG.md

What changed:
1. Import page now shows clear CSV setup instructions.
2. Judging class imports use preferred strict headers but accept common aliases.
3. Accepted registration imports use preferred strict headers but accept common aliases.
4. Accepted registration imports create missing judging classes when class_code/class_name/class/division/judging_class is supplied.
5. Import result message reports missing classes created.
6. Extra custom fields are allowed and ignored for now.
7. Release history and changelog documentation added/updated.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add app.py database.py templates/admin_show_import.html docs/IMPORT_WORKFLOW.md docs/RELEASE_HISTORY.md docs/CHANGELOG.md README_DROPIN_0.9.2-beta_v3.txt
git commit -m "Release 0.9.2-beta harden class and registration imports"
git push origin main
