PDF Inspection for DATN_1951060985_TranHongSon.pdf
Total Pages: 64

=== FIRST 10 PAGES ===
--- PAGE 1 ---
i 
BỘ GIÁO DỤC VÀ ĐÀO TẠO BỘ NÔNG NGHIỆP VÀ MÔI TRƯỜNG 
TRƯỜNG ĐẠI HỌC THỦY LỢI 
 
 
HỌ VÀ TÊN: TRẦN HỒNG SƠN 
 
 
NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO HỖ TRỢ TUYỂN 
SINH CHO TRƯỜNG ĐẠI HỌC THỦY LỢI DỰA TRÊN KỸ THUẬT RAG 
 
ĐỒ ÁN TỐT NGHIỆP/KHÓA LUẬN TỐT NGHIỆP 
 
 
 
 
 
 
HÀ NỘI, NĂM 2026


--- PAGE 2 ---
i 
BỘ GIÁO DỤC VÀ ĐÀO TẠO BỘ NÔNG NGHIỆP VÀ MÔI TRƯỜNG 
TRƯỜNG ĐẠI HỌC THỦY LỢI 
 
 
TRẦN HỒNG SƠN 
 
 
NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO  
HỖ TRỢ TUYỂN SINH CHO TRƯỜNG ĐẠI HỌC THỦY LỢI  
DỰA TRÊN KỸ THUẬT RAG 
 
 
 
 
 
 
NGƯỜI HƯỚNG DẪN: TS. Lý Anh Tuấn 
 
 
 
HÀ NỘI, NĂM 2026
Ngành : Công Nghệ Thông Tin 
Mã số:             7480201 

--- PAGE 3 ---
i 
 
 
 
 
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM 
Độc lập  - Tự do  - Hạnh phúc 
----------★---------- 
NHIỆM VỤ ĐỒ ÁN TỐT NGHIỆP 
 
Họ tên sinh viên: Trần Hồng Sơn   Hệ đào tạo: Đại học chính quy 
Lớp: 61TH1       Ngành: Công nghệ thông tin 
Khoa: Công nghệ thông tin 
1- TÊN ĐỀ TÀI: 
NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO HỖ TRỢ TUYỂN SINH 
CHO TRƯỜNG ĐẠI HỌC THỦY LỢI DỰA TRÊN KỸ THUẬT RAG  
2- CÁC TÀI LIỆU 
[1] P. Lewis et al., "Retrieval -Augmented Generation for Knowledge -Intensive NLP 
Tasks," NeurIPS, 2020. 
[2] A. Vaswani et al., "Attention Is All You Need," NeurIPS, 2017. 
[3] Y. Gao et al., "Retrieval -Augmented Generation for Large Language Models: A 
Survey," arXiv preprint, 2024. 
[4] J. Devlin et al., "BERT: Pre -training of Deep Bidirectional Transformers for 
Language Understanding," NAACL, 2019. 
[5] T. Brown et al., "Language Models are Few-Shot Learners," NeurIPS, 2020. 
[6] LangChain AI, "LangChain Documentation," 2024. 
[7] Chroma, "ChromaDB Documentation," 2024. 
[8] Google, "Google Gemini API Reference," 2024. 


--- PAGE 4 ---
ii 
3 - NỘI DUNG CÁC PHẦN THUYẾT MINH VÀ TÍNH TOÁN: 
Nội dung các phần Tỷ lệ 
Tìm hiểu tổng quan về bài toán hướng nghiệp, các công nghệ liên quan 
(RAG, LLM, Vector Database). 
20% 
Phân tích thiết kế hệ thống, xác định yêu cầu chức năng, phi chức năng và 
kiến trúc giải pháp. 
30% 
Thu thập, tiền xử lý và xây dựng cơ sở dữ liệu hướng nghiệp đa phương 
thức. 
20% 
Cài đặt và triển khai hệ thống (chatbot Zalo, Web Dashboard, backend 
RAG). 
20% 
Đánh giá kết quả, viết báo cáo tổng kết và chuẩn bị tài liệu thuyết minh. 10% 
4. GIÁO VIÊN HƯỚNG DẪN TỪNG PHẦN 
Phần Họ tên giáo viên hướng dẫn 
Toàn bộ dự án TS. Lý Anh Tuấn 
5. NGÀY GIAO NHIỆM VỤ ĐỒ ÁN TỐT NGHIỆP 
 Ngày ............  tháng .........  năm 2026 
               Trưởng Bộ môn 
            (Ký và ghi rõ Họ tên) 
                             Giáo viên hướng dẫn chính 
                              (Ký và ghi rõ Họ tên) 
 
 
        
                                TS. Lý Anh Tuấn 
  

