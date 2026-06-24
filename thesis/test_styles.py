import sys
import docx
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def test_styles():
    doc = Document('Ref/HoangThaiDuy_DATN.docx')
    for style_name, size, bold, italic, align, space_before, space_after, line_spacing, all_caps in [
        ('Normal', 13, False, False, WD_ALIGN_PARAGRAPH.JUSTIFY, 10, 0, 1.5, False),
        ('Heading 1', 14, True, False, WD_ALIGN_PARAGRAPH.LEFT, 24, 24, 1.0, True),
        ('Heading 2', 13, True, False, WD_ALIGN_PARAGRAPH.LEFT, 6, 12, 1.0, False),
        ('Heading 3', 13, True, True, WD_ALIGN_PARAGRAPH.LEFT, 6, 12, 1.0, False),
        ('Heading 4', 13, False, True, WD_ALIGN_PARAGRAPH.LEFT, 6, 12, 1.0, False),
        ('Caption', 12, False, True, WD_ALIGN_PARAGRAPH.CENTER, 6, 6, 1.0, False),
        ('List Paragraph', 13, False, False, WD_ALIGN_PARAGRAPH.LEFT, 0, 0, 1.5, False)
    ]:
        if style_name in doc.styles:
            style = doc.styles[style_name]
            if hasattr(style, 'font'):
                style.font.name = 'Times New Roman'
                style.font.size = Pt(size)
                style.font.bold = bold
                style.font.italic = italic
                style.font.color.rgb = RGBColor(0, 0, 0)
                if all_caps:
                    style.font.all_caps = True
            if hasattr(style, 'paragraph_format'):
                style.paragraph_format.alignment = align
                style.paragraph_format.space_before = Pt(space_before)
                style.paragraph_format.space_after = Pt(space_after)
                style.paragraph_format.line_spacing = line_spacing
    doc.save('DocOutput/Test_Styles.docx')
    print("Saved to DocOutput/Test_Styles.docx")

test_styles()
