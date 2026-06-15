Release 0.9.1-beta - Participant-Restricted Voting

Drop-in files:
- app.py
- database.py
- utils/print_cards.py
- templates/admin_show_detail.html
- templates/voter_activate.html
- templates/restricted_vote.html
- templates/restricted_vote_success.html
- templates/restricted_vote_complete.html
- templates/restricted_vote_not_authorized.html
- docs/PARTICIPANT_RESTRICTED_VOTING.md
- docs/DATABASE_MIGRATION_0.9.1-beta.md

What this adds:
1. New voting mode: participant_restricted.
2. Participant voting access via QR on the back of registered windshield cards.
3. One active vote per category per voter.
4. Vote changes before voting closes.
5. Voting progress and voting complete pages.
6. Staff-issued judge access codes from Admin > Show Detail.
7. Database tables: show_voters and restricted_votes.
8. Keeps 0.9.0-beta role/admin foundation and bumps APP_VERSION to 0.9.1-beta.

Important operational notes:
- For participant voting, set the show Voting Mode to "Participant/Judge restricted voting".
- Voting must still be open.
- Registered cards printed with back side enabled will show "Voting Access" QR.
- Placeholder/open cards still show the owner claim QR.
- Participants cannot vote for their own car.
- Judges can vote using staff-issued judge access links.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested tests:
1. Set a show to participant_restricted and voting_open = 1.
2. Print a registered card with back side enabled.
3. Scan /vote-access/<show_slug>/<car_token>.
4. Scan a vehicle category QR.
5. Cast a vote.
6. Vote again in the same category and confirm it changes the vote.
7. Complete all categories and confirm the completion page.
8. Create a judge code in Admin > Show Detail and verify it activates voting access.

Suggested commit:
git add app.py database.py utils/print_cards.py templates/admin_show_detail.html templates/voter_activate.html templates/restricted_vote.html templates/restricted_vote_success.html templates/restricted_vote_complete.html templates/restricted_vote_not_authorized.html docs/PARTICIPANT_RESTRICTED_VOTING.md docs/DATABASE_MIGRATION_0.9.1-beta.md
git commit -m "Release 0.9.1-beta add participant-restricted voting and judge access codes"
git push origin main
