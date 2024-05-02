# Projet-7-Pierre Hirsch
 
OpenClassRooms_Projet7
Implémentez un modèle de scoring
Présentation

La mission principale de ce projet est de prédire le risque de faillite d'un client pour une société de crédit. Pour cela, nous devons configurer un modèle de classification binaire et d'en analyser les différentes métriques.

Ce projet consiste à créer une API web avec un Dashboard interactif. Celui-ci devra a minima contenir les fonctionnalités suivantes :

    Permettre de visualiser le score et l’interprétation de ce score pour chaque client de façon intelligible pour une personne non experte en data science.
    Permettre de visualiser des informations descriptives relatives à un client (via un système de filtre).

Ce dépôt contient :

    Un dossier avec le Notebook Jupyter pour l'étude des données, l'entraînement et la configuration du modèle de classification.
    Une note technique qui explique en détails la construction et les résultats du modèle.
    Le fichier app.py qui est le code de la partie API Flask.
    Un dossier dashboard qui contient le code de la partie dashboard streamlit.
    Un dataset app_test_dashboard_with_prediction qui est utilisé par ces deux parties.
    Un dossier model_weights qui contiennent les fichiers pickle sauvegardés.

Modèle de classification

Le modèle retenu pour cet exercice est le modèle XGBoost.

Dashboard / API

J'ai utilisé deux librairies Python pour ce sujet :

    Flask
    Streamlit

Données d'entrées

    Lien de téléchargement des données d'entrées : https://www.kaggle.com/c/home-credit-default-risk/data
    Notebook de départ pour la partie Features Engineering : https://www.kaggle.com/willkoehrsen/start-here-a-gentle-introduction

