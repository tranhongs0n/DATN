import docx

doc = docx.Document("Ref/HoangThaiDuy_DATN.docx")
print("--- TOC for HoangThaiDuy_DATN.docx ---")
for p in doc.paragraphs[:200]:
    if "CHƯƠNG" in p.text.upper() or p.style.name.startswith("Heading"):
        print(p.text)
