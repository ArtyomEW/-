from models.message import Message 
from utils.repository import SQLAlchemyRepository


class MessageRepository(SQLAlchemyRepository):
    model = Message
