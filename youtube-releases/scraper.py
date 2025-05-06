from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from deep_translator import GoogleTranslator
import time
from typing import Dict


def get_page_data(url: str) -> Dict:
    """抓取單一網頁的資料"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 取得各項資料
        publish_time = soup.select_one(".o-noteContentHeader__date time").text.strip()
        title = soup.select_one(".o-noteContentHeader__title").text.strip()

        # 翻譯標題
        try:
            translator = GoogleTranslator(source="auto", target="zh-TW")
            title_translation = translator.translate(title)
        except Exception as e:
            print(f"翻譯失敗: {str(e)}")
            title_translation = ""

        author = soup.select_one(".o-noteContentHeader__name").text.strip()
        author_page = soup.select_one(".o-noteContentHeader__name a")["href"]

        a = urlparse(url)

        # 處理價格
        price_element = soup.select_one(".m-before-purchasing-button")
        if price_element:
            # 移除被刪除線標記的價格
            for strike_through in price_element.select(".line-through"):
                strike_through.decompose()
            price = price_element.text.strip()
        else:
            price = ""

        likes = soup.select_one('[class*="o-noteLikeV3__count"]')
        likes = likes.text.strip() if likes else "0"

        data = {
            "發表時間": publish_time,
            "標題": title,
            "標題翻譯": title_translation,
            "noteURL": url,
            "作者": author,
            "作者頁面": author_page,
            "價格": price,
            "likes": likes,
            "x帳號": "",
        }

        print(f"已抓取: {publish_time} - {title} - {author}")

        return data

    except Exception as e:
        print(f"抓取失敗 {url}: {str(e)}")
        return None


def main():
    # 讀取網址列表
    with open("urls.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_data = []

    # 抓取每個網址的資料
    for url in urls:
        data = get_page_data(url)
        if data:
            all_data.append(data)
        time.sleep(1)  # 避免請求過於頻繁

    # 將資料寫入 CSV
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("output.csv", index=False, encoding="utf-8-sig")
        print(f"\n成功將 {len(all_data)} 筆資料寫入 output.csv")


if __name__ == "__main__":
    main()
