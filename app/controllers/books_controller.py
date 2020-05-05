"""
Provide logic for /books endpoint
"""
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.schemas.books_schema import BooksAction
from app.models.books_model import Books


def get_books(sql: Session):
    """return books record"""
    return sql.query(Books).all()


def get_book(sql: Session, book_id: int):
    """return a specific book record"""
    return sql.query(Books).filter(Books.BookId == book_id).first()


def create_book(sql: Session, book: BooksAction):
    """
    Create a record of book with its Title
    """
    new_book = Books(
        Title=book.Title,
        AuthorId=book.AuthorId,
    )
    sql.add(new_book)
    sql.commit()
    sql.refresh(new_book)
    return new_book


def update_book(sql: Session, book_id: int, book: BooksAction):
    """
    Update a specific book
    """
    old_data = sql.query(Books).filter(Books.BookId == book_id).first()

    if old_data is not None:
        new_data = book.dict()
        old_data.Title = new_data["Title"]

        sql.commit()

    return old_data


def delete_book(sql: Session, book_id: int):
    """Delete a specific book"""
    old_data = sql.query(Books).filter(Books.BookId == book_id).first()

    if old_data:
        sql.query(Books).filter(Books.BookId == book_id).delete(
            synchronize_session='evaluate')
        sql.commit()
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"Book with Id: {book_id} cannot be found."}
        )

    return JSONResponse(
        status_code=204,
        content={
            "message": f"Book with id: {book_id} has been successfully deleted."}
    )
