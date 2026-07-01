=== PAGE 45 ===
36 
CHƯƠNG 3: TRIỂN KHAI HỆ THỐNG 
3.1. Thiết lập môi trường phát triển 
Dự án được phân chia thành các phân h ệ độc lập nhằm tối ưu hóa quá trình qu ản trị 
và bảo trì mã nguồn. Cấu trúc thư mục ngăn cách rõ ràng giữa tầng cấu hình, nghiệp 
vụ cốt lõi và giao diện quản trị. 
 
Hình 3.1: Sơ đồ cấu trúc thư mục dự án 
Kiến trúc phần mềm sử dụng khối công nghệ lõi bao gồm FastAPI làm máy chủ điều 
phối luồng mạng, LangChain thiết lập đường ống xử lý thông tin và Vector Database 
đóng vai trò kho lưu trữ. Việc phát triển theo mô hình nguyên khối phân hệ giúp quản 
trị viên có thể thay thế LLM khác chỉ bằng cách cấu hình lại tệp môi trường mà không 
cần can thiệp vào thuật toán truy xuất. 
3.2. Triển khai phân hệ quản trị người dùng 
Trong quá trình xây d ựng hệ thống, an toàn thông tin và b ảo mật phân quyền là yếu 
tố bắt bu ộc đ ối v ới m ột h ệ thống c ấp trư ờng. Đ ồ án đã phát tri ển m ột User 
Management Module, đ ộc lập hoàn toàn v ới luồng tương tác c ủa trợ lý ảo trên ứng 
dụng nhắn tin. 


=== PAGE 46 ===
37 
3.2.1. Cơ chế xác thực và mã hóa 
Hệ thống sử dụng CSDL nội bộ để lưu trữ thông tin. Mật khẩu người dùng không bao 
giờ được lưu dưới dạng văn bản thô. Hàm băm mật khẩu áp dụng thư viện chuẩn với 
cơ chế sinh Salt tự động. Quá trình đ ối chiếu mật khẩu đảm bảo chống lại các cuộc 
Brute-force và Rainbow Table. 
Hệ thống sử dụng cơ chế xác thực JWT stateless thay vì sử dụng phiên truyền thống. 
Khi cán bộ đăng nhập thành công qua cổng xác thực, hệ thống khởi tạo một chuỗi mã 
chứa định danh người dùng và th ời gian hết hạn là 24 gi ờ. Mọi yêu cầu thao tác d ữ 
liệu từ Web Admin Dashboard lên máy ch ủ đều phải đính kèm chu ỗi mã này. L ớp 
trung gian chịu trách nhiệm giải mã và xác th ực quyền hạn trước khi cho phép hàm 
logic thực thi. 
3.2.2. Quản lý vòng đời tài khoản và lưu vết 
Phân hệ cung cấp bộ giao thức kết nối hoàn chỉnh để quản trị viên cấp cao có thể khởi 
tạo, cập nhật, xóa và truy xuất danh sách nhân sự. Hệ thống tích hợp logic ràng buộc 
chặn quản trị viên tự xóa chính tài khoản đang đăng nhập của mình để tránh gây lỗi 
mất quyền kiểm soát toàn cục. 
Mọi hành động nhạy cảm như thêm mới tài khoản, đổi mật khẩu hay xóa quyền truy 
cập đều được hệ thống tự động lưu vết qua Audit Logging tích hợp sẵn. Điều này giúp 
minh bạch hóa trách nhiệm và dễ dàng truy vết khi có sự cố thay đổi dữ liệu. 
3.3. Triển khai phân hệ tự động thu thập dữ liệu 
Một trong những thách thức lớn nhất của hệ thống hỏi đáp là việc duy trì sự cập nhật 
của CSTT. Thay vì ép bu ộc cán bộ tuyển sinh phải tự tải về từng văn bản thông báo 
trên trang web của trường rồi tải ngược lên hệ thống, đồ án đã phát triển Web Scraper 
đóng vai trò như một công cụ tự động hóa quy trình nghiệp vụ. 

