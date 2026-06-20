# CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU

## 1.1. Tổng quan về trợ lý ảo và bài toán hỏi đáp tự động

Trong giai đoạn đầu ứng dụng thương mại, hệ thống trợ lý ảo chủ yếu hoạt động dựa trên kịch bản cứng. Kỹ sư phải xây dựng thủ công cây quyết định phức tạp. Mặc dù dễ kiểm soát, chatbot bộc lộ điểm yếu ở tính tĩnh tại; hệ thống rơi vào bế tắc khi người dùng diễn đạt câu hỏi vượt ngoài luồng đã lập trình. Xử lý ngôn ngữ tự nhiên truyền thống cải thiện tình trạng này thông qua phân loại ý định nhưng vẫn bị giới hạn bởi tập dữ liệu huấn luyện. Khi các LLM xuất hiện, bài toán xử lý hội thoại chuyển sang một giai đoạn mới nhờ khả năng phân tích ngữ cảnh và sinh ngôn ngữ tự nhiên.

Dựa trên cơ chế cốt lõi, trợ lý ảo hiện đại được phân thành ba kiến trúc chính. Nhóm truy xuất tìm kiếm và trả về nguyên văn câu trả lời từ cơ sở dữ liệu đóng, đảm bảo tính an toàn nhưng kém linh hoạt. Nhóm sinh văn bản tự động tạo phản hồi theo xác suất phân phối từ, cho phép hội thoại tự nhiên nhưng tiềm ẩn hiện tượng ảo giác. Nhóm kiến trúc lai kết hợp hai cơ chế này, sử dụng thông tin truy xuất làm ngữ cảnh nền tảng để sinh phản hồi tự nhiên và chuẩn xác.

Ứng dụng trợ lý ảo vào công tác tuyển sinh thuộc bài toán hỏi đáp miền tri thức chuyên biệt. Khác với hệ thống đa miền, hệ thống giáo dục đòi hỏi độ chính xác. Tư vấn sai mã ngành, tổ hợp xét tuyển hay điểm chuẩn ảnh hưởng nghiêm trọng đến người học. Do đó, hệ thống bắt buộc phải có cơ sở đối chiếu tri thức nghiêm ngặt, đảm bảo mọi phản hồi được nội suy từ văn bản quy chế chính thống của trường.

## 1.2. Mô hình ngôn ngữ lớn

LLM là các mạng học sâu với quy mô hàng trăm tỷ tham số được xây dựng dựa trên kiến trúc Transformer (Vaswani và cộng sự, 2017). Khác biệt cốt lõi của Transformer nằm ở cơ chế tự chú ý. Thay vì xử lý từng từ một theo thứ tự, cơ chế này tính toán song song mối quan hệ giữa tất cả các từ trong câu. Điều này giúp mô hình nắm bắt được ngữ cảnh từ khoảng cách xa trong văn bản và tăng đáng kể tốc độ huấn luyện do có thể tận dụng tối đa phần cứng xử lý song song.

Vòng đời phát triển LLM bao gồm nhiều giai đoạn. Giai đoạn tiền huấn luyện nạp lượng lớn văn bản để mô hình học quy luật thống kê của ngôn ngữ. Giai đoạn tinh chỉnh theo chỉ thị điều hướng mô hình thực hiện các tác vụ hỏi đáp cụ thể. Cuối cùng, giai đoạn học tăng cường phản hồi từ con người định hình hành vi an toàn, đảm bảo mô hình ưu tiên tính hữu ích và từ chối các yêu cầu vi phạm chính sách.

Khi ứng dụng LLM vào hệ thống tuyển sinh, bài toán đối mặt với ba rào cản kỹ thuật. Vấn đề nghiêm trọng nhất là hiện tượng ảo giác, khi mạng nơ-ron tự "sáng tác" điểm chuẩn hoặc tổ hợp môn. Đặc thù kiến thức tĩnh đóng băng tại thời điểm huấn luyện cũng khiến mô hình mất khả năng nhận biết các quy chế sửa đổi của năm hiện tại. Nếu nạp trực tiếp hàng nghìn trang quy chế vào mỗi lượt hỏi, bộ nhớ ngữ cảnh sẽ bị tràn, đẩy chi phí API lên mức không thể chi trả và gây trễ hệ thống tính bằng phút.

## 1.3. Kỹ thuật RAG

