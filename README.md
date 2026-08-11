# 📸 AutoYearSorter

解決從 iCloud 批次匯出照片時，系統「建立時間」遺失與排序大亂的終極救星。

從 iCloud 匯出照片時，系統常會把「修改時間」變成「下載當下」，導致照片無法按年份排序。此外，蘋果會將真實拍攝時間記錄在獨立的 `Photo Details.csv` 中。

本專案提供全自動 Python 腳本，能讀取 CSV、精準還原拍攝時間，並將照片自動歸檔到對應的「年份資料夾」。

## ✨ 核心功能 (Features)

- 🤖 **全自動資料夾巡邏 (Auto-Patrol)**
  只需在最外層目錄執行，程式會自動掃描所有子資料夾並處理照片，免去手動逐一操作的麻煩。
- 🔍 **無敵模糊比對 (Fuzzy Extension Matching)**
  無視蘋果匯出時的副檔名變更（如 `.HEIC` 變 `.jpg`），只要主檔名一致就能自動抓取比對。
- 🕒 **特規時間解析 (Apple Date Parsing)**
  內建轉換機制，自動解析蘋果特規的純英文時間格式（如 `Thursday February 13,2025`），避免中文語系系統報錯。
- 🛡️ **自動防撞名機制 (Smart Deduplication)**
  當不同資料夾的同名照片集中到同個年份資料夾時，程式會自動加上編號（如 `_1`, `_2`），保護照片不被覆蓋。
- 📂 **雙模式支援 (Dual Mode)**
  除 iCloud 專用腳本外，另附 `sort_normal_photos.py`，支援直接讀取檔案系統時間，用來整理一般日常照片。

---

## 🚀 使用說明 (Usage)

### 模式一：處理 iCloud 照片 (`sort_photos.py`)

1. 將 `sort_photos.py` 放置於**最外層資料夾**（即包含所有照片子資料夾的目錄）。
2. 確保子資料夾內包含照片與對應的 `Photo Details.csv`。
3. 雙擊執行 .py，或於終端機執行
4. 程式會自動讀取 CSV、校正時間，並將照片集中建立至外層的「年份資料夾」。

模式二：處理一般照片 (sort_normal_photos.py)
適用於非 iCloud 下載、本身已具備正確「系統修改時間」的照片。
將 sort_normal_photos.py 放在欲整理的照片目錄外層。
執行腳本，程式將不依賴 CSV，直接讀取檔案時間並依年份歸檔。

🛠️ 技術細節 (Technical Details)
語言: Python 3.x
內建模組: os, shutil, csv, datetime (免安裝第三方套件)
環境: 支援 Windows / macOS

⚠️ 注意事項
本腳本會直接修改檔案的系統時間（os.utime）並搬移實體檔案，執行前建議先備份重要照片。
若照片來自 LINE 或 Facebook 等社群平台（原始時間通常已被平台抹除），執行「模式二」時會統一歸類至下載當年的資料夾。
