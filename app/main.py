"""
Main app setup project details
"""
from os import getenv
from fastapi import FastAPI

from app.config import set_dotenv

set_dotenv()

app: FastAPI = FastAPI(
    redoc_url=None,
    openapi_url=f"{getenv('API_PREFIX')}/openapi.json",
    title="REST API Starter Kit",
    description="This is a very basic starter kit with some basic endpoints",
    version="1.0.0"
)
