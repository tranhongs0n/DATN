import docx
from pathlib import Path

DOC_PATH = Path(r"D:\DATN\thesis\DocOutput\DATN_Report_V2.docx")
doc = docx.Document(DOC_PATH)

print("Searching for images in paragraphs...")
for i, p in enumerate(doc.paragraphs):
    if 'w:drawing' in p._p.xml:
        text = p.text.strip()
        style_name = p.style.name
        print(f"Paragraph {i}: Style='{style_name}', TextLen={len(text)}, Text='{text[:30]}...'")