--- PAGE 5 ---
iii 
Nhiệm vụ Đồ án tốt nghiệp đã được Hội đồng thi tốt nghiệp của Khoa thông qua 
                                           Ngày. . . . .tháng. . . . .năm 2026
                                                        Chủ tịch Hội đồng   
                 (Ký và ghi rõ Họ tên) 
 
 
 
 
Sinh viên đã hoàn thành và nộp bản Đồ án tốt nghiệp cho Hội đồng thi ngày...  tháng... 
năm 2026. 
                         Sinh viên làm Đồ án tốt nghiệp 
                          (Ký và ghi rõ Họ tên) 
        
 
  

--- PAGE 6 ---
iv 
 
 
TRƯỜNG ĐẠI HỌC THUỶ LỢI  
KHOA CÔNG NGHỆ THÔNG TIN 
 
ĐỀ CƯƠNG ĐỒ ÁN TỐT NGHIỆP 
 
TÊN ĐỀ TÀI: Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường 
Đại học Thủy Lợi dựa trên kỹ thuật RAG 
Sinh viên thực hiện: Trần Hồng Sơn 
Lớp:   61TH1 
Mã sinh viên:  1951060985 
Số điện thoại:  0866113953 
Email:   1951060985@e.tlu.edu.vn 
Giáo viên hướng dẫn: TS. Lý Anh Tuấn 
Thời gian thực hiện: … tuần:   từ ngày: 31/03/2026  đến ngày: 30/06/2026 
 
TÓM TẮT ĐỀ TÀI 
Đề tài: Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại 
học Thủy Lợi dựa trên kỹ thuật RAG 
Sinh viên: Trần Hồng Sơn (61TH1) 
GVHD: TS. Lý Anh Tuấn 
Đề tài tập trung thiết kế và phát triển hệ thống trợ lý ảo hỗ trợ công tác tư vấn tuyển sinh 
tại Trường Đại học Thủy Lợi, hướng tới mục tiêu tự động hóa việc giải đáp thông tin đa 


--- PAGE 7 ---
v 
phân luồng. Triển khai cơ chế phân tách và lập chỉ mục đa luồng, hỗ trợ chuyển đổi linh 
hoạt các định dạng văn bản (PDF, DOCX) thành cơ sở dữ liệu vector. Hệ thống truy 
xuất nhanh chóng các điều khoản quy định giáo dục mà không phá vỡ cấu trúc ngữ nghĩa 
gốc. 
Sử dụng mô hình ngôn ngữ lớn của Google Gemini, bắt buộc mạng nơ -ron trả lời dựa 
trên tài liệu cung cấp. Hệ thống giải quyết tốt bài toán lọc câu hỏi ngoài phạm vi nghiệp 
vụ giáo dục nhằm ngăn chặn hiện tượng cung cấp thông tin sai lệch ngoài dữ liệu gốc 
của nhà trường. 
Cấu trúc đồ án gồm 4 chương. Chương 1 trình bày cơ sở lý thuyết về bài toán hỏi đáp 
và mô hình RAG. Chương 2 phân tích yêu cầu thiết kế hệ thống. Chương 3 triển khai 
các luồng xử lý kỹ thuật trên máy chủ FastAPI. Chương 4 thiết lập kịch bản đánh giá để 
kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác 
của hệ thống. 
KẾT QUẢ DỰ KIẾN 
1. Hoàn thiện quyển đồ án tốt nghiệp với đầy đủ cơ sở lý thuyết về RAG, cơ sở dữ liệu 
vector và quy trình phân tích thiết kế hệ thống. 
2. Xây dựng được website tích hợp chatbot trợ lý ảo đáp ứng đầy đủ các yêu cầu đã đề 
ra. 
3. Tiến hành triển khai thử nghiệm website tích hợp trợ lý ảo trên môi trường thực tế, 
kiểm tra tính chính xác của câu trả lời dựa trên tập dữ liệu mẫu. 
4. Đánh giá chất lượng câu trả lời của hệ thống theo các metric tiêu chuẩn: Context 
Precision, Context Recall và Answer Relevance đạt kết quả từ 0.8 (80%) trở lên; 
riêng chỉ số Faithfulness đạt mức tiệm cận 1.0 (100%). 
  

