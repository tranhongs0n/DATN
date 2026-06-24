import docx
from docx.shared import Inches

doc = docx.Document("DocOutput/DATN_Report_temp.docx")
print(f"Total sections: {len(doc.sections)}")
for i, section in enumerate(doc.sections):
    width = section.page_width.inches if section.page_width else None
    height = section.page_height.inches if section.page_height else None
    print(f"Section {i}: {width}x{height} inches, Orientation: {section.orientation}")
