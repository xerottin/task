from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from ..database import get_db
from ..deps import get_current_active_user
from ..models.user import User
from ..schemas.user import User as UserSchema, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

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
    # Проверяем, не занят ли email другим пользователем
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