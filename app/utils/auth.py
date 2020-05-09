"""
Auth functions
"""
from datetime import datetime, timedelta
from os import getenv

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config import set_dotenv
from app.schemas.users_schema import UsersAction


set_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{getenv('API_PREFIX')}/signin")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify user password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """hashed password"""
    return pwd_context.using(rounds=3).hash(password)


def check_user(data: dict, username: str):
    """get user data"""
    if username == data["Username"]:
        return UsersAction(**data)


def authenticate_user(user, username: str, password: str):
    """authenticate user credential"""
    user_data = check_user(user, username)

    if not user_data:
        return False
    if not verify_password(password, user_data.Password):
        return False

    return user_data


def create_access_token(*, data: dict, expires_time: timedelta = None) -> str:
    """generate access token to user"""
    _encode = data.copy()

    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(getenv("ACCESS_TOKEN_VALIDITY")))

    _encode.update({"exp": expire})
    encoded_jwt = jwt.encode(_encode, getenv(
        "SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt
