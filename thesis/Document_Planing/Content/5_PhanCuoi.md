# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## Lời cảm ơn

Em xin chân thành cảm ơn TS. Lý Anh Tuấn đã dành nhiều thời gian và tâm huyết hướng dẫn em thực hiện đồ án này. Những định hướng kiến trúc và phân tích thuật toán từ thầy là tiền đề quan trọng giúp em hoàn thiện hệ thống.

Em cũng gửi lời tri ân đến các thầy cô khoa Công nghệ thông tin, Trường Đại học Thủy Lợi vì nền tảng kiến thức quý báu trong 4 năm học. Trân trọng cảm ơn Hội đồng bảo vệ đã dành thời gian đánh giá và cho em cơ hội trình bày kết quả nghiên cứu.

---

# TÓM TẮT ĐỒ ÁN

**Đề tài:** Nghiên cứu và xây dựng hệ thống trợ lý ảo hỗ trợ tuyển sinh cho Trường Đại học Thủy Lợi dựa trên kỹ thuật RAG
**Sinh viên:** Trần Hồng Sơn (61TH1)
**GVHD:** TS. Lý Anh Tuấn

Đề tài tập trung thiết kế và phát triển hệ thống trợ lý ảo hỗ trợ công tác tư vấn tuyển sinh tại Trường Đại học Thủy Lợi, hướng tới mục tiêu tự động hóa việc giải đáp thông tin đa phân luồng. Triển khai cơ chế phân tách và lập chỉ mục đa luồng, hỗ trợ chuyển đổi linh hoạt các định dạng văn bản (PDF, DOCX) thành cơ sở dữ liệu vector. Hệ thống truy xuất nhanh chóng các điều khoản quy định giáo dục mà không phá vỡ cấu trúc ngữ nghĩa gốc.

Mô hình thiết kế khung chỉ thị cá nhân hóa trên lõi Google Gemini, bắt buộc mạng nơ-ron trả lời dựa trên tài liệu cung cấp. Hệ thống giải quyết tốt bài toán lọc câu hỏi ngoài phạm vi nghiệp vụ giáo dục nhằm ngăn chặn hiện tượng cung cấp thông tin sai lệch ngoài dữ liệu gốc của nhà trường.

Cấu trúc đồ án gồm 4 chương. Chương 1 trình bày cơ sở lý thuyết về bài toán hỏi đáp và mô hình RAG. Chương 2 phân tích yêu cầu thiết kế hệ thống. Chương 3 triển khai các luồng xử lý kỹ thuật trên máy chủ FastAPI. Chương 4 thiết lập kịch bản đánh giá để kiểm thử năng lực truy xuất, tốc độ phản hồi và khả năng phòng chống thông tin ảo giác của hệ thống.

---

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1. Tổng kết kết quả đạt được
Nghiên cứu hoàn thiện luồng xử lý từ khâu thu thập tri thức đến khâu tương tác người dùng. Hệ thống làm rõ cơ chế RAG trong việc khắc phục điểm yếu của LLM khi xử lý quy chế tuyển sinh tiếng Việt. Đồ án xây dựng thành công hai phân hệ giao diện: Zalo Bot hỗ trợ tra cứu và Web Dashboard phục vụ quản trị dữ liệu nội bộ.

## 2. Đánh giá mức độ hoàn thành mục tiêu
Hệ thống hoàn thành phần lớn các yêu cầu đề ra đối với chức năng hỏi đáp tư vấn, nhưng vẫn bộc lộ một số giới hạn kỹ thuật trong các kịch bản tra cứu phức tạp.

| Mục tiêu | Kết quả thực hiện | Đánh giá thực nghiệm |
|----------|-------------------|----------------------|
| Tích hợp ngôn ngữ tự nhiên vào tuyển sinh | Xây dựng lõi giao tiếp RAG với Zalo OA, xử lý triệt để ngôn ngữ viết tắt, không dấu. | Đạt độ chính xác ngữ nghĩa > 90% theo Ragas |
| Tổ chức dữ liệu đa cấp độ | Phân rã và lưu trữ thành công 86 tài liệu; phân vùng không gian tìm kiếm độc lập theo bậc đào tạo. | Lưu trữ và lập chỉ mục 100% tài liệu nội bộ |
| Hạn chế ảo giác trong tư vấn | Khung chỉ thị từ chối tốt dữ liệu ngoài phạm vi, nhưng vẫn xuất hiện sai lệch ở các truy vấn điều kiện chéo phức tạp. | Đáp ứng Faithfulness 0.89 |
| Đảm bảo tốc độ phản hồi | Tích hợp luồng dòng sự kiện liên tục, duy trì độ trễ ổn định trong môi trường xử lý đơn lẻ. | Độ trễ phản hồi trung bình < 3s |
| Xử lý cấu trúc dữ liệu đa phương thức | Xây dựng đường ống xử lý ảnh 3 bước: phát hiện viền bảng bằng thư viện thị giác máy tính, bóc tách vùng chữ và gọi OCR để tái tạo cấu trúc Markdown. | Sai số nhận diện < 5% |

*Bảng 5.1: Đối chiếu kết quả thực hiện so với mục tiêu đề tài*

## 3. Hạn chế của đề tài

Khi xử lý các truy vấn chứa nhiều mệnh đề điều kiện, độ chính xác của tài liệu truy xuất bị suy giảm đáng kể. Cấu trúc chia cắt cố định vô tình cắt đứt sự liên kết giữa các điều khoản liên quan, dẫn đến tình trạng mất định hướng ngữ cảnh khi người dùng đặt câu hỏi dài. Giới hạn bộ nhớ của hàng đợi tin nhắn chưa được tối ưu triệt để. Trong phiên làm việc kéo dài, mô hình bắt đầu mất dần bộ nhớ về những thông tin cung cấp ở đầu phiên do cơ chế cắt tỉa lược sử chưa tính toán tỷ trọng tương quan ngữ nghĩa.

## 4. Hướng phát triển

Để khắc phục các rào cản kỹ thuật, hệ thống cần được nâng cấp kiến trúc truy xuất nhiều giai đoạn. Phương pháp này sẽ ứng dụng mô hình nhúng kép để vừa tìm kiếm thô diện rộng, vừa tính toán lại điểm tương quan chính xác ở bước cuối.

Thuật toán cắt rã tài liệu cần chuyển dịch sang kỹ thuật phân mảnh theo cấu trúc ngữ nghĩa thay vì phụ thuộc hoàn toàn vào số lượng ký tự tĩnh. Việc nâng cấp đường ống tích hợp đồ thị tri thức sẽ cung cấp mạng lưới liên kết chặt chẽ giữa các điều kiện tuyển sinh phức tạp, triệt tiêu tận gốc hiện tượng suy giảm hiệu năng trên câu hỏi chuỗi. Dự án định hướng mở rộng hệ thống RAG để hỗ trợ các mảng cố vấn học tập và quy chế học vụ, mang lại giải pháp tự động hóa toàn diện cho người học.

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
