from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .routes import auth, users, messages, test
from .database import engine
from .bot import start_bot
from .models import user, message

# Создаем таблицы в базе данных
user.Base.metadata.create_all(bind=engine)
message.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Telegram Web Messenger API",
    description="API для веб-мессенджера с интеграцией Telegram",
    version="1.0.0",
    # Добавляем теги для группировки эндпоинтов в документации
    openapi_tags=[
        {"name": "auth", "description": "Операции аутентификации"},
        {"name": "users", "description": "Операции с пользователями"},
        {"name": "messages", "description": "Операции с сообщениями"},
        {"name": "debug", "description": "Отладочные эндпоинты"},
    ]
)

# Настройка CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
    "http://localhost:5001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(test.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Telegram Web Messenger API"}

@app.on_event("startup")
async def startup_event():
    """
    Запуск бота при старте приложения
    """
    asyncio.create_task(start_bot())