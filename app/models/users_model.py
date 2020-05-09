"""
Users database model
"""
from sqlalchemy import Column
from sqlalchemy.dialects import mysql


from app.settings.mysql_settings import Base


class Users(Base):
    """
    A class used to represent Users table
    """
    __tablename__ = "Users"

    UserId = Column(mysql.INTEGER, primary_key=True,
                    index=True, autoincrement=True)
    Username = Column(mysql.VARCHAR(32))
    Fullname = Column(mysql.VARCHAR(150))
    Email = Column(mysql.TEXT)
    Password = Column(mysql.VARCHAR(32))
    Status = Column(mysql.BOOLEAN, default=False)
