import unittest
import json
from app import app  # Import the Flask app to be tested

class TestApp(unittest.TestCase):
    
    def setUp(self):
        # Setup method to create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        # Test for the default route "/"
        response = self.app.get('/')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response data matches the expected "Hello World!" message
        self.assertEqual(response.data.decode('utf-8'), 'Hello World!')

    def test_infos_client(self):
        # Test for the "/infos_client" endpoint
        response = self.app.get('/infos_client?id_client=1001')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response data contains the expected fields for client information
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue("status_famille" in data)
        self.assertTrue("nb_enfant" in data)
        # Add more assertions for other fields as needed

    def test_predict_client(self):
        # Test for the "/predict_client" endpoint
        response = self.app.get('/predict_client?id_client=1001')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response data contains the expected fields for prediction
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue("prediction" in data)
        self.assertTrue("prediction_proba" in data)
        # Add more assertions for other fields as needed

    def test_predict(self):
        # Test for the "/predict" endpoint
        # Prepare test data for prediction
        test_data = {
            "SK_ID_CURR": 1001,
            "NAME_FAMILY_STATUS": "Married",
            "CNT_CHILDREN": 1,
            "DAYS_BIRTH": -15000,
            # Add other necessary fields
        }
        # Make a POST request to the endpoint with test data
        response = self.app.post('/predict', json=test_data)
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response data contains the expected fields for prediction
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue("prediction" in data)
        self.assertTrue("prediction_proba" in data)
        # Add more assertions for other fields as needed

if __name__ == '__main__':
    unittest.main()
