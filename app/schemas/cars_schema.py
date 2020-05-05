"""
It is a Pydantic model for Cars
"""
from pydantic import BaseModel, Field


class CarsBase(BaseModel):
    """
    A schema class used to represent Cars table column values
    """
    Id: int
    Name: str
    Price: int = Field(..., gt=0,
                       description="The price must be greated than zero")

    class Config:
        """
        Instead of using id = data["id"]
        replace it with id = data.id
        """
        orm_mode = True


class CarActions(BaseModel):
    """
    A schema class used to represent column to create a new Car
    """
    Name: str
    Price: int = Field(..., gt=0,
                       description="The price must be greated than zero")

    class Config:
        """
        Instead of using name = data["Name"]
        replace it with name = data.Name
        """
        orm_mode = True
