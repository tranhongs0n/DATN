# CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ

## 4.1. Thiết kế phương pháp đánh giá

Để xác thực tính khả thi và đo lường mức độ hoàn thiện của hệ thống trợ lý ảo trước khi đưa vào môi trường thực tế, một quy trình đánh giá nghiêm ngặt được thiết lập. Quá trình này không chỉ dừng lại ở việc hệ thống có trả lời được hay không, mà còn phân tích sâu vào cách hệ thống truy xuất dữ liệu và tổng hợp ngôn ngữ dưới nhiều tình huống giao tiếp khác nhau.

### 4.1.1. Bộ câu hỏi kiểm thử 5 nhóm
Hệ thống được thử thách thông qua một ma trận kiểm thử bao gồm 5 nhóm câu hỏi, được thiết kế để bao quát toàn bộ phổ tình huống mà một thí sinh có thể đưa ra trong thực tế:

- Nhóm 1 tập trung vào tra cứu thông tin cơ bản, gồm các câu hỏi trực diện về mã ngành, chỉ tiêu, điểm chuẩn và lịch xét tuyển. Mục đích nhằm đánh giá khả năng truy xuất chính xác các thông tin có cấu trúc.
- Nhóm 2 xoay quanh ngôn ngữ thí sinh thực tế, chứa các câu hỏi cố tình sử dụng từ viết tắt, không dấu và từ lóng phổ biến trên mạng xã hội (ví dụ: "diem chuan thuy loi 2025", "nganh cntt lay bn diem"). Mục đích nhằm đo lường năng lực của mô hình nhúng trong việc thấu hiểu ngữ nghĩa tiếng Việt không chuẩn mực.
- Nhóm 3 thử thách hệ thống với câu hỏi phức tạp có điều kiện chéo, yêu cầu người dùng cung cấp một bộ hồ sơ giả định và hỏi về khả năng trúng tuyển (ví dụ: "Em tốt nghiệp năm 2022, có IELTS 6.5, điểm bạ khối A00 là 23, vậy có đủ điều kiện xét tuyển thẳng ngành CNTT không?"). Mục đích nhằm đánh giá khả năng mô hình tổng hợp thông tin từ nhiều mảnh dữ liệu khác nhau để đưa ra kết luận logic.
- Nhóm 4 đánh giá bằng câu hỏi bẫy ngoài phạm vi, chứa các câu hỏi không thuộc thẩm quyền của trường hoặc hoàn toàn không có trong cơ sở dữ liệu (ví dụ: "Học phí của Đại học Bách Khoa năm nay là bao nhiêu?"). Mục đích nhằm kiểm tra năng lực chống ảo giác và sự tuân thủ nghiêm ngặt đối với bộ chỉ thị từ chối trả lời.
- Nhóm 5 đề cập đến câu hỏi đa bậc đào tạo, đưa ra các truy vấn liên quan đến bậc Thạc sĩ, Tiến sĩ hoặc các chương trình liên kết quốc tế. Mục đích nhằm xác thực khả năng phân vùng không gian tìm kiếm, đảm bảo hệ thống không lấy nhầm quy chế của đại học để tư vấn cho nghiên cứu sinh.

### 4.1.2. Các tiêu chí đánh giá đo lường
Việc đánh giá được lượng hóa thông qua 5 tiêu chuẩn chính xác:

- Độ bao phủ ngữ cảnh (Context Recall) kiểm tra xem hệ thống có trích xuất đủ tất cả các thông tin cần thiết từ cơ sở tri thức để giải quyết trọn vẹn câu hỏi hay không. Mục tiêu đặt ra là đạt từ 0.8 trở lên.
- Độ chuẩn xác ngữ cảnh (Context Precision) đo lường xem các mảnh văn bản mà cơ sở dữ liệu vector trả về có thực sự chứa nội dung hữu ích hay bị lẫn nhiều thông tin nhiễu. Mục tiêu đặt ra là đạt từ 0.8 trở lên.
- Độ liên quan của câu trả lời (Answer Relevance) đánh giá mức độ đi thẳng vào vấn đề của câu trả lời, không lan man hay lạc đề so với câu hỏi gốc. Mục tiêu đặt ra là đạt từ 0.8 trở lên.
- Độ trung thành (Faithfulness) đánh giá việc phản hồi sinh ra có bám sát và giới hạn hoàn toàn trong phạm vi tài liệu được truy xuất hay không, qua đó đo lường khả năng triệt tiêu ảo giác. Đây là tiêu chí sống còn, mục tiêu đặt ra phải tiệm cận 1.0.
- Độ trễ phản hồi được tính bằng giây, từ lúc hệ thống tiếp nhận tin nhắn cuối cùng đến lúc luồng phản hồi đầu tiên xuất hiện trên giao diện.
- Tỉ lệ từ chối chuẩn xác phản ánh khả năng hệ thống nhận diện đúng các câu hỏi nằm ngoài cơ sở tri thức và đưa ra thông báo từ chối lịch sự thay vì cố gắng suy diễn.
- Đánh giá trải nghiệm người dùng (MOS - Mean Opinion Score) sử dụng thang đo 5 mức độ (từ 1: Rất không hài lòng đến 5: Rất hài lòng) để thu thập phản hồi chủ quan của thí sinh đối với chất lượng giao diện, độ rõ ràng của câu trả lời và tính hữu ích.

