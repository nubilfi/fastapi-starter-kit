"""
It is a Pydantic model for Message
"""
from pydantic import BaseModel


class Message(BaseModel):
    """
    A schema class used to represent message feedback to user
    """
    message: str
