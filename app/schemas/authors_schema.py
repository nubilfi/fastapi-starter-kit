"""
It is a Pydantic model for Authors
"""
from pydantic import BaseModel


class AuthorsBase(BaseModel):
    """
    A schema class used to represent Authors table column values
    """
    AuthorId: int
    Name: str

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class AuthorsAction(BaseModel):
    """
    A schema class used to represent column to create a new author
    """
    Name: str

    class Config:
        """
        Instead of using name = data["Name"]
        replace it with name = data.Name
        """
        orm_mode = True
