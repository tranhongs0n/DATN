# GATHERED INFORMATION FOR THESIS DECLARATION

This file contains the consolidated information extracted from the thesis PDF `DATN_1951060985_TranHongSon.pdf` and the codebase.

## 1. General Information
- **Student Name (Sinh viên):** Trần Hồng Sơn
- **Student ID (MSSV):** 1951060985
- **Class (Lớp):** 61TH1
- **Department/Major (Ngành):** Công nghệ thông tin, Khoa Công nghệ thông tin, Trường Đại học Thủy Lợi.
- **Thesis Advisor (GVHD):** TS. Lý Anh Tuấn
- **Reviewer (GVPB):** (Keep blank for department assignment)
- **Thesis Title (Tên đề tài):** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG
- **Implementation Period (Thời gian thực hiện):** 31/03/2026 - 30/06/2026
- **Submission Date (Ngày nộp bản tự đánh giá):** 30/06/2026
- **Target Users (Đối tượng sử dụng):** Thí sinh, phụ huynh tra cứu thông tin; Ban tuyển sinh Trường Đại học Thủy Lợi quản trị dữ liệu.
- **Core Technologies (Công nghệ chính):** Python, FastAPI, LangChain, ChromaDB, Google Gemini (gemini-embedding-2, Gemini API), Zalo OA API, React, SQLite.

---

## 2. Details for Steps (1 to 8)

### BƯỚC 1: NGỰ CẢNH & BÀI TOÁN (Context & Scope)
- **Bối cảnh & Bài toán:** Công tác tư vấn tuyển sinh tại Trường Đại học Thủy Lợi đòi hỏi giải đáp lượng thông tin lớn, đa dạng ở nhiều bậc đào tạo (Đại học, Thạc sĩ, Tiến sĩ). Các quy chế tuyển sinh gồm nhiều văn bản phức tạp (86 tệp tài liệu gốc).
- **Hiện trạng:** Việc tư vấn thủ công tốn thời gian, dễ sai sót hoặc không cập nhật kịp thời các thay đổi quy chế tuyển sinh hàng năm.
- **Tác động:** Trễ hạn thông tin, quá tải nhân sự mùa tuyển sinh, học sinh/phụ huynh khó tiếp cận thông tin chính thức nhanh chóng.
- **Phạm vi (In-scope/Out-of-scope):**
  - *In-scope:* Tư vấn tự động thông tin tuyển sinh Đại học, Thạc sĩ, Tiến sĩ của TLU dựa trên kho quy chế chính thức; quản trị tài liệu, thu thập tin tuyển sinh tự động trên web trường, quản lý từ viết tắt/từ lóng.
  - *Out-of-scope:* Không tư vấn các thông tin ngoài lề, không tự động quyết định xét tuyển, không hỗ trợ ngoài các văn bản chính thức được nạp vào hệ thống.

### BƯỚC 2: VẤN ĐỀ CỐT LÕI (Pain Points)
- **Vấn đề cốt lõi:**
  1. Trì trệ cập nhật dữ liệu tuyển sinh do văn bản thay đổi hàng năm.
  2. Hiện tượng ảo giác (hallucination) của LLM thông thường dẫn đến trả lời sai quy chế học thuật/tuyển sinh.
  3. Chi phí gọi API LLM lớn và tốc độ phản hồi chậm khi phục vụ số lượng lớn thí sinh.
  4. Ngôn ngữ tự do của thí sinh (từ viết tắt như "cntt", từ lóng, tiếng Việt không dấu) làm giảm độ chính xác truy xuất ngữ nghĩa.