=== PAGE 47 ===
38 
3.3.1. Kiến trúc luồng thu thập dữ liệu 
Công cụ thu thập được lập trình để quét mã nguồn của cổng thông tin tuyển sinh. Phân 
hệ này bóc tách các bài vi ết thông báo m ới nhất theo t ừng danh m ục định sẵn. Hệ 
thống duy trì t ệp trạng thái để ghi nhớ mốc thời gian cào dữ liệu gần nhất. Khi kích 
hoạt thông qua cổng lệnh kiểm tra, hệ thống tiến hành đối chiếu và chỉ tải về những 
thông báo chưa từng xuất hiện. 
3.3.2. Xử lý đa luồng và tạo tài liệu động 
Để tăng tốc độ quét hàng trăm bài viết, hệ thống sử dụng cơ chế xử lý đa luồng. Việc 
chạy song song giúp tải các tệp đính kèm như PDF ho ặc DOCX cùng một lúc thông 
qua thư viện kết nối mạng. 
Điểm đột phá k ỹ thuật nằm ở cơ chế chuyển đổi nội dung web sang đ ịnh dạng cấu 
trúc. Nếu bài viết tuyển sinh không có tệp đính kèm mà chỉ có văn bản trực tiếp trên 
web, hệ thống sẽ dùng công cụ bóc tách để trích xuất văn bản thuần túy và bỏ qua mã 
rác. Sau đó, hệ thống dùng thư viện xử lý tài liệu để tự động tạo ra một tệp Word mới 
với tiêu đề chính là tên bài vi ết, chứa toàn bộ nội dung của bài viết, rồi đẩy tệp này 
vào luồng tiền xử lý của Vector Database. Nh ờ đó, máy chủ có thể đọc hiểu cả các 
thông báo văn bản ngắn trên web. 
3.4. Triển khai phân hệ quản trị kho tri thức và dữ liệu vector 
Luồng nghi ệp v ụ xử lý d ữ liệu c ủa đ ề tài không d ừng l ại ở việc thi ết l ập Vector 
Database, mà bao hàm toàn b ộ quy trình kiểm soát trạng thái tệp gốc thông qua mô 
đun quản lý dữ liệu. 
3.4.1. Cơ chế xóa và ghi đè thông minh 
Trong bối cảnh văn bản hành chính, một quy chế của năm nay có thể sẽ thay thế hoàn 
toàn bản quy chế năm trước. Nếu cả hai văn bản cùng tồn tại trong kho lưu tr ữ, mô 
hình AI sẽ gặp tình trạng Knowledge Conflict. Giao th ức xóa tệp giải quyết triệt để 

=== PAGE 48 ===
39 
bài toán này thông qua luồng xóa đồng bộ. Quy trình bắt đầu bằng việc nhận lệnh xóa 
từ giao diện web, tiến hành xóa tệp vật lý tương ứng trên máy chủ, và kết nối trực tiếp 
với Vector Database để thanh lọc toàn bộ các Points thuộc về tệp đó. Cơ chế xóa triệt 
để này đảm bảo dữ liệu máy học và dữ liệu vật lý luôn đồng nhất. 
3.4.2. Thống kê và xử lý tệp rác 
Cổng thống kê cung cấp cái nhìn toàn cảnh về bộ não nhân tạo, bao gồm tổng số lượng 
tài liệu vật lý đã t ải lên và t ổng số mảnh văn b ản đã đư ợc phân rã thành công. H ệ 
thống hỗ trợ đường dẫn chuyên dò tìm các tệp không nằm trong danh sách định dạng 
chuẩn, giúp dọn dẹp không gian lưu tr ữ rác và các quá trình nh ận dạng văn bản thất 
bại. 
3.5. Triển khai cơ chế tối ưu hóa hệ thống 
Để đảm bảo khả năng chịu tải và tốc độ phản hồi trong mùa cao điểm tuyển sinh, hệ 
thống tích hợp ba cơ chế tối ưu hóa cấp độ kiến trúc. 
3.5.1. Cơ chế Semantic Cache 
Đây là một điểm sáng nhằm giảm thiểu chi phí dịch vụ và triệt tiêu độ trễ mạng. Thay 
vì gọi dịch vụ AI liên tục cho cùng một câu hỏi, hệ thống xây dựng một bảng nhớ đệm 
ngữ nghĩa cục bộ. 
Khi người dùng hỏi một câu, câu hỏi được nhúng thành vector. Nếu sau đó có người 
khác hỏi một câu tương tự về mặt ngữ nghĩa, hệ thống không tốn tài nguyên truy xuất 
lại toàn bộ kho tri thức. Mã nguồn trích xuất các mảng vector từ bảng nhớ đệm, chuyển 
thành ma trận và sử dụng Dot product và Norm để đo lường độ tương đồng. Nếu điểm 
số đạt ngưỡng khắt khe, hệ thống trả thẳng kết quả cũ từ máy chủ cục bộ với độ trễ 
siêu thấp. Vòng đời của bộ nhớ đệm được thiết lập là 30 ngày. 

