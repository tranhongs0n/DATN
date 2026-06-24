import docx
from docx.shared import Inches

doc = docx.Document("DocOutput/DATN_Report_temp.docx")
for i, section in enumerate(doc.sections):
    print(f"Section {i} Margins:")
    print(f"  Top: {section.top_margin.inches if section.top_margin else None}")
    print(f"  Bottom: {section.bottom_margin.inches if section.bottom_margin else None}")
    print(f"  Left: {section.left_margin.inches if section.left_margin else None}")
    print(f"  Right: {section.right_margin.inches if section.right_margin else None}")
