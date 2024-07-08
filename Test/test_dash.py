import pytest
from unittest.mock import patch, Mock
import os
import sys

# Obtenir le répertoire du fichier actuel 
current_file_directory = os.path.dirname(__file__)

# Créer un chemin relatif vers le dossier contenant dash
scripts_directory = os.path.abspath(os.path.join(current_file_directory, '..'))

# Insérer ce chemin au début de sys.path
sys.path.insert(0, scripts_directory)

# Simulation d'un état pour st.session_state
mocked_session_state = {'state': {'data_received': False, 'data': None, 'last_sk_id_curr': None}}

# Définir le décorateur pytest pour simuler st.session_state
@pytest.fixture
def mocked_st(monkeypatch):
    # Utilisez monkeypatch pour remplacer l'attribut session_state de streamlit par notre état simulé
    monkeypatch.setattr("streamlit.session_state", mocked_session_state)
    return mocked_session_state


#TESTS

# Utilise pytest.mark pour appliquer le mock à des tests spécifiques
@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_compute_color(mocked_st):
    # Importez la fonction compute_color à partir du module dashboard
    from dashboard import compute_color
    # Teste la fonction compute_color pour différentes valeurs
    assert compute_color(30) == "green", "Erreur dans la fonction compute_color."
    assert compute_color(50) == "red", "Erreur dans la fonction compute_color."

@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_format_value(mocked_st):
    # Importez la fonction format_value à partir du module dashboard
    from dashboard import format_value
    # Teste la fonction format_value pour différentes valeurs
    assert format_value(5.67) == 5.67, "Erreur dans la fonction format_value."
    assert format_value(5.00) == 5, "Erreur dans la fonction format_value."

@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_find_closest_description(mocked_st):
    # Importez les fonctions find_closest_description et definition_features_df à partir du module dashboard
    from dashboard import find_closest_description, definition_features_df
    # Teste la fonction pour trouver la description la plus proche d'un terme donné
    description = find_closest_description("AMT_INCOME_TOTAL", definition_features_df)
    assert description is not None, "Erreur dans la fonction find_closest_description."

def test_get_state(mocked_st):	
    # Importez la fonction get_state à partir du module dashboard
    from dashboard import get_state
    state = get_state()
    assert isinstance(state, dict), "La fonction get_state doit renvoyer un dictionnaire."
    assert "data_received" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'data_received'."
    assert "data" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'data'."
    assert "last_sk_id_curr" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'last_sk_id_curr'."


# import os
# import sys
# import unittest
# from unittest.mock import patch, MagicMock
# import numpy as np
# import pandas as pd
# import importlib

# # Add the parent directory to the sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import dash

# class TestDashApp(unittest.TestCase):

#     def setUp(self):
#         # Mock st.session_state
#         self.mock_session_state = MagicMock()
#         self.mock_session_state.__getitem__.side_effect = self.get_session_state_side_effect
#         dash.st.session_state = self.mock_session_state

#     def get_session_state_side_effect(self, key):
#         if key == 'state':
#             return {
#                 'df_selection': pd.DataFrame({
#                     'NAME_CONTRACT_TYPE': ['Cash loans'],
#                     'CODE_GENDER': ['M'],
#                     'NAME_FAMILY_STATUS': ['Married'],
#                     'NAME_HOUSING_TYPE': ['House / apartment'],
#                     'CNT_CHILDREN': [0],
#                     'DAYS_BIRTH': [-10000],
#                     'Prediction : 1': [0.1]
#                 }),
#                 'nombre_clients': 2,
#                 'average_age': 30.1,
#                 'average_prediction': 15.0
#             }
#         else:
#             raise KeyError(f"Key '{key}' not found in session_state mock")

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
#             filtered_df = dash.st.session_state['df_selection']
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
#             self.assertEqual(dash.st.session_state['nombre_clients'], 2)
#             self.assertAlmostEqual(dash.st.session_state['average_age'], 30.1)
#             self.assertAlmostEqual(dash.st.session_state['average_prediction'], 15.0)

#             print("Assertions passed for test_statistics_calculation")

#         except Exception as e:
#             print(f"Error in test_statistics_calculation: {e}")
#             raise

# if __name__ == '__main__':
#     unittest.main()


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
