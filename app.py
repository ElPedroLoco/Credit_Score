import unittest
import os
import sys
import joblib
import pandas as pd
import numpy as np
import shap

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app 

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Charger le modèle et le scaler en mémoire
        current_directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_directory, "model_weights", "clf_xgb_o.pkl")
        self.model = joblib.load(model_path)
        scaler_path = os.path.join(current_directory, "model_weights", "scaler.pkl")
        self.scaler = joblib.load(scaler_path)

        # Charger les données de test
        csv_path = os.path.join(current_directory, "model_weights", "df_test.csv")
        self.df_test = pd.read_csv(csv_path)

    def tearDown(self):
        pass

    def test_predict_endpoint(self):
        # Teste l'API /predict_client avec un SK_ID_CURR valide
        sk_id_curr = 156003  # Remplacez par un ID existant dans votre jeu de données de test
        data = {'SK_ID_CURR': sk_id_curr}

        response = self.app.post('/predict_client', json=data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertIn('probability', response_data)
        self.assertIn('shap_values', response_data)
        self.assertIn('feature_names', response_data)
        self.assertIn('feature_values', response_data)

        proba = response_data['probability']
        shap_values = response_data['shap_values']
        feature_names = response_data['feature_names']
        feature_values = response_data['feature_values']

        # Vérifier que les valeurs retournées sont correctes
        self.assertIsInstance(proba, float)
        self.assertIsInstance(shap_values, list)
        self.assertIsInstance(feature_names, list)
        self.assertIsInstance(feature_values, list)

        # Vérifier que les noms de colonnes correspondent aux données
        self.assertEqual(len(feature_names), len(feature_values))

        # Vérifier que les valeurs SHAP ont la bonne structure et taille
        if isinstance(shap_values, list) and len(shap_values) > 1:
            self.assertEqual(len(shap_values[1]), len(feature_names))
        else:
            self.assertEqual(len(shap_values), len(feature_names))

    def test_predict_invalid_sk_id_curr(self):
        # Teste l'API /predict_client avec un SK_ID_CURR invalide
        sk_id_curr = 99999  # Remplacez par un ID qui n'existe pas dans votre jeu de données de test
        data = {'SK_ID_CURR': sk_id_curr}

        response = self.app.post('/predict_client', json=data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data['probability'], 0.0)
        self.assertEqual(response_data['shap_values'], [])
        self.assertEqual(response_data['feature_names'], [])
        self.assertEqual(response_data['feature_values'], [])

if __name__ == '__main__':
    unittest.main()



# import os
# import joblib
# import pandas as pd
# import shap
# from flask import Flask, jsonify, request

# app = Flask(__name__)

# # Récupérez le répertoire actuel du fichier app.py
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Charger le modèle en dehors de la clause if __name__ == "__main__":
# model_path = os.path.join(current_directory, "model_weights", "clf_xgb_o.pkl")
# model = joblib.load(model_path)

# # Charger le scaler
# scaler_path = os.path.join(current_directory, "model_weights", "scaler.pkl")
# scaler = joblib.load(scaler_path)

# @app.route("/predict_client", methods=['POST'])
# def predict():
#     data = request.json
#     sk_id_curr = data['SK_ID_CURR']

#     # Construisez le chemin complet vers df_train.csv en utilisant le chemin relatif depuis l'emplacement de api.py
#     csv_path = os.path.join(current_directory, "model_weights", "df_test.csv")
#     # Charger le CSV
#     df = pd.read_csv(csv_path)
#     sample = df[df['SK_ID_CURR'] == sk_id_curr]

#     # Supprimer la colonne ID pour la prédiction
#     sample = sample.drop(columns=['SK_ID_CURR'])

#     # Appliquer le scaler
#     sample_scaled = scaler.transform(sample)

#     # Prédire
#     prediction = model.predict_proba(sample_scaled)
#     proba = prediction[0][1] # Probabilité de la seconde classe

#     # Calculer les valeurs SHAP pour l'échantillon donné
#     explainer = shap.TreeExplainer(model)
#     shap_values = explainer.shap_values(sample_scaled)

#     # Handle SHAP output depending on its structure
#     if isinstance(shap_values, list):
#         if len(shap_values) > 1:
#             shap_values_output = shap_values[1][0].tolist()
#         else:
#             shap_values_output = shap_values[0][0].tolist()
#     else:
#         shap_values_output = shap_values.tolist()
    
#     # Retourner les valeurs SHAP avec la probabilité
#     return jsonify({
#         'probability': proba*100, 
#         'shap_values': shap_values_output,
#         'feature_names': sample.columns.tolist(),
#         'feature_values': sample.values[0].tolist()
#     })

# if __name__ == "__main__":
#     port = os.environ.get("PORT", 5000)
#     app.run(host='0.0.0.0', port=5000, debug=True)
    
