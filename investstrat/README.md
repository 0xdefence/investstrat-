# InvestStrat

A Python + PostgreSQL trading-signal prototype that:

- Fetches BTC/USD data from CoinGecko
- Backfills recent historical prices
- Computes a simple moving average
- Generates a basic LONG/SHORT signal
- Logs prices and signals to PostgreSQL

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
   - Prints log line in this format:

```text
TIMESTAMP | LONG OR SHORT | PRICE VALUE | MOVING AVG VALUE
```

## Tech Stack

- Python
- PostgreSQL
- CoinGecko API

## Project Structure

- `main.py`: Orchestrates startup backfill + 15-minute polling loop
- `api.py`: CoinGecko API calls for historical and live prices
- `signals.py`: Moving-average calculation + signal generation
- `db.py`: PostgreSQL connection + inserts/table creation
- `db.sql`: SQL table schema reference
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
pip install requests python-dotenv psycopg2-binary
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
python main.py
```

Expected behavior:

- Backfills recent historical prices
- Logs one signal every 15 minutes
- Runs for ~4 hours total (16 iterations)

Example output:

```text
2026-03-11 10:15:00.123456 | LONG | 84250.11 | 83620.44
```

## Notes About Current Implementation

- `api.py` currently hardcodes historical `days` to `91` and returns the last 30 data points from that response.
- The moving average is calculated from the in-memory historical list fetched at startup.
- Historical backfill is inserted each run and may create duplicate dates unless deduplicated at DB level.

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
  - Re-run dependency installation.

## Security

- Never commit `.env`.
- Keep DB credentials out of source control.

## Future Improvements

- Add `requirements.txt` and pinned versions.
- Add unique constraints for historical rows.
- Refresh moving average with live appended data.
- Add unit tests for signal and API layers.
- Add structured logging and metrics.