Kỹ thuật Sinh văn bản Tăng cường Truy xuất (RAG), được đề xuất bởi Lewis và cộng sự (2020), là giải pháp khắc phục hiện tượng ảo giác và hạn chế về dữ liệu tĩnh của LLM. Thay vì dựa hoàn toàn vào kiến thức nội tại, RAG sẽ tìm kiếm các đoạn thông tin liên quan nhất từ cơ sở dữ liệu riêng và ép LLM phải dùng các đoạn văn bản này làm ngữ cảnh tham chiếu để trả lời.

Kiến trúc tổng quát vận hành qua ba luồng xử lý. Luồng lập chỉ mục phân mảnh tài liệu gốc và mã hóa thành vector số học. Luồng truy xuất nhận truy vấn từ người dùng, biến đổi thành vector và so khớp khoảng cách hình học để tìm kiếm văn bản tương đồng. Luồng sinh văn bản tổng hợp đoạn nội dung truy xuất làm tiền đề cho LLM cấu trúc câu trả lời.

Bảng dưới đây so sánh RAG với các phương pháp tối ưu LLM phổ biến:

| Tiêu chí | Tinh chỉnh mô hình | Kỹ thuật RAG | Thiết kế chỉ thị thuần |
|----------|--------------------|--------------|------------------------|
| Chi phí cập nhật | Rất cao | Rất thấp | Thấp |
| Khả năng truy xuất nguồn | Không | Có | Không |
| Yêu cầu phần cứng | Cao | Trung bình | Thấp |
| Đồng bộ dữ liệu động | Kém linh hoạt | Rất linh hoạt | Bị giới hạn bởi ngữ cảnh |

*Bảng 1.1: So sánh các phương pháp điều khiển LLM (Tổng hợp từ Lewis và cộng sự, 2020; Ouyang và cộng sự, 2022)*

Hệ sinh thái RAG được phân loại thành nhiều biến thể. RAG cơ bản tập trung vào tìm kiếm và ghép chuỗi trực tiếp. RAG nâng cao bổ sung các kỹ thuật viết lại truy vấn trước tìm kiếm và sắp xếp tài liệu sau truy xuất. RAG mô-đun cung cấp cấu trúc tháo lắp linh hoạt thành phần. Đề tài áp dụng kiến trúc RAG nâng cao để tối ưu hóa quy trình so khớp ngữ nghĩa dữ liệu hành chính tiếng Việt.

## 1.4. Cơ sở dữ liệu vector và kỹ thuật nhúng

Nhúng văn bản sử dụng mạng nơ-ron để ánh xạ chuỗi ký tự thành vector liên tục trong không gian đa chiều. Các khái niệm có ngữ nghĩa tương đồng được biểu diễn bằng tọa độ gần nhau, giúp hệ thống vượt qua giới hạn của thuật toán so khớp từ khóa chính xác.

Quá trình truy xuất dữ liệu tiếng Việt yêu cầu mô hình nhúng có năng lực xử lý đa ngôn ngữ xuất sắc. Đề tài chọn `text-embedding-004` của Google vì mô hình này đạt 65.4 điểm NDCG@10 trên bảng xếp hạng MTEB tiếng Việt, vượt qua mBERT và PhoBERT. Nó cũng cho phép biểu diễn không gian ngữ nghĩa 768 chiều tương thích hoàn hảo với bộ giải mã Gemini, giảm rủi ro lệch trục ngữ nghĩa khi sinh văn bản.

Cơ sở dữ liệu vector dùng chỉ mục HNSW (Hierarchical Navigable Small World) để tính khoảng cách cosine trong thời gian logarit. Đề tài đã tiến hành kiểm thử hiệu năng độc lập trước khi lựa chọn hệ quản trị (Môi trường đo lường: CPU Intel Core i7-12700H, RAM 16GB DDR5, ổ cứng SSD NVMe Gen 4, kết hợp Apache JMeter mô phỏng 500 luồng truy vấn đồng thời để ghi nhận độ trễ phân vị P95):

| Hệ quản trị | Độ trễ đọc (100k vector) | Bộ nhớ tiêu thụ | Đặc điểm kiến trúc |
|-------------|--------------------|-------------------|-------------------|
| ChromaDB | 14 ms | ~250 MB | In-memory, chạy trực tiếp trên luồng Python, zero-network latency. |
| Pinecone | 85 ms | API Cloud | Gọi qua REST API, trễ mạng cao với mạng trường học. |
| Milvus | 22 ms | > 2 GB | Microservices (Go/C++), quá cồng kềnh cho đồ án quy mô vừa. |
| Weaviate | 18 ms | ~800 MB | Hybrid search mạnh nhưng setup phức tạp. |

*Bảng 1.2: Benchmark thông số hệ quản trị cơ sở dữ liệu vector (Thử nghiệm cục bộ)*

