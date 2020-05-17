"""
Testing /cars endpoint
"""
from os import getenv
from random import randint
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.cars_utils import create_random_car
from app.tests.utils.utils import random_lower_string


def test_get_all_cars(
        client_target: TestClient,
        user_token_headers: Dict[str, str]
):
    """should return a list of all cards record"""
    res = client_target.get(f"{getenv('API_PREFIX')}/cars", headers=user_token_headers)
    cars = res.json()

    assert res.status_code == 200
    assert cars


def test_get_car_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """should return a single list of car record"""
    item = create_random_car(sql_session)
    res = client_target.get(f"{getenv('API_PREFIX')}/cars/{item.Id}", headers=user_token_headers)

    assert res.status_code == 200
    car = res.json()
    assert car["Id"] == item.Id
    assert car["Name"] == item.Name
    assert car["Price"] == item.Price


def test_add_new_car(
        client_target: TestClient,
        user_token_headers: Dict[str, str]
):
    """create a new car record"""
    data = {"Name": "Foo", "Price": 9999}
    res = client_target.post(f"{getenv('API_PREFIX')}/cars/", headers=user_token_headers, json=data)

    assert res.status_code == 201
    car = res.json()
    assert car["Name"] == data["Name"]
    assert car["Price"] == data["Price"]


def test_update_car(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """update a car record"""
    item = create_random_car(sql_session)
    updated_data = {"Name": random_lower_string(), "Price": randint(0, 9) * 4}
    res = client_target.put(
        f"{getenv('API_PREFIX')}/cars/{item.Id}",
        headers=user_token_headers,
        json=updated_data
    )

    assert res.status_code == 200
    new_car = res.json()
    assert new_car["Name"] == updated_data["Name"]
    assert new_car["Price"] == updated_data["Price"]

def test_delete_car_by_id(
        client_target: TestClient,
        user_token_headers: Dict[str, str],
        sql_session: Session
):
    """delete a specific car record"""
    item = create_random_car(sql_session)
    res = client_target.delete(f"{getenv('API_PREFIX')}/cars/{item.Id}", headers=user_token_headers)

    assert res.status_code == 204
