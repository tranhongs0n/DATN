# End User (Zalo User) Workflow & Feature List

This document outlines the complete step-by-step workflow and interaction capabilities of a prospective student or parent interacting with the TLU Admission RAG Assistant via Zalo.

## Phase 1: Initiation & Access (Tiếp cận & Khởi tạo)
1. **Discovery**: User opens the Zalo app and navigates to the "Đại học Thủy Lợi" Official Account (OA).
2. **Engagement**: User clicks "Quan tâm" (Follow) and opens the chat interface to begin asking questions.

## Phase 2: Automated Consultation (Tư vấn Tự động qua AI)
1. **Natural Language Querying**: User types questions using natural, everyday language (e.g., "Cho em hỏi ngành Công nghệ thông tin lấy bao nhiêu điểm?").
2. **Contextual Memory (Trí nhớ hội thoại)**: 
   - User asks follow-up questions without needing to repeat the subject (e.g., "Vậy học phí của ngành đó là bao nhiêu?").
   - The AI uses the SQLite history database to remember the context of the last few conversational turns.
3. **Ambiguity Clarification (Xử lý truy vấn thiếu ngữ cảnh)**:
   - If the user asks a vague question (e.g., "Học phí trường mình bao nhiêu?" without specifying a major), the AI halts the RAG hallucination process.
   - The AI politely asks the user to clarify the missing parameters (e.g., "Bạn vui lòng cho biết bạn quan tâm đến ngành nào và năm học nào?").
4. **Relative Time Understanding (Nhận thức thời gian)**:
   - User types "Điểm chuẩn năm ngoái".
   - The AI checks the system's current clock (e.g., 2026), deducts that "năm ngoái" means 2025, and fetches the correct historical data.
5. **Source Verification (Xác thực nguồn)**:
   - User receives the answer along with a direct citation at the bottom of the message (e.g., `Nguồn tham khảo: De_an_tuyen_sinh_2024.pdf`).
   - This ensures the user can trust the AI's response regarding critical admission figures.

## Phase 3: Escalation & Human Handover (Chuyển tiếp cho Tư vấn viên thật)
1. **Triggering Handover**: User encounters a highly specific personal issue or gets frustrated and types keywords like "gặp người thật", "tư vấn viên", or "admin".
2. **AI Pause & Acknowledgment**: 
   - The AI intercepts the keyword and immediately suspends the automated RAG retrieval.
   - The AI sends a comforting confirmation: *"Hệ thống đã ghi nhận yêu cầu của bạn và thông báo cho Thầy/Cô ban tuyển sinh. Vui lòng đợi trong giây lát!"*
3. **Seamless Human Consultation**: 
   - The user receives a push notification on Zalo containing a direct, manually written message from the University's Admission Staff.
   - The user continues to converse normally in the exact same chat window, unaware of the backend switch between AI and Human.

## Phase 4: Exception Handling & Edge Cases (Xử lý lỗi)
1. **Rate Limiting (Chống Spam)**: 
   - If a user sends too many messages in a short period, the system pauses their access and asks them to wait to prevent abuse.
2. **API Unreachable / System Down**: 
   - If the core LLM engine or Vector DB is unresponsive, the system gracefully falls back to an automated message asking the user to wait for a human consultant.
3. **Empty RAG Results (Không có nguồn tham khảo)**:
   - If the AI cannot find relevant documents to back its answer, it honestly states "Hệ thống chưa có thông tin chính thức về câu hỏi này" and offers handover to a human.
