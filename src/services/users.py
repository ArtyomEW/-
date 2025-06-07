from schemas.users import UserSchemaAdd
from utils.unitofwork import IUnitOfWork


class UsersService:
    @staticmethod
    async def add_user(uow: IUnitOfWork, **filter_by):
        async with uow:
            user_id = await uow.users.add_one(**filter_by)
            await uow.commit()
            return user_id

    @staticmethod
    async def get_users(uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    @staticmethod
    async def get_one_user(uow: IUnitOfWork, **filter_by):
        async with uow:
            user = await uow.users.find_one(**filter_by)
            return user
