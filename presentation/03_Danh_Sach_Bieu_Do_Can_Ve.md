# DANH SÁCH BIỂU ĐỒ UML & SƠ ĐỒ CẦN VẼ CHO SLIDE
Giảng viên đã dặn "phần phân tích thiết kế cần nêu mô hình use case, tuần tự, hoạt động quan trọng, lớp, bảng". Đây là danh sách bạn PHẢI VẼ và chèn vào Slide/Báo cáo Word:

## 1. Biểu đồ Use Case (Tổng quát)
- **Actor 1: Thí Sinh:** Tra cứu thông tin, Chat với Bot.
- **Actor 2: Admin:** Đăng nhập, Quản lý Tài khoản, Quản lý Quy chế (Tài liệu), Quản lý Từ điển, Kiểm thử Bot (Chat Tester), Cào dữ liệu (Scraper).

## 2. Biểu đồ Hoạt động (Activity Diagram)
Nên vẽ 1 luồng quan trọng nhất: **Luồng xử lý câu hỏi của Bot**
- Bắt đầu -> User gửi tin nhắn qua Zalo -> Bot nhận text -> Đưa qua bộ lọc từ viết tắt -> Đưa qua Rule Engine chặn câu hỏi ngoài lề (Nếu bị chặn -> Trả lỗi -> Kết thúc).
- Nếu hợp lệ -> Nhúng (Embed) câu hỏi thành Vector -> So sánh với Semantic Cache -> Nếu trúng Cache -> Trả kết quả cũ -> Kết thúc.
- Nếu trượt Cache -> Tìm kiếm ChromaDB -> Lấy top 5 Context -> Gửi Context + Câu hỏi lên Gemini -> Gemini tạo câu trả lời -> Lưu vào Cache -> Gửi về Zalo -> Kết thúc.

## 3. Biểu đồ Tuần tự (Sequence Diagram)
Nên vẽ 1 luồng kỹ thuật: **Luồng truy vấn RAG Streaming**
- Thí sinh --(1. Gửi tin)--> Zalo Webhook --(2. Forward)--> FastAPI.
- FastAPI --(3. Chuyển từ viết tắt)--> SQLite (Dictionary).
- FastAPI --(4. Tính Vector)--> Gemini Embedding.
- FastAPI --(5. Tìm Context)--> ChromaDB.
- FastAPI --(6. Gửi Prompt)--> Gemini LLM.
- Gemini LLM --(7. Sinh chữ dạng Stream)--> FastAPI.
- FastAPI --(8. Bắn API)--> Zalo.

## 4. Biểu đồ Cơ sở dữ liệu (ERD / Mô hình Bảng)
Vẽ quan hệ giữa các bảng trong SQLite:
- `users`: id, username, hashed_password, role, created_at
- `documents`: id, file_name, status, upload_time, doc_metadata
- `dictionaries`: id, short_word, full_word
- `chat_logs`: id, user_id (zalo_id), question, answer, latency_ms, is_cached, created_at

## 5. Sơ đồ Kiến trúc AI (RAG Architecture)
- Vẽ 2 pipeline riêng biệt: Data Pipeline (Nạp dữ liệu từ file Word -> Chunking -> VectorDB) và Chat Pipeline (User -> RAG -> Trả lời). Dùng các icon như Database, AI Chip, Robot để sơ đồ nhìn pro nhất.
