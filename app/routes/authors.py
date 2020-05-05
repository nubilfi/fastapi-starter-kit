"""
Basic endpoint: /authors
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from app.controllers.authors_controller import (
    get_authors, get_author, create_author, update_author, delete_author)
from app.schemas.authors_schema import AuthorsBase, AuthorsAction
from app.settings.mysql_settings import SessionLocal

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name


def db_session():
    """
    Get database connection with DI (Dependencies Injection)
    """
    try:
        dbsession = SessionLocal()
        yield dbsession
    finally:
        dbsession.close()


@router.get('/authors', response_model=List[AuthorsBase])
def get_all_authors(sql: Session = Depends(db_session)):
    """return authors record"""
    result = get_authors(sql)
    return result


@router.get("/authors/{author_id}", response_model=AuthorsBase)
def get_author_by_id(
        author_id: int = Path(..., title="The Id of the author to get", ge=0),
        sql: Session = Depends(db_session)
):
    """return a specific author record"""
    result = get_author(sql, author_id=author_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return result


@router.post("/authors", response_model=AuthorsAction, status_code=HTTP_201_CREATED)
def add_new_author(newauthor: AuthorsAction, sql: Session = Depends(db_session)):
    """
    Create a author with all the information:

    - **name**: must have a name
    """
    result = create_author(sql, author=newauthor)
    return result


@router.put("/authors/{author_id}", response_model=AuthorsAction)
def update_author_by_id(
        author: AuthorsAction,
        author_id: int = Path(...,
                              title="The Id of the author to be updated", ge=0),
        sql: Session = Depends(db_session)
):
    """
    update a author with all the information:

    - **id**: set the Id of the author, it's required
    - **name**: must have a name
    """
    result = update_author(sql, author_id=author_id, author=author)

    if result is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return result


@router.delete("/authors/{author_id}")
def delete_author_by_id(
        author_id: int = Path(...,
                              title="The Id of the author to be deleted", ge=0),
        sql: Session = Depends(db_session)
):
    """delete a specific author"""
    result = delete_author(sql, author_id=author_id)

    return result
