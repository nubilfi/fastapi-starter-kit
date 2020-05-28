"""
It is a Pydantic model for Cars
"""
from typing import Optional
from pydantic import BaseModel, Field


class CarsBase(BaseModel):
    """
    A schema class used to represent Cars table column values
    """
    Name: str = None
    Price: int = None

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class CarsCreate(CarsBase):
    """
    A schema class used to represent column to create a new Car
    """
    Name: str
    Price: int = Field(..., gt=0,
                       description="The price must be greated than zero")

    class Config:
        """enable orm mode"""
        orm_mode = True


class CarsUpdate(CarsBase):
    """
    A schema class used to represent column to create a new Car
    """
    Name: Optional[str]
    Price: Optional[int]

    class Config:
        """enable orm mode"""
        orm_mode = True


class CarsInDBBase(CarsBase):
    """
    A schema class used to represent car data based on its ID
    """
    Id: Optional[int] = None

    class Config:
        """enable orm mode"""
        orm_mode = True
