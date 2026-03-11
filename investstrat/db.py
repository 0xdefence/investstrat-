## logs signals and data into a PostgreSQL database
from dotenv import load_dotenv
import os
import psycopg2

def get_connection():
    load_dotenv()
    host = os.getenv('DB_HOST')
    conn = psycopg2.connect(
        host=host,
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_btc_prices (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            price DECIMAL(30, 8) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS live_btc_prices (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            price DECIMAL(30, 8) NOT NULL,
            long_or_short VARCHAR(10) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def log_signal(signal, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO live_btc_prices (timestamp, price, long_or_short) VALUES (NOW(), %s, %s)",
        (price, signal)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
def save_historical_prices(prices):
    conn = get_connection()
    cursor = conn.cursor()
    for date, price in prices:
        cursor.execute(
            "INSERT INTO daily_btc_prices (date, price) VALUES (to_timestamp(%s / 1000.0)::date, %s)",
            (date, price)
        )
    conn.commit()
    cursor.close()
    conn.close()    