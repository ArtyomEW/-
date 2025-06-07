from typing import List
from fastapi import APIRouter, Response
from exception.errorfile import IncorrectEmailOrPasswordException, PasswordMismatchException, UserAlreadyExistsException
from utils.auth_utils import get_password_hash, authenticate_user, create_access_token
from services.users import UsersService
from schemas.users import SUserRegister, SUserAuth
from api.dependencies import UOWDep
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from schemas.users import SUserRead


templates = Jinja2Templates(directory='frontend')



router = APIRouter(prefix='/auth', tags=['Auth'])


@router.get("/", response_class=HTMLResponse, summary="Страница авторизации")
async def get_categories(request: Request):
    return templates.TemplateResponse("auth/index.html", {"request": request})



@router.get("/users", response_model=List[SUserRead])
async def get_users(uow: UOWDep):
    users_all = await UsersService.get_users(uow=uow)
    # Используем генераторное выражение для создания списка
    return [{'id': user.id, 'name': user.name} for user in users_all]



@router.post("/register/")
async def register_user(uow: UOWDep, user_data: SUserRegister) -> dict:
    user = await UsersService.get_one_user(uow=uow, email=user_data.email) 
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("Пароли не совпадают")
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add_user(uow=uow,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, uow: UOWDep, user_data: SUserAuth):
    check = await authenticate_user(uow=uow, email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}

  
@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}