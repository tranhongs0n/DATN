# Data Pipeline Workflow

This document details the end-to-end lifecycle of a document from acquisition to vector retrieval.

## 1. Data Acquisition
Data enters the system via two distinct channels:
- **Manual Upload**: Admins upload `.pdf`, `.docx`, `.png`, or `.jpg` files directly via the Admin UI. These are saved to `data/AdminUploads/`.
- **Automated Web Scraping**: The system periodically scrapes the TLU Admission website, parsing HTML and saving articles as structured documents.

## 2. Multimodal Processing
1. **Detection**: The system detects unsupported file types (e.g., images, scanned PDFs) in the data directory.
2. **AI Conversion**: 
   - The file is sent to the Google Gen AI API (Gemini Multimodal).
   - The AI acts as an OCR/Digitizer, extracting text and tabular data while preserving Markdown structure.
   - A clean `.docx` file is saved locally, and the original unsupported file is marked as processed.

## 3. Document Parsing & Chunking
1. **Loading**: The `DocumentLoader` scans the local directory and parses `.pdf` and `.docx` files using LangChain community loaders.
2. **Chunking**: The `RecursiveCharacterTextSplitter` divides the documents into chunks (e.g., 1000 characters) with overlapping segments (e.g., 200 characters) to preserve contextual boundaries.

## 4. Embedding Generation
1. **Batching**: Chunks are grouped into batches of 100 to optimize API throughput and prevent rate limits.
2. **Vectorization**: Batches are sent to the `models/text-embedding-004` API via the `GeminiEmbeddings` class.

## 5. Vector Storage (ChromaDB)
1. **Backup**: A backup of the current ChromaDB is created.
2. **Indexing**: New document chunks and their corresponding vectors are injected into ChromaDB.
3. **Rollback**: If the indexing fails, the backup is restored seamlessly.
