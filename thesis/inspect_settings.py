import docx
doc = docx.Document("DocOutput/DATN_Report_temp.docx")
print("Settings:")
try:
    print(doc.settings.element.xml)
except Exception as e:
    print(e)
