# app/routes/user.py
from fastapi import APIRouter
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate):
    return {"msg": f"User {user.username} created!"}

@router.get("/")
def list_users():
    return [{"username": "john"}, {"username": "jane"}]