Hotfix 0.9.2-beta - Judge Access Option and Missing Route Fix

Fixes:
- Adds missing admin_create_judge_code route so /admin/shows/<id> no longer crashes.
- Adds judge_vote_access route for staff-issued judge links.
- Adds participant voting access routes/templates back into app.py package.
- Adds Participant/Judge access checkbox to show setup.
- Hides judge-code panel unless restricted voting is enabled for the show.
- Saves participant_voting_enabled on the show record.

Deploy:
python -m py_compile app.py database.py utils/print_cards.py
git add app.py database.py templates README_HOTFIX_0.9.2-beta_judge_access.txt
git commit -m "Hotfix 0.9.2-beta add optional judge access routes"
git push origin main

Test:
/admin/shows/<id>
Enable Voting Mode = Participant/Judge restricted voting
Create judge code
Open Judge Link
