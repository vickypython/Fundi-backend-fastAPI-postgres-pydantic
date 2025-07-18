from passlib.context import CryptContext
from sqlalchemy.orm import Session
import random
from jose import jwt,JWTError as PyJWTError
from .database import get_db
from .models import User
password_context=CryptContext(schemes=['bcrypt'],deprecated="auto")
def generate_code():
    return f"{random.randint(1000,9999)}"
def hash_password(password:str):
    return password_context.hash(password)
def verify_password(hashed_password:str,plain_password:str):
    return password_context.verify(hashed_password,plain_password)
def get_user_from_token(token:str,db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,settings.Secret_key,algorithm=settings.ALGORITHM)
        user_id=payload.get("sub")
        if user_id is None:
         return None
        user=db.query(User).filter(User.id==user_id).first()
        return user
    except PyJWTError:
        return None