import unittest
from app import app

class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        # Create test client
        self.client = app.test_client()
        self.client.testing = True

    def test_success(self):
        response = self.client.get("/weather?city=Delhi")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn("city", data)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)

    def test_missing_city(self):
        response = self.client.get("/weather")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "City parameter is required")

    def test_multiple_success(self):
        response = self.client.post(
            "/weather/many",
            json={"cities": ["Delhi", "Mumbai"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_multiple_empty(self):
        response = self.client.post(
            "/weather/many",
            json={}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Cities list required")

    def test_invalid_city(self):
        response = self.client.get("/weather?city=InvalidCity123")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()