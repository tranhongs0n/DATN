# CẤU TRÚC SLIDE BẢO VỆ (Cập nhật - 17 Slide, 10 Phút)

Slide đã được giãn cách thành 17 trang để không bị nhồi nhét chữ, đảm bảo mỗi trang chiếu khoảng 30-40 giây.

## Slide 1: Trang bìa
- Thông tin đề tài, SV, GVHD.

## Slide 2: Đặt vấn đề thực tiễn
- Lượng thông tin tuyển sinh lớn, thay đổi liên tục.
- Cán bộ quá tải, thí sinh đợi lâu. LLM bị ảo giác.

## Slide 3: Mục tiêu hệ thống
- Tự động hóa 24/7 trên Zalo. Chặn câu hỏi ngoài lề.
- Ứng dụng RAG, Web Scraper và Web Admin.

## Slide 4: Công nghệ sử dụng
- Gemini, ChromaDB, LangChain.
- FastAPI, ReactJS, Zalo Bot, SQLite.

## Slide 5: Phân tích thiết kế - Biểu đồ Use Case
- 2 Actor: Thí sinh và Ban tuyển sinh.

## Slide 6: Phân tích thiết kế - Biểu đồ Hoạt động
- Luồng xử lý tin nhắn Zalo có Rule Engine.

## Slide 7: Phân tích thiết kế - Biểu đồ Tuần tự
- Giao tiếp bất đồng bộ Zalo - FastAPI - ChromaDB - Gemini.

## Slide 8: Thiết kế Cơ sở dữ liệu Quản trị
- 4 bảng SQLite: USERS, DOCUMENTS, DICTIONARIES, CHAT_LOGS.

## Slide 9: Kiến trúc RAG Pipeline
- 3 bước: Embedding -> Retrieval -> Generation.

## Slide 10: Tự động hóa Dữ liệu
- Web Scraper & thuật toán Chunking. Vấn đề phân mảnh.

## Slide 11: Thuật toán tối ưu: Semantic Cache (Giới thiệu)
- Tránh gọi API liên tục. Dùng Tích vô hướng so sánh câu hỏi cũ.

## Slide 12: Đánh giá hiệu năng Semantic Cache
- Giảm trễ từ 2400ms xuống 8ms. Tiết kiệm 62% chi phí.

## Slide 13: Phương pháp đánh giá mô hình AI
- 4 chỉ số RAGAS trên 1200 mẫu test.

## Slide 14: Kết quả thực nghiệm RAGAS
- Precision 0.94, Faithfulness 0.89. 

## Slide 15: Giao diện thực tế
- Ảnh chụp Zalo Bot và Web Admin.

## Slide 16: Hạn chế & Hướng phát triển
- GraphRAG, Redis, đa nền tảng.

## Slide 17: Q&A
- Cảm ơn và chuyển sang Demo.
