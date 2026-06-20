# Đánh Giá 1_Chuong1.md

## 1. Dấu Hiệu AI & Ngôn Ngữ (AI Pattern Recognition & Linguistic Authenticity)
**Đánh giá: AI sinh 100% (High probability of AI generation).**

Lỗi diễn đạt máy móc, sáo rỗng (AI Hallmarks & Fluff).
> "Hành trình phát triển của trợ lý ảo bắt đầu từ những năm 1960..."
> "Trải qua nhiều thập kỷ, trợ lý ảo đã tiến hóa mạnh mẽ."
> "Cuộc cách mạng thực sự chỉ diễn ra khi..."
Lý do: Giọng văn Wikipedia/LLM đặc trưng. Dài dòng, không đúng trọng tâm khoa học.
Hành động: Cắt bỏ bối cảnh lịch sử thừa.

Lỗi chuyển ý dập khuôn (Predictable transitions).
> "Dù sở hữu năng lực ngôn ngữ mạnh mẽ, LLM vẫn bộc lộ ba hạn chế cốt lõi..."
> "Để thấy rõ ưu việt của RAG, cần đặt kỹ thuật này lên bàn cân so sánh..."
Lý do: AI tạo "cầu nối" văn bản giả tạo.

Lỗi vi phạm quy tắc viết (Rule violations).
> "Tinh chỉnh mô hình (Fine-tuning)"
> "Đám mây toàn phần (SaaS)"
> "RAG Nguyên thủy (Naive RAG)"
> "RAG Nâng cao (Advanced RAG)"
> "RAG Mô-đun (Modular RAG)"
Lý do: Vi phạm rõ ràng quy tắc "Cấm viết song ngữ" trong RULE. AI dịch word-by-word.
Hành động: Xóa ngoặc tiếng Anh. Định nghĩa trong `00_DanhMucTuVietTat.md`.

## 2. Tính Liêm Chính Học Thuật (Academic Integrity)
Lỗi chắp vá kiến thức, thiếu trích dẫn (Uncited generalizations).
> "...Đại học Bang Georgia (GSU) đã triển khai hệ thống Pounce..."
> "...Đại học Deakin ra mắt Genie..."
> "...Đại học FPT hay Đại học Kinh tế TP.HCM (UEH)..."
Lý do: Nêu tên hệ thống nhưng không có citation (tài liệu tham khảo [1], [2]...). Đây là kiến thức chung chung do LLM tự bịa hoặc tóm tắt từ data training. 
Hành động: Bổ sung citation chuẩn IEEE hoặc APA.

## 3. Độ Sâu Kỹ Thuật (Methodological Rigor)
Lỗi kiến thức kỹ thuật lạc hậu/sai lệch (Superficial/Outdated claims).
> "...việc nhồi nhét toàn bộ 86 tệp quy chế tuyển sinh hàng trăm trang vào từng lượt hỏi đáp là bất khả thi về mặt kỹ thuật..."
Lý do: Sai. LLM hiện tại (như Gemini 1.5 Pro) có context window 2M token, dư sức nhồi 86 file. Lý luận lỗi thời. Phải so sánh về latency, cost, hoặc focus, không phải "bất khả thi".

Lỗi ngụy biện kỹ thuật (Pseudoscientific claims).
> "Được huấn luyện đồng bộ với tư duy của LLM Gemini, mô hình [Embedding] này giúp giảm thiểu độ lệch ngữ nghĩa..."
Lý do: "Huấn luyện đồng bộ với tư duy" là thuật ngữ bịa đặt (marketing fluff). Không có cơ sở học thuật.
Hành động: Viết lại chuẩn kỹ thuật (cùng embedding space, semantic alignment).

## 4. Hình Thức (Formatting)
Phần giới thiệu lịch sử (ELIZA, 1960s) padding quá đà.
Hành động: Xóa padding. Tập trung trực tiếp vào RAG và LLM trong NLP hiện đại.

Kết luận: Rác. Sinh viên dùng AI prompt tạo nguyên chương 1. Cần viết lại 100% dựa trên paper thực.
