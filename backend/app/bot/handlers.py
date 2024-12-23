from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import User

router = Router()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для отправки сообщений.\n"
        "Чтобы привязать аккаунт, используйте команду /link\n"
        f"Ваш Telegram ID: {message.from_user.id}"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📝 Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/link - Показать ваш Telegram ID для привязки\n"
        "/status - Проверить статус привязки"
    )

@router.message(Command("link"))
async def cmd_link(message: Message):
    await message.answer(
        "🔗 Для привязки аккаунта используйте этот ID:\n"
        f"`{message.from_user.id}`\n\n"
        "Перейдите в веб-интерфейс и введите этот ID в соответствующее поле.",
        parse_mode="Markdown"
    )

@router.message(Command("status"))
async def cmd_status(message: Message):
    db = get_db()
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    
    if user:
        await message.answer(
            f"✅ Ваш Telegram аккаунт привязан к пользователю: {user.username}"
        )
    else:
        await message.answer(
            "❌ Ваш Telegram аккаунт не привязан к какому-либо пользователю.\n"
            "Используйте команду /link для получения инструкций по привязке."
        ) 