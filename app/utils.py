import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

SYMBOL = 'ETH'
API_KEY = environ.get('COINMARKETCAP_API_KEY')
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


def get_ethereum_price():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    parameters = {
        'symbol': SYMBOL,
        'convert': 'USD'
    }

    try:
        response = requests.get(API_URL, headers=headers, params=parameters)
        response.raise_for_status()

        data = response.json()

        if 'data' in data and SYMBOL in data['data']:
            eth_data = data['data'][SYMBOL]
            price = eth_data['quote']['USD']['price']
            percent_change_24h = eth_data['quote']['USD']['percent_change_24h']

            # Valores fixos conforme solicitado: min: 4.222k e max: 4.722k
            min_price = 4222  # 4.222k em formato numérico
            max_price = 4722  # 4.722k em formato numérico

            return {
                'price': round(price, 2),
                'change_24h': round(percent_change_24h, 2),
                'min': min_price,
                'max': max_price,
                'success': True
            }
        else:
            return {'success': False, 'error': 'Dados não encontrados na resposta'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Erro na requisição: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'Erro inesperado: {str(e)}'}
