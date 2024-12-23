from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, User as UserSchema
from ..schemas.token import Token
from ..security import verify_password, get_password_hash, create_access_token
from ..config import settings
from ..deps import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserSchema)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    print(f"Attempting to register user: {user_in.username}")
    
    # Проверяем, существует ли пользователь с таким email
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        print(f"Email {user_in.email} already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Проверяем, существует ли пользователь с таким username
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        print(f"Username {user_in.username} already taken")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Создаем нового пользователя
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=True
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"Successfully registered user: {user_in.username}")
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 совместимый токен для логина JWT
    """
    print(f"Login attempt for user: {form_data.username}")
    
    # Пытаемся найти пользователя по username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        print(f"User not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем пароль
    if not verify_password(form_data.password, user.hashed_password):
        print(f"Invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    print(f"Login successful for user: {form_data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/test-token", response_model=UserSchema)
async def test_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Тестовый эндпоинт для проверки токена
    """
    return current_user

@router.get("/users", tags=["debug"])
def get_all_users(db: Session = Depends(get_db)):
    """
    Временный эндпоинт для отладки
    """
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]