--- PAGE 8 ---
vi 
 
TIẾN ĐỘ THỰC HIỆN 
 
TT Thời gian Nội dung công việc Kết quả dự kiến đạt được 
1 01/04/2026 - 
15/04/2026 
Nghiên cứu lý thuyết, thu thập, tiền 
xử lý dữ liệu và phân tích thi ết kế 
kiến trúc hệ thống. 
Cơ sở dữ liệu chuẩn hóa, 
tài liệu thiết kế hệ thống. 
2 16/04/2026 - 
15/05/2026 
Lập trình xây d ựng pipeline RAG, 
cơ s ở dữ liệu vector và phát tri ển 
giao diện tích hợp. 
Pipeline RAG hoàn 
chỉnh 
3 16/05/2026 - 
15/06/2026 
Xây dựng bộ dữ liệu kiểm thử, đo 
lường đánh giá h ệ thống theo các 
metric và tinh chỉnh tối ưu. 
Bảng k ết qu ả đánh giá 
metric, hệ thống được tối 
ưu. 
4 16/06/2026 - 
30/06/2026 
Phân tích kết quả thực nghiệm, viết 
báo cáo tổng kết và chuẩn bị tài liệu 
bảo vệ. 
Báo cáo đ ồ án hoàn 
chỉnh. 
 
 

--- PAGE 9 ---
i 
GÁY BÌA ĐỒ ÁN TỐT NGHIỆP, KHÓA LUẬN TỐT NGHIỆP 
 
HỌ VÀ TÊN: Trần Hồng Sơn                    ĐỒ ÁN/KL TỐT NGHIỆP                                                    HÀ NỘI, NĂM 2026 

--- PAGE 10 ---
i 
Nhiệm vụ Đồ án tốt nghiệp đã được Hội đồng thi tốt nghiệp của Khoa thông qua 
                                           Ngày. . . . .tháng. . . . .năm 2026
                                                        Chủ tịch Hội đồng   
                 (Ký và ghi rõ Họ tên) 
 
 
 
 
Sinh viên đã hoàn thành và nộp bản Đồ án tốt nghiệp cho Hội đồng thi ngày...  tháng... 
năm 2026. 
                         Sinh viên làm Đồ án tốt nghiệp 
                          (Ký và ghi rõ Họ tên) 
        
 
  


=== KEYWORD SEARCH ===

Keyword: hướng dẫn
  Page 2: ... ẦN HỒNG SƠN      NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO   HỖ TRỢ TUYỂN SINH CHO TRƯỜNG ĐẠI HỌC THỦY LỢI   DỰA TRÊN KỸ THUẬT RAG              NGƯỜI HƯỚNG DẪN: TS. Lý Anh Tuấn        HÀ NỘI, NĂM 2026 Ngành : Công Nghệ Thông Tin  Mã số:             7480201  ...
  Page 4: ...  thống (chatbot Zalo, Web Dashboard, backend  RAG).  20%  Đánh giá kết quả, viết báo cáo tổng kết và chuẩn bị tài liệu thuyết minh. 10%  4. GIÁO VIÊN HƯỚNG DẪN TỪNG PHẦN  Phần Họ tên giáo viên hướng dẫn  Toàn bộ dự án TS. Lý Anh Tuấn  5. NGÀY GIAO NHIỆM VỤ ĐỒ ÁN TỐT NGHIỆP   Ngày ............  tháng ........ ...
  Page 6: ...  Sinh viên thực hiện: Trần Hồng Sơn  Lớp:   61TH1  Mã sinh viên:  1951060985  Số điện thoại:  0866113953  Email:   1951060985@e.tlu.edu.vn  Giáo viên hướng dẫn: TS. Lý Anh Tuấn  Thời gian thực hiện: … tuần:   từ ngày: 31/03/2026  đến ngày: 30/06/2026    TÓM TẮT ĐỀ TÀI  Đề tài: Nghiên cứu và xây dựng hệ thống ...
  Page 12: ... inh thần học  tập và tác phong làm việc chuyên nghiệp trong suốt quá trình học tập tại trường.  Em đặc biệt tri ân TS. Lý Anh Tu ấn, người đã tận tâm hướng dẫn, luôn đồng hành,  góp ý và định hướng cho em trong quá trình th ực hiện đồ án tốt nghiệp này. Những  chia sẻ và chỉ dẫn của thầy là nguồn động lực lớ ...
  Page 42: ... ự nhiên.  Cấu trúc chỉ thị được thiết lập tại lớp điều phối trung tâm, sử dụng kỹ thuật cung cấp  mẫu hội thoại kết hợp nhập vai nhân vật. Khung lệnh hướng dẫn mô hình đóng vai trò  là chuyên viên tư vấn chính thức, bắt buộc phải trả lời trực tiếp và ngắn gọn dựa hoàn  toàn vào các tài liệu ngữ cảnh trích xu ...
  (Truncated, more matches found...)

