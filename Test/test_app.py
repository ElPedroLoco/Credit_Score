import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import os

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

    def test_infos_client_valid_id(self):
        # Mock request with valid id_client
        with self.client:
            response = self.client.get('/infos_client?id_client=100001')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)

    def test_infos_client_invalid_id(self):
        # Mock request with invalid id_client
        with self.client:
            response = self.client.get('/infos_client?id_client=abc')
            data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            
    def test_predict_client_valid_id(self):
        with self.client:
            # Send a GET request to /predict_client with a valid id_client
            response = self.client.get('/predict_client?id_client=100001')
            
            # Verify the response status code
            self.assertEqual(response.status_code, 200)

            # Get the JSON data from the response
            data = response.json

            # Assert that the response is a list
            self.assertIsInstance(data, list)

            # Assert that the first dictionary in the list has 'prediction' key
            self.assertIn('prediction', data[0])

    def test_predict_client_invalid_id(self):
        # Mock request with invalid id_client
        with self.client:
            response = self.client.get('/predict_client?id_client=abc')
            data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
