# Semantic Cache (Bộ nhớ đệm ngữ nghĩa)

## 1. Khái niệm và Bài toán
Vào mùa thi, hàng ngàn thí sinh có thể hỏi chung một nội dung nhưng khác cách diễn đạt (Vd: "Điểm chuẩn CNTT là nhiêu?" vs "Công nghệ thông tin lấy mấy điểm").
Nếu cứ mỗi câu hỏi đều phải lấy đi nhúng vector -> tìm DB -> gửi lên Gemini API thì:
- Quá tốn kém tiền API.
- Tốc độ trả lời cực chậm.

## 2. Giải pháp Semantic Cache
Sinh viên đã tự xây dựng một bộ nhớ đệm "ngữ nghĩa" (không phải đệm khớp chính xác từng chữ như Redis thông thường).
- **Cách hoạt động:** Khi có câu hỏi mới, nó biến thành Vector. Đem so sánh với các Vector của các CÂU HỎI CŨ đã lưu trong Cache.
- Nếu độ tương đồng vượt một ngưỡng (vd > 95%), hệ thống kết luận hai câu này ý nghĩa giống nhau -> Lấy ngay CÂU TRẢ LỜI CŨ trả về luôn. Bỏ qua hoàn toàn bước gọi LLM API.

## 3. Hiệu quả chứng minh được
- **Tốc độ:** Giảm độ trễ từ 2400ms (nếu gọi Gemini) xuống chỉ còn 8ms (đọc thẳng từ RAM).
- **Chi phí:** Tiết kiệm 62% chi phí gọi API nhờ tỷ lệ trúng đệm cao.
