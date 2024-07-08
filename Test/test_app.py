import os
import sys
import joblib
import pandas as pd
import pytest
from flask import Flask, jsonify, request

# Ajouter le chemin relatif du fichier app.py au sys.path pour pouvoir l'importer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les éléments nécessaires du fichier api.py
from app import app, model, predict

# Créer un client de test pour l'application Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Teste le chargement du modèle de prédiction
def test_model_loading():
    # # Détermine le chemin du répertoire courant
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du fichier contenant le modèle entraîné
    model_path = os.path.join("model_weights", "model.pkl")
    # Charge le modèle à partir du fichier
    model = joblib.load(model_path)
    # Vérifie que le modèle a été chargé correctement
    assert model is not None, "Erreur dans le chargement du modèle."

# Teste le chargement du fichier CSV contenant les données de train
def test_csv_loading():
    # # Détermine le chemin du répertoire courant
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du fichier CSV
    csv_path = os.path.join("model_weights", "df_train.csv")
    # Charge le fichier CSV dans un DataFrame pandas
    df = pd.read_csv(csv_path)
    # Vérifie que le DataFrame n'est pas vide
    assert not df.empty, "Erreur dans le chargement du CSV."

# Teste la fonction de prédiction de l'API
def test_prediction():
    import os
    import pandas as pd
    from flask import json
    # Détermine le chemin du répertoire courant
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du fichier CSV contenant les données de test
    csv_path = os.path.join("model_weights", "df_train.csv")
    # Charge le fichier CSV dans un DataFrame pandas
    df = pd.read_csv(csv_path)
    # Prend un échantillon pour la prédiction
    sk_id_curr = df.iloc[0]['SK_ID_CURR']
    # Crée une requête de test pour la prédiction en utilisant l'échantillon sélectionné
    with app.test_client() as client:
        response = client.post('/predict', json={'SK_ID_CURR': sk_id_curr})
        data = json.loads(response.data)
        prediction = data['probability']
        # Vérifie que la prédiction a été effectuée correctement
        assert prediction is not None, "La prédiction a échoué."



# import unittest
# from unittest.mock import patch, MagicMock
# import os
# import sys
# import joblib
# import pandas as pd
# import shap
# import json

# # Add the parent directory to the sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import app

# class TestFlaskApp(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#         # Charger le modèle et le scaler en mémoire
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         model_path = os.path.join(current_directory, "..", "model_weights", "clf_xgb_o.pkl")
#         self.model = joblib.load(model_path)
#         scaler_path = os.path.join(current_directory, "..", "model_weights", "scaler.pkl")
#         self.scaler = joblib.load(scaler_path)

#         # Charger les données de test
#         csv_path = os.path.join(current_directory, "..", "model_weights", "df_test.csv")
#         self.df_test = pd.read_csv(csv_path)

#         # Mock de st.session_state pour éviter l'erreur de KeyError
#         self.mock_session_state = MagicMock()
#         patcher = patch('streamlit.session_state', self.mock_session_state)
#         patcher.start()
#         self.addCleanup(patcher.stop)

#     def tearDown(self):
#         pass

#     def test_predict_endpoint_with_valid_sk_id_curr(self):
#         # Teste l'API /predict_client avec un SK_ID_CURR valide
#         sk_id_curr = 156003
#         data = {'SK_ID_CURR': sk_id_curr}

#         response = self.app.post('/predict_client', json=data)
#         self.assertEqual(response.status_code, 200)

#         response_data = json.loads(response.data.decode('utf-8'))
#         self.assertIn('probability', response_data)
#         self.assertIn('shap_values', response_data)
#         self.assertIn('feature_names', response_data)
#         self.assertIn('feature_values', response_data)

#         proba = response_data['probability']
#         shap_values = response_data['shap_values']
#         feature_names = response_data['feature_names']
#         feature_values = response_data['feature_values']

#         # Vérifier que les valeurs retournées sont correctes
#         self.assertIsInstance(proba, float)
#         self.assertIsInstance(shap_values, list)
#         self.assertIsInstance(feature_names, list)
#         self.assertIsInstance(feature_values, list)

