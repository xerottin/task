from pydantic import BaseModel, validator
from dotenv import load_dotenv
import os
import time

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str | None = None
    SECRET_KEY: str
    TELEGRAM_BOT_TOKEN: str

    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        # Ждем установки DATABASE_URL максимум 30 секунд
        timeout = 30
        while not v and timeout > 0:
            print(f"Waiting for DATABASE_URL... {timeout}s remaining")
            v = os.getenv('DATABASE_URL')
            if v:
                break
            time.sleep(1)
            timeout -= 1
            
        if not v:
            raise ValueError("DATABASE_URL must be set")
            
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

settings = Settings(
    DATABASE_URL=os.getenv('DATABASE_URL'),
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key'),
    TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')
) 