"""
Testing /books endpoint
"""
from os import getenv
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.books_utils import create_random_book
from app.tests.utils.authors_utils import create_random_author


def test_get_books(
        client_target: TestClient,
        user_token_headers: Dict[str, str]
):
    """should return a list of all books record"""
    res = client_target.get(f"{getenv('API_PREFIX')}/books", headers=user_token_headers)
    books = res.json()

    assert res.status_code == 200

    if books:
        assert books
    else:
        assert len(books) == 0


def test_get_book_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """should return a single list of book record"""
    item = create_random_book(sql_session)
    res = client_target.get(
        f"{getenv('API_PREFIX')}/books/{item.BookId}",
        headers=user_token_headers
    )

    assert res.status_code == 200
    book = res.json()
    assert book["BookId"] == item.BookId
    assert book["Title"] == item.Title
    assert book["AuthorId"] == item.AuthorId


def test_add_new_book(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """create a new author record"""
    author = create_random_author(sql_session)
    data = {"Title": "Foo", "AuthorId": author.AuthorId}

    res = client_target.post(
        f"{getenv('API_PREFIX')}/books/",
        headers=user_token_headers,
        json=data
    )

    assert res.status_code == 201
    author = res.json()
    assert author["Title"] == data["Title"]
    assert author["AuthorId"] == data["AuthorId"]


def test_update_book(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """update a book record"""
    author = create_random_author(sql_session)
    item = create_random_book(sql_session)
    updated_data = {"Title": "Foo", "AuthorId": author.AuthorId}

    res = client_target.put(
        f"{getenv('API_PREFIX')}/books/{item.BookId}",
        headers=user_token_headers,
        json=updated_data
    )

    assert res.status_code == 200
    new_book = res.json()
    assert new_book["Title"] == updated_data["Title"]
    assert new_book["AuthorId"] == updated_data["AuthorId"]


def test_delete_book_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """delete a specific book record"""
    item = create_random_book(sql_session)
    res = client_target.delete(
        f"{getenv('API_PREFIX')}/books/{item.BookId}",
        headers=user_token_headers
    )

    assert res.status_code == 204
