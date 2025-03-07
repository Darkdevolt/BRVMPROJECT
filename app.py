import streamlit as st
from data_manager import DataManager

# Titre de l'application
st.title("Correction de fichier CSV")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Créer une instance de DataManager
    data_manager = DataManager()
    
    # Traiter le fichier téléchargé
    df, error_message = data_manager.process_data(uploaded_file)
    
    if error_message:
        st.error(error_message)  # Afficher un message d'erreur si quelque chose s'est mal passé
    else:
        st.success("Fichier CSV traité avec succès !")
        
        # Afficher les données corrigées dans un tableau
        st.write("Données corrigées :")
        st.dataframe(df)
        
        # Option pour sauvegarder les données corrigées
        if st.button("Sauvegarder les données corrigées"):
            output_file = "data/output/corrected_data.csv"  # Chemin du fichier de sortie
            data_manager.save_corrected_csv(output_file)
            st.success(f"Données sauvegardées sous : {output_file}")
