from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base
from schemas.comments import CommentsSchema
from .post import Post

class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    user_email: Mapped[str] = mapped_column(Text)
    comment: Mapped[str] = mapped_column(Text)

    def to_read_model(self) -> CommentsSchema:
        return CommentsSchema(
            id=self.id,
            post_id=self.post_id,
            user_email=self.user_email,
            comment=self.comment
        )
    