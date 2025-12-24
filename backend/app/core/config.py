from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    DATABASE_URL: str
    JWT_SECRET: str
    TENANCY_MODE: str = "shared"  # or "schema"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()