"""
Cars database model
"""
from sqlalchemy import Column
from sqlalchemy.dialects import mysql

from app.settings.mysql_settings import Base


class Cars(Base):
    """
    A class used to represent Cars table
    """
    __tablename__ = "Cars"

    Id = Column(mysql.INTEGER, primary_key=True,
                index=True, autoincrement=True)
    Name = Column(mysql.VARCHAR(150))
    Price = Column(mysql.INTEGER)
