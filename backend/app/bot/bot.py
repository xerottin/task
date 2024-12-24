from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from ..config import settings
import random
import string
import asyncio

# Создаем экземпляр бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Глобальная переменная для хранения кодов подключения
connection_codes = {}

@dp.message(Command("start"))
async def cmd_start(message):
    """
    Обработчик команды /start
    """
    try:
        # Генерируем уникальный код для подключения
        code = ''.join(random.choices(string.digits, k=6))
        connection_codes[code] = message.from_user.id
        
        print(f"Generated code {code} for Telegram ID {message.from_user.id}")
        
        await message.answer(
            f"Ваш код для подключения: {code}\n\n"
            "Введите этот код на сайте для привязки Telegram аккаунта."
        )
    except Exception as e:
        print(f"Error in start command: {e}")

async def start_bot():
    """
    Функция запуска бота
    """
    try:
        print("Starting bot...")
        print(f"Bot token: {settings.TELEGRAM_BOT_TOKEN[:5]}...")  # Показываем только начало токена
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"Error starting bot: {e}")
        if not bot.session.closed:
            await bot.session.close()

async def stop_bot():
    """
    Функция остановки бота
    """
    try:
        if not bot.session.closed:
            await bot.session.close()
    except Exception as e:
        print(f"Error stopping bot: {e}")

# Экспортируем бота для использования в других модулях
__all__ = ['bot', 'dp', 'connection_codes', 'start_bot', 'stop_bot'] 