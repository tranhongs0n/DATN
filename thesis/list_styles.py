from docx import Document
doc = Document(r'D:\DATN\thesis\DocOutput\DATN_Report_OnGoing.docx')
for s in doc.styles:
    if 'list' in s.name.lower() or 'bullet' in s.name.lower():
        print(s.name)
