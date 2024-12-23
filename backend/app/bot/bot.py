from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from ..config import settings
from . import handlers

async def check_token(token: str) -> bool:
    """Проверка валидности токена"""
    try:
        test_bot = Bot(token=token)
        me = await test_bot.get_me()
        print(f"Бот успешно авторизован как: {me.username}")
        await test_bot.session.close()
        return True
    except Exception as e:
        print(f"Ошибка проверки токена: {e}")
        return False

# Инициализация бота и диспетчера
bot = None  # Инициализируем позже

# Временно для отладки
TELEGRAM_TOKEN = "7503574488:AAHd3Jm7UP0iRjnxIrYxE8xOkF_B7R5WjZQ"

async def start_bot():
    """
    Запуск бота
    """
    global bot
    token = TELEGRAM_TOKEN
    print(f"Starting bot with token: {token}")
    
    if not await check_token(token):
        print("Неверный токен бота! Проверьте TELEGRAM_BOT_TOKEN в .env файле")
        return

    try:
        bot = Bot(token=token)
        dp = Dispatcher()
        dp.include_router(handlers.router)
        
        print("Bot successfully initialized!")
        print(f"Bot info: @{(await bot.get_me()).username}")
        
        await bot.delete_webhook(drop_pending_updates=True)
        print("Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        if bot and bot.session and not bot.session.closed:
            await bot.session.close() 