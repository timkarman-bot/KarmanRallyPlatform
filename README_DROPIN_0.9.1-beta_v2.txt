Release 0.9.1-beta v2 - Admin Form Cleanup and Simple Participant Judging

Drop-in file:
- templates/admin_show_detail.html

What changed:
1. Registration day/session section now defaults to one visible row.
2. Additional days/sessions are hidden until the admin clicks "Add another day/session".
3. Placeholder text is generic instead of example-specific.
4. Participant/Judge voting section now explains that participant voters are created automatically from car registrations when the participant scans the voting access QR on the back of the windshield card.
5. Removed duplicate judge-code form tag.

Business rule:
- For participant-only judging, registered car participants do not need to be imported manually as judges.
- Their registration already provides the owner/car record.
- Their voting access is granted by scanning their own voting access QR.
- Manual judge codes are only for outside judges, staff judges, or special voting groups.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add templates/admin_show_detail.html README_DROPIN_0.9.1-beta_v2.txt
git commit -m "Release 0.9.1-beta clean up registration sessions and participant judge access"
git push origin main
