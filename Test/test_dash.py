import unittest
import pandas as pd
from unittest.mock import patch
import sys
import os

# Ajouter le répertoire parent au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les éléments nécessaires depuis votre script dash.py
from dash import df

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
        # Vérifie que le filtrage fonctionne correctement
        from dash import df_selection  # Importer df_selection après avoir patché les filtres
        self.assertFalse(df_selection.empty)
        self.assertEqual(df_selection.iloc[0]["NAME_CONTRACT_TYPE"], 'Cash loans')
        self.assertEqual(df_selection.iloc[0]["CODE_GENDER"], 'F')
        self.assertEqual(df_selection.iloc[0]["NAME_FAMILY_STATUS"], 'Married')
        self.assertEqual(df_selection.iloc[0]["NAME_HOUSING_TYPE"], 'House / apartment')
        self.assertEqual(df_selection.iloc[0]["CNT_CHILDREN"], 0)

if __name__ == '__main__':
    unittest.main()
