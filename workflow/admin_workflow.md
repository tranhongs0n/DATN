# Admin User Workflow & Feature List

This document outlines the complete step-by-step workflow and capabilities of an Administrator within the TLU Admission RAG Assistant system. This document can be used to evaluate the completeness of the administrative CRM and CMS system.

## Phase 1: Access & Security (Quản lý Truy cập)
1. **Admin Login**: Admin navigates to the dashboard and authenticates using secure credentials (passwords hashed with `bcrypt`).
2. **Session Management**: Token-based session with TTL expiration handles subsequent API requests.
3. **User Management (CRUD)**:
   - View list of all active administrators and their roles.
   - Create new admin accounts (Requires 'superadmin' level access).
   - Delete/Revoke admin accounts (Requires 'superadmin' level access).
   - **Audit Logging**: All critical actions (creation, deletion, rebuilds) are securely logged for accountability.

## Phase 2: Data Acquisition (Thu thập dữ liệu)
1. **Manual File Upload**: Admin selects and uploads local `.pdf`, `.docx`, `.png`, or `.jpg` documents containing admission policies, scores, or quotas.
2. **Automated Web Scraping (TLU Portal)**: 
   - Admin configures the "Limit" parameter (e.g., Top 5, 10, or 50).
   - Clicks "Scrape Latest Files" to trigger the backend to pull the latest articles directly from the TLU API.
   - System automatically deduplicates and skips files that have already been downloaded to save bandwidth.
3. **Error Handling (Data Acquisition)**:
   - If an upload fails (e.g., file too large, unsupported format), the system rejects it and alerts the admin.
   - If scraping returns 0 new articles, the admin is notified that the database is already up to date.

## Phase 3: Data Processing & Indexing (Xử lý & Nhúng dữ liệu)
1. **File Status Tracking**: Admin views a real-time table of all local files, displaying statuses such as `Indexed`, `Pending`, or `Missing Local`.
2. **AI Multimodal Conversion**:
   - Admin identifies unsupported files (e.g., images of tables, scanned PDFs).
   - Admin clicks "Convert" (single file) or "Bulk Convert All".
   - System sends the file to Google Gen AI API (Gemini Multimodal), extracts text/tables, and saves it as a clean structured `.docx` file ready for text chunking.
3. **Rebuild Vector Database**: 
   - Admin triggers a full re-index.
   - The system creates a backup of the old ChromaDB, chunks all valid documents, generates embeddings, and replaces the old DB safely. If it fails, the backup is restored.
4. **Error Handling (Processing)**:
   - If the DB rebuild fails midway, the system rolls back to the previous DB state to avoid downtime.

## Phase 4: System Monitoring & Testing (Giám sát & Kiểm thử)
1. **Dashboard Analytics**: Admin monitors polled stats (refreshed periodically) including total loaded documents, vector chunks, and the active LLM version.
2. **Live Test Chat**: Admin uses an embedded chat interface inside the dashboard to query the RAG system and verify accuracy *before* real users ask the Zalo bot.

## Phase 5: CRM & Zalo Integration (Chăm sóc Thí sinh)
1. **Zalo Conversations List**: Admin views a periodically refreshed feed of all Zalo users who have interacted with the bot.
2. **Human Handover Alert (Smart Fallback)**: 
   - If an end-user types "gặp người thật", "tư vấn viên", or the bot detects high confusion, the user is flagged with a red `Human Needed` badge in the Admin's list.
3. **Full Chat History Inspection**: Admin clicks on a user to read the exact historical timeline of messages between the student and the AI (Contextual Memory).
4. **Manual Override & Reply**: 
   - Admin types a response directly into the dashboard chat box.
   - The backend pushes the message to the student's Zalo app via the Zalo Send API.
   - The message is logged in the timeline with a distinct Admin visual style (Shield icon, dark blue background) to differentiate it from AI responses.
   - The `Human Needed` badge is automatically cleared.
