import openai
import config

openai.api_key = config.GPT_API_KEY

def decide_trade(data):
    prompt = (
        f"Symbol: {data['symbol']}, Price: {data['price']}, Signal: {data['signal']}.\n"
        "이 데이터를 참고해 'long' 또는 'short' 중 하나를 결정하세요. "
        "오직 'long'이나 'short'만 답변해주세요."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a trading assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        decision = response['choices'][0]['message']['content'].strip().lower()
        if decision not in ['long', 'short']:
            raise ValueError(f"Unexpected GPT response: {decision}")
        return decision
    except Exception as e:
        print(f"Error in decide_trade: {e}")
        return None
