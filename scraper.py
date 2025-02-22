from bs4 import BeautifulSoup
import requests

def fetch_finance_data():
    """
    Récupère les données financières depuis Sika Finance.
    """
    url = "https://www.sika-finance.com"  # Remplacez par l'URL réelle
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lève une exception si la requête échoue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Exemple : Récupération du cours de l'action (à adapter selon la structure HTML)
        price_element = soup.find('span', {'class': 'price'})
        if price_element:
            price = price_element.text.strip()
        else:
            price = "N/A"
        
        # Exemple de données (à adapter selon les informations disponibles)
        data = {
            'price': price,
            'volume': "100,000",  # Exemple de volume
            'change': "+1.5%",  # Exemple de variation
        }
        return data
    except requests.RequestException as e:
        return {"error": f"Erreur lors de la récupération des données : {e}"}
