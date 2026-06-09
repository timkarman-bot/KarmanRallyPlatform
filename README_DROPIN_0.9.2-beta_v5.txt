Release 0.9.2-beta v5 - Import Page Cleanup

Drop-in files:
- templates/admin_show_import.html
- docs/RELEASE_HISTORY.md
- docs/CHANGELOG.md

Purpose:
The import page now keeps the green downloadable template section and removes the redundant blue CSV instruction block.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add templates/admin_show_import.html docs/RELEASE_HISTORY.md docs/CHANGELOG.md README_DROPIN_0.9.2-beta_v5.txt
git commit -m "Release 0.9.2-beta clean up import page instructions"
git push origin main
