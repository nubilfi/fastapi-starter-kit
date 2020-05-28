"""
It is a Pydantic model for Books
"""
from typing import Optional
from pydantic import BaseModel


class BooksBase(BaseModel):
    """
    A schema class used to represent Books table column values
    """
    Title: Optional[str] = None
    AuthorId: Optional[int] = None

    class Config:
        """
        Instead of using title = data["Title"]
        replace it with title = data.Title
        """
        orm_mode = True


class BooksCreate(BooksBase):
    """
    A schema class used to represent column to create a new book
    """
    Title: str
    AuthorId: int

    class Config:
        """enable orm mode"""
        orm_mode = True


class BooksUpdate(BooksBase):
    """
    A schema class used to represent column to create a new book
    """
    Title: str
    AuthorId: int

    class Config:
        """enable orm mode"""
        orm_mode = True


class BooksInDBBase(BooksBase):
    """
    A schema class used to represent book data based on its ID
    """
    BookId: Optional[int] = None

    class Config:
        """enable orm mode"""
        orm_mode = True
        