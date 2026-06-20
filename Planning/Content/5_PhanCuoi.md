# LỜI CẢM ƠN

Trong suốt quá trình thực hiện đồ án tốt nghiệp, em đã nhận được sự quan tâm, giúp đỡ và động viên rất lớn từ các thầy cô giáo, gia đình và bạn bè.

Trước hết, em xin gửi lời tri ân sâu sắc nhất đến TS. Lê Anh Tuấn. Thầy đã dành nhiều thời gian quý báu để tận tình hướng dẫn, định hướng công nghệ và tháo gỡ những vướng mắc cho em trong suốt quá trình triển khai hệ thống trợ lý ảo này. Những lời khuyên chuyên môn của thầy là kim chỉ nam giúp đồ án đi đúng hướng và đạt được kết quả như hiện tại.

Em cũng xin gửi lời cảm ơn chân thành đến Ban Giám hiệu Trường Đại học Thủy Lợi và toàn thể các thầy cô giáo khoa Công nghệ thông tin. Các thầy cô đã truyền đạt cho em những kiến thức nền tảng vô giá trong suốt những năm tháng ngồi trên giảng đường, tạo nền móng vững chắc để em có thể tự tin nghiên cứu và ứng dụng các công nghệ mới.

Đồng thời, em cũng xin bày tỏ lòng biết ơn vô hạn đối với gia đình và những người bạn đã luôn ở bên cạnh, động viên tinh thần và tạo mọi điều kiện thuận lợi nhất để em có thể hoàn thành tốt chương trình học thuật của mình.

Mặc dù đã nỗ lực hết sức, nhưng do giới hạn về mặt thời gian và kiến thức cá nhân, đồ án chắc chắn không tránh khỏi những thiếu sót. Em rất mong nhận được sự góp ý quý báu từ hội đồng các thầy cô để đề tài được hoàn thiện hơn.

Em xin chân thành cảm ơn!

---

# TÓM TẮT ĐỒ ÁN

**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG
**Sinh viên:** Trần Hồng Sơn (61TH1)
**GVHD:** TS. Lý Anh Tuấn

Đồ án tập trung nghiên cứu và xây dựng một hệ thống trợ lý ảo thông minh nhằm hỗ trợ công tác tư vấn tuyển sinh tại Trường Đại học Thủy Lợi. Động lực của nghiên cứu xuất phát từ thực trạng lượng thông tin tuyển sinh ngày càng đồ sộ, dẫn đến tình trạng phân mảnh tri thức và gây quá tải nghiêm trọng cho bộ phận tư vấn truyền thống trong các khoảng thời gian cao điểm.

Để giải quyết bài toán này, đồ án đã ứng dụng kiến trúc RAG kết hợp với sức mạnh của LLM. Hệ thống được phát triển chuyên sâu dựa trên ngôn ngữ lập trình Python, sử dụng khung điều phối LangChain và cơ sở dữ liệu vector ChromaDB để tự động quản lý, phân mảnh và truy xuất thông tin từ bộ hồ sơ 86 tệp đề án tuyển sinh đa bậc học. Điểm nổi bật nhất của hệ thống nằm ở khả năng phân tách tài liệu đa phương thức và cơ chế chống lại hiện tượng sinh văn bản ảo giác, đảm bảo mọi câu trả lời đều được trích xuất chính xác và trung thực từ nguồn dữ liệu chính thống của nhà trường.

Cấu trúc đồ án được tổ chức thành 4 chương chính. Chương 1 tổng quan các nền tảng lý thuyết cốt lõi về hệ thống hỏi đáp tự động và mô hình ngôn ngữ lớn. Chương 2 đi sâu vào phân tích bài toán, bóc tách các thách thức về dữ liệu và xây dựng kiến trúc tổng thể. Chương 3 hiện thực hóa bản thiết kế thông qua việc triển khai các luồng xử lý kỹ thuật phức tạp trên máy chủ FastAPI. Cuối cùng, Chương 4 thiết lập bộ tiêu chuẩn đo lường và tiến hành thử nghiệm, chứng minh hệ thống không chỉ đạt tốc độ phản hồi ấn tượng trên giao diện Zalo Bot mà còn cung cấp một bảng điều khiển trung tâm hỗ trợ quản trị tri thức hiệu quả. Kết quả đạt được mở ra tiềm năng to lớn trong việc triển khai giải pháp tự động hóa này vào chu trình tư vấn thực tế của trường trong tương lai.

