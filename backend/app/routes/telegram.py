from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from ..database import get_db
from ..deps import get_current_active_user
from ..models.user import User
from ..telegram import telegram_client
from ..schemas.message import MessageCreate

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post("/link/{telegram_id}")
async def link_telegram_account(
    telegram_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Привязка Telegram аккаунта к профилю пользователя
    """
    # Проверяем, не привязан ли уже этот Telegram ID к другому пользователю
    existing_user = db.query(User).filter(
        User.telegram_id == telegram_id,
        User.id != current_user.id
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Telegram account is already linked to another user"
        )
    
    # П��оверяем существование Telegram аккаунта
    if not await telegram_client.verify_telegram_account(telegram_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Telegram ID"
        )
    
    # Привязываем Telegram ID к пользователю
    current_user.telegram_id = telegram_id
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    # Отправляем приветственное сообщение
    await telegram_client.send_message(
        telegram_id,
        f"Your Telegram account has been successfully linked to {current_user.username}!"
    )
    
    return {"status": "success"}

@router.delete("/unlink")
async def unlink_telegram_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Отвязка Telegram аккаунта от профиля пользователя
    """
    if not current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Telegram account linked"
        )
    
    # Отправляем прощальное сообщение
    await telegram_client.send_message(
        current_user.telegram_id,
        "Your Telegram account has been unlinked from your profile."
    )
    
    current_user.telegram_id = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"status": "success"}

@router.post("/send")
async def send_telegram_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Отправка сообщения через Telegram
    """
    if not current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Telegram account linked"
        )
    
    # Отправляем сообщение через Telegram
    await telegram_client.send_message(
        current_user.telegram_id,
        message.content
    )
    
    return {"status": "success"} 