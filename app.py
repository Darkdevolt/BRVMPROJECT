import streamlit as st
import pandas as pd
import os
import altair as alt  # Utilisation de Altair pour les graphiques
from utils.data_utils import load_data, save_data, update_data, clean_numeric_columns

# Titre de l'application
st.title("Analyse des actions BRVM")

# Dictionnaire de correspondance entre noms abrégés et noms complets
actions_dict = {
    "ABJC": "SERVAIR ABIDJAN COTE D'IVOIRE",
    "BICC": "BICI COTE D'IVOIRE",
    "BNBC": "BERNABE COTE D'IVOIRE",
    "BOAB": "BANK OF AFRICA BENIN",
    "BOABF": "BANK OF AFRICA BURKINA FASO",
    "BOAC": "BANK OF AFRICA COTE D'IVOIRE",
    "BOAM": "BANK OF AFRICA MALI",
    "BOAN": "BANK OF AFRICA NIGER",
    "BOAS": "BANK OF AFRICA SENEGAL",
    "CABC": "SICABLE COTE D'IVOIRE",
    "CBIBF": "CORIS BANK INTERNATIONAL BURKINA FASO",
    "CFAC": "CFAO MOTORS COTE D'IVOIRE",
    "CIEC": "CIE COTE D'IVOIRE",
    "ECOC": "ECOBANK COTE D'IVOIRE",
    "ETIT": "Ecobank Transnational Incorporated TOGO",
    "FTSC": "FILTISAC COTE D'IVOIRE",
    "LNBB": "LOTERIE NATIONALE DU BENIN",
    "NEIC": "NEI-CEDA COTE D'IVOIRE",
    "NSBC": "NSIA BANQUE COTE D'IVOIRE",
    "NTLC": "NESTLE COTE D'IVOIRE",
    "ONTBF": "ONATEL BURKINA FASO",
    "ORAC": "ORANGE COTE D'IVOIRE",
    "ORGT": "ORAGROUP TOGO",
    "PALC": "PALM COTE D'IVOIRE",
    "PRSC": "TRACTAFRIC MOTORS COTE D'IVOIRE",
    "SAFC": "SAFCA COTE D'IVOIRE",
    "SCRC": "SUCRIVOIRE COTE D'IVOIRE",
    "SDCC": "SODE COTE D'IVOIRE",
    "SDSC": "AFRICA GLOBAL LOGISTICS COTE D'IVOIRE",
    "SEMC": "EVIOSYS PACKAGING SIEM COTE D'IVOIRE",
    "SGBC": "SOCIETE GENERALE COTE D'IVOIRE",
    "SHEC": "VIVO ENERGY COTE D'IVOIRE",
    "SIBC": "SOCIETE IVOIRIENNE DE BANQUE COTE D'IVOIRE",
    "SICC": "SICOR COTE D'IVOIRE",
    "SIVC": "AIR LIQUIDE COTE D'IVOIRE",
    "SLBC": "SOLIBRA COTE D'IVOIRE",
    "SMBC": "SMB COTE D'IVOIRE",
    "SNTS": "SONATEL SENEGAL",
    "SOGC": "SOGB COTE D'IVOIRE",
    "SPHC": "SAPH COTE D'IVOIRE",
    "STAC": "SETAO COTE D'IVOIRE",
    "STBC": "SITAB COTE D'IVOIRE",
    "SVOC": "MOVIS COTE D'IVOIRE",
    "TTLC": "TOTALENERGIES MARKETING COTE D'IVOIRE",
    "TTLS": "TOTALENERGIES MARKETING SENEGAL",
    "TTRC": "TRITURAF Ste en Liquid",
    "UNLC": "UNILEVER COTE D'IVOIRE",
    "UNXC": "UNIWAX COTE D'IVOIRE"
}

# Créer une liste combinée pour la recherche (noms abrégés + noms complets)
search_options = list(actions_dict.keys()) + list(actions_dict.values())

# Champ de recherche pour sélectionner l'action
selected_action = st.selectbox("Recherchez une action (nom abrégé ou nom complet)", search_options)

# Récupérer le nom abrégé correspondant
if selected_action in actions_dict:
    action_key = selected_action  # Si l'utilisateur a tapé un nom abrégé
else:
    # Si l'utilisateur a tapé un nom complet, trouver le nom abrégé correspondant
    action_key = [k for k, v in actions_dict.items() if v == selected_action][0]

# Afficher le nom abrégé et le nom complet sélectionnés
st.info(f"Action sélectionnée : {action_key} - {actions_dict[action_key]}")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le fichier CSV téléchargé
    new_data = pd.read_csv(uploaded_file)
    
    # Nettoyer les colonnes numériques
    new_data = clean_numeric_columns(new_data)
    
    # Afficher le message de confirmation AVANT l'aperçu des données
    st.warning("Voulez-vous vraiment mettre à jour les données ? Cette action écrasera les données existantes.")
    
    # Boutons de confirmation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirmer la mise à jour"):
            # Mettre à jour les données historiques
            update_data(action_key, new_data)
            st.success(f"Données pour {action_key} mises à jour avec succès!")
    with col2:
        if st.button("Annuler la mise à jour"):
            st.info("Mise à jour annulée.")
    
    # Afficher un aperçu des nouvelles données
    st.subheader("Aperçu des nouvelles données")
    st.write(new_data)

# Afficher les données historiques
if st.button("Afficher les données historiques"):
    historical_data = load_data(action_key)
    if historical_data is not None:
        st.subheader(f"Données historiques pour {action_key}")
        st.write(historical_data)
        
        # Afficher la dernière date enregistrée
        last_date = historical_data["Date"].max()
        st.info(f"Dernière date enregistrée : {last_date}")
        
        # Créer un graphique avec Altair
        st.subheader("Graphique des données historiques")
        chart = alt.Chart(historical_data).mark_line().encode(
            x="Date",
            y="Close",
            tooltip=["Date", "Close"]
        ).properties(
            title=f"Évolution du cours de {action_key}"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning(f"Aucune donnée trouvée pour {action_key}.")
