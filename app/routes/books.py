"""
Basic endpoint: /books
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from app.controllers.books_controller import (
    get_books, get_book, create_book, update_book, delete_book)
from app.schemas.books_schema import BooksBase, BooksAction
from app.settings.mysql_settings import SessionLocal

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name


def db_session():
    """
    Get database connection with DI (Dependencies Injection)
    """
    try:
        dbsession = SessionLocal()
        yield dbsession
    finally:
        dbsession.close()


@router.get('/books', response_model=List[BooksBase])
def get_all_books(sql: Session = Depends(db_session)):
    """return books record"""
    result = get_books(sql)
    return result


@router.get("/books/{book_id}", response_model=BooksBase)
def get_book_by_id(
        book_id: int = Path(..., title="The Id of the book to get", ge=0),
        sql: Session = Depends(db_session)
):
    """return a specific book record"""
    result = get_book(sql, book_id=book_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return result


@router.post("/books", response_model=BooksAction, status_code=HTTP_201_CREATED)
def add_new_book(newbook: BooksAction, sql: Session = Depends(db_session)):
    """
    Create a book with all the information:

    - **Title**: must have a title
    - **AuthorId**: set the Id of the author (optional field)
    """
    result = create_book(sql, book=newbook)
    return result


@router.put("/books/{book_id}", response_model=BooksAction)
def update_book_by_id(
        book: BooksAction,
        book_id: int = Path(...,
                            title="The Id of the book to be updated", ge=0),
        sql: Session = Depends(db_session)
):
    """
    update a book with all the information:

    - **book_id**: set the Id of the book, it's required
    - **Title**: must have a title
    - **AuthorId**: set the Id of the author if you want to update it (optional field)
    """
    result = update_book(sql, book_id=book_id, book=book)

    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return result


@router.delete("/books/{book_id}")
def delete_book_by_id(
        book_id: int = Path(...,
                            title="The Id of the book to be deleted", ge=0),
        sql: Session = Depends(db_session)
):
    """delete a specific book"""
    result = delete_book(sql, book_id=book_id)

    return result
