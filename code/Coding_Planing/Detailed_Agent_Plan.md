# Detailed AI Agent Implementation Plan: TLU Multimodal RAG

This document provides a highly detailed, step-by-step implementation plan for an AI Coding Agent to build the TLU Admission RAG system. The AI agent should execute these steps sequentially, verifying the success of each step before moving on.

## Phase 1: Project Initialization & Configuration

**Objective**: Set up the project structure, dependencies, and configuration management.

1. **Initialize Dependencies (`pyproject.toml`)**
   - Create or update `pyproject.toml` with the following dependencies:
     - `fastapi`, `uvicorn[standard]`
     - `langchain`, `langchain-google-genai`
     - `chromadb`
     - `beautifulsoup4`, `requests`
     - `pydantic`, `pydantic-settings`
     - `python-dotenv`
     - `pypdf`, `python-docx`, `docx2txt`
     - `pytest` (for dev)
   - *Action:* Write `pyproject.toml` and run `pip install -e .`

2. **Configuration Management (`src/config/settings.py`)**
   - Create a Pydantic `BaseSettings` class.
   - Define fields: `GOOGLE_API_KEY`, `ZALO_APP_ID`, `ZALO_APP_SECRET`, `CHROMA_DB_DIR` (default: `./data/chroma`), `DATA_DIR` (default: `./data/raw`).
   - Create a `.env.example` file.

3. **Logging System (`src/utils/logger.py`)**
   - Configure the standard Python `logging` library.
   - Set up console and file handlers (e.g., `logs/app.log`) with formatting to track module execution and errors.

## Phase 2: Data Ingestion & Processing

**Objective**: Build utilities to scrape, load, and chunk data.

1. **Web Scraper (`src/utils/scraper.py`)**
   - Create class `TLUAdmissionScraper`.
   - Implement methods to fetch HTML from `ts.tlu.edu.vn`.
   - Use `BeautifulSoup4` to extract article titles, content, and dates.
   - Save scraped content as markdown or raw text into `DATA_DIR/scraped/`.

2. **Document Loaders (`src/utils/loaders.py`)**
   - Implement functions to recursively scan `DATA_DIR` for `.pdf` and `.docx` files.
   - Wrap `PyPDFLoader` and `Docx2txtLoader` from LangChain to extract text.
   - Include metadata (filename, source type, extraction date).

3. **Multimodal Converter (`src/utils/multimodal_converter.py`)**
   - Create a function to use `gemini-2.0-flash` (or `gemini-1.5-flash`) via `google-genai` API to convert complex PDF/images (e.g., tables of admission scores) into structured Markdown.
   - This handles the "Dữ liệu ẩn trong hình ảnh" and "Bảng biểu phức tạp" requirements.

4. **Text Processing & Chunking (`src/utils/text_processor.py`)**
   - Use LangChain's `RecursiveCharacterTextSplitter`.
   - Configure chunk size (e.g., 1000 characters) and overlap (e.g., 200 characters).
   - Ensure metadata is attached to every chunk (source, page number, year).

## Phase 3: Vector Database & RAG Core

**Objective**: Implement embedding generation, vector storage, and the retrieval engine.

1. **Embedding Wrapper (`src/core/embeddings.py`)**
   - Initialize `GoogleGenerativeAIEmbeddings` using model `models/embedding-001` or `text-embedding-004`.
   - Define retry logic for API rate limits.

2. **Vector Store Manager (`src/core/vector_store.py`)**
   - Create `VectorDBManager` class wrapping `Chroma`.
   - Implement methods: `add_documents()`, `similarity_search_with_score()`, `delete_collection()`.
   - Ensure the DB persists to `CHROMA_DB_DIR`.

3. **Indexing Service (`src/core/indexing_service.py`)**
   - Combine Phase 2 (loaders/chunker) and VectorDB.
   - Create an `index_all_data()` pipeline: Load -> Chunk -> Embed -> Save to Chroma.
   - Add batching (e.g., process 100 chunks at a time) to prevent API quota issues.

4. **Retriever & Prompt Templates (`src/core/retriever.py` & `src/core/prompts.py`)**
   - Define the `SystemInstruction` for the Gemini LLM. It must restrict the LLM to *only* use provided context and answer in Vietnamese.
   - Implement `RAGRetriever`: Take a user query, perform a similarity search on ChromaDB, and format the retrieved chunks into a context string.

5. **Multimodal Engine (`src/core/rag_engine.py`)**
   - Combine the retriever and `ChatGoogleGenerativeAI` (Gemini Flash).
   - Implement `generate_response()` and `stream_response()` methods.
   - Pass the context + user query to the LLM and return the generated answer.

## Phase 4: API Backend (FastAPI) & Integrations

**Objective**: Expose the core logic via RESTful APIs.

1. **FastAPI Setup (`src/app/main.py`)**
   - Initialize FastAPI app.
   - Add CORS middleware.
   - Mount static files for the Web Admin.

2. **Chat & Admin Endpoints (`src/app/api/endpoints.py`)**
   - `POST /api/chat`: Accepts a JSON `{ "query": "..." }`, returns RAG response (use Server-Sent Events for streaming if possible).
   - `POST /api/admin/index`: Triggers `IndexingService.index_all_data()`.
   - `POST /api/admin/scrape`: Triggers `TLUAdmissionScraper`.
   - `POST /api/admin/upload`: Endpoint to upload new PDF/DOCX files to `DATA_DIR`.

3. **Zalo Webhook (`src/app/api/zalo_handler.py`)**
   - Implement `POST /webhook/zalo`.
   - Verify Zalo signature.
   - Extract user message, send to `rag_engine`, and use Zalo Open API to send the response back to the user.

## Phase 5: Web Admin Dashboard (Presentation Layer)

**Objective**: Build a simple GUI for administrators.

1. **Admin UI (`src/app/static/index.html` & `app.js`)**
   - Create a clean HTML/TailwindCSS (or plain CSS) interface.
   - Sections:
     - **Chat Testing**: A chat box to test the bot locally.
     - **Data Management**: File upload form and a "Trigger Web Scraper" button.
     - **Vector DB Status**: Button to "Rebuild Index" and show status (Loading...).
   - Wire up `app.js` to call the FastAPI endpoints defined in Phase 4.

## Phase 6: Testing & Refinement

**Objective**: Ensure the system works correctly and handles errors gracefully.

1. **Unit Tests (`tests/`)**
   - Write tests for text chunking (`test_text_processor.py`).
   - Write tests for ChromaDB insertion/retrieval (`test_vector_store.py`).
   - Write tests for API endpoints using FastAPI `TestClient` (`test_api.py`).

2. **Integration & Refinement**
   - Run the full pipeline: Scrape -> Index -> Chat.
   - Tune `chunk_size`, `chunk_overlap`, and retrieval `k` (e.g., top 5 documents) based on response quality.
   - Ensure "I don't know" logic triggers correctly when the RAG context is empty.

---

**Execution Instructions for AI Agent:**
When executing this plan, start at Phase 1, Step 1. Do not move to the next step until the current step's code is written, runs without syntax errors, and is logically sound. Use `run_command` to verify syntax (e.g., `python -m py_compile <file>`) where applicable.
