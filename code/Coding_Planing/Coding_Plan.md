# Kế Hoạch Lập Trình (Coding Plan)

Dựa trên cấu trúc đồ án và kiến trúc hệ thống đã chốt, quá trình lập trình được chia thành 6 giai đoạn (Phases) nhằm đảm bảo tiến độ, dễ dàng kiểm thử và tích hợp liên tục.

## Giai đoạn 1: Khởi tạo dự án & Môi trường (Project Initialization)
**Mục tiêu:** Thiết lập bộ khung chuẩn cho toàn bộ hệ thống backend.
- Thiết lập cấu trúc thư mục dự án chuẩn (theo pattern `src/`, `tests/`, `configs/`).
- Khởi tạo môi trường ảo (venv) và quản lý thư viện bằng `pyproject.toml` (hoặc `requirements.txt`).
- Cấu hình các biến môi trường (`.env`) và file `config.yaml` cho toàn bộ hệ thống (Gemini API keys, Zalo token, đường dẫn database).
- Xây dựng module quản lý log (Logger) để theo dõi luồng dữ liệu.

## Giai đoạn 2: Module Thu Thập & Tiền Xử Lý Dữ Liệu (Data Ingestion)
**Mục tiêu:** Xử lý và làm sạch dữ liệu đầu vào đa dạng.
- **Web Scraper (`TLUAdmissionScraper`):** Viết script thu thập dữ liệu từ website tuyển sinh của trường sử dụng `BeautifulSoup4`.
- **Document Loaders:** Tích hợp `PyPDFLoader` và `Docx2txtLoader` để quét và đọc các tệp PDF, DOCX hiện có.
- **Multimodal File Converter:** Cài đặt luồng gửi tệp ảnh/PDF scan qua Gemini Vision API để trích xuất nội dung thành định dạng Markdown/DOCX, bảo toàn cấu trúc bảng biểu.
- Viết các hàm làm sạch văn bản (Text Cleaner) và chia mảnh văn bản (Chunking) với `RecursiveCharacterTextSplitter`.

## Giai đoạn 3: Lõi RAG & Cơ sở dữ liệu Vector (VectorDB & RAG Core)
**Mục tiêu:** Xây dựng bộ não truy xuất thông tin của hệ thống.
- **Embedding Wrapper (`GeminiEmbeddings`):** Tích hợp mô hình `gemini-embedding-2` của Google vào LangChain.
- **ChromaDB Manager:** Xây dựng lớp quản lý cơ sở dữ liệu ChromaDB cục bộ (Khởi tạo, Thêm chunk, Xóa, Cập nhật).
- **Indexing Service:** Viết luồng tự động nhúng vector các mảnh văn bản và lưu vào ChromaDB (hỗ trợ xử lý batch để tránh rate limit).
- **Retriever & Prompt Engineering:** Thiết lập cơ chế truy xuất (Retrieval) và xây dựng cấu trúc Prompt Template chống ảo giác.
- Cài đặt cơ chế Streaming (trả lời theo từng ký tự) với `MultimodalEngine`.

## Giai đoạn 4: API Backend (FastAPI) & Tích Hợp Zalo
**Mục tiêu:** Mở cổng giao tiếp cho hệ thống ra bên ngoài.
- Khởi tạo app FastAPI, cấu hình CORS Middleware.
- Xây dựng các API Endpoints cho Web Admin (Tải file, Xóa file, Kích hoạt Scraper, Cập nhật VectorDB).
- Thiết lập API `/chat` hỗ trợ Server-Sent Events (SSE) để stream câu trả lời.
- Cài đặt Zalo Webhook Endpoint để nhận tin nhắn từ Zalo Bot, tiền xử lý tin nhắn, đưa vào luồng RAG và gửi phản hồi (Quick Reply) về lại Zalo.

## Giai đoạn 5: Giao diện Web Admin (Presentation Layer)
**Mục tiêu:** Cung cấp công cụ quản trị dữ liệu trực quan.
- Dựng giao diện HTML/CSS/JS (Vanilla hoặc Jinja2 Templates) tích hợp sẵn trong FastAPI.
- Tích hợp các tính năng trực quan: 
  - Kéo thả upload file tài liệu.
  - Theo dõi tiến trình (progress bar) khi Indexing và Embedding.
  - Bảng điều khiển thống kê (số lượng tài liệu, dung lượng DB).

## Giai đoạn 6: Kiểm Thử & Tối Ưu (Testing & Refinement)
**Mục tiêu:** Đánh giá độ chính xác và đảm bảo hệ thống vận hành ổn định.
- Triển khai bộ câu hỏi kiểm thử theo 5 nhóm (đã định nghĩa trong báo cáo).
- Xử lý các Edge Cases: 
  - Đầu vào không liên quan (chặn bằng System Prompt).
  - Rate limit của Gemini API (thiết lập cơ chế Retry).
- Tối ưu Metadata Filtering cho cơ sở dữ liệu Vector.
- Dọn dẹp mã nguồn và viết file `README.md` hướng dẫn triển khai.

---
**Trạng thái hiện tại:** Sẵn sàng bắt đầu Giai đoạn 1.
