import os
import re
import sys
import urllib.request
from pathlib import Path

import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Document_Planing" / "Content"
TEMPLATE_PATH = BASE_DIR / "DocTemplate" / "HuongDanTB_HPTN_(26-2-2020).docx"
OUTPUT_PATH = BASE_DIR / "DocOutput" / "DATN_Report.docx"
IMAGES_DIR = BASE_DIR / "DocOutput" / "Images"

PROJECT_INFO = {
    "ho_va_ten":   "TRẦN HỒNG SƠN",
    "ten_de_tai":  "NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO HỖ TRỢ TUYỂN SINH CHO TRƯỜNG ĐẠI HỌC THỦY LỢI DỰA TRÊN KỸ THUẬT RAG",
    "nganh":       "Công nghệ thông tin",
    "ma_so":       "7480201",
    "nguoi_hd_1":  "TS. Lý Anh Tuấn",
    "nam":         "2026",
    "ten_chinh":   "Trần Hồng Sơn",
}

CHAPTER_FILES = {
    "1_Chuong1.md",
    "2_Chuong2.md",
    "3_Chuong3.md",
    "4_Chuong4.md",
}

sys.stdout.reconfigure(encoding="utf-8")


def fetch_mermaid_png(mermaid_code: str, counter: int) -> str | None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = IMAGES_DIR / f"mermaid_{counter}.png"
    try:
        url = "https://kroki.io/mermaid/png"
        req = urllib.request.Request(
            url, data=mermaid_code.encode("utf-8"), method="POST"
        )
        req.add_header("Content-Type", "text/plain")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            out_path.write_bytes(resp.read())
        print(f"  -> Mermaid {counter}: OK ({out_path.name})")
        return str(out_path)
    except Exception as e:
        print(f"  -> Mermaid {counter}: FAILED ({e})")
        return None


def patch_numbering_trailing_dots(doc: Document) -> None:
    """Sua lvlText cua abstractNumId=20 de them dau cham cuoi cho H2/H3/H4."""
    try:
        numbering = doc.part.numbering_part.numbering_definitions._numbering
    except Exception:
        return

    num_to_abstract: dict[str, str] = {}
    for child in numbering:
        tag = child.tag.split("}")[1]
        if tag == "num":
            nid = child.get(qn("w:numId"))
            abs_el = child.find(qn("w:abstractNumId"))
            if abs_el is not None:
                num_to_abstract[nid] = abs_el.get(qn("w:val"))

    target_abs = num_to_abstract.get("28")
    if not target_abs:
        return

    for child in numbering:
        tag = child.tag.split("}")[1]
        if tag == "abstractNum" and child.get(qn("w:abstractNumId")) == target_abs:
            for lvl in child.findall(qn("w:lvl")):
                ilvl = lvl.get(qn("w:ilvl"))
                if ilvl == "0":
                    continue
                lvlText_el = lvl.find(qn("w:lvlText"))
                if lvlText_el is not None:
                    val = lvlText_el.get(qn("w:val"), "")
                    if val and not val.endswith("."):
                        lvlText_el.set(qn("w:val"), val + ".")
            print("  -> Patch numbering: OK (trailing dots added)")
            break


def replace_paragraph_text(para, old: str, new: str) -> None:
    full = para.text
    if old not in full:
        return
    new_full = full.replace(old, new)
    for run in para.runs:
        run.text = ""
    if para.runs:
        para.runs[0].text = new_full
    else:
        para.add_run(new_full)


def fill_table_cell(cell, text: str) -> None:
    for para in cell.paragraphs:
        for run in para.runs:
            run.text = ""
    p = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
    if p.runs:
        p.runs[0].text = text
    else:
        p.add_run(text)


def patch_front_matter(doc: Document) -> None:
    placeholders = [
        ("họ và tên",              PROJECT_INFO["ho_va_ten"]),
        ("HỌ VÀ TÊN",             PROJECT_INFO["ho_va_ten"].upper()),
        ("TÊN ĐỀ TÀI đatn, kltn", PROJECT_INFO["ten_de_tai"]),
        ("202…",                   PROJECT_INFO["nam"]),
        ("202\u2026",              PROJECT_INFO["nam"]),
        ("Nguyễn Văn T",           PROJECT_INFO["ten_chinh"]),
    ]
    for para in doc.paragraphs:
        for old, new in placeholders:
            if old in para.text:
                replace_paragraph_text(para, old, new)

    tables = doc.tables
    if len(tables) > 2:
        tbl2 = tables[2]
        fill_table_cell(tbl2.rows[0].cells[1], PROJECT_INFO["nganh"])
        fill_table_cell(tbl2.rows[1].cells[1], PROJECT_INFO["ma_so"])
    if len(tables) > 3:
        tbl3 = tables[3]
        fill_table_cell(tbl3.rows[0].cells[1], "1. " + PROJECT_INFO["nguoi_hd_1"])
        fill_table_cell(tbl3.rows[1].cells[1], "")
    if len(tables) > 4:
        tbl4 = tables[4]
        fill_table_cell(tbl4.rows[0].cells[1], PROJECT_INFO["ten_chinh"])
    print("  -> Patch front matter: OK")


