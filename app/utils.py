import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

API_KEY = environ.get('COINMARKETCAP_API_KEY')
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


def get_ethereum_price(SYMBOL='ETH'):
    """
    Fetches current Ethereum price data from CoinMarketCap API.

    Retrieves real-time price information, 24-hour change percentage,
    and trading volume, returning formatted data with custom min/max range values.

    Args:
        SYMBOL (str, optional): Cryptocurrency symbol. Defaults to 'ETH'.

    Returns:
        dict: Formatted price data with success status or error message
    """
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    parameters = {
        'symbol': SYMBOL,
        'convert': 'USD'
    }

    try:
        # Make API request to CoinMarketCap
        response = requests.get(API_URL, headers=headers, params=parameters)
        response.raise_for_status()

        data = response.json()

        # Extract and format price data from response
        if 'data' in data and SYMBOL in data['data']:
            eth_data = data['data'][SYMBOL]
            price = eth_data['quote']['USD']['price']
            percent_change_24h = eth_data['quote']['USD']['percent_change_24h']
            volume_24h = eth_data['quote']['USD']['volume_24h']

            return {
                'price': round(price, 2),
                'change_24h': round(percent_change_24h, 2),
                'volume_24h': round(volume_24h, 2),
                'min': environ.get('MIN_PRICE'),
                'max': environ.get('MAX_PRICE'),
                'success': True
            }
        else:
            return {'success': False, 'error': 'Data not found in API response'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}
