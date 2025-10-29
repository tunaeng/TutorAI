import os
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/ai_tutor_local"
    )
    
    # App
    PROJECT_NAME: str = "AI Tutor"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Admin auth
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")

    # Secret key for sessions
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-.env")

    # Feature flags
    ADMIN_I18N_ENABLED: bool = os.getenv("ADMIN_I18N_ENABLED", "true").lower() == "true"

settings = Settings()