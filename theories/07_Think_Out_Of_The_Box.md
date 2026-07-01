# TƯ DUY PHẢN BIỆN (Think Out Of The Box)

Đây là các câu hỏi cực "khoai" mà Hội đồng bảo vệ (GVPB) có thể vặn hỏi để kiểm tra xem sinh viên có thực sự làm chủ hệ thống không. Bạn cần nắm thật kỹ cách trả lời dưới đây.

## Câu 1: Tại sao em không dùng Dialogflow (chatbot theo kịch bản) mà phải cực khổ tự build RAG phức tạp?
**Bản chất:** GVPB muốn hỏi xem bạn có phân biệt được hệ thống rule-based cũ và AI sinh tạo mới không.
**Cách trả lời:** 
"Dạ thưa thầy, Dialogflow cực kỳ tốt nếu kịch bản ít và cố định (Rule-based intent). Tuy nhiên, quy chế tuyển sinh của TLU rất dài, phức tạp và cập nhật liên tục hàng năm. Nếu dùng Dialogflow, ban tuyển sinh sẽ phải tự gõ hàng ngàn kịch bản hỏi-đáp bằng tay. 
Với kiến trúc RAG, hệ thống tự động hóa hoàn toàn. Ban tuyển sinh chỉ cần upload file Word/PDF quy chế mới vào, hệ thống tự nhúng vector và chatbot tự khắc hiểu. Chi phí bảo trì bằng 0."

## Câu 2: API Gemini miễn phí thì sẽ có giới hạn (Rate Limit). Lỡ mùa thi cao điểm 5000 em vào hỏi một lúc, hệ thống của em có "sập" không?
**Bản chất:** GVPB kiểm tra khả năng tư duy thiết kế hệ thống lớn (System Design) và khả năng bắt lỗi (Error Handling).
**Cách trả lời:**
"Dạ em đã dự liệu vấn đề này và xử lý bằng 2 lớp bảo vệ:
1. **Lớp 1 - Semantic Cache:** Gần 60% câu hỏi của thí sinh là giống nhau (vd: học phí bao nhiêu, điểm CNTT). Các câu này sẽ bị chặn ở Cache và lấy kết quả cũ trả về ngay lập tức (mất 8ms), hoàn toàn KHÔNG GỌI API Gemini.
2. **Lớp 2 - Rate Limit Backoff:** Nếu thực sự bị nghẽn API (lỗi HTTP 429), code em viết hàm tự động chờ (sleep) vài giây rồi thử lại tối đa 3 lần. Nếu vẫn không được, hệ thống sẽ trả về câu thân thiện 'Hệ thống đang quá tải, em vui lòng đợi 1 phút' thay vì bị crash server báo lỗi đỏ chót ạ."

## Câu 3: Học sinh dùng từ viết tắt, tiếng lóng kiểu "điểm chuẩn cntt bnhiu đh tl", mô hình nhúng (Embedding) đọc có hiểu không?
**Bản chất:** Vector db rất dở ở chỗ bắt lỗi chính tả, hoặc viết tắt nếu mô hình không được train tốt ở VN.
**Cách trả lời:**
"Dạ đây chính là nhược điểm thực tế của embedding thuần. Để khắc phục, em đã tự code một mô-đun **Tiền xử lý (Pre-processing) kết hợp Từ điển viết tắt**. Từ điển này do Admin quản lý trên Web. 
Khi câu hỏi tới, thuật toán sẽ thay 'cntt' thành 'Công nghệ thông tin', 'bnhiu' thành 'bao nhiêu' TRƯỚC KHI đem đi nhúng vector. Nhờ vậy, điểm tương đồng (similarity score) tăng lên đáng kể và tìm tài liệu chính xác tuyệt đối."

