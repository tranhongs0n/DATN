# ĐÁNH GIÁ PHẢN BIỆN ĐỒ ÁN TỐT NGHIỆP
**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG
**Nhận định chung:** Đồ án có dấu hiệu sinh bằng AI (LLM) rất rõ rệt. Nội dung thiếu chiều sâu học thuật, mâu thuẫn logic nghiêm trọng và sử dụng văn phong dịch thuật máy móc. Cần chỉnh sửa toàn diện hoặc đánh trượt nếu không giải trình được thực tế nghiên cứu.

## 1. Dấu hiệu sinh tự động (AI Pattern Recognition & Linguistic Authenticity)
**Đánh giá:** Rất cao. Văn phong mang đậm phong cách dịch thuật từ tiếng Anh (translationese) và lạm dụng các cấu trúc liệt kê đặc trưng của ChatGPT/Gemini.
- **Trích dẫn lỗi 1:** *"Cơ chế này định lượng mức độ tương quan giữa các từ trong chuỗi đầu vào song song, loại bỏ điểm yếu phụ thuộc tuần tự của các mạng truyền thống."* (Chương 1)
  - **Phân tích:** Dịch cứng nhắc từ "quantifies the degree of correlation... parallel input sequences". Không sử dụng ngôn ngữ học thuật tự nhiên của ngành CNTT Việt Nam.
- **Trích dẫn lỗi 2:** *"Sự suy thoái ngữ cảnh cũng xuất hiện trong các phiên đối thoại kéo dài"* (Phần cuối)
  - **Phân tích:** "Sự suy thoái ngữ cảnh" là dịch word-by-word của "context degradation". Người Việt thường dùng "mất ngữ cảnh" hoặc "trôi ngữ cảnh".
- **Trích dẫn lỗi 3:** *"Việc thử nghiệm thực tế các tham số tiền xử lý mang lại dữ liệu tham chiếu hữu ích cho việc triển khai RAG trên văn bản hành chính địa phương."* (Phần mở đầu)
  - **Phân tích:** Ảo giác AI rõ rệt. Đề tài làm về trường Đại học, tại sao lại kết luận về "văn bản hành chính địa phương" (local government documents)? AI đã tự động sinh một câu kết luận mẫu (template conclusion).

## 2. Tính toàn vẹn học thuật và Đạo văn (Academic Integrity)
**Đánh giá:** Yếu. Trình bày kiến thức nền tảng như của riêng mình, lờ đi trích dẫn gốc.
- **Lỗi thiếu trích dẫn bối cảnh:** Toàn bộ phần 1.1, 1.2, 1.3, 1.4 trình bày về Transformer, LLM, RAG nhưng **không hề có một trích dẫn nào** trong văn bản (in-text citation) trỏ về Vaswani (Transformer) hay Lewis (RAG), dù có liệt kê ở mục Tài liệu tham khảo. 
- **Lỗi tổng quan hời hợt:** *"Hệ thống Pounce tại Đại học Bang Georgia [1] hỗ trợ cung cấp thông tin nhập học. Nền tảng Genie tại Đại học Deakin [2] hướng dẫn dịch vụ sinh viên."* (Chương 1). Chỉ tóm tắt bằng đúng 1 câu vô thưởng vô phạt, không phân tích sâu kỹ thuật họ dùng là gì, ưu nhược điểm ra sao. Rõ ràng là AI tóm tắt từ khóa.

## 3. Độ sâu kỹ thuật và Lỗ hổng Phương pháp luận (Methodological Rigor)
**Đánh giá:** Rất hời hợt. Tự mâu thuẫn logic chứng tỏ tác giả không thực sự xây dựng hoặc không hiểu hệ thống.
- **MÂU THUẪN LOGIC CHÍNH:**
  - Tại Chương 2 (2.2) chém gió: *"Thông tin về năm ban hành và bậc đào tạo được nhúng chặt vào cấu trúc vector... dò tìm và xóa bỏ các vector mang cùng nguồn phát hành"*.
  - Tại Chương 4 (4.3.2) lại biện minh lỗi: *"Vấn đề niên khóa của tài liệu tạo ra thách thức khi hệ thống nhúng nhầm quy chế cũ do tài liệu nguồn không chứa siêu dữ liệu về năm ban hành."*
  - **Phân tích:** Nếu đã "nhúng chặt" ở Chương 2, tại sao Chương 4 lại báo "không chứa siêu dữ liệu"? Đây là bằng chứng thép cho việc dùng AI sinh từng chương rời rạc mà không có sự kiểm duyệt logic.
- **Thiếu kiểm chứng thực nghiệm:** *"chạy trên tập dữ liệu kiểm thử gồm 50 câu hỏi đa dạng."* (Chương 4). 50 câu hỏi là con số quá nhỏ, không đủ ý nghĩa thống kê cho một đồ án tốt nghiệp đại học. Đánh giá "Độ chính xác 0.88" vô nghĩa khi không trình bày phương pháp chấm điểm (ai chấm? chấm bằng thang đo nào? exact match hay semantic similarity?).

## 4. Cấu trúc và Hình thức (Formatting & Structural Cohesion)
**Đánh giá:** Đạt chuẩn hình thức cơ bản của Markdown/Văn bản nhưng đứt gãy logic học thuật.
- Đoạn kết luận và tóm tắt chỉ lặp lại các từ khóa một cách máy móc. 
- Không có mô tả chi tiết về hàm mất mát, siêu tham số cụ thể của thuật toán phân rã ngoài việc nhắc đến "1000/200" một cách chung chung. Các bảng số liệu (Bảng 4.1) không có độ lệch chuẩn hay phân tích biến thiên.

**KẾT LUẬN CUỐI CÙNG:** Đồ án có xác suất sinh bởi AI >95%. Sinh viên cần đối chất trực tiếp về mã nguồn và giải thích mâu thuẫn giữa Chương 2 và Chương 4. Đề nghị hội đồng đánh giá khắt khe phần thực hành.
