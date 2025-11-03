import yaml
import sys
import os

# --- 檔案名稱設定 ---
INPUT_YAML_FILE = 'glossary.yaml'     # 讀取這個 YAML 檔案
OUTPUT_MD_FILE = 'glossary_export.md' # 產生這個 Markdown 檔案
# --------------------

def join_field(data_list):
    """輔助函式：將列表 (List) 用分號(;) 合併回一個字串"""
    if not data_list:
        return ""
    # 使用分號 + 空格，更易讀
    return "; ".join(data_list)

def export_yaml_to_markdown():
    
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

    # 關鍵：在寫入前，先依照筆劃 (strokes) 排序
    # 這能確保 .md 檔案的順序和您網站上的順序一致
    try:
        sorted_data = sorted(yaml_data, key=lambda term: term.get('strokes', 0))
    except Exception as e:
        print(f"資料排序時發生錯誤 (可能 'strokes' 欄位有問題): {e}")
        sorted_data = yaml_data

    print(f"正在將資料寫入 '{OUTPUT_MD_FILE}'...")
    
    try:
        with open(OUTPUT_MD_FILE, 'w', encoding='utf-8') as outfile:
            outfile.write("# 園藝科技術語詞典 (審閱用)\n\n")
            
            current_stroke_group = -1

            # 遍歷排序後的「術語」
            for term in sorted_data:
                strokes = term.get('strokes', 0)
                
                # 檢查是否需要寫入新的「筆劃標題」
                if strokes != current_stroke_group:
                    if strokes > 0:
                        outfile.write(f"\n## {strokes} 劃\n\n")
                    else:
                        outfile.write(f"\n## 其他 (0 劃)\n\n")
                    current_stroke_group = strokes

                # --- 寫入術語標題 ---
                term_name = term.get('term', 'N/A')
                original_name = term.get('original_name', '')
                if original_name:
                    outfile.write(f"### {term_name} ({original_name})\n\n")
                else:
                    outfile.write(f"### {term_name}\n\n")

                # --- 寫入中繼資料 ---
                outfile.write(f"**UID：** `{term.get('uid', '')}`\n\n") # 使用 `...` 讓 UID 更顯眼

                if term.get('aliases'):
                    outfile.write(f"**同義詞：** {join_field(term.get('aliases'))}\n\n")
                
                if term.get('category'):
                    outfile.write(f"**分類：** {join_field(term.get('category'))}\n\n")
                
                if term.get('related_terms'):
                    outfile.write(f"**廣義詞：** {join_field(term.get('related_terms'))}\n\n")
                
                # --- 寫入定義 ---
                definitions = term.get('definitions', [])
                if definitions:
                    outfile.write("#### 定義\n\n")
                    for i, definition in enumerate(definitions):
                        # 處理多行文字 (將 \n 轉換為 Markdown 的換行 <br>)
                        # 但 Markdown 會自動處理段落，所以我們直接寫入即可
                        text = definition.get('text', '').strip()
                        outfile.write(f"{text}\n\n")
                        
                        # 使用「區塊引言」來顯示來源和作者
                        outfile.write(f"> **來源：** {definition.get('source', 'N/A')}\n")
                        if definition.get('author'):
                            outfile.write(f"> **作者：** {definition.get('author')}\n")
                        
                        # 如果有多筆定義，在中間加個分隔線
                        if i < len(definitions) - 1:
                            outfile.write(f"\n---\n\n") # 分隔線
                
                outfile.write("\n---\n\n") # 每個術語之間用一個更粗的分隔線

        print("\n🎉 成功！")
        print(f"已成功將 '{INPUT_YAML_FILE}' 匯出為 '{OUTPUT_MD_FILE}' 檔案。")
        print("您現在可以將這個 .md 檔案傳送給專家進行審閱。")

    except Exception as e:
        print(f"寫入 Markdown 檔案時發生錯誤: {e}")

# --- 執行腳本 ---
if __name__ == "__main__":
    export_yaml_to_markdown()