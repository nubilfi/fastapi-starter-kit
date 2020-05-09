"""
It is a Pydantic model for Token
"""
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    Username: str = None
