# place_order function that takes signal, coin and sz as parameters. maps signal to is_buy - long (true) or short (false). then calls the hyperliquid API to place the order. returns the order id and status, 
# however, don't PLACE REAL ORDERS, just print the order details to the console for now. also handle any potential errors from the API call and print them to the console.
import requests
def place_order(signal, coin, sz):
    print(f"placed order called with signal: {signal}, coin: {coin}, size: {sz}", flush=True)
    is_buy = signal == 'LONG'
    order_details = {
        'coin': coin,
        'size': sz,
        'side': 'long' if is_buy else 'short'
    }
    # Simulate API call to Hyperliquid
    try:
        # this is where API call SHOULD Go but for now just order details 
        print(f"Placing order: {order_details}", flush=True)
        # Simulate a successful response
        order_id = "12345"  #what api response would return 
        status = "success"  #also from order response 
        print(f"Demo order result: order_id={order_id}, status={status}", flush=True)
        return order_id, status
    except Exception as e:
        print(f"Error placing order: {e}", flush=True)
        return None, "error" 