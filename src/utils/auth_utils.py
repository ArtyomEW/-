from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from config.config import SECRET_KEY, ALGORITHM
from services.users import UsersService
from api.dependencies import UOWDep

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(uow: UOWDep, email: EmailStr, password: str):
    user = await UsersService.get_one_user(uow=uow, email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user
 

