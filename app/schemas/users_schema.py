"""
It is a Pydantic model for Users
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class UsersBase(BaseModel):
    """
    A schema class used to represent Users table column values
    """
    Username: Optional[str] = None
    Fullname: Optional[str] = None
    Email: Optional[EmailStr] = None
    Status: bool = None

    class Config:
        """
        Instead of using username = data["Username"]
        replace it with username = data.Username
        """
        orm_mode = True


class UsersCreate(UsersBase):
    """
    A schema class used to represent column to create a new user
    """
    Username: str
    Password: str

    class Config:
        """enable orm mode"""
        orm_mode = True


class UsersUpdate(UsersBase):
    """
    A schema class used to update user password
    """
    Password: Optional[str] = None

    class Config:
        """enable orm mode"""
        orm_mode = True


class UsersInDBBase(UsersBase):
    """
    A schema class used to represent user data based on its ID
    """
    UserId: Optional[int] = None

    class Config:
        """enable orm mode"""
        orm_mode = True


class User(UsersInDBBase):
    """
    Provide a user data
    """
    pass #pylint: disable=unnecessary-pass


class UsersInDB(UsersInDBBase):
    """Store hashed password through this property"""
    Password: str
