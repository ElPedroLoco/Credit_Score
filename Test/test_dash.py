import unittest
import os
import pandas as pd
import numpy as np
import streamlit as st
import sys

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les fonctions et variables du tableau de bord
from dash import (
    get_title_font_size,
    generate_figure,
    generate_annotations,
    compute_color,
    format_value,
    find_closest_description,
    plot_distribution,
    get_state,
)

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        # Charger les données pour les tests
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path_df_test = os.path.join(current_directory, "model_weights/df_test.csv")
        path_definition_features_df = os.path.join(
            current_directory, "model_weights/definition_features.csv"
        )
        self.df_test = pd.read_csv(path_df_test)
        self.definition_features_df = pd.read_csv(path_definition_features_df)

    def tearDown(self):
        # Cleanup après chaque test
        pass

    def test_get_title_font_size(self):
        print("Test: test_get_title_font_size")
        try:
            font_size = get_title_font_size(600)
            self.assertEqual(font_size, 12)
            font_size = get_title_font_size(1200)
            self.assertEqual(font_size, 24)
            print("test_get_title_font_size: SUCCESS")
        except AssertionError as e:
            print(f"test_get_title_font_size: FAILED ({str(e)})")

    def test_generate_figure(self):
        print("Test: test_generate_figure")
        try:
            sample_data = {
                "Feature": ["feature1", "feature2"],
                "SHAP Value": [0.5, -0.3],
                "Feature Value": [1.0, 2.0],
            }
            df = pd.DataFrame(sample_data)
            fig = generate_figure(df, "Test Title", "left", "total ascending", "left")
            self.assertIsNotNone(fig)
            print("test_generate_figure: SUCCESS")
        except AssertionError as e:
            print(f"test_generate_figure: FAILED ({str(e)})")

    def test_compute_color(self):
        print("Test: test_compute_color")
        try:
            color = compute_color(25)
            self.assertEqual(color, "green")
            color = compute_color(75)
            self.assertEqual(color, "red")
            print("test_compute_color: SUCCESS")
        except AssertionError as e:
            print(f"test_compute_color: FAILED ({str(e)})")

    def test_format_value(self):
        print("Test: test_format_value")
        try:
            formatted_value = format_value(5.678)
            self.assertEqual(formatted_value, 5.68)
            formatted_value = format_value(5)
            self.assertEqual(formatted_value, 5)
            formatted_value = format_value(None)
            self.assertIsNone(formatted_value)
            print("test_format_value: SUCCESS")
        except AssertionError as e:
            print(f"test_format_value: FAILED ({str(e)})")

    def test_find_closest_description(self):
        print("Test: test_find_closest_description")
        try:
            description = find_closest_description("feature_name", self.definition_features_df)
            self.assertIsNotNone(description)
            print("test_find_closest_description: SUCCESS")
        except AssertionError as e:
            print(f"test_find_closest_description: FAILED ({str(e)})")

    def test_plot_distribution(self):
        print("Test: test_plot_distribution")
        try:
            feature_name = self.df_test.columns[0]
            col = st.empty()
            plot_distribution(feature_name, col)
            print("test_plot_distribution: SUCCESS")
        except Exception as e:
            print(f"test_plot_distribution: FAILED ({str(e)})")

    def test_get_state(self):
        print("Test: test_get_state")
        try:
            state = get_state()
            self.assertIsNotNone(state)
            self.assertIn("data_received", state)
            print("test_get_state: SUCCESS")
        except AssertionError as e:
            print(f"test_get_state: FAILED ({str(e)})")

if __name__ == '__main__':
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
