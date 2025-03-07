import pandas as pd
import numpy as np

def check_structure(df):
    """
    Vérifie la structure du fichier CSV.
    Retourne True si la structure est correcte, sinon False.
    """
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    return all(column in df.columns for column in required_columns)

def handle_missing_data(df):
    """
    Gère les données manquantes en utilisant une interpolation linéaire.
    Retourne le DataFrame traité.
    """
    # Convertir la colonne 'Date' en datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    
    # Trier les données par date
    df = df.sort_values(by='Date')
    
    # Interpolation linéaire pour les colonnes numériques
    df['Open'] = df['Open'].interpolate(method='linear')
    df['High'] = df['High'].interpolate(method='linear')
    df['Low'] = df['Low'].interpolate(method='linear')
    df['Close'] = df['Close'].interpolate(method='linear')
    
    return df

def process_data(file):
    """
    Charge un fichier CSV, vérifie sa structure, et gère les données manquantes.
    Retourne le DataFrame traité ou None si la structure est incorrecte.
    """
    try:
        # Charger le fichier CSV
        df = pd.read_csv(file)
        
        # Vérifier la structure
        if not check_structure(df):
            print("Erreur : La structure du fichier CSV est incorrecte.")
            return None
        
        # Gérer les données manquantes
        df = handle_missing_data(df)
        
        return df
    
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {e}")
        return None
