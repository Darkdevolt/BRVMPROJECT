import streamlit as st
import pandas as pd
import os
from utils.data_utils import load_data, save_data, update_data

# Titre de l'application
st.title("Analyse des actions BRVM")

# Liste complète des actions BRVM
actions = [
    "ABJC", "BICC", "BNBC", "BOAB", "BOABF", "BOAC", "BOAM", "BOAN", "BOAS",
    "CABC", "CBIBF", "CFAC", "CIEC", "ECOC", "ETIT", "FTSC", "LNBB", "NEIC",
    "NSBC", "NTLC", "ONTBF", "ORAC", "ORGT", "PALC", "PRSC", "SAFC", "SCRC",
    "SDCC", "SDSC", "SEMC", "SGBC", "SHEC", "SIBC", "SICC", "SIVC", "SLBC",
    "SMBC", "SNTS", "SOGC", "SPHC", "STAC", "STBC", "SVOC", "TTLC", "TTLS",
    "TTRC", "UNLC", "UNXC"
]

# Liste déroulante pour sélectionner l'action
selected_action = st.selectbox("Sélectionnez l'action", actions)

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez le fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le fichier CSV téléchargé
    new_data = pd.read_csv(uploaded_file)
    
    # Afficher un aperçu des nouvelles données
    st.subheader("Aperçu des nouvelles données")
    st.write(new_data)
    
    # Boîte de dialogue de confirmation
    st.warning("Voulez-vous vraiment mettre à jour les données ? Cette action écrasera les données existantes.")
    if st.button("Confirmer la mise à jour"):
        # Mettre à jour les données historiques
        update_data(selected_action, new_data)
        st.success(f"Données pour {selected_action} mises à jour avec succès!")
    else:
        st.info("Mise à jour annulée.")

# Afficher les données historiques
if st.button("Afficher les données historiques"):
    historical_data = load_data(selected_action)
    if historical_data is not None:
        st.subheader(f"Données historiques pour {selected_action}")
        st.write(historical_data)
    else:
        st.warning(f"Aucune donnée trouvée pour {selected_action}.")
