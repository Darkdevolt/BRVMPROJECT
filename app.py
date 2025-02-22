import streamlit as st
import pandas as pd
import os
import altair as alt
from utils.data_utils import load_data, save_data, update_data, clean_numeric_columns

# Titre de l'application
st.title("Analyse des actions BRVM")

# Dictionnaire de correspondance entre noms abrégés et noms complets
actions_dict = {
    # ... (contenu inchangé du dictionnaire) ...
}

# Créer une liste combinée pour la recherche
search_options = list(actions_dict.keys()) + list(actions_dict.values())

# Champ de recherche pour sélectionner l'action
selected_action = st.selectbox("Recherchez une action (nom abrégé ou nom complet)", search_options)

# Récupérer le nom abrégé correspondant
if selected_action in actions_dict:
    action_key = selected_action
else:
    action_key = [k for k, v in actions_dict.items() if v == selected_action][0]

# Afficher le nom abrégé et le nom complet
st.info(f"Action sélectionnée : {action_key} - {actions_dict[action_key]}")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lire le fichier avec les paramètres européens
        new_data = pd.read_csv(
            uploaded_file,
            parse_dates=['Date'],
            dayfirst=True,
            thousands=' ',
            decimal=','
        )
        
        # Conversion spécifique pour la colonne Volume
        if 'Vol.' in new_data.columns:
            new_data['Vol.'] = (
                new_data['Vol.']
                .astype(str)
                .str.replace('[Kk]', '', regex=True)
                .str.replace(',', '.')
                .astype(float) * 1000
            )
        
        # Nettoyage supplémentaire
        new_data = clean_numeric_columns(new_data)
        
        # Validation des dates
        if new_data['Date'].isnull().any():
            st.error("Format de date invalide détecté. Utilisez le format JJ/MM/AAAA")
        
        # Confirmation de mise à jour
        st.warning("Voulez-vous vraiment mettre à jour les données ? Cette action est irréversible.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmer la mise à jour"):
                update_data(action_key, new_data)
                st.success(f"Données {action_key} mises à jour !")
        with col2:
            if st.button("Annuler"):
                st.info("Mise à jour annulée")
        
        # Aperçu des données
        st.subheader("Aperçu des données importées")
        st.write(new_data.head())

    except Exception as e:
        st.error(f"Erreur de traitement : {str(e)}")

# Affichage des données historiques
if st.button("Afficher l'historique complet"):
    historical_data = load_data(action_key)
    
    if historical_data is not None:
        st.subheader(f"Historique {action_key}")
        st.write(historical_data)
        
        # Dernière date disponible
        last_date = historical_data["Date"].max().strftime('%d/%m/%Y')
        st.info(f"Dernière mise à jour : {last_date}")
        
        # Visualisation graphique
        chart = alt.Chart(historical_data).mark_line().encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('Close:Q', title='Cours de clôture'),
            tooltip=['Date', 'Close']
        ).properties(
            title=f'Évolution de {action_key}',
            width=800,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Aucune donnée historique disponible")
