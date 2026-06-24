import docx

doc = docx.Document("DocOutput/DATN_Report.docx")
for i, p in enumerate(doc.paragraphs):
    if "Hình 2.1" in p.text or "Hình 2.2" in p.text:
        print(f"Para {i}: [{p.style.name}] {p.text}")
