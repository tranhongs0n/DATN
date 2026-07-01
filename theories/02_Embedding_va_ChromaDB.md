# Vector Embedding & ChromaDB

## 1. Vector Embedding là gì?
- Là cách biến đổi văn bản (chữ viết) thành các con số (vector) trong không gian nhiều chiều. Cụ thể trong đồ án, mô hình `gemini-embedding-2` tạo ra vector có độ dài 768 chiều.
- **Mục đích:** Giúp máy tính tính toán được "ngữ nghĩa" thay vì chỉ so khớp "từ khóa" (keyword matching). Ví dụ: "Học phí" và "Tiền học" khác hẳn nhau về mặt chữ cái, nhưng vector của chúng sẽ nằm rất sát nhau trong không gian.

## 2. ChromaDB là gì?
- Là một Cơ sở dữ liệu Vector (Vector Database) mã nguồn mở, sinh ra để lưu trữ và tìm kiếm các dãy số vector này.
- **Tại sao chọn ChromaDB?** Nó chạy trực tiếp cục bộ (local) trên RAM/Ổ cứng, không gọi qua mạng Internet (như Pinecone hay Weaviate). Nhờ vậy, độ trễ truy xuất chỉ mất 14ms và hoàn toàn miễn phí.

## 3. Cosine Similarity & Dot Product (Tích vô hướng)
- Khi người dùng đặt câu hỏi, câu hỏi cũng được biến thành 1 vector.
- Hệ thống lấy vector này tính "tích vô hướng" (Dot Product) với toàn bộ vector tài liệu trong ChromaDB.
- Khoảng cách càng gần (điểm càng cao) thì đoạn văn bản đó càng mang ý nghĩa giống với câu hỏi. ChromaDB sẽ trả về Top K đoạn văn bản gần nhất.
