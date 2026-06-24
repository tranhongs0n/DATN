import docx

doc = docx.Document("DocOutput/DATN_Report.docx")
print("=== SEARCH FOR CAPTION KEYWORDS ===")
keywords = ["Benchmark", "Thống kê nguồn", "1.2", "2.1", "4.1", "5.1"]
for i, p in enumerate(doc.paragraphs):
    for kw in keywords:
        if kw in p.text:
            print(f"[{i}] Style: {p.style.name} | Text: {p.text}")
            break
