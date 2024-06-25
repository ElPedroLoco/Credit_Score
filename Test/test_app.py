import unittest
from unittest.mock import patch, MagicMock
import os
from app import app  # Assuming your Flask app instance is named 'app'

# Adjust the path to include the parent directory
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
        # Mock request with valid id_client
        with self.client:
            response = self.client.get('/predict_client?id_client=100001')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn('prediction', data)

    def test_predict_client_invalid_id(self):
        # Mock request with invalid id_client
        with self.client:
            response = self.client.get('/predict_client?id_client=abc')
            data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()


# import unittest
# import json
# import sys
# import os

# # Adjust the path to include the parent directory
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import app  # Import the app from the dashboard module
# class TestApp(unittest.TestCase):
    
#     def setUp(self):
#         # Setup method to create a test client for the Flask app
#         self.app = app.test_client()
#         self.app.testing = True

#     def test_hello(self):
#         # Test for the default route "/"
#         response = self.app.get('/')
#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#         # Check if the response data matches the expected "Hello World!" message
#         self.assertEqual(response.data.decode('utf-8'), 'Hello World!')

#     def test_infos_client(self):
#         # Test for the "/infos_client" endpoint
#         response = self.app.get('/infos_client?id_client=100001')
#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#         # Check if the response data contains the expected fields for client information
#         data = json.loads(response.data.decode('utf-8'))
#         self.assertTrue("status_famille" in data)
#         self.assertTrue("nb_enfant" in data)
#         # Add more assertions for other fields as needed

#     def test_predict_client(self):
#         # Test for the "/predict_client" endpoint
#         response = self.app.get('/predict_client?id_client=100001')
#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#         # Check if the response data contains the expected fields for prediction
#         data = json.loads(response.data.decode('utf-8'))
#         self.assertTrue("prediction" in data)
#         self.assertTrue("prediction_proba" in data)

#     def test_predict(self):
#         # Test for the "/predict" endpoint
#         # Prepare test data for prediction
#         test_data = {
#             "SK_ID_CURR": 100001,
#         }
#         # Make a POST request to the endpoint with test data
#         response = self.app.post('/predict', json=test_data)
#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#         # Check if the response data contains the expected fields for prediction
#         data = json.loads(response.data.decode('utf-8'))
#         self.assertTrue("prediction" in data)
#         self.assertTrue("prediction_proba" in data)

# if __name__ == '__main__':
#     unittest.main()
