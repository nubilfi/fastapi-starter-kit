"""
Authors database model
"""
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql

from app.settings.mysql_settings import Base


class Authors(Base):
    """
    A class used to represent Authors table
    """
    __tablename__ = "Authors"

    AuthorId = Column(mysql.INTEGER, primary_key=True,
                      index=True, autoincrement=True)
    Name = Column(mysql.VARCHAR(150))

    book = relationship("Books", back_populates="author")
