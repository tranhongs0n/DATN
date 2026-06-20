# Cấu Trúc Đồ Án Tốt Nghiệp
Đề tài: Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG.
Sinh viên: Trần Hồng Sơn — Lớp 61TH1
GVHD: TS. Lê Anh Tuấn

## PHẦN HÌNH THỨC
- LỜI CẢM ƠN
- TÓM TẮT ĐỒ ÁN (Tiếng Việt + Abstract tiếng Anh)
- MỤC LỤC
- DANH MỤC HÌNH ẢNH
- DANH MỤC BẢNG BIỂU
- DANH MỤC TỪ VIẾT TẮT

## PHẦN MỞ ĐẦU
1. Lý do chọn đề tài
   - Bối cảnh bùng nổ AI trong giáo dục và xu hướng chuyển đổi số tuyển sinh tại các trường đại học Việt Nam
   - Thực trạng tại Đại học Thủy Lợi: lượng câu hỏi lớn trong mùa tuyển sinh, thông tin phân tán trên nhiều kênh, nhân sự tư vấn quá tải
   - Hạn chế của chatbot truyền thống dạng rule-based khi áp dụng cho tuyển sinh (dữ liệu thay đổi hàng năm, câu hỏi đa dạng, ngôn ngữ thí sinh không chuẩn)
   - Kỹ thuật RAG như một giải pháp khả thi: kết hợp sức mạnh LLM với dữ liệu riêng của tổ chức mà không cần huấn luyện lại mô hình

2. Mục tiêu nghiên cứu
   - Mục tiêu lý thuyết: Nghiên cứu, phân tích và đánh giá kiến trúc RAG trong bài toán hỏi đáp miền tri thức chuyên biệt
   - Mục tiêu thực tiễn: Xây dựng hệ thống trợ lý ảo hoàn chỉnh gồm backend RAG, giao diện quản trị web, và kênh tương tác Zalo Bot — xử lý dữ liệu tuyển sinh 3 bậc (đại học, thạc sĩ, tiến sĩ) bao gồm cả dữ liệu đa phương thức

3. Đối tượng và phạm vi nghiên cứu
   - Đối tượng nghiên cứu: kiến trúc RAG, DB vector, LLM, nhu cầu thông tin của thí sinh và phụ huynh
   - Phạm vi dữ liệu: toàn bộ tài liệu tuyển sinh chính thức của TLU (86 tệp, 3 bậc đào tạo, giai đoạn 2020–2026)
   - Phạm vi kỹ thuật: hệ thống backend Python (FastAPI + LangChain + ChromaDB), frontend Zalo Bot, giao diện quản trị web
   - Giới hạn: chỉ xử lý thông tin tuyển sinh TLU

4. Phương pháp nghiên cứu
   - Nghiên cứu lý thuyết: tổng hợp, phân tích tài liệu về NLP, LLM, RAG, DB vector
   - Nghiên cứu thực nghiệm: so sánh, đánh giá các mô hình embedding và LLM khác nhau trên tập dữ liệu tuyển sinh tiếng Việt
   - Phương pháp phát triển phần mềm: phân tích yêu cầu → thiết kế kiến trúc → lập trình → tích hợp → kiểm thử

5. Ý nghĩa khoa học và thực tiễn
   - Đóng góp kỹ thuật: phân tích các thách thức khi áp dụng RAG cho dữ liệu tiếng Việt trong lĩnh vực tuyển sinh
   - Đóng góp thực tiễn: hệ thống có thể triển khai thực tế tại TLU, giảm tải nhân sự tư vấn

## CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU

1.1. Tổng quan về trợ lý ảo và bài toán hỏi đáp tự động
   - Lịch sử phát triển chatbot: từ ELIZA → chatbot rule-based → chatbot NLP → chatbot LLM
   - Phân loại chatbot theo cơ chế: rule-based, retrieval-based, generative, hybrid
   - Bài toán hỏi đáp miền tri thức chuyên biệt: đặc điểm, thách thức, yêu cầu về độ chính xác

1.2. Mô hình ngôn ngữ lớn
   - Kiến trúc Transformer: cơ chế self-attention, positional encoding, tại sao vượt trội so với RNN/LSTM
   - Quá trình huấn luyện LLM: pre-training trên dữ liệu lớn, instruction tuning, RLHF
   - Hạn chế cốt lõi ảnh hưởng trực tiếp đến bài toán tuyển sinh:
     - Ảo giác: sinh thông tin sai một cách tự tin → nguy hiểm khi cung cấp mã ngành, điểm chuẩn sai
     - Kiến thức đóng băng: không cập nhật đề án tuyển sinh mới mà không can thiệp kỹ thuật
     - Context window giới hạn: không thể nhồi toàn bộ tài liệu tuyển sinh vào prompt

