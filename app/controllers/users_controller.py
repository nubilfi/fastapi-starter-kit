"""
Provide logic for /users endpoint
"""
from sqlalchemy.orm import Session

from app.schemas.users_schema import UsersCreate, UsersUpdate
from app.models.users_model import Users
from app.utils import auth


def get_users(sql: Session):
    """return users record"""
    return sql.query(Users).all()


def get_user(sql: Session, user_id: int):
    """return a specific user record"""
    return sql.query(Users).filter(Users.UserId == user_id).first()


def check_user(sql: Session, username: str):
    """return a user data"""
    user = sql.query(Users).filter(Users.Username == username).first()
    return user


def create_user(sql: Session, user: UsersCreate):
    """
    Create a record of user with its Username and Password
    Password will be hashed
    """
    new_user = Users(
        Username=user.Username,
        Password=auth.get_password_hash(user.Password)
    )
    sql.add(new_user)
    sql.commit()
    sql.refresh(new_user)
    return new_user


def update_user(sql: Session, user_id: int, user: UsersUpdate):
    """
    Update a specific user data
    """
    old_data = sql.query(Users).filter(Users.UserId == user_id).first()

    if old_data is not None:
        new_data = user.dict()
        old_data.Fullname = new_data["Fullname"]
        old_data.Email = new_data["Email"]
        old_data.Password = auth.get_password_hash(new_data["Password"])
        old_data.Status = new_data["Status"]

        sql.commit()

    return old_data
