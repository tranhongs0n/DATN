# QUY TẮC VIẾT BÁO CÁO

Tránh văn AI. Chuyên nghiệp, nhất quán.

## 1. Viết tắt và Thuật ngữ tiếng Anh (Abbreviations & Terminology)
- **Cấm viết song ngữ:** Cấm mẫu "Từ tiếng Việt (Tiếng Anh)". Ví dụ: cấm viết "cơ sở dữ liệu tri thức (Knowledge Base)".
- **Quy trình xử lý thuật ngữ mới:** Nếu bắt buộc phải dùng một khái niệm tiếng Anh mới, hãy dịch thuần sang tiếng Việt trong văn bản báo cáo. Sau đó, **bắt buộc** mang thuật ngữ nguyên gốc tiếng Anh đó ghi vào bảng ở tệp `00_DanhMucTuVietTat.md` để lưu vết tham chiếu.
- Chỉ dùng trực tiếp từ viết tắt (`KB`, `RAG`) nếu nó đã được định nghĩa trong `00_DanhMucTuVietTat.md`.

## 2. Định dạng & Phong cách (Formatting & Style)
- **Cấm in đậm tiêu đề con đầu dòng:** Cấm `- **Tên:** Mô tả` hoặc `1. **Bước 1:** Mô tả`. Viết câu tự nhiên.
- **Cấm ngoặc kép nhấn mạnh:** Cấm `hiện tượng "ảo giác"`. Viết `hiện tượng ảo giác`. Dấu `""` chỉ cho trích dẫn/tên đề tài.
- **Tránh liệt kê máy móc:** Thay gạch đầu dòng bằng đoạn văn liền mạch nếu được.
- **Văn phong:** Học thuật, tự nhiên, đi thẳng vấn đề.
- **Cấm từ nối liệt kê & văn AI:** Cấm "Thứ nhất,", "Thứ hai,", "Kế tiếp,", "Kế đến,", "Cuối cùng,", "Hơn nữa,", "Đồng thời,", "Tuy nhiên,". Tránh chủ ngữ giả như "Việc thiết lập", "Quá trình này". Dùng động từ mạnh và luồng logic để chuyển ý.
- **Quy tắc số nhiều:** Cấm thêm "s" vào từ viết tắt. Dùng "các LLM" thay "các LLMs".
- **Cấm dấu gạch ngang dài (—):** Dùng (), phẩy, hoặc hai chấm.
- **Cấm Emoji:** Không sử dụng bất kỳ biểu tượng cảm xúc (emoji) nào trong toàn bộ tài liệu báo cáo.
## 3. Quy trình QA (QA Framework)
Chạy QA Loop trước khi trả kết quả:
1. **Bước 1:** Viết thô.
2. **Bước 2 (Kiểm tra Regex):** Dùng `grep_search`. Rà soát:
   - Ngoặc tiếng Anh: `\([a-zA-Z\s-]+\)`
   - Từ nối & Văn AI: `(Thứ nhất|Thứ hai|Thứ ba|Kế tiếp|Kế đến|Cuối cùng|Hơn nữa|Đồng thời|Tuy nhiên),`
   - Số nhiều: `các [A-Z]+s`
   - In đậm danh sách: `^\s*[-*0-9.]+\s*\*\*[^*]+\*\*\s*:`
   - Ngoặc kép: `"[^"]+"` (tránh nhấn mạnh sai).
3. **Bước 3:** Sửa lỗi nếu có. Chỉ trả kết quả khi sạch lỗi.

## 4. Khung quy trình (Workflow Framework)
Tuân thủ 3 bước "Chia để trị":
1. **Bước 1 (Brainstorm):** Chỉ gạch đầu dòng ý chính. Không viết chi tiết.
2. **Bước 2 (Feedback):** Gửi người dùng chốt ý tưởng.
3. **Bước 3 (Triển khai):** Viết chi tiết theo dàn ý chốt. Chạy QA (Mục 3) trước khi trả kết quả.

## 5. Chiều sâu kỹ thuật & Tính xác thực (Technical Rigor & Integrity)
- **Cấm mô tả chung chung:** Không liệt kê tính năng suông (vd: "gọi API", "trích xuất metadata"). Phải nêu đích danh thuật toán (vd: "thuật toán Token-Bucket", "OpenCV kết hợp PaddleOCR").
- **Tính chính xác của thuật toán và kiến trúc:** Phải ghép đúng công nghệ với bản chất vấn đề (Vd: Phân tích DOCX phải dùng cấu trúc OpenXML thay vì DOM HTML; Nhận diện chữ phải dùng OCR thay vì YOLOv8; Giới hạn rate limit phải code đúng logic Token-Bucket thực tế thay vì chia tỷ lệ đơn giản).
- **Tính chính xác của Thống kê & Toán học:** 
  - Phân phối độ dài văn bản thường tuân theo Log-Normal hoặc Poisson, tuyệt đối không chém gió thành phân phối chuẩn Gauss. 
  - Hệ số đồng thuận nhãn: Dùng Cohen's Kappa cho 2 người (rater) và Fleiss' Kappa cho >= 3 người.
- **Số liệu Benchmark & Thực nghiệm:** 
  - Bảng so sánh công nghệ bắt buộc có thông số thực nghiệm (độ trễ P95, dung lượng RAM) và cấu hình máy (Hardware specs).
  - Không ngụy tạo thông số phi thực tế (Vd: Cấm thiết lập 10.000 luồng JMeter đồng thời trên laptop; Cấm đo metric ở Chương 5 nếu chưa được thực nghiệm ở Chương 4). 
- **Tính xác thực của dữ liệu:** Không ngụy tạo số liệu. Khi dùng tập dữ liệu lớn, phải có phương pháp luận minh bạch (vd: Data Augmentation sinh dữ liệu bằng LLM kết hợp kiểm định chéo, thiết lập Mock Server bằng FastAPI để test lõi mạng cục bộ).
