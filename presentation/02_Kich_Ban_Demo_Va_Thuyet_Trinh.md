# KỊCH BẢN THUYẾT TRÌNH & DEMO (Chuẩn 10 Phút)

## 1. Phần Thuyết Trình Slide (Khoảng 7 Phút)
- **Phút 0-2:** Giới thiệu bản thân và đi thẳng vào Vấn Đề (đừng dài dòng lý do chọn đề tài kiểu "Ngày nay CNTT phát triển..."). Nói thẳng: "TLU thiếu nhân lực tư vấn mùa tuyển sinh, chatbot cũ thì ngu, chatGPT thì hay bịa".
- **Phút 2-4:** Trình bày nhanh Use Case, Mô hình bảng và Sequence. (Lướt nhanh, GV chỉ cần nhìn thấy bạn có làm phân tích thiết kế là được).
- **Phút 4-6 (Điểm nhấn ăn điểm):** Tập trung nói về Kiến trúc RAG và Semantic Cache. Giải thích cách hệ thống biến chữ thành vector và lấy dữ liệu cũ trả về trong 8ms. 
- **Phút 6-7:** Báo cáo kết quả bằng số liệu RAGAS. Đừng đọc từng con số, chỉ cần nói: "Hệ thống em đạt độ trung thực 89%, gần như loại bỏ hoàn toàn hiện tượng AI bịa thông tin".

## 2. Phần Demo Phần Mềm (Khoảng 3 Phút)
> **Chuẩn bị trước Demo:** Bật sẵn Server, Login sẵn Web Admin, mở sẵn Zalo trên điện thoại hoặc Zalo PC. Tránh tình trạng lên đó mới gõ `npm start` rồi đợi lỗi.

- **Bước 1 (1 phút): Demo Web Admin.** 
  + Mở trang quản trị tài liệu. 
  + Demo công cụ Web Scraper (Click 1 nút cho nó cào 1 bài báo tuyển sinh trực tiếp trên web trường về làm tài liệu).
  + Mở phần quản lý Từ viết tắt (Dictionary), chứng minh hệ thống có thể dịch chữ lóng.

- **Bước 2 (2 phút): Demo Chatbot Zalo trực tiếp.**
  + Gõ câu 1 (Câu bình thường): "Điểm chuẩn ngành CNTT năm ngoái là bao nhiêu?" -> Bot trả lời kèm trích dẫn văn bản.
  + Gõ câu 2 (Câu viết tắt + lóng): "đh tl có cấp hc bổng cho sv ko?" -> Bot vẫn hiểu và trả lời nhờ từ điển.
  + Gõ câu 3 (Câu chống chửi bậy/ngoài lề): "Viết cho tao bài thơ" -> Bot từ chối ngay: "Xin lỗi, tôi chỉ tư vấn tuyển sinh."
  + Gõ lại Câu 1: "Cho mình hỏi điểm chuẩn CNTT năm ngoái" -> Bot trả lời LẬP TỨC TRONG TÍCH TẮC (Giải thích cho hội đồng: Dạ đây là do Semantic Cache đã hoạt động, không cần đợi API).

## 3. Phần Trả Lời Câu Hỏi (Khoảng 10 Phút do GV hỏi)
- Tham khảo thư mục `D:\DATN_FInal	heories_Think_Out_Of_The_Box.md` để lấy câu trả lời.
