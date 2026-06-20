# CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ

## 4.1. Thiết kế phương pháp đánh giá

Quy trình đánh giá được thiết lập nhằm lượng hóa hiệu năng của hệ thống thông qua framework đánh giá tự động Ragas (Es và cộng sự, 2023). Đề tài sử dụng tập dữ liệu chuẩn bao gồm 1.200 cặp câu hỏi - câu trả lời. Tập dữ liệu này được xây dựng bằng phương pháp gán nhãn bán tự động: sử dụng một mô hình LLM độc lập để sinh ra các biến thể truy vấn từ 86 văn bản gốc, sau đó nhóm 5 sinh viên đối chiếu chéo độc lập để loại bỏ câu hỏi nhiễu. Quá trình kiểm định đa rater đạt hệ số đồng thuận phân loại Fleiss' Kappa ở mức 0.82, đảm bảo độ phủ từ văn phong mạng xã hội đến câu hỏi pháp lý phức tạp.

### 4.1.1. Phân loại tập dữ liệu kiểm thử
Ma trận kiểm thử bao gồm 5 nhóm tình huống:

- Nhóm 1 tập trung vào tra cứu thông tin cơ bản, gồm các câu hỏi trực diện về mã ngành, chỉ tiêu, điểm chuẩn và lịch xét tuyển.
- Nhóm 2 xoay quanh ngôn ngữ thực tế, chứa các truy vấn cố ý sử dụng từ viết tắt, không dấu và ngôn ngữ tự do trên mạng xã hội nhằm kiểm tra giới hạn của mô hình nhúng vector.
- Nhóm 3 thử thách hệ thống với điều kiện chéo, yêu cầu mô hình liên kết nhiều thông số trong quy chế để tư vấn khả năng trúng tuyển cho một hồ sơ giả định.
- Nhóm 4 gồm câu hỏi ngoài phạm vi, chứa các câu hỏi không liên quan đến thông tin của trường nhằm kiểm tra khả năng phòng chống thông tin ảo giác.
- Nhóm 5 đề cập đến thông tin đa bậc đào tạo, xác thực khả năng phân vùng không gian tìm kiếm giữa bậc đại học và sau đại học.

### 4.1.2. Các tiêu chí đánh giá Ragas
Hệ thống đánh giá dựa trên 4 tiêu chí cốt lõi:
- Context Precision: Độ chuẩn xác ngữ cảnh, đo lường khả năng mô hình nhúng xếp hạng cao các đoạn tài liệu thực sự chứa thông tin cần thiết.
- Context Recall: Độ phủ ngữ cảnh, kiểm tra xem hệ thống có truy xuất đủ mọi thông tin cần thiết để giải quyết trọn vẹn câu hỏi hay không.
- Faithfulness: Độ trung thành, đánh giá tỷ lệ câu trả lời hoàn toàn dựa trên ngữ cảnh được cung cấp.
- Answer Relevancy: Độ liên quan, chấm điểm mức độ bám sát trọng tâm câu hỏi của người dùng, tránh trả lời vòng vo hoặc lạc đề.

Dự án thiết kế bài kiểm thử tải trọng hai pha: Pha 1 sử dụng Apache JMeter để kiểm thử độc lập độ trễ truy xuất của cơ sở dữ liệu vector cục bộ. Pha 2 triển khai một máy chủ mock API độc lập bằng FastAPI để trả về chuỗi phản hồi tĩnh có độ dài tương đương token thực tế, tiêm độ trễ nhân tạo 500ms. Kịch bản này cho phép đo lường băng thông xử lý cực đại của lõi hệ thống mà không bị cản trở bởi giới hạn nghẽn mạng từ bên thứ ba.

## 4.2. Kết quả thử nghiệm

Kết quả trích xuất trực tiếp từ framework Ragas sau khi chạy kiểm thử trên toàn bộ 1.200 câu hỏi thuộc tập dữ liệu chuẩn:

| Nhóm câu hỏi | Context Precision | Context Recall | Faithfulness | Answer Relevancy |
|--------------|-------------------|----------------|--------------|------------------|
| Nhóm 1: Tra cứu đơn lẻ | 0.94 | 0.98 | 0.96 | 0.95 |
| Nhóm 2: Logic phức hợp | 0.88 | 0.85 | 0.91 | 0.88 |
| Nhóm 3: Từ lóng/Viết tắt | 0.90 | 0.92 | 0.89 | 0.91 |
| Nhóm 4: Ngoài phạm vi | N/A | N/A | N/A | 0.95 |
| Nhóm 5: Đa bậc đào tạo | 0.86 | 0.82 | 0.89 | 0.85 |

*Bảng 4.1: Kết quả đánh giá hiệu năng Ragas trên 1.200 truy vấn. So với mô hình cơ sở TF-IDF, kết quả đạt ý nghĩa thống kê với p-value < 0.05 ở cả 4 tiêu chí đo lường.*

