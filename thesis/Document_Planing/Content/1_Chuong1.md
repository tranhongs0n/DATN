# CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU

## 1.1. Tổng quan về trợ lý ảo và bài toán hỏi đáp tự động

Trong giai đoạn đầu ứng dụng thương mại, hệ thống trợ lý ảo chủ yếu hoạt động dựa trên kịch bản cứng. Kỹ sư phải xây dựng thủ công các cây quyết định phức tạp, định nghĩa từng nhánh hội thoại tương ứng với lựa chọn của người dùng. Mặc dù kiến trúc này dễ kiểm soát và đảm bảo tính chính xác tuyệt đối trong giới hạn kịch bản, kiến trúc này bộc lộ điểm yếu ở tính tĩnh tại. Hệ thống rơi vào bế tắc hoặc lặp vòng khi người dùng diễn đạt câu hỏi vượt ngoài luồng hoặc sử dụng từ lóng, biến thể ngôn ngữ mà lập trình viên chưa dự liệu trước.

Xử lý ngôn ngữ tự nhiên truyền thống cải thiện một phần tình trạng này thông qua cơ chế phân loại ý định và nhận diện thực thể. Các hệ thống như Dialogflow hay Rasa cho phép gán nhãn hàng ngàn câu mẫu để huấn luyện mô hình học máy nhận biết ý định người dùng. Giới hạn cốt lõi vẫn tồn tại khi chatbot không tự hiểu ngôn ngữ, mô hình chỉ so khớp xác suất văn bản đầu vào với các nhãn đã định nghĩa, và quan trọng nhất, hệ thống không có khả năng tự động sinh ra một câu trả lời mới mẻ. Phản hồi cuối cùng vẫn là những chuỗi văn bản tĩnh được soạn sẵn.

Sự bùng nổ của các LLM đánh dấu sự chuyển mình từ so khớp mẫu sang hiểu và sinh ngôn ngữ. Bài toán xử lý hội thoại chuyển sang một giai đoạn mới nhờ khả năng phân tích ngữ cảnh dài, suy luận logic cơ bản và sinh ngôn ngữ tự nhiên như con người.

Dựa trên cơ chế cốt lõi, trợ lý ảo hiện đại được phân thành ba kiến trúc chính:
- Kiến trúc truy xuất thuần túy tập trung tìm kiếm và trả về nguyên văn câu trả lời từ cơ sở dữ liệu đóng. Phương pháp này đảm bảo tính an toàn cao nhất nhưng kém linh hoạt, chỉ trả lời được khi câu hỏi trùng khớp cao với dữ liệu mẫu.
- Kiến trúc sinh văn bản tự động tạo phản hồi theo xác suất phân phối từ của LLM, cho phép hội thoại cực kỳ tự nhiên. Kiến trúc này tiềm ẩn rủi ro hiện tượng ảo giác, tức là sinh ra thông tin có vẻ hợp lý nhưng hoàn toàn sai sự thật do không có cơ chế đối chiếu.
- Kiến trúc lai kết hợp hai cơ chế này, sử dụng thông tin truy xuất chính xác từ cơ sở dữ liệu nội bộ làm ngữ cảnh nền tảng, sau đó cấp cho LLM để sinh phản hồi tự nhiên và chuẩn xác dựa trên ngữ cảnh đó.

Ứng dụng trợ lý ảo vào công tác tuyển sinh thuộc bài toán hỏi đáp miền tri thức chuyên biệt. Khác với hệ thống tán gẫu đa miền, hệ thống giáo dục đòi hỏi độ chính xác tuyệt đối. Tư vấn sai mã ngành, tổ hợp xét tuyển, hay điểm chuẩn có thể làm lỡ dở cơ hội học tập của thí sinh. Hệ thống bắt buộc phải có cơ sở đối chiếu tri thức nghiêm ngặt, đảm bảo mọi phản hồi được nội suy trực tiếp từ văn bản quy chế chính thống của trường.

## 1.2. LLM và kiến trúc Transformer

### 1.2.1. Kiến trúc Transformer và cơ chế tự chú ý
Các LLM hiện đại như GPT-4, Llama 3 hay Google Gemini đều được xây dựng dựa trên kiến trúc Transformer, lần đầu được giới thiệu bởi Vaswani và cộng sự (2017). Khác biệt cốt lõi của Transformer so với các mạng nơ-ron tuần tự truyền thống nằm ở cơ chế tự chú ý.

