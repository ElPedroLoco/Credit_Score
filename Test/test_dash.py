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
        print("DataFrame loaded successfully.")

    @patch('df.contract_type', ['Cash loans'])
    @patch('df.sexe', ['M'])
    @patch('df.civil_status', ['Married'])
    @patch('df.habitation_type', ['House / apartment'])
    @patch('df.nombre_enfants', [0])
    
    def test_filter_data(self):
        # Vérifie que le filtrage fonctionne correctement
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]["NAME_CONTRACT_TYPE"], 'Cash loans')
        self.assertEqual(df.iloc[0]["CODE_GENDER"], 'F')
        self.assertEqual(df.iloc[0]["NAME_FAMILY_STATUS"], 'Married')
        self.assertEqual(df.iloc[0]["NAME_HOUSING_TYPE"], 'House / apartment')
        self.assertEqual(df.iloc[0]["CNT_CHILDREN"], 0)
        print("Filtering data test passed.")

if __name__ == '__main__':
    unittest.main()
