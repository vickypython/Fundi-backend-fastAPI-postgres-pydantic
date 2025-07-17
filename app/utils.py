from fastapi import status,Depends,HTTPException
import jwt
from jwt import PyJWTError
from datetime import datetime,timedelta
from typing import List,Optional
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .database import get_db
from pydantic import BaseModel
from .schemas import StandardResponse
from .models import User

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl='login',
    description="log in to your Fundi app account to access the APIs"
)




class TokenData(BaseModel):
    email:Optional[str]=None
    id:Optional[str]=None

#you need an id,secret key and algorithm and expiresIn:'24h'
def access_token(data:dict,expire_delta:Optional[timedelta]=None):
    encode_data=data.copy()
    if expire_delta:
        expires=datetime.now()+expire_delta 
    else:
        expires=datetime.now()+timedelta(days=7)
    encode_data.update({'expires':expires})
    encoded_jwt=jwt.encode(encode_data,settings.Secret_key,algorithm['HS256'])
    return encoded_jwt
def refresh_token(data:dict):
    encode_data=data.copy()
    expires=datetime.now()+timedelta(days=setting.Refresh_token_expires_days)
    encode_data.update({"expires":expires})
    encoded_jwt=jwt.encode(encode_data,settings.Secret_key,algorithm=settings.ALGORITHM)
    return encoded_jwt
#already log in so we will fetch db to get and return also we need to decode the jwt
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    creditial_exception=HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
        detail=StandardResponse(
            status="error",
            message="Could not validate credentials",
            data=None,
            error={
                "code": status.HTTP_401_UNAUTHORIZED,
                "details": [{"message": "Invalid or expired token"}]
            }
        ).model_dump()
    )
    try:

        payload=jwt.decode(token,settings.Secret_key,algorithm=settings.ALGORTHM)
        user_id:str=payload.get("sub")
        if user_id is None:
            raise creditial_exception
        else:
           token_data=TokenData(id=user_id)
    except PyJWTError:
        raise creditial_exception
    user=db.query(User).filter(User.id==token_data.id).first()
    if user is None:
        raise creditial_exception
    else:
        return user
    
    