### BƯỚC 3: MỤC TIÊU (Objectives)
- **Mục tiêu hệ thống:** Xây dựng hệ thống trợ lý ảo tuyển sinh dựa trên RAG hoạt động đa nền tảng (Zalo, Web Admin) ổn định, chính xác, bảo mật.
- **Chỉ số đo lường cụ thể:**
  - *Chất lượng câu trả lời:* Answer Relevance > 90% (vượt mức 0.90), Faithfulness (độ trung thực chống ảo giác) đạt 0.89, Context Precision > 86%.
  - *Hiệu năng:* Độ trễ truy vấn trúng đệm (Semantic Cache) đạt 8ms, tiết kiệm 62% chi phí gọi API. Tốc độ truyền streaming SSE dưới 1 giây.
  - *Tự động hóa:* Tiết kiệm 95% thời gian nạp tài liệu thủ công nhờ Web Scraper tự động.
  - *An toàn thông tin:* Chặn 95% câu hỏi ngoài phạm vi nghiệp vụ tuyển sinh.
- **Mục tiêu bắt buộc:** Pipeline RAG tiếng Việt, Chatbot Zalo OA, Web Admin Dashboard quản lý tài liệu & từ viết tắt, Semantic Cache, JWT Authentication.
- **Mục tiêu mở rộng:** Nâng cấp GraphRAG, phân quyền chi tiết, lưu trữ đệm Redis phân tán.

### BƯỚC 4: RÀNG BUỘC (Constraints)
- **Ràng buộc kỹ thuật:** Python 3.10+, FastAPI backend, ChromaDB cục bộ (độ trễ mạng bằng 0), sử dụng Google Gemini API.
- **Ràng buộc dữ liệu:** Chỉ sử dụng 86 văn bản quy chế chính thức của TLU (38 tệp Đại học, 36 tệp Thạc sĩ, 12 tệp Tiến sĩ). Bảo vệ dữ liệu hội thoại và thông tin cá nhân.
- **Ràng buộc bảo mật:** Xác thực cán bộ qua JWT stateless (hết hạn sau 24 giờ), ghi vết hoạt động (Audit Logging), Rule Engine lọc câu hỏi độc hại/ngoài phạm vi.
- **Loại trừ:** Không hỗ trợ điều khiển thiết bị từ xa, không thu thập dữ liệu cá nhân nhạy cảm ngoài thông tin hội thoại tư vấn.

### BƯỚC 5: GIẢI PHÁP / CÁCH LÀM (Method & Architecture)
- **Kiến trúc hệ thống:** Mô hình RAG End-to-End gồm 3 phân hệ chính:
  1. *Web Scraper đa luồng:* Tự động thu thập bài viết tuyển sinh, chuyển đổi trang web không tệp đính kèm thành tệp Word cấu trúc.
  2. *Pipeline RAG:* LangChain điều phối luồng, chia văn bản bằng `RecursiveCharacterTextSplitter`, tạo vector nhúng bằng mô hình `gemini-embedding-2` (768 chiều), lưu trữ CSDL vector ChromaDB cục bộ.
  3. *Tầng API & Giao diện:* FastAPI backend hỗ trợ Server-Sent Events (SSE) cho streaming; tích hợp Zalo OA API; Web Admin Dashboard (React, SQLite) để quản lý tài liệu, từ điển viết tắt, tài khoản và kiểm thử (Chat Tester, Query Test).
- **Cơ chế tối ưu cốt lõi:**
  - *Semantic Cache:* Đo độ tương đồng vector câu hỏi bằng Dot Product & Norm, bỏ qua gọi API nếu trùng lặp ngữ nghĩa (trễ 8ms).
  - *Rate Limit Backoff:* Tự động bắt lỗi API quá tải, thử lại tối đa 3 lần.
- **Phần sinh viên tự làm:** Phân tích, thiết kế kiến trúc RAG, phát triển Web Scraper đa luồng, thiết lập pipeline xử lý từ viết tắt, cài đặt Semantic Cache, tích hợp Zalo OA, xây dựng Web Admin Dashboard và viết toàn bộ backend API.
- **Điểm mới:** Kết hợp Semantic Cache cục bộ giúp giảm chi phí và độ trễ vượt trội, kết hợp Web Scraper tự động chuyển đổi trang web thành tài liệu cấu trúc đồng bộ vector DB.

