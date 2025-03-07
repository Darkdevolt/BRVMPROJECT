import pandas as pd

# Définition de la structure de référence
expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
dtypes_ref = {'Date': str, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float}

def check_structure(df):
    """
    Vérifie si le fichier CSV respecte la structure attendue.
    Retourne un message d'erreur si la structure est incorrecte, sinon None.
    """
    # Normaliser les noms de colonnes (enlever les espaces et mettre en minuscules)
    df.columns = df.columns.str.strip().str.lower()
    expected_columns_lower = [col.lower() for col in expected_columns]

    # Vérifier les colonnes
    if list(df.columns) != expected_columns_lower:
        return "❌ Erreur : La structure du fichier ne correspond pas au modèle attendu."

    # Vérifier les types de données
    type_errors = []
    for col, expected_type in dtypes_ref.items():
        try:
            df[col] = df[col].astype(expected_type)
        except ValueError:
            type_errors.append(f"{col} (Attendu: {expected_type}, Trouvé: {df[col].dtype})")

    if type_errors:
        return "❌ Erreur : Les types de certaines colonnes ne correspondent pas."

    return None  # Aucune erreur

def handle_missing_data(df):
    """
    Gère les données manquantes en utilisant une interpolation linéaire.
    Retourne le DataFrame traité.
    """
    try:
        # Convertir la colonne 'Date' en datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
        
        # Vérifier si la conversion a échoué pour certaines dates
        if df['Date'].isnull().any():
            st.warning("⚠️ Certaines dates n'ont pas pu être converties. Elles seront ignorées.")
            df = df.dropna(subset=['Date'])  # Supprimer les lignes avec des dates invalides
        
        # Trier les données par date
        df = df.sort_values(by='Date')
        
        # Interpolation linéaire pour les colonnes numériques
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            df[col] = df[col].interpolate(method='linear')
        
        return df
    except Exception as e:
        raise ValueError(f"Erreur lors de la gestion des données manquantes : {e}")

def process_data(file):
    """
    Charge un fichier CSV, vérifie sa structure, et gère les données manquantes.
    Retourne le DataFrame traité et un message d'erreur (ou None si tout est OK).
    """
    try:
        # Charger le fichier CSV
        df = pd.read_csv(file)
        
        # Vérifier la structure
        error_message = check_structure(df)
        if error_message:
            return None, error_message
        
        # Gérer les données manquantes
        df = handle_missing_data(df)
        
        return df, None  # Retourner le DataFrame traité et aucun message d'erreur
    
    except Exception as e:
        return None, f"❌ Erreur lors de la lecture ou du traitement du fichier : {e}"
