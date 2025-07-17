# app/main.py
from fastapi import FastAPI,webSocket,webSocketDisconnect
from app.routers import users


app = FastAPI()

# Register route
app.include_router(users.router)


