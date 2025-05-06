import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import os

# 檔案名稱設定
input_csv = "r_stevie_moore_albums_with_tracks.csv"
original_csv = "r_stevie_moore_albums_final.csv"
delay = 1.0  # 每次抓取間隔秒數，可依情況調整

# 嘗試讀取之前抓到一半的檔案，否則就從原始清單開始
if os.path.exists(input_csv):
    print(f"🔄 從已存在的檔案繼續：{input_csv}")
    df = pd.read_csv(input_csv)
else:
    print(f"📥 從原始專輯清單開始：{original_csv}")
    df = pd.read_csv(original_csv)
    df["Track Count"] = None  # 加上欄位

# 開始抓取歌曲數
for i, row in df.iterrows():
    if pd.notna(row.get("Track Count")):
        print(f"[{i+1}/{len(df)}] ✅ 已抓過，略過：{row['Title']}")
        continue

    url = row["URL"]
    print(f"[{i+1}/{len(df)}] 抓取：{url}")
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        tracks = soup.select("tr.track_row_view")  # ✅ 正確選擇歌曲列
        df.at[i, "Track Count"] = len(tracks)
        print(f" → 抓到 {len(tracks)} 首歌")
    except Exception as e:
        print(f" ⚠️ 發生錯誤：{e}")
        df.at[i, "Track Count"] = None

    # 每筆寫入一次
    df.to_csv(input_csv, index=False)
    time.sleep(delay)

print(f"\n✅ 全部完成或已略過，最終結果已儲存至：{input_csv}")
