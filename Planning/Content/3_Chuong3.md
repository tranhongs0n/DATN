# CHƯƠNG 3: TRIỂN KHAI, THỬ NGHIỆM VÀ ĐÁNH GIÁ

## 3.1. Quá trình thu thập và chuẩn bị dữ liệu
Triển khai hệ thống RAG đòi hỏi một quy trình xử lý dữ liệu đầu vào cực kỳ chặt chẽ. Hệ thống được xây dựng bằng ngôn ngữ lập trình Python, tận dụng sức mạnh của bộ khung LangChain để điều phối các tác vụ cốt lõi.

### 3.1.1. Kỹ thuật thu thập dữ liệu
Kho dữ liệu tuyển sinh bao gồm hai nguồn chính là văn bản trên website đại học và các tệp tin lưu trữ định dạng PDF và Word. Để xử lý nguồn website, hệ thống tích hợp bộ công cụ Web Scraper để cào thông tin tự động từ các trang tin tức tuyển sinh, tập trung bóc tách các thẻ HTML chứa nội dung trọng tâm và loại bỏ các thành phần quảng cáo. Đối với nguồn dữ liệu tệp tin, công cụ Document Loader được lập trình để đọc và trích xuất chữ viết từ các bản ghi quyết định tuyển sinh. Quá trình này được tối ưu hóa nhằm đảm bảo không làm thất thoát các dữ liệu quan trọng nằm ẩn trong các biểu đồ hay bảng điểm chuẩn phức tạp.

### 3.1.2. Phân mảnh văn bản và mã hóa
Điểm đột phá trong khâu xử lý dữ liệu nằm ở kỹ thuật phân mảnh thông minh thông qua thư viện Text Splitters. Thay vì cắt văn bản một cách cơ học theo số lượng ký tự, hệ thống nhận diện cấu trúc ngữ nghĩa để đảm bảo mỗi mảnh văn bản đều trọn vẹn ý nghĩa. Đặc biệt, hệ thống tự động gán siêu dữ liệu cho từng mảnh văn bản bao gồm năm ban hành và đối tượng áp dụng. Sau khi được phân nhỏ, các mảnh văn bản giàu ngữ cảnh này được đưa qua mô hình nhúng thế hệ mới gemini-embedding-2 do Google cung cấp. Mô hình nhúng này chịu trách nhiệm chuyển đổi toàn bộ ngôn ngữ tự nhiên thành các vector toán học đa chiều, tạo nền tảng vững chắc cho quá trình tìm kiếm tương đồng sau này.

## 3.2. Cài đặt hệ thống lõi FastAPI và Giao diện quản trị
Trái tim của hệ thống là máy chủ xử lý trung tâm được xây dựng trên nền tảng FastAPI, đảm bảo khả năng xử lý bất đồng bộ với tốc độ cực cao.

### 3.2.1. Triển khai Cơ sở dữ liệu ChromaDB
Để lưu trữ hàng ngàn vector toán học sinh ra từ bước mã hóa, hệ thống tích hợp cơ sở dữ liệu ChromaDB hoạt động hoàn toàn độc lập tại môi trường cục bộ. Cơ sở dữ liệu này được tinh chỉnh để thực thi các thuật toán tìm kiếm khoảng cách vector siêu tốc, cho phép máy chủ truy xuất những mảnh tài liệu có độ tương đồng cao nhất với câu hỏi của người dùng chỉ trong một phần nghìn giây. Việc lưu trữ cục bộ cũng giúp hệ thống hoàn toàn chủ động về mặt bảo mật và không bị phụ thuộc vào các dịch vụ lưu trữ đám mây đắt đỏ.

### 3.2.2. Kết nối mô hình sinh ngôn ngữ và thiết kế bộ chỉ thị
Sức mạnh sinh văn bản của hệ thống được hậu thuẫn bởi mô hình sinh ngôn ngữ lớn gemini-3-flash-preview. Đây là phiên bản mô hình được Google tối ưu hóa đặc biệt cho tốc độ phản hồi tức thời. Để kiểm soát chặt chẽ đầu ra của mô hình, hệ thống áp dụng kỹ thuật thiết kế bộ chỉ thị nâng cao. Bộ chỉ thị này bao bọc câu hỏi của người dùng và các mảnh tài liệu tìm được vào một khuôn khổ mệnh lệnh khắt khe. Nó ép buộc mô hình chỉ được phép tổng hợp câu trả lời dựa trên tài liệu được cung cấp, cấm tuyệt đối hành vi tự suy diễn và bắt buộc phải cảnh báo người dùng nếu dữ liệu đầu vào không đủ để đưa ra kết luận.

### 3.2.3. Bảng điều khiển quản trị
Nhằm hỗ trợ ban tuyển sinh vận hành hệ thống một cách chủ động, một bảng điều khiển quản trị nền Web được phát triển thông qua các giao thức API của FastAPI. Giao diện này cung cấp một không gian thao tác thân thiện để cán bộ tuyển sinh trực tiếp kéo thả các tệp tin quy chế mới lên máy chủ. Hệ thống sẽ tự động gọi các hàm xử lý nền tảng để băm nhỏ, mã hóa và cập nhật vào ChromaDB. Bên cạnh đó, bảng điều khiển còn cung cấp các chỉ số thống kê theo thời gian thực về số lượng tài liệu đã lập chỉ mục và dung lượng cơ sở dữ liệu hiện hành.

## 3.3. Tích hợp Zalo Bot
Giao diện tiếp xúc duy nhất với thí sinh và phụ huynh là ứng dụng Zalo Bot. Kiến trúc tích hợp được thiết kế để tận dụng tối đa hệ sinh thái Zalo, mang lại trải nghiệm tra cứu tự nhiên nhất.

