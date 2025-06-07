from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from services.message import MessageService
from schemas.message import MessageRead, MessageCreate
from services.users import UsersService
from utils.dependencies import get_current_user
from api.dependencies import UOWDep 
from models.users import Users
import asyncio
import logging


router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='frontend')


# Страница чата
@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, uow: UOWDep, user_data: Users = Depends(get_current_user)):
    users_all = await UsersService.get_users(uow)
    return templates.TemplateResponse("chat.html",
                                      {"request": request, "user": user_data, 'users_all': users_all})



@router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, uow:UOWDep, current_user: Users = Depends(get_current_user)):
    res = await MessageService.get_messages_between_users(uow=uow, user_id_1=current_user.id, user_id_2=user_id) or []
    return res
    




active_connections: Dict[int, WebSocket] = {}


# Функция для отправки сообщения пользователю, если он подключен
async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        # Отправляем сообщение в формате JSON
        await websocket.send_json(message)


# WebSocket эндпоинт для соединений
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Принимаем WebSocket-соединение
    await websocket.accept()
    # Сохраняем активное соединение для пользователя
    active_connections[user_id] = websocket
    try:
        while True:
            # Просто поддерживаем соединение активным (1 секунда паузы)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, uow:UOWDep, current_user: Users = Depends(get_current_user)):
    # Add new message to the database
    await MessageService.add_message(uow=uow,
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id
    )
    
# Подготавливаем данные для отправки сообщения
    message_data = {
        'sender_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
    }
    # Уведомляем получателя и отправителя через WebSocket
    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)

    # Возвращаем подтверждение сохранения сообщения

    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}