from flask import Flask, request, jsonify
from config import WEBHOOK_SECRET
from gpt_logic import decide_trade
from utils.trade_executor import execute_trade
from utils.snapshot import save_snapshot_from_text
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 웹훅 수신:", data)

    # 1. 보안 체크
    if not data or data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # 2. GPT 판단 로직에 JSON 전체 전달 (text로 변환 가능)
    json_text = json.dumps(data, ensure_ascii=False)
    gpt_signal = decide_trade(data)
    if not gpt_signal:
        return jsonify({"error": "GPT 판단 실패"}), 400

    symbol = data.get("symbol", "BTCUSDT")
    qty = float(data.get("qty", 0.01))

    # 3. Bybit 매매 실행
    result = execute_trade(signal=gpt_signal, symbol=symbol, qty=qty)

    # 4. 스냅샷 저장 (수신된 전체 JSON 문자열 저장)
    save_snapshot_from_text(json_text=json_text)

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
