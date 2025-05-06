from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def scrape_youtube_releases(channel_url):
    # 設定 Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 無頭模式，不會開啟瀏覽器視窗
    driver = webdriver.Chrome(options=options)
    
    try:
        # 訪問頻道的發行內容頁面
        driver.get(channel_url)
        
        # 新增：自動捲動頁面直到底部，最多捲動 20 次
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        scroll_attempts = 0
        max_attempts = 20
        
        while scroll_attempts < max_attempts:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
                
            last_height = new_height
            scroll_attempts += 1
            print(f"正在載入更多內容... ({scroll_attempts}/{max_attempts})")

        # 獲取藝人訊息
        artist_name = driver.find_elements(By.TAG_NAME, 'h1')[1].text
        artist_handle = driver.find_elements(By.CLASS_NAME, 'yt-core-attributed-string--link-inherit-color')[1].text
        print(f"藝人：{artist_name}, 頻道：{artist_handle}")
        
        # 獲取所有專輯元素
        albums = driver.find_elements(By.TAG_NAME, 'ytd-rich-item-renderer')
        print(f"找到 {len(albums)} 個專輯")
        
        total_albums = 0
        total_songs = 0
        
        # 遍歷每個專輯
        for album in albums:
            try:
                # 獲取專輯標題
                # album_title = album.find_element(By.CSS_SELECTOR, 'h2.title').text
                album_title = album.find_element(By.TAG_NAME, 'h3').text
                
                # 獲取歌曲列表
                songs = album.find_elements(By.CSS_SELECTOR, 'ytd-thumbnail-overlay-bottom-panel-renderer')[1].text
                # songs_count = len(songs)
                songs_count = int(songs.split(' ')[0])
                
                print(f"專輯：{album_title}")
                print(f"歌曲數：{songs_count}")
                print("-" * 30)
                
                total_albums += 1
                total_songs += songs_count
                
            except Exception as e:
                print(f"發生錯誤：{str(e)}")
                continue
        
        print(f"\n總計：")
        print(f"藝人：{artist_name} ({artist_handle}), 專輯數：{total_albums}, 歌曲數：{total_songs}")
        
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
    
    finally:
        driver.quit()

# 使用範例
if __name__ == "__main__":
    # channel_releases_url = "https://www.youtube.com/@LoFi_TOKYOCITY/releases" # LoFi Tokyo
    # channel_releases_url = "https://www.youtube.com/@VibeMatchRadio/releases" # Vibe Match Radio
    # channel_releases_url = "https://www.youtube.com/@Lofi-hina/releases" # Lofi Hina Music
    channel_releases_url = "https://www.youtube.com/@Tokyo-Night-Lofi-Girl/releases" # T's item
    scrape_youtube_releases(channel_releases_url) 