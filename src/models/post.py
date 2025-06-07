from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import LargeBinary, ForeignKey
from .users import Users
from schemas.posts import PostsSchema

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    file_name: Mapped[str] = mapped_column(nullable=True)
    user_email: Mapped[str] = mapped_column(nullable=False)


    def to_read_model(self) -> PostsSchema:
        return PostsSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            file_name=self.file_name,
            user_email=self.user_email,
        )
