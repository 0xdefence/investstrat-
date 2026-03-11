## Signal compares polling data on a 15m timeframe (self chosen) and 30 day moving average
def calculate_moving_average(prices):
    extracted = [entry[1] for entry in prices]
    return sum(extracted) / len(extracted)

def generate_signal(current_price, moving_average):
    return 'LONG' if current_price > moving_average else 'SHORT'