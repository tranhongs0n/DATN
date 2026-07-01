# Web Scraper & Chunking Data

## 1. Web Scraper Đa Luồng
- **Web Scraper:** Là đoạn mã tự động truy cập vào trang tuyển sinh của TLU, trích xuất text từ các bài báo hoặc tự tải file Word/PDF đính kèm.
- **Đa luồng (Multi-threading):** Tải nhiều bài cùng một lúc giúp tăng tốc.
- **Giá trị:** Tiết kiệm 95% thời gian cho cán bộ tuyển sinh so với việc copy-paste thủ công.

## 2. Chunking (Chia nhỏ văn bản)
- Mô hình LLM có giới hạn gọi là "Context Window" (số lượng từ tối đa đọc trong 1 lần). Không thể đẩy nguyên cuốn tài liệu 100 trang cho LLM.
- **Giải pháp:** Cắt nhỏ tài liệu ra. Trong LangChain, dùng `RecursiveCharacterTextSplitter` cắt tài liệu thành các đoạn dài cỡ 1000 ký tự.

## 3. Hạn chế: Chunking Conflict (Phân mảnh ngữ cảnh)
- Đây là một **lỗi điển hình của RAG**. Khi cắt nhỏ, một điều kiện tuyển sinh rẽ nhánh có thể bị cắt làm đôi nằm ở 2 đoạn (chunk) khác nhau.
- Ví dụ: Chunk 1: "Điều kiện tuyển thẳng: Học sinh trường chuyên". Chunk 2: "VÀ có IELTS 6.5". Khi tìm kiếm, DB chỉ trả về Chunk 1. LLM trả lời thiếu điều kiện IELTS.
- **Hướng giải quyết (nêu trong tương lai):** Dùng GraphRAG (Mạng tri thức) để lưu các điều kiện dưới dạng đồ thị có liên kết với nhau thay vì cắt mù quáng.
