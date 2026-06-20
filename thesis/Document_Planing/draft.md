4.3.2. Phân tích nguyên nhân thất bại

Hệ thống ghi nhận một số kịch bản truy vấn trả về kết quả chưa chính xác. Khuyết điểm đầu tiên nằm ở hiện tượng xung đột dữ liệu lịch sử. Khi thí sinh yêu cầu cung cấp điểm chuẩn ngành Công nghệ thông tin, hệ thống RAG truy xuất và trộn lẫn thông tin đề án tuyển sinh của cả năm 2023 lẫn năm 2024. Mô hình ngôn ngữ lớn thiếu manh mối để ưu tiên dữ liệu mới nhất. Lỗi này xuất phát từ việc kỹ thuật tìm kiếm vector hiện tại chỉ tính toán độ tương đồng ngữ nghĩa. Cơ sở dữ liệu ChromaDB cần được nâng cấp thêm bộ lọc siêu dữ liệu nhằm giới hạn phạm vi tìm kiếm theo mốc năm học.

Trường hợp thất bại tiếp theo liên quan đến các câu hỏi ghép đa điều kiện. Thí sinh đưa ra yêu cầu tìm kiếm ngành học tại cơ sở Hà Nội, sở hữu điểm chuẩn dưới 23 và có mức học phí dưới 15 triệu đồng. Thuật toán cắt mảnh văn bản phá vỡ cấu trúc bảng biểu nguyên thủy. Mối liên hệ logic giữa tên ngành, tổ hợp thi và học phí bị đứt gãy. Kết quả truy xuất trả về các mảnh thông tin rời rạc, khiến LLM không thể tổng hợp thành câu trả lời đáp ứng đủ ba điều kiện. Điểm yếu này chứng minh giải pháp RAG thuần túy gặp giới hạn lớn khi phải xử lý các lệnh tìm kiếm mang tính chất quan hệ.

Hướng phát triển trong tương lai

Kiến trúc hệ thống đa tác tử đóng vai trò nâng cấp trọng tâm trong phiên bản tiếp theo. Luồng xử lý đơn tuyến hiện tại sẽ được phân tách thành các luồng chuyên biệt. Tác tử định tuyến sẽ đánh giá câu hỏi đầu vào để phân phối tác vụ. Tác tử truy xuất đảm nhận việc tương tác với ChromaDB. Tác tử tư vấn chuyên phân tích hồ sơ thí sinh. Mô hình phân tán này giảm tải cho một lượt gọi LLM duy nhất và tăng độ chính xác phản hồi.

Việc tích hợp đồ thị tri thức sẽ khắc phục nhược điểm mất thông tin cấu trúc của kỹ thuật RAG truyền thống. Bản đồ liên kết cứng giữa mã ngành, tổ hợp xét tuyển và mức học phí giúp hệ thống đối chiếu chéo các thông tin tuyển sinh. Cơ chế tìm kiếm kết hợp giữa vector và đồ thị tri thức đảm bảo khả năng xử lý các câu hỏi phức tạp.

Hệ thống cần bổ sung các lớp màng lọc bảo mật dữ liệu ở khâu tiền xử lý. Chatbot công khai trên mạng xã hội dễ đối mặt với các lệnh tấn công chèn câu lệnh độc hại. Việc cài đặt các rào chắn kiểm duyệt sẽ ngăn chặn người dùng lợi dụng API của nhà trường để giải toán, dịch thuật hoặc tạo nội dung sai mục đích.

Bộ nhớ dài hạn theo định danh thí sinh là chìa khóa để tiến tới tư vấn cá nhân hóa. Chatbot sẽ lưu trữ toàn bộ chuỗi hội thoại xuyên suốt các phiên làm việc. Hệ thống tự động ghi nhớ khối thi, mức điểm và sở thích của từng học sinh. Chức năng này chuyển dịch hệ thống từ trạng thái bị động cung cấp thông tin sang chủ động gợi ý lộ trình xét tuyển tối ưu.
