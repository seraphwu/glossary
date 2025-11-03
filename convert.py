import csv
import yaml
import sys
import os
try:
    # ###########################################################
    #
    #  **** 感謝您！我們現在改用 'strokes' ****
    #
    # ###########################################################
    from strokes import strokes
except ImportError:
    print("錯誤：找不到 'strokes' 套件。")
    print("請在您的終端機執行： pip install strokes")
    sys.exit(1)


# --- 檔案名稱設定 ---
INPUT_CSV_FILE = 'input.csv'    
OUTPUT_YAML_FILE = 'glossary.yaml' 
# --------------------

def clean_value(value):
    """
    輔助函式：強力清理字串，移除各種空格。
    """
    if not value:
        return ""
    # \xa0 是您 CSV 中的那種「假空格」
    return value.replace('\xa0', ' ').replace('\u3000', ' ').strip()

def split_field(value):
    """輔助函式：將用分號(;)分隔的欄位拆分為列表"""
    value_cleaned = clean_value(value)
    if not value_cleaned:
        return []
    return [item.strip() for item in value_cleaned.split(';') if item.strip()]

# ###########################################################
#
#  **** 這是使用 'strokes' 的「最終正確」筆劃計算函式 ****
#
# ###########################################################
def get_stroke_count(term_string):
    """
    自動計算術語第一個字的筆劃數 (strokes 版)。
    """
    term_string_cleaned = clean_value(term_string)
    
    if not term_string_cleaned:
        return 0 # 如果清理後是空的，返回 0
        
    try:
        # 取得第一個「真正」的字元
        first_char = term_string_cleaned[0]
        
        # **** 這是您提供的、正確的指令 ****
        # 它會自動處理非中文字元 (回傳 0)
        stroke_val = strokes(first_char)
        
        # 確保回傳的是數字
        if isinstance(stroke_val, int):
            return stroke_val
        else:
            return 0
            
    except Exception as e:
        # 處理任何突發錯誤
        # print(f"警告：在計算 '{term_string}' 的筆劃時發生錯誤: {e}")
        return 0

def convert_csv_to_yaml():
    
    if not os.path.exists(INPUT_CSV_FILE):
        print(f"錯誤：找不到輸入檔案 '{INPUT_CSV_FILE}'")
        return

    terms_data = {}
    print(f"正在讀取 '{INPUT_CSV_FILE}'...")

    try:
        with open(INPUT_CSV_FILE, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            
            if not reader.fieldnames:
                 print("錯誤：CSV 檔案是空的。")
                 return

            for row in reader:
                uid = clean_value(row.get('uid'))
                if not uid:
                    continue 

                term_value = clean_value(row.get('術語'))

                if uid not in terms_data:
                    terms_data[uid] = {
                        'uid': uid,
                        'term': term_value,
                        'original_name': clean_value(row.get('術語原文')),
                        
                        # 自動計算筆劃 (現在會呼叫正確的函式)
                        'strokes': get_stroke_count(term_value), 
                        
                        'aliases': split_field(row.get('中名同義詞')) + split_field(row.get('英名同義詞')),
                        'related_terms': split_field(row.get('廣義詞')),
                        'category': split_field(row.get('分類')),
                        
                        'definitions': []
                    }

                # 處理定義 (不清理由換行符號，只清理特殊空格)
                definition_text = row.get('定義', '')
                if definition_text:
                    definition_text = definition_text.replace('\xa0', ' ').replace('\u3000', ' ')
                
                definition_entry = {
                    'text': definition_text,
                    'author': clean_value(row.get('作者')),
                    'source': clean_value(row.get('出處'))
                }
                
                # 只有在任一欄位有內容時才加入
                if definition_entry['text'] or definition_entry['author'] or definition_entry['source']:
                    terms_data[uid]['definitions'].append(definition_entry)

    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return

    # --- 轉換與寫入 ---
    final_yaml_data = list(terms_data.values())

    if len(final_yaml_data) == 0:
        print("\n!! 轉換了 0 筆資料 !!")
    else:
        print(f"轉換完成。正在寫入 {len(final_yaml_data)} 筆術語資料到 '{OUTPUT_YAML_FILE}'...")
        try:
            with open(OUTPUT_YAML_FILE, mode='w', encoding='utf-8') as outfile:
                yaml.dump(final_yaml_data, outfile, allow_unicode=True, sort_keys=False, width=80)
            
            print("\n🎉 成功！")
            print(f"已成功生成 '{OUTPUT_YAML_FILE}' 檔案。")

        except Exception as e:
            print(f"寫入 YAML 檔案時發生錯誤: {e}")

# --- 執行腳本 ---
if __name__ == "__main__":
    convert_csv_to_yaml()