Keyword: tên đề tài
  Page 3: ... NGHIỆP    Họ tên sinh viên: Trần Hồng Sơn   Hệ đào tạo: Đại học chính quy  Lớp: 61TH1       Ngành: Công nghệ thông tin  Khoa: Công nghệ thông tin  1- TÊN ĐỀ TÀI:  NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRỢ LÝ ẢO HỖ TRỢ TUYỂN SINH  CHO TRƯỜNG ĐẠI HỌC THỦY LỢI DỰA TRÊN KỸ THUẬT RAG   2- CÁC TÀI LIỆU  [1] P. Lewis et a ...
  Page 6: ... iv      TRƯỜNG ĐẠI HỌC THUỶ LỢI   KHOA CÔNG NGHỆ THÔNG TIN    ĐỀ CƯƠNG ĐỒ ÁN TỐT NGHIỆP    TÊN ĐỀ TÀI: Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường  Đại học Thủy Lợi dựa trên kỹ thuật RAG  Sinh viên thực hiện: Trần Hồng Sơn   ...

Keyword: FastAPI
  Page 7: ...  thuyết về bài toán hỏi đáp  và mô hình RAG. Chương 2 phân tích yêu cầu thiết kế hệ thống. Chương 3 triển khai  các luồng xử lý kỹ thuật trên máy chủ FastAPI. Chương 4 thiết lập kịch bản đánh giá để  kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác  của hệ thống.  KẾT  ...
  Page 24: ...  86 tệp tài liệu nguyên thủy (38 tệp đại học, 36 tệp thạc sĩ và  12 tệp tiến sĩ). Khung ph ần mềm chạy trên Python, đi ều phối luồng truy xu ất bằng  FastAPI và lưu trữ embeddings cục bộ qua ChromaDB. Hệ thống từ chối trả lời mọi  câu hỏi không thuộc phạm vi tuyển sinh nội bộ.  4. Phương pháp nghiên cứu  N ...
  Page 34: ... a được thiết lập cục bộ, quản lý toàn bộ cấu trúc chỉ mục vector  của văn bản tuyển sinh.  - Máy chủ nền tảng phát triển bằng ngôn ngữ Python kết hợp FastAPI. Cấu trúc  xử lý bất đồng bộ đáp ứng hàng trăm luồng truy vấn mạng song song. Giao  thức Server-Sent Events (SSE) được ứng dụng để truyền tải tức thờ ...
  Page 45: ...  cấu hình, nghiệp  vụ cốt lõi và giao diện quản trị.    Hình 3.1: Sơ đồ cấu trúc thư mục dự án  Kiến trúc phần mềm sử dụng khối công nghệ lõi bao gồm FastAPI làm máy chủ điều  phối luồng mạng, LangChain thiết lập đường ống xử lý thông tin và Vector Database  đóng vai trò kho lưu trữ. Việc phát triển theo m ...

