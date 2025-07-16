from bybit import Bybit
from config import BYBIT_API_KEY, BYBIT_SECRET

client = Bybit(
    testnet=True,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_SECRET
)

def execute_trade(signal: str, symbol: str = "BTCUSDT", qty: float = 0.01):
    signal = signal.lower()
    if signal not in ["long", "short"]:
        return {"status": "error", "message": f"Invalid signal: {signal}"}

    side = "Buy" if signal == "long" else "Sell"

    try:
        result = client.place_active_order(
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel"
        )

        if result.get("ret_code") == 0:
            return {
                "status": "success",
                "signal": signal,
                "side": side,
                "symbol": symbol,
                "qty": qty,
                "response": result
            }
        else:
            return {
                "status": "error",
                "message": f"Bybit error: {result.get('ret_msg', 'Unknown')}",
                "response": result
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
