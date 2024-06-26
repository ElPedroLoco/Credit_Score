import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestApp(unittest.TestCase):

    @patch('app.pd.read_csv')
    def setUp(self, mock_read_csv):
        # Mock dataset
        self.mock_data = MagicMock()
        self.mock_data.empty = False  # Ensure mock data is not empty
        mock_read_csv.return_value = self.mock_data

        # Create a test client
        self.client = app.test_client()
        print("Test Setup completed.")

    def test_infos_client_valid_id(self):
        with self.client:
            try:
                print("Testing /infos_client with valid id_client...")
                response = self.client.get('/infos_client?id_client=100001')
                data = response.get_json()
                self.assertEqual(response.status_code, 200)
                self.assertIn('data', data)
                print("/infos_client test passed with valid id_client.")
            except Exception as e:
                print(f"Error in test_infos_client_valid_id: {e}")
                raise

    def test_infos_client_invalid_id(self):
        with self.client:
            try:
                print("Testing /infos_client with invalid id_client...")
                response = self.client.get('/infos_client?id_client=abc')
                data = response.get_json()
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', data)
                print("/infos_client test passed with invalid id_client.")
            except Exception as e:
                print(f"Error in test_infos_client_invalid_id: {e}")
                raise

    def test_predict_client_valid_id(self):
        with self.client:
            try:
                print("Testing /predict_client with valid id_client...")
                response = self.client.get('/predict_client?id_client=100001')
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIsInstance(data, list)
                self.assertIn('prediction', data[0])
                print("/predict_client test passed with valid id_client.")
            except Exception as e:
                print(f"Error in test_predict_client_valid_id: {e}")
                raise

    def test_predict_client_invalid_id(self):
        with self.client:
            try:
                print("Testing /predict_client with invalid id_client...")
                response = self.client.get('/predict_client?id_client=abc')
                data = response.get_json()
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', data)
                print("/predict_client test passed with invalid id_client.")
            except Exception as e:
                print(f"Error in test_predict_client_invalid_id: {e}")
                raise

    def test_home_page(self):
        with self.client:
            try:
                print("Testing home page / ...")
                response = self.client.get('/')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Credit Score', response.data)
                print("Home page test passed.")
            except Exception as e:
                print(f"Error in test_home_page: {e}")
                raise

    def test_404_page(self):
        with self.client:
            try:
                print("Testing 404 page ...")
                response = self.client.get('/nonexistentpage')
                self.assertEqual(response.status_code, 404)
                print("404 page test passed.")
            except Exception as e:
                print(f"Error in test_404_page: {e}")
                raise

if __name__ == '__main__':
    unittest.main()
