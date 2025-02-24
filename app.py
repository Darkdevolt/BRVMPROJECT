import streamlit as st
from scraper import fetch_finance_data

# Configuration de la page
st.set_page_config(page_title="Sika Finance Data", page_icon="📈")

# Titre de l'application
st.title("📊 Sika Finance Data Fetcher")
st.markdown("Cette application récupère les données financières de Sika Finance.")

# Bouton pour rafraîchir les données
if st.button("Rafraîchir les données"):
    with st.spinner("Récupération des données en cours..."):
        try:
            data = fetch_finance_data()  # Récupère les données
            if data:
                st.subheader("Données financières")
                st.write(data)
            else:
                st.error("Aucune donnée trouvée.")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")

# Pied de page
st.markdown("---")
st.markdown("© 2023 - Mon Application Sika Finance")
