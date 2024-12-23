from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Базовая схема сообщения
class MessageBase(BaseModel):
    content: str
    recipient_id: int

# Схема для создания сообщения
class MessageCreate(MessageBase):
    pass

# Схема для отображения сообщения
class Message(MessageBase):
    id: int
    sender_id: int
    telegram_message_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True 