import csv
import pandas as pd

class DataManager:
    def __init__(self):
        """
        Initialise la classe DataManager.
        """
        self.corrected_data = []  # Pour stocker les données corrigées
        self.header = None  # Pour stocker l'en-tête du fichier CSV

    def process_data(self, uploaded_file):
        """
        Traite le fichier CSV téléchargé via Streamlit.
        :param uploaded_file: Fichier téléchargé via Streamlit.
        :return: DataFrame des données corrigées et un message d'erreur (ou None si tout va bien).
        """
        try:
            # Lire le fichier CSV avec pandas
            df = pd.read_csv(uploaded_file)
            
            # Vérifier si le fichier a les colonnes attendues
            expected_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
            if not all(col in df.columns for col in expected_columns):
                return None, "Le fichier CSV ne contient pas les colonnes attendues."
            
            # Stocker les données corrigées
            self.corrected_data = df.values.tolist()
            self.header = df.columns.tolist()
            
            # Retourner le DataFrame et aucun message d'erreur
            return df, None
        
        except Exception as e:
            # En cas d'erreur, retourner None et le message d'erreur
            return None, f"Erreur lors du traitement du fichier : {str(e)}"

    def save_corrected_csv(self, output_file):
        """
        Sauvegarde les données corrigées dans un nouveau fichier CSV.
        :param output_file: Chemin du fichier CSV de sortie.
        """
        if not self.corrected_data:
            print("Aucune donnée corrigée à sauvegarder.")
            return
        
        # Écrire les données corrigées dans un nouveau fichier CSV
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(self.header)  # Écrire l'en-tête
            writer.writerows(self.corrected_data)  # Écrire les données
        
        print(f"Fichier corrigé enregistré sous : {output_file}")

    def get_corrected_data(self):
        """
        Retourne les données corrigées.
        :return: Liste des données corrigées (y compris l'en-tête).
        """
        return self.corrected_data
