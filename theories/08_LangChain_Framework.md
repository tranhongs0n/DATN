# LangChain Framework - Xương sống của hệ thống AI

Nhiều người thắc mắc: *"Nếu chỉ cần gọi AI trả lời, tại sao không dùng hàm `requests.post()` gọi thẳng API của Gemini cho nhanh mà phải cài thêm một bộ khung (Framework) nặng nề mang tên LangChain làm gì?"* 

Dưới đây là lý thuyết và cách ứng dụng thực tế của LangChain trong dự án này:

## 1. LangChain là gì?
- **Định nghĩa:** LangChain là một framework mã nguồn mở được thiết kế đặc biệt để giúp các lập trình viên xây dựng ứng dụng xoay quanh các Mô hình Ngôn ngữ Lớn (LLMs) dễ dàng hơn.
- **Vai trò:** Nó đóng vai trò như một "chất keo kết dính" (Glue code) tiêu chuẩn hóa. Thay vì bạn phải tự viết hàng trăm dòng code phức tạp để LLM nói chuyện được với Database, đọc được file PDF/Word, hay ghi nhớ được lịch sử chat, LangChain cung cấp sẵn các module đã được tối ưu hóa để làm việc đó.

## 2. Lý thuyết cốt lõi: Kiến trúc Tách rời (Decoupled Architecture)
- Lợi ích lớn nhất của LangChain là giúp hệ thống của bạn **không bị phụ thuộc (Vendor Lock-in)** vào một nhà cung cấp AI nào.
- Nếu bạn code "chết" bằng SDK riêng của Google, ngày mai nếu muốn chuyển sang dùng OpenAI ChatGPT, bạn sẽ phải đập đi viết lại toàn bộ luồng RAG.
- Nhưng nhờ LangChain, dự án này chỉ gọi LLM qua một giao diện chung (Interface). Việc khai báo `ChatGoogleGenerativeAI` giúp gắn não Gemini vào dự án. Nếu muốn đổi sang ChatGPT, bạn chỉ cần thay thành `ChatOpenAI`. Toàn bộ luồng tìm kiếm ChromaDB, thao tác nhúng (Embedding), cắt văn bản (Chunking) ở bên dưới vẫn tương thích và giữ nguyên 100%.

## 3. LangChain được ứng dụng làm gì trong dự án này?
Dựa vào mã nguồn của dự án (cụ thể tại thư mục `src/core/`), LangChain được sử dụng để gánh vác 4 nhiệm vụ cốt lõi:

### A. Phân mảnh văn bản thông minh (Text Splitting)
- **Vấn đề:** Không thể nhồi nguyên 1 file quy chế 50 trang vào Gemini vì sẽ làm tràn bộ nhớ (vượt giới hạn Context Window).
- **Giải pháp:** Sử dụng hàm `RecursiveCharacterTextSplitter` của LangChain.
- **Lý thuyết hoạt động:** Thuật toán "Recursive" (Đệ quy) của LangChain rất thông minh. Khác với việc cắt mù quáng cứ đủ 1000 chữ là chặt đứt, nó sẽ ưu tiên tìm dấu ngắt đoạn `\n\n`, sau đó đến dấu chấm câu `.`, và cuối cùng mới đến dấu cách để cắt. Điều này đảm bảo việc chia nhỏ tài liệu không phá vỡ tính vẹn toàn ý nghĩa của một câu.

### B. Quản lý Nhúng và Vector (Embeddings & Retrievers)
- Dự án sử dụng `GoogleGenerativeAIEmbeddings` của LangChain để biến văn bản chữ cái thành các vector không gian (768 chiều).
- Dùng module `langchain_chroma` để tự động hóa việc giao tiếp với cơ sở dữ liệu ChromaDB. 
- Thay vì phải tự viết các câu lệnh truy vấn phức tạp, LangChain cung cấp cơ chế `Retriever`. Hàm `vector_db.as_retriever(search_kwargs={"k": 5})` tự động thực hiện phép toán Cosine Similarity và lấy ra 5 văn bản giống với câu hỏi của thí sinh nhất.

### C. Khuôn mẫu Nhắc việc (Prompt Templates)
- LangChain cung cấp `PromptTemplate` để "đóng gói" câu hỏi của thí sinh vào một cái khuôn (template) được tinh chỉnh trước khi gửi cho AI. 
- Nhờ cái khuôn này, hệ thống dễ dàng nhét thêm **Ngữ cảnh (Context)** tìm từ ChromaDB và **Bộ quy tắc ứng xử (Guardrails)** (VD: *Cấm sinh markdown cho Zalo, không trả lời chuyện chính trị*) vào cùng một lúc một cách có cấu trúc rõ ràng.

### D. Truyền phát Thời gian thực (Streaming)
- Thay vì bắt hệ thống phải chờ đợi AI viết xong 100% câu trả lời rồi mới trả về (mất 2-4 giây gây cảm giác giật lag), dự án tận dụng cơ chế `stream()` của LangChain. 
- Nó cho phép backend bắt được từng từ (token) mà AI vừa suy nghĩ ra và đẩy ngay lập tức về giao diện Web (thông qua SSE). Việc này mang lại trải nghiệm chữ chạy mượt mà theo thời gian thực giống hệt như ChatGPT.
