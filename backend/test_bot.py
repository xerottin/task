import asyncio
from aiogram import Bot

async def test_bot():
    token = "7503574488:AAHd3Jm7UP0iRjnxIrYxE8xOkF_B7R5WjZQ"
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"Бот успешно авторизован как: {me.username}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_bot()) 