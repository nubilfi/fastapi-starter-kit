"""
Testing /signin endpoint
"""
from os import getenv

from fastapi.testclient import TestClient


def test_access_token(client_target: TestClient) -> None:
    """
    get access token with user data
    make sure the following user EXIST in user table
    """
    login_data = {
        "username": "johndoe",
        "password": "secret"
    }

    res = client_target.post(f"{getenv('API_PREFIX')}/signin", data=login_data)
    tokens = res.json()
    assert res.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
