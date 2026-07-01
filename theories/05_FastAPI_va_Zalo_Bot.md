# FastAPI, SSE & Zalo Bot (Kiến trúc Hệ thống Backend)

## 1. FastAPI và Lập trình Bất đồng bộ (Asynchronous)
- **Định nghĩa:** FastAPI là một web framework hiện đại, hiệu năng cao dùng để xây dựng API bằng Python.
- **Lý thuyết Bất đồng bộ (Async/Await):** 
  - Trong kiến trúc phần mềm truyền thống (Synchronous/WSGI), khi server nhận 1 request và gọi API của LLM (thường mất 2-3 giây chờ phản hồi), luồng (thread) xử lý đó sẽ bị "đóng băng" (block) hoàn toàn. Nếu có nhiều người hỏi cùng lúc, server có thể quá tải vì cạn kiệt thread.
  - FastAPI giải quyết vấn đề này bằng mô hình **Bất đồng bộ (ASGI - Asynchronous Server Gateway Interface)** qua cơ chế Event Loop. Khi request đang chờ Gemini trả lời, Event Loop sẽ tạm gác nó qua một bên để dùng thread đó đi phục vụ các request khác. Khi có kết quả từ Gemini, nó mới quay lại xử lý tiếp. Điều này giúp server xử lý hàng ngàn request đồng thời với tài nguyên CPU/RAM cực thấp.

## 2. Server-Sent Events (SSE) & Streaming Response
- **Vấn đề của HTTP truyền thống:** HTTP request-response bình thường đòi hỏi server phải tính toán xong 100% dữ liệu rồi mới trả về một lần. Với AI sinh văn bản, người dùng sẽ phải nhìn màn hình chờ (loading) trắng trơn trong nhiều giây, gây trải nghiệm rất tệ.
- **Giải pháp bằng SSE:** SSE là công nghệ đẩy dữ liệu một chiều từ Server về Client theo thời gian thực (Real-time). Dữ liệu được truyền qua HTTP với header `Transfer-Encoding: chunked` và `Content-Type: text/event-stream`.
- **Cách dự án triển khai (`codebase/src/app/routers/chat.py`):** 
  - Sử dụng class `StreamingResponse` của FastAPI. 
  - AI sinh ra đến chữ nào (`yield`), FastAPI lập tức đẩy luồng byte đó về trình duyệt. Nhờ vậy, người dùng trên nền tảng Web có trải nghiệm chữ hiện ra từng từ giống hệt ChatGPT, giảm **độ trễ cảm nhận (Perceived Latency)** xuống dưới 1 giây.

## 3. Zalo Bot Webhook (Tích hợp nền tảng Chat)
- Khác với giao diện Web chủ động gọi API, Zalo Bot hoạt động dựa trên cơ chế **Event-driven (Hướng sự kiện)** thông qua Webhook.
- **Luồng xử lý lý thuyết (`codebase/src/app/routers/zalo_bot.py`):**
  1. Người dùng nhắn tin vào Zalo OA (Zalo Bot).
  2. Máy chủ Zalo đóng gói tin nhắn thành một HTTP POST request và tự động bắn vào API Webhook của dự án (`/zalo/bot/webhook`).
  3. **Bảo mật:** FastAPI sẽ kiểm tra header `X-Bot-Api-Secret-Token` để xác thực request thực sự đến từ Zalo, chống lại các cuộc tấn công giả mạo (Spoofing).
  4. Hệ thống chạy RAG để tạo câu trả lời.
  5. Gọi ngược lại REST API của Zalo (`bot-api.zaloplatforms.com`) kèm Token xác thực để đẩy tin nhắn hiển thị lên điện thoại người dùng.
# FastAPI, SSE & Zalo Bot (Kiến trúc Hệ thống Backend)

## 1. FastAPI và Lập trình Bất đồng bộ (Asynchronous)
- **Định nghĩa:** FastAPI là một web framework hiện đại, hiệu năng cao dùng để xây dựng API bằng Python.
- **Lý thuyết Bất đồng bộ (Async/Await):** 
  - Trong kiến trúc phần mềm truyền thống (Synchronous/WSGI), khi server nhận 1 request và gọi API của LLM (thường mất 2-3 giây chờ phản hồi), luồng (thread) xử lý đó sẽ bị "đóng băng" (block) hoàn toàn. Nếu có nhiều người hỏi cùng lúc, server có thể quá tải vì cạn kiệt thread.
  - FastAPI giải quyết vấn đề này bằng mô hình **Bất đồng bộ (ASGI - Asynchronous Server Gateway Interface)** qua cơ chế Event Loop. Khi request đang chờ Gemini trả lời, Event Loop sẽ tạm gác nó qua một bên để dùng thread đó đi phục vụ các request khác. Khi có kết quả từ Gemini, nó mới quay lại xử lý tiếp. Điều này giúp server xử lý hàng ngàn request đồng thời với tài nguyên CPU/RAM cực thấp.

