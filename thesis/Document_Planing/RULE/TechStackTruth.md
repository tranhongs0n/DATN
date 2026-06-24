# SOURCE OF TRUTH: TECH STACK & ALGORITHMS

This file documents the exact technologies and algorithms implemented in the codebase (`D:\DATN\codebase`). Do not write thesis content that contradicts this file.

## 1. Models & AI APIs
- **LLM (Generation):** `gemini-3.1-flash-lite` (via Google Gemini API, `google-genai` SDK)
- **Embedding Model:** `models/gemini-embedding-2`
- **Multimodal (Vision):** Gemini API is used to convert unsupported files (e.g., images) into Markdown/DOCX format.

## 2. Core Architecture
- **Framework:** FastAPI (`uvicorn` server)
- **RAG Orchestration:** LangChain (`langchain`, `langchain-community`)
- **Vector Database:** ChromaDB (`langchain-chroma`)
- **Hybrid Search:** Combines Semantic Search (ChromaDB cosine distance) and Keyword Search (`rank_bm25`).

## 3. Document Processing (Ingestion)
- **PDF Loader:** `docling` (DocumentConverter) - Converts PDF to Markdown.
- **DOCX Loader:** `Docx2txtLoader` from `langchain_community.document_loaders`.
- **Text Loader:** Standard UTF-8 file reading for `.txt`.
- **Chunking Algorithm:** `RecursiveCharacterTextSplitter` from `langchain-text-splitters`.
  - Chunk Size: `1000`
  - Chunk Overlap: `200`

## 4. Other Features
- **Semantic Cache:** Custom caching mechanism built to reduce API calls for repeated identical semantic queries.
- **Zalo Integration:** Polling mechanism (`zalo_polling.py`) connecting to Zalo Bot.
- **Admin UI / Chat UI:** Served via FastAPI `static/` HTML/JS/CSS (No modern JS frontend framework).
- **Authentication:** `bcrypt` for password hashing in Admin UI.