1.3. Kỹ thuật RAG
   - Khái niệm và động cơ ra đời: giải quyết 3 hạn chế cốt lõi của LLM ở mục 1.2
   - Kiến trúc tổng quát: Indexing → Retrieval → Generation
   - Phân tích so sánh RAG với các phương pháp thay thế (bảng so sánh: Fine-tuning vs RAG vs Prompt Engineering thuần)
   - Các biến thể RAG nâng cao: Naive RAG → Advanced RAG → Modular RAG
   - Vị trí của đề tài trong bản đồ RAG

1.4. DB vector và kỹ thuật nhúng
   - Text Embedding: nguyên lý chuyển văn bản thành vector đa chiều, không gian ngữ nghĩa
   - Các mô hình embedding phổ biến và khả năng xử lý tiếng Việt
   - DB vector: nguyên lý tìm kiếm tương đồng, các thuật toán indexing (HNSW, IVF)
   - So sánh các DB vector: ChromaDB vs Pinecone vs Weaviate vs Milvus → lý do chọn ChromaDB

1.5. Tổng quan nghiên cứu liên quan
   - Survey các hệ thống chatbot tuyển sinh trên thế giới
   - Survey tại Việt Nam: chatbot tuyển sinh các trường
   - Phân tích khoảng trống nghiên cứu: chưa có giải pháp RAG cho tuyển sinh tiếng Việt xử lý dữ liệu đa phương thức
   - Đóng góp dự kiến của đề tài so với các công trình trước

1.6. Các công nghệ và công cụ sử dụng trong đề tài
   - LangChain: vai trò orchestration framework, lý do chọn
   - Google Gemini API: Gemini 3 Flash + Gemini Embedding 2, lý do chọn hệ sinh thái Google
   - ChromaDB: phù hợp cho quy mô nhỏ-vừa, triển khai cục bộ
   - FastAPI: lý do chọn thay vì Flask/Django, ưu điểm async + SSE streaming
   - Các thư viện hỗ trợ: BeautifulSoup4, PyPDF, Docx2txt, python-docx

## CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

2.1. Phân tích yêu cầu hệ thống
   2.1.1. Xác định các tác nhân: thí sinh/phụ huynh, quản trị viên
   2.1.2. Yêu cầu chức năng:
      - Người dùng cuối: hỏi đáp qua Zalo Bot, xem lịch sử, truy cập tài liệu gốc
      - Quản trị viên: upload tài liệu → tự động chunk/embed, rebuild DB vector, scrape website TLU, chuyển đổi tệp qua AI, giám sát indexing, xem thống kê
   2.1.3. Yêu cầu phi chức năng: độ chính xác, độ trễ < 5s, khả năng mở rộng, tính nhất quán dữ liệu

2.2. Phân tích chuyên sâu dữ liệu tuyển sinh TLU
   2.2.1. Phân loại và thống kê nguồn dữ liệu (ĐH: 38 tệp, ThS: 36 tệp, TS: 12 tệp)
   2.2.2. Phân tích 7 thách thức xử lý dữ liệu tuyển sinh:
      - Dữ liệu phân tán đa kênh, đa định dạng
      - Bảng biểu phức tạp → mất cấu trúc khi trích xuất
      - Mất ngữ cảnh khi chia chunk
      - Xung đột thời gian: dữ liệu cũ lẫn mới
      - Khoảng cách từ vựng: ngôn ngữ hành chính vs ngôn ngữ thí sinh
      - Quy tắc tuyển sinh có tính điều kiện chéo
      - Dữ liệu ẩn trong hình ảnh
   2.2.3. Chiến lược xử lý cho từng thách thức

2.3. Thiết kế kiến trúc tổng thể
   2.3.1. Kiến trúc 3 tầng: Data Layer → Service Layer → Presentation Layer
   2.3.2. Pipeline nạp dữ liệu: Thu thập → Tiền xử lý → Chuyển đổi multimodal → Chia chunk → Nhúng vector → Lưu ChromaDB
   2.3.3. Pipeline truy vấn và sinh câu trả lời: Tiếp nhận → Tiền xử lý query → Truy xuất → Prompt assembly → Streaming generation → Phản hồi

2.4. Thiết kế Prompt Engineering
   2.4.1. Triết lý thiết kế prompt: ưu tiên độ chính xác, không ảo giác, văn phong tự nhiên
   2.4.2. Cấu trúc System Instruction
   2.4.3. Cấu trúc Query Template
   2.4.4. Kỹ thuật chống ảo giác
   2.4.5. Quá trình lặp và cải tiến prompt

