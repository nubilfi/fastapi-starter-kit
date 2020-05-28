"""
Basic endpoint: /books
"""
from typing import List, Generator
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from app.controllers.books_controller import (
    get_books, get_book, create_book, update_book, delete_book)
from app.schemas.books_schema import BooksInDBBase, BooksCreate, BooksUpdate
from app.schemas.users_schema import UsersBase
from app.settings.mysql_settings import SessionLocal
from app.utils.auth import get_current_active_user

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


@router.get("/", response_model=List[BooksInDBBase])
def get_all_books(
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """return books record"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = get_books(sql)
    return result


@router.get("/{book_id}", response_model=BooksInDBBase)
def get_book_by_id(
        book_id: int = Path(..., title="The Id of the book to get", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """return a specific book record"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = get_book(sql, book_id=book_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return result


@router.post("/", response_model=BooksCreate, status_code=HTTP_201_CREATED)
def add_new_book(
        newbook: BooksCreate,
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """
    Create a book with all the information:

    - **Title**: must have a title
    - **AuthorId**: set the Id of the author (optional field)
    """
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = create_book(sql, book=newbook)
    return result


@router.put("/{book_id}", response_model=BooksUpdate)
def update_book_by_id(
        book: BooksUpdate,
        book_id: int = Path(...,
                            title="The Id of the book to be updated", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """
    update a book with all the information:

    - **book_id**: set the Id of the book, it's required
    - **Title**: must have a title
    - **AuthorId**: set the Id of the author if you want to update it, it's required
    """
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = update_book(sql, book_id=book_id, book=book)

    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return result


@router.delete("/{book_id}")
def delete_book_by_id(
        book_id: int = Path(...,
                            title="The Id of the book to be deleted", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """delete a specific book"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = delete_book(sql, book_id=book_id)
    return result
