from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path

# Получаем абсолютный путь к .env файлу
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / '.env'

print(f"Looking for .env file at: {env_path}")
load_dotenv(env_path)

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"Loaded TELEGRAM_BOT_TOKEN: {self.TELEGRAM_BOT_TOKEN}")

settings = Settings() 