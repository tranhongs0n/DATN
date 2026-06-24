# Đặc tả Phân hệ Quản trị Tri thức và Dữ liệu Vector (Data Management)

Luồng nghiệp vụ xử lý dữ liệu của đề tài không dừng lại ở việc thiết lập một Vector Database (ChromaDB), mà còn bao hàm toàn bộ quy trình kiểm soát tình trạng tệp gốc thông qua phân hệ `admin_data.py`.

## 1. Bảng điều khiển Thống kê trực quan (Stats Dashboard)
Để cán bộ quản trị nắm bắt "độ lớn" của bộ não AI, endpoint `/api/admin/stats` cung cấp cái nhìn toàn cảnh:
- Tổng số lượng tài liệu vật lý đã tải lên (`doc_count`).
- Tổng số mảnh văn bản (Chunks) đã được phân rã thành công (`chunk_count`).
- Thông tin về mô hình ngôn ngữ đang cấu hình (Gemini LLM) và không gian nhúng (Embedding Model).

## 2. Quản lý trạng thái vòng đời tài liệu (Document Lifecycle)
Hệ thống lưu giữ cả tệp thô (FS - File System) và biểu diễn vector (ChromaDB) của tệp đó. API `/api/admin/files` trả về danh sách tất cả các tệp đang lưu trữ kèm theo trạng thái:
- **Đã nhúng thành công:** Dữ liệu đã sẵn sàng cho Zalo Bot truy xuất.
- **Lỗi xử lý:** Tệp bị lỗi định dạng hoặc lỗi quá trình trích xuất văn bản (OCR failed).
- Hệ thống hỗ trợ xử lý luồng lỗi bằng API `/files/unsupported` chuyên dò tìm các tệp không nằm trong danh sách định dạng chuẩn (PDF, DOCX), giúp dọn dẹp không gian lưu trữ rác.

## 3. Cơ chế Xóa và Ghi đè thông minh (Smart Deletion & Overwriting)
Trong bối cảnh văn bản hành chính, một quy chế của năm 2024 có thể sẽ thay thế hoàn toàn bản quy chế năm 2023. Nếu cả hai văn bản cùng tồn tại trong Vector DB, LLM sẽ gặp tình trạng "xung đột tri thức" (knowledge conflict).
API `/api/admin/files/{filename}` giải quyết triệt để bài toán này thông qua luồng xóa đồng bộ:
1. Nhận lệnh xóa từ giao diện Web.
2. Xóa tệp vật lý tương ứng trên ổ cứng (`os.remove()`).
3. Thực thi câu lệnh truy vấn nội bộ xóa toàn bộ các Vector (Points) có Metadata chứa thuộc tính `source` trỏ tới tệp đó (`db.delete(where={"source": file_path})`).

Cơ chế xóa triệt để này giúp kho tri thức luôn trong trạng thái tinh gọn, sạch sẽ và đảm bảo người dùng cuối nhận được thông tin phản hồi từ phiên bản văn bản quy phạm pháp luật mới nhất.
