import os
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

# .env 절대 경로 지정 + override
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path, override=True)

# 환경변수 → 파이썬 변수로 저장
GPT_API_KEY = os.getenv("GPT_API_KEY")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_SECRET")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")

# ✅ 확인용 출력 (개발 중만 사용, 이후 삭제 권장)
print("✅ GPT 키:", GPT_API_KEY[:10] + "..." if GPT_API_KEY else "❌ 없음")
