# HƯỚNG DẪN GẶP GIẢNG VIÊN PHẢN BIỆN (PRE-DEFENSE)

Giảng viên phản biện (GVPB) là người sẽ chấm điểm sơ bộ (trung bình 2 người >= 5.5 mới được ra hội đồng). 
Đặc thù khi gặp GVPB (có thể online qua Teams/Zalo hoặc ra quán cafe/phòng lab):

## 1. Mục đích của GVPB
Họ không có thời gian nghe bạn thuyết trình dài dòng. Họ chỉ muốn biết:
1. Đồ án có **thật** không? Bạn có tự code không hay đi mua?
2. Khối lượng công việc có đủ lớn để bảo vệ không?
3. Tính ứng dụng có thật không?

## 2. Cần mang theo gì khi gặp?
- Máy tính laptop đã **chạy sẵn** code, server khởi động sẵn. Cực kỳ cấm kỵ việc ngồi chờ run code bị lỗi thư viện trước mặt thầy.
- File PDF bản thảo đồ án (Hoặc bản in nếu gặp offline).
- File Word "Hướng dẫn SV làm rõ nội dung" (mà mình vừa điền ở bước trước).
- Bản in của Slide thuyết trình (Dù chưa bảo vệ nhưng có Slide show ra thầy sẽ đánh giá cao tính cẩn thận).

## 3. Chiến thuật nói chuyện
- Đừng chờ thầy hỏi "Em làm gì?", hãy chủ động: *"Dạ em chào thầy, em xin phép trình bày ngắn 3 phút về sản phẩm đồ án của em. Cốt lõi của em là hệ thống chatbot RAG kết nối thẳng vào Zalo và có hệ thống Admin quản trị bằng React. Em xin phép demo nhanh cho thầy xem luôn ạ."*
- **Tuyệt đối trung thực:** Nếu thầy hỏi phần giao diện web admin lấy ở đâu, cứ nói thật là dùng thư viện React Material/AntD sẵn có, nhưng API backend, luồng RAG và Semantic Cache là em tự viết hoàn toàn. (Thầy đánh giá backend và logic AI cao hơn cái web đẹp).

## 4. Chuẩn bị tinh thần bị chê
- GVPB có nhiệm vụ "bắt lỗi" để bạn sửa trước khi ra hội đồng lớn.
- Nếu thầy chê biểu đồ vẽ sai mũi tên, mô hình bảng thiếu chuẩn hóa -> Cứ vâng ạ em sẽ sửa ngay, đừng cãi.
- Nếu thầy chê Chatbot chậm hoặc bịa thông tin -> Mở luôn file test 1200 câu hỏi ra (File CSV) chứng minh là em đã đo lường bằng RAGAS, tỷ lệ trung thực lên tới 89%, và đã dùng Cache để giảm độ trễ xuống 8ms. Đem "Số liệu" ra nói chuyện sẽ chặn họng được những nhận xét cảm tính.
