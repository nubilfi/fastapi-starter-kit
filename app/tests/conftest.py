"""
Setup fixtures for auth user & endpoints
"""
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.server import app
from app.settings.mysql_settings import SessionLocal
from app.tests.utils.auth import auth_token


@pytest.fixture(scope="session")
def sql_session() -> Generator:
    """session state"""
    yield SessionLocal()


@pytest.fixture(scope="module")
def client_target() -> Generator:
    """setup client"""
    with TestClient(app) as target:
        yield target


@pytest.fixture(scope="module")
def user_token_headers(client_target: TestClient, sql_session: Session) -> Dict[str, str]:
    """fake user data auth"""
    return auth_token(
        client=client_target, username="johndoe", sql=sql_session)
