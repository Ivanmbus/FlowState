# app/main.py
from fastapi import FastAPI
from app.api.v1 import routes_users

app = FastAPI(title="Flow State API")

app.include_router(routes_users.router, prefix="/api/v1")