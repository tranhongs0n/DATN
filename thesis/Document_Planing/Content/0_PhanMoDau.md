# PHẦN MỞ ĐẦU

## 1. Lý do chọn đề tài

Trường Đại học Thủy Lợi tiếp nhận lượng lớn yêu cầu tư vấn trong mỗi kỳ tuyển sinh. Nội dung thắc mắc trải rộng từ phương thức xét tuyển, chỉ tiêu, điểm chuẩn đến học phí và học bổng. Tình trạng thông tin phân tán trên nhiều hệ thống văn bản, đề án và thông báo khiến người học mất nhiều thời gian tra cứu. Thực trạng này đòi hỏi nhân sự tuyển sinh phải liên tục đối chiếu qua nhiều tài liệu để trả lời các câu hỏi mang tính chu kỳ.

Để tự động hóa quy trình này, các trường từng áp dụng chatbot dựa trên luật tĩnh. Kiến trúc rẽ nhánh thất bại khi sinh viên hỏi câu ghép phức tạp hoặc dùng ngôn ngữ tự do. Phí bảo trì cũng gia tăng vì kỹ sư phải sửa mã nguồn mỗi lần nhà trường cập nhật quy chế.

Kỹ thuật Sinh văn bản Tăng cường Truy xuất (Lewis và cộng sự, 2020) kết hợp sức mạnh tổng hợp ngôn ngữ của mô hình lớn với cơ sở tri thức độc lập. Nhờ tách rời cơ sở dữ liệu và mô hình suy luận, hệ thống tránh được hiện tượng ảo giác sinh ra thông tin sai lệch. Khi quy chế thay đổi, quản trị viên chỉ cần nạp lại tài liệu văn bản mà không phải huấn luyện lại mạng nơ-ron. Xuất phát từ nhu cầu thực tiễn đó, đề tài "Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG" được triển khai.

## 2. Mục tiêu nghiên cứu

Nghiên cứu kiến trúc hệ thống RAG, bao gồm các phương pháp phân mảnh văn bản, tối ưu hóa quá trình nhúng dữ liệu và truy xuất trên cơ sở dữ liệu vector. Đề tài tập trung đánh giá mức độ tương thích của các mô hình nhúng và LLM đối với ngôn ngữ tiếng Việt trong lĩnh vực giáo dục.

Xây dựng hệ thống trợ lý ảo hoạt động trên nền tảng Zalo, hỗ trợ giải đáp thông tin tuyển sinh ở các bậc đại học, thạc sĩ và tiến sĩ. Hệ thống cần khả năng phân loại ý định người dùng và truy xuất chính xác nguồn dữ liệu nội bộ.

Phát triển trang quản trị nền tảng Web cho phép đội ngũ tuyển sinh cập nhật trực tiếp văn bản quy định mới, đồng thời giám sát lịch sử hội thoại và chất lượng phản hồi từ hệ thống.

## 3. Đối tượng và phạm vi nghiên cứu

Đối tượng nghiên cứu là kỹ thuật RAG, tập trung vào việc thiết lập luồng tiền xử lý tài liệu đa định dạng. Hệ thống tích hợp thư viện LangChain để giải xuất các tệp DOCX và áp dụng nền tảng Docling nhằm tái cấu trúc tệp PDF sang định dạng Markdown. Quá trình chia nhỏ văn bản được thực hiện thông qua thuật toán RecursiveCharacterTextSplitter để chuẩn bị dữ liệu đầu vào cho mô hình nhúng. Nền tảng tri thức cốt lõi là tập dữ liệu tuyển sinh chính thức của trường từ năm 2020 đến 2026.

Phạm vi dữ liệu bao gồm 86 tệp tài liệu nguyên thủy (38 tệp đại học, 36 tệp thạc sĩ và 12 tệp tiến sĩ). Khung phần mềm chạy trên Python, điều phối luồng truy xuất bằng FastAPI và lưu trữ embeddings cục bộ qua ChromaDB. Hệ thống từ chối trả lời mọi câu hỏi không thuộc phạm vi tuyển sinh nội bộ.

## 4. Phương pháp nghiên cứu

Nghiên cứu tài liệu học thuật về trí tuệ nhân tạo và hệ thống truy xuất thông tin để xác định thiết kế kiến trúc chuẩn cho toàn bộ quy trình RAG.

Nghiên cứu thực nghiệm được thực hiện để đo lường độ trễ, độ chính xác của các chiến lược phân đoạn văn bản và thuật toán so khớp vector. Kết quả này định hướng lựa chọn cấu hình siêu tham số tối ưu.

Phát triển phần mềm tuân thủ quy trình kiểm thử liên tục, phân tách rõ ràng luồng dữ liệu giữa giao diện nhắn tin, hệ thống máy chủ và khối cơ sở dữ liệu.

## 5. Ý nghĩa khoa học và thực tiễn

Đề tài góp phần hệ thống hóa quy trình xây dựng ứng dụng hỏi đáp dựa trên tri thức chuyên biệt bằng tiếng Việt. Kinh nghiệm thử nghiệm và tinh chỉnh các tham số trên dữ liệu thực tế đóng vai trò quan trọng cho công tác triển khai RAG đối với các tài liệu quy định giáo dục vốn có tính khuôn mẫu và phức tạp cao.

Sản phẩm cung cấp hệ thống tư vấn tự động 24/7, giảm tải khối lượng công việc cho phòng ban tuyển sinh. Trang quản trị hỗ trợ số hóa và giám sát tập trung toàn bộ kho dữ liệu đầu vào, tạo tiền đề cho các dự án chuyển đổi số tiếp theo của nhà trường.
