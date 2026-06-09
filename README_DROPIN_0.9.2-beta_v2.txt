Release 0.9.2-beta v2 - Paper Ballot Completion Mode

Files included:
- app.py
- database.py
- templates/admin_paper_ballot_entry.html
- templates/admin_paper_ballot_import.html
- templates/paper_ballot_print.html
- templates/admin_command_center.html
- templates/admin_show_detail.html
- templates/admin_show_import.html
- templates/admin_shows.html
- templates/admin_vote_reviews.html
- templates/base.html
- templates/leaderboard.html
- templates/restricted_vote*.html
- templates/voter_activate.html
- docs/PAPER_BALLOT_COMPLETION_MODE.md

What changed:
- Adds participant car number lookup to Paper Ballot Entry.
- Staff can load QR/electronic voting progress for that participant.
- Paper ballots can fill remaining unvoted class/place choices.
- Any QR/electronic vote made before paper entry remains the official vote for that class/place.
- Duplicate paper entries for already-voted class/place choices are skipped, not counted twice.
- CSV template/import now supports participant_car_number.
- The phone session/cookie remains a convenience for resume; database token remains the authority.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add app.py database.py templates docs README_DROPIN_0.9.2-beta_v2.txt
git commit -m "Release 0.9.2-beta add paper ballot completion mode"
git push origin main

Test:
- Scan valid voter access QR.
- Submit one QR vote.
- Open /admin/paper-ballots.
- Enter participant car number and load status.
- Enter remaining paper votes.
- Confirm already-voted choices are skipped and missing choices are counted.
