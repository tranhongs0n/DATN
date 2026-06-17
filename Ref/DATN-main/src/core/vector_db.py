import os
import shutil
import logging
import google.genai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from src.config.settings import settings

logger = logging.getLogger(__name__)

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name=None):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME

    def embed_documents(self, texts):
        embeddings = []
        # Process in batches of 100
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            # Format each text as a separate Content object to ensure batch processing works correctly
            batch = [{"parts": [{"text": t if t.strip() else "[EMPTY]"}]} for t in texts[i:i + batch_size]]
            try:
                result = self.client.models.embed_content(
                    model=self.model_name,
                    contents=batch,
                    config={"task_type": "retrieval_document"}
                )
                # The response format for google.genai is result.embeddings
                embeddings.extend([e.values for e in result.embeddings])
            except Exception as e:
                logger.error(f"Error embedding batch {i//batch_size}: {e}")
                raise e
        return embeddings

    def embed_query(self, text):
        try:
            # Gradio or LangChain might pass a dictionary instead of a string in some versions
            if isinstance(text, dict) and "text" in text:
                text = text["text"]
            elif isinstance(text, list):
                text = text[0] if text else ""
                
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=text,
                config={"task_type": "retrieval_query"}
            )
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            raise e

class VectorDBManager:
    def __init__(self, chroma_path=None):
        self.chroma_path = chroma_path or str(settings.CHROMA_PATH)
        self.embeddings = GeminiEmbeddings()

    def build_from_documents(self, docs, append=False):
        if not docs:
            return None
            
        logger.info(f"Splitting {len(docs)} documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        # Filter out empty chunks to prevent embedding errors
        chunks = [c for c in chunks if c.page_content.strip()]
        logger.info(f"Split into {len(chunks)} valid chunks.")

        if not append and os.path.exists(self.chroma_path):
            logger.info(f"Removing existing vector DB at {self.chroma_path}")
            shutil.rmtree(self.chroma_path)

        if append and os.path.exists(self.chroma_path):
            # To avoid duplicates, we should remove existing chunks for the files we are about to index
            db = self.get_db()
            source_files = list(set(d.metadata.get('source') for d in docs if d.metadata.get('source')))
            if source_files:
                logger.info(f"Removing existing chunks for {len(source_files)} files to prevent duplicates...")
                for source in source_files:
                    db.delete(where={"source": source})
            
            logger.info("Adding chunks to existing database...")
            db.add_documents(chunks)
        else:
            logger.info("Creating new Chroma vector DB...")
            db = Chroma.from_documents(
                chunks,
                self.embeddings,
                persist_directory=self.chroma_path
            )
        
        logger.info("Vector DB update successful.")
        return db

    def get_db(self):
        if not os.path.exists(self.chroma_path):
            return None
        return Chroma(persist_directory=self.chroma_path, embedding_function=self.embeddings)

    def get_indexed_files(self):
        db = self.get_db()
        if not db:
            return set()
        
        collection = db.get()
        metadatas = collection.get('metadatas', [])
        # Extract 'source' and get unique basenames
        indexed_files = set(os.path.basename(m.get('source', '')) for m in metadatas if m.get('source'))
        return indexed_files

    def get_stats(self):
        db = self.get_db()
        if db is None:
            return {"doc_count": 0, "chunk_count": 0}
        
        # Get count of unique source files in metadata
        collection = db.get()
        metadatas = collection.get('metadatas', [])
        unique_files = set(m.get('source') for m in metadatas if m.get('source'))
        
        return {
            "doc_count": len(unique_files),
            "chunk_count": len(metadatas)
        }
