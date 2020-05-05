"""
Testing basic route
"""
from fastapi.testclient import TestClient

from app.server import app


client = TestClient(app)


def test_read_root():
    """test root / endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_item():
    """test /items/{item_id} endpoint"""
    response = client.get("/items/3")

    assert response.status_code == 200
    assert response.json() == {"item_id": 3, "query": None}
