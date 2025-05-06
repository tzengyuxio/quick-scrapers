# quick-scrapers
臨時爬蟲腳本的收納倉庫

🕷 收集一些臨時用的小型爬蟲腳本，主要用於一次性的資料擷取與測試。  
這些程式多半是快速寫成，結構不完整，僅供個人使用或參考。

## 📁 爬蟲列表

部分有其對應專案。沒有對應專案的則於此 repo 以資料夾歸類收納。

- `bandcamp` (2025): 收集並統計多產音樂人 R. STEVIE MOORE (*註) 總共發行過多少專輯與單曲
  - 註: [R. Stevie Moore - Wikipedia](https://en.wikipedia.org/wiki/R._Stevie_Moore) 上顯示發行過 400 張專輯以上
- `youtube-releases` (2025): 針對 YouTube 音樂頻道的專輯發行清單建立連結列表
    - 網頁有 lazy loader 所以使用 selenium
- `scrapbook` (2023) https://github.com/tzengyuxio/scrapbook
    - `ef`: 收集網站使用者資訊
    - `retro`: 下載 [レトロゲームの説明書保管庫](https://gamemanual.midnightmeattrain.com/) 的所有遊戲說明書與圖檔
- `baharank` (2020): 收集巴哈討論版人氣排行資料，於 crontab 中每日執行以追蹤變化
- `corpus`: https://github.com/tzengyuxio/corpus
  - 為研究漢字字頻建立語料庫的工具, 有以下爬蟲
    - 博客來 (books.py)
    - 蘋果日報 (appledaily.py)
    - 鉅亨網(雜誌) (magcnyes.py)
    - Yahoo 新聞 (newsyahoo.py)
    - 維基百科 (wikipedia.py)
- `python-five91`: https://github.com/tzengyuxio/python-five91/
  - 收集 591 資料。原本想整理成 python package, 但是 591 變動快，又防爬蟲，後作罷。

## 📌 Notes

- 本倉庫中的程式皆為臨時用途，不適合長期執行或大規模使用。
- 各腳本通常為單檔或簡易資料夾，視情況有註解或簡單說明。
- 有些可能需要額外套件或 API 金鑰，請依實際需求調整。

## 📄 License

MIT License
