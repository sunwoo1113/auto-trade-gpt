# utils/snapshot.py

import os
import json
from datetime import datetime

def save_snapshot(data):
    # 1. 저장할 디렉토리
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 2. 타임스탬프 기반 파일명
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{log_dir}/snapshot_{timestamp}.json"

    # 3. JSON 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"📸 스냅샷 저장됨: {filename}")
