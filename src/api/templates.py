from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from api.dependencies import UOWDep
from models.users import Users
from utils.dependencies import get_current_user
from services.posts import PostService
from services.users import UsersService


router = APIRouter()

templates = Jinja2Templates(directory='templates/')


# Страница входа
@router.get("/auth", response_class=HTMLResponse, summary="auth template")
async def auth_template(request: Request):
    return templates.TemplateResponse("auth/index.html",
                                      {"request": request})


#страница постов
@router.get("/posts", response_class=HTMLResponse, summary="posts template")
async def posts_template(request: Request):
    return templates.TemplateResponse("posts/mainpost.html",
                                      {"request": request})
 
 

@router.get('/my_posts', response_class=HTMLResponse, summary="posts users")
async def my_posts(request: Request):
    return templates.TemplateResponse("my_post/my_posts.html", {"request": request})
  

 
@router.get('/post', response_class=HTMLResponse, summary="add post")
async def add_post(request: Request):
    return templates.TemplateResponse("my_post/add.html", {"request": request})

 

@router.get('/post/ed/{post_id}', response_class=HTMLResponse, summary="edit post")
async def edit_post(request: Request, post_id: str):
    return templates.TemplateResponse("my_post/edit.html", {"request": request, "post_id": post_id})



@router.get('/post/ed/{post_id}', response_class=HTMLResponse, summary="edit post")
async def edit_post(request: Request, post_id: str):
    return templates.TemplateResponse("my_post/edit.html", {"request": request, "post_id": post_id})


@router.get('/chat/', response_class=HTMLResponse, summary="chat post")
async def chat_post(request: Request, uow: UOWDep,  user_data: Users = Depends(get_current_user)):
    users_all = await UsersService().get_users(uow)
    return templates.TemplateResponse("chat/chat.html", {"request": request, "user": user_data,  'users_all': users_all})
