# Đặc tả Phân hệ Cào dữ liệu tự động (Automated Web Scraper)

Một trong những thách thức lớn nhất của các hệ thống RAG là việc duy trì sự cập nhật của cơ sở tri thức. Thay vì ép buộc cán bộ tuyển sinh phải tự tải về từng văn bản thông báo trên website của trường rồi upload ngược lên hệ thống, đề tài đã phát triển **Phân hệ Cào dữ liệu tự động (Web Scraper)**.

## 1. Kiến trúc luồng thu thập dữ liệu
Phân hệ này (nằm tại `admin_scrape.py` và `scraper.py`) hoạt động như một công cụ tự động hóa luồng nghiệp vụ (RPA - Robotic Process Automation). 
- Công cụ `TLUAdmissionScraper` được lập trình để quét mã nguồn HTML của Cổng thông tin tuyển sinh Đại học Thủy Lợi.
- Nó bóc tách các bài viết thông báo mới nhất theo từng danh mục (category) định sẵn (ví dụ: Tin Đại học, Tin Thạc sĩ).
- Hệ thống duy trì một tệp trạng thái để ghi nhớ mốc thời gian cào dữ liệu gần nhất (`update_last_crawl()`). Khi kích hoạt, nó sử dụng hàm `check_new()` để đối chiếu và chỉ tải về những thông báo chưa từng xuất hiện.

## 2. API Điều khiển Cào dữ liệu
Hệ thống cung cấp hai Endpoint chính để Web Dashboard giao tiếp:
1. **Kiểm tra bài viết mới (`GET /api/admin/scrape/check`):**
   - API này phản hồi lại thời điểm cào gần nhất (`last_crawl`) và đếm số lượng bài viết mới (`new_count`) trên website trường nhưng chưa có trong hệ thống RAG. 
   - Nó giúp cán bộ nắm bắt tình hình mà không cần phải chạy lại toàn bộ tiến trình quét dữ liệu nặng nề.

2. **Kích hoạt tiến trình quét (`POST /api/admin/scrape`):**
   - Cho phép truyền tham số `category` (một danh mục cụ thể hoặc `all` cho tất cả) và `limit` (giới hạn số trang cần quét).
   - Tiến trình sẽ tải dữ liệu văn bản và các tệp đính kèm (PDF, DOCX) nằm trong bài viết đó, tự động chuyển chúng sang luồng tiền xử lý để nhúng vào ChromaDB.

## 3. Lợi ích hệ thống
Tính năng này tự động hóa 90% khối lượng công việc cập nhật tri thức của phòng đào tạo. Nó biến hệ thống RAG từ một kho dữ liệu tĩnh trở thành một trợ lý sống động, đồng bộ trực tiếp với những biến động mới nhất về quy chế hay điểm chuẩn của nhà trường ngay khi được công bố trên trang chủ.
