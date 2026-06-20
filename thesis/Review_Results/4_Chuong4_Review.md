# Đánh Giá 4_Chuong4.md

## 1. Dấu Hiệu AI & Ngôn Ngữ (AI Pattern Recognition & Linguistic Authenticity)
**Đánh giá: AI sinh 100% (High probability of AI generation).**

Lỗi hành văn hoa mỹ, sáo rỗng (Poetic AI / Word salad).
> "...bức tranh toàn cảnh về năng lực của hệ thống đã được khắc họa rõ nét."
> "Trải nghiệm thực tế của toàn bộ hệ thống được hội tụ qua hai không gian giao diện tương tác độc lập."
Lý do: Báo cáo kỹ thuật không dùng văn phong "khắc họa bức tranh" hay "hội tụ không gian". Dấu hiệu rõ ràng của AI sinh chữ nhồi nhét.

Lỗi cấu trúc câu dập khuôn (Predictable structures).
> "Quá trình này không chỉ dừng lại ở việc... mà còn phân tích sâu vào..."
Lý do: Cấu trúc "not only... but also" kinh điển của LLM.

Lỗi lặp từ ngớ ngẩn (Redundancy).
> "...giao diện điều khiển trung tâm nền tảng Web mang đến một bảng điều khiển mang tính kỹ thuật cao."
Lý do: AI sinh văn bản thiếu kiểm soát logic.

## 2. Tính Liêm Chính Học Thuật (Academic Integrity)
Lỗi ngụy tạo số liệu kiểm thử (Fabricated evaluation metrics).
> Bảng 4.1: Điểm số 0.98, 0.95, 1.00...
> Đoạn: "50 học sinh trung học phổ thông thao tác trực tiếp... MOS đạt 4.2/5"
Lý do: Các chỉ số RAG (Context Precision, Faithfulness) đòi hỏi ground truth và thư viện đánh giá (như Ragas, TruLens). Sinh viên không đề cập công cụ đo lường nhưng lại đưa ra con số chính xác 0.98. Khảo sát 50 học sinh ở đâu? Minh chứng đâu? Rất có khả năng sinh viên prompt "Tạo bảng kết quả đánh giá RAG đẹp, hợp lý". Đây là vi phạm liêm chính học thuật (ngụy tạo số liệu).
Hành động: Yêu cầu cung cấp source code đo lường (evaluate.py), file export log đánh giá, danh sách 50 học sinh và form khảo sát. Xóa toàn bộ nếu không có minh chứng.

## 3. Độ Sâu Kỹ Thuật (Methodological Rigor)
Lỗi test tải vô căn cứ (Unvalidated load testing).
> "...thử nghiệm tăng tải lên mức 200 yêu cầu đồng thời, hệ thống bắt đầu ghi nhận mã lỗi 429..."
Lý do: API free/tier thấp của Gemini giới hạn Rate Limit (RPM/RPD) rất thấp (ví dụ 15 RPM). Gửi 200 concurrent requests là bất khả thi nếu không có Enterprise tier. Sinh viên hallucinate thông số test tải.
Hành động: Cung cấp report của JMeter/Locust chứng minh test tải 200 CCU.

## 4. Hình Thức (Formatting)
Mô tả ví dụ hội thoại dài dòng, thay vì dùng dạng bảng trích xuất (Input - Expected - Output - Metric).

Kết luận: Vi phạm liêm chính học thuật nghiêm trọng (bịa số liệu). Đánh trượt hoặc yêu cầu làm lại toàn bộ chương 4 với số liệu thực chạy.
