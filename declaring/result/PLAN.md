# PLAN TO FILL THE THESIS DECLARATION DOCUMENT

## Goal
Fill the template file `Mau Word_Huong_dan_SV_lam_ro_noi_dung_do_an_tot_nghiep.docx` with Trần Hồng Sơn's thesis details and save it as `D:\DATN_FInal\declaring\result\Huong_dan_SV_lam_ro_noi_dung_do_an_tot_nghiep_TranHongSon.docx`.

## Steps
1. **Analyze Document Structure:**
   - Template contains tables. First table is student details.
   - Subsequent tables correspond to Bước 1 through Bước 8, plus a final summary table.
   - Text placeholders use dots (e.g., `........................`).

2. **Automated Filling Strategy (Python Script):**
   - Write a python script `fill_docx.py` using `python-docx` to programmatically open the template and modify the table cells.
   - **Table 0 (Student Info):**
     - Cell (0, 1): Fill Student name `Trần Hồng Sơn`
     - Cell (0, 3): Fill Project Title `Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG`
     - Cell (1, 1): Fill ID `1951060985`
     - Cell (1, 3): Fill Target Users `Thí sinh, phụ huynh tra cứu thông tin; Ban tuyển sinh Trường Đại học Thủy Lợi quản trị dữ liệu.`
     - Cell (2, 1): Fill Class `61TH1`
     - Cell (2, 3): Fill Tech `FastAPI / ChromaDB / Google Gemini / LangChain / Zalo OA / React / SQLite`
     - Cell (3, 1): Fill Advisor `TS. Lý Anh Tuấn`
     - Cell (3, 3): Fill Duration `31/03/2026 - 30/06/2026`
     - Cell (4, 1): Fill Reviewer `....................................` (Blank)
     - Cell (4, 3): Fill Submission Date `30/06/2026`
   - **Step Tables (Bước 1 to 8):**
     - Locate each step table based on text content (e.g., "BƯỚC 1", "BƯỚC 2", etc.).
     - In each step table, find the cell containing the `....................` pattern in column index 2 (Answer column) and replace it with the detailed markdown text mapped from `gathered_information.md`.
     - Specifying percentages in Step 8:
       - "Tham khảo/kế thừa: 30 %"
       - "Tự làm/đóng góp: 70 %"
       - "Mức độ tự hiểu: 95 %"
   - **Final Summary Table:**
     - Locate the summary table. Fill the cell under "ĐỒ ÁN THỰC SỰ ĐÓNG GÓP GÌ?" with the summary of contributions.

3. **Execution & Verification:**
   - Run the script `fill_docx.py`.
   - Verify file generation.
   - Extract content from the new document to ensure text replaced properly.
