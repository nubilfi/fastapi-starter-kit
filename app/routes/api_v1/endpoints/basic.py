"""
Basic endpoint: /
"""
from fastapi import APIRouter

#pylint: disable=invalid-name
router = APIRouter()
#pylint: enable=invalid-name

@router.get('/')
def read_root():
    """return basic value"""
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, query: str = None):
    """return param and querystring value"""
    return {"item_id": item_id, "query": query}