## 4.2. Kết quả thử nghiệm

Quá trình thử nghiệm được tiến hành trên 250 câu hỏi giả định phân bổ đều cho 5 nhóm, ghi nhận lại kết quả thực tế từ hệ thống mô phỏng.

Bảng 4.1: Tổng hợp kết quả thử nghiệm theo các nhóm kiểm thử

| Nhóm kiểm thử | Context Recall | Context Precision | Answer Relevance | Faithfulness | Độ trễ trung bình |
|---------------|----------------|-------------------|------------------|--------------|-------------------|
| Nhóm 1: Cơ bản | 0.98 | 0.95 | 0.96 | 1.00 | 2.1 giây |
| Nhóm 2: Ngôn ngữ thực tế | 0.92 | 0.89 | 0.88 | 1.00 | 2.3 giây |
| Nhóm 3: Điều kiện chéo | 0.81 | 0.78 | 0.85 | 0.96 | 3.5 giây |
| Nhóm 4: Ngoài phạm vi | N/A | N/A | 0.98 | 0.98 | 1.8 giây |
| Nhóm 5: Đa bậc đào tạo | 0.90 | 0.88 | 0.92 | 0.98 | 2.5 giây |

Dưới đây là một số ví dụ minh họa chi tiết về chất lượng hội thoại thực tế được trích xuất từ các nhóm kiểm thử.

Với nhóm 2 kiểm tra ngôn ngữ thực tế, hệ thống đã xử lý thành công cách nói tắt của thí sinh. Ví dụ, khi học sinh hỏi: "ad cho e hoi nganh tmdt diem chuan 2024 bn a", trợ lý ảo phản hồi chính xác: "Ngành Thương mại điện tử (Mã ngành: 7340122E) của Trường Đại học Thủy lợi có mức điểm chuẩn năm 2024 là 25.20 điểm (đối với phương thức xét tuyển theo điểm thi THPT)."

Với nhóm 3 về điều kiện chéo, hệ thống đôi khi gặp lỗi thiếu dữ kiện do không thể liên kết nhiều mảnh thông tin phức tạp. Ví dụ, khi học sinh hỏi: "Em được 24 điểm khối A00, có chứng chỉ IELTS 5.5, em có đủ điều kiện xét tuyển thẳng vào ngành CNTT không?", trợ lý ảo trả lời: "Chào bạn, theo Đề án tuyển sinh, để xét tuyển thẳng kết hợp chứng chỉ ngoại ngữ, bạn cần có IELTS từ 5.0 trở lên. Với IELTS 5.5, bạn đã đạt yêu cầu về ngoại ngữ. Tuy nhiên, hệ thống chưa có thông tin về ngưỡng điểm sàn học bạ/thi THPT kết hợp năm nay. Bạn vui lòng đợi thông báo mới nhất nhé."

Với nhóm 4 về các bẫy ngoài phạm vi, hệ thống chống ảo giác thành công. Chẳng hạn, trước câu hỏi: "Cho mình hỏi học phí ngành Kỹ thuật phần mềm bên Đại học Công nghệ là bao nhiêu?", trợ lý ảo đưa ra phản hồi an toàn: "Hệ thống hiện chưa có thông tin về vấn đề này. Tôi chỉ hỗ trợ cung cấp thông tin tuyển sinh chính thức của Trường Đại học Thủy lợi. Bạn có cần tư vấn về ngành Kỹ thuật phần mềm của trường không?"

