import os
import shutil
import logging
import google.genai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_community.retrievers import BM25Retriever
import pickle
from src.config.settings import settings

logger = logging.getLogger(__name__)

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name=None):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME

    def embed_documents(self, texts):
        embeddings = []
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = [{"parts": [{"text": t if t.strip() else "[EMPTY]"}]} for t in texts[i:i + batch_size]]
            try:
                result = self.client.models.embed_content(
                    model=self.model_name,
                    contents=batch,
                    config={"task_type": "retrieval_document"}
                )
                embeddings.extend([e.values for e in result.embeddings])
            except Exception as e:
                logger.error(f"Error embedding batch {i//batch_size}: {e}")
                raise e
        return embeddings

    def embed_query(self, text):
        try:
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
        self._db = None
        self._bm25 = None
        self._bm25_loaded = False

    def _invalidate_cache(self):
        self._db = None
        self._bm25 = None
        self._bm25_loaded = False

    def build_from_documents(self, docs, append=False):
        if not docs:
            return None
            
        logger.info(f"Splitting {len(docs)} documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        chunks = [c for c in chunks if c.page_content.strip()]
        logger.info(f"Split into {len(chunks)} valid chunks.")

        if not append and os.path.exists(self.chroma_path):
            logger.info(f"Removing existing vector DB at {self.chroma_path}")
            backup_path = f"{self.chroma_path}_backup"
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path, ignore_errors=True)
            try:
                shutil.copytree(self.chroma_path, backup_path)
            except Exception:
                pass
            
            db = self.get_db()
            if db:
                try:
                    db.delete_collection()
                except Exception as e:
                    logger.warning(f"Could not delete collection: {e}")
            
            try:
                shutil.rmtree(self.chroma_path, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Could not rmtree {self.chroma_path}: {e}")

        try:
            if append and os.path.exists(self.chroma_path):
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
            
            logger.info("Building BM25 Retriever for Hybrid Search...")
            all_docs_for_bm25 = chunks
            if append:
                try:
                    all_data = db.get()
                    from langchain_core.documents import Document
                    all_docs_for_bm25 = [Document(page_content=c, metadata=m) for c, m in zip(all_data['documents'], all_data['metadatas'])]
                except Exception as e:
                    logger.warning(f"Could not load all docs for BM25 append, using only new chunks: {e}")
                    
            bm25_retriever = BM25Retriever.from_documents(all_docs_for_bm25)
            os.makedirs(self.chroma_path, exist_ok=True)
            bm25_path = os.path.join(self.chroma_path, "bm25.pkl")
            with open(bm25_path, 'wb') as f:
                pickle.dump(bm25_retriever, f)
            logger.info("BM25 Retriever saved.")
            
        except Exception as e:
            if not append and 'backup_path' in locals() and os.path.exists(backup_path):
                logger.error(f"Vector DB build failed: {e}. Restoring backup...")
                if os.path.exists(self.chroma_path):
                    shutil.rmtree(self.chroma_path)
                shutil.move(backup_path, self.chroma_path)
            raise e
        
        if not append and 'backup_path' in locals() and os.path.exists(backup_path):
            shutil.rmtree(backup_path)

        self._invalidate_cache()
        logger.info("Vector DB update successful.")
        return db

    def get_db(self):
        if self._db is not None:
            return self._db
        if not os.path.exists(self.chroma_path):
            return None
        self._db = Chroma(persist_directory=self.chroma_path, embedding_function=self.embeddings)
        return self._db

    def get_bm25_retriever(self):
        if self._bm25_loaded:
            return self._bm25

        bm25_path = os.path.join(self.chroma_path, "bm25.pkl")
        old_path = f"{self.chroma_path}_bm25.pkl"
        if not os.path.exists(bm25_path) and os.path.exists(old_path):
            bm25_path = old_path

        if os.path.exists(bm25_path):
            try:
                with open(bm25_path, 'rb') as f:
                    self._bm25 = pickle.load(f)
            except Exception as e:
                logger.error(f"Failed to load BM25 retriever: {e}")
                self._bm25 = None
        self._bm25_loaded = True
        return self._bm25

    def get_indexed_files(self):
        db = self.get_db()
        if not db:
            return set()
        
        collection = db.get(include=["metadatas"])
        metadatas = collection.get('metadatas', [])
        indexed_files = set(os.path.basename(m.get('source', '')) for m in metadatas if m.get('source'))
        return indexed_files

    def get_stats(self):
        db = self.get_db()
        if db is None:
            return {"doc_count": 0, "chunk_count": 0}
        
        collection = db.get(include=["metadatas"])
        metadatas = collection.get('metadatas', [])
        unique_files = set(m.get('source') for m in metadatas if m.get('source'))
        
        return {
            "doc_count": len(unique_files),
            "chunk_count": len(metadatas)
        }
