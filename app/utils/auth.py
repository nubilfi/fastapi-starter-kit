"""
Auth functions
"""
from datetime import datetime, timedelta
from typing import Optional, Generator
from os import getenv

import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.controllers.users_controller import check_user
from app.models.users_model import Users
from app.schemas.token_schema import TokenData
from app.schemas.users_schema import UsersBase
from app.settings.mysql_settings import SessionLocal
from app.config import set_dotenv

set_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{getenv('API_PREFIX')}/signin")


def db_session() -> Generator:
    """
    Get database connection with DI (Dependencies Injection)
    """
    dbsession = SessionLocal()
    try:
        yield dbsession
    finally:
        dbsession.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify user password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """hashed password"""
    return pwd_context.hash(password)


def authenticate_user(sql: Session, username: str, password: str) -> Optional[Users]:
    """authenticate user credential"""
    user_data = check_user(sql, username=username)

    if not user_data:
        return None
    if not verify_password(password, user_data.Password):
        return None

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


def get_current_user(sql: Session = Depends(db_session), token: str = Depends(oauth2_scheme)):
    """get authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")]
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(Username=username)
    except PyJWTError:
        raise credentials_exception

    user = check_user(sql, username=token_data.Username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_active_user(current_user: UsersBase = Depends(get_current_user)):
    """check user status"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_password_reset_token(token: str) -> Optional[str]:
    """validate user token to reset password"""
    try:
        decoded_token = jwt.decode(token, getenv(
            "SECRET_KEY"), algorithm=getenv("ALGORITHM"))
        return decoded_token["sub"]
    except PyJWTError:
        return None
