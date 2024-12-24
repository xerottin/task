from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Any
from pydantic import BaseModel

from ..database import get_db
from ..deps import get_current_active_user
from ..models.user import User
from ..schemas.user import User as UserSchema, UserUpdate
from ..bot.bot import connection_codes

router = APIRouter(prefix="/users", tags=["users"])

# Добавляем модель для получения кода
class TelegramConnect(BaseModel):
    code: str

@router.get("/me", response_model=UserSchema)
def read_current_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Получить текущего пользователя.
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Обновить данные текущего пользователя.
    """
    # Проверяем, не занят ли email д��угим пользователем
    if user_in.email:
        user = db.query(User).filter(
            User.email == user_in.email,
            User.id != current_user.id
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Проверяем, не занят ли username другим пользователем
    if user_in.username:
        user = db.query(User).filter(
            User.username == user_in.username,
            User.id != current_user.id
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Обновляем данные пользователя
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user 

@router.post("/connect-telegram")
async def connect_telegram(
    data: TelegramConnect,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Подключение Telegram аккаунта к пользователю
    """
    try:
        print(f"Attempting to connect Telegram with code: {data.code}")
        print(f"Available codes: {connection_codes}")
        
        if data.code not in connection_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный код подключения"
            )
        
        # Получаем Telegram ID и конвертируем в строку
        telegram_id = str(connection_codes[data.code])  # Конвертируем в строку
        print(f"Found Telegram ID: {telegram_id}")
        
        # Проверяем существующего пользователя
        existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот Telegram аккаунт уже привязан к другому пользователю"
            )
        
        # Обновляем пользователя
        current_user.telegram_id = telegram_id
        db.commit()
        
        del connection_codes[data.code]
        
        print(f"Successfully connected Telegram for user {current_user.username}")
        return {"status": "success", "message": "Telegram успешно подключен"}
        
    except Exception as e:
        print(f"Error connecting Telegram: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 