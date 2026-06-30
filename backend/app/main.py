# app/main.py
from fastapi import FastAPI
from app.api.v1 import routes_users

app = FastAPI(title="Flow State API")

app.include_router(routes_users.router, prefix="/api/v1")
app.include_router(routes_users.router, prefix="/api/v1/users")
app.include_router(routes_users.router, prefix="/api/v1/auth")
app.include_router(routes_users.router, prefix="/api/v1/tracks")