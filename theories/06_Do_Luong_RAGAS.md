# RAGAS Metrics - Khung Đo Lường Chất Lượng RAG

Để chứng minh hệ thống AI không chỉ "nói bừa" mà thực sự thông minh và chính xác, đồ án sử dụng bộ 1200 câu hỏi và khung đo lường **RAGAS (Retrieval Augmented Generation Assessment)**. RAGAS là tiêu chuẩn ngành hiện nay để đánh giá hệ thống RAG độc lập trên từng thành phần (Truy xuất và Sinh văn bản) mà không cần dữ liệu nhãn thủ công phức tạp (sử dụng LLM-as-a-judge).

Dưới đây là lý thuyết chuyên sâu và cách tính toán 4 chỉ số cốt lõi:

## 1. Context Precision (Độ chính xác của ngữ cảnh - 0.94)
- **Ý nghĩa:** Đo lường tỷ lệ tín hiệu trên nhiễu (Signal-to-Noise Ratio) của VectorDB (ChromaDB). Nó trả lời câu hỏi: *"Trong các tài liệu móc lên được, có bị lẫn rác không? Các tài liệu đúng có được xếp hạng ưu tiên lên đầu không?"*
- **Cách tính toán (Toán học):** Chỉ số này phạt rất nặng nếu các tài liệu không liên quan (rác) chiếm chỗ ở các vị trí Top 1, Top 2. 
  - Ragas sử dụng một LLM độc lập để đọc từng chunk được truy xuất và dán nhãn `1` (có liên quan) hoặc `0` (không liên quan).
  - Công thức tính dựa trên độ đo `Precision@K`.
- **Giải thích con số 0.94:** Đạt 0.94 tức là 94% các đoạn văn bản mà ChromaDB truy xuất và xếp hạng ở trên cùng là thông tin chính xác, không chứa dữ liệu thừa, giúp LLM không bị rối.

## 2. Context Recall (Độ bao phủ của ngữ cảnh - 0.98)
- **Ý nghĩa:** Đo lường xem VectorDB có tìm **ĐỦ** thông tin hay không. Nó trả lời câu hỏi: *"Hệ thống có vô tình bỏ sót tài liệu quan trọng nào cần thiết để giải quyết câu hỏi không?"*
- **Cách tính toán:**
  - Ragas so sánh **Ground Truth** (Câu trả lời tham chiếu chuẩn) với các tài liệu truy xuất được.
  - LLM sẽ chia Ground Truth thành các câu nhận định nhỏ (statements).
  - Công thức: `Context Recall = (Số lượng câu nhận định có thể tìm thấy trong Context) / (Tổng số câu nhận định trong Ground Truth)`.
- **Giải thích con số 0.98:** 0.98 là một con số gần như tuyệt đối, chứng tỏ với các câu hỏi đơn lẻ, ChromaDB luôn móc lên đủ dữ liệu. Tuy nhiên, với câu hỏi "logic phức hợp" nhiều vế, chỉ số này có thể tụt xuống 0.85 do hiện tượng **Chunking Conflict** (câu điều kiện bị cắt làm đôi và nằm ở 2 chunk khác nhau).

## 3. Faithfulness (Độ trung thực - 0.89)
- **Ý nghĩa:** Đo lường mức độ "ảo giác" (Hallucination) của LLM. Nó trả lời câu hỏi: *"Mô hình AI có đang bịa chuyện, tự suy diễn thông tin ngoài tài liệu nhà trường cung cấp hay không?"*
- **Cách tính toán:**
  - Bước 1: LLM trích xuất toàn bộ các khẳng định (claims) từ câu trả lời mà AI sinh ra.
  - Bước 2: LLM đối chiếu từng khẳng định đó với tập tài liệu (Context) đã được truy xuất.
  - Công thức: `Faithfulness = (Số lượng khẳng định được Context hỗ trợ) / (Tổng số khẳng định AI tạo ra)`.
- **Giải thích con số 0.89:** Con số này có nghĩa là 89% nội dung chatbot phát ngôn có thể truy xuất ngược lại chính xác từng chữ trong tài liệu quy chế gốc. 11% còn lại có thể là các câu chào hỏi, suy diễn từ ngữ tương đương hoặc lỗi ảo giác nhẹ.

## 4. Answer Relevancy (Độ phù hợp của câu trả lời)
- **Ý nghĩa:** Đo lường xem câu trả lời có đi thẳng vào trọng tâm câu hỏi hay không, tránh tình trạng "hỏi một đằng, trả lời dài dòng một nẻo".
- **Cách tính toán:**
  - Ragas không đo trực tiếp câu trả lời. Thay vào đó, nó dùng LLM để **đọc câu trả lời và tự sinh ra (reverse-engineer) các câu hỏi tiềm năng**.
  - Ragas tính toán **Cosine Similarity** (Độ tương đồng Cosine) giữa câu hỏi gốc của người dùng và các câu hỏi vừa được sinh ngược ra.
  - Nếu câu trả lời đi đúng trọng tâm, câu hỏi sinh ngược sẽ rất giống câu hỏi gốc (Cosine Similarity tiến tới 1).

---

## ⚠️ LƯU Ý QUAN TRỌNG VỀ MINH CHỨNG (REFERENCES) TRONG DỰ ÁN
Hiện tại, sau khi kiểm tra toàn bộ mã nguồn trong thư mục `codebase/`, **TÔI KHÔNG TÌM THẤY BẤT CỨ MINH CHỨNG NÀO** cho những con số này.
- **Không có tập dữ liệu test:** Không tìm thấy file `.csv` hay `.json` nào chứa bộ "1200 câu hỏi" kèm Ground Truth.
- **Không có mã nguồn RAGAS:** Không có script Python nào (như `evaluate.py`) sử dụng thư viện `ragas` hay `langchain` để tính toán tự động các chỉ số này.

**Lời khuyên:** Nếu hội đồng chấm thi (hoặc giáo viên hướng dẫn) yêu cầu bạn chứng minh làm sao ra được con số 0.94 hay 0.98, bạn sẽ không có cơ sở để bảo vệ. Bạn cần:
1. Tạo một file `eval_dataset.csv` chứa các cột: `question`, `ground_truth`.
2. Viết một script nhỏ cài đặt thư viện `ragas` để chạy test 100-200 câu hỏi thực tế và sinh ra báo cáo (Report) tự động.
