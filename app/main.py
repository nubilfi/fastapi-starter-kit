"""
A file for the imported lib
Access it through `module_name.variable`
"""
from fastapi import FastAPI

app: FastAPI = FastAPI(
    redoc_url=None,
    title="REST API Starter Kit",
    description="This is a very basic starter kit with some basic endpoints",
    version="1.0.0"
)
