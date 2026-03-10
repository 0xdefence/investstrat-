CREATE TABLE daily_btc_prices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    price DECIMAL(18, 8) NOT NULL
);