### BƯỚC 6: ĐÁNH GIÁ / KIỂM CHỨNG (Evaluation)
- **Kịch bản kiểm thử:** Đánh giá trên tập dữ liệu chuẩn 1200 cặp câu hỏi/câu trả lời gán nhãn từ 86 văn bản gốc, chia làm 5 nhóm truy vấn (tra cứu đơn lẻ, từ lóng viết tắt, logic phức hợp, ngoài phạm vi, đa bậc đào tạo).
- **Chỉ số kết quả:**
  - Nhóm 1 (tra cứu đơn lẻ): Context Precision 0.94, Context Recall 0.98, Faithfulness 0.96, Answer Relevancy 0.95.
  - Nhóm 2 (từ lóng viết tắt): Context Precision 0.90, Context Recall 0.92, Faithfulness 0.89, Answer Relevancy 0.91.
  - Nhóm 3 (logic phức hợp): Context Precision 0.88, Context Recall 0.85, Faithfulness 0.91, Answer Relevancy 0.88.
  - Nhóm 4 (ngoài phạm vi): Từ chối 95% câu hỏi ngoài lề (Answer Relevancy 0.95).
  - Nhóm 5 (đa bậc): Context Precision 0.86, Context Recall 0.82, Faithfulness 0.89, Answer Relevancy 0.85.
- **Kiểm thử hiệu năng:**
  - Semantic Cache: Trúng đệm 100% đối với câu hỏi tương đồng cao (trễ 8ms, 0% chi phí API). Thực tế trúng đệm ~62% (trễ trung bình 950ms).
  - Thử nghiệm chịu tải: Ép tải 2000 luồng đồng thời, tỷ lệ vận hành thành công >99% nhờ cơ chế tự động chờ Rate Limit.
- **Minh chứng:** File log CSV 5 nhóm kiểm thử, video demo hoạt động, ảnh chụp dashboard admin và giao diện chat Zalo OA.

### BƯỚC 7: ĐÓNG GÓP & GIÁ TRỊ THỰC (Impact)
- **Đóng góp:** Hoàn thiện giải pháp trợ lý ảo tuyển sinh RAG tối ưu hóa cho tiếng Việt và bối cảnh quy chế trường đại học.
- **Giá trị thực tiễn:** Tiết kiệm 95% công sức cập nhật tài liệu cho ban tuyển sinh. Giúp thí sinh tra cứu tức thì thông tin chính thống với độ trễ thấp và độ tin cậy cao (~89% độ trung thực).
- **Hạn chế:** Ngữ cảnh bị phân mảnh khi chia văn bản (Chunking Conflict) đối với các câu hỏi logic rẽ nhánh quá phức tạp; Semantic Cache lưu cục bộ chưa tối ưu cho cân bằng tải đa máy chủ.
- **Hướng phát triển:** Nâng cấp lên GraphRAG giải quyết câu hỏi điều kiện chéo; chuyển Semantic Cache sang Redis; phát triển Autonomous Agent Scraper.

### BƯỚC 8: TỰ ĐÁNH GIÁ & CAM KẾT (Self-assessment)
- **Tỷ lệ tham khảo/kế thừa:** 30% (mã nguồn mở LangChain, thư viện ChromaDB, giao diện mẫu React, SDK Google Gemini).
- **Tỷ lệ tự làm/đóng góp:** 70% (logic Web Scraper, xử lý từ viết tắt, cơ chế Semantic Cache cục bộ, tích hợp Zalo OA, thiết kế hệ thống API, xây dựng kịch bản và thực hiện đánh giá).
- **Mức độ tự hiểu:** 95% (tự tin giải thích kiến trúc RAG, luồng dữ liệu SSE, giải thuật so khớp vector đệm, và nguyên nhân giới hạn Chunking).
- **Cam kết:** Cam kết học thuật trung thực, chịu trách nhiệm hoàn toàn về tỷ lệ tự làm và tính chính xác của dữ liệu thực nghiệm.
