import unittest
import os
import pandas as pd
import numpy as np
import streamlit as st
import sys

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import dash

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_predict_valid_id(self):
        print("Test: test_predict_valid_id")
        try:
            valid_id = 156003  
            response = self.app.post('/predict_client', json={'SK_ID_CURR': valid_id})
            self.assertEqual(response.status_code, 200)
            data = response.json
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
            invalid_id = 999999  
            response = self.app.post('/predict_client', json={'SK_ID_CURR': invalid_id})
            self.assertEqual(response.status_code, 404)
            data = response.json
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'ID not found')
            print("test_predict_invalid_id: SUCCESS")
        except AssertionError as e:
            print(f"test_predict_invalid_id: FAILED ({str(e)})")

if __name__ == "__main__":
    unittest.main()


# import unittest
# from unittest.mock import patch, MagicMock
# import pandas as pd
# import sys
# import os
# import importlib

# # Add the parent directory to the sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Import the module only once to apply patches correctly
# import dash

# class TestDashApp(unittest.TestCase):

#     @patch('dash.st.sidebar.multiselect')
#     @patch('dash.st.dataframe')
#     @patch('dash.pd.read_csv')
#     def test_filter_data(self, mock_read_csv, mock_dataframe, mock_multiselect):
#         print("Starting test_filter_data")
#         try:
#             # Mocking the data
#             data = {
#                 'NAME_CONTRACT_TYPE': ['Cash loans', 'Revolving loans'],
#                 'CODE_GENDER': ['M', 'F'],
#                 'NAME_FAMILY_STATUS': ['Married', 'Single'],
#                 'NAME_HOUSING_TYPE': ['House / apartment', 'Rented apartment'],
#                 'CNT_CHILDREN': [0, 1],
#                 'DAYS_BIRTH': [-10000, -12000],
#                 'Prediction : 1': [0.1, 0.2]
#             }
#             df = pd.DataFrame(data)
#             mock_read_csv.return_value = df

#             # Mocking user input
#             mock_multiselect.side_effect = [
#                 ['Cash loans'],  # contract_type
#                 ['M'],           # sexe
#                 ['Married'],     # civil_status
#                 ['House / apartment'],  # habitation_type
#                 [0]              # nombre_enfants
#             ]

#             # Patching Streamlit functions
#             dash.st.set_page_config = MagicMock()
#             dash.st.title = MagicMock()
#             dash.st.markdown = MagicMock()
#             dash.st.subheader = MagicMock()
#             dash.st.plotly_chart = MagicMock()

#             # Re-execute the code within the dash module with mocks in place
#             importlib.reload(dash)

#             # Assertions to ensure that the DataFrame is filtered correctly
#             filtered_df = dash.df_selection
#             self.assertEqual(filtered_df.shape[0], 1)
#             self.assertEqual(filtered_df.iloc[0]['NAME_CONTRACT_TYPE'], 'Cash loans')
#             self.assertEqual(filtered_df.iloc[0]['CODE_GENDER'], 'M')
#             self.assertEqual(filtered_df.iloc[0]['NAME_FAMILY_STATUS'], 'Married')
#             self.assertEqual(filtered_df.iloc[0]['NAME_HOUSING_TYPE'], 'House / apartment')
#             self.assertEqual(filtered_df.iloc[0]['CNT_CHILDREN'], 0)

#             print("Assertions passed for test_filter_data")

#         except Exception as e:
#             print(f"Error in test_filter_data: {e}")
#             raise

#     @patch('dash.st.text_input')
#     @patch('dash.requests.get')
#     def test_api_calls(self, mock_get, mock_text_input):
#         print("Starting test_api_calls")
#         try:
#             # Mocking user input
#             mock_text_input.side_effect = ['123', '456']

#             # Mocking the API response
#             mock_response = MagicMock()
#             mock_response.status_code = 200
#             mock_response.json.return_value = {'info': 'some client info'}
#             mock_get.return_value = mock_response

#             # Mocking Streamlit write function
#             dash.st.write = MagicMock()

#             # Re-execute the code within the dash module with mocks in place
#             importlib.reload(dash)

#             # Assertions to ensure that the API call is made correctly
#             dash.requests.get.assert_any_call('http://ec2-35-181-155-27.eu-west-3.compute.amazonaws.com:5000/infos_client?id_client=123')
#             dash.requests.get.assert_any_call('http://ec2-35-181-155-27.eu-west-3.compute.amazonaws.com:5000/predict_client?id_client=456')
#             dash.st.write.assert_called_with({'info': 'some client info'})

#             print("Assertions passed for test_api_calls")

#         except Exception as e:
#             print(f"Error in test_api_calls: {e}")
#             raise

#     @patch('dash.st.sidebar.multiselect')
#     @patch('dash.pd.read_csv')
#     def test_statistics_calculation(self, mock_read_csv, mock_multiselect):
#         print("Starting test_statistics_calculation")
#         try:
#             # Mocking the data
#             data = {
#                 'NAME_CONTRACT_TYPE': ['Cash loans', 'Revolving loans'],
#                 'CODE_GENDER': ['M', 'F'],
#                 'NAME_FAMILY_STATUS': ['Married', 'Single'],
#                 'NAME_HOUSING_TYPE': ['House / apartment', 'Rented apartment'],
#                 'CNT_CHILDREN': [0, 1],
#                 'DAYS_BIRTH': [-10000, -12000],
#                 'Prediction : 1': [0.1, 0.2]
#             }
#             df = pd.DataFrame(data)
#             mock_read_csv.return_value = df

#             # Mocking user input
#             mock_multiselect.side_effect = [
#                 ['Cash loans', 'Revolving loans'],  # contract_type
#                 ['M', 'F'],           # sexe
#                 ['Married', 'Single'],     # civil_status
#                 ['House / apartment', 'Rented apartment'],  # habitation_type
#                 [0, 1]              # nombre_enfants
#             ]

#             # Patching Streamlit functions
#             dash.st.set_page_config = MagicMock()
#             dash.st.title = MagicMock()
#             dash.st.markdown = MagicMock()
#             dash.st.subheader = MagicMock()
#             dash.st.plotly_chart = MagicMock()

#             # Re-execute the code within the dash module with mocks in place
#             importlib.reload(dash)

#             # Assertions to ensure that statistics are calculated correctly
#             self.assertEqual(dash.nombre_clients, 2)
#             self.assertAlmostEqual(dash.average_age, 30.1)
#             self.assertAlmostEqual(dash.average_prediction, 15.0)

#             print("Assertions passed for test_statistics_calculation")

#         except Exception as e:
#             print(f"Error in test_statistics_calculation: {e}")
#             raise

# if __name__ == '__main__':
#     unittest.main()