=== PAGE 49 ===
40 
3.5.2. Kiến trúc đa phương thức và cơ chế chống quá tải 
Khi ứng dụng nhận hàng ngàn tin nh ắn, việc gọi dịch vụ có thể bị từ chối do chạm 
mốc giới hạn tài nguyên. L ớp MultimodalEngine được bọc bởi thuật toán bẫy lỗi tự 
động nhận diện tình trạng từ chối dịch vụ. Khi bị từ chối, luồng xử lý không làm treo 
máy chủ mà sẽ đi vào trạng thái chờ và thực hiện thử lại tối đa 3 lần. Nhờ đó, hệ thống 
giữ được tính kiên cường cực cao. Mô đun này s ử dụng công cụ kết nối mới nhất để 
tải tệp vật lý trực tiếp lên đám mây, theo dõi vòng đ ời tệp từ khi xử lý đến khi hoàn 
tất, và tự động dọn dẹp không gian sau khi thao tác xong. 
3.5.3. Cơ chế dự phòng thu thập tin nhắn 
Ứng dụng tương tác thư ờng hoạt động qua cơ ch ế đẩy thông báo tr ực tiếp. Khi h ệ 
thống bảo trì hoặc chạy trong môi trường không có địa chỉ mạng tĩnh, cơ chế này sẽ 
vô tác dụng. Đồ án xử lý vấn đề này bằng việc cung cấp một tiến trình nền thực hiện 
Long Polling. Hàm cập nhật liên tục giữ kết nối mạng đến máy chủ trung gian, kiểm 
soát con trỏ để đảm bảo không bỏ sót bất kỳ tin nhắn nào của thí sinh, tạo thành lưới 
an toàn hoàn hảo. 
3.6. Triển khai giao diện lập trình ứng dụng 
Hệ thống máy ch ủ đóng vai trò c ầu nối điều khiển luồng giao ti ếp mạng thông qua 
thiết kế chuẩn hóa. Tuyến dịch vụ cốt lõi truyền luồng dữ liệu theo định dạng Server-
Sent Events (SSE), mang l ại Streaming giúp gi ảm độ trễ hiển thị xuống mức thấp 
nhất. 
Hệ thống hỗ trợ xử lý luồng nhận thông báo để đồng bộ với hạ tầng máy chủ của ứng 
dụng nhắn tin, kết hợp với CORS Middleware để chấp nhận kết nối đa miền từ Web 
Admin Dashboard. Bảng điều khiển và tập lệnh trình duyệt được phục vụ thông qua 
công cụ phát tệp tĩnh tích hợp sẵn. 
 

