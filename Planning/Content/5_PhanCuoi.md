# LỜI CẢM ƠN

Trong suốt quá trình thực hiện đồ án tốt nghiệp, em đã nhận được sự quan tâm, giúp đỡ và động viên rất lớn từ các thầy cô giáo, gia đình và bạn bè.

Trước hết, em xin gửi lời tri ân sâu sắc nhất đến TS. Lê Anh Tuấn. Thầy đã dành nhiều thời gian quý báu để tận tình hướng dẫn, định hướng công nghệ và tháo gỡ những vướng mắc cho em trong suốt quá trình triển khai hệ thống trợ lý ảo này. Những lời khuyên chuyên môn của thầy là kim chỉ nam giúp đồ án đi đúng hướng và đạt được kết quả như hiện tại.

Em cũng xin gửi lời cảm ơn chân thành đến Ban Giám hiệu Trường Đại học Thủy Lợi và toàn thể các thầy cô giáo khoa Công nghệ thông tin. Các thầy cô đã truyền đạt cho em những kiến thức nền tảng vô giá trong suốt những năm tháng ngồi trên giảng đường, tạo nền móng vững chắc để em có thể tự tin nghiên cứu và ứng dụng các công nghệ mới.

Đồng thời, em cũng xin bày tỏ lòng biết ơn vô hạn đối với gia đình và những người bạn đã luôn ở bên cạnh, động viên tinh thần và tạo mọi điều kiện thuận lợi nhất để em có thể hoàn thành tốt chương trình học thuật của mình.

Mặc dù đã nỗ lực hết sức, nhưng do giới hạn về mặt thời gian và kiến thức cá nhân, đồ án chắc chắn không tránh khỏi những thiếu sót. Em rất mong nhận được sự góp ý quý báu từ hội đồng các thầy cô để đề tài được hoàn thiện hơn.

Em xin chân thành cảm ơn!

---

# TÓM TẮT ĐỒ ÁN

Đồ án tập trung nghiên cứu và xây dựng một hệ thống trợ lý ảo thông minh nhằm hỗ trợ công tác tư vấn tuyển sinh tại Trường Đại học Thủy Lợi. Động lực của nghiên cứu xuất phát từ thực trạng lượng thông tin tuyển sinh ngày càng đồ sộ, dẫn đến tình trạng phân mảnh thông tin và gây quá tải cho bộ phận tư vấn truyền thống trong các khoảng thời gian cao điểm.

Để giải quyết bài toán này, đồ án đã ứng dụng kiến trúc RAG kết hợp với mô hình sinh ngôn ngữ lớn. Hệ thống được phát triển dựa trên ngôn ngữ lập trình Python, sử dụng khung điều phối LangChain và cơ sở dữ liệu dạng vector ChromaDB để quản lý và truy xuất thông tin từ các đề án tuyển sinh. Điểm nổi bật của hệ thống là khả năng chống lại hiện tượng sinh văn bản sai lệch, đảm bảo mọi câu trả lời đều được trích xuất chính xác từ nguồn dữ liệu chính thống của nhà trường.

Hệ thống được thiết kế với hai nền tảng giao diện tách biệt. Người dùng cuối tương tác trực tiếp với hệ thống thông qua kênh Zalo Bot, mang lại trải nghiệm hỏi đáp tự nhiên, liên tục và không đòi hỏi kỹ năng công nghệ phức tạp. Ở chiều ngược lại, nền tảng quản trị dành cho ban tuyển sinh được xây dựng dưới dạng ứng dụng Web, cung cấp bộ công cụ toàn diện để cập nhật cơ sở dữ liệu và giám sát chất lượng hội thoại theo thời gian thực.

Kết quả thử nghiệm cho thấy hệ thống hoạt động ổn định, có tốc độ phản hồi nhanh và khả năng xử lý tốt các câu hỏi đa luồng. Sản phẩm không chỉ minh chứng cho tính ứng dụng cao của trí tuệ nhân tạo trong giáo dục mà còn mở ra tiềm năng phát triển thành một hệ thống tư vấn tuyển sinh tự động toàn diện trong tương lai.

---

# TÀI LIỆU THAM KHẢO

[1] Patrick Lewis và các cộng sự, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS, 2020.
[2] LangChain AI, *LangChain Documentation*, trang tài liệu kỹ thuật chính thức.
[3] Google, *Google Gemini API Reference*, trang tài liệu dành cho nhà phát triển.
[4] Chroma, *ChromaDB Documentation*, trang tài liệu kỹ thuật cơ sở dữ liệu dạng vector.
[5] Trường Đại học Thủy Lợi, *Đề án tuyển sinh trình độ đại học các năm*, cổng thông tin tuyển sinh chính thức.
[6] Trường Đại học Thủy Lợi, *Thông báo tuyển sinh trình độ thạc sĩ và tiến sĩ*, cổng thông tin tuyển sinh chính thức.
