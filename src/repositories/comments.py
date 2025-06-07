from models.comment import Comments
from utils.repository import SQLAlchemyRepository


class CommentsRepository(SQLAlchemyRepository):
    model = Comments
