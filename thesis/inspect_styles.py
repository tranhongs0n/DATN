"""Inspect heading style XML details in the template."""
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")

TEMPLATE = Path(__file__).resolve().parent / "Ref" / "HoangThaiDuy_DATN.docx"
doc = Document(TEMPLATE)

# Check heading styles
for style_name in ["Heading 1", "Heading 2", "Heading 3", "Heading 4"]:
    try:
        style = doc.styles[style_name]
        el = style.element
        print(f"\n{'='*60}")
        print(f"Style: {style_name}")
        print(etree.tostring(el, pretty_print=True).decode())
    except:
        print(f"Style {style_name} not found")

# Check Heading 1N if exists
try:
    style = doc.styles["Heading 1N"]
    print(f"\n{'='*60}")
    print(f"Style: Heading 1N")
    print(etree.tostring(style.element, pretty_print=True).decode())
except:
    print("No Heading 1N style")

# Check Content style
try:
    style = doc.styles["Content"]
    print(f"\n{'='*60}")
    print(f"Style: Content")
    print(etree.tostring(style.element, pretty_print=True).decode())
except:
    print("No Content style")

# Also check if there's any theme color causing blue
print("\n\n=== Checking first heading in body for run properties ===")
body = doc.element.body
for idx, child in enumerate(body):
    tag = child.tag.split("}")[1]
    if tag == "p":
        from docx.text.paragraph import Paragraph
        p = Paragraph(child, doc)
        if p.style and p.style.name and "Heading" in p.style.name:
            print(f"\n[{idx}] {p.style.name}: '{p.text[:60]}'")
            print(etree.tostring(child, pretty_print=True).decode()[:2000])
            break
