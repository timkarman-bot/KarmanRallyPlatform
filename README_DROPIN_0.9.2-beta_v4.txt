Release 0.9.2-beta v4 - Downloadable Import Templates

Drop-in files:
- app.py
- templates/admin_show_import.html
- docs/IMPORT_WORKFLOW.md
- docs/RELEASE_HISTORY.md
- docs/CHANGELOG.md

Adds:
- /admin/shows/<show_id>/import/template/classes.csv
- /admin/shows/<show_id>/import/template/registrations.csv
- /admin/shows/<show_id>/import/template/combined.csv

Import page now includes:
- Classes CSV download
- Registrations CSV download
- Combined CSV download
- Preferred field instructions

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add app.py templates/admin_show_import.html docs/IMPORT_WORKFLOW.md docs/RELEASE_HISTORY.md docs/CHANGELOG.md README_DROPIN_0.9.2-beta_v4.txt
git commit -m "Release 0.9.2-beta add downloadable import templates"
git push origin main
