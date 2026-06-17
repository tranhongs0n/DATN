# THÔNG TIN BỐI CẢNH DỰ ÁN (PROJECT CONTEXT)

File này lưu trữ các thông tin cốt lõi của dự án để đảm bảo tính nhất quán trong toàn bộ quá trình viết báo cáo đồ án tốt nghiệp.

## 1. Thông tin chung
- **Tên đề tài:** Xây dựng hệ thống Chatbot tư vấn tuyển sinh (Virtual Assistant) dựa trên kiến trúc RAG.
- **Sinh viên thực hiện:** Trần Hồng Sơn (Lớp: 61TH1)
- **Giảng viên hướng dẫn:** TS. Lê Anh Tuấn
- **Lĩnh vực nghiên cứu:** Trí tuệ nhân tạo (AI), Xử lý ngôn ngữ tự nhiên (NLP), Trợ lý ảo (Chatbot).

## 2. Công nghệ & Nền tảng cốt lõi
- **Platform:** Nền tảng nhắn tin Zalo Bot (Giao diện duy nhất cho người dùng cuối) và Bảng điều khiển quản trị trên nền Web. Không sử dụng Webchat.
- **Technology Stack:**
    - **Ngôn ngữ/Framework:** Python, FastAPI.
    - **Orchestration:** LangChain.
    - **Vector Database:** ChromaDB.
    - **LLM & Embedding:** Google Gemini API (gemini-3-flash-preview, gemini-embedding-2).
- **Kỹ thuật xử lý ngôn ngữ cốt lõi:** RAG (Retrieval-Augmented Generation) kết hợp với các LLM.
- **Cơ sở dữ liệu (Database):** Cơ sở dữ liệu dạng vector dùng để lưu trữ và truy xuất ngữ nghĩa (Knowledge Base).
- **Nền tảng tích hợp (Frontend/Giao diện người dùng):** Zalo Bot (Lưu ý: Trợ lý ảo được tích hợp trực tiếp dưới dạng Zalo Bot, không gọi là Zalo OA Bot).
- **Nguồn dữ liệu:** Dữ liệu tuyển sinh chính thức của Trường Đại học Thủy Lợi (thông báo điểm chuẩn, quy chế, thông tin ngành học).
