from docx import Document
doc = Document(r'D:\DATN\thesis\DocOutput\DATN_Report_OnGoing.docx')
count = 0
for p in doc.paragraphs:
    if "CHƯƠNG 1:" in p.text.upper():
        print("Found:", p.text)
        count += 1
print("Total CHƯƠNG 1 found in OnGoing:", count)
