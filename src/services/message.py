from utils.unitofwork import IUnitOfWork
from sqlalchemy import select, and_, or_
from models.message import Message

class MessageService:
    model = Message

    @classmethod
    async def get_messages_between_users(cls, uow: IUnitOfWork, user_id_1: int, user_id_2: int):
        """
        Асинхронно находит и возвращает все сообщения между двумя пользователями.

        Аргументы:
            user_id_1: ID первого пользователя.
            user_id_2: ID второго пользователя.

        Возвращает:
            Список сообщений между двумя пользователями.
        """
        async with uow: 

            query = select(cls.model).filter(
                or_(
                    and_(cls.model.sender_id == user_id_1, cls.model.recipient_id == user_id_2),
                    and_(cls.model.sender_id == user_id_2, cls.model.recipient_id == user_id_1)
                )
            ).order_by(cls.model.id)

            res = await uow.session.execute(query)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    @staticmethod
    async def add_message(uow: IUnitOfWork, **filter_by):
        async with uow:
            message_id = await uow.message.add_one(**filter_by)
            await uow.commit()
            return message_id
 









