# Bản đồ Đối chiếu Chức năng (Function Mapping)

Tài liệu này ánh xạ các chức năng thực tế trong mã nguồn (Codebase) với các mục tương ứng trong Đề cương Đồ án (Thesis Outline), được phân chia theo từng nhóm người dùng.

## 1. Người Dùng Cuối (Thí sinh / Phụ huynh)

| Function (Chức năng) | Codebase (Vị trí mã nguồn) | Thesis (Mục trong Đề cương) |
| --- | --- | --- |
| **Nhắn tin hỏi đáp qua Zalo OA** | `src/utils/zalo_api.py`, `api.py` | 3.5.3. Tích hợp Zalo Bot |
| **Nhận phản hồi tự động từ hệ thống RAG** | `src/core/chat_service.py`, `multimodal.py` | 3.4.2. chat_response (Luồng RAG hoàn chỉnh) |
| **Đánh giá câu trả lời (👍/👎)** | `src/core/chat_db.py`, `api.py` | *Cần bổ sung vào Đề cương* |

## 2. Quản Trị Viên (Admin User)

| Function (Chức năng) | Codebase (Vị trí mã nguồn) | Thesis (Mục trong Đề cương) |
| --- | --- | --- |
| **Đăng nhập / Đăng xuất hệ thống** | `src/core/auth.py`, `api.py` | *Cần bổ sung vào 3.6* |
| **Quản lý tài khoản Quản trị (CRUD Admin Users)** | `src/core/auth.py`, `api.py`, `main.js` | *Cần bổ sung vào 3.6* |
| **Test Chat (Trực tiếp trên Dashboard)** | `src/app/static/index.html`, `js/main.js` | 3.6. Triển khai giao diện Web Admin |
| **Xem thống kê cơ sở dữ liệu (Stats)** | `src/core/vector_db.py`, `api.py` | 3.3.2. VectorDBManager (thống kê) |
| **Rebuild toàn bộ Vector Database** | `src/core/indexing.py`, `api.py` | 3.3.3. IndexingService |
| **Tải lên tài liệu thủ công (Upload File)** | `src/app/api.py`, `index.html` | 3.3.3. IndexingService |
| **Cào dữ liệu (Scrape TLU Portal) theo số lượng** | `src/utils/scraper.py`, `api.py` | 3.2.1. Web Scraper (TLUAdmissionScraper) |
| **Xem danh sách tài liệu đã Index** | `src/core/vector_db.py`, `api.py` | 3.3.3. IndexingService |
| **Phát hiện tệp lỗi / không hỗ trợ** | `src/utils/document_loader.py`, `api.py` | 3.2.2. Document Loader |
| **Chuyển đổi tệp đa phương thức AI (Đơn/Hàng loạt)** | `src/utils/multimodal_converter.py`, `api.py` | 3.2.3. Multimodal File Converter |
| **Xem danh sách & Lịch sử Zalo Chat** | `src/core/chat_db.py`, `api.py`, `main.js` | *Cần bổ sung vào 3.6* |
| **Gửi phản hồi thủ công qua Zalo** | `src/core/chat_db.py`, `api.py`, `zalo_api.py` | *Cần bổ sung vào 3.6* |
| **Chặn/Bỏ chặn người dùng Zalo (Block User)** | `src/core/chat_db.py`, `api.py`, `main.js` | *Cần bổ sung vào 3.6* |
| **Xuất dữ liệu Chat & Tài liệu (CSV Export)** | `api.py` | *Cần bổ sung vào 3.6* |

## 3. Hệ Thống Cốt Lõi (Core Backend Tasks)

| Function (Chức năng) | Codebase (Vị trí mã nguồn) | Thesis (Mục trong Đề cương) |
| --- | --- | --- |
| **Đọc tệp PDF / DOCX (Document Parsing)** | `src/utils/document_loader.py` | 3.2.2. Document Loader |
| **Chia nhỏ văn bản (Text Chunking)** | `src/utils/text_processor.py` | 3.3.2. VectorDBManager (chunking) |
| **Tính toán Embedding & Batching** | `src/core/vector_db.py` | 3.3.1. GeminiEmbeddings |
| **Công cụ Tìm kiếm Lai (Hybrid Search - BM25 & Chroma)** | `src/core/vector_db.py`, `chat_service.py` | *Cần bổ sung vào Đề cương (Nâng cao)* |
| **Bộ nhớ đệm Ngữ nghĩa (Semantic Query Caching)** | `src/core/semantic_cache.py`, `chat_service.py` | *Cần bổ sung vào Đề cương (Nâng cao)* |
| **Bảo vệ Hệ thống (Rate Limiting & Audit Logging)** | `api.py`, `logger_setup.py` | *Cần bổ sung vào bảo mật* |
| **Làm mới Zalo Access Token tự động** | `src/utils/zalo_token_refresh.py` | *Cần bổ sung vào 3.5.3* |
| **Kiểm tra trạng thái hệ thống (Health Check)** | `api.py` | *Cần bổ sung vào 3.6* |
| **Đánh giá tự động (Ragas Framework)** | `tests/evaluate.py`, `tests/*.json` | 4.1. Thiết kế phương pháp đánh giá |
| **Quản trị qua dòng lệnh (CLI)** | `main.py` | 3.1. Thiết lập môi trường phát triển |
