from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from .config import settings
from .database import SessionLocal
from .models.user import User

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start
    """
    await message.answer(
        "Привет! Я бот для отправки сообщений. "
        "Чтобы привязать аккаунт, используйте ваш Telegram ID: "
        f"{message.from_user.id}"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обработчик команды /help
    """
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Пок��зать это сообщение\n"
        "/id - Показать ваш Telegram ID"
    )

@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    """
    Обработчик команды /id
    """
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")

async def start_bot():
    """
    Запуск бота
    """
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close() 