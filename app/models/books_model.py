"""
Books database model
"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql

from app.settings.mysql_settings import Base
from .authors_model import Authors


class Books(Base):
    """
    A class used to represent Books table
    """
    __tablename__ = "Books"

    BookId = Column(mysql.INTEGER, primary_key=True,
                    index=True, autoincrement=True)
    Title = Column(mysql.TEXT)
    AuthorId = Column(mysql.INTEGER, ForeignKey(
        Authors.AuthorId), nullable=False)

    author = relationship("Authors", back_populates="book")