Thay vì xử lý từng từ một theo thứ tự, cơ chế tự chú ý tính toán song song mối quan hệ giữa tất cả các từ trong một chuỗi văn bản đầu vào. Quá trình này giúp mô hình đánh giá xem từ nào quan trọng hơn để tập trung xử lý khi phân tích một câu hỏi cụ thể. Nhờ tính toán song song ma trận, kiến trúc này giúp mô hình nắm bắt được ngữ cảnh từ khoảng cách cực xa trong văn bản và tăng đáng kể tốc độ huấn luyện do tận dụng tối đa sức mạnh của phần cứng.

### 1.2.2. Vòng đời huấn luyện của LLM
Để trở thành một trợ lý ảo thực thụ, một LLM phải trải qua ba giai đoạn huấn luyện cốt lõi:
- Tiền huấn luyện diễn ra khi mô hình được nạp một lượng dữ liệu khổng lồ từ Internet, Wikipedia, sách, báo. Mục tiêu của mô hình ở giai đoạn này chỉ đơn giản là dự đoán từ tiếp theo. Nhờ vậy, mô hình học được ngữ pháp, từ vựng và một lượng kiến thức tổng quát khổng lồ của nhân loại.
- Tinh chỉnh theo chỉ thị sử dụng khối lượng lớn dữ liệu hỏi đáp chất lượng cao do con người viết ra để dạy mô hình cách tương tác. Mô hình học cách phản hồi lại một câu lệnh thay vì chỉ viết tiếp văn bản một cách vô định.
- Học tăng cường từ phản hồi con người sử dụng thuật toán tối ưu hóa để thưởng hoặc phạt mô hình dựa trên thang điểm đánh giá của người dán nhãn. Giai đoạn này định hình hành vi an toàn, đảm bảo mô hình ưu tiên tính hữu ích, không thiên kiến và từ chối các yêu cầu vi phạm chính sách.

### 1.2.3. Hạn chế của LLM trong hệ thống tri thức đóng
Khi ứng dụng LLM nguyên bản vào hệ thống tuyển sinh, bài toán đối mặt với ba rào cản kỹ thuật lớn:
- Hiện tượng ảo giác là rủi ro nguy hiểm nhất. Bản chất của LLM là thống kê xác suất, LLM không có khái niệm biết hay không biết. Khi được hỏi về điểm chuẩn ngành Công nghệ thông tin của trường năm nay, nếu chưa từng thấy dữ liệu này, mô hình sẽ sinh ra một con số ngẫu nhiên vì cấu trúc đó hợp lý về mặt ngữ pháp, dù thông tin đó là hoàn toàn bịa đặt.
- Khuyết thiếu tri thức nội bộ khiến kiến thức của mô hình bị đóng băng tại thời điểm quá trình huấn luyện hoàn tất. Mô hình không thể biết các thông báo xét tuyển bổ sung vừa được ban hành. Việc tinh chỉnh lại toàn bộ mạng nơ-ron hàng trăm tỷ tham số mỗi khi có một thông báo mới là bất khả thi về mặt tài chính và thời gian.
- Giới hạn cửa sổ ngữ cảnh quy định số lượng từ tối đa mô hình có thể xử lý trong một lần gọi. Nếu nạp trực tiếp toàn bộ 86 tệp quy chế vào phần lệnh của mỗi lượt hỏi, bộ nhớ ngữ cảnh sẽ bị tràn. Ngay cả với các mô hình hiện đại hỗ trợ cửa sổ lớn, việc nạp quá nhiều văn bản rác sẽ gây nhiễu chú ý và đẩy chi phí lên mức không thể chi trả, kèm theo độ trễ xử lý tính bằng hàng chục giây.

## 1.3. Kỹ thuật sinh văn bản tăng cường truy xuất

### 1.3.1. Khái niệm và kiến trúc cốt lõi
Kỹ thuật RAG được công bố lần đầu bởi Patrick Lewis và cộng sự (2020) là giải pháp triệt để nhằm khắc phục hiện tượng ảo giác và hạn chế về dữ liệu tĩnh của LLM. Thay vì buộc mô hình phải ghi nhớ mọi thứ vào các trọng số mạng nơ-ron, RAG tách bạch tri thức ra một cơ sở dữ liệu độc lập.

