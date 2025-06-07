from repositories.comments import CommentsRepository
from repositories.message import MessageRepository
from repositories.users import UsersRepository
from repositories.posts import PostRepository
from db.db import async_session_maker
from abc import ABC, abstractmethod
from typing import Type


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    posts: Type[MessageRepository]
    comments: Type[CommentsRepository]
    posts: Type[PostRepository]


    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.comments = CommentsRepository(self.session)
        self.posts = PostRepository(self.session)
        self.message = MessageRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
