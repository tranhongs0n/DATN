from docx import Document
doc = Document(r'D:\DATN\thesis\DocOutput\DATN_Report_OnGoing.docx')
doc.add_paragraph('Test bullet', style='Bullet')
doc.save(r'D:\DATN\thesis\DocOutput\test_bullet.docx')
