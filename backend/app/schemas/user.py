from pydantic import BaseModel, EmailStr
from typing import Optional

# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Схема для создания пользователя
class UserCreate(UserBase):
    password: str

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    telegram_id: Optional[str] = None

# Схема для отображения пользователя
class User(UserBase):
    id: int
    is_active: bool
    telegram_id: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "username",
                "id": 1,
                "is_active": True,
                "telegram_id": None
            }
        }