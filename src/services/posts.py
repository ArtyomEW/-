from schemas.posts import PostsSchema
from utils.unitofwork import IUnitOfWork


class PostService:
    @staticmethod
    async def add_posts(uow: IUnitOfWork, schema):
        async with uow:
            posts_id = await uow.posts.add_one(**schema)
            await uow.commit()
            return posts_id

    @staticmethod
    async def get_posts_for_main(uow: IUnitOfWork):
        async with uow:
            posts = await uow.posts.find_all()
            return posts

    @staticmethod
    async def get_one_posts(uow: IUnitOfWork, **filter_by):
        async with uow:
            posts = await uow.posts.find_one(**filter_by)
            return posts
    
    @staticmethod
    async def get_posts(uow: IUnitOfWork, user_email):
        async with uow:
            posts = await uow.posts.find_all({"user_email": user_email})
            return posts
    

    @staticmethod
    async def delete_post(uow: IUnitOfWork, post_id):
        async with uow:
            await uow.posts.delete(id=post_id)
            await uow.commit()

    @staticmethod
    async def edit_post(uow: IUnitOfWork,post_id, data):

        async with uow:
            await uow.posts.edit_one(id=post_id, data=data)
            await uow.commit()


