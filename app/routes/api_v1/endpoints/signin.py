"""
Basic endpoint: /users
"""
from os import getenv
from datetime import timedelta
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt import PyJWTError

from app.utils.auth import (
    authenticate_user, create_access_token, check_user, oauth2_scheme, jwt
)
from app.controllers.users_controller import login_user
from app.schemas.users_schema import UsersBase
from app.schemas.token_schema import Token, TokenData
from app.settings.mysql_settings import SessionLocal

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name


def db_session() -> Generator:
    """
    Get database connection with DI (Dependencies Injection)
    """
    try:
        dbsession = SessionLocal()
        yield dbsession
    finally:
        dbsession.close()


fetched_user = {}


async def get_current_user(token: str = Depends(oauth2_scheme)):
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

    user = check_user(fetched_user, username=token_data.Username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: UsersBase = Depends(get_current_user)):
    """check user status"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/signin", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        sql: Session = Depends(db_session)
):
    """Provide access token to user for accessing a specific endpoint"""
    try:
        res = login_user(sql, form_data.username)

        fetched_user.update({
            "Username": res.Username,
            "Fullname": res.Fullname,
            "Password": res.Password,
            "Email": res.Email,
            "Status": res.Status
        })
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(
        fetched_user, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=int(getenv("ACCESS_TOKEN_VALIDITY")))
    access_token = create_access_token(
        data={"sub": user.Username}, expires_time=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
