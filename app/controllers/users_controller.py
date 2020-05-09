"""
Provide logic for /users endpoint
"""
from sqlalchemy.orm import Session

from app.schemas.users_schema import UsersAction
from app.models.users_model import Users


def get_users(sql: Session):
    """return users record"""
    return sql.query(Users).all()


def get_user(sql: Session, user_id: int):
    """return a specific user record"""
    return sql.query(Users).filter(Users.UserId == user_id).first()


def login_user(sql: Session, username: str):
    """return a user data"""
    user = sql.query(Users).filter(Users.Username == username).first()
    return user


def create_user(sql: Session, user: UsersAction):
    """
    Create a record of user with its Username, Email, Password
    Password will be hashed
    """
    new_user = Users(
        Username=user.Name,
        Email=user.Email,
        Password=user.Password
    )
    sql.add(new_user)
    sql.commit()
    sql.refresh(new_user)
    return new_user