## 2. Server-Sent Events (SSE) & Streaming Response
- **Vấn đề của HTTP truyền thống:** HTTP request-response bình thường đòi hỏi server phải tính toán xong 100% dữ liệu rồi mới trả về một lần. Với AI sinh văn bản, người dùng sẽ phải nhìn màn hình chờ (loading) trắng trơn trong nhiều giây, gây trải nghiệm rất tệ.
- **Giải pháp bằng SSE:** SSE là công nghệ đẩy dữ liệu một chiều từ Server về Client theo thời gian thực (Real-time). Dữ liệu được truyền qua HTTP với header `Transfer-Encoding: chunked` và `Content-Type: text/event-stream`.
- **Cách dự án triển khai (`codebase/src/app/routers/chat.py`):** 
  - Sử dụng class `StreamingResponse` của FastAPI. 
  - AI sinh ra đến chữ nào (`yield`), FastAPI lập tức đẩy luồng byte đó về trình duyệt. Nhờ vậy, người dùng trên nền tảng Web có trải nghiệm chữ hiện ra từng từ giống hệt ChatGPT, giảm **độ trễ cảm nhận (Perceived Latency)** xuống dưới 1 giây.

## 3. Zalo Bot Webhook (Tích hợp nền tảng Chat)
- Khác với giao diện Web chủ động gọi API, Zalo Bot hoạt động dựa trên cơ chế **Event-driven (Hướng sự kiện)** thông qua Webhook.
- **Luồng xử lý lý thuyết (`codebase/src/app/routers/zalo_bot.py`):**
  1. Người dùng nhắn tin vào Zalo OA (Zalo Bot).
  2. Máy chủ Zalo đóng gói tin nhắn thành một HTTP POST request và tự động bắn vào API Webhook của dự án (`/zalo/bot/webhook`).
  3. **Bảo mật:** FastAPI sẽ kiểm tra header `X-Bot-Api-Secret-Token` để xác thực request thực sự đến từ Zalo, chống lại các cuộc tấn công giả mạo (Spoofing).
  4. Hệ thống chạy RAG để tạo câu trả lời.
  5. Gọi ngược lại REST API của Zalo (`bot-api.zaloplatforms.com`) kèm Token xác thực để đẩy tin nhắn hiển thị lên điện thoại người dùng.
- **Tối ưu hóa UI cho Zalo (`chat_service.py`):** Do ứng dụng Zalo không hỗ trợ render định dạng Markdown chuẩn. Hệ thống tự động nhận diện nền tảng (`is_zalo=True`) và tiêm thêm một lệnh ngầm vào Prompt (System Prompt) cấm AI sinh ra các ký tự Markdown (như in đậm `**`, bảng biểu) để văn bản hiển thị gọn gàng, thân thiện trên màn hình điện thoại.

## 4. Kiến trúc Đa cơ sở dữ liệu (Polyglot Persistence)
Hệ thống áp dụng triết lý phân chia CSDL theo đúng chức năng tối ưu của chúng:
- **ChromaDB (Vector Database):** Chuyên dụng để lưu trữ Embedding (Vector 768 chiều) và thực hiện tính toán khoảng cách không gian (Cosine Similarity). Không phù hợp để lưu dữ liệu có cấu trúc.
- **SQLite (Relational Database):** Triển khai tại `codebase/src/core/chat_db.py`. Dùng để lưu trữ dữ liệu có cấu trúc quan hệ chặt chẽ.

## 5. Cơ chế Quản lý Lịch sử Hội thoại (Memory & Session Management)
Để chatbot AI không bị "mất trí nhớ" sau mỗi câu hỏi, hệ thống triển khai cơ chế quản lý lịch sử tinh vi cho cả 2 nền tảng:

### A. Quản lý bộ nhớ cốt lõi (LangChain Memory)
- Tại tầng xử lý logic (`core/chat_service.py`), hệ thống sử dụng module `ConversationBufferMemory` của thư viện LangChain.
- Khi nhận được danh sách lịch sử, module này tự động phân loại tin nhắn của sinh viên (`user`) và bot (`assistant`), sau đó nối lại thành một khối văn bản tổng hợp.
- Khối văn bản này được "tiêm" (inject) trực tiếp vào Prompt gửi cho Gemini. Nhờ vậy, AI có đủ **Ngữ cảnh (Context)** để hiểu các câu hỏi tiếp nối đại từ (Ví dụ: "Học phí của **ngành đó** là bao nhiêu?").

### B. Cơ chế lưu trữ theo Nền tảng
- **Trên Web UI (`app/routers/chat.py`):** Lịch sử hội thoại được lưu trữ trực tiếp dưới Local Storage của trình duyệt. Mỗi khi chat, trình duyệt chủ động gửi kèm mảng `history` lên API. Nhờ vậy, server không cần lưu trạng thái (Stateless).
- **Trên Zalo Bot (`core/chat_db.py`):** Zalo Webhook không gửi kèm tin nhắn cũ. Do đó, backend phải tự duy trì bộ nhớ bằng SQLite:
  - **Quản lý Phiên (Session TTL):** Mỗi người dùng (`zalo_user_id`) được cấp một `session_id` có thời hạn 24 giờ (86400 giây).
  - **Khôi phục trí nhớ:** Nếu sinh viên tiếp tục chat trong vòng 24h, code sẽ Query SQLite để lấy các đoạn chat cũ nạp vào LangChain Memory. Nếu quá 24h, hệ thống tự động sinh `session_id` mới và reset trí nhớ, tránh việc bot bị loạn ngữ cảnh cũ.
