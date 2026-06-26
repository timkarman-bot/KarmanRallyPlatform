import os
import tempfile
import unittest


class Release010Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        cls.db_path = os.path.join(cls.temp_dir.name, "release-010.db")
        os.environ["DB_PATH"] = cls.db_path
        os.environ["APP_ENV"] = "testing"
        os.environ["FLASK_SECRET"] = "test-secret"
        os.environ["ADMIN_PASSWORD"] = "test-password"

        import database
        database.DB_PATH = cls.db_path
        database.init_db()

        import app
        cls.database = database
        cls.app_module = app
        cls.app = app.app
        cls.app.config.update(TESTING=True)
        cls.show_counter = 0

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def _show(self, slug=None, voting_mode="participant_only"):
        type(self).show_counter += 1
        slug = slug or f"test-show-{type(self).show_counter}"
        return self.database.create_show_admin(
            slug=slug,
            flyer_image_path="",
            title="Test Show",
            date="2026-07-01",
            time="",
            location_name="Test Lot",
            address="",
            benefiting="Test Charity",
            suggested_donation="",
            description="",
            status="active",
            short_details="",
            qr_message="",
            cta_label="",
            cta_url="",
            show_on_site=1,
            sort_order=1,
            voting_mode=voting_mode,
        )

    def test_restricted_voting_mode_is_preserved(self):
        show_id = self._show()
        row = self.database.get_show_by_id(show_id)
        self.assertEqual(row["voting_mode"], "participant_only")

    def test_contact_center_only_returns_consented_records(self):
        show_id = self._show()
        conn = self.database._conn()
        conn.execute(
            "INSERT INTO people (name, phone, email, opt_in_future, sponsor_opt_in, charity_opt_in) VALUES (?, ?, ?, 1, 0, 1)",
            ("Participant One", "555-0101", "participant@example.com"),
        )
        person_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO show_cars (show_id, person_id, car_number, car_token, year, make, model) VALUES (?, ?, 1, 'car-token-1', '1967', 'Ford', 'Mustang')",
            (show_id, person_id),
        )
        conn.execute(
            "INSERT INTO people (name, phone, email, opt_in_future, sponsor_opt_in, charity_opt_in) VALUES (?, ?, ?, 0, 0, 0)",
            ("No Consent", "555-0102", "private@example.com"),
        )
        private_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO show_cars (show_id, person_id, car_number, car_token, year, make, model) VALUES (?, ?, 2, 'car-token-2', '1970', 'Chevy', 'Nova')",
            (show_id, private_id),
        )
        conn.commit()
        conn.close()

        self.database.create_attendee(
            show_id, "Attendee", "Two", "", "attendee@example.com", "",
            False, False, True, "consent", "2026-06-25",
        )
        contacts = self.database.list_marketing_contacts(show_id)
        names = {row["full_name"] for row in contacts}
        self.assertIn("Participant One", names)
        self.assertIn("Attendee Two", names)
        self.assertNotIn("No Consent", names)

    def test_admin_posts_require_csrf(self):
        client = self.app.test_client()
        response = client.get("/admin")
        self.assertEqual(response.status_code, 200)
        response = client.post("/admin/login", data={"password": "test-password"})
        self.assertEqual(response.status_code, 400)
        with client.session_transaction() as session:
            token = session["_csrf_token"]
        response = client.post(
            "/admin/login",
            data={"password": "test-password", "_csrf_token": token},
        )
        self.assertEqual(response.status_code, 302)

    def test_restricted_voter_type_policy(self):
        self.assertTrue(self.app_module._restricted_voter_allowed({"voting_mode": "participant_only"}, "participant"))
        self.assertFalse(self.app_module._restricted_voter_allowed({"voting_mode": "participant_only"}, "judge"))
        self.assertTrue(self.app_module._restricted_voter_allowed({"voting_mode": "judge_only"}, "judge"))
        self.assertFalse(self.app_module._restricted_voter_allowed({"voting_mode": "judge_only"}, "participant"))

    def test_registration_persists_all_three_permissions(self):
        show_id = self._show(slug="registration-consent-show", voting_mode="none")
        self.database.set_active_show(show_id)
        conn = self.database._conn()
        conn.execute(
            "UPDATE shows SET waiver_text = ?, waiver_version = ?, registration_fee_cents = 0 WHERE id = ?",
            ("Test waiver text", "test-1", show_id),
        )
        conn.commit()
        conn.close()

        client = self.app.test_client()
        response = client.post(
            "/register/registration-consent-show",
            data={
                "name": "Consent Owner",
                "phone": "555-0100",
                "email": "owner@example.com",
                "year": "1967",
                "make": "Ford",
                "model": "Mustang",
                "opt_in_future": "on",
                "sponsor_opt_in": "on",
                "charity_opt_in": "on",
                "waiver_signed_name": "Consent Owner",
                "waiver_accepted": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        contacts = self.database.list_marketing_contacts(show_id)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]["event_opt_in"], 1)
        self.assertEqual(contacts[0]["sponsor_opt_in"], 1)
        self.assertEqual(contacts[0]["charity_opt_in"], 1)


if __name__ == "__main__":
    unittest.main()
