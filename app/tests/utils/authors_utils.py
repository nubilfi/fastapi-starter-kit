"""test authors util functions"""
from sqlalchemy.orm import Session
from app.controllers.authors_controller import create_author
from app.schemas.authors_schema import AuthorsBase
from app.models.authors_model import Authors
from app.tests.utils.utils import random_lower_string


def create_random_author(sql: Session) -> Authors:
    """create a random author values"""
    name = random_lower_string()

    author_in = AuthorsBase(Name=name)
    return create_author(sql, author=author_in)
