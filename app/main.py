# app/main.py
from fastapi import FastAPI
from app.routers import users

app = FastAPI()

# Register route
app.include_router(users.router)
