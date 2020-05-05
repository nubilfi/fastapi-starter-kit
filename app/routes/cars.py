"""
Basic endpoint: /cars
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from app.controllers.cars_controller import get_cars, get_car, create_car, update_car, delete_car
from app.schemas.cars_schema import CarsBase, CarActions
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


@router.get('/cars', response_model=List[CarsBase])
def get_all_cars(sql: Session = Depends(db_session)):
    """return cars record"""
    result = get_cars(sql)
    return result


@router.get("/cars/{car_id}", response_model=CarsBase)
def get_car_by_id(
        car_id: int = Path(..., title="The Id of the car to get", ge=0),
        sql: Session = Depends(db_session)
):
    """return a specific car record"""
    result = get_car(sql, car_id=car_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return result


@router.post("/cars", response_model=CarActions, status_code=HTTP_201_CREATED)
def add_new_car(newcar: CarActions, sql: Session = Depends(db_session)):
    """
    Create a car with all the information:

    - **name**: must have a name
    - **price**: required
    """
    result = create_car(sql, car=newcar)
    return result


@router.put("/cars/{car_id}", response_model=CarActions)
def update_car_by_id(
        car: CarActions,
        car_id: int = Path(..., title="The Id of the car to be updated", ge=0),
        sql: Session = Depends(db_session)
):
    """
    update a car with all the information:

    - **id**: set the Id of the car, it's required
    - **name**: must have a name
    - **price**: required
    """
    result = update_car(sql, car_id=car_id, car=car)

    if result is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return result


@router.delete("/cars/{car_id}")
def delete_car_by_id(
        car_id: int = Path(..., title="The Id of the car to be deleted", ge=0),
        sql: Session = Depends(db_session)
):
    """delete a specific car"""
    result = delete_car(sql, car_id=car_id)

    return result
