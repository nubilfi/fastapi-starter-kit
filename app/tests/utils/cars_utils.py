"""test cars util functions"""
from random import randint

from sqlalchemy.orm import Session
from app.controllers.cars_controller import create_car
from app.schemas.cars_schema import CarsBase
from app.models.cars_model import Cars
from app.tests.utils.utils import random_lower_string


def create_random_car(sql: Session) -> Cars:
    """create a random car values"""
    name = random_lower_string()
    price = randint(0, 9) * 99

    car_in = CarsBase(Name=name, Price=price)
    return create_car(sql, car=car_in)
