"""
It is a Pydantic model for Books
"""
from pydantic import BaseModel


class BooksBase(BaseModel):
    """
    A schema class used to represent Books table column values
    """
    BookId: int
    Title: str
    AuthorId: int

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class BooksAction(BaseModel):
    """
    A schema class used to represent column to create a new book
    """
    Title: str
    AuthorId: int = None

    class Config:
        """
        Instead of using title = data["Title"]
        replace it with title = data.Title
        """
        orm_mode = True
