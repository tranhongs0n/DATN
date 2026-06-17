# QUY TẮC VIẾT BÁO CÁO (WRITING CONVENTIONS)

Để đảm bảo tính nhất quán, chuyên nghiệp và tránh lối viết máy móc ("AI-ish"), toàn bộ quá trình soạn thảo đồ án cần tuân thủ các quy tắc sau:

## 1. Sử dụng từ viết tắt (Abbreviations)
- **Tuyệt đối không** sử dụng cấu trúc "Từ tiếng Việt (Từ tiếng Anh)". Ví dụ: Không viết "cơ sở dữ liệu tri thức (Knowledge Base)".
- Nếu một thuật ngữ có từ viết tắt, hãy cập nhật vào file `00_DanhMucTuVietTat.md`.
- Trong văn bản, chỉ sử dụng trực tiếp từ viết tắt đó (ví dụ: dùng `KB`, `RAG`, `LLMs`, `DB`).

## 2. Định dạng và Phong cách trình bày (Formatting & Style)
- **Hạn chế in đậm (Bold) lạm dụng:** Không dùng in đậm ở đầu các gạch đầu dòng theo kiểu tóm tắt ngắn. (Ví dụ: Tránh kiểu `- **Về mặt dữ liệu:** Tập trung vào...`).
- **Tránh lạm dụng dấu ngoặc kép (" "):** Không dùng dấu ngoặc kép để nhấn mạnh thuật ngữ chuyên ngành hoặc từ thông thường (khiến câu văn trông giống văn bản do AI sinh ra). Ví dụ: Viết `hiện tượng ảo giác` thay vì `hiện tượng "ảo giác"`. Dấu ngoặc kép chỉ dùng cho trích dẫn nguyên văn hoặc tên đề tài chính thức.
- **Tránh lối liệt kê máy móc:** Thay vì lúc nào cũng dùng gạch đầu dòng phân nhánh với tiêu đề phụ, hãy chuyển thành các đoạn văn tự nhiên (paragraphs) nếu các ý có sự gắn kết liền mạch. Nếu phải liệt kê, chỉ dùng gạch đầu dòng đơn giản.
- Văn phong cần giữ tính học thuật, tự nhiên của tiếng Việt, đi thẳng vào vấn đề thay vì diễn giải dài dòng theo khuôn mẫu.
- **Không dùng từ nối liệt kê kém trang trọng:** Tuyệt đối không bắt đầu các đoạn văn bằng những cụm từ như "Thứ nhất,", "Thứ hai,", "Kế tiếp,", "Cuối cùng,". Thay vào đó, hãy sử dụng luồng logic ý tưởng để liên kết đoạn văn, hoặc dùng các cấu trúc câu chuyển ý mang tính học thuật cao hơn.
- **Quy tắc số nhiều với từ viết tắt:** Trong văn bản tiếng Việt, khi kết hợp từ chỉ số lượng với từ viết tắt tiếng Anh, KHÔNG thêm "s" ở cuối (thuần Việt hơn). Ví dụ: Viết "các LLM" thay vì "các LLMs".

## 3. Quy trình Đảm bảo chất lượng nội dung (QA Framework)
Để đảm bảo tất cả các quy tắc trên được thực thi triệt để, bắt buộc phải chạy quy trình QA Loop sau đây trước khi gửi kết quả phản hồi cuối cùng:
1. **Bước 1 (Soạn thảo):** Viết nội dung thô.
2. **Bước 2 (Chạy lệnh tự kiểm tra):** Bắt buộc sử dụng công cụ tìm kiếm mã (ví dụ `grep_search` hoặc `Select-String`) để rà soát văn bản vừa tạo. Các mẫu (Regex) bắt buộc phải kiểm tra:
   - Vi phạm ngoặc tiếng Anh: `\([a-zA-Z\s-]+\)`
   - Vi phạm từ nối liệt kê: `(Thứ nhất|Thứ hai|Thứ ba|Kế tiếp|Cuối cùng),`
   - Vi phạm số nhiều từ viết tắt: `các [A-Z]+s`
   - Lạm dụng ngoặc kép: Cần rà soát các từ nằm trong dấu ngoặc kép `"[^"]+"` để đảm bảo đó không phải là hành vi nhấn mạnh thuật ngữ sai quy tắc.
3. **Bước 3 (Sửa chữa và Hoàn tất):** Nếu Bước 2 trả về kết quả vi phạm, phải sử dụng công cụ sửa tệp để loại bỏ lỗi. Chỉ khi văn bản hoàn toàn "sạch lỗi" mới được phép thông báo hoàn thành cho người dùng.

## 4. Khung quy trình làm việc (Workflow Framework)
Để đảm bảo chất lượng nội dung đạt độ sâu tối đa và đúng ý đồ, bắt buộc phải tuân thủ quy trình "Chia để trị" 3 bước sau đối với bất kỳ phần mục nào:
1. **Bước 1 (Lên danh sách ý tưởng - Brainstorming List):** Không viết văn bản chi tiết ngay. Bắt đầu bằng việc liệt kê các ý chính (gạch đầu dòng) cần trình bày trong mục đó.
2. **Bước 2 (Vòng lặp phản hồi - Feedback Loop):** Gửi danh sách ý tưởng cho người dùng đánh giá. Lặp lại việc tinh chỉnh, thêm bớt ý tưởng cho đến khi người dùng hoàn toàn đồng ý chốt danh sách.
3. **Bước 3 (Triển khai chi tiết - Detailed Drafting):** Chỉ sau khi danh sách ý tưởng được chốt, mới tiến hành viết văn bản chi tiết dựa trên dàn ý đó. Đồng thời, bắt buộc phải chạy luồng QA Framework (Mục 3) trước khi trả kết quả cuối cùng.
