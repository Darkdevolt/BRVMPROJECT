import pandas as pd
import os

# Chemin du dossier de données
DATA_DIR = "data"

def clean_numeric_columns(df):
    """
    Nettoie les colonnes numériques en supprimant les séparateurs de milliers (points).
    """
    for col in df.columns:
        # Vérifier si la colonne contient des données numériques formatées avec des points
        if df[col].dtype == "object":  # Si la colonne est de type "object" (chaîne de caractères)
            try:
                # Essayer de supprimer les points et de convertir en nombres
                df[col] = df[col].astype(str).str.replace(".", "", regex=False).astype(float)
            except (ValueError, TypeError):
                # Si la conversion échoue, ignorer cette colonne (elle n'est pas numérique)
                continue
    return df

def load_data(action):
    """
    Charge les données historiques pour une action spécifique.
    """
    file_path = os.path.join(DATA_DIR, f"{action}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Nettoyer les colonnes numériques lors du chargement
        df = clean_numeric_columns(df)
        return df
    return None

def save_data(action, data):
    """
    Sauvegarde les données pour une action spécifique.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_path = os.path.join(DATA_DIR, f"{action}.csv")
    data.to_csv(file_path, index=False)

def update_data(action, new_data):
    """
    Met à jour les données historiques avec de nouvelles données.
    """
    historical_data = load_data(action)
    if historical_data is not None:
        # Fusionner les anciennes et nouvelles données
        updated_data = pd.concat([historical_data, new_data]).drop_duplicates().reset_index(drop=True)
    else:
        updated_data = new_data
    
    # Sauvegarder les données mises à jour
    save_data(action, updated_data)
