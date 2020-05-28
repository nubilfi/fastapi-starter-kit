"""
Provide logic for /authors endpoint
"""
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.schemas.authors_schema import AuthorsCreate, AuthorsUpdate
from app.models.authors_model import Authors


def get_authors(sql: Session):
    """return authors record"""
    return sql.query(Authors).all()


def get_author(sql: Session, author_id: int):
    """return a specific author record"""
    return sql.query(Authors).filter(Authors.AuthorId == author_id).first()


def create_author(sql: Session, author: AuthorsCreate):
    """
    Create a record of author with its Name
    """
    new_author = Authors(
        Name=author.Name,
    )
    sql.add(new_author)
    sql.commit()
    sql.refresh(new_author)
    return new_author


def update_author(sql: Session, author_id: int, author: AuthorsUpdate):
    """
    Update a specific author
    """
    old_data = sql.query(Authors).filter(Authors.AuthorId == author_id).first()

    if old_data is not None:
        new_data = author.dict()
        old_data.Name = new_data["Name"]

        sql.commit()

    return old_data


def delete_author(sql: Session, author_id: int):
    """Delete a specific author"""
    old_data = sql.query(Authors).filter(Authors.AuthorId == author_id).first()

    if old_data:
        sql.query(Authors).filter(Authors.AuthorId == author_id).delete(
            synchronize_session='evaluate')
        sql.commit()
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"Author with Id: {author_id} cannot be found."}
        )

    return JSONResponse(
        status_code=204,
        content={
            "message": f"Author with id: {author_id} has been successfully deleted."}
    )
