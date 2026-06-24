# CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 5.1. Tổng kết kết quả đạt được

Nghiên cứu đã hoàn thiện một luồng xử lý End-to-End RAG có tính thực tiễn cao, khắc phục các giới hạn của LLM tĩnh trong bài toán tư vấn tuyển sinh bằng tiếng Việt. Đồ án không chỉ xây dựng thành công bộ đôi giao diện cho người dùng và quản trị viên mà còn ứng dụng các quy chuẩn công nghệ phần mềm tiên tiến nhất để tối ưu hóa kiến trúc.

Cụ thể, hệ thống đã đạt được các cột mốc kỹ thuật xuất sắc:
- Về RPA (Robotic Process Automation), phân hệ Web Scraper đa luồng giải quyết triệt để rào cản cập nhật tài liệu, tự động chuyển đổi mã nguồn trang web thành không gian vector. 
- Về tối ưu hóa tài nguyên, ứng dụng thành công Semantic Cache giúp đẩy tốc độ phản hồi đối với các truy vấn trùng lặp xuống dưới 10ms, tiết kiệm hơn 60 phần trăm chi phí gọi dịch vụ đám mây. 
- Về tính kiên cường, Rate Limit Backoff và cơ chế dự phòng của nền tảng nhắn tin đảm bảo hệ thống không bị treo hoặc rớt tin nhắn dưới áp lực truy vấn khổng lồ. 
- Về quản trị độc lập, việc xây dựng thành công cơ chế xác thực nội bộ và đồng bộ hóa thao tác xóa dữ liệu vật lý với dữ liệu vector đã giải quyết triệt để hiện tượng Knowledge Conflict.

## 5.2. Đánh giá mức độ hoàn thành mục tiêu

Hệ thống hoàn thành xuất sắc các mục tiêu đề ra về hiệu năng và chức năng nền tảng.

| Mục tiêu | Kết quả thực hiện | Đánh giá thực nghiệm |
|----------|-------------------|----------------------|
| Tích hợp ngôn ngữ tự nhiên | Xây dựng lõi xử lý văn bản, xử lý từ lóng, tiếng Việt không dấu. | Answer Relevancy vượt mức 90 phần trăm |
| Tự động hóa tri thức | Phát triển công cụ tự động cào dữ liệu thu thập từ cổng thông tin. | Tiết kiệm 95 phần trăm thời gian nạp tài liệu thủ công |
| Hạn chế bịa đặt thông tin | Khung chỉ thị nghiêm ngặt ép hệ thống từ chối tư vấn nếu không có trong cơ sở dữ liệu. | Đạt độ trung thực 0.89 |
| Đảm bảo tốc độ luồng | Triển khai Semantic Cache và cơ chế Server-Sent Events (SSE). | Trúng đệm giảm trễ còn 8ms, tốc độ luồng dưới 1 giây |

*Bảng 5.1: Đối chiếu kết quả thực hiện so với mục tiêu đề tài*

## 5.3. Hạn chế của hệ thống

Bên cạnh các thành tựu tối ưu hóa máy chủ, kiến trúc của hệ thống vẫn bộc lộ một số giới hạn về mặt xử lý ngôn ngữ tự nhiên sâu.

- Về ngữ cảnh rời rạc (Chunking Conflict), khi học sinh đưa ra một hồ sơ chứa nhiều điều kiện rẽ nhánh như điểm số, chứng chỉ, hoặc ưu tiên vùng miền, RecursiveCharacterTextSplitter vô tình cắt đứt sự liên kết giữa các điều khoản. Hệ quả là hệ thống không thể tổng hợp đủ biến số để đưa ra kết luận tư vấn cuối cùng.
- Về kiến trúc đệm đơn bộ, Semantic Cache hiện tại đang lưu trữ trực tiếp trên cơ sở dữ liệu máy chủ cục bộ. Dù tốc độ rất nhanh, nhưng nếu ứng dụng triển khai theo mô hình phân tán nhiều máy chủ để cân bằng tải, Local Database sẽ không thể đồng bộ hóa bộ nhớ đệm chéo giữa các máy.

## 5.4. Hướng phát triển

Để thương mại hóa và nâng cấp kiến trúc lên quy quy mô lớn hơn, đồ án đề xuất các hướng đi cụ thể.

- Hướng phát triển đầu tiên là kiến trúc GraphRAG. Thay vì chỉ tìm kiếm vector thuần túy, hệ thống sẽ được nâng cấp lên kiến trúc GraphRAG. Việc tích hợp cơ sở dữ liệu đồ thị sẽ cung cấp mạng lưới liên kết biểu diễn các mối quan hệ phức tạp, ví dụ như quan hệ ngành Công nghệ thông tin yêu cầu khối A00 và được cộng điểm chứng chỉ tiếng Anh. Kiến trúc này triệt tiêu hoàn toàn điểm mù khi trả lời câu hỏi điều kiện chéo.
- Hướng phát triển thứ hai là nâng cấp cơ sở hạ tầng đệm. Chuyển đổi lưu trữ đệm ngữ nghĩa từ cục bộ sang hệ thống máy chủ Redis. Điều này cho phép hệ thống triển khai theo Microservices, nhiều máy trạm có thể dùng chung một siêu bộ nhớ đệm, tối ưu cho bài toán Horizontal Scaling.
- Hướng phát triển thứ ba là Autonomous Agent Scraper. Phân hệ thu thập hiện tại sử dụng thuật toán phân tích mã tĩnh. Hệ thống sẽ được trang bị Multi-Agent, trong đó AI sẽ tự động học cách điều hướng các cổng thông tin thay đổi cấu trúc mã nguồn liên tục, biến hệ thống thu thập tri thức thành một quy trình hoàn toàn tự trị.

---

# TÀI LIỆU THAM KHẢO

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS*, 2020.
[2] A. Vaswani et al., "Attention Is All You Need," *NeurIPS*, 2017.
[3] Y. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey," *arXiv preprint*, 2024.
[4] J. Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," *NAACL*, 2019.
[5] S. Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation," *arXiv preprint*, 2023.
[6] LangChain AI, "LangChain Documentation," 2024. [Online]. Available: https://python.langchain.com.
[7] Chroma, "ChromaDB Documentation," 2024. [Online]. Available: https://docs.trychroma.com.
[8] Google, "Google Gemini API Reference," 2024. [Online]. Available: https://ai.google.dev.
[9] Trường Đại học Thủy Lợi, "Đề án tuyển sinh trình độ đại học," 2020-2024. [Online]. Available: http://tuyensinh.tlu.edu.vn.
[10] L. Page and M. Gehlbach, "How an artificially intelligent virtual assistant helps students navigate the road to college," *AERA Open*, vol. 3, no. 4, 2017.
