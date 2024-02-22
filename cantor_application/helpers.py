from requests import get
import requests

def lookup(symbol: str):
    """ This function queries the NBP (National Bank of Poland) Web API to retrieve the
        exchange rate for the specified currency symbol.

        Returns:
            tuple: when symbol does not exist in API.
                - If the symbol does not exist in the API, returns (None, None).
                - If the request is successful, returns a tuple
                  with the currency exchange rate (float) and the name of the currency (str)
        """

    # NBP Web API
    url = f'http://api.nbp.pl/api/exchangerates/rates/A/{symbol}/'

    try:
        with get(url, timeout=10) as content:
            content.raise_for_status()

            data = content.json()

            currency = data['rates'][0]['mid']
            currency_name = data['currency']

            return currency, currency_name
    except (
        ValueError, KeyError, IndexError,
        requests.exceptions.RequestException, requests.exceptions.HTTPError
        ):
        return None, None
