"""
Router list
"""
from fastapi import APIRouter

from app.routes.api_v1.endpoints import (
    basic, signin, authors, books, cars, users
)

routers = APIRouter()

routers.include_router(signin.router, tags=["Signin"])
routers.include_router(basic.router, tags=["Basic"])
routers.include_router(authors.router, prefix="/cars", tags=["Cars"])
routers.include_router(books.router, prefix="/authors", tags=["Authors"])
routers.include_router(cars.router, prefix="/books", tags=["Books"])
routers.include_router(users.router, prefix="/users", tags=["Users"])
