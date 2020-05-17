"""
It is a Pydantic model for Token
"""
from pydantic import BaseModel


class Token(BaseModel):
    """
    A schema class used to represent token data for application
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    A schema class used to represent user credential
    """
    Username: str = None
