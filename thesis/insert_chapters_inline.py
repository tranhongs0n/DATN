import sys
from pathlib import Path
import docx
from docx import Document
from build_doc import process_content_file, CHAPTER_FILES

BASE_DIR = Path(r"D:\DATN\thesis")
INPUT_DIR = BASE_DIR / "Document_Planing" / "Content"
ONGOING_DOC = BASE_DIR / "DocOutput" / "DATN_Report_OnGoing.docx"
OUTPUT_DOC = BASE_DIR / "DocOutput" / "DATN_Report_Final_Inserted.docx"

def insert_inline():
    print(f"Loading {ONGOING_DOC.name}...")
    doc = Document(ONGOING_DOC)
    body = doc._body._body
    
    # Find insertion points
    start_elem = None
    end_elem = None
    
    for p in doc.paragraphs:
        text = p.text.upper()
        if "CHƯƠNG 1:" in text and start_elem is None:
            start_elem = p._element
        if "TÀI LIỆU THAM KHẢO" in text and end_elem is None:
            end_elem = p._element

    if start_elem is None or end_elem is None:
        print("Lỗi: Không tìm thấy CHƯƠNG 1 hoặc TÀI LIỆU THAM KHẢO để thay thế!")
        return

    print("Found insertion bounds. Deleting old chapters...")
    # Delete everything from start_elem to just before end_elem
    elements_to_delete = []
    started = False
    for child in body:
        if child == start_elem:
            started = True
        if child == end_elem:
            started = False
            break
        if started:
            elements_to_delete.append(child)

    for child in elements_to_delete:
        body.remove(child)

    print("Old chapters deleted.")

    # Record how many children exist before we append the new chapters
    num_children_before = len(body)
    
    md_files = sorted(INPUT_DIR.glob("*.md"))
    mermaid_counter = [1]
    chapters_to_append = ["1_Chuong1.md", "2_Chuong2.md", "3_Chuong3.md", "4_Chuong4.md", "5_PhanCuoi.md"]
    
    print("Building new chapters and appending to end...")
    for md_file in md_files:
        if md_file.name not in chapters_to_append:
            continue
            
        is_numbered = md_file.name in CHAPTER_FILES
        print(f"  -> {md_file.name}")
        process_content_file(doc, md_file, is_numbered, mermaid_counter)
        if md_file.name != "5_PhanCuoi.md":
            doc.add_page_break()

    # Now we have all the new chapter elements at the end of the body.
    # We must move them to exactly before end_elem!
    print("Moving newly built elements to the correct insertion point...")
    
    # We collect them first
    new_elements = []
    children = list(body)
    for child in children[num_children_before:]:
        new_elements.append(child)

    for child in new_elements:
        body.remove(child)
        end_elem.addprevious(child)

    # Save
    OUTPUT_DOC.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_DOC)
    print(f"\nSUCCESS! File mới được lưu tại: {OUTPUT_DOC}")

if __name__ == "__main__":
    insert_inline()
