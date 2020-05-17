"""
Basic endpoint: /users
"""
from typing import Generator

from fastapi import APIRouter, Depends

from app.utils.auth import get_current_active_user
from app.schemas.users_schema import UsersBase
from app.settings.mysql_settings import SessionLocal

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


@router.get("/profile/", response_model=UsersBase, response_model_exclude_unset=True)
def read_users_me(current_user: UsersBase = Depends(get_current_active_user)):
    """retrieve signed user data"""
    return current_user


@router.get("/profile/items/")
def read_own_items(current_user: UsersBase = Depends(get_current_active_user)):
    """return misc item"""
    return [{"item_id": "Foo", "owner": current_user.Username}]


# @router.get('/users', response_model=List[UsersBase])
# def get_all_users(sql: Session = Depends(db_session)):
#     """return users record"""
#     result = check_users(sql)
#     return result
