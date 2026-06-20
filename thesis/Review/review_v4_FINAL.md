# BIÊN BẢN ĐÁNH GIÁ CHUNG KHẢO (QUYẾT ĐỊNH CUỐI CÙNG)
**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG

**Nhận định chung:** Sinh viên đã nộp lại file log và chỉnh sửa các mâu thuẫn câu chữ. Tuy nhiên, hành động này càng phơi bày rõ hơn bản chất làm giả số liệu và lạm dụng công cụ AI một cách vô tội vạ. 

## Bằng chứng giả mạo khoa học (Khoảng thời gian thực thi)
1. **Sự vô lý về mặt thời gian:** Bạn nộp lại bản sửa lỗi cùng 2 file `ragas_1200_dataset.json` (371KB) và `ragas_eval_1200_log.csv` (63KB) chỉ trong vòng **vài phút** sau khi bị yêu cầu. 
2. **Bản chất của Ragas:** Framework Ragas đánh giá tự động dựa trên việc gọi API của các LLM (như GPT-4, Gemini) để chấm điểm từng tiêu chí (Precision, Recall, Faithfulness, Relevancy) cho từng câu hỏi. Việc gọi API để sinh câu trả lời và chấm điểm cho **1.200 câu hỏi** sẽ tiêu tốn hàng nghìn lượt API calls. Tốc độ trung bình (kể cả có chạy batch/async) sẽ mất ít nhất vài tiếng đồng hồ và tốn một khoản chi phí API không nhỏ. 
3. **Kết luận:** Việc bạn tạo ra file CSV 1200 dòng trong vòng vài phút chứng minh 100% rằng file CSV này là **do AI (như ChatGPT hoặc Gemini) viết ra nguyên xi một bảng dữ liệu giả**, chứ không hề có một hệ thống RAG thực sự nào chạy qua Ragas.

## Nhận xét tổng kết
Dù bạn đã dùng AI để lấp liếm các mâu thuẫn logic về văn bản (sửa câu chữ cho khớp bảng số liệu, giải thích 1200 vs 250 câu), nhưng khoa học thực nghiệm không thể dùng ngôn từ để che đậy. Đồ án của bạn là một tác phẩm được sinh ra hoàn toàn bằng prompt AI, từ văn bản, kiến trúc, cho đến số liệu kiểm thử, mà không có thực chứng hệ thống.

**QUYẾT ĐỊNH CỦA HỘI ĐỒNG:** 
- **ĐÁNH TRƯỢT (ĐIỂM F)** môn Đồ án Tốt nghiệp.
- Sinh viên bị đình chỉ bảo vệ kỳ này do vi phạm quy tắc liêm chính học thuật (ngụy tạo số liệu nghiên cứu khoa học). Sinh viên phải làm lại một đề tài khác vào học kỳ sau và chứng minh được toàn bộ mã nguồn thực thi cũng như nhật ký hệ thống (system logs) thực tế.
