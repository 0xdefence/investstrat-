## Orchestrator, runs the startup backfill and the 15-minute polling loop for 4 hours
import time
import datetime
import os
import hyperliquid_order
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file 
from api import fetch_historical_data, fetch_current_price
from signals import calculate_moving_average, generate_signal
from db import create_tables, log_signal, save_historical_prices  

def main():
    create_tables()  # Create the necessary tables
    coin_id = 'bitcoin'
    vs_currency = 'usd'
    
    # 1. Backfill historical data
    historical_prices = fetch_historical_data(coin_id, vs_currency, days=91)
    if historical_prices:
        save_historical_prices(historical_prices)
        print(f"Backfilled historical data for {len(historical_prices)} days.", flush=True)
    else:
        print("Failed to fetch historical data. Exiting.", flush=True)
        return
    
    # 2. Polling loop for 4 hours (16 iterations of 15 minutes)
    for _ in range(16):
        current_price = fetch_current_price(coin_id, vs_currency)
        if current_price is not None and historical_prices is not None:
            moving_average = calculate_moving_average(historical_prices)
            signal = generate_signal(current_price, moving_average)
            log_signal(signal, current_price)
            print(f"{datetime.datetime.now()} | {signal} | {current_price} | {moving_average:.2f}", flush=True)
            print(f"DEBUG: about to call place_order with signal={signal}", flush=True)
            try:
                order_id, status = hyperliquid_order.place_order(signal, 'BTC', 0.01)  # Example order placement
                print(f"DEBUG: place_order returned order_id={order_id}, status={status}", flush=True)
            except Exception as order_err:
                print(f"ERROR: place_order failed: {order_err}", flush=True)
        else:
            print(
                f"DEBUG: skipping order placement (current_price={current_price}, "
                f"historical_prices_is_none={historical_prices is None})",
                flush=True,
            )
        time.sleep(900)  # Sleep for 15 minutes

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")