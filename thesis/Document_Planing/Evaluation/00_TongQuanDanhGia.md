# TỔNG QUAN BỘ DỮ LIỆU ĐÁNH GIÁ

## 1. Mục đích thiết lập bộ dữ liệu
Bộ dữ liệu đánh giá được thiết kế với mục tiêu mô phỏng chính xác và toàn diện các luồng câu hỏi thực tế mà người dùng sẽ tương tác với hệ thống trợ lý ảo tuyển sinh. Quá trình kiểm thử bằng bộ dữ liệu này nhằm định lượng hiệu năng của hệ thống theo các tiêu chí đã được thiết lập, đảm bảo chất lượng hệ thống trước khi đưa vào môi trường trực tuyến.

## 2. Cấu trúc bộ câu hỏi
Tập dữ liệu kiểm thử (ground-truth dataset) quy mô lớn bao gồm 1.200 câu hỏi - câu trả lời. Để minh họa trực quan, tài liệu này trích xuất một tập mẫu đại diện (sample set) gồm 250 câu hỏi điển hình, chia đều cho 5 nhóm chuyên biệt. Mỗi nhóm đóng vai trò kiểm tra một giới hạn cụ thể của hệ thống, đi từ đơn giản đến phức tạp. Nhóm 1 kiểm tra khả năng trích xuất thông tin có cấu trúc tĩnh như mã ngành, điểm chuẩn, chỉ tiêu. Nhóm 2 đánh giá khả năng hiểu tiếng Việt không chuẩn mực, viết tắt, từ lóng mạng xã hội. Nhóm 3 thử thách khả năng suy luận logic dựa trên nhiều mệnh đề dữ kiện trong một bộ hồ sơ giả định. Nhóm 4 tập trung vào khả năng chống ảo giác, triệt tiêu việc sinh thông tin sai lệch và tuân thủ ranh giới nội dung. Nhóm 5 xác minh độ chính xác trong việc phân mảnh không gian tìm kiếm, đảm bảo sự tách biệt giữa bậc đại học và bậc sau đại học.

## 3. Các tiêu chí đánh giá
Sức mạnh của hệ thống được đo lường bằng khung đánh giá tự động kết hợp đối chiếu chéo với 4 chỉ số cốt lõi. Độ bao phủ ngữ cảnh kiểm tra sự đầy đủ của tài liệu truy xuất, yêu cầu lớn hơn hoặc bằng 0.8. Độ chuẩn xác ngữ cảnh kiểm tra tỷ lệ nhiễu trong tài liệu truy xuất, yêu cầu lớn hơn hoặc bằng 0.8. Độ liên quan của câu trả lời kiểm tra khả năng bám sát chủ đề câu hỏi, yêu cầu lớn hơn hoặc bằng 0.8. Cuối cùng, độ trung thành kiểm tra việc tuân thủ tuyệt đối văn bản gốc, không bịa thông tin, yêu cầu tiệm cận 1.0.

## 4. Danh mục tài liệu triển khai
Các tệp chi tiết chứa định nghĩa, tiêu chí đầu vào và danh sách câu hỏi mẫu cho 5 nhóm bao gồm:
- `01_Nhom1_TraCuuCoBan.md`
- `02_Nhom2_NgonNguThucTe.md`
- `03_Nhom3_DieuKienCheo.md`
- `04_Nhom4_BayNgoaiPhamVi.md`
- `05_Nhom5_DaBacDaoTao.md`