2.5. Thiết kế Use Case và luồng hoạt động
   2.5.1. Sơ đồ Use Case tổng thể
   2.5.2. Luồng hoạt động chi tiết (Activity Diagram):
      - Luồng cập nhật tài liệu
      - Luồng tư vấn đa lượt
      - Luồng chuyển đổi tệp đa phương thức
      - Luồng scrape dữ liệu

2.6. Thiết kế giao diện
   2.6.1. Giao diện Zalo Bot: webhook, UI native (horizontal scroll, quick reply, persistent menu)
   2.6.2. Giao diện Web Admin Dashboard: layout, upload, indexing status, thống kê, scraping, chuyển đổi tệp

## CHƯƠNG 3: TRIỂN KHAI HỆ THỐNG

3.1. Thiết lập môi trường phát triển
   - Cấu trúc dự án, quản lý dependencies (pyproject.toml)
   - Quản lý cấu hình: config.yaml + .env + prompts.yaml + Pydantic Settings

3.2. Triển khai module thu thập dữ liệu
   3.2.1. Web Scraper (TLUAdmissionScraper): API nội bộ TLU, ThreadPoolExecutor, phân loại category
   3.2.2. Document Loader: quét đệ quy, phát hiện định dạng, PyPDFLoader + Docx2txtLoader
   3.2.3. Multimodal File Converter: upload → Gemini Vision → markdown → docx

3.3. Triển khai module xử lý và lưu trữ vector
   3.3.1. GeminiEmbeddings: custom LangChain wrapper, batch 100/lần, task_type phân biệt
   3.3.2. VectorDBManager: build ChromaDB, chunking (1000/200), append mode, thống kê
   3.3.3. IndexingService: orchestration, trạng thái file, upload admin, chuyển đổi multimodal

3.4. Triển khai module hỏi đáp RAG
   3.4.1. MultimodalEngine: Gemini API wrapper, streaming, retry 429, temperature=0.0, cleanup
   3.4.2. chat_response: luồng RAG hoàn chỉnh (extract → greeting check → retrieval → prompt → stream)
   3.4.3. Xử lý edge case: input đa dạng, message ngắn, DB chưa build

3.5. Triển khai API Backend (FastAPI)
   3.5.1. Kiến trúc REST API: SSE streaming chat, admin endpoints
   3.5.2. CORS middleware
   3.5.3. Tích hợp Zalo Bot: webhook, xử lý sự kiện, format response
   3.5.4. Serve static files

3.6. Triển khai giao diện Web Admin
   - Layout và UX design
   - Các tính năng: upload, index, rebuild, scrape, convert, thống kê
   - Tương tác với backend qua REST API

## CHƯƠNG 4: THỬ NGHIỆM VÀ ĐÁNH GIÁ

4.1. Thiết kế phương pháp đánh giá
   4.1.1. Bộ câu hỏi kiểm thử 5 nhóm:
      - Nhóm 1: Tra cứu thông tin cơ bản (mã ngành, chỉ tiêu, điểm chuẩn)
      - Nhóm 2: Ngôn ngữ thí sinh thực tế (viết tắt, không dấu, slang)
      - Nhóm 3: Câu hỏi phức tạp có điều kiện chéo
      - Nhóm 4: Câu hỏi bẫy ngoài phạm vi
      - Nhóm 5: Câu hỏi đa bậc đào tạo (thạc sĩ, tiến sĩ, quốc tế)
   4.1.2. Các metric đánh giá: Correctness, Faithfulness, Relevance, Latency, Rejection accuracy

4.2. Kết quả thử nghiệm
   4.2.1. Kết quả theo từng nhóm (bảng tổng hợp + ví dụ minh họa)
   4.2.2. Phân tích hiệu suất: latency, throughput, ảnh hưởng quota
   4.2.3. So sánh chất lượng giữa các cấu hình prompt

4.3. Phân tích kết quả và thảo luận
   4.3.1. Trường hợp xử lý tốt → phân tích nguyên nhân
   4.3.2. Trường hợp thất bại → root cause analysis
   4.3.3. Đánh giá tổng thể: điểm mạnh, điểm yếu, mức độ sẵn sàng triển khai

4.4. Demo và minh họa hệ thống
   - Screenshot Zalo Bot
   - Screenshot Web Admin Dashboard
   - Minh họa luồng end-to-end

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
1. Tổng kết kết quả đạt được (lý thuyết + thực tiễn)
2. Đánh giá mức độ hoàn thành mục tiêu (đối chiếu từng mục tiêu → kết quả)
3. Những hạn chế còn tồn tại
4. Hướng phát triển trong tương lai

## TÀI LIỆU THAM KHẢO

## PHỤ LỤC
- Phụ lục A: Bảng câu hỏi kiểm thử đầy đủ và kết quả
- Phụ lục B: Mã nguồn các module chính (trích đoạn có chú thích)
- Phụ lục C: Hướng dẫn cài đặt và triển khai hệ thống
