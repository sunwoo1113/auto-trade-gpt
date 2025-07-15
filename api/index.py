# Vercel 서버리스 엔드포인트
from flask import Request
import json

def handler(request: Request):
    data = request.get_json()
    return json.dumps({"status": "received", "price": data.get("price")}), 200, {"Content-Type": "application/json"}