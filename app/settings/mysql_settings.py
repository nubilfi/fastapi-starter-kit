"""
MySQL database settings
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import set_dotenv

set_dotenv()

if getenv('APP_MODE') == 'TESTING':
    # modify the following connection string
    SQLALCHEMY_DATABASE_URL = "mysql://root:1234@172.17.0.1/mytest"
else:
    # pylint: disable=line-too-long
    SQLALCHEMY_DATABASE_URL = f"mysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
    # pylint: enable=line-too-long

# pylint: disable=invalid-name
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# pylint: enable=invalid-name
