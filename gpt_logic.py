# GPT 판단 로직
import openai
import config

def decide_trade(data):
    prompt = f"Symbol: {data['symbol']}, Price: {data['price']}, Signal: {data['signal']}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "롱 또는 숏 중 하나를 판단하라."},
                 {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip().lower()