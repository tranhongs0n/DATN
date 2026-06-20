# ĐÁNH GIÁ PHẢN BIỆN LẦN 3 (CỰC KỲ NGHIÊM TRỌNG)
**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG

**Nhận định chung:** Mức độ sử dụng AI để lấp liếm lỗi sai đã đến mức **báo động đỏ về đạo đức học thuật**. Việc sinh viên phản hồi quá nhanh (vài phút) chứng tỏ bạn không hề tự tay viết hay đọc lại bài, mà chỉ đơn thuần "ném" lỗi vào LLM và bảo nó tự sửa. Kết quả là tạo ra một "mớ bòng bong" số liệu giả.

## 1. Số liệu thực nghiệm bịa đặt (Tội nặng nhất)
Bạn đã dùng AI để sinh bảng số liệu Ragas ở Chương 4 (Bảng 4.1) một cách hoàn toàn vô căn cứ.
- **Mâu thuẫn 1:** Trong `4_Chuong4.md` (mục 4.1), bạn mạnh miệng tuyên bố: *"Tập dữ liệu này bao gồm 1.200 cặp câu hỏi - câu trả lời được trích xuất ngẫu nhiên"*.
- **Mâu thuẫn 2:** Tuy nhiên, trong file thiết kế đánh giá gốc của bạn (`Evaluation\00_TongQuanDanhGia.md`), mục 2 lại ghi rành rành: *"Ma trận kiểm thử bao gồm tổng cộng 250 câu hỏi giả định"*.
- **Mâu thuẫn 3:** Trong phần phân tích (4.3.2), bạn lại quên chưa xóa câu văn phân tích của bảng cũ: *"Hệ thống gặp rào cản khi xử lý nhóm câu hỏi điều kiện chéo với chỉ số chính xác giảm xuống mức 0.72"*. Trong khi đó, ở cái Bảng 4.1 "mới" mà bạn vừa bịa ra, chả có con số 0.72 nào ở Nhóm 3 cả (Context Precision 0.75, Context Recall 0.70).
=> **Kết luận:** Bạn chém gió từ 50 câu -> 1200 câu (trong word) -> 250 câu (trong thiết kế). Toàn bộ số liệu chạy đánh giá của bạn là **bịa đặt** (fake data) bởi AI.

## 2. Phần sửa điểm cộng (Duy nhất 1 chỗ)
- Ở Chương 1 (mục 1.5), bạn (hay đúng hơn là AI của bạn) đã phân tích khá tốt về lỗ hổng của các hệ thống chatbot thế hệ 2 dùng phân loại ý định (Rasa, Dialogflow) khi gặp câu hỏi điều kiện chéo, qua đó làm bật lên giá trị của RAG. Đây là một đoạn có chất lượng chuyên môn tốt. Nhưng một hạt sạn tốt không cứu được cả nồi cơm khê.

**KẾT LUẬN LẦN 3 VÀ QUYẾT ĐỊNH:** 
Hành vi giả mạo số liệu kiểm thử là lỗi vi phạm nghiêm trọng nhất trong làm nghiên cứu khoa học/đồ án. Yêu cầu sinh viên trình bày mã nguồn thư mục chạy Ragas và file xuất log thật của 250 (hay 1200?) câu hỏi. Nếu không chứng minh được file log thực tế khớp với số liệu trong báo cáo, đồ án này xứng đáng nhận điểm F.
