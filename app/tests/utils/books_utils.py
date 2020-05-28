"""test books util functions"""
from sqlalchemy.orm import Session
from app.controllers.books_controller import create_book
from app.schemas.books_schema import BooksBase
from app.models.books_model import Books
from app.tests.utils.authors_utils import create_random_author
from app.tests.utils.utils import random_lower_string


def create_random_book(sql: Session) -> Books:
    """create a random book values"""
    title = random_lower_string()
    author = create_random_author(sql)

    book_in = BooksBase(Title=title, AuthorId=author.AuthorId)
    return create_book(sql, book=book_in)
