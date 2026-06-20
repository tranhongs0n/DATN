import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Document_Planing" / "Content"
TEMPLATE_PATH = BASE_DIR / "DocTemplate" / "HuongDanTB_HPTN_(26-2-2020).docx"
OUTPUT_PATH = BASE_DIR / "DocOutput" / "DATN_Report_v3.docx"
IMAGES_DIR = BASE_DIR / "DocOutput" / "Images"

def process_mermaid(mermaid_code, counter):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_png = IMAGES_DIR / f"mermaid_{counter}.png"
    
    try:
        # Gọi API Kroki bằng Python (không cần Node.js)
        url = "https://kroki.io/mermaid/png"
        req = urllib.request.Request(url, data=mermaid_code.encode('utf-8'), method="POST")
        req.add_header("Content-Type", "text/plain")
        req.add_header("User-Agent", "Mozilla/5.0")
        
        with urllib.request.urlopen(req) as response:
            with open(out_png, "wb") as f:
                f.write(response.read())
                
        return str(out_png)
    except Exception as e:
        print(f"Lỗi khi tải ảnh sơ đồ {counter} từ API: {e}")
        return None

def main():
    print(f"Đang đọc template từ: {TEMPLATE_PATH}")
    if not TEMPLATE_PATH.exists():
        print("Không tìm thấy file template!")
        return

    # Khởi tạo Document từ file template có sẵn
    doc = Document(TEMPLATE_PATH)
    
    # Xóa nội dung có sẵn trong file template (chỉ giữ lại Style và định dạng trang)
    for p in doc.paragraphs:
        p_element = p._element
        p_element.getparent().remove(p_element)
    
    md_files = sorted(INPUT_DIR.glob("*.md"))
    mermaid_counter = 1
    
    for md_file in md_files:
        print(f"Đang xử lý file: {md_file.name}...")
        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        in_mermaid = False
        mermaid_code = ""
        
        for line in lines:
            stripped = line.strip()
            
            # --- XỬ LÝ SƠ ĐỒ MERMAID (Gọi Node.js) ---
            if stripped.startswith("```mermaid"):
                in_mermaid = True
                mermaid_code = ""
                continue
            elif in_mermaid and stripped.startswith("```"):
                in_mermaid = False
                print(f"  -> Đang dùng Python API kết xuất ảnh Mermaid số {mermaid_counter}...")
                img_path = process_mermaid(mermaid_code, mermaid_counter)
                
                if img_path and os.path.exists(img_path):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run()
                    # Giảm kích thước ảnh xuống 4.5 inch để không bị quá to
                    r.add_picture(img_path, width=Inches(4.5))
                mermaid_counter += 1
                continue
            elif in_mermaid:
                mermaid_code += line
                continue
                
            # --- XỬ LÝ VĂN BẢN VÀ HEADING ---
            if not stripped:
                doc.add_paragraph()
                continue
                
            is_heading = False
            level = 0
            text = stripped
            
            # Bổ sung xử lý Heading 4 (####)
            if stripped.startswith("#### "):
                is_heading = True
                level = 4
                text = stripped[5:]
            elif stripped.startswith("### "):
                is_heading = True
                level = 3
                text = stripped[4:]
            elif stripped.startswith("## "):
                is_heading = True
                level = 2
                text = stripped[3:]
            elif stripped.startswith("# "):
                is_heading = True
                level = 1
                text = stripped[2:]
                
            # Xóa các ký hiệu in đậm Markdown (**)
            text = text.replace("**", "")
            
            # Xóa tiền tố đánh số (CHƯƠNG X: hoặc 1.1., 2.4.1.1.) để tránh lặp với tự động đánh số của Word
            text = re.sub(r'^CHƯƠNG\s+\d+:\s*', '', text, flags=re.IGNORECASE)
            text = re.sub(r'^(\d+\.)+\s*', '', text)
            
            if is_heading:
                try:
                    # Gán style chuẩn từ Template
                    p = doc.add_paragraph(text, style=f'Heading {level}')
                except KeyError:
                    # Dự phòng nếu Template gốc không có sẵn style Heading 4
                    p = doc.add_paragraph(text)
                    p.style.font.bold = True
            else:
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
        # Thêm ngắt trang sau mỗi chương
        doc.add_page_break()
        
    doc.save(OUTPUT_PATH)
    print(f"\n✅ Hoàn tất! File Word đã được xuất ra tại: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
