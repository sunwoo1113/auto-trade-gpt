import json
import os
from datetime import datetime

def save_snapshot_from_text(json_text: str, image_path: str = None):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(log_dir, f"snapshot_{timestamp}.json")

    try:
        data = json.loads(json_text)
        if image_path:
            data["image"] = image_path
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📸 Snapshot saved: {filename}")
    except Exception as e:
        print(f"❌ Snapshot save failed: {e}")
