import os
import logging
from google import genai
from google.genai import types
from src.config.settings import settings

logger = logging.getLogger(__name__)

class MultimodalConverter:
    def __init__(self):
        # We need the google-genai library as mentioned in pyproject.toml
        # If API key is missing, it will fail gracefully or the library handles it.
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY) if settings.GOOGLE_API_KEY else None
        self.model_name = "gemini-2.5-flash" # Standard multimodal model
        
    def upload_and_convert(self, file_path: str) -> str:
        """
        Uploads an image or PDF to Gemini Vision API and returns extracted Markdown text.
        Particularly useful for scanning tables of admission scores.
        """
        if not self.client:
            logger.error("Google API key is missing. Cannot use Multimodal Converter.")
            return ""
            
        logger.info(f"Uploading and converting file: {file_path}")
        try:
            # Upload file
            gemini_file = self.client.files.upload(file=file_path)
            
            prompt = (
                "Extract all the text and data from this document. "
                "If there are any tables, ensure they are formatted perfectly as Markdown tables. "
                "Do not add any conversational filler, just the exact content of the document."
            )
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[gemini_file, prompt]
            )
            
            # Delete file to clean up space on Google servers
            self.client.files.delete(name=gemini_file.name)
            
            if response.text:
                return response.text
            return ""
            
        except Exception as e:
            logger.error(f"Failed to convert file {file_path}: {e}")
            return ""