=== PAGE 50 ===
41 
3.7. Triển khai giao diện quản trị và ứng dụng người dùng 
Hệ thống cung cấp hai phương thức tương tác chính: giao diện dành cho người dùng 
cuối (thí sinh, phụ huynh) và giao diện quản trị tập trung (dành cho ban tuyển sinh). 
3.7.1. Giao diện người dùng trên nền tảng nhắn tin 
Người dùng tương tác thông qua nền tảng nhắn tin Zalo. Việc triển khai trực tiếp trên 
ứng dụng nhắn tin loại bỏ rào cản cài đặt phần mềm mới, giúp quá trình tra cứu thông 
tin diễn ra mượt mà và trực tiếp từ thiết bị di động cá nhân. Mọi thao tác nhắn tin đều 
tuân thủ thói quen sử dụng thông thường của người dùng. 
 


=== PAGE 51 ===
42 
Hình 3.2: Hệ thống trợ lý ảo đang tư vấn trực tiếp trên nền tảng Zalo 
3.7.2. Bảng điều khiển quản trị tổng quan (Dashboard) 
Web Admin Dashboard cung cấp một nền tảng quản trị trực quan, hiển thị các thông 
số thống kê theo thời gian thực về máy chủ, số lượng tài liệu đã mã hóa, cũng như lịch 
sử tương tác. T ại giao di ện này, qu ản trị viên có th ể theo dõi nhanh hi ệu suất hoạt 
động của bộ não nhân tạo. 
 
Hình 3.3: Bảng điều khiển quản trị tổng quan trên Web Admin Dashboard 
3.7.3. Phân hệ quản lý tài liệu và mã hóa dữ liệu 
Danh sách tài li ệu quản lý tập trung phản ánh trạng thái từng tệp bằng mã màu tiêu 
chuẩn. Giao diện hỗ trợ quản trị viên tải tệp lên (PDF, DOCX) bằng thao tác kéo thả, 
trực tiếp kích hoạt quá trình bóc tách và giám sát ti ến trình mã hóa thành các Vector 
đa chiều. Các tệp rác hoặc lỗi đều có thể được xóa trực tiếp tại đây. 


=== PAGE 52 ===
43 
 
Hình 3.4: Giao diện quản trị tri thức và tải lên tài liệu 
3.7.4. Phân hệ thu thập dữ liệu tự động (Web Scraper) 
Giao diện quản lý Scraper cho phép qu ản trị viên kích ho ạt công c ụ cào dữ liệu từ 
trang web tuyển sinh của trường. Giao diện sẽ hiển thị chi tiết tiến trình cào dữ liệu, 
số lượng bài viết mới được phát hiện và tự động báo cáo kết quả sau khi quy trình bóc 
tách hoàn tất. 
 


=== PAGE 53 ===
44 
Hình 3.5: Giao diện điều khiển bộ tự động thu thập dữ liệu 
3.7.5. Giao diện kiểm thử hệ thống (Chat Tester) 
Để đảm bảo độ chính xác trước khi cung cấp dịch vụ ra công chúng, Web Admin cung 
cấp một công cụ Chat Tester độc lập. Tại đây, quản trị viên có thể nhập câu hỏi để giả 
lập luồng hội thoại. Hệ thống sẽ trả về câu trả lời cùng với các tham số đo lường thời 
gian trễ và tài liệu nguồn đã dùng để suy luận. 
 
Hình 3.6: Giao diện kiểm thử trợ lý ảo (Chat Tester) dành cho quản trị viên 
3.7.6. Phân hệ quản lý người dùng 
Để đảm bảo tính bảo mật của hệ thống, giao diện quản trị cung cấp phân hệ quản lý 
người dùng. Quản trị viên cấp cao có th ể tạo mới, cập nhật, cấp quyền hoặc thu hồi 
quyền truy cập của các thành viên trong ban tuy ển sinh. Các thao tác đều được giám 
sát và lưu vết để đảm bảo tính minh bạch. 


=== PAGE 54 ===
45 
 
