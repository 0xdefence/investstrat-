## Fetches historical data for backfill from CoinGecko API, fetches current data for signal

## 1. Fetch historical data for backfill
import requests
import time 
def fetch_historical_data(coin_id, vs_currency, days):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': 91
    }
    max_retries = 3
    for attempt in range(max_retries):
        response = requests.get(url, params=params)  # request is FIRST
        if response.status_code == 200:
            return response.json()['prices'][-30:]
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limit. Waiting {retry_after}s. Attempt {attempt + 1}/{max_retries}")
            time.sleep(retry_after)
        else:
            print(f"Failed. Status: {response.status_code}")
            break
    return None

## 2. Fetch current data for signal generation
def fetch_current_price(coin_id, vs_currency):
    url = f'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': coin_id,
        'vs_currencies': vs_currency
    }
    max_retries = 3
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()[coin_id][vs_currency]
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limit. Waiting {retry_after}s. Attempt {attempt + 1}/{max_retries}")
            time.sleep(retry_after)
        else:
            print(f"Failed. Status: {response.status_code}")
            break
    return None