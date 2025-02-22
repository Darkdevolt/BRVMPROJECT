import streamlit as st
import pandas as pd
import os
import altair as alt
from utils.data_utils import load_data, save_data, update_data, clean_numeric_columns

# Titre de l'application
st.title("Analyse des actions BRVM")

# Dictionnaire complet des actions
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

# Création de la liste de recherche
search_options = list(actions_dict.keys()) + list(actions_dict.values())

# Sélection de l'action avec gestion d'erreur améliorée
selected_action = st.selectbox("Recherchez une action (nom abrégé ou nom complet)", search_options)

try:
    if selected_action in actions_dict:
        action_key = selected_action
    else:
        matches = [k for k, v in actions_dict.items() if v == selected_action]
        if not matches:
            st.error("Aucune correspondance trouvée. Veuillez sélectionner une action valide.")
            st.stop()
        action_key = matches[0]
except Exception as e:
    st.error(f"Erreur de sélection : {str(e)}")
    st.stop()

st.info(f"Action sélectionnée : {action_key} - {actions_dict[action_key]}")

# Téléchargement et traitement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lecture avec paramètres européens
        new_data = pd.read_csv(
            uploaded_file,
            parse_dates=['Date'],
            dayfirst=True,
            decimal=',',
            thousands=' '
        )
        
        # Conversion spécifique pour la colonne Volume
        if 'Vol.' in new_data.columns:
            new_data['Vol.'] = (
                new_data['Vol.']
                .astype(str)
                .str.replace('[Kk]', '', regex=True)
                .str.replace(',', '.')
                .astype(float)
                * 1000
            )
        
        # Nettoyage des données
        new_data = clean_numeric_columns(new_data)
        
        # Validation des dates
        if new_data['Date'].isnull().any():
            st.error("Format de date invalide! Utilisez JJ/MM/AAAA")
            st.stop()

        # Interface de confirmation
        st.warning("Voulez-vous vraiment mettre à jour les données? Cette action est irréversible.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmer la mise à jour"):
                update_data(action_key, new_data)
                st.success(f"Données pour {action_key} mises à jour avec succès!")
        with col2:
            if st.button("Annuler la mise à jour"):
                st.info("Mise à jour annulée.")
        
        # Affichage des données
        st.subheader("Aperçu des nouvelles données")
        st.dataframe(new_data.style.format({
            'Vol.': '{:,.0f}',
            'Variation %': '{:.2f}%'
        }))

    except Exception as e:
        st.error(f"Erreur de traitement du fichier : {str(e)}")
        st.stop()

# Affichage des données historiques
if st.button("Afficher les données historiques"):
    try:
        historical_data = load_data(action_key)
        
        if historical_data is not None:
            st.subheader(f"Données historiques pour {action_key}")
            st.dataframe(historical_data)
            
            # Dernière date disponible
            last_date = historical_data["Date"].max().strftime('%d/%m/%Y')
            st.info(f"Dernière mise à jour : {last_date}")
            
            # Visualisation graphique
            chart = alt.Chart(historical_data).mark_line().encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Close:Q', title='Cours de clôture'),
                tooltip=['Date', 'Close']
            ).properties(
                title=f'Évolution historique de {action_key}',
                width=800,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Aucune donnée historique disponible pour cette action.")
            
    except Exception as e:
        st.error(f"Erreur de chargement des données : {str(e)}")
        st.stop()