ssHình 3.7: Giao diện phân hệ quản lý người dùng 
3.7.7. Giao diện quản lý từ viết tắt 
Trong ngữ cảnh tuyển sinh, học sinh thường sử dụng rất nhiều từ lóng hoặc từ viết tắt 
(VD: "cntt" thay cho "Công ngh ệ thông tin"). Giao di ện này cho phép qu ản trị viên 
định nghĩa và cập nhật linh hoạt từ điển viết tắt. Khi câu hỏi đi vào hệ thống, các từ 
này sẽ được tự động giải nghĩa trước khi đưa vào luồng tìm kiếm. 
 


=== PAGE 55 ===
46 
Hình 3.8: Giao diện quản lý và định nghĩa từ viết tắt 
3.7.8. Kiểm thử tiền xử lý (Query Test) 
Mô đun Query Test cho phép qu ản trị viên xem trước cách thức hệ thống tiền xử lý 
và nhúng (embedding) câu hỏi. Quản trị viên có thể kiểm tra xem câu hỏi có được giải 
nghĩa đúng từ viết tắt hay không, và danh sách các đoạn văn bản (chunks) nào sẽ được 
Vector Database truy xuất lên. Điều này giúp tinh chỉnh cơ sở dữ liệu một cách hiệu 
quả nhất. 
 
Hình 3.9: Giao diện kiểm thử luồng tiền xử lý câu hỏi (Query Test) 
 
  


=== PAGE 56 ===
47 
CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ 
4.1. Thiết kế phương pháp đánh giá 
Quy trình đánh giá đư ợc thiết lập nhằm lượng hóa toàn di ện hai khía c ạnh của hệ 
thống bao gồm chất lượng sinh văn bản và hiệu năng máy chủ. Đề tài sử dụng tập dữ 
liệu chuẩn chứa 1200 cặp câu hỏi và câu trả lời được gán nhãn bán tự động từ 86 văn 
bản gốc. 
4.1.1. Phân loại tập dữ liệu kiểm thử 
Ma trận kiểm thử bao gồm năm nhóm tình huống chính. Nhóm đầu tiên là tra cứu trực 
diện mã ngành, ch ỉ tiêu và điểm chuẩn. Nhóm thứ hai tập trung vào các truy v ấn sử 
dụng từ viết tắt hoặc ngôn ngữ tự do trên mạng xã hội. Nhóm thứ ba kiểm tra các điều 
kiện chéo phức hợp với nhiều biến số đầu vào. Nhóm thứ tư đánh giá khả năng phản 
hồi đối với các câu hỏi nằm ngoài phạm vi tuyển sinh. Nhóm cuối cùng yêu cầu truy 
xuất thông tin trải dài trên đa bậc đào tạo. 
4.1.2. Tiêu chí đánh giá chất lượng sinh 
Hệ thống đánh giá chất lượng sinh văn bản dựa trên bốn tiêu chí cốt lõi (Es và c ộng 
sự, 2023). Bốn tiêu chí này bao gồm Context Precision, Context Recall, độ trung thực 
để chống Hallucination, và cuối cùng là Answer Relevancy. 
4.1.3. Kịch bản kiểm thử hiệu năng tối ưu hóa 
Bên cạnh bài kiểm tra truy xuất tiêu chuẩn, hệ thống được thử nghiệm chịu tải thông 
qua hai bài kiểm thử chuyên biệt nhằm đánh giá các cơ chế tối ưu mới được tích hợp. 
Bài kiểm thử Semantic Cache tiến hành gửi 500 truy vấn lặp lại hoặc có biến thể ngữ 
nghĩa nhẹ để đo lường tỷ lệ trúng đệm và sự chênh lệch độ trễ. Bài kiểm thử chống 
quá tải thực hiện gửi dồn dập 2000 luồng truy vấn đồng thời qua cổng kết nối dịch vụ 
AI để cố tình gây tràn hạn mức, qua đó quan sát khả năng chống sập của hệ thống. 

