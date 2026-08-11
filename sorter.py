import csv
import os
import shutil
from datetime import datetime

def parse_apple_date(date_str):
    date_str = date_str.strip()
    
    # 嘗試解析標準數字格式
    try:
        clean_date = date_str.replace("T", " ")[:19].replace("/", "-")
        return datetime.strptime(clean_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
        
    # 處理蘋果的全英文格式
    months = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }
    
    try:
        parts = date_str.split(" ", 1)
        if len(parts) > 1 and parts[0].endswith("day"):
            date_str = parts[1]
        
        for eng, num in months.items():
            if date_str.startswith(eng):
                date_str = date_str.replace(eng, num, 1)
                break
        
        return datetime.strptime(date_str, "%m %d,%Y %I:%M %p GMT")
    except Exception:
        raise ValueError(f"無法解析的時間格式: {date_str}")

def get_unique_path(dest_dir, filename):
    """如果遇到同名檔案，自動加上 _1, _2 避免覆蓋"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return os.path.join(dest_dir, new_filename)

def main():
    root_dir = os.getcwd()
    print("\n" + "="*50)
    print(f"🚀 開始全自動處理！目前外層資料夾：\n{root_dir}")
    print("="*50 + "\n")
    
    total_success = 0
    total_not_found = 0

    # os.walk 會自動鑽進所有的子資料夾
    for current_dir, dirs, files in os.walk(root_dir):
        if "Photo Details.csv" not in files:
            continue  # 如果這個資料夾沒有 CSV，就跳過繼續找下一個
            
        csv_path = os.path.join(current_dir, "Photo Details.csv")
        folder_name = os.path.basename(current_dir)
        print(f"📂 找到 CSV，正在處理子資料夾: {folder_name}")
        
        # 建立「實際檔案對照表」 (只看當前子資料夾)
        actual_files = {}
        for f in os.listdir(current_dir):
            if os.path.isfile(os.path.join(current_dir, f)) and f != "Photo Details.csv" and not f.endswith('.py'):
                basename = os.path.splitext(f)[0].lower()
                actual_files[basename] = f

        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            
            # 自動判斷蘋果的 CSV 欄位名稱版本
            if fields and 'imgName' in fields and 'originalCreationDate' in fields:
                name_column = 'imgName'
                date_column = 'originalCreationDate'
            elif fields and 'File Name' in fields and 'Creation Date' in fields:
                name_column = 'File Name'
                date_column = 'Creation Date'
            else:
                print(f"  ⚠️ 無法辨識此 CSV 的欄位，跳過此資料夾。")
                continue

            folder_success = 0
            
            for row in reader:
                csv_filename = row.get(name_column)
                date_str = row.get(date_column)
                
                if not csv_filename or not date_str:
                    continue
                
                csv_basename = os.path.splitext(csv_filename)[0].lower()
                
                # 模糊比對主檔名
                if csv_basename in actual_files:
                    real_filename = actual_files[csv_basename]
                    real_filepath = os.path.join(current_dir, real_filename)
                    
                    try:
                        dt = parse_apple_date(date_str)
                        # 將年份資料夾統一建立在「最外層 (root_dir)」
                        year_folder = os.path.join(root_dir, str(dt.year))
                        
                        if not os.path.exists(year_folder):
                            os.makedirs(year_folder)
                        
                        # 同步修正修改時間
                        timestamp = dt.timestamp()
                        os.utime(real_filepath, (timestamp, timestamp))
                        
                        # 取得不重複的新路徑並搬移
                        dest_path = get_unique_path(year_folder, real_filename)
                        shutil.move(real_filepath, dest_path)
                        
                        folder_success += 1
                        # 搬移後從清單中移除
                        del actual_files[csv_basename]
                        
                    except ValueError:
                        print(f"  ⚠️ 格式錯誤 ({csv_filename}): '{date_str}'")
                else:
                    total_not_found += 1
            
            total_success += folder_success
            print(f"  ✅ {folder_name} 完成！成功搬移 {folder_success} 張。\n")

    print("="*50)
    print(f"🎉 75 個資料夾全部掃描與搬移完畢！")
    print(f"總共成功分類: {total_success} 張 | 找不到檔案: {total_not_found} 張")
    print(f"所有照片已經統一集中到 {root_dir} 的各個年份資料夾了！")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
    
    input("👉 請按 Enter 鍵關閉此視窗...")
