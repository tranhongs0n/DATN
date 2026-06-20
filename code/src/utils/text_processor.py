import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split a list of Langchain documents into smaller chunks."""
        logger.info(f"Processing and chunking {len(documents)} documents...")
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents.")
            return chunks
        except Exception as e:
            logger.error(f"Error during document chunking: {e}")
            return []
