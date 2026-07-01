# RAGAS Metrics - Chỉ số đo lường chất lượng

Để chứng minh chatbot thông minh, đồ án dùng tập 1200 câu hỏi và đo lường 4 chỉ số sau:

## 1. Context Precision (Độ chính xác của ngữ cảnh - 0.94)
- **Câu hỏi đặt ra:** Các tài liệu ChromaDB tìm ra có bị "rác" không? 
- **Giải thích:** Đạt 0.94 tức là 94% các đoạn văn bản DB móc lên là trúng phóc thông tin cần thiết.

## 2. Context Recall (Độ bao phủ của ngữ cảnh - 0.98)
- **Câu hỏi đặt ra:** Tài liệu tìm được có ĐỦ thông tin không hay bị thiếu hụt?
- **Giải thích:** Đạt 0.98 cho câu hỏi đơn lẻ là rất cao. Nhưng với câu hỏi "logic phức hợp", chỉ số này tụt xuống 0.85 (do lỗi Chunking Conflict).

## 3. Faithfulness (Độ trung thực - 0.89)
- **Câu hỏi đặt ra:** LLM có bịa chuyện không?
- **Giải thích:** Câu trả lời của LLM được đối chiếu ngược lại với tài liệu. 0.89 nghĩa là hầu như chatbot bám sát 100% tài liệu nhà trường cung cấp.

## 4. Answer Relevancy (Độ phù hợp của câu trả lời)
- **Câu hỏi đặt ra:** Trả lời có đúng trọng tâm không?
- **Giải thích:** Đôi khi LLM trả lời dài dòng lan man. Chỉ số này đảm bảo LLM trả lời đúng thẳng vào vấn đề thí sinh hỏi.
