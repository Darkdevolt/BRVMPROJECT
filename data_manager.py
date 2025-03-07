import csv

class DataManager:
    def __init__(self, input_file):
        self.input_file = input_file
        self.corrected_data = []  # Pour stocker les données corrigées
        self.header = None  # Pour stocker l'en-tête du fichier CSV

    def correct_csv(self):
        """
        Lit le fichier CSV, corrige les lignes incomplètes et stocke les données corrigées.
        """
        # Ouvrir le fichier CSV d'entrée
        with open(self.input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            
            # Lire l'en-tête (première ligne)
            self.header = next(reader)
            self.corrected_data.append(self.header)  # Ajouter l'en-tête aux données corrigées
            
            # Vérifier chaque ligne
            for row in reader:
                # Si la ligne a le bon nombre de colonnes (6 colonnes dans ce cas)
                if len(row) == 6:
                    self.corrected_data.append(row)  # Ajouter la ligne aux données corrigées
                else:
                    print(f"Ignoré : Ligne incomplète : {row}")  # Afficher un message pour les lignes incomplètes

    def save_corrected_csv(self, output_file):
        """
        Sauvegarde les données corrigées dans un nouveau fichier CSV.
        """
        if not self.corrected_data:
            print("Aucune donnée corrigée à sauvegarder.")
            return
        
        # Écrire les données corrigées dans un nouveau fichier CSV
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(self.corrected_data)
        
        print(f"Fichier corrigé enregistré sous : {output_file}")

    def get_corrected_data(self):
        """
        Retourne les données corrigées.
        """
        return self.corrected_data
