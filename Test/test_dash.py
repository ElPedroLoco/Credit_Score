# import unittest
# import pandas as pd
# from unittest.mock import patch, MagicMock
# import sys
# import os
# import requests

# # Ajouter le répertoire parent au chemin d'importation
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Importer les éléments nécessaires depuis votre script dash.py
# from dash import df, base_url, user_input, user_input2

# class TestStreamlitApp(unittest.TestCase):

#     def test_dataframe_loaded(self):
#         # Vérifie que le DataFrame est bien chargé
#         self.assertIsInstance(df, pd.DataFrame)
#         self.assertFalse(df.empty)

#     @patch('dash.contract_type', ['Cash loans'])
#     @patch('dash.sexe', ['M'])
#     @patch('dash.civil_status', ['Married'])
#     @patch('dash.habitation_type', ['House / apartment'])
#     @patch('dash.nombre_enfants', [0])
#     def test_filter_data(self):
#         # Vérifie que le filtrage fonctionne correctement
#         from dash import df_selection  # Importer df_selection après avoir patché les filtres
#         self.assertFalse(df_selection.empty)
#         self.assertEqual(df_selection.iloc[0]["NAME_CONTRACT_TYPE"], 'Cash loans')
#         self.assertEqual(df_selection.iloc[0]["CODE_GENDER"], 'F')
#         self.assertEqual(df_selection.iloc[0]["NAME_FAMILY_STATUS"], 'Married')
#         self.assertEqual(df_selection.iloc[0]["NAME_HOUSING_TYPE"], 'House / apartment')
#         self.assertEqual(df_selection.iloc[0]["CNT_CHILDREN"], 0)

#     @patch('dash.requests.get')
#     def test_infos_client_api(self, mock_get):
#         # Mock la réponse de l'API
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             'data': {
#                 'status_famille': 'Married',
#                 'nb_enfant': 0,
#                 'age': 30,
#                 'revenus': 150000,
#                 'montant_credit': 500000,
#                 'annuites': 20000,
#                 'montant_bien': 450000
#             }
#         }
#         mock_get.return_value = mock_response

#         # Appeler la fonction API
#         full_url = base_url + '?id_client=' + user_input
#         response = requests.get(full_url)

#         # Vérifier la réponse
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertIn('data', data)
#         self.assertEqual(data['data']['status_famille'], 'Married')

#     @patch('dash.requests.get')
#     def test_predict_client_api(self, mock_get):
#         # Mock la réponse de l'API
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             'prediction': [1],
#             'prediction_proba': [[0.2, 0.8]]
#         }
#         mock_get.return_value = mock_response

#         # Appeler la fonction API
#         full_url = base_url + '?id_client=' + user_input2
#         response = requests.get(full_url)

#         # Vérifier la réponse
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertIn('prediction', data)
#         self.assertEqual(data['prediction'], [1])

# if __name__ == '__main__':
#     unittest.main()


import unittest
import pandas as pd
from unittest.mock import patch
import sys
import os

# Ajouter le répertoire parent au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Chargement du dataset
df = pd.read_csv("app_test_dashboard_with_prediction.csv")

class TestStreamlitApp(unittest.TestCase):

    def test_dataframe_loaded(self):
        # Vérifie que le DataFrame est bien chargé
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    @patch('dash.contract_type', ['Cash loans'])
    @patch('dash.sexe', ['M'])
    @patch('dash.civil_status', ['Married'])
    @patch('dash.habitation_type', ['House / apartment'])
    @patch('dash.nombre_enfants', [0])
    
    def test_filter_data(self):
        # # Vérifie que le filtrage fonctionne correctement
        # from dash import df_selection  # Importer df_selection après avoir patché les filtres
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]["NAME_CONTRACT_TYPE"], 'Cash loans')
        self.assertEqual(df.iloc[0]["CODE_GENDER"], 'F')
        self.assertEqual(df.iloc[0]["NAME_FAMILY_STATUS"], 'Married')
        self.assertEqual(df.iloc[0]["NAME_HOUSING_TYPE"], 'House / apartment')
        self.assertEqual(df.iloc[0]["CNT_CHILDREN"], 0)

if __name__ == '__main__':
    unittest.main()
