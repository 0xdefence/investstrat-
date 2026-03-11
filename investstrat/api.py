## Fetches historical data for backfill from CoinGecko API, fetches current data for signal

## 1. Fetch historical data for backfill
import requests
import time 
def fetch_historical_data(coin_id, vs_currency, days):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': 30
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['prices']  # List of [timestamp, price]
    else:
        retry_after = int(response.headers.get('Retry-After', 1))  # Default to 1 second if not provided
        print(f"Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return fetch_historical_data(coin_id, vs_currency, days)  # Retry the

## 2. Fetch current data for signal generation
def fetch_current_price(coin_id, vs_currency):
    url = f'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': coin_id,
        'vs_currencies': vs_currency
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data[coin_id][vs_currency]  # Current price
    else:
        retry_after = int(response.headers.get('Retry-After', 1))  # Default to 1 second if not provided
        print(f"Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return fetch_current_price(coin_id, vs_currency)  # Retry the request