- **Tính năng Xuất Báo Cáo:** Lịch sử chat không hiển thị trực tiếp thành giao diện trên Web Admin để tránh giật lag. Thay vào đó, nó được cung cấp qua API `GET /api/admin/data/export/chats`. Cán bộ có thể tải file `chats.csv` (Excel) để tra cứu mọi câu hỏi và phân tích đánh giá (Rating) từ thí sinh.

## 6. Danh sách các API Endpoint trong dự án
Hệ thống Backend cung cấp một loạt các API phân chia theo từng chức năng quản lý. Nếu chạy dự án ở local, bạn có thể xem toàn bộ tài liệu Swagger UI tự động tại `http://localhost:8000/docs`.

Dưới đây là sơ đồ tổng thể các luồng API:

### 💬 Nhóm Chat & Tương tác (Client/Zalo)
- `POST /api/chat`: Nhận tin nhắn từ giao diện Web và trả về luồng stream (SSE) câu trả lời của AI.
- `POST /api/chat/feedback`: Lưu đánh giá (rating hài lòng/không hài lòng) của người dùng cho từng câu trả lời.
- `POST /zalo/bot/webhook`: Cổng Webhook đón dữ liệu tự động đẩy về từ nền tảng Zalo OA.

### 🔐 Nhóm Xác thực (Authentication)
- `POST /api/auth/login`: Xác thực tài khoản Admin và cấp phiên làm việc (Token).
- `POST /api/auth/logout`: Hủy phiên đăng nhập.
- `GET /api/auth/me`: Kiểm tra thông tin tài khoản đang đăng nhập.

### 👥 Nhóm Quản trị Tài khoản (Admin Users)
- `GET /api/admin/users`: Lấy danh sách toàn bộ cán bộ quản trị viên.
- `POST /api/admin/users`: Thêm tài khoản quản trị mới.
- `PUT /api/admin/users/{user_id}`: Cập nhật thông tin/đổi mật khẩu.
- `DELETE /api/admin/users/{user_id}`: Xóa quyền truy cập của một quản trị viên.

### 🗄️ Nhóm Quản trị Tri thức & RAG (Admin Data)
Đây là nhóm API phức tạp nhất, dùng để vận hành hệ thống RAG:
- **Quản lý Tài liệu (Files):**
  - `GET /api/admin/data/files`: Lấy danh sách tất cả các tài liệu đã nạp vào hệ thống.
  - `GET /api/admin/data/files/unsupported`: Lọc các file bị lỗi định dạng.
  - `DELETE /api/admin/data/files/{filename}`: Xóa tài liệu khỏi bộ nhớ.
  - `POST /api/admin/data/files/convert`: Đổi đuôi/định dạng các file không tương thích.
- **Quản trị VectorDB (ChromaDB Indexing):**
  - `POST /api/admin/data/index/upload`: Tải file mới lên và băm nhỏ (chunking) rồi nhúng (embedding) ngay vào DB.
  - `POST /api/admin/data/index/rebuild`: Quét lại toàn bộ thư mục và nhúng lại từ đầu.
  - `GET /api/admin/data/test_retrieval`: Hàm dùng để test riêng thuật toán Vector Search (xem nó móc tài liệu có chuẩn không) mà không bị mất tiền gọi API của AI.
- **Thống kê & Báo cáo Xuất khẩu:**
  - `GET /api/admin/data/stats`: Cung cấp số liệu tổng quan (Dashboard) cho Admin.
  - `GET /api/admin/data/export/chats`: Tải lịch sử hỏi đáp của sinh viên ra file CSV.
  - `GET /api/admin/data/export/documents`: Tải danh sách tài liệu ra file CSV.
  - `GET /api/admin/data/api/logs`: Xem lịch sử log hoạt động của hệ thống.
- **Quản lý Từ điển Viết tắt (Abbreviations):**
  - Bao gồm các API CRUD cơ bản (`GET`, `POST`, `PUT`, `DELETE`) và `POST /import` để quản lý bộ chuyển đổi từ lóng của sinh viên (Ví dụ: tự động dịch chữ "cntt" thành "Công nghệ thông tin" trước khi mang đi tìm kiếm).

### 🕷️ Nhóm Thu thập Dữ liệu (Web Scraper)
- `GET /api/admin/scrape/check`: Dò tìm xem trên web tuyển sinh của trường có bài viết nào mới không.
- `POST /api/admin/scrape`: Kích hoạt bot cào dữ liệu ngay lập tức.
