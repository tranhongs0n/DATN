# Web Scraper & Chunking Data (Thu thập và Phân mảnh Dữ liệu)

## 1. Web Scraper Đa luồng (Thu thập dữ liệu tự động)
- **Định nghĩa:** Web Scraper (cào dữ liệu) là công cụ tự động hóa việc truy cập và trích xuất thông tin từ các trang web thay cho thao tác thủ công của con người. Trong dự án này, hệ thống tự động thu thập thông tin từ trang tin tuyển sinh của trường Đại học (TLU).
- **Cơ chế hoạt động trong dự án:**
  - Logic thu thập được định nghĩa tại lớp `TLUAdmissionScraper` (`codebase/src/utils/scraper.py`).
  - Thay vì bóc tách HTML cổ điển (dễ lỗi khi web đổi giao diện), hệ thống gọi trực tiếp vào các **API ẩn** của trang web (`list_api`, `detail_api`). Điều này đảm bảo dữ liệu trả về luôn ở định dạng chuẩn (JSON/Cấu trúc rõ ràng).
  - Tự động nhận diện và quét nội dung từ cả bài viết web lẫn các tệp đính kèm (Word, PDF).
- **Tối ưu hóa (Đa luồng):** Quá trình thu thập áp dụng đa luồng (multi-threading) để tải đồng thời nhiều bài viết cùng lúc, khắc phục nút thắt cổ chai về mạng (I/O Bound).
- **Giá trị thực tiễn:** Tiết kiệm đến 95% thời gian cho cán bộ quản lý dữ liệu, tự động hóa luồng cập nhật tri thức (Knowledge Base) để AI luôn có câu trả lời mới nhất.

## 2. Chunking (Kỹ thuật Phân mảnh văn bản)
- **Vấn đề (Giới hạn Context Window):** Mọi mô hình LLM (như GPT-4, Gemini) đều có giới hạn về số lượng token (từ ngữ) xử lý trong một lần đọc. Hơn nữa, việc nhồi nhét quá nhiều tài liệu vào prompt sẽ gây ra hiện tượng "Lost in the middle" (mô hình quên hoặc bỏ qua thông tin ở giữa văn bản).
- **Giải pháp - Chunking:** Là kỹ thuật chia nhỏ tài liệu gốc thành các phân đoạn (chunk) ngắn hơn để dễ dàng thực hiện Vector Embedding và tìm kiếm.
- **Cách dự án triển khai:**
  - Sử dụng module `RecursiveCharacterTextSplitter` của framework Langchain (tại `codebase/src/core/vector_db.py`).
  - **Cấu hình thuật toán:** Hệ thống sử dụng `chunk_size = 1000` và `chunk_overlap = 200`.
    - `chunk_size = 1000`: Khống chế mỗi đoạn văn không vượt quá 1000 ký tự. Thuật toán "Recursive" sẽ ưu tiên cắt ở các dấu chấm đoạn, dấu chấm câu trước, rồi mới đến khoảng trắng để giữ nguyên vẹn câu nhất có thể.
    - `chunk_overlap = 200`: (Rất quan trọng) Các đoạn cắt sẽ nối gối lên nhau (trùng lặp) 200 ký tự. Kỹ thuật này giúp giữ lại ngữ cảnh (context) ở phần giáp lai giữa hai đoạn cắt, tránh việc một khái niệm quan trọng bị chặt đứt làm đôi.

## 3. Hạn chế: Chunking Conflict (Xung đột do phân mảnh)
- Đây là một **lỗi điển hình của các hệ thống RAG cơ bản**. Dù có dùng Overlap, việc cắt văn bản cơ học theo độ dài vẫn có thể vô tình phá vỡ cấu trúc logic hoặc các điều kiện rẽ nhánh phức tạp.
- **Ví dụ thực tế:** 
  - Quy chế ghi: *"Thí sinh được xét tuyển thẳng nếu: Là học sinh trường chuyên (1) VÀ có chứng chỉ IELTS 6.5 trở lên (2)"*.
  - Do vô tình, khi cắt chunk, điều kiện (1) rơi vào Chunk A, điều kiện (2) rơi vào Chunk B.
  - Khi hỏi "Học sinh trường chuyên có được tuyển thẳng không?", ChromaDB tra cứu thấy Chunk A rất khớp (Similarity cao) nên trả về Chunk A. LLM đọc Chunk A và trả lời: "Có, bạn được tuyển thẳng", dẫn đến **sai lệch thông tin nghiêm trọng** vì thiếu điều kiện (2).
- **Hướng giải quyết (Tầm nhìn tương lai):** 
  - Thay thế hoặc kết hợp với **GraphRAG (Knowledge Graph - Đồ thị Tri thức):** Kỹ thuật này không cắt văn bản một cách mù quáng, mà dùng AI để phân tích câu thành các Thực thể (Entities) và Mối quan hệ (Relationships). Từ đó vẽ ra một mạng lưới đồ thị liên kết. Khi đó, điều kiện (1) và (2) sẽ được liên kết với nhau bằng sợi dây "VÀ", giúp mô hình không bao giờ bỏ sót ngữ cảnh.
