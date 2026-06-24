"""Inspect template structure around key sections."""
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")

TEMPLATE = Path(__file__).resolve().parent / "Ref" / "HoangThaiDuy_DATN.docx"
doc = Document(TEMPLATE)
body = doc.element.body

print("=" * 80)
print("FULL BODY ELEMENT DUMP (paragraphs and tables)")
print("=" * 80)

for idx, child in enumerate(body):
    tag = child.tag.split("}")[1]
    if tag == "p":
        from docx.text.paragraph import Paragraph
        p = Paragraph(child, doc)
        style_name = p.style.name if p.style else "None"
        text_preview = p.text[:120].replace('\n', '\\n') if p.text else ""
        if text_preview.strip():
            print(f"[{idx:4d}] P  style={style_name:30s} | {text_preview}")
    elif tag == "tbl":
        # Count rows
        rows = child.findall(qn("w:tr"))
        first_row_text = ""
        if rows:
            cells = rows[0].findall(qn("w:tc"))
            cell_texts = []
            for c in cells[:3]:
                paras = c.findall(qn("w:p"))
                ct = " ".join(p_el.text or "" for p_el in paras if hasattr(p_el, "text"))
                # Get actual text from runs
                runs_text = []
                for p_el in paras:
                    for r in p_el.findall(qn("w:r")):
                        t = r.find(qn("w:t"))
                        if t is not None and t.text:
                            runs_text.append(t.text)
                cell_texts.append("".join(runs_text))
            first_row_text = " | ".join(cell_texts)
        print(f"[{idx:4d}] TBL rows={len(rows):3d}  first_row: {first_row_text[:100]}")
    elif tag == "sdt":
        # Structured document tag (TOC)
        alias_el = child.find(".//" + qn("w:alias"))
        alias_val = alias_el.get(qn("w:val")) if alias_el is not None else "?"
        print(f"[{idx:4d}] SDT alias={alias_val}")
    elif tag == "sectPr":
        print(f"[{idx:4d}] SECTPR")
    else:
        print(f"[{idx:4d}] {tag}")

print("\n\n")
print("=" * 80)
print("ALL STYLES IN DOCUMENT")
print("=" * 80)
for s in doc.styles:
    if s.type is not None:
        print(f"  {s.style_id:30s}  type={s.type}  name={s.name}")