## Câu 4: RAG tốt đấy, nhưng nếu có người dùng bot để chửi bậy, hỏi thông tin chính trị độc hại, hoặc yêu cầu bot 'Viết code cho tao' thì bot có trả lời không?
**Bản chất:** GVPB test khả năng bảo mật (Security & Guardrails) của AI.
**Cách trả lời:**
"Dạ hệ thống của em có tích hợp **Rule Engine (Bộ lọc Guardrails)** đứng ở cửa ngõ. Nó sẽ phân tích Ý ĐỊNH (Intent) của câu hỏi. Nếu câu hỏi có tính chất thù địch, độc hại, hoặc KHÔNG THUỘC PHẠM VI TUYỂN SINH (ví dụ hỏi giải toán, viết code), hệ thống sẽ chủ động chặn và trả lời: 'Xin lỗi, tôi chỉ hỗ trợ thông tin tuyển sinh Đại học Thủy Lợi'. Em đã test 1200 câu và chặn thành công 95% câu ngoài phạm vi."

## Câu 5: Hệ thống Web Admin của em bảo mật thế nào? Lỡ sinh viên khác truy cập vào xóa mất tài liệu tuyển sinh thì sao?
**Bản chất:** Test kiến thức căn bản của backend.
**Cách trả lời:**
"Dạ Web Admin của em được bảo vệ nghiêm ngặt bằng token JWT (JSON Web Token) dạng stateless. Chỉ cán bộ có tài khoản mã hóa Bcrypt trong database mới lấy được token. Token này có thời hạn ngắn (24h).
Ngoài ra, mọi thao tác nhạy cảm (như Thêm, Sửa, Xóa tài liệu) đều được em ghi log vào bảng **Audit Logging** trong SQLite: Lưu rõ ID người dùng, thao tác lúc mấy giờ, IP nào. Nếu có sự cố hoàn toàn truy vết được ạ."

## Câu 6: Dữ liệu của trường hiện có 86 tệp. Nếu sang năm trường mở rộng lên 10.000 tệp văn bản thì ChromaDB cục bộ (local) của em chạy nổi không, hay phải đổi sang dùng DB trên mạng?
**Bản chất:** Hỏi về khả năng mở rộng (Scalability).
**Cách trả lời:**
"Dạ hoàn toàn chạy nổi ạ. Bản chất ChromaDB tìm kiếm vector dựa trên thuật toán HNSW (Hierarchical Navigable Small World) - một thuật toán tìm kiếm trên đồ thị có độ phức tạp là O(log N).
Nghĩa là dù tăng từ 86 tệp lên 10.000 tệp, tốc độ truy xuất vẫn cực kỳ nhanh (chỉ tăng thêm vài ms). Giới hạn duy nhất là dung lượng RAM của máy chủ để chứa 10.000 vector đó, mà với vector 768 chiều thì 10.000 tệp chỉ chiếm vài MB RAM. Một máy chủ 4GB RAM sinh viên cũng chịu tải dư sức ạ."

## Câu 7: Tại sao lại đánh giá hệ thống bằng "Context Precision" và "Context Recall"? Tại sao không lấy câu trả lời cuối cùng đọc xem đúng hay sai là được?
**Bản chất:** Kiểm tra hiểu biết cốt lõi về quy trình đánh giá RAG (RAGAS).
**Cách trả lời:**
"Dạ nếu chỉ đọc câu trả lời cuối cùng, khi sai mình sẽ không biết LỖI Ở ĐÂU.
- Nếu câu trả lời sai do **tìm tài liệu sai**, thì lỗi nằm ở ChromaDB và Embedding (Lúc này Context Precision/Recall sẽ thấp).
- Nếu tìm tài liệu trúng phóc, mà **LLM vẫn trả lời sai**, thì lỗi nằm ở mô hình Gemini hoặc do Prompt chưa đủ chặt chẽ (Lúc này Faithfulness sẽ thấp).
Đánh giá tách bạch 4 chỉ số này giúp em chẩn đoán chính xác bệnh của hệ thống nằm ở khâu Tìm kiếm (Retrieval) hay khâu Sinh văn bản (Generation) để tối ưu ạ."

