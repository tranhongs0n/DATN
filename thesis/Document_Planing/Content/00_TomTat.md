**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG
**Sinh viên:** Trần Hồng Sơn (61TH1)
**GVHD:** TS. Lý Anh Tuấn

Đề tài tập trung thiết kế và phát triển hệ thống trợ lý ảo hỗ trợ công tác tư vấn tuyển sinh tại Trường Đại học Thủy Lợi, hướng tới mục tiêu tự động hóa việc giải đáp thông tin đa phân luồng. Triển khai cơ chế phân tách và lập chỉ mục đa luồng, hỗ trợ chuyển đổi linh hoạt các định dạng văn bản (PDF, DOCX) thành Vector Database. Hệ thống truy xuất nhanh chóng các điều khoản quy định giáo dục mà không phá vỡ cấu trúc ngữ nghĩa gốc.

Mô hình thiết kế khung chỉ thị cá nhân hóa trên lõi Google Gemini, bắt buộc mạng nơ-ron trả lời dựa trên tài liệu cung cấp. Hệ thống giải quyết tốt bài toán lọc câu hỏi ngoài phạm vi nghiệp vụ giáo dục nhằm ngăn chặn hiện tượng cung cấp thông tin sai lệch ngoài dữ liệu gốc của nhà trường.

Cấu trúc đồ án gồm 4 chương. Chương 1 trình bày cơ sở lý thuyết về bài toán hỏi đáp và mô hình RAG. Chương 2 phân tích yêu cầu thiết kế hệ thống. Chương 3 triển khai các luồng xử lý kỹ thuật trên máy chủ FastAPI. Chương 4 thiết lập kịch bản đánh giá để kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác của hệ thống.
