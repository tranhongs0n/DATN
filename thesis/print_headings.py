from docx import Document
doc = Document(r'D:\DATN\thesis\DocOutput\DATN_Report_Final_Inserted.docx')
headings = []
for p in doc.paragraphs:
    if p.style.name.startswith('Heading'):
        headings.append(p.style.name + ': ' + p.text)
for h in headings:
    print(h)
