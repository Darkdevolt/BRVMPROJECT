import pandas as pd
import os

# Chemin du dossier de données
DATA_DIR = "data"

def load_data(action):
    """
    Charge les données historiques pour une action spécifique.
    """
    file_path = os.path.join(DATA_DIR, f"{action}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
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
