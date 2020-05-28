"""
It is a Pydantic model for Authors
"""
from typing import Optional
from pydantic import BaseModel


class AuthorsBase(BaseModel):
    """
    A schema class used to represent Authors table column values
    """
    Name: Optional[str] = None

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class AuthorsCreate(AuthorsBase):
    """
    A schema class used to represent column to create a new author
    """
    Name: str

    class Config:
        """enable orm mode"""
        orm_mode = True



class AuthorsUpdate(AuthorsBase):
    """
    A schema class used to represent column to create a new author
    """
    Name: str

    class Config:
        """enable orm mode"""
        orm_mode = True


class AuthorsInDBBase(AuthorsBase):
    """
    A schema class used to represent user data based on its ID
    """
    AuthorId: Optional[int] = None

    class Config:
        """enable orm mode"""
        orm_mode = True
