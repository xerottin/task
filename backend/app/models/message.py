from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    telegram_message_id = Column(String, nullable=True)
    is_bot_message = Column(Boolean, default=False)

    # Отношения
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")