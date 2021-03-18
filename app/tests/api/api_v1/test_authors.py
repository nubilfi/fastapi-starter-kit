"""
Testing /authors endpoint
"""
from os import getenv
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.authors_utils import create_random_author
from app.tests.utils.utils import random_lower_string


def test_get_all_authors(
        client_target: TestClient,
        user_token_headers: Dict[str, str]
):
    """should return a list of all author record"""
    res = client_target.get(f"{getenv('API_PREFIX')}/authors", headers=user_token_headers)
    authors = res.json()

    assert res.status_code == 200

    if authors:
        assert authors
    else:
        assert len(authors) == 0


def test_get_author_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """should return a single list of author record"""
    item = create_random_author(sql_session)
    res = client_target.get(
        f"{getenv('API_PREFIX')}/authors/{item.AuthorId}",
        headers=user_token_headers
    )

    assert res.status_code == 200
    author = res.json()
    assert author["AuthorId"] == item.AuthorId
    assert author["Name"] == item.Name


def test_add_new_author(
        client_target: TestClient,
        user_token_headers: Dict[str, str]
):
    """create a new author record"""
    data = {"Name": "Foo"}
    res = client_target.post(
        f"{getenv('API_PREFIX')}/authors/",
        headers=user_token_headers, json=data
    )

    assert res.status_code == 201
    author = res.json()
    assert author["Name"] == data["Name"]


def test_update_author(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """update an author record"""
    item = create_random_author(sql_session)
    updated_data = {"Name": random_lower_string()}
    res = client_target.put(
        f"{getenv('API_PREFIX')}/authors/{item.AuthorId}",
        headers=user_token_headers,
        json=updated_data
    )

    assert res.status_code == 200
    new_author = res.json()
    assert new_author["Name"] == updated_data["Name"]


def test_delete_author_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """delete a specific author record"""
    item = create_random_author(sql_session)
    res = client_target.delete(
        f"{getenv('API_PREFIX')}/authors/{item.AuthorId}",
        headers=user_token_headers
    )

    assert res.status_code == 204