Về mặt hiệu năng máy chủ, hệ thống đạt độ trễ trung bình toàn dải ở mức 2.4 giây cho mỗi truy vấn, hoàn toàn đáp ứng được tính thời gian thực trên giao diện Zalo. Thông lượng hệ thống hoạt động ổn định khi xử lý dưới 50 yêu cầu đồng thời. Tuy nhiên, khi cố tình thực hiện thử nghiệm tăng tải lên mức 200 yêu cầu đồng thời, hệ thống bắt đầu ghi nhận mã lỗi 429 từ máy chủ Google do chạm ngưỡng giới hạn băng thông giao tiếp ứng dụng, buộc hệ thống phải kích hoạt chế độ hàng đợi chờ 30 giây làm tăng đột biến độ trễ đối với người dùng cuối.

Ngoài các thông số đo lường hệ thống tự động, quá trình thử nghiệm còn được mở rộng với sự tham gia của 50 học sinh trung học phổ thông thao tác trực tiếp trên ứng dụng Zalo. Kết quả đánh giá theo thang đo MOS (Mean Opinion Score) cho thấy điểm trung bình đạt mức 4.2/5. Nhóm người dùng thử nghiệm đánh giá rất cao tốc độ phản hồi tức thời và cách hệ thống tự động định dạng thông tin điểm chuẩn một cách mạch lạc, trực quan.

## 4.3. Phân tích kết quả và thảo luận

Từ các số liệu lượng hóa và phản hồi thực tế, bức tranh toàn cảnh về năng lực của hệ thống đã được khắc họa rõ nét. Bức tranh này chỉ ra ranh giới rõ ràng giữa những tác vụ mà kiến trúc máy học hiện tại có thể giải quyết triệt để và những rào cản kỹ thuật vẫn đang tồn tại.

### 4.3.1. Những điểm vượt trội của hệ thống
Hệ thống chứng minh năng lực xuất sắc ở hai khía cạnh vận hành cốt lõi. Khía cạnh đầu tiên là khả năng thấu hiểu ngôn ngữ tự nhiên không chuẩn mực của thí sinh. Việc ứng dụng mô hình nhúng không gian đa chiều giúp hệ thống vượt qua rào cản sai chính tả hay từ viết tắt. Thay vì rà quét từng ký tự đơn lẻ, thuật toán biến đổi câu hỏi viết tắt thành một tọa độ vector bao hàm ý nghĩa tổng quát, từ đó trích xuất chính xác mảnh tài liệu chứa điểm chuẩn bất chấp cấu trúc ngữ pháp sai lệch ban đầu. Khía cạnh vượt trội thứ hai là năng lực phòng chống hiện tượng sinh ảo giác thông tin. Thử nghiệm ở nhóm câu hỏi ngoài phạm vi đạt tỉ lệ từ chối đúng lên đến 98%. Triết lý thiết kế bộ chỉ thị ép buộc chặt chẽ đã phát huy tác dụng tối đa; mô hình ngôn ngữ đã bị tước bỏ hoàn toàn quyền tự do sáng tạo nội dung, đảm bảo hệ thống luôn trả về thông báo từ chối lịch sự khi không có cơ sở dữ liệu hợp lệ.

### 4.3.2. Những rào cản và điểm yếu cần khắc phục
Bên cạnh những điểm sáng, hệ thống vẫn bộc lộ một số giới hạn rõ rệt khi xử lý các truy vấn có tính điều kiện chéo phức tạp. Sự sụt giảm độ chính xác ở nhóm câu hỏi này xuất phát từ hiện tượng mất ngữ cảnh khi phân mảnh văn bản. Các bản quy chế xét tuyển thẳng thường chứa những mệnh đề trải dài qua nhiều trang giấy. Việc áp dụng thuật toán cắt mảnh cố định đã vô tình chặt đứt một luồng thông tin liên tục thành các khối riêng lẻ. Khi quá trình truy vấn chỉ bốc tách được một nửa mệnh đề, mô hình sinh ngôn ngữ lập tức bị thiếu hụt dữ kiện để đưa ra kết luận tư vấn chính xác.

