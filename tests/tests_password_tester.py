# UNIT TESTS FOR THE PASSWORD TESTER (Python file)

import unittest
from flask import Flask, json
import sys
import os

# Add parent directory to system path for importing password tester module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.password_tester import (
    evaluate_password,
)  # Import password evaluation function


# Define a custom Flask application to test password evaluation
class PasswordTesterApp(Flask):
    def __init__(self):
        super().__init__(__name__)  # Initialize Flask application
        # Add a route to handle POST requests for password evaluation
        self.route("/evaluate_password", methods=["POST"])(evaluate_password)


# Define test cases for the password evaluator
class TestPasswordEvaluator(unittest.TestCase):
    # Set up a test client for the Flask app before each test
    def setUp(self):
        self.app = PasswordTesterApp()
        self.client = self.app.test_client()

    # Test evaluation of a blank password input
    def test_evaluate_password_blank_input(self):
        response = self.client.post("/evaluate_password", json={"password": ""})
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        # Expect blank scores for a blank input
        self.assertEqual(data["score"], "---")
        self.assertEqual(data["crack_time_offline"], "---")
        self.assertEqual(data["crack_time_online_throttled"], "---")

    # Test evaluation of a very unsafe password
    def test_evaluate_password_very_unsafe(self):
        response = self.client.post("/evaluate_password", json={"password": "1234"})
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        self.assertIn(data["score"], ["1 (very unsafe)"])  # Expect low safety score

    # Test evaluation of a weak password
    def test_evaluate_password_weak(self):
        response = self.client.post(
            "/evaluate_password", json={"password": "WeakPassword"}
        )
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        self.assertIn(data["score"], ["2 (weak)"])  # Expect weak score

    # Test evaluation of an okay-strength password
    def test_evaluate_password_okay(self):
        response = self.client.post(
            "/evaluate_password", json={"password": "OkayPassword1234"}
        )
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        self.assertIn(data["score"], ["3 (okay)"])  # Expect okay score

    # Test evaluation of a good password
    def test_evaluate_password_good(self):
        response = self.client.post(
            "/evaluate_password", json={"password": "GoodPassw0rd!"}
        )
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        self.assertIn(data["score"], ["4 (good)"])  # Expect good score

    # Test evaluation of a strong password
    def test_evaluate_password_strong(self):
        response = self.client.post(
            "/evaluate_password", json={"password": "StrongPassw0rd!5891"}
        )
        self.assertEqual(response.status_code, 200)  # Check for successful response
        data = json.loads(response.data)
        self.assertIn(data["score"], ["5 (strong)"])  # Expect strong score


# Run the unit tests
if __name__ == "__main__":
    unittest.main()