Keyword: Chroma
  Page 3: ... " NAACL, 2019.  [5] T. Brown et al., "Language Models are Few-Shot Learners," NeurIPS, 2020.  [6] LangChain AI, "LangChain Documentation," 2024.  [7] Chroma, "ChromaDB Documentation," 2024.  [8] Google, "Google Gemini API Reference," 2024.   ...
  Page 24: ... học, 36 tệp thạc sĩ và  12 tệp tiến sĩ). Khung ph ần mềm chạy trên Python, đi ều phối luồng truy xu ất bằng  FastAPI và lưu trữ embeddings cục bộ qua ChromaDB. Hệ thống từ chối trả lời mọi  câu hỏi không thuộc phạm vi tuyển sinh nội bộ.  4. Phương pháp nghiên cứu  Nghiên cứu tài liệu học thuật về AI và hệ ...
  Page 32: ... ấn đồng thời:  Bảng 1.2: So sánh thông số hệ quản trị Vector Database  Hệ quản  trị  Độ trễ  đọc P95  Tài nguyên  tiêu thụ  Đặc điểm kiến trúc  Bảng  Chroma  14 ms 250 MB Chạy trực tiếp trên tiến trình nội bộ, độ  trễ mạng bằng không. Rất phù hợp cho  ứng dụng nguyên khối.  Bảng  Pinecone  85 ms Sử dụng d ...
  Page 33: ... 24  Dựa trên kết quả thực nghiệm, Chroma được lựa chọn nhờ khả năng nhúng trực tiếp  vào ứng dụng máy chủ, mang lại độ trễ mạng bằng 0 và đáp ứng dư dả nhu cầu truy  xuất của phạm vi đồ án.  ...
  Page 34: ...  liệu và tối ưu  độ chính xác ngữ nghĩa cho tiếng Việt, tránh được hiện tượng sai lệch không  gian vector giữa mô hình nhúng và mô hình sinh.  - CSDL Chroma được thiết lập cục bộ, quản lý toàn bộ cấu trúc chỉ mục vector  của văn bản tuyển sinh.  - Máy chủ nền tảng phát triển bằng ngôn ngữ Python kết hợp F ...
  (Truncated, more matches found...)

Keyword: Gemini
  Page 3: ... -Shot Learners," NeurIPS, 2020.  [6] LangChain AI, "LangChain Documentation," 2024.  [7] Chroma, "ChromaDB Documentation," 2024.  [8] Google, "Google Gemini API Reference," 2024.   ...
  Page 7: ... r. Hệ thống truy  xuất nhanh chóng các điều khoản quy định giáo dục mà không phá vỡ cấu trúc ngữ nghĩa  gốc.  Sử dụng mô hình ngôn ngữ lớn của Google Gemini, bắt buộc mạng nơ -ron trả lời dựa  trên tài liệu cung cấp. Hệ thống giải quyết tốt bài toán lọc câu hỏi ngoài phạm vi nghiệp  vụ giáo dục nhằm ngăn  ...
  Page 27: ... hống của  trường.  1.2. LLM và kiến trúc Transformer  1.2.1. Kiến trúc Transformer và cơ chế tự chú ý  Các LLM hiện đại như GPT-4, Llama 3 hay Google Gemini đ ều được xây dựng dựa  trên kiến trúc Transformer, l ần đầu được giới thiệu bởi Vaswani và c ộng sự (2017).  Khác biệt cốt lõi của Transformer so vớ ...
  Page 32: ... á các hệ quản trị vector  Quá trình truy xu ất dữ liệu tiếng Việt yêu cầu mô hình nhúng có năng l ực xử lý đa  ngôn ngữ xuất sắc. Đề tài chọn mô hình gemini -embedding-2 của Google, sinh ra  vector 768 chiều.  Để quản lý các vector này, hệ thống đã tiến hành kiểm thử hiệu năng đsssộc lập trước  khi lựa ch ...
  Page 34: ... hối LangChain đóng vai trò xâu chuỗi linh hoạt quá trình tiền xử  lý văn bản, tương tác truy xuất vector và giao tiếp máy chủ LLM.  - Nền tảng Google Gemini xử lý mã hóa vector và sinh văn bản tự nhiên. Giải  pháp sử dụng chung hệ sinh thái này tăng tốc độ luân chuyển dữ liệu và tối ưu  độ chính xác ngữ n ...
  (Truncated, more matches found...)