Bên cạnh đó, sự suy thoái cấu trúc bảng biểu do định dạng nguồn quá phức tạp cũng đóng góp đáng kể vào sai số hệ thống. Các bộ tài liệu PDF chứa bảng lồng ghép nhiều cột thường làm rối loạn công cụ trích xuất văn bản thô, khiến mã ngành và mức điểm tương ứng bị xô lệch khoảng trắng. Khi tiến hành nhúng vector, sự xô lệch cấu trúc này trực tiếp làm đứt gãy tính liên kết ngữ nghĩa giữa tên chuyên ngành và điểm số.

Một điểm yếu khác đang tồn tại là vấn đề xung đột siêu dữ liệu về mặt thời gian. Quá trình thu thập thông báo tự động từ trang chủ đôi khi gặp phải các bài đăng không đính kèm niên khóa rõ ràng ở tiêu đề. Hậu quả là hệ thống mã hóa đoạn văn bản với bộ siêu dữ liệu khuyết thiếu, dẫn đến hiện tượng thuật toán tìm kiếm lấy nhầm thông tin điều chỉnh chỉ tiêu của các năm học cũ để tư vấn cho mùa tuyển sinh hiện tại. 

Nhìn chung tổng thể, giải pháp RAG được xây dựng thể hiện điểm mạnh tuyệt đối về độ an toàn thông tin và sự thân thiện trong giao tiếp tự nhiên. Hệ thống đã đạt mức sẵn sàng cao để đảm nhận vị trí tư vấn viên vòng ngoài, giải đáp nhanh các thắc mắc lặp đi lặp lại. Mặc dù vậy, đối với các trường hợp hồ sơ đặc thù yêu cầu đối chiếu chéo nhiều tiêu chí, việc tích hợp chức năng chuyển tiếp cuộc trò chuyện thẳng đến cán bộ tuyển sinh con người vẫn là một chốt chặn bắt buộc để bảo vệ quyền lợi tối đa cho thí sinh.

## 4.4. Demo và minh họa hoạt động hệ thống

Trải nghiệm thực tế của toàn bộ hệ thống được hội tụ qua hai không gian giao diện tương tác độc lập.

Trên nền tảng ứng dụng Zalo, giao diện học sinh được thiết kế theo dạng hội thoại trực quan. Ngay khi người dùng tìm kiếm và nhắn tin cho trang thông tin chính thức của trường, trợ lý ảo lập tức phản hồi lời chào định hướng. Các câu trả lời từ chatbot không hiển thị toàn bộ cùng một lúc mà được truyền tải trực tiếp từng cụm từ lên màn hình điện thoại, tạo hiệu ứng thị giác mượt mà và giảm thiểu sự sốt ruột của người chờ. Đặc biệt, khi danh sách ngành học hoặc các mốc thời gian được truy xuất, chatbot không liệt kê thành đoạn văn bản dài mà tự tự động định dạng thành các gạch đầu dòng có khoảng trắng rõ ràng, trong đó các thông số quan trọng như điểm chuẩn và mã ngành tự động được in đậm nổi bật. Ngay dưới mỗi luồng giải đáp, hệ thống tích hợp sẵn thang đo đánh giá MOS, cho phép học sinh chấm điểm chất lượng câu trả lời từ 1 đến 5 sao chỉ với một cú chạm.

Chuyển sang góc độ vận hành, giao diện điều khiển trung tâm nền tảng Web mang đến một bảng điều khiển mang tính kỹ thuật cao. Tại trung tâm màn hình là một biểu đồ thống kê trực tiếp tiến trình xây dựng cơ sở dữ liệu, biểu diễn chi tiết số lượng tài liệu đã nạp và số lượng vector đang lưu trữ. Phân hệ nạp dữ liệu nằm bên phải hỗ trợ cán bộ kéo thả các tệp PDF hoặc DOCX trực tiếp từ máy tính. Ngay khi tệp được thả vào vùng xử lý, một thanh tiến trình tự động chạy thông báo trạng thái chia mảnh văn bản và đồng bộ hóa vector. Với các hình ảnh đồ họa chứa lịch thi, quản trị viên sử dụng khu vực chuyển đổi trí tuệ nhân tạo; chỉ mất vài giây, toàn bộ chữ trên hình ảnh được bóc tách và đóng gói lại thành tài liệu chuẩn, sẵn sàng cung cấp tri thức mới cho trợ lý ảo mà không cần gõ lại thủ công. Quy trình khép kín này đảm bảo tính năng động của kho tri thức, giữ cho trợ lý ảo luôn được trang bị thông tin tuyển sinh mới nhất trong từng phút vận hành.
