import time
import os
import json
import requests
from datetime import datetime

# --- frisk-V3 設定 ---
TRAIN_LIMIT = 20 * 60  # 20分間フル稼働
USER_AGENT = "frisk-V3/1.0 (contact: yuniaochaoyang@gmail.com)"
DATA_FILE = "data/learned_data.json"
TARGET_KEYWORDS = ["Python", "JavaScript", "アルゴリズム", "機械学習", "GitHub"] # 最初はこの辺から

def fetch_wiki(title):
    url = "https://ja.wikipedia.org"
    params = {"action": "query", "format": "json", "titles": title, "prop": "extracts", "explaintext": True}
    try:
        res = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        pages = res.json().get("query", {}).get("pages", {})
        for pid in pages:
            return pages[pid].get("extract", "")
    except:
        return ""

def main():
    os.makedirs("data", exist_ok=True)
    start_time = time.time()
    
    # 既存の記憶をロード
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            memory = json.load(f)
    else:
        memory = {"total_pages": 0, "knowledge": []}

    print(f"frisk-V3 学習開始: {datetime.now()}")

    for kw in TARGET_KEYWORDS:
        # 20分経過したら即終了
        if (time.time() - start_time) > TRAIN_LIMIT:
            break
            
        text = fetch_wiki(kw)
        if text:
            # 取得したテキストを要約したりパターン抽出したりする（ここが本気の見せ所）
            memory["knowledge"].append({
                "keyword": kw,
                "text_snippet": text[:500], # 最初は500文字ずつ蓄積
                "timestamp": str(datetime.now())
            })
            memory["total_pages"] += 1
            print(f"Success: {kw} を学習したぞ")
            time.sleep(1) # Wikipediaへの最低限の礼儀

    # 保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
