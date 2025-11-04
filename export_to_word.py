import pypandoc
import sys
import os

# --- 檔案名稱設定 ---
INPUT_MD_FILE = 'glossary_export.md'
OUTPUT_DOCX_FILE = 'glossary_for_review.docx'
# --------------------

def convert_md_to_word():
    
    # 檢查 Markdown 檔案是否存在
    if not os.path.exists(INPUT_MD_FILE):
        print(f"錯誤：找不到輸入檔案 '{INPUT_MD_FILE}'")
        print("請先執行 'export_to_md.py' 來產生 Markdown 檔案。")
        sys.exit(1)

    print(f"正在讀取 '{INPUT_MD_FILE}' 並轉換為 Word (.docx)...")

    try:
        # 核心轉換指令
        pypandoc.convert_file(
            INPUT_MD_FILE, 
            'docx',  # 轉換的目標格式
            outputfile=OUTPUT_DOCX_FILE
        )
        
        print(f"\n🎉 成功！")
        print(f"已成功將 '{INPUT_MD_FILE}' 轉換為 '{OUTPUT_DOCX_FILE}'。")
        print("您現在可以將這個 .docx 檔案傳送給專家進行審閱。")

    except FileNotFoundError as e:
        # 這是最常見的錯誤：使用者尚未安裝 Pandoc 主程式
        print("\n--- 錯誤 (FileNotFoundError) ---", file=sys.stderr)
        print("錯誤：找不到 'pandoc' 執行檔。", file=sys.stderr)
        print("您似乎已經安裝了 'pypandoc' (Python 套件)，但您尚未安裝 'Pandoc' (主程式)。", file=sys.stderr)
        print("\n請前往 Pandoc 官方網站下載並安裝：", file=sys.stderr)
        print("https://pandoc.org/installing.html", file=sys.stderr)
        
    except Exception as e:
        print(f"\n轉換時發生未預期的錯誤: {e}", file=sys.stderr)

# --- 執行腳本 ---
if __name__ == "__main__":
    convert_md_to_word()