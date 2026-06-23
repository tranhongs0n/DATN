import os
import logging
from typing import List
from src.config.settings import settings

logger = logging.getLogger(__name__)

SUPPORTED_DOC_EXTENSIONS = ('.pdf', '.docx', '.txt')
SUPPORTED_ASSET_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

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