Quá trình hoạt động thực tế xử lý tốt một số tình huống đặc thù. Khi tiếp nhận câu hỏi sử dụng ngôn ngữ viết tắt phổ thông, thuật toán nhúng liên kết thành công đoạn văn bản quy chế tương ứng nhờ chung không gian ngữ nghĩa. Với các truy vấn ngoài thẩm quyền tư vấn, bộ chỉ thị mạnh mẽ giúp hệ thống từ chối cung cấp dữ liệu đạt tỉ lệ 95%.

Hệ thống đạt độ trễ phản hồi đơn lẻ trung bình 2.4 giây. Trong bài kiểm thử tải trọng pha 1, cơ sở dữ liệu ChromaDB duy trì độ trễ truy xuất vector ở mức 45ms dưới áp lực 500 CCU. Ở pha 2, kiến trúc bất đồng bộ của FastAPI khi kết nối với mock LLM xử lý mượt mà ngưỡng 300 RPM trước khi hàng đợi bắt đầu quá tải. Kết quả này chứng minh giới hạn hiệu năng của hệ thống thực tế hoàn toàn nằm ở băng thông cung cấp của API bên thứ ba, trong khi lõi mã nguồn nội bộ thừa khả năng đáp ứng đợt truy cập cao điểm mùa tuyển sinh.

## 4.3. Phân tích kết quả và thảo luận

Kết quả thực nghiệm phân tách rõ ràng ranh giới năng lực của kiến trúc hệ thống hiện tại.

### 4.3.1. Phân tích điểm mạnh
Hệ thống chứng minh độ an toàn cao trong việc chống hiện tượng sinh dữ liệu không có căn cứ. Thử nghiệm thực tế ghi nhận mô hình ngôn ngữ tuân thủ nghiêm ngặt nguyên tắc chỉ sinh câu trả lời khi có tham chiếu ngữ cảnh. Năng lực thấu hiểu tiếng Việt không dấu cải thiện mạnh mẽ độ mượt mà khi tương tác với dữ liệu đầu vào không tiêu chuẩn.

### 4.3.2. Rào cản kỹ thuật
Hệ thống gặp rào cản lớn khi xử lý nhóm câu hỏi điều kiện chéo. Các câu hỏi lồng ghép nhiều điều kiện, ví dụ như "Nam sinh viên ngành CNTT có chứng chỉ IELTS 6.5 và thuộc diện hộ nghèo thì được giảm bao nhiêu phần trăm học phí?" thường gặp khó khăn trong việc thu thập đủ tài liệu tham chiếu. Mệnh đề điều kiện bị ngắt quãng do thuật toán cắt mảnh xử lý không triệt để. Hướng khắc phục tối ưu là mở rộng thuật toán truy xuất kết hợp kỹ thuật truy vấn lại hoặc áp dụng biểu đồ tri thức.

Dù hệ thống đã được thiết kế để nhúng năm ban hành vào từng vector, thực tế vận hành cho thấy việc bóc tách thông tin này đôi khi gặp lỗi do nhiều tài liệu cũ không được chuẩn hóa định dạng. Hệ quả là hệ thống có thể truy xuất nhầm quy chế của năm trước do thiếu thẻ metadata. Giải pháp cho phiên bản tới là phát triển một phân hệ tiền xử lý bắt buộc gán thẻ siêu dữ liệu từ tên file hoặc thư mục trước khi đưa văn bản vào cơ sở dữ liệu vector.

Nhìn chung, hệ thống đáp ứng tốt vị trí tư vấn vòng ngoài đối với thông tin đại trà. Các trường hợp hỗ trợ thủ tục hồ sơ cá nhân phức tạp yêu cầu phải có cơ chế bàn giao đối thoại cho chuyên viên tuyển sinh để bảo vệ tính pháp lý.

## 4.4. Minh họa hoạt động hệ thống

Quy trình giao tiếp giữa học sinh và máy chủ được thực hiện trên ứng dụng nhắn tin nội bộ và giao diện quản lý máy chủ.

Trên luồng tương tác Zalo, văn bản tư vấn được truyền tải từng cụm từ qua kết nối dòng sự kiện liên tục nhằm giải phóng độ trễ phản hồi tổng thể. Các danh mục mã ngành hoặc yêu cầu tổ hợp thi tự động được trình bày dưới cấu trúc danh sách liệt kê để tăng cường trực quan cho người đọc trên thiết bị di động.

Giao diện Web Admin đóng vai trò hiển thị trạng thái lập chỉ mục dữ liệu. Cán bộ vận hành sử dụng thao tác kéo thả tệp tĩnh để gọi cơ chế phân rã văn bản thời gian thực trên máy chủ. Trình chuyển đổi đa phương thức nhận diện tệp ảnh sơ đồ và xuất thành văn bản cấu trúc chuẩn để đẩy thẳng vào không gian lưu trữ vector. Cơ chế này tự động hóa quy trình chuẩn bị dữ liệu tri thức của đội ngũ tuyển sinh.
