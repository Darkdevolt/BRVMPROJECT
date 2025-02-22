def clean_data(data):
    """
    Nettoie et formate les données récupérées.
    """
    cleaned_data = {
        'price': data['price'],
        'volume': f"{data['volume']:,}",  # Formatage du volume
        'change': data['change'],
    }
    return cleaned_data
