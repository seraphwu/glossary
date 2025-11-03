import yaml
import csv
import sys
import os

# --- 檔案名稱設定 ---
INPUT_YAML_FILE = 'glossary.yaml'     # 讀取這個 YAML 檔案
OUTPUT_CSV_FILE = 'glossary_export.csv' # 產生這個 CSV 檔案
# --------------------

def join_field(data_list):
    """輔助函式：將列表 (List) 用分號(;) 合併回一個字串"""
    if not data_list:
        return ""
    return ";".join(data_list)

def export_yaml_to_csv():
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(INPUT_YAML_FILE):
        print(f"錯誤：找不到輸入檔案 '{INPUT_YAML_FILE}'")
        return

    print(f"正在讀取 '{INPUT_YAML_FILE}'...")
    
    try:
        with open(INPUT_YAML_FILE, 'r', encoding='utf-8') as infile:
            yaml_data = yaml.safe_load(infile)
    except Exception as e:
        print(f"讀取 YAML 檔案時發生錯誤: {e}")
        return
    
    if not yaml_data:
        print("錯誤：YAML 檔案是空的。")
        return

    # 這是 CSV 的標題列，必須和 convert.py 能讀取的一致
    # (我們不匯出 '筆劃' 欄位，因為那是自動計算的)
    # (我們將所有 'aliases' 都先匯出到 '中名同義詞' 欄位，這最簡單)
    headers = [
        'uid', '術語', '術語原文', 
        '中名同義詞', '英名同義詞', '廣義詞', '分類', 
        '定義', '作者', '出處'
    ]

    print(f"正在將資料寫入 '{OUTPUT_CSV_FILE}'...")
    
    try:
        with open(OUTPUT_CSV_FILE, 'w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            
            # 寫入標題列
            writer.writeheader()
            
            # 遍歷 YAML 中的每一個「術語」
            for term in yaml_data:
                # 1. 準備「共享」的資料
                shared_row_data = {
                    'uid': term.get('uid'),
                    '術語': term.get('term'),
                    '術語原文': term.get('original_name'),
                    # 將 'aliases' 列表合併回字串，並放入 '中名同義詞'
                    # (convert.py 會再把它們讀取回來)
                    '中名同義詞': join_field(term.get('aliases', [])), 
                    '英名同義詞': '', # 匯出時先留空
                    '廣義詞': join_field(term.get('related_terms', [])),
                    '分類': join_field(term.get('category', [])),
                }

                # 2. 遍歷該術語的「每一個定義」
                definitions = term.get('definitions', [])
                
                if definitions:
                    for definition in definitions:
                        # 建立一個新資料列
                        row_to_write = shared_row_data.copy()
                        
                        # 填入「獨有」的定義資料
                        row_to_write['定義'] = definition.get('text')
                        row_to_write['作者'] = definition.get('author')
                        row_to_write['出處'] = definition.get('source')
                        
                        # 寫入這「一筆定義」的資料列
                        writer.writerow(row_to_write)
                else:
                    # 如果這個術語沒有任何定義，我們還是要寫入一列
                    # 這樣才不會遺失這個術語
                    writer.writerow(shared_row_data)

        print("\n🎉 成功！")
        print(f"已成功將 '{INPUT_YAML_FILE}' 匯出為 '{OUTPUT_CSV_FILE}' 檔案。")
        print("您現在可以用 Excel 開啟這個 CSV 檔案來進行修改。")

    except Exception as e:
        print(f"寫入 CSV 檔案時發生錯誤: {e}")

# --- 執行腳本 ---
if __name__ == "__main__":
    export_yaml_to_csv()