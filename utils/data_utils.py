import pandas as pd
import os

def load_data(action_key):
    """Charge les données historiques avec gestion des formats"""
    filename = f"data/{action_key}_historique.csv"
    if os.path.exists(filename):
        try:
            return pd.read_csv(
                filename,
                parse_dates=['Date'],
                dayfirst=True,
                decimal=',',
                thousands=' '
            )
        except Exception as e:
            print(f"Erreur de chargement : {str(e)}")
            return None
    return None

def save_data(action_key, df):
    """Sauvegarde les données dans le format correct"""
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{action_key}_historique.csv", index=False, encoding='utf-8-sig')

def update_data(action_key, new_df):
    """Met à jour les données existantes avec les nouvelles"""
    existing_df = load_data(action_key)
    if existing_df is not None:
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates('Date')
    else:
        combined_df = new_df
    save_data(action_key, combined_df)

def clean_numeric_columns(df):
    """Nettoie les colonnes numériques avec conversions"""
    numeric_cols = ['Dernier', 'Ouv.', 'Plus Haut', 'Plus Bas', 'Variation %']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '.')
                .str.replace('[^0-9.]', '', regex=True)
                .astype(float)
            )
    
    return df
