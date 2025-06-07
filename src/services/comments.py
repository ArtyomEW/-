from utils.unitofwork import IUnitOfWork

class CommentsService:

    @staticmethod
    async def get_comments(uow: IUnitOfWork, post_id: int):
        
        async with uow:
            comments = await uow.comments.find_all({"post_id": post_id})
        
        return comments
    

    @staticmethod
    async def add_comments(uow: IUnitOfWork, post_id, schema, user_email):
        schema = schema.model_dump()
        schema["post_id"] = post_id
        schema["user_email"] = user_email
        async with uow:
            id_model = await uow.comments.add_one(**schema)
            await uow.commit()
            return id_model
        

    @staticmethod
    async def delete_comment(uow: IUnitOfWork, comment_id):
        async with uow:
            await uow.comments.delete(comment_id)
            await uow.commit()