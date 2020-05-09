"""
Basic endpoint: /users
"""
from typing import Generator

from fastapi import APIRouter, Depends

from app.routes.api_v1.endpoints.signin import get_current_active_user
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


@router.get("/me/", response_model=UsersBase, response_model_exclude_unset=True)
async def read_users_me(current_user: UsersBase = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: UsersBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.Username}]


# @router.get('/users', response_model=List[UsersBase])
# def get_all_users(sql: Session = Depends(db_session)):
#     """return users record"""
#     result = check_users(sql)
#     return result
