import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("🚫 Telegram 설정 누락")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        if response.ok:
            print("✅ 텔레그램 전송 완료")
        else:
            print("❌ 텔레그램 전송 실패", response.text)
    except Exception as e:
        print("❌ Telegram 예외:", str(e))
