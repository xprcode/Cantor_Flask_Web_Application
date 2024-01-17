from requests import get
import requests

def lookup(symbol):
    """Look up quote for symbol."""
    
    # NBP Web API
    url = f'http://api.nbp.pl/api/exchangerates/rates/A/{symbol}/'
    
    try:
        # Query API
        with get(url) as content:
            content.raise_for_status()
            
            data = content.json()
            
            currency = data['rates'][0]['mid']
            
            return currency
    except (ValueError, KeyError, IndexError, requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        return None
    



    
