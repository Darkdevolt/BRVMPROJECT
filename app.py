import streamlit as st
import data_manager

def main():
    st.title("Gestion des données CSV")
    
    # Téléverser un fichier CSV
    uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Traiter les données
        df = data_manager.process_data(uploaded_file)
        
        if df is not None:
            st.success("Données traitées avec succès !")
            st.write("Aperçu des données :")
            st.dataframe(df)  # Afficher le DataFrame traité
        else:
            st.error("Le traitement des données a échoué. Vérifiez la structure du fichier CSV.")

if __name__ == "__main__":
    main()
