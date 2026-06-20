# Đánh Giá 2_Chuong2.md

## 1. Dấu Hiệu AI & Ngôn Ngữ (AI Pattern Recognition & Linguistic Authenticity)
**Đánh giá: AI sinh 100% (High probability of AI generation).**

Lỗi từ vựng phi tự nhiên (Unnatural Vocabulary).
> "...đóng vai trò là chất xám quyết định trực tiếp..."
> "...duy trì văn phong giao tiếp tự nhiên không mang dấp dáng của máy móc."
Lý do: Không ai dùng "chất xám" để mô tả tập dữ liệu, hoặc "dấp dáng" trong văn phong học thuật. Dịch máy hoặc LLM rặn chữ.
Hành động: Dùng từ phổ thông: "dữ liệu nền tảng", "đặc trưng máy móc".

Lỗi chuyển ý dập khuôn (Generic transitions).
> "Quá trình chuẩn bị tập dữ liệu đồ sộ này đặt ra nhiều bài toán..."
> "Một rào cản lớn khác nằm ở..."
> "Hiện tượng mất ngữ cảnh khi phân mảnh cũng là một rủi ro tiềm ẩn."
> "Một rào cản cuối cùng là..."
Lý do: AI dùng cấu trúc liệt kê tuyến tính. Văn phong thiếu sự móc nối logic chuyên sâu.

## 2. Độ Sâu Kỹ Thuật (Methodological Rigor)
Lỗi thông số vô căn cứ (Magic numbers / Lack of validation).
> "...kích thước phân mảnh văn bản được cấu hình ở ngưỡng lớn là 1000 ký tự cùng độ trùm lặp 200 ký tự..."
> "...truy xuất 3 đoạn tài liệu có độ tương quan cao nhất."
Lý do: Tại sao 1000/200? Tại sao 3 đoạn? Không có thực nghiệm đánh giá (empirical validation) nào được trích dẫn để bảo vệ các hằng số này.
Hành động: Phải giải thích cơ sở chọn tham số hoặc trích dẫn thực nghiệm ở chương sau.

Lỗi ngụy biện trong sơ đồ (Superficial claims in design).
> Khối "Gửi văn bản thấu hiểu ngữ nghĩa" (Sơ đồ 2.5.1)
Lý do: Thuật ngữ tối nghĩa, phi kỹ thuật. Chuyển văn bản thô cho embedding model chứ không phải "gửi văn bản thấu hiểu ngữ nghĩa".

## 3. Hình Thức & Cấu Trúc (Formatting & Structural Cohesion)
Lỗi đánh số mục (Numbering error).
> Lặp lại mục "2.5.3":
> `### 2.5.3. Luồng tư vấn hỏi đáp đa lượt`
> `### 2.5.3. Luồng chuyển đổi tệp đa phương thức`
Lý do: AI sinh lỗi nhảy số (hallucinated sequence). Lỗi cơ bản của việc không kiểm duyệt.
Hành động: Sửa lại thứ tự 2.5.3, 2.5.4, 2.5.5.

Lỗi văn mẫu trong mô tả sơ đồ (Fluff).
> "Giải quyết triệt để các thách thức về dữ liệu yêu cầu một kiến trúc hệ thống RAG đồng bộ và phân lớp rõ ràng."
Lý do: Văn mẫu dẫn vào sơ đồ. Không có giá trị thông tin.

Kết luận: Rác. Sinh viên prompt AI xong không thèm đọc lại (lỗi đánh số mục). Cần đập bỏ viết lại, đưa số liệu kỹ thuật thực tế vào thay vì văn mẫu.
