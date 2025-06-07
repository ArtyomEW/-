from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)    



    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password)
