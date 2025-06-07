from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base
from schemas.message import MessageSchema


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)

    def to_read_model(self) -> MessageSchema:
        return MessageSchema(
            id=self.id,
            sender_id=self.sender_id,
            recipient_id=self.recipient_id,
            content=self.content
        )
    
    