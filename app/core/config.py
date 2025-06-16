from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/tododb"
    QDRANT_URL: str = "http://host.docker.internal:6333"
    OLLAMA_URL: str = "http://host.docker.internal:11434"

    class Config:
        env_file = ".env"

settings = Settings()
