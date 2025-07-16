from flask import Flask, request, jsonify
from config import WEBHOOK_SECRET
from trade_executor import execute_trade
from utils.snapshot import save_snapshot
from utils.firebase import upload_trade_snapshot

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 웹훅 수신:", data)

    # 1. 보안 체크
    if not data or data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "❌ Invalid secret"}), 403

    # 2. 신호 파싱 (Buy → long, Sell → short)
    signal_map = {"Buy": "long", "Sell": "short", "Long": "long", "Short": "short"}
    signal = signal_map.get(data.get("signal"))
    if not signal:
        return jsonify({"error": "❌ Unknown signal"}), 400

    symbol = data.get("symbol", "BTCUSDT")
    qty = float(data.get("qty", 0.01))

    # 3. 매매 실행
    result = execute_trade(signal=signal, symbol=symbol, qty=qty)

    # 4. 기록 저장
    save_snapshot(result)
    upload_trade_snapshot(result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
