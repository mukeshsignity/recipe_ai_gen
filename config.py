from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_ORG_KEY: str
    GOOGLE_CLOUD_TTS_KEY: str | None = None
    MODEL_PATH: str = "models/best.pt"
    ROBOWFLOW_API_KEY: str | None = None
    FFMPEG_PATH: str = "/usr/bin/ffmpeg"  # Default for Linux-based servers
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # Still allows local `.env` usage

# Load settings
settings = Settings()
