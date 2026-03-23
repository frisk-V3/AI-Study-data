import time
import os
import json
import requests
from datetime import datetime

# --- frisk-V3 設定 ---
TRAIN_LIMIT = 20 * 60  # 20分
USER_AGENT = "frisk-V3/1.0 (contact: yuniaochaoyang@gmail.com)"
DATA_FILE = "data/learned_data.json"

def fetch_wiki_full(title):
    url = "https://ja.wikipedia.org"
    params = {
        "action": "query", "format": "json", "titles": title,
        "prop": "extracts", "explaintext": True, "redirects": 1
    }
    try:
        res = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=15)
        pages = res.json().get("query", {}).get("pages", {})
        for pid in pages:
            return pages[pid].get("extract", "")
    except:
        return ""

def main():
    os.makedirs("data", exist_ok=True)
    start_time = time.time()
    
    # 記憶をロード
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            memory = json.load(f)
    else:
        # 初回は空のリストと既読リスト、未読キューを作成
        memory = {"total_pages": 0, "history": [], "queue": ["Python", "JavaScript", "GitHub", "機械学習", "アルゴリズム"], "knowledge": []}

    print(f"frisk-V3 本気モード開始: {datetime.now()}")

    # 20分経つか、キューが空になるまでループ
    while (time.time() - start_time) < TRAIN_LIMIT and memory["queue"]:
        target = memory["queue"].pop(0) # 次の獲物を取り出す
        
        if target in memory["history"]:
            continue

        print(f"学習中: {target} (詳細を取得中...)")
        full_text = fetch_wiki_full(target)
        
        if full_text:
            # 【重要】詳細を丸ごと保存
            memory["knowledge"].append({
                "keyword": target,
                "details": full_text, # ここにWikipediaの全本文が入る！
                "timestamp": str(datetime.now())
            })
            memory["history"].append(target)
            memory["total_pages"] += 1
            
            # 簡易的に次のキーワードを増やす（本文から単語を拾うロジックは次で！）
            # とりあえず止まらないように予備を入れる
            if len(memory["queue"]) < 3:
                memory["queue"].extend(["コンパイラ", "データ構造", "OpenAI"])
            
            time.sleep(1) # マナー

    # 最終的な成果を保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
    print(f"完了！合計 {memory['total_pages']} ページの詳細を保存したぞ。")

if __name__ == "__main__":
    main()
