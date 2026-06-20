# PRD: RAG-based Admission Virtual Assistant for Thuy Loi University (TLU)

## Overview
An intelligent virtual assistant designed to consult applicants and parents about Thuy Loi University (TLU) admissions. The system utilizes Advanced RAG (Retrieval-Augmented Generation) with Google Gemini, storing data in a local ChromaDB, managed via a Web Admin Dashboard, and interacting with users via a Zalo Bot.

## Task 1: Project Initialization & Environment Configuration
Set up baseline dependencies, environment variables, configuration files, and logging mechanisms.
- Validate project structure (`src/`, `tests/`, `configs/`).
- Configure Python environment with `pyproject.toml` and lock files.
- Set up system configurations in `config.yaml` and credentials in `.env` (Gemini API keys, Zalo token, Database paths).
- Standardize the logging utility to track scraping, ingestion, database operations, and user interactions.

## Task 2: Data Ingestion Module (Scrapers, Loaders & Multimodal Converter)
Build utilities to collect, extract, clean, and split source information from various formats.
- Complete `TLUAdmissionScraper` to crawl and fetch news content and admission portals from TLU website (`https://ts.tlu.edu.vn`).
- Build standard Document Loaders for PDF and DOCX documents in the `data/` folder.
- Implement the `Multimodal File Converter` using Gemini Vision API to parse images/scanned documents into Markdown while retaining table structures.
- Implement text pre-processing and dynamic chunking using `RecursiveCharacterTextSplitter`.

## Task 3: VectorDB Manager & Core RAG Pipeline
Implement vector embeddings, semantic storage, context retrieval, and generation.
- Integrate Google Gemini Embeddings (`models/text-embedding-004`) via LangChain.
- Complete `VectorDBManager` to interface with a local ChromaDB instance (CRUD operations: insert, delete, query, rebuild index).
- Implement `Indexing Service` supporting incremental updates (append mode) and batching to avoid API rate limits.
- Design prompts in `prompts.yaml` targeting strict factual compliance (no hallucinations, Vietnamese language structure, markdown formatting with bold metrics).
- Implement text streaming generation in the RAG pipeline.

## Task 4: FastAPI Backend & Zalo Webhook Integration
Expose server endpoints and establish connection with Zalo OA.
- Set up FastAPI server with CORS and error handling middlewares.
- Expose Admin REST APIs for dashboard interactions (upload files, trigger scraping, delete documents, trigger DB rebuild).
- Implement `/api/chat` SSE (Server-Sent Events) streaming endpoint.
- Implement Zalo API integrations (webhook verification, message parsing, forwarding to RAG engine, formatting responsive payloads like Quick Replies).

## Task 5: Web Admin Dashboard UI
Create a clean administration dashboard.
- Create single-page admin interface embedded in the FastAPI project.
- Implement drag-and-drop file upload component.
- Display real-time indexing status and system logs.
- Provide simple statistics panel (number of documents indexed, vector store size, recent scraper logs).

## Task 6: Testing, Evaluation & System Refinement
Verify accuracy, handle operational edge cases, and finalize documentation.
- Implement test query sets grouped by 5 categories (basic info, slang/no-diacritics, complex multi-conditional queries, out-of-scope queries, multi-level degrees).
- Implement query metadata filtering (filtering by school year/academic year) to address historical data conflicts.
- Implement rate-limiting retries (backoff strategy) for Gemini API queries.
- Clean up unused files and prepare the system `README.md`.
