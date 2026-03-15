# InvestStrat

A Python + PostgreSQL trading-signal prototype that:

- Fetches BTC/USD data from CoinGecko
- Backfills recent historical prices
- Computes a simple moving average
- Generates a basic LONG/SHORT signal
- Logs prices and signals to PostgreSQL
- Simulates Hyperliquid demo order placement for each generated signal

The current implementation is designed around a 4-hour runtime window with polling every 15 minutes.

## What It Does

1. Creates required PostgreSQL tables (if they do not exist).
2. Fetches historical BTC prices from CoinGecko.
3. Stores historical prices in `daily_btc_prices`.
4. Runs a loop for 16 iterations (4 hours total):
   - Fetches live BTC price
   - Computes moving average from historical prices
   - Generates signal:
     - `LONG` if current price > moving average
     - `SHORT` otherwise
   - Logs result to `live_btc_prices`
   - Calls demo order placement in `hyperliquid_order.py`
   - Prints log line in this format:

```text
TIMESTAMP | LONG OR SHORT | PRICE VALUE | MOVING AVG VALUE
```

## Tech Stack

- Python
- PostgreSQL
- CoinGecko API
- Hyperliquid order simulator (demo mode)

## Project Structure

- `main.py`: Orchestrates startup backfill + 15-minute polling loop
- `api.py`: CoinGecko API calls for historical and live prices
- `signals.py`: Moving-average calculation + signal generation
- `db.py`: PostgreSQL connection + inserts/table creation
- `hyperliquid_order.py`: Demo order placement function used after each signal
- `db.sql`: SQL table schema reference
- `requirements.txt`: Python dependency manifest
- `.env.example`: Environment variable template
- `guide.md`: Original assignment/spec

## Prerequisites

- Python 3.10+
- PostgreSQL running locally or remotely
- Network access to CoinGecko API

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in values:

```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

## Database

You can let the app create tables automatically via `create_tables()` in `db.py`, or manually create schema using `db.sql`.

Tables:

- `daily_btc_prices`
  - `id` SERIAL PRIMARY KEY
  - `date` DATE NOT NULL
  - `price` DECIMAL(30,8) NOT NULL

- `live_btc_prices`
  - `id` SERIAL PRIMARY KEY
  - `timestamp` TIMESTAMP NOT NULL
  - `price` DECIMAL(30,8) NOT NULL
  - `long_or_short` VARCHAR(10) NOT NULL

## Run

```bash
python3 main.py
```

Expected behavior:

- Backfills recent historical prices
- Logs one signal every 15 minutes
- Prints demo order details for each generated signal
- Runs for ~4 hours total (16 iterations)

Example output:

```text
2026-03-11 10:15:00.123456 | LONG | 84250.11 | 83620.44
DEBUG: about to call place_order with signal=LONG
placed order called with signal: LONG, coin: BTC, size: 0.01
Placing order: {'coin': 'BTC', 'size': 0.01, 'side': 'long'}
Demo order result: order_id=12345, status=success
```

## Notes About Current Implementation

- `api.py` currently hardcodes historical `days` to `91` and returns the last 30 data points from that response.
- The moving average is calculated from the in-memory historical list fetched at startup.
- Historical backfill is inserted each run and may create duplicate dates unless deduplicated at DB level.
- Hyperliquid integration is demo-only right now and does not submit live orders.

## Troubleshooting

- Connection errors:
  - Verify PostgreSQL is running.
  - Verify `.env` values are correct.
  - Ensure user has INSERT/CREATE privileges.

- CoinGecko rate-limit responses (`429`):
  - The code retries up to 3 times using `Retry-After`.
  - Retry later if all attempts fail.

- Missing Python modules:
  - Ensure virtual environment is active.
  - Re-run `pip install -r requirements.txt`.

## Security

- Never commit `.env`.
- Keep DB credentials out of source control.

## Future Improvements

- Add unique constraints for historical rows.
- Refresh moving average with live appended data.
- Add unit tests for signal and API layers.
- Add structured logging and metrics.
- Add real Hyperliquid API integration behind a feature flag.
