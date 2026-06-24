# CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ

## 4.1. Thiết kế phương pháp đánh giá

Quy trình đánh giá được thiết lập nhằm lượng hóa toàn diện hai khía cạnh của hệ thống bao gồm chất lượng sinh văn bản và hiệu năng máy chủ. Đề tài sử dụng tập dữ liệu chuẩn chứa 1200 cặp câu hỏi và câu trả lời được gán nhãn bán tự động từ 86 văn bản gốc.

### 4.1.1. Phân loại tập dữ liệu kiểm thử
Ma trận kiểm thử bao gồm năm nhóm tình huống chính. Nhóm đầu tiên là tra cứu trực diện mã ngành, chỉ tiêu và điểm chuẩn. Nhóm thứ hai tập trung vào các truy vấn sử dụng từ viết tắt hoặc ngôn ngữ tự do trên mạng xã hội. Nhóm thứ ba kiểm tra các điều kiện chéo phức hợp với nhiều biến số đầu vào. Nhóm thứ tư đánh giá khả năng phản hồi đối với các câu hỏi nằm ngoài phạm vi tuyển sinh. Nhóm cuối cùng yêu cầu truy xuất thông tin trải dài trên đa bậc đào tạo.

### 4.1.2. Tiêu chí đánh giá chất lượng sinh
Hệ thống đánh giá chất lượng sinh văn bản dựa trên bốn tiêu chí cốt lõi (Es và cộng sự, 2023). Bốn tiêu chí này bao gồm Context Precision, Context Recall, độ trung thực để chống Hallucination, và cuối cùng là Answer Relevancy.

### 4.1.3. Kịch bản kiểm thử hiệu năng tối ưu hóa
Bên cạnh bài kiểm tra truy xuất tiêu chuẩn, hệ thống được thử nghiệm chịu tải thông qua hai bài kiểm thử chuyên biệt nhằm đánh giá các cơ chế tối ưu mới được tích hợp. Bài kiểm thử Semantic Cache tiến hành gửi 500 truy vấn lặp lại hoặc có biến thể ngữ nghĩa nhẹ để đo lường tỷ lệ trúng đệm và sự chênh lệch độ trễ. Bài kiểm thử chống quá tải thực hiện gửi dồn dập 2000 luồng truy vấn đồng thời qua cổng kết nối dịch vụ AI để cố tình gây tràn hạn mức, qua đó quan sát khả năng chống sập của hệ thống.

## 4.2. Kết quả thử nghiệm

### 4.2.1. Đánh giá độ chính xác
Kết quả trích xuất sau khi chạy kiểm thử trên toàn bộ 1200 câu hỏi:

| Nhóm câu hỏi | Context Precision | Context Recall | Faithfulness | Answer Relevancy |
|--------------|--------------|-----------------|---------------|--------------|
| Nhóm 1: Tra cứu đơn lẻ | 0.94 | 0.98 | 0.96 | 0.95 |
| Nhóm 2: Từ lóng viết tắt | 0.90 | 0.92 | 0.89 | 0.91 |
| Nhóm 3: Logic phức hợp | 0.88 | 0.85 | 0.91 | 0.88 |
| Nhóm 4: Ngoài phạm vi | Không có | Không có | Không có | 0.95 |
| Nhóm 5: Đa bậc đào tạo | 0.86 | 0.82 | 0.89 | 0.85 |

*Bảng 4.1: Kết quả đánh giá hiệu năng trên tập truy vấn*

Bộ chỉ thị mạnh mẽ giúp hệ thống từ chối cung cấp dữ liệu ngoài luồng đạt tỉ lệ 95 phần trăm. Với nhóm ngôn ngữ mạng xã hội, thuật toán nhúng vector vẫn liên kết thành công văn bản quy chế nhờ chung không gian ngữ nghĩa.

### 4.2.2. Đánh giá hiệu năng và cơ chế tối ưu hóa

Kết quả bài kiểm thử Semantic Cache mang lại sự đột phá về tốc độ:

| Kịch bản | Tỷ lệ trúng đệm | Độ trễ trung bình | Mức tiêu thụ API |
|----------|-----------------|-------------------|------------------|
| Câu hỏi mới hoàn toàn | 0 phần trăm | 2400 ms | 100 phần trăm |
| Câu hỏi tương đồng cao | 100 phần trăm | 8 ms | 0 phần trăm |
| Truy vấn ngẫu nhiên thực tế | Khoảng 62 phần trăm | 950 ms | Tiết kiệm 62 phần trăm chi phí |

*Bảng 4.2: Đánh giá hiệu năng của Semantic Cache*

Trong bài kiểm thử ép tải kích hoạt mã lỗi hạn mức truy cập, hệ thống không xảy ra hiện tượng treo cứng. Lớp MultimodalEngine kích hoạt cơ chế chờ tự động thành công, đưa các luồng vượt ngưỡng vào trạng thái chờ 30 giây và tiếp tục phục hồi xử lý khi hạn mức được mở lại, duy trì tỷ lệ vận hành thành công đạt trên 99 phần trăm. Cơ chế dự phòng cập nhật liên tục cũng thu thập trọn vẹn tin nhắn mà không bị rớt gói dữ liệu nào.

## 4.3. Phân tích kết quả và thảo luận

Kết quả thực nghiệm phân tách rõ ràng ranh giới năng lực của kiến trúc đề xuất.

Về điểm sáng kỹ thuật, hệ thống chứng minh độ an toàn cực cao trong việc ngăn chặn hiện tượng ảo giác (Hallucination). Sự kết hợp giữa Semantic Cache và thuật toán thử lại tự động giải quyết triệt để vấn đề thắt cổ chai của nền tảng dịch vụ đám mây. Sự kết hợp này biến hệ thống thành một giải pháp hoàn toàn khả thi để triển khai thương mại trong mùa cao điểm.

Về rào cản tồn đọng, hệ thống gặp khó khăn khi xử lý nhóm câu hỏi có logic phức hợp lồng ghép nhiều biến số. Ví dụ đối với câu hỏi xác định mức giảm học phí cho một nam sinh ngành Công nghệ thông tin có chứng chỉ ngoại ngữ và thuộc diện hộ nghèo. Các mệnh đề điều kiện rời rạc nằm ở các văn bản khác nhau thường bị mất bối cảnh khi hệ thống phân rã tài liệu theo kích thước, dẫn đến Context Recall bị giảm. 

## 4.4. Minh họa hoạt động hệ thống

Quy trình giao tiếp giữa học sinh và máy chủ được thực hiện trên ứng dụng nhắn tin nội bộ và giao diện quản lý máy chủ. Trên luồng tương tác, văn bản tư vấn được truyền tải từng cụm từ qua Server-Sent Events (SSE) nhằm triệt tiêu cảm giác chờ đợi của người dùng.

[ CHÈN ẢNH ZALO BOT HOẠT ĐỘNG THỰC TẾ VÀO ĐÂY ]
*Hình 4.1: Hệ thống trợ lý ảo đang tư vấn trực tiếp trên nền tảng nhắn tin*

[ CHÈN ẢNH WEB ADMIN DASHBOARD HOẠT ĐỘNG THỰC TẾ VÀO ĐÂY ]
*Hình 4.2: Giao diện nạp dữ liệu tri thức tự động trên Web Admin Dashboard*
