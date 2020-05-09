"""
It is a Pydantic model for Users
"""
from pydantic import BaseModel


class Users(BaseModel):
    """
    A schema class used to represent Users table column values
    """
    UserId: int = None

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class UsersBase(Users):
    """
    A schema class used to represent Users table column values
    """
    Username: str
    Fullname: str = None
    Email: str
    Status: bool = None

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class UsersAction(UsersBase):
    """
    A schema class used to represent column to create a new user
    """
    Password: str

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True
