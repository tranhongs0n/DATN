# PHẦN MỞ ĐẦU

## 1. Lý do chọn đề tài
Trong những năm gần đây, sự bùng nổ của trí tuệ nhân tạo đã làm thay đổi mạnh mẽ cách thức con người tương tác và tìm kiếm thông tin. Đặc biệt trong lĩnh vực giáo dục đại học, công tác tuyển sinh luôn là một hoạt động trọng điểm thu hút sự quan tâm của đông đảo học sinh và phụ huynh. Tại Trường Đại học Thủy Lợi, mỗi kỳ tuyển sinh thường tiếp nhận hàng ngàn lượt truy cập, tin nhắn và cuộc gọi yêu cầu tư vấn về các ngành học, điểm chuẩn, quy chế xét tuyển cũng như học phí. 

Tuy nhiên, lượng thông tin tuyển sinh này thường rất đồ sộ và được phân tán trên nhiều kênh khác nhau. Điều này không chỉ gây khó khăn cho thí sinh trong việc tra cứu nhanh chóng mà còn tạo áp lực rất lớn lên đội ngũ tư vấn viên. Việc hỗ trợ giải đáp bằng sức người gặp nhiều giới hạn về mặt thời gian, nhân lực và khó có thể duy trì tần suất phản hồi tức thì 24/7. Thực tế này đòi hỏi một giải pháp công nghệ tự động hóa, có khả năng thấu hiểu ngôn ngữ tự nhiên và cung cấp câu trả lời chính xác dựa trên nguồn dữ liệu đặc thù của nhà trường.

Để giải quyết bài toán trên, việc ứng dụng các LLM kết hợp với kỹ thuật RAG đang nổi lên như một hướng tiếp cận tối ưu. Khác với các hệ thống truyền thống vốn khô khan và cứng nhắc, RAG cho phép hệ thống truy xuất thông tin trực tiếp từ các tài liệu chính thống, sau đó sử dụng sức mạnh ngôn ngữ của các LLM để tổng hợp thành câu trả lời tự nhiên nhất. Sự kết hợp này giúp hạn chế tình trạng sinh thông tin sai lệch thường gặp ở AI, đảm bảo tính chính xác cho thông tin tuyển sinh. Nhận thấy tiềm năng to lớn đó, em quyết định thực hiện đề tài: **"Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG"**. Hệ thống được kỳ vọng sẽ tích hợp liền mạch lên nền tảng Zalo Bot, mang lại một kênh tư vấn thông minh và hiệu quả cho người dùng.

## 2. Mục tiêu nghiên cứu
Mục tiêu cốt lõi của đề tài là xây dựng thành công một hệ thống trợ lý ảo, đóng vai trò như một tư vấn viên tuyển sinh túc trực 24/7 cho Trường Đại học Thủy Lợi. Để đạt được mục tiêu này, đề tài hướng tới các mục tiêu cụ thể sau đây. 

Về nền tảng lý thuyết, đề tài tập trung nghiên cứu cơ chế hoạt động của kỹ thuật RAG và các LLM hiện đại để nắm vững phương pháp thiết kế hệ thống. Dựa trên nền tảng đó, một CSTT chuyên biệt sẽ được xây dựng nhằm xử lý dữ liệu thô từ các tài liệu tuyển sinh chính thức, đồng thời lưu trữ dưới dạng vector để phục vụ quá trình truy xuất ngữ nghĩa.

Sản phẩm đầu ra đòi hỏi phải là một trợ lý ảo hoàn chỉnh, có khả năng nhận diện ý định của người dùng, trích xuất thông tin từ CSTT và sinh ra câu trả lời tự nhiên, bám sát ngữ cảnh câu hỏi. Nhằm tối ưu hóa tính tiện dụng và khả năng tiếp cận, hệ thống sẽ được triển khai và tích hợp trực tiếp lên nền tảng nhắn tin phổ biến là Zalo Bot.

## 3. Đối tượng và phạm vi nghiên cứu
Đối tượng nghiên cứu của đề tài xoay quanh các công nghệ nền tảng tạo nên hệ thống hỏi đáp thông minh, bao gồm kỹ thuật RAG, DB dạng vector và các LLM. Bên cạnh đó, nhu cầu tìm kiếm thông tin của học sinh và phụ huynh trong giai đoạn tìm hiểu thông tin tuyển sinh cũng là một đối tượng nghiên cứu quan trọng để tối ưu hóa trải nghiệm tương tác.

Về phạm vi nghiên cứu, đối với khía cạnh dữ liệu, đề tài chỉ giới hạn trong các văn bản, quy chế, thông báo điểm chuẩn và thông tin ngành học liên quan trực tiếp đến công tác tuyển sinh của Trường Đại học Thủy Lợi. Về khía cạnh công nghệ, đề tài tập trung vào việc phát triển luồng xử lý RAG backend, đồng thời xây dựng giao diện người dùng frontend tích hợp duy nhất trên nền tảng Zalo Bot để đảm bảo tập trung tối đa vào chất lượng ứng dụng.

## 4. Phương pháp nghiên cứu
Để hoàn thành các mục tiêu đã đề ra, đồ án áp dụng kết hợp chặt chẽ ba phương pháp nghiên cứu chính. 

Phương pháp nghiên cứu lý thuyết được sử dụng nhằm thu thập và phân tích các tài liệu khoa học liên quan đến NLP, các LLM và đặc biệt là kiến trúc RAG. Quá trình này giúp xây dựng nền tảng kiến thức vững chắc làm cơ sở cho các quyết định thiết kế.

Song song đó, phương pháp nghiên cứu thực nghiệm được triển khai thông qua các bài kiểm thử hiệu năng giữa các LLM khác nhau. Các thử nghiệm này đóng vai trò quan trọng trong việc đánh giá độ chính xác của các mô hình nhúng và tìm ra cấu hình DB dạng vector phù hợp nhất, từ đó đo lường chất lượng câu trả lời cuối cùng sinh ra.

Phương pháp phát triển phần mềm được vận dụng xuyên suốt quá trình xây dựng sản phẩm thực tế. Đề tài tuân thủ quy trình phát triển phần mềm chuẩn mực từ bước phân tích yêu cầu, thiết kế kiến trúc hệ thống, lập trình API, cho đến giai đoạn tích hợp và kiểm thử giao diện Zalo Bot. Quá trình này đảm bảo hệ thống làm ra có tính ứng dụng cao và sẵn sàng vận hành trong thực tế.
