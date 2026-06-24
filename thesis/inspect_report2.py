import docx

doc = docx.Document("DocOutput/DATN_Report.docx")
for i in range(320, 330):
    p = doc.paragraphs[i]
    print(f"Para {i}: [{p.style.name}] {p.text}")