Kiến trúc tổng quát vận hành qua hai pha chính: pha lập chỉ mục và pha truy xuất sinh văn bản.
- Pha lập chỉ mục diễn ra độc lập, trong đó tài liệu văn bản thô được làm sạch, cắt thành nhiều mảnh nhỏ, sau đó đưa qua một mô hình nhúng để biến đổi thành các vector đa chiều và lưu trữ tại Vector Database. Quá trình này có thể thực hiện định kỳ mỗi khi có tài liệu mới.
- Pha truy xuất khởi động khi câu hỏi người dùng được mô hình nhúng chuyển đổi thành vector. Cơ sở dữ liệu sử dụng thuật toán tìm kiếm khoảng cách gần nhất để trích xuất ra các mảnh tài liệu liên quan nhất. Các mảnh tài liệu này được đẩy vào ngữ cảnh cùng với câu hỏi gốc, ép LLM đóng vai trò đọc hiểu để rút trích câu trả lời từ chính đoạn văn bản vừa tìm được.

### 1.3.2. Tiền xử lý và các chiến lược phân mảnh
Phân mảnh là bước tiền xử lý mang tính quyết định đến độ chính xác của RAG. Nếu mảnh quá lớn, vector sinh ra sẽ bị loãng ngữ nghĩa, chứa nhiều thông tin nhiễu khiến truy xuất không tập trung. Nếu mảnh quá nhỏ, văn bản bị cắt vụn, mất đi bối cảnh khiến mô hình không đủ cơ sở để lập luận. 

Một số chiến lược phân mảnh phổ biến được xem xét trong nghiên cứu:
- Phân rã theo kích thước cố định (Fixed-size Chunking) tiến hành cắt tài liệu thành các khối có số ký tự bằng nhau. Phương pháp này nhanh, dễ triển khai nhưng làm gãy đôi các câu hoặc đoạn văn, phá vỡ cấu trúc ngữ nghĩa ngữ pháp.
- Phân rã đệ quy (Recursive Chunking) cố gắng giữ lại trọn vẹn đoạn văn và câu thông qua việc kiểm tra các ký tự phân tách. Thuật toán cắt theo đoạn văn trước, nếu đoạn văn vẫn dài hơn giới hạn, thuật toán sẽ đệ quy cắt theo câu, rồi cắt theo khoảng trắng. Phương pháp này cân bằng giữa hiệu suất và việc duy trì tính toàn vẹn của ngữ cảnh.
- Phân rã theo ngữ nghĩa (Semantic Chunking) ứng dụng các công cụ nhận diện cấu trúc tiêu đề để cô lập từng nội dung. Nhờ đó, thông tin của điểm khoản 1 và điểm khoản 2 không bị trộn lẫn vào nhau một cách cơ học.

Bảng dưới đây so sánh RAG với các phương pháp tối ưu LLM phổ biến:

| Tiêu chí | Tinh chỉnh mô hình | Kỹ thuật RAG | Thiết kế chỉ thị thuần |
|----------|--------------------|--------------|------------------------|
| Chi phí cập nhật tri thức | Rất cao | Rất thấp | Thấp |
| Khả năng truy xuất nguồn | Không | Có | Không |
| Yêu cầu phần cứng | Rất cao | Trung bình | Thấp |
| Đồng bộ dữ liệu | Rất chậm | Tức thời | Bị giới hạn bởi độ dài lệnh |

*Bảng 1.1: So sánh các phương pháp điều khiển LLM*

## 1.4. Vector Database và kỹ thuật nhúng

### 1.4.1. Không gian vector và độ đo khoảng cách
Kỹ thuật nhúng văn bản sử dụng các mạng nơ-ron chuyên biệt để ánh xạ chuỗi ký tự thành một vector liên tục trong không gian đa chiều. Đặc điểm vi diệu của không gian này là các khái niệm có ngữ nghĩa tương đồng sẽ có tọa độ gần nhau. 

