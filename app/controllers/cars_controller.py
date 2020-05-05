"""
Provide logic for /cars endpoint
"""
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.schemas.cars_schema import CarActions
from app.models.cars_model import Cars


def get_cars(sql: Session):
    """return cars record"""
    return sql.query(Cars).all()


def get_car(sql: Session, car_id: int):
    """return a specific car record"""
    return sql.query(Cars).filter(Cars.Id == car_id).first()


def create_car(sql: Session, car: CarActions):
    """
    Create a record of car with its Name & Price
    """
    new_car = Cars(
        Name=car.Name,
        Price=car.Price
    )
    sql.add(new_car)
    sql.commit()
    sql.refresh(new_car)
    return new_car


def update_car(sql: Session, car_id: int, car: CarActions):
    """
    Update a specific car
    """
    old_data = sql.query(Cars).filter(Cars.Id == car_id).first()

    if old_data is not None:
        new_data = car.dict()
        old_data.Name = new_data["Name"]
        old_data.Price = new_data["Price"]

        sql.commit()

    return old_data


def delete_car(sql: Session, car_id: int):
    """Delete a specific car"""
    old_data = sql.query(Cars).filter(Cars.Id == car_id).first()

    if old_data:
        sql.query(Cars).filter(Cars.Id == car_id).delete(
            synchronize_session='evaluate')
        sql.commit()
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"Car with Id: {car_id} cannot be found."}
        )

    return JSONResponse(
        status_code=204,
        content={
            "message": f"Car with id: {car_id} has been successfully deleted."}
    )
