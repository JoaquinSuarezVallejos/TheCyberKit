import unittest
from flask import Flask, json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.password_tester import evaluate_password

class PasswordTesterApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.route('/evaluate_password', methods=['POST'])(evaluate_password)

class TestPasswordEvaluator(unittest.TestCase):
    def setUp(self):
        self.app = PasswordTesterApp()
        self.client = self.app.test_client()

    def test_evaluate_password_blank_input(self):
        response = self.client.post('/evaluate_password', json={"password": ""})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["score"], "---")
        self.assertEqual(data["crack_time_offline"], "---")
        self.assertEqual(data["crack_time_online_throttled"], "---")
        
    def test_evaluate_password_very_unsafe(self):
        response = self.client.post('/evaluate_password', json={"password": "1234"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn(data["score"], ["1 (very unsafe)"])

    def test_evaluate_password_weak(self):
        response = self.client.post('/evaluate_password', json={"password": "WeakPassword"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn(data["score"], ["2 (weak)"])

    def test_evaluate_password_okay(self):
        response = self.client.post('/evaluate_password', json={"password": "OkayPassword1234"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn(data["score"], ["3 (okay)"])

    def test_evaluate_password_good(self):
        response = self.client.post('/evaluate_password', json={"password": "GoodPassw0rd!"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn(data["score"], ["4 (good)"])
    
    def test_evaluate_password_strong(self):
        response = self.client.post('/evaluate_password', json={"password": "StrongPassw0rd!5891"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn(data["score"], ["5 (strong)"])

if __name__ == '__main__':
    unittest.main()
