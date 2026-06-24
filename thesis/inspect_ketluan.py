import docx

doc = docx.Document("DocOutput/DATN_Report_PhuLuc.docx")
for i, p in enumerate(doc.paragraphs):
    if "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN" in p.text.upper() or "LỜI CẢM ƠN" in p.text.upper() or "CHÂN THÀNH CẢM ƠN" in p.text.upper():
        print(f"Para {i}: [{p.style.name}] {p.text}")
