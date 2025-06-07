from exception.errorfile import TokenExpiredException, NoJwtException, NoUserIdException, TokenNoFoundException
from fastapi import Request, HTTPException, status, Depends
from config.config import SECRET_KEY, ALGORITHM
from services.users import UsersService
from datetime import datetime, timezone
from jose import jwt, JWTError
from api.dependencies import UOWDep


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNoFoundException
    return token



async def get_current_user(uow: UOWDep, token: str = Depends(get_token)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException
    
    user = await UsersService.get_one_user(uow=uow, id=int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user



