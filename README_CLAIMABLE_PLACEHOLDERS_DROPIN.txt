Karman Kar Shows — Claimable Placeholder + Auto Class Drop-in

FILES INCLUDED
- app.py
- database.py
- templates/admin_shows.html
- templates/admin_placeholders.html
- utils/print_cards.py

WHAT THIS PATCH DOES
1. Treats placeholder/windscreen cards as open inventory.
   - Pre-registered cars keep their assigned numbers.
   - Missing numbers up to Max Cars can be created as open placeholders.
   - Open cards can be shuffled and handed out at multiple registration lines.

2. Adds a new admin button on Placeholder Cars:
   - “Create missing open placeholders up to Max Cars”
   - Example: Max Cars = 100, pre-registered cars #1-#4 already exist, button creates open placeholders #5-#100.

3. Changes day-of placeholder claim behavior.
   - Staff collects payment first.
   - Owner receives windscreen card.
   - Owner scans back QR and enters owner/vehicle/waiver info.
   - The system does NOT send them to online checkout.
   - The system marks payment as paid_cash.

4. Adds judging classes and simple auto-class assignment.
   - Manage Shows now has an Advanced Judging Classes / Auto Class Rules section.
   - Rules can use year range, make contains, model contains, and award places.
   - If exactly one class matches the entered vehicle, it assigns the class.
   - If no class or multiple classes match, the car is flagged “Needs review.”

5. Updates windshield card printing.
   - Front card shows Class field.
   - Empty/open placeholders have write-in lines.
   - Back card says payment was already collected at the booth.

LOCAL TEST STEPS
1. Stop Flask with CTRL+C.
2. Replace the files.
3. Run:
   python -m py_compile app.py database.py utils/print_cards.py
4. Run:
   python app.py
5. Open:
   http://127.0.0.1:8080/admin/shows
6. Set Max Cars on the active show.
7. Add at least one judging class rule, example:
   Class Name: British Sports Cars
   Make contains: MG, Triumph, Austin-Healey, Jaguar
   Award places: 3
8. Save the show.
9. Go to Admin > Placeholder Cars.
10. Click “Create missing open placeholders up to Max Cars.”
11. Print OPEN day-of cards with backs.
12. Scan/open the claim link for one open card and enter vehicle info.
13. Confirm it does not ask for payment and the car becomes paid_cash.
14. Confirm class is assigned or marked Needs review.

DO NOT COMMIT
- instance/
- app.db
- local waiver files
- __pycache__/

IMPORTANT
This patch creates the foundation for class-based judging, but final results/report screens by class are still the next feature layer.
