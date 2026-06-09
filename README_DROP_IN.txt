Karman Kar Shows & Events — Multi-Day / Multi-Session Registration Drop-In

Files included:
- app.py
- database.py
- templates/register.html
- templates/placeholder_claim.html
- templates/admin.html
- templates/admin_shows.html
- templates/admin_car_search.html
- templates/checkin.html

What this adds:
1. Keeps existing one-day-only behavior as the default.
2. Adds a show setting named registration_slot_selection_mode:
   - single = radio buttons / one day-session only
   - multiple = checkboxes / allow several day-session-activity selections
3. Adds a join table show_car_registration_slots so one car can be attached to multiple days/sessions/activities.
4. Keeps the old show_cars.registration_slot_id field for backward compatibility.
5. Adds registration_slot_ids JSON storage to registration_intents so pending/paid registrations preserve all selected sessions.
6. Updates public registration and placeholder claim pages to switch between radio buttons and checkboxes automatically.
7. Updates admin search/check-in display to show selected day(s)/session(s).

Install:
1. Back up your current project first.
2. Copy these files into the matching locations in your project root.
3. Run the app once. database.init_db() will add the new columns/table automatically.
4. Go to Admin > active show settings or Manage Shows.
5. For Journey Church, set Day/Session Selection to "Multiple allowed — checkboxes".
6. Add slots such as:
   - Saturday Cruise-In
   - Sunday Father’s Day Display
   - Tech Session
   - Road Drive

Notes:
- Existing shows remain single-select unless changed.
- Capacity is checked per selected slot.
- Existing registrations using the old one-slot field still show correctly.
