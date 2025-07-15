from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_SECRET

# ✅ 바이비트 세션 생성 (테스트넷)
session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_SECRET,
    testnet=True
)

def execute_trade(signal: str, symbol: str = "BTCUSDT", qty: float = 0.01):
    signal = signal.lower()
    if signal not in ["long", "short"]:
        return {"status": "error", "message": f"❌ 잘못된 신호: {signal}"}

    side = "Buy" if signal == "long" else "Sell"

    try:
        result = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel"
        )

        if result.get("retCode") == 0:
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
                "message": f"Bybit 오류: {result.get('retMsg', 'Unknown')}",
                "response": result
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
