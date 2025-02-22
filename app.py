import streamlit as st
from scraper import fetch_finance_data
from utils.helpers import clean_data

# Configuration de la page
st.set_page_config(page_title="Sika Finance Data", page_icon="📈")

# Titre de l'application
st.title("📊 Sika Finance Data Fetcher")
st.markdown("Cette application récupère les données financières de Sika Finance.")

# Bouton pour rafraîchir les données
if st.button("Rafraîchir les données"):
    with st.spinner("Récupération des données en cours..."):
        data = fetch_finance_data()  # Récupère les données
        cleaned_data = clean_data(data)  # Nettoie les données
        
        # Affichage des données
        st.subheader("Données financières")
        st.write(cleaned_data)

        # Exemple de graphique (optionnel)
        st.line_chart(cleaned_data['price'])  # Adaptez selon les données

# Pied de page
st.markdown("---")
st.markdown("© 2023 - Mon Application Sika Finance")
