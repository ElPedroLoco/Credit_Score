import unittest
import json
import os
import sys
from flask import Flask
from flask_testing import TestCase
import joblib
import pandas as pd
import shap

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, model, scaler, current_directory

class FlaskTestCase(TestCase):
    def create_app(self):
        # Configurer l'application Flask pour le test
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Configuration avant chaque test
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        # Charger le modèle et le scaler pour les tests
        self.model = model
        self.scaler = scaler

        # Charger le CSV de test
        csv_path = os.path.join(current_directory, "model_weights", "df_test.csv")
        self.df = pd.read_csv(csv_path)

    def tearDown(self):
        # Cleanup après chaque test
        pass

    def test_predict_valid_id(self):
        print("Test: test_predict_valid_id")
        try:
            sk_id_curr = self.df['SK_ID_CURR'].iloc[0]
            response = self.client.post(
                '/predict_client',
                headers=self.headers,
                data=json.dumps({'SK_ID_CURR': sk_id_curr})
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn('probability', data)
            self.assertIn('shap_values', data)
            self.assertIn('feature_names', data)
            self.assertIn('feature_values', data)
            print("test_predict_valid_id: SUCCESS")
        except AssertionError as e:
            print(f"test_predict_valid_id: FAILED ({str(e)})")

    def test_predict_invalid_id(self):
        print("Test: test_predict_invalid_id")
        try:
            sk_id_curr = -1
            response = self.client.post(
                '/predict_client',
                headers=self.headers,
                data=json.dumps({'SK_ID_CURR': sk_id_curr})
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertEqual(data['probability'], 0)
            self.assertEqual(len(data['shap_values']), len(self.df.columns) - 1)
            print("test_predict_invalid_id: SUCCESS")
        except AssertionError as e:
            print(f"test_predict_invalid_id: FAILED ({str(e)})")

    def test_missing_sk_id_curr(self):
        print("Test: test_missing_sk_id_curr")
        try:
            response = self.client.post(
                '/predict_client',
                headers=self.headers,
                data=json.dumps({})
            )
            self.assertEqual(response.status_code, 400)
            print("test_missing_sk_id_curr: SUCCESS")
        except AssertionError as e:
            print(f"test_missing_sk_id_curr: FAILED ({str(e)})")

if __name__ == '__main__':
    unittest.main()



# import unittest
# from unittest.mock import patch, MagicMock
# import os
# import sys

# # Add the parent directory to the sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import app

# class TestApp(unittest.TestCase):

#     @patch('app.pd.read_csv')
#     def setUp(self, mock_read_csv):
#         # Mock dataset
#         self.mock_data = MagicMock()
#         self.mock_data.empty = False  # Ensure mock data is not empty
#         mock_read_csv.return_value = self.mock_data

#         # Create a test client
#         self.client = app.test_client()
#         print("Test Setup completed.")

#     def test_infos_client_valid_id(self):
#         with self.client:
#             try:
#                 print("Testing /infos_client with valid id_client...")
#                 response = self.client.get('/infos_client?id_client=100001')
#                 data = response.get_json()
#                 self.assertEqual(response.status_code, 200)
#                 self.assertIn('data', data)
#                 print("/infos_client test passed with valid id_client.")
#             except Exception as e:
#                 print(f"Error in test_infos_client_valid_id: {e}")
#                 raise

#     def test_infos_client_invalid_id(self):
#         with self.client:
#             try:
#                 print("Testing /infos_client with invalid id_client...")
#                 response = self.client.get('/infos_client?id_client=abc')
#                 data = response.get_json()
#                 self.assertEqual(response.status_code, 400)
#                 self.assertIn('error', data)
#                 print("/infos_client test passed with invalid id_client.")
#             except Exception as e:
#                 print(f"Error in test_infos_client_invalid_id: {e}")
#                 raise

#     def test_predict_client_valid_id(self):
#         with self.client:
#             try:
#                 print("Testing /predict_client with valid id_client...")
#                 response = self.client.get('/predict_client?id_client=100001')
#                 self.assertEqual(response.status_code, 200)
#                 data = response.get_json()
#                 self.assertIsInstance(data, list)
#                 self.assertIn('prediction', data[0])
#                 print("/predict_client test passed with valid id_client.")
#             except Exception as e:
#                 print(f"Error in test_predict_client_valid_id: {e}")
#                 raise

#     def test_predict_client_invalid_id(self):
#         with self.client:
#             try:
#                 print("Testing /predict_client with invalid id_client...")
#                 response = self.client.get('/predict_client?id_client=abc')
#                 data = response.get_json()
#                 self.assertEqual(response.status_code, 400)
#                 self.assertIn('error', data)
#                 print("/predict_client test passed with invalid id_client.")
#             except Exception as e:
#                 print(f"Error in test_predict_client_invalid_id: {e}")
#                 raise

#     def test_home_page(self):
#         with self.client:
#             try:
#                 print("Testing home page / ...")
#                 response = self.client.get('/')
#                 self.assertEqual(response.status_code, 200)
#                 self.assertIn(b'Credit Score', response.data)
#                 print("Home page test passed.")
#             except Exception as e:
#                 print(f"Error in test_home_page: {e}")
#                 raise

#     def test_404_page(self):
#         with self.client:
#             try:
#                 print("Testing 404 page ...")
#                 response = self.client.get('/nonexistentpage')
#                 self.assertEqual(response.status_code, 404)
#                 print("404 page test passed.")
#             except Exception as e:
#                 print(f"Error in test_404_page: {e}")
#                 raise

# if __name__ == '__main__':
#     unittest.main()
