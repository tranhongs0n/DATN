# ĐÁNH GIÁ PHẢN BIỆN LẦN 2 (SAU KHI SỬA ĐỔI)
**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG

**Nhận định chung:** Sinh viên đã có nỗ lực sửa chữa các lỗi dịch thuật máy móc và thêm trích dẫn. Tuy nhiên, việc sửa đổi mang tính đối phó, cắt ghép (copy-paste) thiếu cẩn trọng, dẫn đến tạo ra những mâu thuẫn học thuật MỚI còn nghiêm trọng hơn cả bản gốc. Dấu hiệu dùng AI để sinh nội dung đối phó vẫn cực kỳ rõ rệt.

## 1. Mâu thuẫn Logic mới (Cực kỳ nghiêm trọng)
Tại Chương 4, sinh viên cố gắng giải quyết lời phê bình "50 câu hỏi là quá ít" bằng cách chèn thêm một đoạn hoành tráng về framework Ragas, nhưng lại quên sửa bảng kết quả:
- **Tại mục 4.1:** Tuyên bố sử dụng *framework đánh giá tự động Ragas trên tập dữ liệu quy mô lớn 1.200 cặp câu hỏi*. Liệt kê 4 thang đo của Ragas: Context Precision, Context Recall, Faithfulness, Answer Relevancy.
- **Tại mục 4.2 (Bảng kết quả):** Vẫn giữ nguyên văn bản cũ *"Kết quả trích xuất trực tiếp từ kịch bản tự động evaluate.py trên 50 truy vấn"*. Bảng kết quả (Bảng 4.1) không hề có 4 thang đo Ragas mà vẫn dùng 2 thang đo cũ ("Độ chính xác truy xuất", "Độ trễ trung bình") với nguyên vẹn các con số cũ (0.88, 0.84...).
**=> Đánh giá:** Lỗi "râu ông nọ cắm cằm bà kia". Rõ ràng sinh viên đã yêu cầu AI sinh thêm đoạn văn mô tả "1200 câu hỏi và framework Ragas" rồi dán vào phần Phương pháp, nhưng lười/quên không cập nhật phần Kết quả. Đây là minh chứng rõ nhất cho việc thiếu trung thực học thuật và không thực sự chạy thực nghiệm.

## 2. Các vấn đề chưa được khắc phục (Từ lần 1)
- **Tổng quan nghiên cứu (Mục 1.5) vẫn hời hợt:** Sinh viên chưa hề sửa lỗi này. Các trích dẫn [1], [2] về hệ thống Pounce và Genie vẫn chỉ được mô tả bằng đúng 1 câu vô thưởng vô phạt (*"Hệ thống Pounce tại Đại học Bang Georgia [1] hỗ trợ cung cấp thông tin nhập học"*). Không có sự phân tích độ sâu về kỹ thuật của các nghiên cứu trước. 

## 3. Các điểm đã sửa (Có tiến bộ nhưng chưa đủ)
- Đã sửa các lỗi dịch thuật ngô nghê ("suy thoái ngữ cảnh" -> "trôi ngữ cảnh", bỏ câu "văn bản hành chính địa phương").
- Đã thêm trích dẫn Vaswani (2017) và Lewis (2020) vào văn bản.
- Đã xử lý khéo léo mâu thuẫn logic siêu dữ liệu ở Chương 2 và Chương 4 bằng cách thêm lời giải thích *"trong điều kiện lý tưởng..."* (Chương 2) và *"thực tế vận hành cho thấy việc bóc tách thông tin này đôi khi gặp lỗi..."* (Chương 4).

**KẾT LUẬN LẦN 2:** Vẫn chưa đạt yêu cầu bảo vệ. Sinh viên sửa lỗi theo kiểu "chữa cháy" cục bộ bằng AI mà không đọc kỹ lại toàn bộ văn bản, gây ra mâu thuẫn số liệu nghiêm trọng ở Chương 4 (Tuyên bố làm 1200 câu nhưng kết quả chỉ có 50 câu). Hội đồng yêu cầu sinh viên cung cấp log file/báo cáo xuất ra từ Ragas cho 1200 câu hỏi để chứng minh không làm giả số liệu.
