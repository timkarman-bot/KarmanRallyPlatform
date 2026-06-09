Windscreen Card Customization Drop-In
====================================

Replace these files in your project:

1. app.py
2. database.py
3. templates/admin_shows.html
4. utils/print_cards.py

What this adds
--------------
- Per-show windshield card headline
- Per-show windshield card subheadline
- Per-show card layout mode:
  - Auto
  - Voting
  - Information
  - Sponsor / thank-you
- Automatic info-card layout when voting is disabled or the show is a cruise-in
- Uses existing show fields for QR content:
  - cta_url = QR destination
  - cta_label = QR label
  - qr_message = main card message

After replacing files
---------------------
Run:

python -m py_compile app.py database.py utils/print_cards.py

Then deploy normally.

Important
---------
The database columns are added automatically by init_db() using ALTER TABLE statements. No manual SQL migration should be required.

Recommended settings for a church cruise-in
-------------------------------------------
Show Type: Cruise In
Voting Mode: None — voting disabled
Voting Payment Mode: None — no vote payment
Card Layout Mode: Information card or Auto
Card Headline: WELCOME
Card Subheadline: Journey Church Cruise-In
CTA Label: More information
CTA URL: church website
QR Message: Scan for church information, event details, and updates.
