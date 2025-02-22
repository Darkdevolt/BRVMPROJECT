import requests
from bs4 import BeautifulSoup

def fetch_finance_data():
    """
    Récupère les données financières depuis Sika Finance.
    """
    url = "https://www.sika-finance.com"  # Remplacez par l'URL réelle
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Exemple : Récupération du cours de l'action
        price = soup.find('span', {'class': 'price'}).text  # Adaptez selon la structure HTML
        
        # Exemple de données (à adapter selon les informations disponibles)
        data = {
            'price': float(price.replace(',', '')),  # Convertir en float
            'volume': 100000,  # Exemple de volume
            'change': '+1.5%',  # Exemple de variation
        }
        return data
    else:
        raise Exception(f"Erreur lors de la récupération des données : {response.status_code}")
