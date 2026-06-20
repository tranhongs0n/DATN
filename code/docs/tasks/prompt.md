# Instructions for Ralph Loop Agent

Please follow these guidelines during execution:

1. **Strict Context Alignment**: All RAG answers must be derived strictly from retrieved ChromaDB context. Return "Hệ thống hiện chưa có thông tin về vấn đề này." if context lacks the answer.
2. **Vietnamese Localization**: Ensure all user-facing messaging (chatbot response, administrative messages) is in Vietnamese.
3. **Robust Data Parsing**: Make sure table structure is preserved when converting PDF/DOCX or parsing scraped HTML to ensure correct answer generation for multi-criteria inputs.
4. **Environment Consistency**: Read credentials from `.env` and system settings from `config.yaml` using the configured settings class (`src/config/settings.py`).