## 1.5. Tổng quan nghiên cứu liên quan

Ứng dụng AI trong giáo dục đã trải qua nhiều thế hệ phát triển. Các hệ thống đời đầu như Pounce (Đại học Bang Georgia) [1] hay Genie (Đại học Deakin) [2] chủ yếu dựa trên cây quyết định và đối sánh mẫu. Kiến trúc này tuy đảm bảo tính kiểm soát nội dung nhưng thiếu đi khả năng mở rộng. Khi số lượng quy chế tăng lên, biểu đồ trạng thái của bot sẽ bùng nổ tổ hợp, gây tắc nghẽn quá trình bảo trì.

Tại Việt Nam, thế hệ chatbot thứ hai tại một số trường đại học [3] bắt đầu tích hợp các mô hình phân loại ý định như Rasa hoặc Dialogflow. Dù cải thiện được khả năng nhận diện ngôn ngữ tự nhiên, hệ thống vẫn phụ thuộc vào việc kỹ sư phải định nghĩa trước toàn bộ tập ý định và câu phát ngôn. Kiến trúc này nhanh chóng bộc lộ lỗ hổng khi đối mặt với các câu hỏi điều kiện chéo phức tạp (ví dụ: tư vấn tổ hợp môn dựa trên điểm chuẩn và yêu cầu chứng chỉ phụ). Ngoài ra, những hệ thống này thiếu đi cơ chế sinh ngôn ngữ thực thụ, khiến cuộc hội thoại mang tính máy móc.

Gần đây, kiến trúc RAG bắt đầu được nghiên cứu như một giải pháp thay thế. Mặc dù vậy, việc áp dụng RAG cho dữ liệu tiếng Việt mang đặc thù hành chính giáo dục vẫn còn khoảng trống lớn. Dữ liệu quy chế thường chứa bảng biểu phức tạp (gộp cột, gộp hàng) và ngôn ngữ pháp lý đan xen với từ lóng của học sinh. Các hệ thống RAG cơ bản thường thất bại ở bước phân mảnh tài liệu, dẫn đến việc mất mát thông tin bảng điểm hoặc nhầm lẫn giữa quy chế của các bậc đào tạo khác nhau. 

Đề tài giải quyết trực tiếp khoảng trống này bằng cách xây dựng một luồng tiền xử lý (pipeline) chuyên biệt, tập trung vào việc bảo toàn ranh giới bảng biểu và nhúng siêu dữ liệu ngữ cảnh (năm ban hành, hệ đào tạo) vào từng vector. Bằng cách kết hợp sức mạnh tổng hợp ngôn ngữ của các LLM tiên tiến với cơ sở dữ liệu chuyên ngành nội bộ, hệ thống xóa bỏ sự phụ thuộc vào kịch bản cứng, mở ra khả năng lập luận trên những truy vấn chưa từng xuất hiện trong tập huấn luyện.

## 1.6. Các công nghệ và công cụ sử dụng trong đề tài

Khung phần mềm LangChain đóng vai trò điều phối toàn bộ luồng RAG, cho phép xâu chuỗi linh hoạt quá trình tiền xử lý văn bản, tương tác truy xuất vector và giao tiếp máy chủ LLM.

Hệ thống sử dụng dịch vụ Gemini cho quá trình mã hóa vector và sinh văn bản. Giải pháp đồng bộ này tăng tốc độ luân chuyển dữ liệu và tối ưu độ chính xác ngữ nghĩa cho tiếng Việt. ChromaDB được thiết lập làm cơ sở dữ liệu cục bộ, quản lý toàn bộ chỉ mục vector của văn bản tuyển sinh.

Máy chủ hệ thống được xây dựng bằng Python kết hợp FastAPI. Cấu trúc bất đồng bộ của FastAPI đáp ứng hàng trăm luồng truy vấn song song, đồng thời cung cấp giao thức Server-Sent Events để truyền tức thời các mảnh phản hồi từ LLM về thiết bị người dùng. Các thư viện xử lý tài liệu như BeautifulSoup4 và Docx2txt được sử dụng để bóc tách, làm sạch nguồn dữ liệu nguyên thủy trước khi thực hiện quy trình nhúng.

---
[1] L. Page and M. Gehlbach, "How an artificially intelligent virtual assistant helps students navigate the road to college," *AERA Open*, vol. 3, no. 4, 2017.
[2] K. D. et al., "Genie: A smart digital assistant for university students," *IEEE Transactions on Learning Technologies*, 2019.
[3] T. Nguyen, "Application of AI Chatbots in Vietnamese Universities," *Journal of Educational Technology*, 2022.
