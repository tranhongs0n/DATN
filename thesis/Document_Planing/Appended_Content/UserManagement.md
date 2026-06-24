# Đặc tả Phân hệ Quản trị Người dùng (User Management Module)

Trong quá trình phân tích và xây dựng hệ thống, an toàn thông tin và bảo mật phân quyền là yếu tố bắt buộc đối với một hệ thống cấp trường. Do đó, đề tài đã phát triển một phân hệ quản trị tài khoản chuyên biệt dành riêng cho đội ngũ cán bộ tuyển sinh, độc lập hoàn toàn với luồng tương tác của Zalo Bot.

## 1. Cơ chế xác thực (Authentication Mechanism)
Hệ thống sử dụng cơ chế xác thực **JSON Web Token (JWT)** không trạng thái (stateless) thay vì sử dụng phiên (session) truyền thống. 
- Khi cán bộ đăng nhập thành công qua endpoint `/api/auth/login`, hệ thống khởi tạo một chuỗi mã JWT chứa mã định danh người dùng và thời gian hết hạn (Expiration Time).
- Mọi yêu cầu (request) thao tác dữ liệu từ Web Dashboard lên máy chủ FastAPI đều phải đính kèm chuỗi JWT này trong HTTP Header (`Authorization: Bearer <token>`).
- Lớp middleware `require_admin` (được định nghĩa trong `dependencies.py`) chịu trách nhiệm giải mã token và xác thực quyền hạn trước khi cho phép hàm logic thực thi.

## 2. Quản lý vòng đời tài khoản (CRUD Operations)
Phân hệ cung cấp bộ API nội bộ hoàn chỉnh (`/api/admin/users`) để quản trị viên cấp cao có thể:
1. **Khởi tạo tài khoản (`POST /api/admin/users`):** Tạo mới một cán bộ hỗ trợ tư vấn. Mật khẩu không bao giờ được lưu dưới dạng văn bản thô (plain-text) mà được băm (hash) bằng thuật toán bcrypt. Hệ thống kiểm tra chặt chẽ tính duy nhất của tên đăng nhập (Username).
2. **Cập nhật thông tin (`PUT /api/admin/users/{user_id}`):** Hỗ trợ đổi mật khẩu định kỳ để đảm bảo an ninh mạng.
3. **Xóa tài khoản (`DELETE /api/admin/users/{user_id}`):** Thu hồi quyền truy cập của cán bộ đã thuyên chuyển công tác. Hệ thống tích hợp logic ràng buộc: quản trị viên không thể tự xóa chính tài khoản đang đăng nhập của mình để tránh gây lỗi mất quyền kiểm soát toàn cục (system lock-out).
4. **Truy xuất danh sách (`GET /api/admin/users`):** Liệt kê toàn bộ nhân sự đang có quyền quản trị tri thức.

## 3. Hệ thống lưu vết thao tác (Audit Logging)
Mọi hành động nhạy cảm như thêm mới tài khoản, đổi mật khẩu hay xóa quyền truy cập đều được hệ thống tự động lưu vết qua module `logger` tích hợp sẵn.
Ví dụ: `logger.info(f"AUDIT: User {current_user['username']} created new account for {req.username}")`.
Điều này giúp minh bạch hóa trách nhiệm và dễ dàng truy vết khi có sự cố thay đổi dữ liệu không mong muốn.