### 3.3.1. Xây dựng kênh tiếp nhận tín hiệu
Máy chủ FastAPI được cấu hình mở một cổng giao tiếp webhook chuyên biệt để lắng nghe mọi sự kiện diễn ra trên kênh Zalo Official Account. Khi học sinh gửi tin nhắn, tín hiệu lập tức được Zalo đẩy về máy chủ của trường. Tại đây, lớp API trung gian sẽ bóc tách nội dung tin nhắn, giải mã danh tính người dùng và đẩy vào hàng đợi của hệ thống xử lý cốt lõi. Sau khi mô hình sinh ngôn ngữ hoàn tất câu trả lời, máy chủ sẽ định dạng lại văn bản và gọi ngược Zalo API để trả tin nhắn về màn hình điện thoại của thí sinh.

### 3.3.2. Quản lý lịch sử hội thoại
Để mô phỏng một cuộc trò chuyện giống người thật, hệ thống được lập trình một phân hệ quản lý ngữ cảnh tạm thời. Mỗi khi nhận được câu hỏi mới, máy chủ sẽ trích xuất lịch sử các câu hỏi và câu trả lời liền kề trước đó của cùng một học sinh. Toàn bộ chuỗi hội thoại này được hệ thống tiền xử lý để làm rõ nghĩa cho câu hỏi hiện tại trước khi mang đi đối chiếu vector. Nhờ đó, học sinh có thể hỏi đáp liên tục nhiều lượt về cùng một ngành học mà không cần nhắc lại tên ngành.

### 3.3.3. Thiết kế giao diện hiển thị bản địa
Thay vì phản hồi những khối văn bản dài dòng, hệ thống áp dụng linh hoạt các cấu trúc hiển thị bản địa của Zalo. Danh sách các ngành đào tạo và biểu đồ điểm chuẩn được hệ thống đóng gói thành các thẻ hiển thị trượt ngang, giúp học sinh dễ dàng lướt xem trên màn hình cảm ứng. Cùng với đó, các nút tương tác nhanh được chèn khéo léo vào cuối mỗi luồng tư vấn, mời gọi người dùng để lại phản hồi đánh giá nhằm giúp hệ thống đo lường chất lượng một cách tự động.

## 3.4. Xây dựng kịch bản thử nghiệm và kết quả
Quá trình thử nghiệm được tiến hành nghiêm ngặt nhằm đánh giá năng lực thực sự của hệ thống trước khi đưa vào vận hành chính thức.

### 3.4.1. Ma trận kịch bản thử nghiệm
Hệ thống phải đối mặt với một ma trận gồm ba nhóm câu hỏi phân cấp theo độ khó. Nhóm câu hỏi cơ bản tập trung vào các truy vấn hỏi đáp trực tiếp về mã ngành và chỉ tiêu. Nhóm thứ hai mô phỏng phong cách ngôn ngữ đời thường, cố tình sử dụng từ lóng và viết tắt để thử thách khả năng bắt lỗi của mô hình nhúng. Nhóm cuối cùng là các câu hỏi bẫy chứa nhiều điều kiện đan chéo, đòi hỏi mô hình sinh ngôn ngữ phải vận dụng tư duy logic để đưa ra câu trả lời chứa đầy đủ các điều kiện tiên quyết.

### 3.4.2. Phân tích kết quả thực tế
Kết quả thử nghiệm cho thấy sự kết hợp giữa mô hình nhúng chuyên biệt và bộ chỉ thị nghiêm ngặt đã phát huy hiệu quả xuất sắc. Hệ thống không chỉ trả lời chính xác các câu hỏi có cấu trúc phức tạp mà còn thể hiện khả năng duy trì ngữ cảnh hội thoại xuyên suốt nhiều lượt chat. Về mặt hiệu năng, việc ứng dụng mô hình gemini-3-flash-preview đã rút ngắn đáng kể thời gian sinh văn bản, mang lại tốc độ phản hồi gần như ngay lập tức, đáp ứng hoàn hảo tiêu chuẩn thời gian thực của các ứng dụng nhắn tin tức thời.

## 3.5. Đánh giá ưu điểm và hạn chế
Thông qua quá trình triển khai và đo lường thực tiễn, hệ thống trợ lý ảo đã chứng minh được tính khả thi và giá trị ứng dụng cao, mặc dù vẫn còn một số điểm cần tiếp tục hoàn thiện.

Về mặt ưu điểm, hệ thống đã giải quyết triệt để vấn đề phân tán thông tin và mất mát ngữ cảnh thường gặp ở các công cụ tìm kiếm truyền thống. Bằng cách ứng dụng cơ sở dữ liệu vector tiên tiến và cơ chế phân mảnh thông minh, trợ lý ảo có khả năng mang đến các câu trả lời mang tính cá nhân hóa và đạt độ tin cậy tuyệt đối. Giao diện Zalo Bot thân thiện cũng phá bỏ mọi rào cản kỹ thuật đối với người sử dụng.

Về mặt hạn chế, do sự phụ thuộc vào giao diện lập trình ứng dụng của Google, hệ thống có thể gặp giới hạn về băng thông nếu lượng thí sinh truy cập tăng đột biến trong mùa tuyển sinh cao điểm. Ngoài ra, phân hệ trích xuất tài liệu từ hình ảnh vẫn cần được tinh chỉnh thêm để đọc chính xác các biểu đồ có thiết kế đồ họa quá phức tạp. Tuy nhiên, kiến trúc hệ thống hiện tại được thiết kế theo hướng mở, sẵn sàng cho các đợt nâng cấp và thay thế mô hình trong tương lai nhằm vượt qua các giới hạn này.
