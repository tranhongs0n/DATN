# CHƯƠNG 4: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 4.1. Những kết quả đạt được
Đề tài đã hoàn thành các mục tiêu nghiên cứu và ứng dụng thực tiễn đề ra ban đầu. Sản phẩm cốt lõi là một hệ thống trợ lý ảo tư vấn tuyển sinh cơ bản, có khả năng vận hành ổn định và đáp ứng được nhu cầu tìm kiếm thông tin của học sinh.

Về mặt công nghệ, đề tài đã tiếp cận và tích hợp các kỹ thuật xử lý ngôn ngữ tự nhiên hiện đại. Việc áp dụng mô hình nhúng và cơ sở dữ liệu dạng vector đã góp phần giải quyết bài toán tìm kiếm theo ngữ nghĩa, vượt qua rào cản của các phương pháp tìm kiếm từ khóa truyền thống. Kỹ thuật phân mảnh thông minh và bộ chỉ thị định hướng đã hạn chế hiện tượng sinh văn bản sai lệch, giúp câu trả lời của trợ lý ảo bám sát các quy chế xét tuyển hiện hành.

Về mặt sản phẩm, hệ thống đã phát triển hai nền tảng giao diện độc lập nhằm phù hợp với từng nhóm đối tượng. Đối với học sinh và phụ huynh, kênh Zalo Bot đóng vai trò là một điểm chạm thân thiện, dễ sử dụng, cho phép truy vấn thông tin mà không yêu cầu cài đặt phần mềm. Đối với ban tư vấn tuyển sinh, bảng điều khiển nền Web cung cấp một công cụ quản trị tri thức trực quan, hỗ trợ rút ngắn thời gian cập nhật tài liệu và quản lý quy trình hội thoại.

## 4.2. Những mặt hạn chế còn tồn tại
Mặc dù đã đạt được nhiều kết quả tích cực, hệ thống vẫn còn tồn tại một số hạn chế nhất định do rào cản về mặt hạ tầng và thói quen sử dụng mạng xã hội của người dùng.

Hạn chế lớn nhất đến từ sự phụ thuộc vào giao diện lập trình ứng dụng của bên thứ ba. Toàn bộ quá trình sinh văn bản hiện đang được xử lý thông qua máy chủ của Google. Điều này tiềm ẩn rủi ro về độ trễ mạng và khả năng gián đoạn dịch vụ nếu lưu lượng truy cập từ thí sinh tăng đột biến trong thời điểm công bố điểm chuẩn.

Vấn đề nan giải tiếp theo nằm ở khả năng xử lý các tin nhắn phân mảnh. Học sinh thường có thói quen ngắt nhỏ câu hỏi thành nhiều tin nhắn ngắn gửi liên tiếp. Việc hệ thống xử lý ngay lập tức từng tin nhắn đơn lẻ khiến cho bộ nhớ hội thoại bị nhiễu loạn, dẫn đến việc trích xuất dữ liệu không chính xác do thiếu hụt ngữ cảnh trầm trọng trong từng dòng tin nhắn.

Bên cạnh đó, trong các cuộc hội thoại kéo dài hàng chục lượt tương tác, hệ thống bắt đầu xuất hiện hiện tượng suy giảm ngữ cảnh. Mô hình sinh văn bản có xu hướng bỏ qua các thông tin quan trọng nằm ở đoạn giữa của chuỗi hội thoại, khiến chất lượng câu trả lời giảm sút đáng kể.

Ngoài ra, công cụ trích xuất văn bản từ hình ảnh chưa đạt được độ hoàn thiện tối đa. Đối với các biểu đồ hoặc bảng điểm được thiết kế phá cách với cấu trúc lồng ghép phức tạp, hệ thống thỉnh thoảng vẫn gặp khó khăn trong việc nhận diện không gian bảng, dẫn đến việc thiếu sót một vài thông số phụ khi chuyển đổi thành vector.

## 4.3. Hướng phát triển trong tương lai
Để biến hệ thống từ một bản thử nghiệm trở thành một sản phẩm có khả năng triển khai thực tế, hệ thống cần được định hướng phát triển thêm các tính năng nâng cao nhằm khắc phục những rào cản nêu trên.

Định hướng quan trọng là việc nghiên cứu chuyển đổi sang sử dụng các mô hình sinh ngôn ngữ mã nguồn mở. Bằng cách thiết lập máy chủ tính toán vật lý tại trường để chạy các mô hình này, hệ thống sẽ tăng cường khả năng tự chủ về hạ tầng công nghệ, giảm thiểu sự phụ thuộc vào kết nối mạng quốc tế và nâng cao tính bảo mật cho cơ sở dữ liệu.

Nhằm giải quyết bài toán tin nhắn phân mảnh, hệ thống cần tích hợp cơ chế hàng đợi chờ. Khi nhận được tín hiệu từ người dùng, hệ thống sẽ tạm hoãn một khoảng thời gian ngắn để gộp các tin nhắn lẻ tẻ thành một truy vấn hoàn chỉnh trước khi chuyển giao cho mô hình xử lý. Kết hợp với kỹ thuật tự động viết lại truy vấn dựa trên ngữ cảnh, phương pháp này sẽ giúp tối ưu hóa số lượng yêu cầu gửi lên máy chủ và duy trì mạch hội thoại một cách tự nhiên nhất.

Song song đó, hệ thống có thể mở rộng các phương thức tương tác để đa dạng hóa trải nghiệm người dùng. Việc tích hợp công nghệ nhận dạng giọng nói sẽ cho phép học sinh gửi tin nhắn thoại trực tiếp qua Zalo, mang lại trải nghiệm tiện lợi như đang gọi điện thoại trực tiếp với tư vấn viên. Hơn thế nữa, việc phát triển tính năng thông báo đẩy chủ động sẽ giúp trợ lý ảo hỗ trợ nhắc nhở thí sinh về lịch nộp hồ sơ, ngày thi năng lực và các mốc thời gian quan trọng khác trong kỳ tuyển sinh.
