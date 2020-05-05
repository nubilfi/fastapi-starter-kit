"""
Testing /cars endpoint
"""
from fastapi.testclient import TestClient

from app.server import app
from app.routes.cars import db_session
from app.settings.mysql_settings import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)


def override_db_session():
    """override the actual db session"""
    try:
        dbsession = SessionLocal()
        yield dbsession
    finally:
        dbsession.close()


app.dependency_overrides[db_session] = override_db_session

client = TestClient(app)

cars_data = [
    {'Id': 1,
     'Name': 'Audi',
     'Price': 52642},
    {'Id': 2,
     'Name': 'Mercedes',
     'Price': 57127},
    {'Id': 3,
     'Name': 'Skoda',
     'Price': 9000},
    {'Id': 4,
     'Name': 'Volvo',
     'Price': 29000},
    {'Id': 5,
     'Name': 'Bentley',
     'Price': 350000},
    {'Id': 6,
     'Name': 'Citroen',
     'Price': 21000},
    {'Id': 7,
     'Name': 'Hummer',
     'Price': 41400},
    {'Id': 8,
     'Name': 'Volkswagen',
     'Price': 21600},
]


# TODO: create pytest fixtures


def test_get_all_cars():
    """should return a list of all cards record"""
    response = client.get("/cars")

    assert response.status_code == 200
    assert response.json() == cars_data


def test_get_car_by_id():
    """should return a single list of car record"""
    response = client.get("/cars/1")

    assert response.status_code == 200
    assert response.json() == cars_data[0]


def test_add_new_car():
    """create a new car record"""
    response = client.post(
        "cars",
        json={"Name": "newdata", "Price": 123}
    )

    assert response.status_code == 201
    assert response.json() == {"Name": "newdata", "Price": 123}


def test_update_car():
    """update a car record"""
    response = client.put(
        "cars/8",
        json={"Name": "Updatedata", "Price": 222}
    )

    assert response.status_code == 200
    assert response.json() == {"Name": "Updatedata", "Price": 222}


def test_delete_car_by_id():
    """delete a specific car record"""
    response = client.delete("cars/8")

    assert response.status_code == 204