Câu hỏi về thời gian thi đánh giá năng lực và lịch thi HSA hoàn toàn không có chung từ khóa, nhưng vector của chúng trong không gian ngữ nghĩa sẽ hội tụ gần nhau. Điều này giúp RAG vượt qua hoàn toàn giới hạn cứng nhắc của thuật toán tìm kiếm truyền thống vốn chỉ dựa trên so khớp từ khóa chính xác.

Quá trình truy xuất dữ liệu yêu cầu đo lường độ tương đồng giữa vector câu hỏi và các vector tài liệu. Độ đo phổ biến và hiệu quả nhất là khoảng cách Cosine, đánh giá góc giữa hai vector thay vì khoảng cách độ lớn của chúng. Giá trị Cosine dao động từ âm 1 đến 1. Giá trị càng tiệm cận 1 cho thấy hai văn bản có ngữ nghĩa càng giống nhau.

### 1.4.2. Thuật toán tìm kiếm xấp xỉ
Với một cơ sở dữ liệu có hàng triệu mảnh văn bản, việc tính toán khoảng cách từ câu hỏi đến toàn bộ các mảnh văn bản sẽ gây nghẽn cổ chai hệ thống. Các Vector Database hiện đại giải quyết bài toán này bằng thuật toán tìm kiếm lân cận gần đúng phân cấp mạng thế giới nhỏ.

Thuật toán xây dựng một cấu trúc đồ thị nhiều lớp. Ở lớp trên cùng, đồ thị rất thưa thớt, chỉ chứa một số ít các điểm tựa. Càng xuống lớp dưới, mật độ điểm càng dày đặc. Quá trình tìm kiếm bắt đầu từ lớp trên cùng, nhanh chóng nhảy các bước dài đến vùng chứa vector gần giống nhất, sau đó đi xuống lớp dưới để tinh chỉnh phạm vi. Cơ chế này giảm độ phức tạp truy xuất xuống mức thời gian logarit, đảm bảo hệ thống phản hồi dưới 50ms ngay cả khi kho dữ liệu lên tới hàng chục Gigabyte.

### 1.4.3. Đánh giá các hệ quản trị vector
Quá trình truy xuất dữ liệu tiếng Việt yêu cầu mô hình nhúng có năng lực xử lý đa ngôn ngữ xuất sắc. Đề tài chọn mô hình gemini-embedding-2 của Google, sinh ra vector 768 chiều. 
Để quản lý các vector này, hệ thống đã tiến hành kiểm thử hiệu năng độc lập trước khi lựa chọn. Môi trường đo lường sử dụng vi xử lý Intel Core i7, bộ nhớ 16GB, kết hợp mô phỏng 500 luồng truy vấn đồng thời:

| Hệ quản trị | Độ trễ đọc P95 | Tài nguyên tiêu thụ | Đặc điểm kiến trúc |
|-------------|----------------|---------------------|--------------------|
| Bảng Chroma | 14 ms | 250 MB | Chạy trực tiếp trên tiến trình nội bộ, độ trễ mạng bằng không. Rất phù hợp cho ứng dụng nguyên khối. |
| Bảng Pinecone | 85 ms | Sử dụng dịch vụ đám mây | Gặp trễ mạng lớn khi đặt tại Việt Nam và phụ thuộc bên thứ ba. |
| Bảng Milvus | 22 ms | Hơn 2 GB | Kiến trúc phân tán, chịu tải hàng tỷ vector nhưng quá cồng kềnh để thiết lập cho đồ án quy mô trung bình. |

*Bảng 1.2: So sánh thông số hệ quản trị Vector Database*

Dựa trên kết quả thực nghiệm, Chroma được lựa chọn nhờ khả năng nhúng trực tiếp vào ứng dụng máy chủ, mang lại độ trễ mạng bằng 0 và đáp ứng dư dả nhu cầu truy xuất của phạm vi đồ án.

## 1.5. Tổng quan nghiên cứu liên quan

Ứng dụng AI trong giáo dục đã trải qua nhiều thế hệ phát triển. Các hệ thống đời đầu như Pounce (Đại học Bang Georgia) hay Genie (Đại học Deakin) chủ yếu dựa trên cây quyết định và đối sánh mẫu. Kiến trúc này tuy đảm bảo tính kiểm soát nội dung nhưng thiếu đi khả năng mở rộng. Khi số lượng quy chế tăng lên, biểu đồ trạng thái của bot sẽ bùng nổ tổ hợp, gây tắc nghẽn quá trình bảo trì.

