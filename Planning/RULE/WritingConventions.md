# QUY TẮC VIẾT BÁO CÁO

Tránh văn AI. Chuyên nghiệp, nhất quán.

## 1. Viết tắt (Abbreviations)
- **Cấm:** "Từ tiếng Việt (Tiếng Anh)". Ví dụ: cấm "cơ sở dữ liệu tri thức (Knowledge Base)".
- Thêm từ viết tắt mới vào `00_DanhMucTuVietTat.md`.
- Chỉ dùng trực tiếp từ viết tắt (`KB`, `RAG`).

## 2. Định dạng & Phong cách (Formatting & Style)
- **Cấm in đậm tiêu đề con đầu dòng:** Cấm `- **Tên:** Mô tả` hoặc `1. **Bước 1:** Mô tả`. Viết câu tự nhiên.
- **Cấm ngoặc kép nhấn mạnh:** Cấm `hiện tượng "ảo giác"`. Viết `hiện tượng ảo giác`. Dấu `""` chỉ cho trích dẫn/tên đề tài.
- **Tránh liệt kê máy móc:** Thay gạch đầu dòng bằng đoạn văn liền mạch nếu được.
- **Văn phong:** Học thuật, tự nhiên, đi thẳng vấn đề.
- **Cấm từ nối liệt kê:** Cấm "Thứ nhất,", "Thứ hai,", "Kế tiếp,", "Cuối cùng,". Dùng luồng logic để chuyển ý.
- **Quy tắc số nhiều:** Cấm thêm "s" vào từ viết tắt. Dùng "các LLM" thay "các LLMs".
- **Cấm dấu gạch ngang dài (—):** Dùng (), phẩy, hoặc hai chấm.

## 3. Quy trình QA (QA Framework)
Chạy QA Loop trước khi trả kết quả:
1. **Bước 1:** Viết thô.
2. **Bước 2 (Kiểm tra Regex):** Dùng `grep_search`. Rà soát:
   - Ngoặc tiếng Anh: `\([a-zA-Z\s-]+\)`
   - Từ nối liệt kê: `(Thứ nhất|Thứ hai|Thứ ba|Kế tiếp|Cuối cùng),`
   - Số nhiều: `các [A-Z]+s`
   - In đậm danh sách: `^\s*[-*0-9.]+\s*\*\*[^*]+\*\*\s*:`
   - Ngoặc kép: `"[^"]+"` (tránh nhấn mạnh sai).
3. **Bước 3:** Sửa lỗi nếu có. Chỉ trả kết quả khi sạch lỗi.

## 4. Khung quy trình (Workflow Framework)
Tuân thủ 3 bước "Chia để trị":
1. **Bước 1 (Brainstorm):** Chỉ gạch đầu dòng ý chính. Không viết chi tiết.
2. **Bước 2 (Feedback):** Gửi người dùng chốt ý tưởng.
3. **Bước 3 (Triển khai):** Viết chi tiết theo dàn ý chốt. Chạy QA (Mục 3) trước khi trả kết quả.
