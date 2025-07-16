# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id:int
    email:EmailStr
    password:str
    class config:
        from_attribute=True
