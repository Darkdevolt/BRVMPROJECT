import streamlit as st
import data_manager

st.title("📊 Gestion des Données CSV")

# Téléverser un fichier CSV
uploaded_file = st.file_uploader("Déposez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Traiter les données
    df, error_message = data_manager.process_data(uploaded_file)
    
    if error_message:
        st.error(error_message)  # Afficher le message d'erreur
    else:
        st.success("✅ Succès : Le fichier est valide et les données manquantes ont été traitées !")
        
        # Afficher les données traitées
        st.write("Aperçu des données traitées :")
        st.dataframe(df)
        
        # Option pour télécharger les données traitées
        st.download_button(
            label="Télécharger les données traitées",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="donnees_traitees.csv",
            mime="text/csv"
        )
