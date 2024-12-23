from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from fastapi import HTTPException, status
from .config import settings

class TelegramClient:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    async def send_message(self, chat_id: str, text: str) -> bool:
        """
        Отправка сообщения через Telegram бота
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            return True
        except TelegramBadRequest as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Telegram error: {str(e)}"
            )
    
    async def verify_telegram_account(self, chat_id: str) -> bool:
        """
        Проверка существования Telegram аккаунта
        """
        try:
            chat = await self.bot.get_chat(chat_id)
            return bool(chat)
        except TelegramBadRequest:
            return False
    
    async def close(self):
        """
        Закрытие сессии бота
        """
        await self.bot.session.close()

telegram_client = TelegramClient() 