def remove_guide_content(doc: Document) -> None:
    """Xoa toan bo noi dung huong dan tu body element index 104 tro di."""
    body = doc.element.body
    to_delete = []
    for idx, child in enumerate(body):
        tag = child.tag.split("}")[1]
        if idx >= 104 and tag in ("p", "tbl"):
            to_delete.append(child)
    for el in to_delete:
        body.remove(el)
    print(f"  -> Removed {len(to_delete)} guide elements")


def replace_loi_cam_on(doc: Document, md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    cam_on_match = re.search(
        r"## Lời cảm ơn\s*\n(.*?)(?=\n---|\n#|\Z)", text, re.DOTALL
    )
    if not cam_on_match:
        return

    cam_on_text = cam_on_match.group(1).strip()
    body = doc.element.body

    loi_cam_on_idx = None
    for idx, child in enumerate(body):
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = docx.text.paragraph.Paragraph(child, doc)
            if "LỜI CÁM ƠN" in p.text or "LỜI CẢM ƠN" in p.text:
                loi_cam_on_idx = idx
                break

    if loi_cam_on_idx is None:
        return

    children_list = list(body)
    placeholder_els = []
    for i in range(loi_cam_on_idx + 1, min(loi_cam_on_idx + 10, len(children_list))):
        child = children_list[i]
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = docx.text.paragraph.Paragraph(child, doc)
            if p.style.name in ("Content", "Normal") and p.text.strip():
                placeholder_els.append(child)
        else:
            break

    for el in placeholder_els:
        body.remove(el)

    anchor = list(body)[loi_cam_on_idx]
    for line in cam_on_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        new_p = OxmlElement("w:p")
        pPr = OxmlElement("w:pPr")
        pStyle = OxmlElement("w:pStyle")
        pStyle.set(qn("w:val"), "Content")
        pPr.append(pStyle)
        new_p.append(pPr)
        r = OxmlElement("w:r")
        t = OxmlElement("w:t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = stripped
        r.append(t)
        new_p.append(r)
        anchor.addnext(new_p)
        anchor = new_p

    print("  -> Loi cam on: OK")


def replace_danh_muc_viet_tat(doc: Document, md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    tables_md = re.findall(r"((?:\|.+\|[ \t]*\n)+)", text)
    if not tables_md:
        return

    body = doc.element.body
    dmvt_idx = None
    for idx, child in enumerate(body):
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = docx.text.paragraph.Paragraph(child, doc)
            if "DANH MỤC CÁC TỪ VIẾT TẮT" in p.text:
                dmvt_idx = idx
                break

    if dmvt_idx is None:
        return

    children_list = list(body)
    placeholder_els = []
    for i in range(dmvt_idx + 1, min(dmvt_idx + 20, len(children_list))):
        child = children_list[i]
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = docx.text.paragraph.Paragraph(child, doc)
            if p.style.name in ("Content", "Normal") and p.text.strip():
                placeholder_els.append(child)
        else:
            break

    for el in placeholder_els:
        body.remove(el)

    anchor = list(body)[dmvt_idx]

    for table_md_str in tables_md:
        rows_raw = [r.strip() for r in table_md_str.strip().splitlines()]
        rows_data = []
        for r in rows_raw:
            if re.match(r"^\|[-:\s|]+\|$", r):
                continue
            cells = [re.sub(r"\*\*(.+?)\*\*", r"\1", c.strip())
                     for c in r.strip("|").split("|")]
            rows_data.append(cells)
        if not rows_data:
            continue
        ncols = max(len(r) for r in rows_data)

        tbl = OxmlElement("w:tbl")
        tblPr = OxmlElement("w:tblPr")
        tblStyle = OxmlElement("w:tblStyle")
        tblStyle.set(qn("w:val"), "BK_Table")
        tblW = OxmlElement("w:tblW")
        tblW.set(qn("w:w"), "0")
        tblW.set(qn("w:type"), "auto")
        tblPr.append(tblStyle)
        tblPr.append(tblW)
        tbl.append(tblPr)

        for r_idx, row_cells in enumerate(rows_data):
            tr = OxmlElement("w:tr")
            for c_idx in range(ncols):
                cell_text = row_cells[c_idx] if c_idx < len(row_cells) else ""
                tc = OxmlElement("w:tc")
                p_el = OxmlElement("w:p")
                pPr_el = OxmlElement("w:pPr")
                pStyle_el = OxmlElement("w:pStyle")
                pStyle_el.set(qn("w:val"), "BK_Table")
                pPr_el.append(pStyle_el)
                p_el.append(pPr_el)
                r_el = OxmlElement("w:r")
                if r_idx == 0:
                    rPr_el = OxmlElement("w:rPr")
                    b_el = OxmlElement("w:b")
                    rPr_el.append(b_el)
                    r_el.append(rPr_el)
                t_el = OxmlElement("w:t")
                t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                t_el.text = cell_text
                r_el.append(t_el)
                p_el.append(r_el)
                tc.append(p_el)
                tr.append(tc)
            tbl.append(tr)

        sep_p = OxmlElement("w:p")
        anchor.addnext(tbl)
        tbl.addnext(sep_p)
        anchor = sep_p

    print("  -> Danh muc viet tat: OK")


def parse_inline(text: str) -> list[tuple[str, bool, bool, bool]]:
    """Phan tich inline formatting. Tra ve list (text, bold, italic, code)."""
    result = []
    pattern = re.compile(
        r"(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)|`([^`]+)`)"
    )
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            result.append((text[last:m.start()], False, False, False))
        raw = m.group(1)
        if raw.startswith("***"):
            result.append((m.group(2), True, True, False))
        elif raw.startswith("**"):
            result.append((m.group(3), True, False, False))
        elif raw.startswith("*"):
            result.append((m.group(4), False, True, False))
        else:
            result.append((m.group(5), False, False, True))
        last = m.end()
    if last < len(text):
        result.append((text[last:], False, False, False))
    return result


def add_formatted_paragraph(
    doc: Document,
    text: str,
    style_name: str,
    align: WD_ALIGN_PARAGRAPH | None = None,
) -> docx.text.paragraph.Paragraph:
    para = doc.add_paragraph(style=style_name)
    if align is not None:
        para.alignment = align
    for seg_text, bold, italic, code in parse_inline(text):
        if not seg_text:
            continue
        run = para.add_run(seg_text)
        run.bold = bold
        run.italic = italic
        if code:
            run.font.name = "Courier New"
            run.font.size = Pt(10)
    return para


def add_caption(doc: Document, caption_text: str) -> None:
    para = doc.add_paragraph(style="Caption")
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(caption_text)
    run.italic = True


def add_word_table(doc: Document, rows_data: list[list[str]]) -> None:
    ncols = max(len(r) for r in rows_data)
    tbl = doc.add_table(rows=len(rows_data), cols=ncols)
    tbl.style = "Table Grid"
    for r_idx, row_cells_data in enumerate(rows_data):
        for c_idx in range(ncols):
            cell_text = row_cells_data[c_idx] if c_idx < len(row_cells_data) else ""
            cell = tbl.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for seg_text, bold, italic, is_code in parse_inline(cell_text):
                run = p.add_run(seg_text)
                run.bold = bold or (r_idx == 0)
                run.italic = italic
                if is_code:
                    run.font.name = "Courier New"
                    run.font.size = Pt(10)
    tbl_pr = tbl._tbl.tblPr
    jc = OxmlElement("w:jc")
    jc.set(qn("w:val"), "center")
    tbl_pr.append(jc)


def strip_md_numbering(text: str, level: int) -> str:
    if level == 1:
        text = re.sub(r"^CHƯƠNG\s+\d+[:\s]*", "", text, flags=re.IGNORECASE).strip()
    elif level in (2, 3, 4):
        text = re.sub(r"^(\d+\.)+\s*", "", text).strip()
    return text


def process_content_file(
    doc: Document,
    md_path: Path,
    is_numbered: bool,
    mermaid_counter: list[int],
) -> None:
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    in_mermaid = False
    mermaid_code = ""
    in_code = False
    code_lines: list[str] = []
    pending_table_caption: str | None = None
    table_buffer: list[str] = []
    in_table = False

    def flush_table():
        nonlocal pending_table_caption, in_table, table_buffer
        rows_raw = [r.strip() for r in table_buffer]
        rows_data = []
        for r in rows_raw:
            if re.match(r"^\|[-:\s|]+\|$", r):
                continue
            cells = [
                re.sub(r"\*\*(.+?)\*\*", r"\1", c.strip())
                for c in r.strip("|").split("|")
            ]
            rows_data.append(cells)
        if rows_data:
            if pending_table_caption:
                add_caption(doc, pending_table_caption)
                pending_table_caption = None
            add_word_table(doc, rows_data)
        table_buffer.clear()
        in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if in_mermaid:
            if stripped.startswith("```"):
                in_mermaid = False
                img_path = fetch_mermaid_png(mermaid_code, mermaid_counter[0])
                mermaid_counter[0] += 1
                if img_path and os.path.exists(img_path):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run()
                    run.add_picture(img_path, width=Inches(5.5))
            else:
                mermaid_code += line + "\n"
            i += 1
            continue

        if in_code:
            if stripped.startswith("```"):
                in_code = False
                if code_lines:
                    p = doc.add_paragraph()
                    run = p.add_run("\n".join(code_lines))
                    run.font.name = "Courier New"
                    run.font.size = Pt(10)
                code_lines.clear()
            else:
                code_lines.append(line)
            i += 1
            continue

        if stripped.startswith("```mermaid"):
            if in_table:
                flush_table()
            in_mermaid = True
            mermaid_code = ""
            i += 1
            continue

        if stripped.startswith("```"):
            if in_table:
                flush_table()
            in_code = True
            code_lines.clear()
            i += 1
            continue

        if stripped.startswith("|"):
            in_table = True
            table_buffer.append(stripped)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("> "):
            content_parts = [stripped[2:]]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith("> "):
                i += 1
                content_parts.append(lines[i].strip()[2:])
            p = add_formatted_paragraph(
                doc, " ".join(content_parts), "Content", WD_ALIGN_PARAGRAPH.JUSTIFY
            )
            p.paragraph_format.left_indent = Pt(24)
            i += 1
            continue

        if re.match(r"^\*Bảng\s+[\d\w]+[\.:].+\*\s*$", stripped):
            pending_table_caption = stripped.strip("*").strip()
            i += 1
            continue

        if re.match(r"^\*(Hình|Bảng)\s+[\d\w]+[\.:].+\*\s*$", stripped):
            add_caption(doc, stripped.strip("*").strip())
            i += 1
            continue

        if stripped == "---":
            doc.add_page_break()
            i += 1
            continue

        level = 0
        heading_text = ""
        if stripped.startswith("#### "):
            level, heading_text = 4, stripped[5:]
        elif stripped.startswith("### "):
            level, heading_text = 3, stripped[4:]
        elif stripped.startswith("## "):
            level, heading_text = 2, stripped[3:]
        elif stripped.startswith("# "):
            level, heading_text = 1, stripped[2:]

        if level > 0:
            heading_text = strip_md_numbering(heading_text, level)
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"\1", heading_text).strip()

            if is_numbered:
                style_name = f"Heading {level}"
                try:
                    doc.add_paragraph(heading_text, style=style_name)
                except KeyError:
                    p = doc.add_paragraph(heading_text)
                    p.runs[0].bold = True
            else:
                if level == 1:
                    doc.add_paragraph(heading_text, style="Heading 1N")
                else:
                    p = add_formatted_paragraph(doc, heading_text, "Content")
                    p.runs[0].bold = True
                    p.runs[0].font.size = Pt(13)
            i += 1
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = stripped[2:]
            add_formatted_paragraph(doc, bullet_text, "Bullet")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            bullet_text = re.sub(r"^\d+\.\s+", "", stripped)
            add_formatted_paragraph(doc, bullet_text, "Bullet")
            i += 1
            continue

        if re.match(r"^\[\d+\]\s+", stripped):
            add_formatted_paragraph(doc, stripped, "Content", WD_ALIGN_PARAGRAPH.JUSTIFY)
            i += 1
            continue

        add_formatted_paragraph(doc, stripped, "Content", WD_ALIGN_PARAGRAPH.JUSTIFY)
        i += 1

    if in_table:
        flush_table()


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not TEMPLATE_PATH.exists():
        print(f"Loi: Khong tim thay template tai {TEMPLATE_PATH}")
        return

    print(f"Doc template: {TEMPLATE_PATH.name}")
    doc = Document(TEMPLATE_PATH)

    print("Sua danh so de muc...")
    patch_numbering_trailing_dots(doc)

    print("Dien thong tin trang bia...")
    patch_front_matter(doc)

    print("Xoa noi dung huong dan mau...")
    remove_guide_content(doc)

    phan_cuoi_path = INPUT_DIR / "5_PhanCuoi.md"
    if phan_cuoi_path.exists():
        print("Dien Loi cam on...")
        replace_loi_cam_on(doc, phan_cuoi_path)

    dmvt_path = INPUT_DIR / "00_DanhMucTuVietTat.md"
    if dmvt_path.exists():
        print("Dien Danh muc tu viet tat...")
        replace_danh_muc_viet_tat(doc, dmvt_path)

    md_files = sorted(INPUT_DIR.glob("*.md"))
    mermaid_counter = [1]

    for md_file in md_files:
        if md_file.name == "00_DanhMucTuVietTat.md":
            continue
        is_numbered = md_file.name in CHAPTER_FILES
        print(f"Xu ly: {md_file.name}  (numbered={is_numbered})")
        process_content_file(doc, md_file, is_numbered, mermaid_counter)
        doc.add_page_break()

    doc.save(OUTPUT_PATH)
    print(f"\nHoan tat! File Word: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
