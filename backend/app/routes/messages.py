from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.message import Message
from ..schemas.message import MessageCreate, Message as MessageSchema
from ..deps import get_current_active_user
from ..bot.bot import bot  # Импортируем бота

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("", response_model=MessageSchema)
async def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Отправка сообщения пользователю
    """
    # Проверяем существование получателя
    recipient = db.query(User).filter(User.id == message.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )

    # Создаем сообщение в БД
    db_message = Message(
        content=message.content,
        sender_id=current_user.id,
        recipient_id=message.recipient_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Если у получателя есть Telegram ID, отправляем сообщение через бота
    if recipient.telegram_id:
        try:
            telegram_message = await bot.send_message(
                chat_id=recipient.telegram_id,
                text=f"Сообщение от {current_user.username}:\n{message.content}"
            )
            # Сохраняем ID сообщения из Telegram
            db_message.telegram_message_id = str(telegram_message.message_id)
            db.commit()
        except Exception as e:
            print(f"Error sending telegram message: {e}")
            # Не выбрасываем исключение, так как сообщение уже сохранено в БД

    return db_message

@router.get("", response_model=List[MessageSchema])
async def get_messages(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получение всех сообщений текущего пользователя
    """
    messages = db.query(Message).filter(
        (Message.sender_id == current_user.id) | 
        (Message.recipient_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    return messages

@router.get("/chat/{user_id}", response_model=List[MessageSchema])
async def get_chat_messages(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получение сообщений чата с конкретным пользователем
    """
    messages = db.query(Message).filter(
        (
            (Message.sender_id == current_user.id) & 
            (Message.recipient_id == user_id)
        ) | (
            (Message.sender_id == user_id) & 
            (Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.desc()).all()
    return messages 

@router.get("/stats", response_model=dict)
async def get_message_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получение статистики сообщений пользователя
    """
    total_messages = db.query(Message).filter(
        (Message.sender_id == current_user.id) | 
        (Message.recipient_id == current_user.id)
    ).count()
    
    return {
        "total_messages": total_messages
    }

@router.post("/send-bot-message")
async def send_bot_message(
    message: str,
    recipient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Отправка сообщения от имени бота конкретному пользователю
    """
    try:
        print(f"Attempting to send message to recipient {recipient_id}")
        # Находим получателя
        recipient = db.query(User).filter(User.id == recipient_id).first()
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Получатель не найден"
            )
            
        print(f"Recipient found: {recipient.username}, telegram_id: {recipient.telegram_id}")
        if not recipient.telegram_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="У получателя не подключен Telegram"
            )
            
        # Отправляем сообщение через бота
        print("Sending message via bot...")
        await bot.send_message(
            chat_id=recipient.telegram_id,
            text=f"🤖 Сообщение от {current_user.username}:\n\n{message}"
        )
        print("Message sent successfully")
        
        # Сохраняем сообщение в базе данных
        db_message = Message(
            content=message,
            sender_id=current_user.id,
            recipient_id=recipient_id
        )
        db.add(db_message)
        db.commit()
        
        return {"status": "success", "message": "Сообщение отправлено"}
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/users", response_model=List[dict])
async def get_users_for_messages(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получение списка пользователей для отправки сообщений
    """
    try:
        print("Getting users for messages...")
        # Получаем только пользователей с подключенным Telegram
        users = db.query(User).filter(
            User.id != current_user.id,  # Исключаем текущего пользователя
            User.telegram_id.isnot(None)  # Только с подключенным Telegram
        ).all()
        
        result = [{"id": user.id, "username": user.username} for user in users]
        print(f"Found {len(result)} users:", result)
        return result
    except Exception as e:
        print(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )