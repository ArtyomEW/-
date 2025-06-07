from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form
from api.dependencies import UOWDep
from services.posts import PostService
from schemas.posts import AddPost
from models.users import Users
from utils.dependencies import get_current_user

router_post = APIRouter(prefix='/posts', tags=["Posts"])


@router_post.post("/add_post", summary="Add post")
async def add_post(
    uow: UOWDep,
    name: str = Form(...),  # Получаем из тела формы
    description: str = Form(...),  # Получаем из тела формы
    file: UploadFile = File(...),
    user_data: Users = Depends(get_current_user)
):
    # Ваша логика обработки
    
    schema = {"name": name, "description": description}
    schema["file_name"] = file.filename
    schema["user_email"] = user_data.email 
    
    file_bytes = await file.read()
    
    with open(f'templates/photo/{schema["file_name"]}', 'wb') as file:
                        file.write(file_bytes)

    post_id = await PostService().add_posts(uow=uow, schema=schema)
    return post_id

 
@router_post.get("/get_all_posts") 
async def get_all_post(uow: UOWDep): 
    posts = await PostService().get_posts_for_main(uow)
    return posts


@router_post.get("/get_my_posts") 
async def get_my_posts(uow: UOWDep, user_data: Users = Depends(get_current_user)):
    if not user_data.email:
        return {'status': "errpr"}
    my_posts = await PostService().get_posts(uow=uow, user_email=user_data.email)
    data = []
    for i in my_posts:
        data.append(i.model_dump()) 
    return data



@router_post.delete("/{post_id}")
async def delete_post(uow: UOWDep, post_id: int, 
                      user_data: Users = Depends(get_current_user)):
    await PostService().delete_post(uow,  post_id)
    return {'status': 200}


@router_post.put("/{post_id}")
async def edit_post(uow: UOWDep,
                        post_id: int,
                        name: str = Form(...),  
                        description: str = Form(...),  
                        file: UploadFile = File(...),
                        user_data: Users = Depends(get_current_user)): 
     
    schema = {"name": name, "description": description}
    schema["file_name"] = file.filename
    schema["user_email"] = user_data.email 
    
    file_bytes = await file.read()
    
    with open(f'templates/photo/{schema["file_name"]}', 'wb') as file:
                        file.write(file_bytes)

    await PostService().edit_post(uow, post_id, schema)
