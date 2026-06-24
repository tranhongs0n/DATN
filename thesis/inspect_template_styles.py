import sys
from docx import Document
from docx.oxml.ns import qn

def extract_style_info(doc_path):
    print(f"--- Styles in {doc_path} ---")
    doc = Document(doc_path)
    for s in doc.styles:
        if s.type == 1: # Paragraph style
            pPr = s.element.get_or_add_pPr()
            rPr = s.element.get_or_add_rPr()
            
            # Font Name
            fonts = rPr.find(qn('w:rFonts'))
            font_name = fonts.get(qn('w:ascii')) if fonts is not None else "Inherit"
            
            # Font Size
            sz = rPr.find(qn('w:sz'))
            sz_val = int(sz.get(qn('w:val')))/2 if sz is not None and sz.get(qn('w:val')) else "Inherit"
            
            # Bold/Italic
            bold = "Bold" if rPr.find(qn('w:b')) is not None else ""
            italic = "Italic" if rPr.find(qn('w:i')) is not None else ""
            
            # Spacing
            spacing = pPr.find(qn('w:spacing'))
            before = spacing.get(qn('w:before')) if spacing is not None else "Inherit"
            after = spacing.get(qn('w:after')) if spacing is not None else "Inherit"
            line = spacing.get(qn('w:line')) if spacing is not None else "Inherit"
            lineRule = spacing.get(qn('w:lineRule')) if spacing is not None else "Inherit"
            
            print(f"Style: {s.name}")
            print(f"  Font: {font_name}, Size: {sz_val}pt {bold} {italic}")
            print(f"  Spacing: Before={before}, After={after}, Line={line}, Rule={lineRule}")
            print("-" * 40)

extract_style_info("DocTemplate/HuongDanTB_HPTN_(26-2-2020).docx")
