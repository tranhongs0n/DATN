import os
import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from src.config.settings import settings

logger = logging.getLogger(__name__)

SUPPORTED_DOC_EXTENSIONS = ('.pdf', '.docx')
SUPPORTED_ASSET_EXTENSIONS = ('.png', '.jpg', '.jpeg')

class DocumentLoader:
    @staticmethod
    def get_available_files(include_assets=False) -> List[str]:
        """Returns a list of all relevant files in the data directory."""
        files = []
        data_dir = settings.DATA_DIR
        
        if not data_dir.exists():
            return []

        extensions = SUPPORTED_DOC_EXTENSIONS
        if include_assets:
            extensions += SUPPORTED_ASSET_EXTENSIONS

        for root, _, filenames in os.walk(data_dir):
            for f in filenames:
                if f.lower().endswith(extensions):
                    files.append(os.path.join(root, f))
        
        return sorted(files)

    @staticmethod
    def load_documents() -> List[Document]:
        """Load all available PDF and DOCX files into Langchain Document objects."""
        all_docs = []
        files = DocumentLoader.get_available_files()
        
        for file_path in files:
            logger.info(f"Loading document: {file_path}")
            try:
                if file_path.lower().endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                elif file_path.lower().endswith('.docx'):
                    loader = Docx2txtLoader(file_path)
                    docs = loader.load()
                else:
                    continue
                    
                # Add source metadata explicitly just in case
                for doc in docs:
                    doc.metadata["source"] = file_path
                all_docs.extend(docs)
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                
        logger.info(f"Successfully loaded {len(all_docs)} document pages/sections.")
        return all_docs
