Karman Kar Shows & Events - Admin Edit Registration Drop-In

Copy these files into your project:

1) app.py -> C:\karman-kar-shows\app.py
2) database.py -> C:\karman-kar-shows\database.py
3) admin_car_search.html -> C:\karman-kar-shows\templates\admin_car_search.html
4) admin_show_mode.html -> C:\karman-kar-shows\templates\admin_show_mode.html
5) admin_registration_edit.html -> C:\karman-kar-shows\templates\admin_registration_edit.html

Then run:

python -m py_compile app.py database.py
python app.py

Test:
- Go to /admin/car-search
- Search a car
- Click Edit
- Save a small change
- Verify the change shows in Car Search and Show Mode

Notes:
- This does not charge money, issue refunds, or change Stripe.
- Payment status changes are admin-only status labels.
- Day/session editing respects the show's single vs multiple selection mode.
