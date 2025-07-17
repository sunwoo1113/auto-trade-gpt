import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# 환경 변수 로딩
load_dotenv()
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_SECRET")
BYBIT_TESTNET = os.getenv("BYBIT_TESTNET", "true").lower() == "true"
BYBIT_SYMBOL = os.getenv("BYBIT_SYMBOL", "BTCUSDT")

# Bybit 클라이언트 생성
client = bybit.bybit(  # ✅ 수정: 'Bybit(...)' → 'bybit.bybit(...)'
    test=BYBIT_TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_SECRET
)


def setup_leverage_and_margin(symbol: str, leverage: int = 1, mode: str = "Isolated"):
    """
    레버리지 및 마진 모드 설정 (테스트용)
    """
    try:
        margin_result = client.set_margin_mode(symbol=symbol, mode=mode)
        leverage_result = client.set_leverage(symbol=symbol, buy_leverage=leverage, sell_leverage=leverage)
        return {
            "status": "success",
            "margin": margin_result,
            "leverage": leverage_result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def place_market_order(symbol: str, side: str, quantity: float):
    """
    Bybit에 시장가 주문 실행
    side: "buy" 또는 "sell"
    """
    try:
        # 진입 전 설정: 격리모드, 1배 레버리지
        setup_leverage_and_margin(symbol, leverage=1, mode="Isolated")

        result = client.place_active_order(
            symbol=symbol,
            side=side.capitalize(),  # Buy / Sell
            order_type="Market",
            qty=quantity,
            time_in_force="GoodTillCancel"
        )

        if result.get("ret_code") == 0 and result.get("result"):
            return {
                "status": "success",
                "price": result["result"].get("avg_fill_price"),
                "id": result["result"].get("order_id"),
                "timestamp": result.get("time_now")
            }
        else:
            return {
                "status": "error",
                "message": result.get("ret_msg", "Unknown error"),
                "response": result
            }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }

def get_open_position(symbol: str):
    """
    현재 해당 심볼에 열린 포지션 정보를 반환
    """
    try:
        pos_data = client.get_position(symbol=symbol)
        result = pos_data.get("result")
        if result and float(result.get("size", 0)) > 0:
            return {
                "status": "open",
                "side": result["side"].lower(),
                "size": float(result["size"]),
                "entry_price": float(result["entry_price"])
            }
        else:
            return {"status": "closed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