=== PAGE 57 ===
48 
4.2. Kết quả thử nghiệm 
4.2.1. Đánh giá độ chính xác 
Kết quả trích xuất sau khi chạy kiểm thử trên toàn bộ 1200 câu hỏi: 
Bảng 4.1: Kết quả đánh giá hiệu năng trên tập truy vấn 
Nhóm câu hỏi Context 
Precision 
Context 
Recall 
Faithfulness Answer 
Relevancy 
Nhóm 1: Tra cứu đơn lẻ 0.94 0.98 0.96 0.95 
Nhóm 2: Từ lóng viết tắt 0.90 0.92 0.89 0.91 
Nhóm 3: Logic phức hợp 0.88 0.85 0.91 0.88 
Nhóm 4: Ngoài phạm vi Không có Không có Không có 0.95 
Nhóm 5: Đa bậc đào tạo 0.86 0.82 0.89 0.85 
Bộ chỉ thị mạnh mẽ giúp hệ thống từ chối cung cấp dữ liệu ngoài luồng đạt tỉ lệ 95 
phần trăm. V ới nhóm ngôn ng ữ mạng xã h sội, thuật toán nhúng vector v ẫn liên k ết 
thành công văn bản quy chế nhờ chung không gian ngữ nghĩa. 
4.2.2. Đánh giá hiệu năng và cơ chế tối ưu hóa 
Kết quả bài kiểm thử Semantic Cache mang lại sự đột phá về tốc độ: 
Bảng 4.2: Đánh giá hiệu năng của Semantic Cache 
Kịch bản Tỷ lệ trúng 
đệm 
Độ trễ trung 
bình 
Mức tiêu thụ API 
Câu hỏi mới hoàn 
toàn 
0% 2400 ms 100% 

=== PAGE 58 ===
49 
Câu hỏi tương 
đồng cao 
100% 8 ms 0% 
Truy vấn ngẫu 
nhiên thực tế 
~ 62% 950 ms Tiết kiệm 62% chi phí 
Trong bài kiểm thử ép tải kích hoạt mã lỗi hạn mức truy cập, hệ thống không xảy ra 
hiện tượng treo c ứng. Lớp MultimodalEngine kích ho ạt cơ ch ế chờ tự động thành 
công, đưa các luồng vượt ngưỡng vào trạng thái chờ 30 giây và tiếp tục phục hồi xử 
lý khi hạn mức được mở lại, duy trì tỷ lệ vận hành thành công đạt trên 99 phần trăm. 
Cơ chế dự phòng cập nhật liên tục cũng thu th ập trọn vẹn tin nhắn mà không b ị rớt 
gói dữ liệu nào. 
4.3. Phân tích kết quả và thảo luận 
Kết quả thực nghiệm phân tách rõ ràng ranh giới năng lực của kiến trúc đề xuất. 
Về điểm sáng kỹ thuật, hệ thống chứng minh độ an toàn cực cao trong việc ngăn chặn 
hiện tượng ảo giác (Hallucination). Sự kết hợp giữa Semantic Cache và thuật toán thử 
lại tự động giải quyết triệt để vấn đề thắt cổ chai của nền tảng dịch vụ đám mây. Sự 
kết hợp này biến hệ thống thành một giải pháp hoàn toàn khả thi để triển khai thương 
mại trong mùa cao điểm. 
Về rào cản tồn đọng, hệ thống gặp khó khăn khi x ử lý nhóm câu h ỏi có logic ph ức 
hợp lồng ghép nhiều biến số. Ví dụ đối với câu hỏi xác định mức giảm học phí cho 
một nam sinh ngành Công ngh ệ thông tin có ch ứng chỉ ngoại ngữ và thuộc diện hộ 
nghèo. Các mệnh đề điều kiện rời rạc nằm ở các văn bản khác nhau thường bị mất bối 
cảnh khi hệ thống phân rã tài liệu theo kích thước, dẫn đến Context Recall bị giảm. 