Tại Việt Nam, thế hệ chatbot thứ hai tại một số trường đại học bắt đầu tích hợp các mô hình phân loại ý định. Dù cải thiện được khả năng nhận diện ngôn ngữ tự nhiên, hệ thống vẫn phụ thuộc vào việc kỹ sư phải định nghĩa trước toàn bộ tập ý định và câu mẫu phát ngôn. Kiến trúc này bộc lộ lỗ hổng khi đối mặt với các câu hỏi điều kiện chéo phức tạp. Các hệ thống này thiếu đi cơ chế sinh ngôn ngữ thực thụ và không thể xâu chuỗi thông tin từ nhiều đoạn quy chế khác nhau.

Gần đây, kiến trúc RAG bắt đầu được nghiên cứu như một giải pháp thay thế hoàn hảo. Việc áp dụng RAG cho dữ liệu tiếng Việt mang đặc thù hành chính giáo dục vẫn còn khoảng trống lớn. Dữ liệu quy chế thường chứa bảng biểu phức tạp gộp cột và ngôn ngữ pháp lý đan xen với từ lóng của học sinh. Các hệ thống cơ bản thường thất bại ở bước phân mảnh tài liệu, dẫn đến việc cắt ngang bảng điểm chuẩn hoặc nhầm lẫn giữa quy chế của bậc đại học với thạc sĩ. 

Đề tài giải quyết trực tiếp khoảng trống này bằng cách xây dựng một luồng tiền xử lý chuyên biệt, tập trung vào việc áp dụng các thư viện số hóa tài liệu mạnh mẽ để bảo toàn định dạng cấu trúc và nhúng siêu dữ liệu ngữ cảnh vào từng mảnh vector. Bằng cách kết hợp sức mạnh tổng hợp ngôn ngữ với cơ sở dữ liệu chuyên ngành nội bộ, hệ thống xóa bỏ sự phụ thuộc vào kịch bản cứng, mở ra khả năng lập luận trên những truy vấn tổ hợp chưa từng xuất hiện trong tập huấn luyện.

## 1.6. Các công nghệ sử dụng trong đề tài

Để xây dựng một hệ thống quy mô thực tế, đồ án vận dụng chuỗi công nghệ hiện đại được phân tách theo từng lớp chức năng:

- Khung điều phối LangChain đóng vai trò xâu chuỗi linh hoạt quá trình tiền xử lý văn bản, tương tác truy xuất vector và giao tiếp máy chủ LLM.
- Nền tảng Google Gemini xử lý mã hóa vector và sinh văn bản tự nhiên. Giải pháp sử dụng chung hệ sinh thái này tăng tốc độ luân chuyển dữ liệu và tối ưu độ chính xác ngữ nghĩa cho tiếng Việt, tránh được hiện tượng sai lệch không gian vector giữa mô hình nhúng và mô hình sinh.
- Cơ sở dữ liệu Chroma được thiết lập cục bộ, quản lý toàn bộ cấu trúc chỉ mục vector của văn bản tuyển sinh.
- Máy chủ nền tảng phát triển bằng ngôn ngữ Python kết hợp FastAPI. Cấu trúc xử lý bất đồng bộ đáp ứng hàng trăm luồng truy vấn mạng song song. Giao thức Server-Sent Events (SSE) được ứng dụng để truyền tải tức thời các mảnh văn bản thẳng về thiết bị người dùng thay vì chờ sinh xong toàn bộ câu, giúp cảm giác độ trễ giảm xuống dưới 1 giây.
- Xử lý tài liệu thô dựa trên thư viện BeautifulSoup và hệ thống nhận dạng quang học OCR để làm sạch nguồn dữ liệu nguyên thủy phức tạp, duy trì cấu trúc bảng biểu trước khi đưa vào hàng đợi lập chỉ mục.
- Giao diện người dùng tích hợp trực tiếp lên nền tảng nhắn tin Zalo Bot giúp tiếp cận thí sinh mà không cần cài đặt thêm ứng dụng di động. Phân hệ Web Admin Dashboard được xây dựng dựa trên ngăn xếp web hiện đại React kết nối thông qua giao thức API.
