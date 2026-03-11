CREATE TABLE daily_btc_prices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    price DECIMAL(30, 8) NOT NULL
);

CREATE TABLE live_btc_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    price DECIMAL(30, 8) NOT NULL,
    long_or_short VARCHAR(10) NOT NULL
    );