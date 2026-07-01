# FastAPI, SSE & Kiến trúc Hệ thống

## 1. FastAPI là gì?
- Là framework Python dùng làm backend API. Đặc điểm: Tốc độ cực nhanh và hỗ trợ lập trình bất đồng bộ (Asynchronous).
- **Bất đồng bộ (Async):** Rất quan trọng vì khi code đợi Google Gemini API trả lời (mất 2-3s), server không bị "đứng hình" mà vẫn có thể tiếp nhận câu hỏi của thí sinh khác.

## 2. Server-Sent Events (SSE) & Streaming
- Khác với API bình thường (đợi LLM nghĩ xong 100% rồi gửi nguyên một cục text mất 3 giây), SSE cho phép truyền dữ liệu theo dạng **suối (stream)**.
- LLM sinh ra chữ nào, FastAPI đẩy chữ đó về Zalo/Web ngay lập tức. Giúp người dùng có trải nghiệm giống hệt ChatGPT đang gõ chữ. Độ trễ cảm nhận < 1 giây.

## 3. Zalo Bot
- Chatbot sử dụng Webhook của Zalo. 
- Luồng: Người dùng nhắn tin -> Zalo gửi tín hiệu (POST request) sang FastAPI -> FastAPI xử lý RAG -> Trả về kết quả -> Gọi API của Zalo để Zalo hiển thị trên điện thoại người dùng.

## 4. SQLite vs ChromaDB
Trong hệ thống chia làm 2 loại Database:
- **ChromaDB:** Chứa Vector và Text quy chế. Dùng để tìm kiếm ngữ nghĩa.
- **SQLite (CSDL Quan hệ):** Lưu tài khoản cán bộ Admin, danh sách từ điển viết tắt, lịch sử cuộc hội thoại (để quản lý xem ai hỏi gì).