#         # Vérifier que les noms de colonnes correspondent aux données
#         self.assertEqual(len(feature_names), len(feature_values))

#         # Vérifier que les valeurs SHAP ont la bonne structure et taille
#         if isinstance(shap_values, list) and len(shap_values) > 1:
#             self.assertEqual(len(shap_values[1]), len(feature_names))
#         else:
#             self.assertEqual(len(shap_values), len(feature_names))

#     def test_predict_endpoint_with_invalid_sk_id_curr(self):
#         # Teste l'API /predict_client avec un SK_ID_CURR invalide
#         sk_id_curr = 999999
#         data = {'SK_ID_CURR': sk_id_curr}

#         response = self.app.post('/predict_client', json=data)
#         self.assertEqual(response.status_code, 200)

#         response_data = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(response_data['probability'], 0.0)
#         self.assertEqual(response_data['shap_values'], [])
#         self.assertEqual(response_data['feature_names'], [])
#         self.assertEqual(response_data['feature_values'], [])

# if __name__ == '__main__':
#     unittest.main()


# class TestFlaskApp(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#         # Charger le modèle et le scaler en mémoire
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         model_path = os.path.join(current_directory, "..", "model_weights", "clf_xgb_o.pkl")
#         self.model = joblib.load(model_path)
#         scaler_path = os.path.join(current_directory, "..", "model_weights", "scaler.pkl")
#         self.scaler = joblib.load(scaler_path)

#         # Charger les données de test
#         csv_path = os.path.join(current_directory, "..", "model_weights", "df_test.csv")
#         self.df_test = pd.read_csv(csv_path)

#     def tearDown(self):
#         pass

#     def test_predict_endpoint_with_valid_sk_id_curr(self):
#         # Teste l'API /predict_client avec un SK_ID_CURR valide
#         sk_id_curr = 12345  # Remplacez par un ID existant dans votre jeu de données de test
#         data = {'SK_ID_CURR': sk_id_curr}

#         response = self.app.post('/predict_client', json=data)
#         self.assertEqual(response.status_code, 200)

#         response_data = json.loads(response.data.decode('utf-8'))
#         self.assertIn('probability', response_data)
#         self.assertIn('shap_values', response_data)
#         self.assertIn('feature_names', response_data)
#         self.assertIn('feature_values', response_data)

#         proba = response_data['probability']
#         shap_values = response_data['shap_values']
#         feature_names = response_data['feature_names']
#         feature_values = response_data['feature_values']

#         # Vérifier que les valeurs retournées sont correctes
#         self.assertIsInstance(proba, float)
#         self.assertIsInstance(shap_values, list)
#         self.assertIsInstance(feature_names, list)
#         self.assertIsInstance(feature_values, list)

#         # Vérifier que les noms de colonnes correspondent aux données
#         self.assertEqual(len(feature_names), len(feature_values))

#         # Vérifier que les valeurs SHAP ont la bonne structure et taille
#         if isinstance(shap_values, list) and len(shap_values) > 1:
#             self.assertEqual(len(shap_values[1]), len(feature_names))
#         else:
#             self.assertEqual(len(shap_values), len(feature_names))

#     def test_predict_endpoint_with_invalid_sk_id_curr(self):
#         # Teste l'API /predict_client avec un SK_ID_CURR invalide
#         sk_id_curr = 99999  # Remplacez par un ID qui n'existe pas dans votre jeu de données de test
#         data = {'SK_ID_CURR': sk_id_curr}

#         response = self.app.post('/predict_client', json=data)
#         self.assertEqual(response.status_code, 200)

#         response_data = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(response_data['probability'], 0.0)
#         self.assertEqual(response_data['shap_values'], [])
#         self.assertEqual(response_data['feature_names'], [])
#         self.assertEqual(response_data['feature_values'], [])

# if __name__ == '__main__':
#     unittest.main()

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
