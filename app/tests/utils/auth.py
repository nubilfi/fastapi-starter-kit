"""
Fake user auth functions
"""
from os import getenv
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controllers.users_controller import check_user, create_user, update_user
from app.schemas.users_schema import UsersCreate, UsersUpdate
from app.tests.utils.utils import random_lower_string
from app.config import set_dotenv

set_dotenv()


def user_auth_headers(
        *,
        client: TestClient,
        username: str,
        password: str
) -> Dict[str, str]:
    """set auth headers"""
    data = {"username": username, "password": password}

    res = client.post(f"{getenv('API_PREFIX')}/signin", data=data)
    result = res.json()
    token = result["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def auth_token(
        *,
        client: TestClient,
        username: str,
        sql: Session
) -> Dict[str, str]:
    """
    return a valid token for the user with given username.
    if the user does not exist, created first
    """
    password = random_lower_string()
    user = check_user(sql, username=username)

    if not user:
        user_in_create = UsersCreate(Username=username, Password=password)
        user = create_user(sql, user=user_in_create)
    else:
        user_in_update = UsersUpdate(Password=password)
        user = update_user(sql, user_id=user.UserId, user=user_in_update)

    return user_auth_headers(client=client, username=username, password=password)
