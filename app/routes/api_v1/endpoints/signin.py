"""
Basic endpoint: /users
"""
from os import getenv
from datetime import timedelta
from typing import Generator, Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils.auth import (
    authenticate_user, create_access_token, get_password_hash, verify_password_reset_token
)
from app.controllers.users_controller import check_user
from app.schemas.token_schema import Token
from app.schemas.message_schema import Message
from app.settings.mysql_settings import SessionLocal

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name


def db_session() -> Generator:
    """
    Get database connection with DI (Dependencies Injection)
    """
    dbsession = SessionLocal()
    try:
        yield dbsession
    finally:
        dbsession.close()


@router.post("/signin", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        sql: Session = Depends(db_session)
) -> Any:
    """Authenticate user data"""
    user = authenticate_user(
        sql, form_data.username, form_data.password)

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


@router.post("/reset-password", response_model=Message)
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        sql: Session = Depends(db_session)
) -> Any:
    """
    reset user password
    """
    user = verify_password_reset_token(token)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    user_data = check_user(sql, username=user)

    if not user_data:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist"
        )

    if user_data.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = get_password_hash(new_password)

    user_data.Password = hashed_password
    sql.add(user_data)
    sql.commit()

    return {"message": "Password update successfully"}