---

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1. Tổng kết kết quả đạt được
Nghiên cứu đã hoàn thiện một luồng công việc kỹ thuật khép kín từ khâu thu thập tri thức gốc cho đến khâu tương tác trực tiếp với thí sinh. Về phương diện lý thuyết, đồ án đã làm rõ cơ chế vận hành của kiến trúc RAG trong việc khắc phục điểm yếu của LLM, đồng thời phân tích cặn kẽ những rào cản đặc thù khi xử lý ngôn ngữ và cấu trúc văn bản tiếng Việt. Về mặt thực tiễn, việc xây dựng thành công hai phân hệ giao diện hoạt động song song (Zalo Bot cho người dùng và Web Dashboard cho quản trị viên) đã chứng minh tính linh hoạt của giải pháp, sẵn sàng đáp ứng nhu cầu tự động hóa nghiệp vụ tư vấn quy mô lớn.

## 2. Đánh giá mức độ hoàn thành mục tiêu
Dựa trên các định hướng thiết lập từ ban đầu, hệ thống đã đáp ứng vượt kỳ vọng ở nhiều khía cạnh kỹ thuật phức tạp.

Bảng 5.1: Đối chiếu kết quả thực hiện so với mục tiêu đề tài

| Mục tiêu đề ra | Kết quả đạt được | Mức độ hoàn thành |
|----------------|------------------|-------------------|
| Tổ chức tự động hóa nguồn dữ liệu đa cấp độ (Đại học, Thạc sĩ, Tiến sĩ) | Xây dựng thành công cơ sở dữ liệu vector chứa 86 tài liệu; tự động phân vùng không gian tìm kiếm tránh xung đột dữ liệu giữa các bậc học. | Hoàn thành xuất sắc |
| Triệt tiêu hiện tượng ảo giác trong tư vấn | Thiết kế thành công bộ chỉ thị ép buộc mô hình từ chối câu hỏi ngoài phạm vi; tỉ lệ từ chối đúng đạt 98% trong thử nghiệm thực tế. | Hoàn thành xuất sắc |
| Đảm bảo tốc độ phản hồi theo chuẩn nhắn tin thời gian thực | Xây dựng luồng kết xuất văn bản bằng công nghệ SSE; giảm độ trễ trải nghiệm xuống dưới 3 giây/truy vấn. | Hoàn thành tốt |
| Xử lý cấu trúc dữ liệu hình ảnh và biểu mẫu | Tích hợp luồng chuyển đổi đa phương thức qua thị giác máy tính, tái tạo thành công cấu trúc văn bản từ ảnh. | Hoàn thành khá |

## 3. Những hạn chế còn tồn tại
Mặc dù đáp ứng tốt các luồng hỏi đáp chuẩn, hệ thống vẫn đối mặt với một số rào cản kỹ thuật nhất định trong quá trình vận hành thực tế:
- Sự phụ thuộc hạ tầng API bên thứ ba thể hiện khi khâu cốt lõi sinh ngôn ngữ hiện hoàn toàn phụ thuộc vào giới hạn băng thông của Google. Khi lượng truy cập đạt đỉnh điểm, việc chậm trễ do báo lỗi 429 quá tải máy chủ là không thể tránh khỏi.
- Hiện tượng tin nhắn phân mảnh xảy ra do thí sinh có thói quen ngắt nhỏ câu hỏi thành 3-4 tin nhắn ngắn lẻ tẻ gửi liên tiếp. Việc hệ thống nhúng và trả lời từng tin nhắn một cách cơ học khiến bộ nhớ ngữ cảnh bị loãng, dẫn đến khả năng truy xuất bị sai lệch nghiêm trọng.
- Sự suy thoái ngữ cảnh hội thoại kéo dài bộc lộ trong một phiên trò chuyện dài hàng chục lượt, khi đó mô hình bắt đầu bộc lộ hiện tượng bỏ quên các thông tin cốt lõi đã đề cập ở các lượt đầu tiên.
- Về vấn đề quản lý vòng đời tri thức, hệ thống hiện tại có khả năng dọn dẹp dữ liệu cũ khi tài liệu mới được nạp vào, nhưng chưa sở hữu thuật toán tự động quét và phát hiện các luồng quy chế đã hết hạn nằm im trong cơ sở dữ liệu.