## Câu 8: RAG rất hay bị lỗi khi một quy chế có nhiều điều kiện "VÀ / HOẶC" bị cắt làm đôi (Chunking Conflict). Em xử lý lỗi này như thế nào?
**Bản chất:** GVPB muốn kiểm tra kiến thức về các giới hạn của Chunking truyền thống và cách tinh chỉnh (Fine-tune RAG).
**Cách trả lời:**
"Dạ đúng ạ, đây là nhược điểm rất phổ biến của RAG. Khi quy chế ghi 'Thí sinh được xét tuyển thẳng nếu là HS chuyên VÀ có IELTS 6.5', do thuật toán chia nhỏ dữ liệu, đoạn văn có thể bị cắt làm đôi khiến AI chỉ đọc được vế đầu và trả lời thiếu điều kiện.
Trong đồ án này, em khắc phục bằng kỹ thuật **Chunk Overlap**. Khi cắt tài liệu, em cấu hình (chunk_size=1000, chunk_overlap=200) để các mảnh ghép tự động lặp lại 200 ký tự giáp lai. Điều này giúp giữ lại 'chiếc cầu nối' ngữ cảnh vắt ngang qua vết cắt. Về dài hạn, hướng phát triển tương lai lý tưởng nhất là nâng cấp lên GraphRAG (Đồ thị tri thức) để lưu các điều kiện dưới dạng logic mạng lưới ạ."

## Câu 9: Tại sao khi em chat trên giao diện Web thì chữ hiện ra từ từ rất mượt, nhưng chat trên Zalo thì lại phải đợi 3-4 giây mới hiện ra cả khối văn bản? Có phải bot Zalo bị lag không?
**Bản chất:** Phân biệt kiến trúc Stream (Server-Sent Events) và kiến trúc Webhook.
**Cách trả lời:**
"Dạ hoàn toàn không phải do lag, mà là chủ đích thiết kế do sự khác biệt về hạ tầng kết nối ạ. 
Trên Web, em kiểm soát toàn bộ luồng kết nối nên em áp dụng công nghệ **Server-Sent Events (SSE)**. Khác với HTTP bình thường, SSE đẩy dữ liệu dạng suối (chunked stream). AI sinh ra chữ nào là trình duyệt Web nhận và in ra ngay.
Ngược lại, Zalo Bot hoạt động thông qua hệ thống Webhook của Zalo. Zalo API bắt buộc hệ thống của em phải đóng gói gửi nguyên một cụm tin nhắn hoàn chỉnh trong 1 lần POST request. Do vậy, backend của em phải chịu khó đợi AI gõ xong 100% rồi mới gửi sang Zalo, tạo ra độ trễ vài giây để đánh đổi lấy sự tiện lợi của ứng dụng Zalo ạ."

## Câu 10: Trong đồ án, em dùng API của Gemini. Lỡ ngày mai Google khóa API ở Việt Nam hoặc bắt đầu thu phí quá đắt, toàn bộ hệ thống của em có phải vứt bỏ làm lại từ đầu không?
**Bản chất:** Đánh giá tính phụ thuộc vào bên thứ 3 (Vendor Lock-in) và kiến trúc mở của hệ thống.
**Cách trả lời:**
"Dạ không ạ. Toàn bộ kiến trúc phần mềm của em được thiết kế theo nguyên lý **Decoupled (Tách rời rạc)** thông qua bộ khung tiêu chuẩn của Langchain. LLM (Gemini) ở đây chỉ đóng vai trò như một 'chiếc não thay thế được' (Pluggable Component).
Nếu sự cố đó xảy ra, em chỉ cần chỉnh sửa đúng 1 dòng khai báo cấu hình để chuyển hệ thống sang dùng OpenAI GPT-4, Claude của Anthropic, hoặc thậm chí triển khai mô hình mã nguồn mở chạy hoàn toàn cục bộ (như Llama-3 hay Qwen) trên server máy chủ của trường mà không cần phải đập bỏ bất cứ logic tìm kiếm (ChromaDB) hay giao diện Zalo nào ạ."
