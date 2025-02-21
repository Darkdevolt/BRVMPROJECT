import streamlit as st
import pandas as pd
import os
import altair as alt
from utils.data_utils import load_data, save_data, update_data

# Titre de l'application
st.title("Analyse des actions BRVM")

# ... (le dictionnaire actions_dict reste inchangé) ...

def clean_numeric_columns(df):
    """Nettoie les colonnes numériques avec des formats spéciaux"""
    # Convertir les dates au format standard
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
    
    # Nettoyer les colonnes numériques
    numeric_columns = ['Dernier', 'Ouv.', 'Plus Haut', 'Plus Bas', 'Vol.', 'Variation %']
    
    for col in numeric_columns:
        if col == 'Vol.':
            # Gérer le format "2,08K" -> 2080
            df[col] = df[col].str.replace('K', '')
            df[col] = df[col].str.replace(',', '.').astype(float) * 1000
        elif col == 'Variation %':
            # Gérer les pourcentages avec virgule
            df[col] = df[col].str.replace(',', '.').str.rstrip('%').astype(float)
        else:
            # Convertir les nombres avec virgule décimale
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    return df

def load_data(action_key):
    """Charge les données historiques avec gestion des formats"""
    filename = f"data/{action_key}_historique.csv"
    if os.path.exists(filename):
        df = pd.read_csv(
            filename,
            parse_dates=['Date'],
            dayfirst=True,  # Important pour les dates européennes
            thousands=' ',  # Gère les espaces comme séparateurs de milliers
            decimal=','     # Gère les virgules comme séparateurs décimaux
        )
        return df
    return None

# ... (le reste du code reste inchangé jusqu'à la partie de téléchargement) ...

if uploaded_file is not None:
    try:
        # Lire le fichier en gérant les formats européens
        new_data = pd.read_csv(
            uploaded_file,
            parse_dates=['Date'],
            dayfirst=True,
            thousands=' ',
            decimal=','
        )
        
        # Conversion supplémentaire pour la colonne Vol.
        if 'Vol.' in new_data.columns:
            new_data['Vol.'] = new_data['Vol.'].astype(str).str.replace('K', '')
            new_data['Vol.'] = pd.to_numeric(new_data['Vol.'].str.replace(',', '.'), errors='coerce') * 1000
        
        # Nettoyage supplémentaire
        new_data = clean_numeric_columns(new_data)
        
        # Vérification du format de date
        if new_data['Date'].isnull().any():
            st.error("Erreur de format de date détectée. Veuillez vérifier le format JJ/MM/AAAA")
        
        # ... (le reste du code de traitement reste inchangé) ...

# ... (la partie d'affichage des données reste inchangé) ...
