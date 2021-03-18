"""test signin util functions"""
from sqlalchemy.orm import Session
from app.controllers.users_controller import check_user


def get_user_test(sql: Session, username: str):
    """get user test data"""
    return check_user(sql, username=username)