=== PAGE 59 ===
50 
4.4. Minh họa hoạt động hệ thống 
Quy trình giao tiếp giữa học sinh và máy chủ được thực hiện trên ứng dụng nhắn tin 
nội bộ và giao diện quản lý máy chủ. Trên luồng tương tác, văn bản tư vấn được truyền 
tải từng cụm từ qua Server-Sent Events (SSE) nh ằm triệt tiêu cảm giác chờ đợi của 
người dùng. 
 
Hình 4.1: Hệ thống trợ lý ảo đang tư vấn trực tiếp trên nền tảng nhắn tin 


=== PAGE 60 ===
51 
 
 Hình 4.2: Giao diện nạp dữ liệu tri thức tự động trên Web Admin Dashboard 
  


=== PAGE 61 ===
52 
CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN 
5.1. Tổng kết kết quả đạt được 
Nghiên cứu đã hoàn thi ện một luồng xử lý End-to-End RAG có tính th ực tiễn cao, 
khắc phục các giới hạn của LLM tĩnh trong bài toán tư vấn tuyển sinh bằng tiếng Việt. 
Đồ án không chỉ xây dựng thành công b ộ đôi giao di ện cho người dùng và qu ản trị 
viên mà còn ứng dụng các quy chu ẩn công ngh ệ phần mềm tiên tiến nhất để tối ưu 
hóa kiến trúc. 
Cụ thể, hệ thống đã đạt được các cột mốc kỹ thuật xuất sắc: 
- Về RPA (Robotic Process Automation), phân hệ Web Scraper đa luồng giải 
quyết triệt để rào cản cập nhật tài liệu, tự động chuyển đổi mã nguồn trang web 
thành không gian vector. 
- Về tối ưu hóa tài nguyên, ứng dụng thành công Semantic Cache giúp đẩy tốc 
độ phản hồi đối với các truy vấn trùng lặp xuống dưới 10ms, tiết kiệm hơn 60 
phần trăm chi phí gọi dịch vụ đám mây. 
- Về tính kiên cường, Rate Limit Backoff và cơ chế dự phòng của nền tảng nhắn 
tin đảm bảo hệ thống không bị treo hoặc rớt tin nhắn dưới áp lực truy vấn khổng 
lồ. 
- Về quản trị độc lập, việc xây dựng thành công cơ chế xác thực nội bộ và đồng 
bộ hóa thao tác xóa dữ liệu vật lý với dữ liệu vector đã giải quyết triệt để hiện 
tượng Knowledge Conflict. 
5.2. Đánh giá mức độ hoàn thành mục tiêu 
Hệ thống hoàn thành xuất sắc các mục tiêu đề ra về hiệu năng và chức năng nền tảng. 

=== PAGE 62 ===
53 
Bảng 5.1: Đối chiếu kết quả thực hiện so với mục tiêu đề tài 
Mục tiêu Kết quả thực hiện Đánh giá thực nghiệm 
Tích hợp ngôn 
ngữ tự nhiên 
Xây dựng lõi xử lý văn bản, xử 
lý từ lóng, tiếng Việt không dấu. 
Answer Relevancy vượt mức 
90 phần trăm 
Tự động hóa 
tri thức 
Phát triển công cụ tự động cào 
dữ liệu thu thập từ cổng thông 
tin. 
Tiết kiệm 95 phần trăm thời 
gian nạp tài liệu thủ công 
Hạn chế bịa 
đặt thông tin 
Khung chỉ thị nghiêm ngặt ép hệ 
thống từ chối tư vấn nếu không 
có trong CSDL. 
Đạt độ trung thực 0.89 
Đảm bảo tốc 
độ luồng 
Triển khai Semantic Cache và cơ 
chế Server-Sent Events (SSE). 
Trúng đệm giảm trễ còn 8ms, 
tốc độ luồng dưới 1 giây 
5.3. Hạn chế của hệ thống 
Bên cạnh các thành tựu tối ưu hóa máy chủ, kiến trúc của hệ thống vẫn bộc lộ một số 
giới hạn về mặt xử lý ngôn ngữ tự nhiên sâu. 
- Về ngữ cảnh rời rạc (Chunking Conflict), khi học sinh đưa ra một hồ sơ chứa 
nhiều điều kiện rẽ nhánh như điểm số, chứng chỉ, hoặc ưu tiên vùng miền, 
RecursiveCharacterTextSplitter vô tình cắt đứt sự liên kết giữa các điều khoản. 
Hệ quả là hệ thống không th ể tổng hợp đủ biến số để đưa ra kết luận tư vấn 
cuối cùng. 
- Về kiến trúc đệm đơn bộ, Semantic Cache hiện tại đang lưu trữ trực tiếp trên 
CSDL máy chủ cục bộ. Dù tốc độ rất nhanh, nhưng nếu ứng dụng triển khai 
theo mô hình phân tán nhiều máy chủ để cân bằng tải, Local Database sẽ không 
thể đồng bộ hóa bộ nhớ đệm chéo giữa các máy. 