Keyword: Zalo
  Page 4: ... kiến trúc giải pháp.  30%  Thu thập, tiền xử lý và xây dựng cơ sở dữ liệu hướng nghiệp đa phương  thức.  20%  Cài đặt và triển khai hệ thống (chatbot Zalo, Web Dashboard, backend  RAG).  20%  Đánh giá kết quả, viết báo cáo tổng kết và chuẩn bị tài liệu thuyết minh. 10%  4. GIÁO VIÊN HƯỚNG DẪN TỪNG PHẦN  ...
  Page 17: ...  ............................................................................... 36  Hình 3.2: Hệ thống trợ lý ảo đang tư vấn trực tiếp trên nền tảng Zalo ................................ 42  Hình 3.3: Bảng điều khiển quản trị tổng quan trên Web Admin Dashboard ....................... 42  Hình 3.4: Giao ...
  Page 24: ... 15  Xây dựng hệ thống trợ lý ảo hoạt động trên nền tảng Zalo, hỗ trợ giải đáp thông tin  tuyển sinh ở các bậc đại học, thạc sĩ và tiến sĩ. Hệ thống cần khả năng phân loại ý định  người dùng và truy xuất chính x ...
  Page 34: ... n thủy phức tạp, duy trì cấu trúc  bảng biểu trước khi đưa vào hàng đợi lập chỉ mục.  - Giao diện người dùng tích hợp trực tiếp lên nền tảng nhắn tin Zalo Bot giúp  tiếp cận thí sinh mà không cần cài đặt thêm ứng dụng di động. Phân hệ Web  Admin Dashboard được xây dựng dựa trên ngăn xếp web hiện đại Rea ...
  Page 35: ... n chức  năng  Đối  tượng  Mô tả chi tiết  F-01 Hỏi đáp  tương tác  tự nhiên  Người  dùng  Hệ thống phải tiếp nhận câu hỏi bằng ngôn  ngữ tự nhiên qua Zalo, nhận diện ý định và  phản hồi chính xác dựa trên quy chế.  F-02 Xử lý đa  luồng hội  thoại  Người  dùng  Có khả năng duy trì ngữ cảnh của cuộc hội   ...
  (Truncated, more matches found...)

Keyword: đánh giá
  Page 4: ... xử lý và xây dựng cơ sở dữ liệu hướng nghiệp đa phương  thức.  20%  Cài đặt và triển khai hệ thống (chatbot Zalo, Web Dashboard, backend  RAG).  20%  Đánh giá kết quả, viết báo cáo tổng kết và chuẩn bị tài liệu thuyết minh. 10%  4. GIÁO VIÊN HƯỚNG DẪN TỪNG PHẦN  Phần Họ tên giáo viên hướng dẫn  Toàn bộ dự á ...
  Page 7: ... nh RAG. Chương 2 phân tích yêu cầu thiết kế hệ thống. Chương 3 triển khai  các luồng xử lý kỹ thuật trên máy chủ FastAPI. Chương 4 thiết lập kịch bản đánh giá để  kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác  của hệ thống.  KẾT QUẢ DỰ KIẾN  1. Hoàn thiện quyển đồ án ...
  Page 8: ... s ở dữ liệu vector và phát tri ển  giao diện tích hợp.  Pipeline RAG hoàn  chỉnh  3 16/05/2026 -  15/06/2026  Xây dựng bộ dữ liệu kiểm thử, đo  lường đánh giá h ệ thống theo các  metric và tinh chỉnh tối ưu.  Bảng k ết qu ả đánh giá  metric, hệ thống được tối  ưu.  4 16/06/2026 -  30/06/2026  Phân tích kết  ...
  Page 13: ... ............................ 22  1.4.2. Thuật toán tìm kiếm xấp xỉ ....................................................................... 22  1.4.3. Đánh giá các hệ quản trị vector ................................................................ 23  1.5. Tổng quan nghiên cứu liên quan ..................... ...
  Page 15: ... ............... 45  3.7.8. Kiểm thử tiền xử lý (Query Test) ............................................................. 46  CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ ........................................................ 47  4.1. Thiết kế phương pháp đánh giá ..................................................... ...
  (Truncated, more matches found...)

