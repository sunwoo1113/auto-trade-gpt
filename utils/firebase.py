import os
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase 인증 초기화
cred_path = os.getenv("FIREBASE_CRED_PATH")
if cred_path and not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_trade_snapshot(data: dict):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    doc_id = uuid.uuid4().hex

    data["timestamp"] = timestamp

    try:
        db.collection("trade_logs").document(doc_id).set(data)
        print(f"✅ Firebase 업로드 완료: {timestamp}")
    except Exception as e:
        print(f"❌ Firebase 업로드 실패: {e.__class__.__name__} - {str(e)}")
