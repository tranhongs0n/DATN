import time
import logging
from google import genai
from src.config.settings import settings

logger = logging.getLogger(__name__)

class MultimodalEngine:
    def __init__(self, model_name=None):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY missing in .env")
            
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = model_name or settings.GEMINI_MODEL_NAME
        self.system_instruction = settings.PROMPTS.get("chatbot", {}).get("system_instruction", "")
        self.uploaded_files = {}

    def upload_file(self, file_path):
        if file_path in self.uploaded_files:
            return self.uploaded_files[file_path]

        logger.info(f"Uploading {file_path} to Gemini...")
        file_obj = self.client.files.upload(file=file_path)
        
        while file_obj.state == "PROCESSING":
            time.sleep(2)
            file_obj = self.client.files.get(name=file_obj.name)
        
        if file_obj.state == "FAILED":
            logger.error(f"File {file_path} processing failed")
            raise RuntimeError(f"File {file_path} processing failed")
            
        self.uploaded_files[file_path] = file_obj
        return file_obj

    def query_stream(self, file_paths, prompt):
        contents = []
        for path in file_paths:
            contents.append(self.upload_file(path))
        contents.append(prompt)
        
        # Retry logic for quota
        for attempt in range(3):
            try:
                response = self.client.models.generate_content_stream(
                    model=self.model_name,
                    contents=contents,
                    config={"system_instruction": self.system_instruction, "temperature": 0.0}
                )
                for chunk in response:
                    yield chunk.text
                return
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    logger.warning(f"Quota hit, waiting 30s (attempt {attempt+1})...")
                    time.sleep(30)
                else:
                    logger.exception("Error during Gemini query")
                    raise e

    def query(self, file_paths, prompt):
        # Fallback non-streaming query
        contents = []
        for path in file_paths:
            contents.append(self.upload_file(path))
        contents.append(prompt)
        
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config={"system_instruction": self.system_instruction, "temperature": 0.0}
                )
                return response.text
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    logger.warning(f"Quota hit, waiting 30s (attempt {attempt+1})...")
                    time.sleep(30)
                else:
                    logger.exception("Error during Gemini query")
                    raise e

    def cleanup(self):
        for file_obj in self.uploaded_files.values():
            try:
                self.client.files.delete(name=file_obj.name)
            except Exception as e:
                logger.debug(f"Failed to delete remote file {file_obj.name}: {e}")
        self.uploaded_files = {}
