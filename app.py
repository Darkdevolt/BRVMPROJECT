import streamlit as st
import pandas as pd

# Définition de la structure de référence
expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
dtypes_ref = {'Date': 'object', 'Open': 'float64', 'High': 'float64', 'Low': 'float64', 'Close': 'float64', 'Volume': 'float64'}

st.title("📊 Vérification de la Structure des Fichiers CSV")

# Upload du fichier par l'utilisateur
uploaded_file = st.file_uploader("Déposez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Vérification des colonnes
        if list(df.columns) != expected_columns:
            st.error("❌ Erreur : La structure du fichier ne correspond pas au modèle attendu.")
            st.write("Colonnes attendues :", expected_columns)
            st.write("Colonnes trouvées :", list(df.columns))
        else:
            # Vérification des types de données
            type_errors = []
            for col, expected_type in dtypes_ref.items():
                if df[col].dtype != expected_type:
                    type_errors.append(f"{col} (Attendu: {expected_type}, Trouvé: {df[col].dtype})")
            
            if type_errors:
                st.error("❌ Erreur : Les types de certaines colonnes ne correspondent pas.")
                for err in type_errors:
                    st.write(err)
            else:
                st.success("✅ Succès : Le fichier est valide et respecte la structure requise !")
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