=== PAGE 63 ===
54 
5.4. Hướng phát triển 
Để thương mại hóa và nâng cấp kiến trúc lên quy quy mô lớn hơn, đồ án đề xuất các 
hướng đi cụ thể. 
- Sử dụng kiến trúc GraphRAG. Thay vì chỉ tìm kiếm vector thuần túy, hệ thống 
sẽ được nâng cấp lên kiến trúc GraphRAG. Việc tích hợp CSDL đồ thị sẽ cung 
cấp mạng lưới liên kết biểu diễn các mối quan hệ phức tạp, ví dụ như quan hệ 
ngành Công nghệ thông tin yêu cầu khối A00 và được cộng điểm chứng chỉ 
tiếng Anh. Kiến trúc này triệt tiêu hoàn toàn điểm mù khi trả lời câu hỏi điều 
kiện chéo. 
- Nâng cấp cơ sở hạ tầng đệm. Chuyển đổi lưu trữ đệm ngữ nghĩa từ cục bộ sang 
hệ thống máy chủ Redis. Điều này cho phép hệ thống triển khai theo 
Microservices, nhiều máy trạm có thể dùng chung một siêu bộ nhớ đệm, tối ưu 
cho bài toán Horizontal Scaling. 
- Sử dụng Autonomous Agent Scraper. Phân hệ thu thập hiện tại sử dụng thuật 
toán phân tích mã tĩnh. Hệ thống sẽ được trang bị Multi-Agent, trong đó AI sẽ 
tự động học cách điều hướng các cổng thông tin thay đổi cấu trúc mã nguồn 
liên tục, biến hệ thống thu thập tri thức thành một quy trình hoàn toàn tự trị. 
  

=== PAGE 64 ===
55 
TÀI LIỆU THAM KHẢO 
[1] P. Lewis et al., "Retrieval -Augmented Generation for Knowledge -Intensive NLP 
Tasks," NeurIPS, 2020. 
[2] A. Vaswani et al., "Attention Is All You Need," NeurIPS, 2017. 
[3] Y. Gao et al., "Retrieval -Augmented Generation for Large Language Models: A 
Survey," arXiv preprint, 2024. 
[4] J. Devlin et al., "BERT: Pre -training of Deep Bidirectional Transformers for 
Language Understanding," NAACL, 2019. 
[5] S. Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented 
Generation," arXiv preprint, 2023. 
[6] LangChain AI, "LangChain Documentation," 2024. [Online]. Available: 
https://python.langchain.com. 
[7] Chroma, "ChromaDB Documentation," 2024. [Online]. Available: 
https://docs.trychroma.com. 
[8] Google, "Google Gemini API Reference," 2024. [Online]. Available: 
https://ai.google.dev. 
[9] Trư ờng Đ ại h ọc Th ủy L ợi, "Đ ề án tuy ển sinh trình đ ộ đại h ọc," 2020 -2024. 
[Online]. Available: http://tuyensinh.tlu.edu.vn. 
[10] L. Page and M. Gehlbach, "How an artificially intelligent virtual assistant helps 
students navigate the road to college," AERA Open, vol. 3, no. 4, 2017. 

