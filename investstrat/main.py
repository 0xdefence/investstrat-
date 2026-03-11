## Orchestrator, runs the startup backfill and the 15-minute polling loop for 4 hours
import time
import datetime
from api import fetch_historical_data, fetch_current_price
from signals import calculate_moving_average, generate_signal
from db import log_signal, save_historical_prices       

def main():
    coin_id = 'bitcoin'
    vs_currency = 'usd'
    
    # 1. Backfill historical data
    historical_prices = fetch_historical_data(coin_id, vs_currency, days=91)
    if historical_prices:
        save_historical_prices(historical_prices)
        print(f"Backfilled historical data for {len(historical_prices)} days.")
    else:
        print("Failed to fetch historical data. Exiting.")
        return
    
    # 2. Polling loop for 4 hours (16 iterations of 15 minutes)
    for _ in range(16):
        current_price = fetch_current_price(coin_id, vs_currency)
        if current_price is not None and historical_prices is not None:
            moving_average = calculate_moving_average(historical_prices)
            signal = generate_signal(current_price, moving_average)
            log_signal(signal, current_price)
            print(f"{datetime.datetime.now()} | {signal} | {current_price} | {moving_average}")

        time.sleep(900)  # Sleep for 15 minutes