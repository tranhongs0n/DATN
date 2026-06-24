from docx import Document
doc = Document(r'D:\DATN\thesis\DocOutput\DATN_Report_Final_Inserted.docx')
paras = [p.text for p in doc.paragraphs if p.text.strip()]
for i, text in enumerate(paras):
    if "CHƯƠNG 1:" in text.upper():
        print(f'--- Match {i} ---')
        print("Before:", paras[i-2] if i>=2 else "")
        print("Before:", paras[i-1] if i>=1 else "")
        print("HIT:", text)
        print("After:", paras[i+1] if i+1<len(paras) else "")
        print("After:", paras[i+2] if i+2<len(paras) else "")
