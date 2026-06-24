import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

TEMPLATE = Path(__file__).resolve().parent / "Ref" / "HoangThaiDuy_DATN.docx"
doc = Document(TEMPLATE)
body = doc.element.body

with open("details_utf8.txt", "w", encoding="utf-8") as f:
    for idx, child in enumerate(body):
        tag = child.tag.split("}")[1]
        if tag == "p":
            from docx.text.paragraph import Paragraph
            p = Paragraph(child, doc)
            text = p.text.strip()
            if text:
                f.write(f"[{idx:4d}] P  style={p.style.name if p.style else 'None'} | {text[:100]}\n")
                # Check for fields
                instrTexts = child.findall(".//" + qn("w:instrText"))
                if instrTexts:
                    f.write(f"       -> Fields: {[t.text for t in instrTexts]}\n")
                # Check for numbering
                numPr = child.find(".//" + qn("w:numPr"))
                if numPr is not None:
                    numId = numPr.find(qn("w:numId"))
                    ilvl = numPr.find(qn("w:ilvl"))
                    f.write(f"       -> Numbering: numId={numId.get(qn('w:val')) if numId is not None else 'None'}, ilvl={ilvl.get(qn('w:val')) if ilvl is not None else 'None'}\n")
        elif tag == "tbl":
            f.write(f"[{idx:4d}] TBL\n")