## 4. Hướng phát triển trong tương lai
Để hiện thực hóa hoàn toàn khát vọng đưa hệ thống thành bộ não tư vấn độc lập tại trường, một số định hướng phát triển công nghệ chuyên sâu cần được xem xét trong tương lai:
- Việc tự chủ hạ tầng với mô hình mã nguồn mở sẽ ưu tiên thử nghiệm các mô hình tiên tiến như DeepSeek-R1 Distill hoặc Gemma 3, vận hành qua các khung nội bộ như Ollama hoặc vLLM. Quá trình triển khai trực tiếp trên cụm GPU máy chủ vật lý của trường sẽ giải quyết dứt điểm bài toán giới hạn băng thông API và bảo mật dữ liệu riêng tư.
- Việc nâng cấp luồng thu thập dữ liệu bằng các công cụ hiện đại như MinerU hoặc MagicPDF sẽ giúp bảo toàn cấu trúc bảng biểu và trích xuất công thức chính xác hơn nhiều so với các thư viện đọc văn bản cơ bản hiện tại.
- Việc nâng cấp cấu trúc tìm kiếm sẽ chuyển từ truy xuất một giai đoạn sang truy xuất hai giai đoạn (two-stage retrieval). Kiến trúc này kết hợp việc thu hẹp phạm vi tài liệu ở giai đoạn một với kỹ thuật xếp hạng lại (reranking) bằng các mô hình như bge-reranker ở giai đoạn hai, giúp triệt tiêu hiện tượng phân mảnh ngữ cảnh và tăng cường độ chính xác khi đối sánh mã số ngành học cụ thể.
- Việc triển khai hàng đợi thông minh sẽ áp dụng kỹ thuật gom cụm tin nhắn bằng hàng đợi. Hệ thống sẽ chờ vài giây để hợp nhất các tin nhắn phân mảnh của học sinh, kết hợp module viết lại truy vấn trước khi tiến hành tra cứu vector, bảo vệ tính vẹn toàn của mạch hội thoại.
- Việc tích hợp kênh phản hồi tự động đa phương thức nhằm phát triển tính năng nhận diện và phản hồi bằng giọng nói trên nền tảng Zalo. Dựa trên các nghiên cứu thành công trước đây trong trường, hệ thống định hướng sẽ tích hợp mô hình `Whisper` cho luồng chuyển đổi giọng nói thành văn bản, và thư viện `gTTS` cho luồng tổng hợp tiếng nói đầu ra.
- Việc mở rộng phạm vi từ tuyển sinh sang cố vấn học tập và hướng nghiệp nhằm biến chatbot thành một trợ lý toàn năng. Hệ thống có thể tham chiếu vào Sổ tay sinh viên, quy chế học vụ, dữ liệu thị trường lao động (VietnamWorks, TopCV) và hồ sơ cựu sinh viên để tư vấn lộ trình nghề nghiệp cá nhân hóa và kết nối thực tập.
- Việc kết hợp với dịch vụ thông báo đẩy tự động nhằm nhắc nhở thí sinh các mốc thời gian nộp hồ sơ quan trọng.
- Việc triển khai đa nền tảng giao diện, mở rộng từ Zalo Bot sang các nền tảng phổ biến với sinh viên công nghệ như Discord Bot. Đồng thời xem xét tích hợp các giải pháp đóng gói sẵn như `Open WebUI` qua Docker để làm phương án thay thế triển khai nhanh chóng cho hệ thống quản trị, giảm tải công sức thiết kế giao diện từ đầu.
- Việc xây dựng đường ống đánh giá tự động tập trung vào nghiên cứu tích hợp khung phần mềm RAGAS, kết hợp mô hình LLM làm giám khảo (LLM-as-a-judge) để tự động tính toán và đo lường liên tục các thông số về độ trung thành cũng như sự liên quan của dữ liệu trả về sau mỗi lần thay đổi bộ chỉ thị, thay thế hoàn toàn quy trình chấm điểm thủ công.

---

# TÀI LIỆU THAM KHẢO

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS*, 2020.
[2] A. Vaswani et al., "Attention Is All You Need," *NeurIPS*, 2017.
[3] Y. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey," *arXiv preprint*, 2024.
[4] J. Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," *NAACL*, 2019.
[5] T. Brown et al., "Language Models are Few-Shot Learners," *NeurIPS*, 2020.
[6] S. Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation," *arXiv preprint*, 2023.
[7] LangChain AI, "LangChain Documentation," 2024. [Online]. Available: https://python.langchain.com.
[8] Chroma, "ChromaDB Documentation," 2024. [Online]. Available: https://docs.trychroma.com.
[9] Google, "Google Gemini API Reference," 2024. [Online]. Available: https://ai.google.dev.
[10] Trường Đại học Thủy Lợi, "Đề án tuyển sinh trình độ đại học," 2020-2024. [Online]. Available: http://tuyensinh.tlu.edu.vn.
[11] Trường Đại học Thủy Lợi, "Các quy chế, thông báo xét tuyển trình độ thạc sĩ và tiến sĩ," 2024. [Online]. Available: http://ts.tlu.edu.vn.
