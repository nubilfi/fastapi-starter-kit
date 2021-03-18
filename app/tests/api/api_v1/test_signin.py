"""
Testing /signin endpoint
"""
from os import getenv

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controllers.users_controller import update_user
from app.schemas.users_schema import UsersUpdate
from app.tests.utils.signin_utils import get_user_test
from app.utils.auth import get_password_hash


def test_access_token(client_target: TestClient, sql_session: Session):
    """
    get access token with user data
    make sure the following user EXIST in user table
    """
    existing_user = get_user_test(sql_session, "johndoe")

    user_in_update = UsersUpdate(Password="secret")
    user = update_user(sql_session, user_id=existing_user.UserId, user=user_in_update)

    if user:
        login_data = {
            "username": user.Username,
            "password": "secret"
        }

        res = client_target.post(f"{getenv('API_PREFIX')}/signin", data=login_data)
        tokens = res.json()
        assert res.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]
