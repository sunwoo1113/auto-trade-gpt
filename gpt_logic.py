import openai
import os
import requests
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from utils import trade_executor  # trade_executor.py 연동

# 환경 변수 로드 및 설정
load_dotenv()
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")
openai.api_key = os.getenv("GPT_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Firebase 초기화
cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def send_telegram_message(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            requests.post(url, data=payload)
        except Exception as e:
            print(f"[텔레그램 알림 오류] {e}")

def get_latest_open_trade(symbol):
    try:
        docs = db.collection("trades").where("symbol", "==", symbol).where("closed", "==", False).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).stream()
        for doc in docs:
            return doc.id, doc.to_dict()
        return None, None
    except Exception as e:
        print(f"[Firestore 조회 오류] {e}")
        return None, None

def close_trade_in_firestore(doc_id):
    try:
        db.collection("trades").document(doc_id).update({"closed": True})
    except Exception as e:
        print(f"[Firestore 업데이트 오류] {e}")

def check_exit_condition(current_price, trade):
    side = trade["gpt_action"].lower()
    tp = trade["take_profit"]
    sl = trade["stop_loss"]

    if side == "buy":
        if current_price >= tp:
            return "TP"
        elif current_price <= sl:
            return "SL"
    elif side == "sell":
        if current_price <= tp:
            return "TP"
        elif current_price >= sl:
            return "SL"
    return None

def monitor_and_close_trade(symbol, current_price):
    doc_id, trade = get_latest_open_trade(symbol)
    if not trade:
        return

    status = check_exit_condition(current_price, trade)
    if status:
        close_trade_in_firestore(doc_id)
        message = f"🚨 {symbol} 거래 종료됨: {status}\n진입가: {trade['entry_price']} → 현재가: {current_price}"
        print(f"✅ {message}")
        send_telegram_message(message)

def gpt_trade_executor(data):
    try:
        position = trade_executor.get_open_position(data['symbol'])

        position_info = ""
        if position['status'] == 'open':
            position_info = (
                f"현재 {data['symbol']}에 대해 {position['side']} 포지션이 열려 있습니다.\n"
                f"- 진입가: {position['entry_price']}\n"
                f"- 사이즈: {position['size']}\n"
                "이 포지션이 아직 종료되지 않은 상태에서, 추가 진입이 적절한지 판단해 주세요.\n\n"
            )

        prompt = f"""
{position_info}
다음은 트레이딩 봇에 입력된 실시간 시황 데이터입니다.

- 심볼: {data['symbol']}
- 현재가: {data['entry']}
- 손절가: {data['stopLoss']}
- 익절1: {data['takeProfit1']}
- 익절2: {data['takeProfit2']}
- RSI: {data['rsi']}, MACD Histogram: {data['macdHist']}, ATR: {data['atr']}
- 시장 상황: {data['marketRegime']}
- 신호 패턴: {data['pattern']}

이 정보들을 기반으로,
1. 현재 진입해야 하는가? (Yes/No)
2. 진입한다면 방향은? (long/short)
3. 목표가 도달 시 익절은 TP1까지만 할지, TP2까지 갈지 판단
4. 판단 이유를 간단히 기술

오직 다음 포맷으로 응답하세요:
{{"action": "Buy"/"Sell"/"Wait", "target": "TP1"/"TP2"/"SL", "reason": "..." }}
        """.strip()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 숙련된 트레이딩 봇입니다. 지표와 시장상황을 종합적으로 분석하여 정확히 판단하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        reply = response['choices'][0]['message']['content']
        decision = eval(reply.strip())

        if decision["action"].lower() == "wait":
            print("⏸️ GPT 판단: 진입하지 않음")
            return

        side = 'buy' if decision["action"].lower() == 'buy' else 'sell'
        target_tp = data['takeProfit1'] if decision["target"] == 'TP1' else data['takeProfit2']

        order_result = trade_executor.place_market_order(
            symbol=data['symbol'],
            side=side,
            quantity=data.get('qty', 0.01)
        )
        if order_result['status'] != 'success':
            raise Exception(order_result['message'])

        trade_record = {
            "symbol": data['symbol'],
            "gpt_action": decision["action"],
            "target": decision["target"],
            "entry_price": data['entry'],
            "executed_price": order_result['price'],
            "take_profit": target_tp,
            "stop_loss": data['stopLoss'],
            "order_id": order_result['id'],
            "timestamp": order_result['timestamp'],
            "reason": decision["reason"],
            "raw_input": data,
            "closed": False
        }
        db.collection("trades").add(trade_record)
        print("✅ GPT 판단에 따른 거래 완료 및 저장됨:", trade_record)

        send_telegram_message(f"🚀 거래 실행됨: {decision['action']} {data['symbol']} @ {order_result['price']}")

    except Exception as e:
        print(f"❌ GPT 판단/실행 오류: {e}")