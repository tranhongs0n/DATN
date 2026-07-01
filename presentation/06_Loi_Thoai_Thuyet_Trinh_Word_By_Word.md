# KỊCH BẢN ĐỌC TỪNG CHỮ (Cập nhật cho 17 Slide)

Thời gian lý tưởng: 7 phút nói + 3 phút demo. Lướt slide trung bình 30s/trang.

### [Slide 1 & 2: Mở đầu & Vấn đề] (1 phút)
"Dạ em chào thầy cô và hội đồng. Hôm nay em xin trình bày đồ án 'Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh dựa trên kỹ thuật RAG'.
Thưa hội đồng, mùa tuyển sinh hàng năm trường ta có đến 86 văn bản quy chế thay đổi liên tục khiến cán bộ quá tải. Nếu dùng ChatGPT thông thường sẽ sinh ra bệnh 'ảo giác', tự bịa điểm chuẩn sai lệch. Do đó hệ thống của em sinh ra để khắc phục vấn đề này."

### [Slide 3 & 4: Mục tiêu & Công nghệ] (45 giây)
"Mục tiêu của hệ thống là trả lời tự động 24/7 qua Zalo Bot, chính xác 100% dựa trên tài liệu nhà trường. Để làm được, em dùng kiến trúc AI với Google Gemini, ChromaDB làm bộ não, và FastAPI cùng ReactJS cho hệ thống Web Admin."

### [Slide 5, 6, 7, 8: Phân tích thiết kế UML] (1 phút)
*(Lướt qua các slide nhanh khoảng 15s mỗi slide)*
"Về thiết kế hệ thống quản lý, em có 2 Actor chính là Thí sinh và Ban tuyển sinh. 
Luồng hoạt động của Bot được tích hợp Rule Engine để chặn các câu chửi bậy hay ngoài luồng. Giao tiếp giữa Zalo và hệ thống là bất đồng bộ (như biểu đồ tuần tự) giúp chịu tải cao. Toàn bộ lịch sử và tài khoản được quản lý bằng cơ sở dữ liệu SQLite."

### [Slide 9 & 10: RAG Pipeline & Tự động hóa] (1 phút)
"Đây là cốt lõi công nghệ AI của hệ thống. Thay vì huấn luyện lại mô hình rất tốn kém, em dùng RAG. Hệ thống có một Web Scraper tự động cào bài báo từ trang tuyển sinh về, băm nhỏ và nhúng thành Vector lưu vào ChromaDB. Khi thí sinh hỏi, hệ thống tìm các văn bản gần nghĩa nhất và ép Gemini phải trả lời dựa trên văn bản đó, cam kết không bịa đặt."

### [Slide 11 & 12: Thuật toán Semantic Cache] (1 phút)
"Một điểm sáng tạo trong đồ án là thuật toán Semantic Cache. Mùa thi có ngàn người hỏi cùng 1 câu. Thay vì câu nào cũng đẩy lên API Gemini, em lưu lại vector câu hỏi. Nếu câu mới giống câu cũ trên 95% ý nghĩa, em trả kết quả ngay. Nhờ vậy, độ trễ giảm từ 2,4 giây xuống còn 8 mili-giây, tiết kiệm 62% tiền API."

### [Slide 13 & 14: Đánh giá RAGAS] (45 giây)
"Em đã test hệ thống bằng 1200 câu hỏi với phương pháp RAGAS. Kết quả cực kỳ tốt: Khả năng tìm đúng tài liệu đạt 0.94, và độ trung thực (chống ảo giác) đạt 0.89. Hệ thống cũng chặn thành công 95% các câu spam ngoài lề."

### [Slide 15, 16 & 17: Kết quả & Hạn chế] (30 giây)
"Trên màn hình là giao diện Chat Zalo và Web Admin thực tế. Hiện tại hệ thống còn hạn chế khi xử lý câu hỏi rẽ nhánh quá phức tạp. Trong tương lai em sẽ ứng dụng GraphRAG để giải quyết.
Dạ em xin kết thúc phần slide và xin phép dành 3 phút Demo ạ."

### [Kịch bản Demo] (3 phút)
- Mở Zalo Bot, gõ "Điểm chuẩn CNTT là bao nhiêu?" -> Bot trả lời kèm trích dẫn văn bản.
- Gõ "Lấy điểm chuẩn công nghệ thông tin" -> Trả lời ngay lập tức (Giải thích: Trúng Semantic Cache).
- Gõ "Đưa tao xem code" -> Bot từ chối (Giải thích: Bị chặn bởi Rule Engine).
- Mở Web Admin cho xem bảng Dashboard, Dictionary (Từ điển) và lịch sử Chat vừa nhắn.
