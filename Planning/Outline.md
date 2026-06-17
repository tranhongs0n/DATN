# Cấu Trúc Đồ Án Tốt Nghiệp
Đề tài: Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG.
Sinh viên: Trần Hồng Sơn

## LỜI CẢM ƠN
## TÓM TẮT ĐỒ ÁN
## MỤC LỤC
## DANH MỤC HÌNH ẢNH, BẢNG BIỂU, TỪ VIẾT TẮT

## PHẦN MỞ ĐẦU
1. Lý do chọn đề tài (Tính cấp thiết của hệ thống hỗ trợ tuyển sinh tự động).
2. Mục tiêu nghiên cứu (Tạo ra chatbot RAG trả lời chính xác thông tin tuyển sinh).
3. Đối tượng và phạm vi nghiên cứu (Thông tin tuyển sinh Đại học Thủy Lợi).
4. Phương pháp nghiên cứu.

## CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ ÁP DỤNG
1.1. Tổng quan về Trợ lý ảo (Chatbot) và bài toán hỏi đáp (Q&A).
1.2. Giới thiệu về Mô hình ngôn ngữ lớn (Large Language Model - LLM).
1.3. Kỹ thuật Retrieval-Augmented Generation (RAG):
   - Khái niệm và cơ chế hoạt động.
   - Ưu điểm của RAG so với việc Fine-tuning mô hình.
1.4. Cơ sở dữ liệu Vector (Vector Database) và kỹ thuật Embedding.
1.5. Các công nghệ sử dụng trong đề tài (LangChain, LlamaIndex, OpenAI/Gemini/Open-source LLM, v.v.).

## CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
2.1. Phân tích yêu cầu hệ thống:
   - Yêu cầu chức năng (Người dùng cuối, Quản trị viên).
   - Yêu cầu phi chức năng (Hiệu năng, độ trễ, tính chính xác).
2.2. Phân tích dữ liệu tuyển sinh Trường Đại học Thủy Lợi.
2.3. Thiết kế kiến trúc tổng thể của hệ thống RAG.
   - Pipeline tiền xử lý dữ liệu (Data Ingestion Pipeline).
   - Pipeline truy vấn và sinh câu trả lời (Retrieval & Generation Pipeline).
2.4. Thiết kế Use Case và luồng hoạt động (Activity Diagrams).
2.5. Thiết kế giao diện và nền tảng tương tác.

## CHƯƠNG 3: TRIỂN KHAI, THỬ NGHIỆM VÀ ĐÁNH GIÁ
3.1. Quá trình thu thập và chuẩn bị dữ liệu (Crawling, làm sạch và chia nhỏ dữ liệu văn bản).
3.2. Cài đặt các thành phần cốt lõi:
   - Nhúng và lưu trữ vào Vector Database.
   - Xây dựng prompt và tích hợp LLM.
3.3. Triển khai và tích hợp hệ thống lên nền tảng Zalo Bot.
3.4. Thử nghiệm và Đánh giá kết quả:
   - Các kịch bản thử nghiệm (Test cases) với các câu hỏi thực tế.
   - Đánh giá chất lượng câu trả lời (Tính chính xác, mức độ liên quan).

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
1. Các kết quả đã đạt được.
2. Những hạn chế còn tồn tại.
3. Hướng phát triển trong tương lai.

## TÀI LIỆU THAM KHẢO
