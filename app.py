import streamlit as st
import pandas as pd
import os
from utils.data_utils import load_data, save_data, update_data

# Titre de l'application
st.title("Analyse des actions BRVM")

# Liste déroulante pour sélectionner l'action
actions = ["SONATEL", "BOA", "ECOBANK", "OTHER"]
selected_action = st.selectbox("Sélectionnez l'action", actions)

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le fichier CSV téléchargé
    new_data = pd.read_csv(uploaded_file)
    
    # Mettre à jour les données historiques
    update_data(selected_action, new_data)
    
    st.success(f"Données pour {selected_action} mises à jour avec succès!")

# Afficher les données historiques
if st.button("Afficher les données historiques"):
    historical_data = load_data(selected_action)
    if historical_data is not None:
        st.write(historical_data)
    else:
        st.warning(f"Aucune donnée trouvée pour {selected_action}.")
