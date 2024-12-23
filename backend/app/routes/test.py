# test.py
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/ping")
async def ping():
    """
    Проверка соединения
    """
    return {"status": "success", "message": "pong"}

@router.get("/health")
async def health_check():
    """
    Проверка здоровья сервера
    """
    return {
        "status": "online",
        "service": "Telegram Web Messenger API",
        "version": "1.0.0"
    }