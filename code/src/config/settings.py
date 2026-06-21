import os
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)

class UIConfig(BaseModel):
    theme: str
    primary_color: str
    background_color: str
    text_color: str

class ProjectConfig(BaseModel):
    name: str
    data_dir: str
    chroma_path: str
    ui: UIConfig

class ModelConfig(BaseModel):
    llm: str
    embedding: str

class CategoryConfig(BaseModel):
    name: str
    cat_id: int
    module_id: int

class ScraperConfig(BaseModel):
    base_url: str
    list_api: str
    detail_api: str
    extensions: List[str]
    categories: List[CategoryConfig]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), env_file_encoding='utf-8', extra='ignore')
    
    GOOGLE_API_KEY: str = ""
    ZALO_ACCESS_TOKEN: str = ""
    ZALO_APP_SECRET: str = ""
    ADMIN_PASSWORD: str = ""
    ALLOWED_ORIGINS: str = ""
    
    PROJECT: ProjectConfig = Field(default=None)
    MODELS: ModelConfig = Field(default=None)
    SCRAPER: ScraperConfig = Field(default=None)
    PROMPTS: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        yaml_data = self._read_yaml_configs()
        
        if "PROJECT" not in kwargs and "project" in yaml_data:
            kwargs["PROJECT"] = yaml_data["project"]
        if "MODELS" not in kwargs and "models" in yaml_data:
            kwargs["MODELS"] = yaml_data["models"]
        if "SCRAPER" not in kwargs and "scraper" in yaml_data:
            kwargs["SCRAPER"] = yaml_data["scraper"]
        if "PROMPTS" not in kwargs and "prompts" in yaml_data:
            kwargs["PROMPTS"] = yaml_data["prompts"]
            
        super().__init__(**kwargs)

    def _read_yaml_configs(self) -> Dict[str, Any]:
        data = {}
        config_path = BASE_DIR / "config.yaml"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data.update(yaml.safe_load(f))
            except Exception as e:
                logger.error(f"Failed to load config.yaml: {e}")
        
        prompts_path = BASE_DIR / "prompts.yaml"
        if prompts_path.exists():
            try:
                with open(prompts_path, "r", encoding="utf-8") as f:
                    data["prompts"] = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Failed to load prompts.yaml: {e}")
        return data

    @property
    def PROJECT_NAME(self) -> str:
        return self.PROJECT.name

    @property
    def CATEGORIES(self) -> List[Dict[str, Any]]:
        return [cat.model_dump() for cat in self.SCRAPER.categories]

    @property
    def DATA_DIR(self) -> Path:
        return BASE_DIR / self.PROJECT.data_dir

    @property
    def CHROMA_PATH(self) -> Path:
        return BASE_DIR / self.PROJECT.chroma_path

    @property
    def GEMINI_MODEL_NAME(self) -> str:
        return self.MODELS.llm

    @property
    def EMBEDDING_MODEL_NAME(self) -> str:
        return self.MODELS.embedding

    @property
    def BASE_URL(self) -> str:
        return self.SCRAPER.base_url

    @property
    def LIST_API(self) -> str:
        return self.SCRAPER.list_api

    @property
    def DETAIL_API(self) -> str:
        return self.SCRAPER.detail_api

    @property
    def EXTENSIONS(self) -> tuple:
        return tuple(self.SCRAPER.extensions)

settings = Settings()
