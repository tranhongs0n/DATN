# RAG (Retrieval-Augmented Generation) & Ảo giác (Hallucination)

## 1. RAG là gì?
RAG là kỹ thuật cung cấp thêm thông tin bên ngoài cho LLM (Mô hình ngôn ngữ lớn) trước khi nó sinh ra câu trả lời.
- **Quy trình:** Người dùng hỏi -> Hệ thống tìm kiếm tài liệu liên quan trong Cơ sở dữ liệu -> Nối tài liệu vào câu hỏi (Context) -> Gửi cho LLM -> LLM sinh câu trả lời dựa trên tài liệu đó.
- **Tại sao dùng RAG cho tuyển sinh?** Quy chế tuyển sinh thay đổi hàng năm và đòi hỏi độ chính xác tuyệt đối 100%. LLM bình thường không được huấn luyện trên dữ liệu nội bộ của ĐH Thủy Lợi, nên nếu chỉ hỏi LLM chay, nó sẽ trả lời sai.

## 2. Ảo giác (Hallucination) là gì?
- Là hiện tượng LLM trả lời sai sự thật, tự bịa ra thông tin (như tự chế ra một điểm chuẩn ảo) nhưng với giọng điệu rất tự tin.
- **Cách khắc phục trong hệ thống:** Prompt (câu lệnh hệ thống) ép buộc LLM CHỈ ĐƯỢC DÙNG dữ liệu từ tài liệu cung cấp. Cài đặt luật: nếu context trống, phải trả lời "Tôi không có thông tin, vui lòng liên hệ phòng đào tạo".

## 3. Tại sao chọn RAG thay vì Fine-tuning (Tinh chỉnh mô hình)?
- **Fine-tuning:** Dạy lại mô hình bằng cách cập nhật trọng số. Cần rất nhiều dữ liệu, tốn tiền mua GPU, mất thời gian, và khi quy chế đổi phải huấn luyện lại từ đầu. Rất khó để xóa một kiến thức đã dạy.
- **RAG:** Dùng mô hình có sẵn (như Gemini). Chỉ việc thay đổi cơ sở dữ liệu bên ngoài. Thêm, sửa, xóa quy chế dễ dàng, phản ánh ngay lập tức mà không cần tốn tiền huấn luyện lại.
