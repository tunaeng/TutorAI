"""
Configuration module for AI Tutor Backend
Supports LOCAL and PROD environments with automatic database URL switching
"""

from enum import Enum
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PROD = "PROD"


class Settings(BaseSettings):
    """Application settings with environment-based configuration"""
    
    # Environment
    environment: Environment = Field(default=Environment.LOCAL, env="ENVIRONMENT")
    
    # Database URL
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/ai_tutor_local",
        env="DATABASE_URL"
    )
    
    # Application
    app_name: str = Field(default="AI Tutor Backend", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Security
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="ALLOWED_ORIGINS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == Environment.PROD
    
    @property
    def is_local(self) -> bool:
        """Check if running in local environment"""
        return self.environment == Environment.LOCAL
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
