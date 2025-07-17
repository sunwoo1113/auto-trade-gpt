from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json

from gpt_logic import gpt_trade_executor
from utils.snapshot import save_snapshot_from_text

# 초기 설정
load_dotenv()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 웹훅 수신:", data)

    # 1. 보안 체크
    if not data or data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # 2. 스냅샷 저장 (로깅)
    json_text = json.dumps(data, ensure_ascii=False)
    save_snapshot_from_text(json_text=json_text)

    # 3. GPT 기반 판단 및 자동 매매 실행
    try:
        gpt_trade_executor(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
