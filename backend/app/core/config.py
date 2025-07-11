from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    APP_NAME: str = "Blueprint AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="ALLOWED_HOSTS"
    )
    
    # Database
    NEO4J_URI: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(..., env="NEO4J_PASSWORD")
    
    # Vector Database
    CHROMA_HOST: str = Field(default="localhost", env="CHROMA_HOST")
    CHROMA_PORT: int = Field(default=8000, env="CHROMA_PORT")
    
    # AI Services
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=100 * 1024 * 1024, env="MAX_FILE_SIZE")  # 100MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=[".pdf", ".docx", ".txt", ".csv", ".xlsx", ".pptx"],
        env="ALLOWED_EXTENSIONS"
    )
    
    # Redis (for caching and Celery)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # External APIs
    SALESFORCE_CLIENT_ID: Optional[str] = Field(default=None, env="SALESFORCE_CLIENT_ID")
    SALESFORCE_CLIENT_SECRET: Optional[str] = Field(default=None, env="SALESFORCE_CLIENT_SECRET")
    SALESFORCE_USERNAME: Optional[str] = Field(default=None, env="SALESFORCE_USERNAME")
    SALESFORCE_PASSWORD: Optional[str] = Field(default=None, env="SALESFORCE_PASSWORD")
    
    # Slack Integration
    SLACK_BOT_TOKEN: Optional[str] = Field(default=None, env="SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET: Optional[str] = Field(default=None, env="SLACK_SIGNING_SECRET")
    
    # Google Drive Integration
    GOOGLE_DRIVE_CREDENTIALS_FILE: Optional[str] = Field(default=None, env="GOOGLE_DRIVE_CREDENTIALS_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 