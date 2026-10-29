import unittest

from app import app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Maternal Health Risk Prediction", response.data)

    def test_valid_prediction(self):
        response = self.client.post(
            "/",
            data={
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

    def test_missing_value(self):
        response = self.client.post(
            "/",
            data={
                "Age": "25",
                "SystolicBP": "130",
                "DiastolicBP": "80",
                "BS": "15.0",
                "BodyTemp": "98.0",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a valid number", response.data)


if __name__ == "__main__":
    unittest.main()