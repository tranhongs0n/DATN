import sys
from pathlib import Path
from docx import Document

ONGOING_DOC = Path(r"D:\DATN\thesis\DocOutput\DATN_Report_OnGoing.docx")

def inspect_docx():
    doc = Document(ONGOING_DOC)
    
    with open("docx_headings.txt", "w", encoding="utf-8") as f:
        f.write("--- HEADINGS IN DOCX ---\n")
        for i, p in enumerate(doc.paragraphs):
            text = p.text.strip()
            if not text:
                continue
            
            if p.style.name.startswith("Heading") or "CHƯƠNG" in text.upper() or "KẾT LUẬN" in text.upper() or "PHỤ LỤC" in text.upper() or "TÀI LIỆU THAM KHẢO" in text.upper():
                f.write(f"[{i}] Style: {p.style.name} | Text: {text[:80]}\n")

if __name__ == "__main__":
    inspect_docx()
