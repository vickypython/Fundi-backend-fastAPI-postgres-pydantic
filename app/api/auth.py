from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import User,DeviceToken
from ..utils import access_token,refresh_token,get_current_user
from ..schemas import StandardResponse,UserCreate,UserLogin,DeviceTokenResponse
from ..token import hash_password,verify_password
router=APIRouter(prefix="/auth")
@router.post("/signup",response_model=StandardResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user.email).first()
    if user:
        return StandardResponse(
        status="Error",
        message="user already exists",
        data=None,
        error={
            "code":status.HTTP_400_BAD_REQUEST,
            "detail":[
                {"message":"Email already exists"}
            ]
        }

    )
    #if user doesnt exists create 
    hashed_password=hash_password(user.password)
    new_user=User(
        email=user.email,
        password=hashed_password,
        role=user.role,
        location=user.location
         )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return StandardResponse(
        status=status.HTTP_201_CREATED,
        message="user successfully created",
        data=new_user,
        error=None

    )
@router.post("/signin",response_model=StandardResponse)
#Todos
#parameters->fetch the user,check if he exists,if yeah
#check for password validity if true 
#assign an accesstoken and refresh token
#save refreshtoken to db and access token send to client 
#with the response object
#i need db,user model
def sign_in(user:UserLogin,db:Session=Depends(get_db)):
    user_in_db=db.query(User).filter(User.email==user.email).first()
    if not user or not verify_password(user.password,user_in_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user or incorrect password",
            headers=None
        )
    expire_date=timedelta(days=2.1)
    user_access_token=access_token(data={"sub":user_in_db.id},expire_delta=expire_date)
    user_refresh_token=refresh_token(data={"sub":user_in_db.id})
    db.add()
    db.commit()
    
    return StandardResponse(
        status="success",
        message="log in succesfully",
        data={
            "access_token":user_access_token,
            "refresh_token":user_refresh_token

        }
    )
#to log out
#what need to happen?
#clear the token,where is it stored
@router.delete("/logout")
def log_out(token_clear:DeviceTokenResponse,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==token_clear.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='failed to log out'
        )
    db_token=db.query(DeviceToken).filter(DeviceToken.token==token_clear.token)
    if db_token:
        token_clear.token=None
    db.commit()
    return StandardResponse(
        status="success",
        message="log out succesfully",
        data={
            "access_token":None,
            "refresh_token":None

        })
    
