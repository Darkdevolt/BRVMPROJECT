import streamlit as st
import pandas as pd
import os
import altair as alt
from utils.data_utils import load_data, save_data, update_data, clean_numeric_columns

# Titre de l'application
st.title("Analyse des actions BRVM")

# Dictionnaire de correspondance original
actions_dict = {
    "ABJC": "SERVAIR ABIDJAN COTE D'IVOIRE",
    "BICC": "BICI COTE D'IVOIRE",
    # ... (conservez tout votre dictionnaire existant tel quel) ...
    "UNXC": "UNIWAX COTE D'IVOIRE"
}

# Création de la liste de recherche (identique à votre version)
search_options = list(actions_dict.keys()) + list(actions_dict.values())

# Sélection de l'action (identique)
selected_action = st.selectbox("Recherchez une action (nom abrégé ou nom complet)", search_options)

# Récupération du nom abrégé AVEC GESTION D'ERREUR
try:
    if selected_action in actions_dict:
        action_key = selected_action
    else:
        # Version sécurisée avec vérification
        matches = [k for k, v in actions_dict.items() if v == selected_action]
        
        if not matches:
            st.error("Action non trouvée ! Veuillez réessayer.")
            st.stop()
            
        action_key = matches[0]
        
except Exception as e:
    st.error(f"Erreur de sélection : {str(e)}")
    st.stop()

# Affichage de la sélection (identique)
st.info(f"Action sélectionnée : {action_key} - {actions_dict[action_key]}")

# Téléchargement CSV (identique)
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lecture du fichier (identique)
        new_data = pd.read_csv(uploaded_file)
        
        # Nettoyage (identique)
        new_data = clean_numeric_columns(new_data)
        
        # Vérification date (nouveau)
        if 'Date' in new_data.columns and new_data['Date'].isnull().any():
            st.error("Format de date invalide détecté !")
            st.stop()
            
        # Confirmation (identique)
        st.warning("Voulez-vous vraiment mettre à jour les données ?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmer"):
                update_data(action_key, new_data)
                st.success("Mise à jour réussie !")
        with col2:
            if st.button("Annuler"):
                st.info("Annulation effectuée")
        
        # Aperçu (identique)
        st.subheader("Aperçu")
        st.write(new_data)
        
    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        st.stop()

# Affichage historique (identique)
if st.button("Afficher les données historiques"):
    historical_data = load_data(action_key)
    
    if historical_data is not None:
        st.subheader(f"Historique {action_key}")
        st.write(historical_data)
        
        # Graphique (identique)
        chart = alt.Chart(historical_data).mark_line().encode(
            x="Date:T",
            y="Close:Q",
            tooltip=["Date", "Close"]
        ).properties(
            title=f"Évolution de {action_key}",
            width=800,
            height=400
        )
        st.altair_chart(chart)
    else:
        st.warning("Aucune donnée disponible")
