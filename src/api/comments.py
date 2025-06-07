from fastapi import APIRouter, Depends
from api.dependencies import UOWDep
from models.users import Users
from services.comments import CommentsService
from schemas.comments import AddComments
from utils.dependencies import get_current_user


router = APIRouter(prefix="/comments", tags=['comments'])
 

@router.get('/get_comments/{post_id}')
async def get_comments(uow: UOWDep, post_id: int):
    comments = await CommentsService().get_comments(uow, post_id)
    return comments
    

@router.post("/add_comments/{post_id}", summary="add_comments")
async def add_comments(uow: UOWDep, post_id: int, schema: AddComments,      
                       user_data: Users = Depends(get_current_user)):
    comment_id = await CommentsService().add_comments(uow, post_id, schema, user_data.email)  
    return comment_id


@router.delete("/{comment_id}")
async def delete(uow: UOWDep, comment_id: int):
    comment_id = await CommentsService().delete_comment(uow, comment_id)  
    return comment_id
