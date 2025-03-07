import data_manager

def main():
    # Chemin du fichier CSV
    file_path = "HistoricalPrices.csv"
    
    # Traiter les données
    df = data_manager.process_data(file_path)
    
    if df is not None:
        print("Données traitées avec succès !")
        print(df.head())  # Afficher les premières lignes du DataFrame traité
    else:
        print("Le traitement des données a échoué.")

if __name__ == "__main__":
    main()
