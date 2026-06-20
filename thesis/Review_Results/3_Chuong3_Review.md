# Đánh Giá 3_Chuong3.md

## 1. Dấu Hiệu AI & Ngôn Ngữ (AI Pattern Recognition & Linguistic Authenticity)
**Đánh giá: AI sinh 100% (High probability of AI generation).**

Lỗi cụm từ dịch máy, word salad (Unnatural / AI phrasing).
> "Sự tương tác cuối cùng của toàn bộ cấu trúc dữ liệu được hiện thực hóa tại mô-đun hỏi đáp RAG..."
> "...hạn chế tình trạng sinh ngôn ngữ hoa mỹ xa rời sự thật."
> "...trả về trực tiếp từng phân đoạn chữ sinh ra từ AI về tay người dùng."
> "Thuật toán tinh tế phân biệt rõ ràng..."
Lý do: Văn phong lai căng, tối nghĩa. Tiếng Việt không ai nói "phân đoạn chữ sinh ra từ AI về tay người dùng" hay tự khen code mình là "thuật toán tinh tế". Dịch thô từ prompt.

Lỗi chuyển ý dập khuôn (Generic transitions).
> "Dù ẩn sau hậu trường, giao diện bảng điều khiển..."
Lý do: AI tạo kịch tính thừa thãi ("Behind the scenes").

## 2. Độ Sâu Kỹ Thuật (Methodological Rigor)
Lỗi thiết kế hệ thống ngây ngô (Naive technical design / Logic flaws).
> "...kiểm tra nhanh nếu câu hỏi người dùng chỉ có nội dung chào hỏi ngắn gọn (như chào, hi) hay dưới 10 ký tự, hệ thống lập tức bỏ qua khâu tìm kiếm tệp vector đắt đỏ."
Lý do: Dùng `len(text) < 10` để phân loại ý định (intent classification) là một thiết kế tồi, thiếu tính học thuật. Nếu người dùng hỏi "Điểm chuẩn" (10 ký tự) hoặc "Học phí" (7 ký tự) thì hệ thống sẽ bỏ qua RAG? Sai lầm nghiêm trọng về thuật toán xử lý NLP.
Hành động: Phải dùng mô hình phân loại ý định (Intent Classifier) hoặc Regex chuẩn. Xóa logic đếm ký tự.

Lỗi tham số vô căn cứ (Magic numbers).
> "...cho phép 5 luồng tải tệp diễn ra song song..."
Lý do: Tại sao 5 luồng? Dựa trên CPU core hay giới hạn API rate limit của trường TLU? Không có căn cứ kỹ thuật.

Lỗi miêu tả quá trình (Superficial description).
> Chế độ SSE được miêu tả như "chuỗi sự kiện tự chuyển".
Lý do: Không đúng thuật ngữ kỹ thuật. SSE là Server-Sent Events.

## 3. Hình Thức (Formatting)
Mô tả kiến trúc lan man. 
Hành động: Tập trung vào luồng dữ liệu (Data flow) thay vì văn tả cảnh hệ thống. Đoạn mô tả Zalo bot và Web Admin viết chung chung, thiếu API specs rõ ràng.

Kết luận: Rác kỹ thuật. Tác giả không hiểu bản chất code, dùng AI viết văn tả cảnh để bôi chữ. Phải sửa lỗi logic nhận diện ý định (<10 ký tự) ngay lập tức.
