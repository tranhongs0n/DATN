import docx
from docx.shared import Inches

def inspect_doc(path, name):
    print(f"=== {name} ===")
    try:
        doc = docx.Document(path)
        print(f"Total Sections: {len(doc.sections)}")
        for i, sec in enumerate(doc.sections):
            w = sec.page_width.inches if sec.page_width else 0
            h = sec.page_height.inches if sec.page_height else 0
            tm = sec.top_margin.inches if sec.top_margin else 0
            bm = sec.bottom_margin.inches if sec.bottom_margin else 0
            lm = sec.left_margin.inches if sec.left_margin else 0
            rm = sec.right_margin.inches if sec.right_margin else 0
            print(f"  Section {i}:")
            print(f"    Page Size: {w:.3f} x {h:.3f} inches")
            print(f"    Margins (L/R/T/B): {lm:.3f} / {rm:.3f} / {tm:.3f} / {bm:.3f} inches")
    except Exception as e:
        print(f"Error loading {name}: {e}")
    print("\n")

inspect_doc("DocTemplate/HuongDanTB_HPTN_(26-2-2020).docx", "OFFICIAL TEMPLATE")
inspect_doc("DocOutput/DATN_Report_temp.docx", "GENERATED DOCX")
