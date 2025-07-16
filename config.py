import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path, override=True)

GPT_API_KEY = os.getenv("GPT_API_KEY")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_SECRET")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