Keyword: kết quả
  Page 4: ... xây dựng cơ sở dữ liệu hướng nghiệp đa phương  thức.  20%  Cài đặt và triển khai hệ thống (chatbot Zalo, Web Dashboard, backend  RAG).  20%  Đánh giá kết quả, viết báo cáo tổng kết và chuẩn bị tài liệu thuyết minh. 10%  4. GIÁO VIÊN HƯỚNG DẪN TỪNG PHẦN  Phần Họ tên giáo viên hướng dẫn  Toàn bộ dự án TS. Lý ...
  Page 7: ... tAPI. Chương 4 thiết lập kịch bản đánh giá để  kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác  của hệ thống.  KẾT QUẢ DỰ KIẾN  1. Hoàn thiện quyển đồ án tốt nghiệp với đầy đủ cơ sở lý thuyết về RAG, cơ sở dữ liệu  vector và quy trình phân tích thiết kế hệ thống.  2.  ...
  Page 8: ... vi    TIẾN ĐỘ THỰC HIỆN    TT Thời gian Nội dung công việc Kết quả dự kiến đạt được  1 01/04/2026 -  15/04/2026  Nghiên cứu lý thuyết, thu thập, tiền  xử lý dữ liệu và phân tích thi ết kế  kiến trúc hệ thống.  Cơ sở  ...
  Page 11: ... 2  LỜI CAM ĐOAN  Em xin cam đoan đây là Đồ án tốt nghiệp của em. Các kết quả, nội dung trong Đồ án  tốt nghiệp này là trung thực, không sao chép từ bất kỳ nguồn nào vào dưới bất kì hình  thức nào. Việc tham khảo tài liệu trong ...
  Page 15: ... ...................................... 47  4.1.3. Kịch bản kiểm thử hiệu năng tối ưu hóa ................................................... 47  4.2. Kết quả thử nghiệm ............................................................................................ 48  4.2.1. Đánh giá độ chính xác ............ ...
  (Truncated, more matches found...)

Keyword: thực nghiệm
  Page 8: ...  thống theo các  metric và tinh chỉnh tối ưu.  Bảng k ết qu ả đánh giá  metric, hệ thống được tối  ưu.  4 16/06/2026 -  30/06/2026  Phân tích kết quả thực nghiệm, viết  báo cáo tổng kết và chuẩn bị tài liệu  bảo vệ.  Báo cáo đ ồ án hoàn  chỉnh.      ...
  Page 24: ... cứu  Nghiên cứu tài liệu học thuật về AI và hệ thống truy xuất thông tin để xác định thiết  kế kiến trúc chuẩn cho toàn bộ quy trình RAG.  Nghiên cứu thực nghiệm được thực hiện để đo lường độ trễ, độ chính xác c ủa các  chiến lược phân đoạn văn bản và thuật toán so khớp vector. Kết quả này định hướng  lựa chọn ...
  Page 33: ... 24  Dựa trên kết quả thực nghiệm, Chroma được lựa chọn nhờ khả năng nhúng trực tiếp  vào ứng dụng máy chủ, mang lại độ trễ mạng bằng 0 và đáp ứng dư dả nhu cầu truy  xuất của phạm vi ...
  Page 58: ...   Cơ chế dự phòng cập nhật liên tục cũng thu th ập trọn vẹn tin nhắn mà không b ị rớt  gói dữ liệu nào.  4.3. Phân tích kết quả và thảo luận  Kết quả thực nghiệm phân tách rõ ràng ranh giới năng lực của kiến trúc đề xuất.  Về điểm sáng kỹ thuật, hệ thống chứng minh độ an toàn cực cao trong việc ngăn chặn  hiện ...
  Page 62: ... 53  Bảng 5.1: Đối chiếu kết quả thực hiện so với mục tiêu đề tài  Mục tiêu Kết quả thực hiện Đánh giá thực nghiệm  Tích hợp ngôn  ngữ tự nhiên  Xây dựng lõi xử lý văn bản, xử  lý từ lóng, tiếng Việt không dấu.  Answer Relevancy vượt mức  90 phần trăm  Tự động hóa ...
  (Truncated, more matches found...)

