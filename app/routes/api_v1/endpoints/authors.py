"""
Basic endpoint: /authors
"""
from typing import List, Generator
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from app.controllers.authors_controller import (
    get_authors, get_author, create_author, update_author, delete_author)
from app.schemas.authors_schema import AuthorsInDBBase, AuthorsCreate, AuthorsUpdate
from app.schemas.users_schema import UsersBase
from app.settings.mysql_settings import SessionLocal
from app.utils.auth import get_current_active_user

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name


def db_session() -> Generator:
    """
    Get database connection with DI (Dependencies Injection)
    """
    try:
        dbsession = SessionLocal()
        yield dbsession
    finally:
        dbsession.close()


@router.get("/", response_model=List[AuthorsInDBBase])
def get_all_authors(
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """return authors record"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = get_authors(sql)
    return result


@router.get("/{author_id}", response_model=AuthorsInDBBase)
def get_author_by_id(
        author_id: int = Path(..., title="The Id of the author to get", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """return a specific author record"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = get_author(sql, author_id=author_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return result


@router.post("/", response_model=AuthorsCreate, status_code=HTTP_201_CREATED)
def add_new_author(
        newauthor: AuthorsCreate,
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """
    Create a author with all the information:

    - **name**: must have a name
    """
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = create_author(sql, author=newauthor)
    return result


@router.put("/{author_id}", response_model=AuthorsUpdate)
def update_author_by_id(
        author: AuthorsUpdate,
        author_id: int = Path(...,
                              title="The Id of the author to be updated", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """
    update a author with all the information:

    - **id**: set the Id of the author, it's required
    - **name**: must have a name
    """
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = update_author(sql, author_id=author_id, author=author)

    if result is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return result


@router.delete("/{author_id}")
def delete_author_by_id(
        author_id: int = Path(...,
                              title="The Id of the author to be deleted", ge=0),
        sql: Session = Depends(db_session),
        current_user: UsersBase = Depends(get_current_active_user)
):
    """delete a specific author"""
    if current_user.Status:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = delete_author(sql, author_id=author_id)
    return result
