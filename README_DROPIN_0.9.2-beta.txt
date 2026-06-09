Release 0.9.2-beta - Paper Ballot Entry and Spreadsheet Import

Drop-in files:
- app.py
- database.py
- templates/admin_command_center.html
- templates/admin_paper_ballot_entry.html
- templates/admin_paper_ballot_import.html
- templates/paper_ballot_print.html
- docs/PAPER_BALLOT_WORKFLOW.md

What this adds:
- Paper ballot entry generated from each show's active judging/voting classes.
- 1st, 2nd, and 3rd place car number fields per class.
- Validation that the car number belongs to that class.
- CSV template generated from the same classes.
- CSV import for staff-entered paper ballots.
- Paper ballot audit tables.
- Paper votes are counted in the existing vote tally/leaderboards.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Test:
/admin/paper-ballots
/admin/paper-ballots/print
/admin/paper-ballots/template.csv
/admin/paper-ballots/import
/admin/command-center

Suggested commit:
git add app.py database.py templates/admin_command_center.html templates/admin_paper_ballot_entry.html templates/admin_paper_ballot_import.html templates/paper_ballot_print.html docs/PAPER_BALLOT_WORKFLOW.md README_DROPIN_0.9.2-beta.txt
git commit -m "Release 0.9.2-beta add class-based paper ballot entry and import"
git push origin main
