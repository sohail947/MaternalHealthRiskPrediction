import os
import sqlite3
import tempfile
import unittest
from contextlib import closing

from app import app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        database_file = tempfile.NamedTemporaryFile(delete=False)
        database_file.close()
        app.config["DATABASE"] = database_file.name
        self.addCleanup(os.unlink, database_file.name)
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Maternal Health Risk Prediction", response.data)
        self.assertIn(b"Total Patients", response.data)
        self.assertIn(b"Patient Records", response.data)

    def test_valid_prediction(self):
        response = self.client.post(
            "/",
            data={
                "patient_name": "Test Patient",
                "Age": "25",
                "SystolicBP": "130",
                "DiastolicBP": "80",
                "BS": "15.0",
                "BodyTemp": "98.0",
                "HeartRate": "86",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Predicted risk:", response.data)
        self.assertIn(b"Test Patient", response.data)
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM patient_records"
            ).fetchone()[0]
        self.assertEqual(count, 1)

    def test_search_and_delete_patient(self):
        self.client.post(
            "/",
            data={
                "patient_name": "Searchable Patient",
                "Age": "25",
                "SystolicBP": "130",
                "DiastolicBP": "80",
                "BS": "15.0",
                "BodyTemp": "98.0",
                "HeartRate": "86",
            },
        )

        response = self.client.get("/?patient_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Searchable Patient", response.data)

        response = self.client.post(
            "/patients/1/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient record 1 was deleted.", response.data)
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM patient_records"
            ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_dashboard_shows_risk_statistics(self):
        self.client.get("/")
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            with connection:
                connection.executemany(
                    """
                    INSERT INTO patient_records (
                        patient_name, Age, SystolicBP, DiastolicBP,
                        BS, BodyTemp, HeartRate, risk_level
                    )
                    VALUES (?, 25, 120, 80, 7.5, 98, 76, ?)
                    """,
                    [
                        ("Low Patient", "low risk"),
                        ("Medium Patient", "mid risk"),
                        ("High Patient", "high risk"),
                    ],
                )

        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertRegex(page, r"<p>Total Patients</p>\s*<strong>3</strong>")
        self.assertRegex(page, r"<p>Low Risk</p>\s*<strong>1</strong>")
        self.assertRegex(page, r"<p>Medium Risk</p>\s*<strong>1</strong>")
        self.assertRegex(page, r"<p>High Risk</p>\s*<strong>1</strong>")

    def test_missing_value(self):
        response = self.client.post(
            "/",
            data={
                "patient_name": "Incomplete Patient",
                "Age": "25",
                "SystolicBP": "130",
                "DiastolicBP": "80",
                "BS": "15.0",
                "BodyTemp": "98.0",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a valid number", response.data)
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM patient_records"
            ).fetchone()[0]
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()