Keyword: phạm vi
  Page 7: ... mô hình ngôn ngữ lớn của Google Gemini, bắt buộc mạng nơ -ron trả lời dựa  trên tài liệu cung cấp. Hệ thống giải quyết tốt bài toán lọc câu hỏi ngoài phạm vi nghiệp  vụ giáo dục nhằm ngăn chặn hiện tượng cung cấp thông tin sai lệch ngoài dữ liệu gốc  của nhà trường.  Cấu trúc đồ án gồm 4 chương. Chương 1 t ...
  Page 22: ...  quy  định vai trò, ngữ điệu và ranh giới hoạt động của  mô hình.  Two-stage  retrieval  Truy xuất  hai giai đoạn  Kiến trúc tìm kiếm kết hợp thu hẹp phạm vi ở giai  đoạn đầu và xếp hạng lại tài liệu ở giai đoạn sau.  Utterance Câu phát  ngôn  Đơn vị hội thoại hoàn chỉnh hoặc chuỗi văn bản  đầu vào do ngườ ...
  Page 24: ... i ngũ tuyển sinh cập nhật trực tiếp  văn bản quy định mới, đồng thời giám sát lịch sử hội thoại và chất lượng phản hồi từ  hệ thống.  3. Đối tượng và phạm vi nghiên cứu  Đối tượng nghiên cứu là kỹ thuật RAG, tập trung vào việc thiết lập luồng tiền xử lý  tài liệu đa đ ịnh d ạng. H ệ thống tích h ợp thư vi  ...
  Page 32: ... á trình tìm kiếm bắt đầu từ lớp trên cùng, nhanh chóng nhảy các bước dài đến  vùng chứa vector gần giống nhất, sau đó đi xuống lớp dưới để tinh chỉnh phạm vi. Cơ  chế này giảm độ phức tạp truy xuất xuống mức thời gian logarit, đ ảm bảo hệ thống  phản hồi dưới 50ms ngay cả khi kho dữ liệu lên tới hàng chục  ...
  Page 33: ...  nghiệm, Chroma được lựa chọn nhờ khả năng nhúng trực tiếp  vào ứng dụng máy chủ, mang lại độ trễ mạng bằng 0 và đáp ứng dư dả nhu cầu truy  xuất của phạm vi đồ án.  1.5. Tổng quan nghiên cứu liên quan  Ứng dụng AI trong giáo dục đã trải qua nhiều thế hệ phát triển. Các hệ thống đời đầu  như Pounce (Đ ại h ...
  (Truncated, more matches found...)

Keyword: hạn chế
  Page 12: ... g cho em trong quá trình th ực hiện đồ án tốt nghiệp này. Những  chia sẻ và chỉ dẫn của thầy là nguồn động lực lớn giúp em hoàn thành đề tài.  Do còn hạn chế về kinh nghiệm thực tế cũng như kiến thức chuyên sâu, đồ án của em  không tránh kh ỏi những thiếu sót. Em r ất mong nh ận được những ý ki ến đóng góp ...
  Page 13: ... .................................. 18  1.2.2. Vòng đời huấn luyện của LLM................................................................. 19  1.2.3. Hạn chế của LLM trong hệ thống tri thức đóng ....................................... 19  1.3. Kỹ thuật sinh văn bản tăng cường truy xuất .................... ...
  Page 28: ...  Giai đoạn  này định hình hành vi an toàn, đảm bảo mô hình ưu tiên tính hữu ích, không  thiên kiến và từ chối các yêu cầu vi phạm chính sách.  1.2.3. Hạn chế của LLM trong hệ thống tri thức đóng  Khi ứng dụng LLM nguyên bản vào hệ thống tuyển sinh, bài toán đối mặt với ba rào  cản kỹ thuật lớn:  - Hiện tượ ...
  Page 29: ...  kiến trúc cốt lõi  Kỹ thuật RAG được công bố lần đầu bởi Patrick Lewis và cộng sự (2020) là giải pháp  triệt để nhằm khắc phục hiện tượng ảo giác và hạn chế về dữ liệu tĩnh của LLM. Thay  vì buộc mô hình phải ghi nhớ mọi thứ vào các trọng số mạng nơ-ron, RAG tách bạch  tri thức ra một CSDL độc lập.  Kiến  ...
  Page 62: ... Tự động hóa  tri thức  Phát triển công cụ tự động cào  dữ liệu thu thập từ cổng thông  tin.  Tiết kiệm 95 phần trăm thời  gian nạp tài liệu thủ công  Hạn chế bịa  đặt thông tin  Khung chỉ thị nghiêm ngặt ép hệ  thống từ chối tư vấn nếu không  có trong CSDL.  Đạt độ trung thực 0.89  Đảm bảo tốc  độ luồng  T ...
  (Truncated, more matches found...)

Keyword: đóng góp
  Page 12: ...  hạn chế về kinh nghiệm thực tế cũng như kiến thức chuyên sâu, đồ án của em  không tránh kh ỏi những thiếu sót. Em r ất mong nh ận được những ý ki ến đóng góp  quý báu từ quý thầy cô để hoàn thiện hơn đề tài này.  Một lần nữa, em xin chân thành cảm ơn!     ...
